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
    "SpireReference",
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
    _repr_names: ClassVar[tuple[str, ...]] = ("id", "shard_id", "spire_id", "name", "status", "state", "kind", "text")
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
    """eg. ``"line"``, ``"info"``, ``"error"`` or ``"marker"``, which marks a change of `state`."""
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


# TODO: Check the kinds other than 0 and 7, and which fields each fills, against the hub captures (#3-47.2.1).
# The fields are from the vm3 captures; the web panel's code reads `stageIndex`, `totalStages`, `subTask` and `success` too.
class LifecycleEvent(AMPObject):
    """The shard hub's `Lifecycle` event: a step in a shard's start, stop or update.

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


# TODO: Type `json` once the hub captures show one (#3-47.2.1).
# The event is sent as two arguments, `(kind, json)`; the web panel only refetches the endpoints on it.
class NetworkStatus(AMPObject):
    """The spire hub's `NetworkStatus` event: something changed in how the panel is reached.

    .. versionadded:: 6.0.0
    """

    kind: str
    json: str
    "A JSON document as a string."


class RunningTask(AMPObject):
    """One long job, such as a shard update: the tasks hub's `TaskUpsert` event, and each of ``GET /api/running-tasks``.

    A finished task leaves the list on its own after about 7 seconds. A failed move's task stays until
    `TaskModule.delete_running_task`.

    .. versionadded:: 6.0.0
    """

    id: str
    tenant_id: str
    type: str
    """eg. ``"ApplicationUpdate"``, ``"ShardClone"`` or ``"ShardMigration"``."""
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


# TODO: Check the hub's `ScheduleRun` payload against this once the hub captures show one (#3-47.2.1).
# The web panel's code reads `scheduleId` and `id` from it; the fields are the REST history's.
class ScheduleExecution(AMPObject):
    """One run of a schedule: the shard hub's `ScheduleRun` event, and each of ``GET .../schedules/{id}/history``.

    .. versionadded:: 6.0.0
    """

    id: str
    schedule_id: str
    tenant_id: str
    shard_id: str
    event_payload: Optional[Any]
    canonical_fire_time: str
    timeout: str
    queued_at: str
    started_at: str
    completed_at: str
    status: str
    """eg. ``"Succeeded"`` or ``"Skipped"`` (a disabled schedule that was run)."""
    attempt_number: int
    worker_node: Optional[str]
    "The spire that ran it."
    error_message: Optional[str]
    step_outcomes: list[ScheduleStepOutcome]
    duration: str


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
    io_read_kbps: float
    io_write_kbps: float
    active_users: int
    max_users: int
    custom: dict[str, Any]
    listening_ports: list[int]


# TODO: Check the hub's `Migration` payload against this once the hub captures show one (#3-47.2.1).
# The web panel's code reads `status` and `shardId` from it; the fields are the REST reply's.
class ShardMigration(AMPObject):
    """A shard's latest move: the shard hub's `Migration` event, and ``GET /api/shards/{id}/migration``.

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
    # TODO: Drop the second half once the record says what AMP does (U22d).
    # AMP 3.0.0.6 reads `False` for a running shard that moves fine, then starts it on the target.
    start_after_move: bool
    """`True` on a move that stopped the shard and failed. A running shard that moves fine reads `False`, yet starts
    on the target."""
    is_active: bool
    "If the move is still running; `True` only while copying."
    blocks_launch: bool
    "If the shard can't be started meanwhile; `True` only while copying."


# TODO: Check against the hub captures and `ShardModule.get_shard_users` once a player joins (#3-47.2.1).
# The fields are the web panel's: it reads `id`, `name` and `sessionId`.
class ShardPlayer(AMPObject):
    """A player on a shard: each of the shard hub's `UserRoster` list, and its `UserJoined` and `UserLeft` events.

    .. versionadded:: 6.0.0
    """

    id: str
    name: str
    session_id: str


# TODO: Check the hub's `Snapshot` payload against this once the hub captures show one (#3-47.2.1).
# The web panel's code treats it as the same graph as the REST reply.
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
    process_id: Optional[Any]
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


# TODO: Check against the hub captures once a spire joins or leaves (#3-47.2.1).
# The fields are the web panel's: `{spire: {id, displayName}, online}`.
class SpirePresence(AMPObject):
    """The spire hub's `SpirePresence` event: a spire came online or went offline.

    .. versionadded:: 6.0.0
    """

    spire: SpireReference
    online: bool


class SpireReference(AMPObject):
    """A spire named inside another event, eg. `SpirePresence.spire`.

    .. versionadded:: 6.0.0
    """

    id: str
    display_name: str


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
