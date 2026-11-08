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
import weakref
from collections import OrderedDict
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

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiohttp import ClientWebSocketResponse

    from ._types import ShardResponse, SpireResponse
    from .session import Session

__all__ = (
    "Hub",
    "HubConnection",
    "HubEvent",
    "PanelHub",
    "ShardHub",
    "SpireHub",
)

LOGGER: logging.Logger = logging.getLogger(__name__)

# Every SignalR JSON frame ends with this record separator, and one WebSocket message can hold several frames.
RECORD_SEPARATOR: str = "\x1e"

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
type Level = Literal["shard", "spire", "panel"]

# TODO: Settle the event names, and which level takes which event, with Kat (#3-47.2.7).
# This table is the one place both live; the `listener` overloads below repeat the names for pyright.
# Each event: the hub socket it comes on, and the hub levels a listener for it can sit on.
EVENTS: dict[str, tuple[str, frozenset[Level]]] = {
    "console": ("shard", frozenset(("shard", "spire", "panel"))),
    "state": ("shard", frozenset(("shard", "spire", "panel"))),
    "lifecycle": ("shard", frozenset(("shard", "spire", "panel"))),
    "metrics": ("shard", frozenset(("shard", "spire", "panel"))),
    "players": ("shard", frozenset(("shard", "spire", "panel"))),
    "player_joined": ("shard", frozenset(("shard", "spire", "panel"))),
    "player_left": ("shard", frozenset(("shard", "spire", "panel"))),
    "migration": ("shard", frozenset(("shard", "spire", "panel"))),
    "snapshot": ("shard", frozenset(("shard", "spire", "panel"))),
    "schedule_run": ("shard", frozenset(("shard", "spire", "panel"))),
    "spire_state": ("spire", frozenset(("spire", "panel"))),
    "spire_presence": ("spire", frozenset(("panel",))),
    "network_status": ("spire", frozenset(("panel",))),
    # Tasks are panel-wide: AMP's tasks hub has no rooms to join.
    "task": ("tasks", frozenset(("panel",))),
}
SHARD_EVENTS: frozenset[str] = frozenset(event for event, (socket, _levels) in EVENTS.items() if socket == "shard")

# Each `/hubs/shard` target: our name for it, the argument that holds the payload, the object it becomes, and the
# argument that holds its shard ID. `ConsoleLine` names no shard; `Lifecycle` carries it in its payload.
SHARD_TARGETS: dict[str, tuple[str, int, type[AMPObject], Optional[int]]] = {
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

# The functions `Hub.listener` has marked, until the class they sit in is made and takes them.
_MARKED: dict[Callable[..., Any], str] = {}


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
    ) -> None:
        self.session: Session = session
        self.hub: str = hub
        self.joins: list[tuple[str, list[Any]]] = joins
        self._on_event: Callable[[HubConnection, str, list[Any]], None] = on_event
        self._socket: Optional[ClientWebSocketResponse] = None
        self._reader: Optional[asyncio.Task[None]] = None
        self._runner: Optional[asyncio.Task[None]] = None
        self._pending: dict[str, asyncio.Future[Any]] = {}
        self._invocations: int = 0
        self._stopping: bool = False

    def __repr__(self) -> str:  # noqa: D105
        return f"<HubConnection hub={self.hub!r} joins={len(self.joins)} running={self.running}>"

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

    async def join(self, target: str, arguments: list[Any]) -> None:
        """Send a join now, and keep it so each reconnect sends it again.

        |coro|

        Raises
        ------
        AMPAPIHubError
            If AMP refuses the join, eg. ``"shards.error.notFound"``.

        """
        self.joins.append((target, arguments))
        result: Any = await self.invoke(target=target, arguments=arguments)
        if isinstance(result, dict) and result.get("error") is not None:  # pyright: ignore[reportUnknownMemberType]
            self.joins.remove((target, arguments))
            raise AMPAPIHubError(hub=self.hub, target=target, error=result.get("error"))  # pyright: ignore[reportUnknownMemberType]

    async def leave(self, join_target: str, leave_target: str, arguments: list[Any]) -> None:
        """Forget a join and send its leave, eg. ``"JoinShard"`` and ``"LeaveShard"``.

        |coro|

        """
        if (join_target, arguments) in self.joins:
            self.joins.remove((join_target, arguments))

        with contextlib.suppress(AMPAPIHubError, ConnectionError, TimeoutError):
            await self.invoke(target=leave_target, arguments=arguments)

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
        self._runner = asyncio.create_task(self._run(), name=f"ampapi hub {self.hub}")

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
        LOGGER.debug("<%s.%s> | Connecting | Hub: %s | Joins: %s", __class__.__name__, "_connect", self.hub, len(self.joins))
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

        for target, arguments in list(self.joins):
            result: Any = await self.invoke(target=target, arguments=arguments)
            if isinstance(result, dict) and result.get("error") is not None:  # pyright: ignore[reportUnknownMemberType]
                await self._socket.close()
                raise AMPAPIHubError(hub=self.hub, target=target, error=result.get("error"))  # pyright: ignore[reportUnknownMemberType]

        LOGGER.info("<%s.%s> | Connected | Hub: %s | Joins: %s", __class__.__name__, "_connect", self.hub, len(self.joins))

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


class _Worker:
    """One listener's queue and the task that works through it, so it keeps its order and a slow one blocks nobody."""

    # `metrics` comes every 3 seconds per shard, so a backlog past this drops its oldest.
    metrics_backlog: ClassVar[int] = 8

    def __init__(self, handler: Callable[[Any], Awaitable[None]], event: str) -> None:
        self.handler: Callable[[Any], Awaitable[None]] = handler
        self.event: str = event
        self.queue: asyncio.Queue[Any] = asyncio.Queue(maxsize=self.metrics_backlog if event == "metrics" else 0)
        self.task: asyncio.Task[None] = asyncio.create_task(self._work(), name=f"ampapi listener {event}")

    def put(self, data: Any) -> None:
        """Queue one event's object, dropping the oldest when a `metrics` backlog is full."""
        if self.queue.full():
            self.queue.get_nowait()
        self.queue.put_nowait(data)

    async def _work(self) -> None:
        """Call the handler for each queued object, in order; a handler that raises is logged and skipped."""
        while True:
            data: Any = await self.queue.get()
            try:
                await self.handler(data)
            except Exception:
                LOGGER.exception(
                    "<%s.%s> | A listener raised | Event: %s | Handler: %s",
                    __class__.__name__,
                    "_work",
                    self.event,
                    self.handler,
                )


class Hub:
    """The base of the three hub levels: it holds the :class:`Session` and runs the listeners a subclass declares.

    A listener is a method marked with :meth:`listener`, called as ``(self, data)`` with the event's object. Each one
    has its own queue, so it keeps its order and a slow one blocks nobody; one that raises is logged and skipped.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session the hub sockets log in through.

    """

    session: Session
    # Which column of `EVENTS` this level is.
    _level: ClassVar[Level]
    # Each event's listener method names, gathered from the class and its bases when the class is made.
    _listeners: ClassVar[dict[str, tuple[str, ...]]] = {}

    def __init__(self, session: Session) -> None:  # noqa: D107
        self.session = session
        self._workers: dict[str, _Worker] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:  # noqa: D105
        super().__init_subclass__(**kwargs)
        gathered: dict[str, list[str]] = {event: list(names) for event, names in cls._listeners.items()}

        for name, value in list(cls.__dict__.items()):
            event: Optional[str] = _MARKED.pop(value, None) if callable(value) else None
            if event is None:
                continue
            if cls._level not in EVENTS[event][1]:
                msg = f"{cls.__name__}.{name} listens for {event!r}, which a {cls._level} hub doesn't get."
                raise TypeError(msg)

            gathered[event] = [*gathered.get(event, []), name]
        cls._listeners = {event: tuple(names) for event, names in gathered.items()}

    @overload
    @classmethod
    def listener[F: Callable[[Any, ConsoleLine], Awaitable[None]]](cls, name: Literal["console"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, ShardStatus], Awaitable[None]]](cls, name: Literal["state"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, LifecycleEvent], Awaitable[None]]](cls, name: Literal["lifecycle"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, ShardMetrics], Awaitable[None]]](cls, name: Literal["metrics"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, list[ShardPlayer]], Awaitable[None]]](cls, name: Literal["players"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, ShardPlayer], Awaitable[None]]](
        cls,
        name: Literal["player_joined", "player_left"],
    ) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, ShardMigration], Awaitable[None]]](cls, name: Literal["migration"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, ShardSnapshots], Awaitable[None]]](cls, name: Literal["snapshot"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, ScheduleExecution], Awaitable[None]]](cls, name: Literal["schedule_run"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, SpireStatus], Awaitable[None]]](cls, name: Literal["spire_state"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, SpirePresence], Awaitable[None]]](cls, name: Literal["spire_presence"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, NetworkStatus], Awaitable[None]]](cls, name: Literal["network_status"]) -> Callable[[F], F]: ...
    @overload
    @classmethod
    def listener[F: Callable[[Any, RunningTask], Awaitable[None]]](cls, name: Literal["task"]) -> Callable[[F], F]: ...
    @classmethod
    def listener[F: Callable[..., Awaitable[None]]](cls, name: HubEvent) -> Callable[[F], F]:
        """Mark a coroutine method of a subclass as the listener for an event, eg. ``@ShardHub.listener(name="console")``.

        The method is called as ``(self, data)``, `data` the event's object. Which events a level takes is in `EVENTS`;
        a method for one its class doesn't take raises `TypeError` when the class is made.

        Parameters
        ----------
        name : :class:`HubEvent`
            The event, eg. ``"console"``.

        Returns
        -------
        Callable
            The decorator, which hands back the method as it was.

        """

        def mark(method: F) -> F:
            _MARKED[method] = name
            return method

        return mark

    def _has_listener(self, events: frozenset[str]) -> bool:
        """If the class declares a listener for any of `events`."""
        return any(self._listeners.get(event) for event in events)

    def _emit(self, event: str, data: Any) -> None:
        """Queue `data` for each of this object's listeners for `event`."""
        for name in self._listeners.get(event, ()):
            worker: Optional[_Worker] = self._workers.get(name)
            if worker is None or worker.task.done():
                worker = _Worker(handler=getattr(self, name), event=event)
                self._workers[name] = worker

            worker.put(data=data)

    async def _stop_workers(self) -> None:
        """Stop this object's listener workers; anything still queued is dropped."""
        for worker in self._workers.values():
            worker.task.cancel()

        await asyncio.gather(*(worker.task for worker in self._workers.values()), return_exceptions=True)
        self._workers.clear()

    async def _open_socket(
        self,
        hub: str,
        joins: list[tuple[str, list[Any]]],
        on_event: Callable[[HubConnection, str, list[Any]], None],
    ) -> Optional[HubConnection]:
        """Open one hub socket; a failure is logged, and the next sync tries again."""
        # A sync that began before a logout mustn't log in again to open a socket.
        if self.session.logged_in is False:
            return None
        connection: HubConnection = HubConnection(session=self.session, hub=hub, joins=joins, on_event=on_event)
        try:
            await connection.start()
        except (AMPAPIHubError, AMPAPIRequestError, ClientError, ConnectionError, TimeoutError) as error:
            LOGGER.warning("<%s.%s> | Failed to open a hub socket | Hub: %s | Error: %s", __class__.__name__, "_open_socket", hub, error)
            return None
        return connection


class ShardHub(Hub):
    """The shard level: listeners for one shard's events, eg. a `Shard` subclass's.

    It is its own subscriber. Its events come through the `Panel`'s shared `/hubs/shard` socket, except `console`:
    AMP's console lines don't name their shard, so a `console` listener opens this shard's own socket, and hears only
    that one.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session the hub sockets log in through.
    panel : Union[:class:`PanelHub`, None]
        The panel that routes this shard's events, `None` for an object made without one.

    """

    _level = "shard"
    id: str
    data: ShardResponse

    def __init__(self, session: Session, panel: Optional[PanelHub]) -> None:  # noqa: D107
        super().__init__(session=session)
        self._panel: Optional[PanelHub] = panel
        self._console: Optional[HubConnection] = None

    @property
    def _shared_events(self) -> frozenset[str]:
        """The events this shard takes from the shared socket: all but `console`."""
        return SHARD_EVENTS - {"console"}

    async def _sync_console(self, listening: bool) -> None:
        """Open this shard's own socket when it has a `console` listener and the panel listens; close it otherwise."""
        wanted: bool = listening is True and self._has_listener(events=frozenset(("console",)))
        if wanted is True and (self._console is None or not self._console.running):
            joins: list[tuple[str, list[Any]]] = [("JoinShard", [self.data["tenantId"], self.id])]
            self._console = await self._open_socket(hub="shard", joins=joins, on_event=self._on_console_socket)

        elif wanted is False and self._console is not None:
            await self._console.stop()
            self._console = None

    def _on_console_socket(self, connection: HubConnection, target: str, arguments: list[Any]) -> None:  # noqa: ARG002
        # The shared socket brings everything else, so only console lines are taken from here.
        if target == "ConsoleLine" and arguments:
            self._emit(event="console", data=ConsoleLine(data=arguments[0]))


class SpireHub(Hub):
    """The spire level: listeners for one spire's `spire_state`, and for the shard events of the shards it subscribes.

    `console` lines reach it unattributed, as AMP's don't name their shard.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session the hub sockets log in through.
    panel : Union[:class:`PanelHub`, None]
        The panel that routes this spire's events, `None` for an object made without one.

    """

    _level = "spire"
    # TODO: Confirm with Kat that `add_subscriber()` with no shard means every shard on the spire (#3-47.2.7).
    # Set to `False` and it subscribes nothing instead.
    none_means_every_shard: ClassVar[bool] = True
    id: str
    data: SpireResponse

    def __init__(self, session: Session, panel: Optional[PanelHub]) -> None:  # noqa: D107
        super().__init__(session=session)
        self._panel: Optional[PanelHub] = panel
        self._every_shard: bool = False
        self._subscribed: set[str] = set()

    async def add_subscriber(self, shard_id: Optional[str] = None) -> None:
        """Take a shard's events into this spire's listeners.

        |coro|

        Parameters
        ----------
        shard_id : Union[:class:`str`, None], optional
            The shard, by default None for every shard on this spire, now and later.

        """
        if shard_id is None:
            self._every_shard = self.none_means_every_shard
        else:
            self._subscribed.add(shard_id)

        if self._panel is not None:
            await self._panel._sync_sockets()  # pyright: ignore[reportPrivateUsage]

    async def remove_subscriber(self, shard_id: Optional[str] = None) -> None:
        """Stop taking a shard's events, or every shard's.

        |coro|

        Parameters
        ----------
        shard_id : Union[:class:`str`, None], optional
            The shard, by default None for all of them.

        """
        if shard_id is None:
            self._every_shard = False
            self._subscribed.clear()
        else:
            self._subscribed.discard(shard_id)

        if self._panel is not None:
            await self._panel._sync_sockets()  # pyright: ignore[reportPrivateUsage]

    def _covers(self, shard_id: str, spire_id: Optional[str]) -> bool:
        """If this spire subscribes `shard_id`, which lives on `spire_id`."""
        return shard_id in self._subscribed or (self._every_shard is True and spire_id == self.id)


class PanelHub(Hub):
    """The panel level: the three shared hub sockets, routing, and listeners for the shards and spires it subscribes.

    :meth:`start_listening` opens, as listeners need them, one `/hubs/shard` socket joined to every shard any level
    needs, one `/hubs/spire` (the network, and each spire needed) and one `/hubs/tasks`. A shard level `console`
    listener adds that shard's own socket. Shard events are routed by the shard ID they carry to the shard's own
    object, to each spire that subscribes it, and to this panel if it does.

    AMP sends every shard's state to every shard socket, subscribed or not, so `state` is filtered by subscriber, and
    the copies are dropped by `(shard_id, revision)`. `console` lines on the shared socket name no shard, so they reach
    this panel's and the spires' `console` listeners unattributed.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session the hub sockets log in through.

    """

    _level = "panel"
    # How often the shard and spire lists are fetched again, in seconds.
    _refresh_every: ClassVar[float] = 300.0
    # How many `(shard_id, revision)` pairs the state seen-set keeps.
    _seen_kept: ClassVar[int] = 2048

    def __init__(self, session: Session) -> None:  # noqa: D107
        super().__init__(session=session)
        self._listening: bool = False
        self._every_shard: bool = False
        self._every_spire: bool = False
        self._subscribed_shards: set[str] = set()
        self._subscribed_spires: set[str] = set()
        self._shard_records: dict[str, ShardResponse] = {}
        self._spire_ids: set[str] = set()
        self._shard_objects: dict[str, weakref.WeakSet[ShardHub]] = {}
        self._spire_objects: dict[str, weakref.WeakSet[SpireHub]] = {}
        self._sockets: dict[str, HubConnection] = {}
        self._seen_states: OrderedDict[tuple[str, int], None] = OrderedDict()
        self._refresher: Optional[asyncio.Task[None]] = None
        self._refresh_wanted: asyncio.Event = asyncio.Event()
        self._sync_lock: asyncio.Lock = asyncio.Lock()
        self._background: set[asyncio.Task[None]] = set()

    @property
    def listening(self) -> bool:
        """If any hub socket is up, or waiting to connect again."""
        sockets: list[HubConnection] = [*self._sockets.values(), *self._console_sockets()]
        return self._listening is True and any(socket.running for socket in sockets)

    def _console_sockets(self) -> list[HubConnection]:
        """The shard objects' own console sockets."""
        consoles: list[Optional[HubConnection]] = [shard._console for shard in self._all_shards()]  # pyright: ignore[reportPrivateUsage]
        return [socket for socket in consoles if socket is not None]

    async def add_subscriber(self, shard_id: Optional[str] = None, spire_id: Optional[str] = None) -> None:
        """Take a shard's or a spire's events into this panel's listeners; with neither, every shard and spire.

        |coro|

        Parameters
        ----------
        shard_id : Union[:class:`str`, None], optional
            The shard, by default None.
        spire_id : Union[:class:`str`, None], optional
            The spire, for its `spire_state`, by default None.

        """
        if shard_id is None and spire_id is None:
            self._every_shard = True
            self._every_spire = True
        if shard_id is not None:
            self._subscribed_shards.add(shard_id)
        if spire_id is not None:
            self._subscribed_spires.add(spire_id)

        await self._sync_sockets()

    async def remove_subscriber(self, shard_id: Optional[str] = None, spire_id: Optional[str] = None) -> None:
        """Stop taking a shard's or a spire's events; with neither, every one's.

        |coro|

        Parameters
        ----------
        shard_id : Union[:class:`str`, None], optional
            The shard, by default None.
        spire_id : Union[:class:`str`, None], optional
            The spire, by default None.

        """
        if shard_id is None and spire_id is None:
            self._every_shard = False
            self._every_spire = False
            self._subscribed_shards.clear()
            self._subscribed_spires.clear()
        if shard_id is not None:
            self._subscribed_shards.discard(shard_id)
        if spire_id is not None:
            self._subscribed_spires.discard(spire_id)

        await self._sync_sockets()

    async def start_listening(self) -> None:
        """List the shards and spires, then open the hub sockets the listeners need.

        |coro|

        Endpoints: ``GET /api/shards``, ``GET /api/spires``, ``POST /api/auth/hub-token`` for each socket

        It returns once the sockets are up; they stay up in the background until :meth:`stop_listening` or a logout.

        """
        if self._listening is True:
            return

        self._listening = True
        await self._refresh_records()
        await self._sync_sockets()
        self._refresher = asyncio.create_task(self._refresh_loop(), name="ampapi hub refresh")

    async def stop_listening(self) -> None:
        """Close every hub socket and stop every listener; anything still queued is dropped.

        |coro|

        """
        self._listening = False
        if self._refresher is not None:
            self._refresher.cancel()

        for task in self._background:
            task.cancel()

        await asyncio.gather(*(socket.stop() for socket in self._sockets.values()), return_exceptions=True)
        self._sockets.clear()
        hubs: list[Hub] = [self, *self._all_shards(), *self._all_spires()]
        for shard in self._all_shards():
            await shard._sync_console(listening=False)  # pyright: ignore[reportPrivateUsage]

        await asyncio.gather(*(hub._stop_workers() for hub in hubs), return_exceptions=True)
        await asyncio.gather(*(task for task in (self._refresher, *self._background) if task is not None), return_exceptions=True)

    async def _list_records(self) -> tuple[list[ShardResponse], list[SpireResponse]]:
        """The shard and spire lists, as AMP sends them; `Panel` fills this in from its REST calls."""
        raise NotImplementedError

    def _register_shard(self, shard: ShardHub) -> None:
        """Keep a shard object so its events reach it; the panel holds it weakly, so keep your own reference."""
        # A deleted shard, eg. from `get_shards(include_deleted=True)`, can't be joined until it's restored.
        if shard.data.get("deleted") is True:
            return
        if shard.id not in self._shard_objects:
            self._shard_objects[shard.id] = weakref.WeakSet()

        self._shard_objects[shard.id].add(shard)
        if self._listening is True and shard._listeners:
            self._in_background(coroutine=self._sync_sockets())

    def _register_spire(self, spire: SpireHub) -> None:
        """Keep a spire object so its events reach it; the panel holds it weakly, so keep your own reference."""
        if spire.id not in self._spire_objects:
            self._spire_objects[spire.id] = weakref.WeakSet()

        self._spire_objects[spire.id].add(spire)
        if self._listening is True and spire._listeners:
            self._in_background(coroutine=self._sync_sockets())

    def _all_shards(self) -> list[ShardHub]:
        return [shard for shards in self._shard_objects.values() for shard in shards]

    def _all_spires(self) -> list[SpireHub]:
        return [spire for spires in self._spire_objects.values() for spire in spires]

    def _in_background(self, coroutine: Awaitable[None]) -> None:
        """Run `coroutine` as a task we keep hold of, so it isn't collected before it ends."""
        task: asyncio.Task[None] = asyncio.ensure_future(coroutine)
        self._background.add(task)
        task.add_done_callback(self._background.discard)

    async def _refresh_records(self) -> None:
        """Fetch the shard and spire lists that routing and `None` subscribers are worked out from."""
        shards, spires = await self._list_records()
        self._shard_records = {shard["id"]: shard for shard in shards}
        self._spire_ids = {spire["id"] for spire in spires}

    async def _refresh_loop(self) -> None:
        """Fetch the lists again every 5 minutes, or sooner when an event names a shard we don't know."""
        while self._listening is True:
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(self._refresh_wanted.wait(), timeout=self._refresh_every)

            self._refresh_wanted.clear()
            # After a logout, fetching would log in again, so we stop instead.
            if self.session.logged_in is False:
                return

            try:
                await self._refresh_records()
                await self._sync_sockets()
            except (AMPAPIRequestError, ClientError) as error:
                LOGGER.warning("<%s.%s> | Failed to refresh the hub lists | Error: %s", __class__.__name__, "_refresh_loop", error)

    def _covers_shard(self, shard_id: str) -> bool:
        return self._every_shard is True or shard_id in self._subscribed_shards

    def _covers_spire(self, spire_id: str) -> bool:
        return self._every_spire is True or spire_id in self._subscribed_spires

    def _needed_shards(self) -> set[str]:
        """The shards the shared `/hubs/shard` socket must join: this panel's, the spires' and each shard object's own."""
        needed: set[str] = set()
        if self._has_listener(events=SHARD_EVENTS):
            needed.update(shard_id for shard_id in self._shard_records if self._covers_shard(shard_id=shard_id))

        for spire in self._all_spires():
            if not spire._has_listener(events=SHARD_EVENTS):
                continue
            for shard_id, record in self._shard_records.items():
                if spire._covers(shard_id, record["spireId"]):  # pyright: ignore[reportPrivateUsage]
                    needed.add(shard_id)

        for shard in self._all_shards():
            if shard._has_listener(events=shard._shared_events):  # pyright: ignore[reportPrivateUsage]
                needed.add(shard.id)
        return {shard_id for shard_id in needed if shard_id in self._shard_records}

    def _needed_spires(self) -> Optional[set[str]]:
        """The spires the `/hubs/spire` socket must join, or `None` when no listener needs that socket at all."""
        panel_wide: bool = self._has_listener(events=frozenset(("spire_presence", "network_status")))
        needed: set[str] = set()
        if self._has_listener(events=frozenset(("spire_state",))):
            needed.update(spire_id for spire_id in self._spire_ids if self._covers_spire(spire_id=spire_id))

        for spire in self._all_spires():
            if spire._has_listener(events=frozenset(("spire_state",))):
                needed.add(spire.id)
        return needed if needed or panel_wide else None

    async def _sync_sockets(self) -> None:
        """Open, join, leave and close the sockets so they match what the listeners and subscribers need now."""
        # After a logout, opening a socket would log in again.
        if self._listening is False or self.session.logged_in is False:
            return

        async with self._sync_lock:
            await self._sync_shard_socket(needed=self._needed_shards())
            await self._sync_spire_socket(needed=self._needed_spires())
            await self._sync_socket(key="tasks", wanted=self._has_listener(events=frozenset(("task",))), on_event=self._on_tasks_socket)
            for shard in self._all_shards():
                # A shard that's deleted, or gone from the list, can't be joined.
                await shard._sync_console(listening=shard.id in self._shard_records)  # pyright: ignore[reportPrivateUsage]

    async def _sync_socket(
        self,
        key: str,
        wanted: bool,
        on_event: Callable[[HubConnection, str, list[Any]], None],
    ) -> Optional[HubConnection]:
        """Open the `key` socket with no joins when `wanted`, and close it when not; hand back the open one."""
        socket: Optional[HubConnection] = self._sockets.get(key)
        if wanted is False:
            if socket is not None:
                await self._sockets.pop(key).stop()
            return None

        if socket is None or not socket.running:
            socket = await self._open_socket(hub=key, joins=[], on_event=on_event)
            if socket is None:
                return None
            self._sockets[key] = socket
        return socket

    async def _sync_shard_socket(self, needed: set[str]) -> None:
        socket: Optional[HubConnection] = await self._sync_socket(key="shard", wanted=bool(needed), on_event=self._on_shard_socket)
        if socket is None:
            return
        # Each join's arguments are `[tenant_id, shard_id]`, so a leave sends them back as they were.
        joined: dict[str, list[Any]] = {arguments[1]: arguments for _target, arguments in socket.joins}
        for shard_id in sorted(joined.keys() - needed):
            await socket.leave(join_target="JoinShard", leave_target="LeaveShard", arguments=joined[shard_id])

        for shard_id in sorted(needed - joined.keys()):
            try:
                await socket.join(target="JoinShard", arguments=[self._shard_records[shard_id]["tenantId"], shard_id])
            except (AMPAPIHubError, ConnectionError, TimeoutError) as error:
                LOGGER.warning(
                    "<%s.%s> | Failed to join a shard | Shard ID: %s | Error: %s",
                    __class__.__name__,
                    "_sync_shard_socket",
                    shard_id,
                    error,
                )
                # Usually a shard deleted since the last list; it's left out until a refresh lists it again.
                self._shard_records.pop(shard_id, None)

    async def _sync_spire_socket(self, needed: Optional[set[str]]) -> None:
        socket: Optional[HubConnection] = await self._sync_socket(key="spire", wanted=needed is not None, on_event=self._on_spire_socket)
        if socket is None or needed is None:
            return
        if ("JoinNetwork", []) not in socket.joins:
            await socket.join(target="JoinNetwork", arguments=[])

        joined: set[str] = {arguments[0] for target, arguments in socket.joins if target == "JoinSpire"}
        for spire_id in sorted(joined - needed):
            await socket.leave(join_target="JoinSpire", leave_target="LeaveSpire", arguments=[spire_id])

        for spire_id in sorted(needed - joined):
            try:
                await socket.join(target="JoinSpire", arguments=[spire_id])
            except (AMPAPIHubError, ConnectionError, TimeoutError) as error:
                LOGGER.warning(
                    "<%s.%s> | Failed to join a spire | Spire ID: %s | Error: %s",
                    __class__.__name__,
                    "_sync_spire_socket",
                    spire_id,
                    error,
                )

    def _on_shard_socket(self, connection: HubConnection, target: str, arguments: list[Any]) -> None:  # noqa: ARG002
        """Route one shared `/hubs/shard` event by the shard it names; a console line goes out unattributed."""
        known: Optional[tuple[str, int, type[AMPObject], Optional[int]]] = SHARD_TARGETS.get(target)
        if known is None or len(arguments) <= known[1]:
            return
        event, index, kind, shard_index = known
        value: Any = arguments[index]
        # `UserRoster` sends a list of players; every other event, one object.
        entries: list[Any] = value if isinstance(value, list) else []  # pyright: ignore[reportUnknownVariableType]
        payload: Any = [kind(data=entry) for entry in entries] if isinstance(value, list) else kind(data=value)
        if event == "console":
            if self._every_shard is True or self._subscribed_shards:
                self._emit(event=event, data=payload)
            for spire in self._all_spires():
                if spire._every_shard is True or spire._subscribed:  # pyright: ignore[reportPrivateUsage]
                    spire._emit(event=event, data=payload)
            return

        shard_id: Any = payload.shard_id if shard_index is None else arguments[shard_index]
        if not isinstance(shard_id, str):
            return
        record: Optional[ShardResponse] = self._shard_records.get(shard_id)
        if record is None:
            # A shard made since the last list; the next refresh brings it in.
            self._refresh_wanted.set()

        # Every shard socket gets every shard's state, so a reconnect or a second socket can bring the same revision twice.
        if isinstance(payload, ShardStatus):
            if (shard_id, payload.revision) in self._seen_states:
                return
            self._seen_states[(shard_id, payload.revision)] = None
            if len(self._seen_states) > self._seen_kept:
                self._seen_states.popitem(last=False)

        for shard in self._shard_objects.get(shard_id, ()):
            shard._emit(event=event, data=payload)

        for spire in self._all_spires():
            if spire._covers(shard_id, record["spireId"] if record is not None else None):  # pyright: ignore[reportPrivateUsage]
                spire._emit(event=event, data=payload)

        if self._covers_shard(shard_id=shard_id):
            self._emit(event=event, data=payload)

    def _on_spire_socket(self, connection: HubConnection, target: str, arguments: list[Any]) -> None:  # noqa: ARG002
        """Route a spire's state by its spire ID; presence and network status are panel-wide."""
        if target == "SpireState" and arguments:
            state: SpireStatus = SpireStatus(data=arguments[0])
            for spire in self._spire_objects.get(state.spire_id, ()):
                spire._emit(event="spire_state", data=state)

            if self._covers_spire(spire_id=state.spire_id):
                self._emit(event="spire_state", data=state)

        elif target == "SpirePresence" and arguments:
            self._emit(event="spire_presence", data=SpirePresence(data=arguments[0]))

        # `NetworkStatus` is sent as two arguments, `(kind, json)`, the second a JSON string with PascalCase keys.
        elif target == "NetworkStatus" and len(arguments) >= 2:
            status: Any = json.loads(arguments[1]) if isinstance(arguments[1], str) else {}
            fields: dict[str, Any] = status if isinstance(status, dict) else {}  # pyright: ignore[reportUnknownVariableType]
            self._emit(event="network_status", data=NetworkStatus(data={"kind": arguments[0], **fields}))

    def _on_tasks_socket(self, connection: HubConnection, target: str, arguments: list[Any]) -> None:  # noqa: ARG002
        if target != "TaskUpsert" or not arguments:
            return
        task: RunningTask = RunningTask(data=arguments[0])
        if task.target_type == "Shard" and task.target_id not in self._shard_records:
            self._refresh_wanted.set()
        self._emit(event="task", data=task)
