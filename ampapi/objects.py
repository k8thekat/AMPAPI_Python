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

import keyword
import logging
import re
import types
from collections.abc import Mapping
from enum import Enum
from typing import Any, ClassVar, Optional, Union, get_args, get_origin, get_type_hints

# The names below are read at run time by `typing.get_type_hints`, so they can't sit under `TYPE_CHECKING`.
from ._enums import (  # noqa: TC001
    LifecycleKind,
    MigrationStatus,
    ShardState,
    SnapshotContent,
    SnapshotKind,
    SnapshotStage,
    SnapshotState,
    TaskState,
)
from ._types import (  # noqa: TC001
    Principal,
    ScheduleStepOutcome,
    ShardSleepStatus,
    ShardStateMetrics,
    SnapshotSettingsResponse,
    SpirePlatform,
    SpireResponse,
    WrappedID,
)
from .base import Base

__all__ = (
    "AMPObject",
    "ConsoleHistory",
    "ConsoleLine",
    "LifecycleEvent",
    "NetworkStatus",
    "RunningTask",
    "ScheduleExecution",
    "ShardMetrics",
    "ShardMigration",
    "ShardPlayer",
    "ShardSnapshots",
    "ShardStatus",
    "Snapshot",
    "SpirePresence",
    "SpireStatus",
)

LOGGER: logging.Logger = logging.getLogger(__name__)

# A lower case letter or digit followed by a capital, where camelCase starts a new word.
_WORD_BREAK: re.Pattern[str] = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def _attribute_name(key: str) -> str:
    """The snake_case attribute `AMPObject` gives a camelCase key, eg. ``"memoryMB"`` becomes ``"memory_mb"``.

    A keyword or ``"data"`` gets a trailing underscore, so it can't hide a statement or the raw dict.
    """
    name: str = _WORD_BREAK.sub("_", key).lower()
    if keyword.iskeyword(name) or name == "data":
        return name + "_"
    return name


class AMPObject:
    """A dict from AMP, unpacked into snake_case attributes, eg. `streamId` becomes `stream_id`.

    Every key is set, declared or not, so nothing AMP sends is lost. A subclass only declares the attributes it knows,
    and those are converted by their annotation: an `AMPObject` subclass, a list of them, or an enum, where a value
    the library doesn't know stays as it came (the same rule as the enum fields elsewhere). Anything else is set as it
    came.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    data : Mapping[:class:`str`, Any]
        The dict as AMP sent it.

    Attributes
    ----------
    data : Mapping[:class:`str`, Any]
        The dict as AMP sent it.

    """

    data: Mapping[str, Any]
    # The attributes `__repr__` shows, the first of these a subclass declares.
    _repr_names: ClassVar[tuple[str, ...]] = ("id", "shard_id", "spire_id", "name", "status", "state", "kind", "online", "text")
    # Each subclass's resolved annotations, worked out on its first object.
    _hints: ClassVar[dict[type[AMPObject], dict[str, Any]]] = {}

    def __init__(self, data: Mapping[str, Any]) -> None:  # noqa: D107
        self.data = data
        hints: dict[str, Any] = self._type_hints()

        for key, value in data.items():
            name: str = _attribute_name(key=key)
            setattr(self, name, self._convert(hint=hints.get(name, Any), value=value))

    def __repr__(self) -> str:  # noqa: D105
        hints: dict[str, Any] = self._type_hints()
        shown: list[str] = [f"{name}={getattr(self, name)!r}" for name in self._repr_names if name in hints and hasattr(self, name)][:3]
        return f"<{type(self).__name__} {' '.join(shown)}>"

    # TODO: Decide if the dict-style access stays once the live checks read attributes (#3-47.2.2).
    # It lets code written against the old TypedDict replies, eg. `state["status"]`, keep working.
    def __getitem__(self, key: str) -> Any:  # noqa: D105
        return getattr(self, _attribute_name(key=key))

    @classmethod
    def _type_hints(cls) -> dict[str, Any]:
        """The class's annotations, resolved once and kept, as `get_type_hints` reads them at run time."""
        if cls not in AMPObject._hints:
            hints: dict[str, Any] = get_type_hints(cls)
            AMPObject._hints[cls] = {name: hint for name, hint in hints.items() if name not in ("data", "_repr_names", "_hints")}

        return AMPObject._hints[cls]

    @classmethod
    def _convert(cls, hint: Any, value: Any) -> Any:
        """`value` turned into what `hint` declares, where it's an `AMPObject`, a list of them or an enum."""
        if value is None:
            return None

        origin: Any = get_origin(hint)
        # `Optional[X]` and `Union[Enum, int]`: the first member that converts is the one used.
        if origin is Union or origin is types.UnionType:
            for member in get_args(hint):
                if member is not type(None) and member is not int and member is not str:
                    return cls._convert(hint=member, value=value)
            return value

        if origin is list and isinstance(value, list):
            item_hint: Any = get_args(hint)[0] if get_args(hint) else Any
            return [cls._convert(hint=item_hint, value=entry) for entry in value]  # pyright: ignore[reportUnknownVariableType]

        if isinstance(hint, type) and issubclass(hint, AMPObject) and isinstance(value, Mapping):
            return hint(data=value)  # pyright: ignore[reportUnknownArgumentType]
        if isinstance(hint, type) and issubclass(hint, Enum) and isinstance(value, int):
            return Base._to_enum(enum=hint, value=value)  # pyright: ignore[reportPrivateUsage]
        if isinstance(hint, type) and issubclass(hint, Enum) and isinstance(value, str):
            return Base._to_enum(enum=hint, value=value)  # pyright: ignore[reportPrivateUsage]
        return value


class ConsoleHistory(AMPObject):
    """``GET /api/shards/{id}/console/history``, the console lines, oldest first.

    .. versionadded:: 6.0.0
    """

    lines: list[ConsoleLine]
    has_more: bool
    "If older lines exist, see `before_seq`."


class ConsoleLine(AMPObject):
    """One console line: the shard hub's `ConsoleLine` event, and each of `ConsoleHistory.lines`.

    The hub's line carries no shard ID; each shard has its own hub connection, which says whose line it is.

    .. versionadded:: 6.0.0
    """

    stream_id: str
    """eg. ``"main"`` (the game), ``"system"`` (AMP) or ``"update"``."""
    text: str
    timestamp: str
    seq: int
    "Rises with each line, with gaps."
    kind: str
    """eg. ``"line"``, ``"info"``, ``"notice"``, ``"error"`` or ``"marker"``, which marks a change of `state`."""
    state: Optional[Union[ShardState, int]]
    "The status a marker line announces, `None` on other lines."
    success: Optional[bool]
    "Set on the markers that end a stop or an update."
    code: Optional[str]
    """A translation key for the text, eg. ``"shards.console.marker.stageOf"``."""
    params: Optional[dict[str, str]]
    "Values for the `code` translation."
    level: Optional[str]
    """The game's log level, eg. ``"INFO"``."""
    origin: Optional[str]
    """The game's log source, eg. ``"Server thread"``."""


# TODO: Nothing makes this until the hubs come back (#3-50.1).
# TODO: Check which fields kinds 4, 6 and 8 fill once a capture shows one (#3-47.2.1).
# Those kinds need a game that asks the player something, a sleep-capable template and a notice.
class LifecycleEvent(AMPObject):
    """The shard hub's `Lifecycle` event: a step in a shard's start, stop or update.

    Each kind fills a few fields and leaves the rest `None`:

    - `LifecycleKind.state_changed`: `state`, and on some a `message`, eg. ``"Waiting for the shard agent to report in"``.
    - `LifecycleKind.update_progress`: `task_id`, `stage_index` (from 1), `total_stages`, `progress_percent` and `message`.
    - `LifecycleKind.information`: the stage's name, with `task_id`, `stage_index` and `total_stages`; an
      `update_progress` with the same text follows it.
    - `LifecycleKind.update_complete`: `success` and `message`, just before the update's last `state_changed`.
    - `LifecycleKind.error`: `message`, `message_code` and `message_params`, eg. ``"agent.msg.executableNotFound"``,
      sent with a `state_changed` to `ShardState.failed_startup`.
    - `LifecycleKind.gateway_key_published`: `gateway_public_key` on a start through a gateway, and empty on the stop.
    - `LifecycleKind.startup_progress`: `progress_percent` and `message`, eg. ``"Preparing spawn area"``.

    .. versionadded:: 6.0.0
    """

    event_id: str
    shard_id: str
    tenant_id: str
    kind: Union[LifecycleKind, int]
    "A number the library doesn't know stays a plain int."
    state: Optional[Union[ShardState, int]]
    "The new status, on a `LifecycleKind.state_changed`."
    progress_percent: Optional[int]
    gateway_public_key: Optional[str]
    task_id: Optional[str]
    stage_index: Optional[int]
    total_stages: Optional[int]
    sub_task: Optional[str]
    version: Optional[str]
    sleep_available: Optional[bool]
    agent_version: Optional[str]
    success: Optional[bool]
    "Set on a `LifecycleKind.update_complete`."
    message: Optional[str]
    """An English sentence, eg. ``"Preparing spawn area"``."""
    message_code: Optional[str]
    """A translation key for the message, eg. ``"shards.msg.launchingAgent"``."""
    message_params: Optional[dict[str, str]]
    in_console: Optional[bool]
    timestamp: str


# TODO: Nothing makes this until the hubs come back (#3-50.1).
class NetworkStatus(AMPObject):
    """The spire hub's `NetworkStatus` event: a publication, tunnel or gateway changed its status.

    AMP sends `(kind, json)`, the status as a JSON string with PascalCase keys; the library parses it, so its keys
    become attributes like any other, eg. `PublicationId` is `publication_id`. Each `kind` fills its own fields and
    the rest are unset. A delete sends nothing for the publication or gateway itself.

    .. versionadded:: 6.0.0
    """

    kind: str
    """``"publication"``, ``"tunnel"`` or ``"gateway"``."""
    publication_id: str
    "A publication's ID, on `publication`."
    tunnel_id: str
    "A tunnel's ID, on `tunnel`."
    binding_id: str
    "A gateway's ID, on `gateway`."
    state: str
    """A publication's `PublicationState` name or a gateway's `GatewayState` name, eg. ``"Active"``."""
    target_spire_id: str
    "The spire a publication reaches its shard on, all zeros once it's disabled."
    resolved_port: int
    "A publication's port on the shard, 0 once it's disabled."
    tunnel_phase: Optional[str]
    "A publication's tunnel phase, through another spire."
    up: bool
    "If a tunnel is up."
    rtt_ms: int
    "A tunnel's round trip time."
    phase: str
    """A tunnel's phase, eg. ``"Provisioning"``, ``"Connecting"``, ``"AgentRejected"``, ``"Up"`` or ``"Releasing"``."""
    address: str
    """A gateway's address on its tunnel, eg. ``"10.83.0.10"``."""
    fault_spire_id: Optional[str]
    "The spire at fault, on `publication` and `tunnel`."
    error: Optional[str]
    """eg. ``"The file does not exist."`` while a first tunnel's agent is set up."""


class RunningTask(AMPObject):
    """One long job, such as a shard update: the tasks hub's `TaskUpsert` event, and each of ``GET /api/running-tasks``.

    A finished task leaves the list on its own after about 7 seconds. A failed one stays for about 30 minutes, unless
    `TaskModule.delete_running_task` dismisses it or a later task of its type on the same target ends.
    `TaskModule.get_task` reads AMP's own record of a task, with its steps.

    .. versionadded:: 6.0.0
    """

    id: str
    tenant_id: str
    type: str
    """eg. ``"ApplicationUpdate"``, ``"ShardClone"``, ``"ShardMigration"`` or ``"Snapshot"``."""
    name: str
    """eg. ``"Update my-shard"``; empty on a clone or a move, which name themselves with `name_code`."""
    name_code: Optional[str]
    """A translation key, eg. ``"tasks.migration.move"`` or ``"tasks.migration.clone"``."""
    name_params: Optional[dict[str, Any]]
    """Values for the `name_code` translation, eg. the shard's `name`."""
    message: Optional[str]
    "The current step, eg. a download, or why a move failed."
    message_code: Optional[str]
    """A translation key for the step, eg. ``"tasks.migration.stage.preparing"``."""
    message_params: Optional[dict[str, Any]]
    speed: Optional[str]
    """How fast a clone or a move copies, eg. ``"56.2 MB/s"``."""
    progress_percent: int
    is_indeterminate: bool
    state: Union[TaskState, int]
    "A number the library doesn't know stays a plain int."
    is_cancellable: bool
    "`True` on clones and moves, even once finished, and `False` on updates."
    is_primary: bool
    principal: Principal
    visibility: int
    target_type: str
    """eg. ``"Shard"``."""
    target_id: str
    correlation_id: WrappedID
    causation_action_id: Optional[WrappedID]
    action_id: WrappedID
    origin: int
    root_principal: Principal
    owner_spire_id: str
    "The spire running the task, the target one for a move or a clone."
    run_id: str
    sub_tasks: list[Any]
    started_at: str
    completed_at: Optional[str]
    cancellation_requested_at: Optional[str]
    updated_at: str
    is_terminal: bool
    "If the task has finished; only a finished task can be dismissed."


class ScheduleExecution(AMPObject):
    """One run of a schedule: the shard hub's `ScheduleRun` event, and each of ``GET .../schedules/{id}/history``.

    A run pushes ``"Running"``, then ``"Succeeded"`` with its `step_outcomes`; a disabled schedule's run pushes one
    ``"Skipped"``.

    .. versionadded:: 6.0.0
    """

    id: str
    schedule_id: str
    tenant_id: str
    shard_id: str
    event_payload: Optional[str]
    """The event that set off an event-triggered run, as a JSON string, eg. ``'{"EventId": ..., "ShardId": ...}'``;
    `None` for a run on a time trigger or a manual one."""
    canonical_fire_time: str
    timeout: str
    queued_at: str
    started_at: str
    completed_at: Optional[str]
    "`None` while it runs."
    status: str
    """``"Queued"``, ``"Running"``, ``"Succeeded"``, ``"CompletedWithErrors"``, ``"Failed"``, ``"TimedOut"`` or
    ``"Skipped"`` (a disabled schedule that was run)."""
    attempt_number: int
    worker_node: Optional[str]
    "The spire that ran it."
    error_message: Optional[str]
    step_outcomes: list[ScheduleStepOutcome]
    duration: Optional[str]
    "`None` while it runs."


class ShardMetrics(AMPObject):
    """One sample of a running shard's load: the shard hub's `Metrics` event, and each of ``GET .../metrics``.

    The hub sends one every 3 seconds while the shard runs.

    .. versionadded:: 6.0.0
    """

    shard_id: str
    tenant_id: str
    timestamp: str
    agent_version: str
    cpu_percent: float
    memory_mb: int
    memory_limit_mb: int
    "0 for no limit."
    io_read_kbps: float
    io_write_kbps: float
    active_users: int
    "-1 when the game doesn't say."
    max_users: int
    "0 when it's unknown or unlimited."
    # TODO: Check against a live capture; typed from AMP's OpenAPI `ShardMetricsSample` alone (#3-56.1z).
    # Every capture has it empty; it needs a template with a `Console.MetricsRegex`.
    custom: dict[str, float]
    """The game's own numbers read from its console, by name, eg. ``"TPS"``."""
    listening_ports: list[int]
    "The shard's ports that are listening now."


class ShardMigration(AMPObject):
    """A shard's latest move: the shard hub's `Migration` event, and ``GET /api/shards/{id}/migration``.

    The hub pushes it as the counters move, through `MigrationStatus.copying`, `validating` and `awaiting_cleanup`.

    .. versionadded:: 6.0.0
    """

    shard_id: str
    tenant_id: str
    owner_spire_id: str
    "The spire running the move, the target one."
    run_id: str
    "The move's `RunningTask.run_id` too."
    source_datastore_id: str
    target_datastore_id: str
    source_shard_id: str
    source_spire_id: str
    "All zeros on a move between datastores of one spire."
    target_spire_id: str
    "All zeros on a move between datastores of one spire."
    source_path: str
    "The shard's old folder on a move between datastores of one spire; empty on a move between spires."
    target_path: str
    """The shard's folder on the target, eg. ``"/opt/cubecoders/amp3/data/Datastores/Default/my-shard-ef6e621c"``."""
    status: Union[MigrationStatus, int]
    "A number the library doesn't know stays a plain int."
    files_total: int
    "0 while copying and the real count once done; a shard with no files reads 0 throughout."
    files_done: int
    bytes_total: int
    "0 while copying and the real count once done."
    bytes_done: int
    error: Optional[str]
    """An English sentence on a failed move, eg. ``"The move failed. The server was left stopped on its source spire. ..."``,
    or ``"Cancelled."`` after `ShardModule.cancel_shard_migration`."""
    started_at: str
    finished_at: Optional[str]
    started_by_user_id: str
    start_after_move: bool
    """If the move starts the shard on the target once it's done: the `start_after_move` it was started with, or else
    its `stop_if_running`. AMP clears it to `False` once it has started the shard, so a finished move that did reads
    `False`."""
    is_active: bool
    "If the move is still running; `True` only while copying."
    blocks_launch: bool
    "If the shard can't be started meanwhile; `True` only while copying."


# TODO: Check against the hub captures and `ShardModule.get_shard_users` once a player joins (#3-47.2.1).
# The fields are the web panel's: it reads `id`, `name` and `sessionId`.
class ShardPlayer(AMPObject):
    """A player on a shard: each of ``GET /api/shards/{id}/users``, the shard hub's `UserRoster` list, and its
    `UserJoined` and `UserLeft` events.

    .. versionadded:: 6.0.0
    """

    id: str
    "The player's ID in the game, eg. a Minecraft UUID; `id_kind` says which."
    name: str
    session_id: str
    "Empty on `minecraft-java`."
    endpoint: Optional[str]
    """The address and port the player connected from, as the shard sees it, `None` when it's not known. Under rootless
    Podman that is the container network's address, eg. ``"10.0.2.100:58590"``, not the player's own."""
    joined_at: str
    "When the player joined, an ISO 8601 time."
    id_kind: str
    """What `id` is, eg. ``"minecraft-uuid"``."""


class ShardSnapshots(AMPObject):
    """A shard's snapshots as a tree and any restore in progress: the shard hub's `Snapshot` event, and ``GET .../snapshots``.

    .. versionadded:: 6.0.0
    """

    shard_id: str
    tenant_id: str
    nodes: list[Snapshot]
    "Each one's `parent_id` links the tree."
    head_id: Optional[str]
    "The newest snapshot."
    settings: SnapshotSettingsResponse
    restoring_id: Optional[str]
    restore_stage: Union[SnapshotStage, int]
    restore_processed: int
    restore_total: int
    restore_owner_spire_id: str
    "All zeros when no restore has run."
    restore_run_id: str


class ShardStatus(AMPObject):
    """A shard's live state: the shard hub's `ShardStateChanged` event, and ``GET /api/shards/{id}/state``.

    The hub sends it often, also with an unchanged `status` when only the heartbeat or the metrics moved.

    .. versionadded:: 6.0.0
    """

    shard_id: str
    tenant_id: str
    status: Union[ShardState, int]
    "A number the library doesn't know stays a plain int."
    revision: int
    metrics: Optional[ShardStateMetrics]
    "`None` while stopped."
    last_heartbeat: str
    active_task_id: Optional[str]
    # TODO: Check against a live capture; typed from AMP's OpenAPI `ShardState` alone (#3-56.1o, #3-56.1z).
    # Every capture has it `None`, even while running.
    process_id: Optional[int]
    "The game's process ID, `None` while stopped."
    running_version: Optional[str]
    agent_version: Optional[str]
    last_error_message: Optional[str]
    last_error_code: Optional[str]
    """eg. ``"agent.msg.executableNotFound"``."""
    last_error_params: Optional[dict[str, str]]
    status_message: Optional[str]
    status_code: Optional[str]
    """eg. ``"shards.msg.launchStage.container"``."""
    status_params: Optional[dict[str, str]]
    started_at: Optional[str]
    sleep: Optional[ShardSleepStatus]
    is_running: bool
    is_stopped: bool
    awaits_licence: bool
    """If the shard is held waiting on its game's licence or not.

    - A start no person was waiting on, eg. a scheduled start, is held before anything launches.
    - While the shard is held, its `status` reads `ShardState.awaiting_user_action`.
    - `ShardModule.accept_shard_eula` or `ShardModule.decline_shard_eula` sets `status` back to `ShardState.stopped`.
      Accepting doesn't start the shard.
    """
    accepts_traffic: bool
    is_busy: bool


class Snapshot(AMPObject):
    """One snapshot (a backup), from `ShardSnapshots.nodes`; taking or restoring one answers with it too.

    .. versionadded:: 6.0.0
    """

    id: str
    parent_id: Optional[str]
    "The snapshot this one builds on, `None` for the first."
    kind: Union[SnapshotKind, int]
    content: Union[SnapshotContent, int]
    trigger: int
    "eg. 0 (taken by a user) or 3 (the one AMP takes before a restore)."
    status: Union[SnapshotState, int]
    name: str
    description: str
    """AMP fills an empty one, eg. ``"Partial backup of app configuration."``."""
    sticky: bool
    "Doesn't stop a delete."
    failure_reason: str
    skipped_files: list[str]
    skipped_count: int
    archive_missing: bool
    created_at: str
    created_by_user_id: str
    size_mb: int
    uncompressed_mb: int
    file_count: int
    owner_spire_id: str
    run_id: str
    stage: Union[SnapshotStage, int]
    processed_files: int
    total_files: int
    datastore_id: str
    zip_file_name: str


class SpirePresence(AMPObject):
    """One spire and if it's online: the spire hub's `SpirePresence` event, and each of ``GET /api/spires/roster``.

    The hub pushes one when a spire goes offline or comes back, some seconds after it does.

    .. versionadded:: 6.0.0
    """

    spire: SpireResponse
    online: bool
    last_seen: Optional[str]
    "The spire's last contact, when it went offline; `None` if it never made one."
    version: Optional[str]
    "The AMP version the spire last reported, `None` if it never has."
    behind: bool
    "If the spire runs an older AMP than the panel."
    installation_version: str


class SpireStatus(AMPObject):
    """A spire's live load: the spire hub's `SpireState` event, and ``GET /api/spires/{id}/state``.

    The hub sends one every 3 seconds for each joined spire. An unknown spire ID answers the REST call with 200,
    `online` `False`, zeros and no `platform`, not 404.

    .. versionadded:: 6.0.0
    """

    spire_id: str
    online: bool
    last_heartbeat: str
    shard_count: int
    cpu_usage_percent: float
    memory_used_mb: int
    memory_total_mb: int
    network_in_kbps: float
    network_out_kbps: float
    disk_active_percent: Optional[float]
    bus_latency_ms: float
    platform: Optional[SpirePlatform]
