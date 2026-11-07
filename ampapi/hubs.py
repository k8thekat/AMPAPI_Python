"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMPAPI_Python.

AMPAPI_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMPAPI_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMPAPI_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
from collections import deque
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Optional, overload

from aiohttp import ClientError, WSMsgType

from .errors import AMPAPIHubError, AMPAPIRequestError
from .objects import (
    AMPObject,
    ConsoleLine,
    LifecycleEvent,
    NetworkStatus,
    RunningTask,
    ScheduleExecution,
    ShardMetrics,
    ShardMigration,
    ShardPlayer,
    ShardSnapshots,
    ShardStatus,
    SpirePresence,
    SpireStatus,
)
from .shards import ShardModule
from .spires import SpireModule

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiohttp import ClientWebSocketResponse

    from .session import Session
    from .shards import Shard
    from .spires import Spire

__all__ = (
    "HubConnection",
    "HubEvent",
    "HubModule",
)

LOGGER: logging.Logger = logging.getLogger(__name__)

# Every SignalR JSON frame ends with this record separator, and one WebSocket message can hold several frames.
RECORD_SEPARATOR: str = "\x1e"

# The events a listener can ask for, by the library's short name.
type HubEvent = Literal[
    "console",
    "state",
    "lifecycle",
    "metrics",
    "players",
    "player_joined",
    "player_left",
    "migration",
    "snapshot",
    "schedule_run",
    "spire_state",
    "spire_presence",
    "network_status",
    "task",
]
# The events from `/hubs/shard`, which `Shard.listen` takes.
type ShardEvent = Literal[
    "console",
    "state",
    "lifecycle",
    "metrics",
    "players",
    "player_joined",
    "player_left",
    "migration",
    "snapshot",
    "schedule_run",
]
# The events about one spire, which `Spire.listen` takes.
type SpireEvent = Literal["spire_state", "spire_presence"]
type ShardHandler[P] = Callable[[Shard, P], Awaitable[None]]
type SpireHandler[P] = Callable[[Spire, P], Awaitable[None]]
type PlainHandler[P] = Callable[[P], Awaitable[None]]

# Each `/hubs/shard` target: our name for it, the argument that holds the payload, the object it becomes, and the
# argument that holds its shard ID. `None` takes the socket's shard: `ConsoleLine` names none, and `Lifecycle` keeps
# to its shard's room. `ShardStateChanged` reaches every shard socket, so it can only go by its own shard ID.
SHARD_TARGETS: dict[str, tuple[ShardEvent, int, type[AMPObject], Optional[int]]] = {
    "ConsoleLine": ("console", 0, ConsoleLine, None),
    "Lifecycle": ("lifecycle", 0, LifecycleEvent, None),
    "Metrics": ("metrics", 1, ShardMetrics, 0),
    "Migration": ("migration", 1, ShardMigration, 0),
    "ScheduleRun": ("schedule_run", 1, ScheduleExecution, 0),
    "ShardStateChanged": ("state", 2, ShardStatus, 1),
    "Snapshot": ("snapshot", 1, ShardSnapshots, 0),
    "UserJoined": ("player_joined", 1, ShardPlayer, 0),
    "UserLeft": ("player_left", 1, ShardPlayer, 0),
    "UserRoster": ("players", 1, ShardPlayer, 0),
}
SHARD_EVENTS: frozenset[str] = frozenset(event for event, _index, _kind, _shard_index in SHARD_TARGETS.values())
SPIRE_EVENTS: frozenset[str] = frozenset(("spire_state", "spire_presence", "network_status"))


class HubConnection:
    """One WebSocket to one of AMP's SignalR hubs, kept open until :meth:`stop` or a logout.

    Each connect gets a fresh 60 second hub token from the :class:`Session`, does the JSON protocol handshake and sends
    every join again. A dropped socket, or one with no frame for 45 seconds (the server pings every 15), is connected
    again after 1, 2, 4, 8 and then every 8 seconds. A logout ends it instead, as does a join AMP refuses.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session whose login the hub token comes from.
    hub : :class:`str`
        The hub, ``"shard"``, ``"spire"`` or ``"tasks"``.
    joins : list[tuple[:class:`str`, list[Any]]]
        The joins to send on each connect, eg. ``[("JoinShard", [tenant_id, shard_id])]``.
    on_event : Callable[[:class:`HubConnection`, :class:`str`, list[Any]], None]
        Called with each event's target and arguments, from the read loop, so it must not block.
    shard_id : Union[:class:`str`, None], optional
        The shard a `/hubs/shard` connection is for, by default None. AMP's console lines don't name their shard.

    """

    # The delays before each try to connect again; past the end, the last one repeats.
    _reconnect_delays: ClassVar[tuple[int, ...]] = (1, 2, 4, 8, 8)
    _silence_limit: ClassVar[float] = 45.0
    _invoke_timeout: ClassVar[float] = 15.0

    def __init__(  # noqa: D107
        self,
        session: Session,
        hub: str,
        *,
        joins: list[tuple[str, list[Any]]],
        on_event: Callable[[HubConnection, str, list[Any]], None],
        shard_id: Optional[str] = None,
    ) -> None:
        self.session: Session = session
        self.hub: str = hub
        self.joins: list[tuple[str, list[Any]]] = joins
        self.shard_id: Optional[str] = shard_id
        self._on_event: Callable[[HubConnection, str, list[Any]], None] = on_event
        self._socket: Optional[ClientWebSocketResponse] = None
        self._reader: Optional[asyncio.Task[None]] = None
        self._runner: Optional[asyncio.Task[None]] = None
        self._pending: dict[str, asyncio.Future[Any]] = {}
        self._invocations: int = 0
        self._stopping: bool = False

    def __repr__(self) -> str:  # noqa: D105
        return f"<HubConnection hub={self.hub!r} shard_id={self.shard_id!r} running={self.running}>"

    @property
    def _ended(self) -> bool:
        """If :meth:`stop` was called or the session logged out, so the connection shouldn't open again."""
        return self._stopping is True or self.session.logged_in is False

    @property
    def running(self) -> bool:
        """If the connection is up, or waiting to connect again."""
        return self._runner is not None and not self._runner.done()

    @property
    def url(self) -> str:
        """The hub's WebSocket address, ``wss://`` for a panel on HTTPS."""
        scheme: str = "wss" if self.session.url.startswith("https://") else "ws"
        return f"{scheme}{self.session.url[self.session.url.index('://') :]}/hubs/{self.hub}"

    async def invoke(self, target: str, arguments: list[Any]) -> Any:
        """Call a hub method and wait for its completion.

        |coro|

        Parameters
        ----------
        target : :class:`str`
            The method, eg. ``"JoinShard"``.
        arguments : list[Any]
            Its arguments.

        Returns
        -------
        Any
            The method's `result`.

        Raises
        ------
        AMPAPIHubError
            If AMP couldn't run the call, eg. a method it doesn't have.
        ConnectionError
            If the connection isn't open, or closes before the reply.
        TimeoutError
            If no reply comes within 15 seconds.

        """
        if self._socket is None or self._socket.closed:
            msg = f"The {self.hub} hub isn't connected."
            raise ConnectionError(msg)

        self._invocations += 1
        invocation_id: str = str(self._invocations)
        reply: asyncio.Future[Any] = asyncio.get_running_loop().create_future()
        self._pending[invocation_id] = reply

        frame: dict[str, Any] = {"type": 1, "invocationId": invocation_id, "target": target, "arguments": arguments}
        await self._socket.send_str(json.dumps(frame) + RECORD_SEPARATOR)
        try:
            return await asyncio.wait_for(reply, timeout=self._invoke_timeout)
        finally:
            self._pending.pop(invocation_id, None)

    async def start(self) -> None:
        """Connect, join, and keep the connection up in the background until :meth:`stop`.

        |coro|

        Raises
        ------
        AMPAPIHubError
            If AMP refuses the handshake or a join, eg. ``"shards.error.notFound"``.
        aiohttp.ClientError
            If the first connect fails, eg. a 401 for the hub token.

        """
        self._stopping = False
        await self._connect()
        self._runner = asyncio.create_task(self._run(), name=f"ampapi hub {self.hub} {self.shard_id or ''}")

    async def stop(self) -> None:
        """Close the connection, saying goodbye to the hub first.

        |coro|

        """
        self._stopping = True
        if self._socket is not None and not self._socket.closed:
            with contextlib.suppress(ClientError, ConnectionError):
                await self._socket.send_str(json.dumps({"type": 7}) + RECORD_SEPARATOR)

            await self._socket.close()

        for task in (self._runner, self._reader):
            if task is not None and not task.done():
                task.cancel()

        await asyncio.gather(*(task for task in (self._runner, self._reader) if task is not None), return_exceptions=True)

    async def _connect(self) -> None:
        """Open the socket with a fresh hub token, do the handshake, start reading and send each join."""
        token: str = (await self.session.get_hub_token())["token"]
        # `get_hub_token` has just made sure the aiohttp session exists.
        client = self.session._session  # pyright: ignore[reportPrivateUsage]
        if client is None:
            msg = "The session has no aiohttp session to open a hub on."
            raise ConnectionError(msg)

        LOGGER.debug("<%s.%s> | Connecting | Hub: %s | Shard ID: %s", __class__.__name__, "_connect", self.hub, self.shard_id)
        self._socket = await client.ws_connect(self.url, params={"access_token": token}, heartbeat=None)
        await self._socket.send_str(json.dumps({"protocol": "json", "version": 1}) + RECORD_SEPARATOR)
        handshake = await self._socket.receive(timeout=self._silence_limit)
        if handshake.type is not WSMsgType.TEXT:
            msg = f"The {self.hub} hub closed before its handshake reply."
            raise ConnectionError(msg)

        # The reply is `{}`, or `{error}` when AMP refuses the protocol; other frames can follow it in the message.
        frames: list[str] = [part for part in str(handshake.data).split(RECORD_SEPARATOR) if part]
        first: Any = json.loads(frames[0]) if frames else {}
        if isinstance(first, dict) and first.get("error"):  # pyright: ignore[reportUnknownMemberType]
            raise AMPAPIHubError(hub=self.hub, target="handshake", error=first.get("error"))  # pyright: ignore[reportUnknownMemberType]

        self._reader = asyncio.create_task(self._read(socket=self._socket), name=f"ampapi hub reader {self.hub}")
        for part in frames[1:]:
            self._handle(frame=json.loads(part))

        for target, arguments in self.joins:
            result: Any = await self.invoke(target=target, arguments=arguments)
            if isinstance(result, dict) and result.get("error") is not None:  # pyright: ignore[reportUnknownMemberType]
                await self._socket.close()
                raise AMPAPIHubError(hub=self.hub, target=target, error=result.get("error"))  # pyright: ignore[reportUnknownMemberType]

        LOGGER.info("<%s.%s> | Connected | Hub: %s | Shard ID: %s", __class__.__name__, "_connect", self.hub, self.shard_id)

    async def _run(self) -> None:
        """Wait for the socket to drop, then connect again, until :meth:`stop`, a logout or a refused join."""
        attempt: int = 0
        while self._stopping is False:
            if self._reader is not None:
                await asyncio.gather(self._reader, return_exceptions=True)

            delay: int = self._reconnect_delays[min(attempt, len(self._reconnect_delays) - 1)]
            await asyncio.sleep(delay=delay)
            # A logout closes every hub socket; that ends the connection, rather than logging in again.
            if self._ended is True:
                LOGGER.info("<%s.%s> | Hub closed, the session is logged out | Hub: %s", __class__.__name__, "_run", self.hub)
                break

            attempt += 1
            try:
                await self._connect()
            except AMPAPIHubError:
                # A refused join, eg. a shard that was deleted, won't be any different next time.
                break
            except (ClientError, AMPAPIRequestError, ConnectionError, TimeoutError) as error:
                LOGGER.warning(
                    "<%s.%s> | Failed to connect again, trying in %s seconds | Hub: %s | Error: %s",
                    __class__.__name__,
                    "_run",
                    self._reconnect_delays[min(attempt, len(self._reconnect_delays) - 1)],
                    self.hub,
                    error,
                )
                self._reader = None
                continue

            attempt = 0

    async def _read(self, socket: ClientWebSocketResponse) -> None:
        """Read frames until the socket closes, AMP says goodbye, or nothing arrives for 45 seconds."""
        try:
            while True:
                message = await socket.receive(timeout=self._silence_limit)
                if message.type is not WSMsgType.TEXT:
                    LOGGER.info("<%s.%s> | Socket closed | Hub: %s | Type: %s", __class__.__name__, "_read", self.hub, message.type)
                    return

                for part in str(message.data).split(RECORD_SEPARATOR):
                    if part and self._handle(frame=json.loads(part)) is False:
                        return
        except TimeoutError:
            LOGGER.warning("<%s.%s> | No frame for %s seconds | Hub: %s", __class__.__name__, "_read", self._silence_limit, self.hub)
        finally:
            for reply in self._pending.values():
                if not reply.done():
                    reply.set_exception(ConnectionError(f"The {self.hub} hub closed."))

            if not socket.closed:
                await socket.close()

    def _handle(self, frame: dict[str, Any]) -> bool:
        """Act on one frame; `False` when AMP closed the connection (type 7). A ping (type 6) needs nothing."""
        kind: Any = frame.get("type")
        if kind == 1:
            try:
                self._on_event(self, frame.get("target", ""), frame.get("arguments", []))
            except Exception:
                LOGGER.exception("<%s.%s> | Failed to dispatch an event | Hub: %s", __class__.__name__, "_handle", self.hub)

        elif kind == 3:
            reply: Optional[asyncio.Future[Any]] = self._pending.get(str(frame.get("invocationId")))
            if reply is not None and not reply.done():
                if frame.get("error"):
                    reply.set_exception(AMPAPIHubError(hub=self.hub, target="invocation", error=frame.get("error")))
                else:
                    reply.set_result(frame.get("result"))

        elif kind == 7:
            LOGGER.info("<%s.%s> | AMP closed the hub | Hub: %s | Error: %s", __class__.__name__, "_handle", self.hub, frame.get("error"))
            return False
        return True


class _Listener:
    """One registered handler, with its own queue and worker, so it keeps its order and a slow one blocks nobody."""

    # `metrics` comes every 3 seconds per shard, so a backlog past this drops its oldest.
    metrics_backlog: ClassVar[int] = 8

    def __init__(self, handler: Callable[..., Awaitable[None]], event: HubEvent, shard_id: Optional[str], spire_id: Optional[str]) -> None:
        self.handler: Callable[..., Awaitable[None]] = handler
        self.event: HubEvent = event
        self.shard_id: Optional[str] = shard_id
        self.spire_id: Optional[str] = spire_id
        self.queue: asyncio.Queue[tuple[Any, ...]] = asyncio.Queue(maxsize=self.metrics_backlog if event == "metrics" else 0)
        self.worker: Optional[asyncio.Task[None]] = None

    def put(self, arguments: tuple[Any, ...]) -> None:
        """Queue one event's handler arguments, dropping the oldest when a `metrics` backlog is full."""
        if self.queue.full():
            self.queue.get_nowait()
        self.queue.put_nowait(arguments)


class HubModule(ShardModule, SpireModule):
    """Live events from AMP's hubs, handed to the handlers registered with :meth:`listen` or :meth:`add_listener`.

    :meth:`start_listening` lists the shards and spires, then opens one `/hubs/shard` connection per shard in scope,
    one `/hubs/spire` and one `/hubs/tasks`, as needed. A listener with no `shard` or `spire` covers everything the
    panel can see; the lists are fetched again every 5 minutes, and when an event names a shard we don't know.

    AMP sends every shard's `ShardStateChanged` to every shard socket, not only the joined shard's. So a `state` event
    goes by the shard ID it carries, to the listeners that cover that shard, and the copies the other sockets get are
    dropped by its `revision`. A console line names no shard, so it goes by its socket.

    .. versionadded:: 6.0.0

    """

    # How often the shard and spire lists are fetched again, in seconds.
    _refresh_every: ClassVar[float] = 300.0
    # How many recent state revisions per shard we remember, to drop the copies the other shard sockets get.
    _revisions_kept: ClassVar[int] = 64

    def __init__(self, session: Session) -> None:  # noqa: D107
        super().__init__(session=session)
        self._listeners: list[_Listener] = []
        self._connections: dict[str, HubConnection] = {}
        self._hub_shards: dict[str, Shard] = {}
        self._hub_spires: dict[str, Spire] = {}
        self._listening: bool = False
        self._refresher: Optional[asyncio.Task[None]] = None
        self._refresh_wanted: asyncio.Event = asyncio.Event()
        self._background: set[asyncio.Task[None]] = set()
        self._state_revisions: dict[str, deque[int]] = {}

    @property
    def listening(self) -> bool:
        """If any hub connection is up, or waiting to connect again."""
        return self._listening is True and any(connection.running for connection in self._connections.values())

    @overload
    def add_listener(self, handler: ShardHandler[ConsoleLine], event: Literal["console"], *, shard: Optional[str] = None) -> None: ...
    @overload
    def add_listener(self, handler: ShardHandler[ShardStatus], event: Literal["state"], *, shard: Optional[str] = None) -> None: ...
    @overload
    def add_listener(self, handler: ShardHandler[LifecycleEvent], event: Literal["lifecycle"], *, shard: Optional[str] = None) -> None: ...
    @overload
    def add_listener(self, handler: ShardHandler[ShardMetrics], event: Literal["metrics"], *, shard: Optional[str] = None) -> None: ...
    @overload
    def add_listener(self, handler: ShardHandler[list[ShardPlayer]], event: Literal["players"], *, shard: Optional[str] = None) -> None: ...
    @overload
    def add_listener(
        self,
        handler: ShardHandler[ShardPlayer],
        event: Literal["player_joined", "player_left"],
        *,
        shard: Optional[str] = None,
    ) -> None: ...
    @overload
    def add_listener(self, handler: ShardHandler[ShardMigration], event: Literal["migration"], *, shard: Optional[str] = None) -> None: ...
    @overload
    def add_listener(self, handler: ShardHandler[ShardSnapshots], event: Literal["snapshot"], *, shard: Optional[str] = None) -> None: ...
    @overload
    def add_listener(
        self,
        handler: ShardHandler[ScheduleExecution],
        event: Literal["schedule_run"],
        *,
        shard: Optional[str] = None,
    ) -> None: ...
    @overload
    def add_listener(self, handler: SpireHandler[SpireStatus], event: Literal["spire_state"], *, spire: Optional[str] = None) -> None: ...
    @overload
    def add_listener(
        self,
        handler: SpireHandler[SpirePresence],
        event: Literal["spire_presence"],
        *,
        spire: Optional[str] = None,
    ) -> None: ...
    @overload
    def add_listener(self, handler: PlainHandler[NetworkStatus], event: Literal["network_status"]) -> None: ...
    @overload
    def add_listener(self, handler: PlainHandler[RunningTask], event: Literal["task"]) -> None: ...
    def add_listener(
        self,
        handler: Callable[..., Awaitable[None]],
        event: HubEvent,
        *,
        shard: Optional[str] = None,
        spire: Optional[str] = None,
    ) -> None:
        """Register `handler` for `event`, for every shard or spire, or only the one named.

        The handler gets the :class:`Shard` or :class:`Spire` first, then the event's object, eg.
        ``async def on_console(shard: Shard, line: ConsoleLine)``. `network_status` and `task` handlers get the object only.
        If we're listening already, the connections it needs are opened.

        Parameters
        ----------
        handler : Callable[..., Awaitable[None]]
            The coroutine function to call.
        event : :class:`HubEvent`
            The event, eg. ``"console"``.
        shard : Union[:class:`str`, None], optional
            Only this shard's events, by default None for every shard.
        spire : Union[:class:`str`, None], optional
            Only this spire's events, by default None for every spire.

        """
        self._register(handler=handler, event=event, shard=shard, spire=spire)

    @overload
    def listen(
        self,
        event: Literal["console"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[ConsoleLine]], ShardHandler[ConsoleLine]]: ...
    @overload
    def listen(
        self,
        event: Literal["state"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[ShardStatus]], ShardHandler[ShardStatus]]: ...
    @overload
    def listen(
        self,
        event: Literal["lifecycle"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[LifecycleEvent]], ShardHandler[LifecycleEvent]]: ...
    @overload
    def listen(
        self,
        event: Literal["metrics"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[ShardMetrics]], ShardHandler[ShardMetrics]]: ...
    @overload
    def listen(
        self,
        event: Literal["players"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[list[ShardPlayer]]], ShardHandler[list[ShardPlayer]]]: ...
    @overload
    def listen(
        self,
        event: Literal["player_joined", "player_left"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[ShardPlayer]], ShardHandler[ShardPlayer]]: ...
    @overload
    def listen(
        self,
        event: Literal["migration"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[ShardMigration]], ShardHandler[ShardMigration]]: ...
    @overload
    def listen(
        self,
        event: Literal["snapshot"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[ShardSnapshots]], ShardHandler[ShardSnapshots]]: ...
    @overload
    def listen(
        self,
        event: Literal["schedule_run"],
        *,
        shard: Optional[str] = None,
    ) -> Callable[[ShardHandler[ScheduleExecution]], ShardHandler[ScheduleExecution]]: ...
    @overload
    def listen(
        self,
        event: Literal["spire_state"],
        *,
        spire: Optional[str] = None,
    ) -> Callable[[SpireHandler[SpireStatus]], SpireHandler[SpireStatus]]: ...
    @overload
    def listen(
        self,
        event: Literal["spire_presence"],
        *,
        spire: Optional[str] = None,
    ) -> Callable[[SpireHandler[SpirePresence]], SpireHandler[SpirePresence]]: ...
    @overload
    def listen(self, event: Literal["network_status"]) -> Callable[[PlainHandler[NetworkStatus]], PlainHandler[NetworkStatus]]: ...
    @overload
    def listen(self, event: Literal["task"]) -> Callable[[PlainHandler[RunningTask]], PlainHandler[RunningTask]]: ...
    def listen(
        self,
        event: HubEvent,
        *,
        shard: Optional[str] = None,
        spire: Optional[str] = None,
    ) -> Callable[[Callable[..., Awaitable[None]]], Callable[..., Awaitable[None]]]:
        """Register the decorated coroutine function for `event`, the decorator form of :meth:`add_listener`.

        eg. ``@panel.listen("console")`` above ``async def on_console(shard: Shard, line: ConsoleLine)``.

        Parameters
        ----------
        event : :class:`HubEvent`
            The event, eg. ``"console"``.
        shard : Union[:class:`str`, None], optional
            Only this shard's events, by default None for every shard.
        spire : Union[:class:`str`, None], optional
            Only this spire's events, by default None for every spire.

        Returns
        -------
        Callable
            The decorator, which hands back the function as it was.

        """

        def register(handler: Callable[..., Awaitable[None]]) -> Callable[..., Awaitable[None]]:
            self._register(handler=handler, event=event, shard=shard, spire=spire)
            return handler

        return register

    def _register(self, handler: Callable[..., Awaitable[None]], event: HubEvent, shard: Optional[str], spire: Optional[str]) -> None:
        """Keep a new listener; when we're listening already, start its worker and open what it needs."""
        listener: _Listener = _Listener(handler=handler, event=event, shard_id=shard, spire_id=spire)
        self._listeners.append(listener)
        if self._listening is True:
            self._start_worker(listener=listener)
            self._in_background(coroutine=self._sync_connections())

    def remove_listener(self, handler: Callable[..., Awaitable[None]], event: HubEvent) -> None:
        """Stop calling `handler` for `event`. Connections it alone needed stay open until :meth:`stop_listening`.

        Parameters
        ----------
        handler : Callable[..., Awaitable[None]]
            The handler given to :meth:`listen` or :meth:`add_listener`.
        event : :class:`HubEvent`
            The event it was registered for.

        """
        for listener in [entry for entry in self._listeners if entry.handler is handler and entry.event == event]:
            self._listeners.remove(listener)
            if listener.worker is not None:
                listener.worker.cancel()

    async def start_listening(self) -> None:
        """List the shards and spires, then open every hub connection the listeners need.

        |coro|

        Endpoints: ``GET /api/shards``, ``GET /api/spires``, ``POST /api/auth/hub-token`` for each connection

        It returns once the connections are up; they stay up in the background until :meth:`stop_listening` or a logout.

        """
        if self._listening is True:
            return

        self._listening = True
        await self._refresh_objects()

        for listener in self._listeners:
            self._start_worker(listener=listener)

        await self._sync_connections()
        self._refresher = asyncio.create_task(self._refresh_loop(), name="ampapi hub refresh")

    async def stop_listening(self) -> None:
        """Close every hub connection and stop the handlers; anything still queued is dropped.

        |coro|

        """
        self._listening = False
        tasks: list[asyncio.Task[None]] = [listener.worker for listener in self._listeners if listener.worker is not None]
        if self._refresher is not None:
            tasks.append(self._refresher)

        for task in (*tasks, *self._background):
            task.cancel()

        await asyncio.gather(*(connection.stop() for connection in self._connections.values()), return_exceptions=True)
        await asyncio.gather(*tasks, *self._background, return_exceptions=True)
        self._connections.clear()
        for listener in self._listeners:
            listener.worker = None

    def _in_background(self, coroutine: Awaitable[None]) -> None:
        """Run `coroutine` as a task we keep hold of, so it isn't collected before it ends."""
        task: asyncio.Task[None] = asyncio.ensure_future(coroutine)
        self._background.add(task)
        task.add_done_callback(self._background.discard)

    def _start_worker(self, listener: _Listener) -> None:
        if listener.worker is None or listener.worker.done():
            listener.worker = asyncio.create_task(self._work(listener=listener), name=f"ampapi listener {listener.event}")

    async def _work(self, listener: _Listener) -> None:
        """Call one listener's handler for each queued event, in order; a handler that raises is logged and skipped."""
        while True:
            arguments: tuple[Any, ...] = await listener.queue.get()
            try:
                await listener.handler(*arguments)
            except Exception:
                LOGGER.exception(
                    "<%s.%s> | A handler raised | Event: %s | Handler: %s",
                    __class__.__name__,
                    "_work",
                    listener.event,
                    listener.handler,
                )

    async def _refresh_objects(self) -> None:
        """Fetch the shard and spire lists that listeners are handed objects from."""
        self._hub_shards = {shard.id: shard for shard in await self.get_shards()}
        self._hub_spires = {spire.id: spire for spire in await self.get_spires()}

    async def _refresh_loop(self) -> None:
        """Fetch the lists again every 5 minutes, or sooner when an event names something we don't know."""
        while self._listening is True:
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(self._refresh_wanted.wait(), timeout=self._refresh_every)

            self._refresh_wanted.clear()
            # After a logout, fetching would log in again, so we stop instead.
            if self.session.logged_in is False:
                return

            try:
                await self._refresh_objects()
                await self._sync_connections()
            except (AMPAPIRequestError, ClientError) as error:
                LOGGER.warning("<%s.%s> | Failed to refresh the hub lists | Error: %s", __class__.__name__, "_refresh_loop", error)

    def _wanted_ids(self, events: frozenset[str], scope: Literal["shard", "spire"]) -> set[str]:
        """The shard or spire IDs the listeners for `events` cover; one with no scope covers every one we know."""
        known: dict[str, Any] = dict(self._hub_shards) if scope == "shard" else dict(self._hub_spires)
        wanted: set[str] = set()
        for listener in self._listeners:
            if listener.event not in events:
                continue

            scoped: Optional[str] = listener.shard_id if scope == "shard" else listener.spire_id
            if scoped is None:
                wanted.update(known)
            elif scoped in known:
                wanted.add(scoped)
        return wanted

    async def _sync_connections(self) -> None:
        """Open the connections the listeners need, and close shard ones nobody needs any more."""
        shard_ids: set[str] = self._wanted_ids(events=SHARD_EVENTS, scope="shard")
        for key in [key for key in self._connections if key.startswith("shard/") and key.removeprefix("shard/") not in shard_ids]:
            await self._connections.pop(key).stop()

        for shard_id in sorted(shard_ids):
            shard: Shard = self._hub_shards[shard_id]
            joins: list[tuple[str, list[Any]]] = [("JoinShard", [shard.data["tenantId"], shard_id])]
            await self._open(key=f"shard/{shard_id}", hub="shard", joins=joins, shard_id=shard_id)

        if any(listener.event in SPIRE_EVENTS for listener in self._listeners):
            spire_ids: set[str] = self._wanted_ids(events=frozenset(("spire_state",)), scope="spire")
            joins = [("JoinNetwork", []), *(("JoinSpire", [spire_id]) for spire_id in sorted(spire_ids))]
            await self._open(key="spire", hub="spire", joins=joins)

        # The tasks hub also tells us of shards we don't know yet, for listeners that cover every shard.
        covers_every_shard: bool = any(listener.event in SHARD_EVENTS and listener.shard_id is None for listener in self._listeners)
        if covers_every_shard or any(listener.event == "task" for listener in self._listeners):
            await self._open(key="tasks", hub="tasks", joins=[])

    async def _open(self, key: str, hub: str, joins: list[tuple[str, list[Any]]], shard_id: Optional[str] = None) -> None:
        """Open one connection, or open it again when its joins changed; a failure is logged and left to the next refresh."""
        existing: Optional[HubConnection] = self._connections.get(key)
        if existing is not None and existing.running and existing.joins == joins:
            return

        if existing is not None:
            await existing.stop()

        connection: HubConnection = HubConnection(session=self.session, hub=hub, joins=joins, on_event=self._dispatch, shard_id=shard_id)
        try:
            await connection.start()
        except (AMPAPIHubError, AMPAPIRequestError, ClientError, ConnectionError, TimeoutError) as error:
            LOGGER.warning("<%s.%s> | Failed to open a hub connection | Key: %s | Error: %s", __class__.__name__, "_open", key, error)
            self._connections.pop(key, None)
            return

        self._connections[key] = connection

    def _dispatch(self, connection: HubConnection, target: str, arguments: list[Any]) -> None:
        """Turn one hub event into its object and queue it for each listener it's for."""
        if connection.hub == "shard":
            self._dispatch_shard(connection=connection, target=target, arguments=arguments)

        elif connection.hub == "spire":
            self._dispatch_spire(target=target, arguments=arguments)

        elif target == "TaskUpsert" and arguments:
            task: RunningTask = RunningTask(data=arguments[0])
            if task.target_type == "Shard" and task.target_id not in self._hub_shards:
                self._refresh_wanted.set()

            self._deliver(event="task", arguments=(task,))

    def _dispatch_shard(self, connection: HubConnection, target: str, arguments: list[Any]) -> None:
        """Attribute one shard hub event to its shard, and drop a state another shard socket already delivered."""
        known: Optional[tuple[ShardEvent, int, type[AMPObject], Optional[int]]] = SHARD_TARGETS.get(target)
        if known is None or len(arguments) <= known[1]:
            LOGGER.debug("<%s.%s> | Skipped a shard event | Target: %s", __class__.__name__, "_dispatch_shard", target)
            return

        event, index, kind, shard_index = known
        shard_id: Any = connection.shard_id if shard_index is None else arguments[shard_index]
        shard: Optional[Shard] = self._hub_shards.get(shard_id) if isinstance(shard_id, str) else None
        if shard is None:
            # A shard made since the last list; the next refresh brings it in.
            self._refresh_wanted.set()
            return

        value: Any = arguments[index]
        # `UserRoster` sends a list of players; every other event, one object.
        entries: list[Any] = value if isinstance(value, list) else []  # pyright: ignore[reportUnknownVariableType]
        payload: Any = [kind(data=entry) for entry in entries] if isinstance(value, list) else kind(data=value)

        # Each shard socket gets every shard's state, so the same revision comes once per socket.
        if isinstance(payload, ShardStatus):
            if shard.id not in self._state_revisions:
                self._state_revisions[shard.id] = deque(maxlen=self._revisions_kept)

            seen: deque[int] = self._state_revisions[shard.id]
            if payload.revision in seen:
                return

            seen.append(payload.revision)

        self._deliver(event=event, arguments=(shard, payload), shard_id=shard.id)

    def _dispatch_spire(self, target: str, arguments: list[Any]) -> None:
        # `NetworkStatus` is sent as two arguments, `(kind, json)`, the second a JSON string with PascalCase keys.
        if target == "NetworkStatus" and len(arguments) >= 2:
            status: Any = json.loads(arguments[1]) if isinstance(arguments[1], str) else {}
            fields: dict[str, Any] = status if isinstance(status, dict) else {}  # pyright: ignore[reportUnknownVariableType]
            self._deliver(event="network_status", arguments=(NetworkStatus(data={"kind": arguments[0], **fields}),))
            return

        if target == "SpireState" and arguments:
            state: SpireStatus = SpireStatus(data=arguments[0])
            spire: Optional[Spire] = self._hub_spires.get(state.spire_id)
            if spire is not None:
                self._deliver(event="spire_state", arguments=(spire, state), spire_id=spire.id)
            return

        if target == "SpirePresence" and arguments:
            presence: SpirePresence = SpirePresence(data=arguments[0])
            spire = self._hub_spires.get(presence.spire["id"])
            if spire is None:
                # A spire that just joined; the next refresh brings it in.
                self._refresh_wanted.set()
                return

            self._deliver(event="spire_presence", arguments=(spire, presence), spire_id=spire.id)

    def _deliver(self, event: HubEvent, arguments: tuple[Any, ...], shard_id: Optional[str] = None, spire_id: Optional[str] = None) -> None:
        """Queue `arguments` for every listener of `event` whose scope takes it."""
        for listener in self._listeners:
            if listener.event != event or (listener.shard_id is not None and listener.shard_id != shard_id):
                continue

            if listener.spire_id is not None and listener.spire_id != spire_id:
                continue

            listener.put(arguments=arguments)
