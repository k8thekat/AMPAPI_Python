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
    ShardContainerMode,
    ShardState,
    SnapshotContent,
    SnapshotKind,
    SnapshotStage,
    SnapshotState,
    TaskState,
    TimeFormat,
    UserExperienceLevel,
)
from ._types import (  # noqa: TC001
    CodedErrorResponse,
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
    "Preferences",
    "RunningTask",
    "ScheduleExecution",
    "ShardInfra",
    "ShardInfraSaveResult",
    "ShardInfraSettings",
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


class Preferences(AMPObject):
    """The logged in user's web panel preferences, from ``GET /api/users/me/preferences``.

    - :meth:`AccountModule.update_preferences`, :meth:`AccountModule.add_favourite` and
      :meth:`AccountModule.delete_favourite` answer with all of the preferences too.
    - A preference never set is `None`, which means the web panel's default.

    .. versionadded:: 6.0.0
    """

    theme: Optional[str]
    """The web panel's theme, eg. ``"dark"``."""
    locale: Optional[str]
    """The language code, eg. ``"en-GB"``."""
    favourite_app_slugs: list[str]
    """The slugs of the logged in user's favourite templates, newest first, eg. ``["teeworlds"]``.
    - The web panel lists the favourites first among the templates.
    - AMP doesn't check the slugs against the templates."""
    pinned_shard_ids: list[str]
    "The IDs of the shards pinned to the web panel's overview, in the order they were pinned."
    notify_on_state_change: Optional[bool]
    "If the web panel notifies the logged in user when a shard's state changes or not."
    notify_on_update_available: Optional[bool]
    "If the web panel notifies the logged in user when an update is available or not."
    compact_shard_header: Optional[bool]
    "If a shard's page shows a compact header without the live graph or not."
    hide_unrouted_shards: Optional[bool]
    """If the networking page hides shards that have no route or not.
    - `None` means off."""
    hide_private_ports: Optional[bool]
    """If the networking page hides the ports a game doesn't expose publicly or not.
    - `None` means on, as a private port can't be published."""
    file_details_width: Optional[int]
    """The width in pixels of the file manager's details pane, `None` for the default width.
    - The web panel keeps the width in range as it reads it, so any number is safe."""
    amp_experience: Optional[Union[UserExperienceLevel, str]]
    """How familiar the logged in user said they are with AMP at their first login, `None` if never asked.
    - A name the library doesn't know stays a plain str."""
    show_tutorials: Optional[bool]
    """If the web panel offers its guided tutorials or not.
    - AMP sets it at the first login from `amp_experience`: on for new and returning users, off for experienced ones."""
    tutorial_prompt_dismissed: Optional[bool]
    """If the logged in user turned down the getting started tutorial for good, or finished it.
    - It stops only the automatic offer. `show_tutorials` still governs each page's tutorial button.
    - `None` or `False` means the web panel still offers the tutorial."""
    tutorials_completed: list[str]
    "The IDs of the tutorials the logged in user ran to the end."
    accessibility_hints_enabled: Optional[bool]
    """If the web panel shows extra accessibility hints or not, eg. how to work its confirm slider by keyboard.
    - `None` if never asked."""
    onboarding_completed: Optional[bool]
    """If the logged in user finished the first login's onboarding or not.
    - `None` or `False` shows the onboarding at the next login."""
    reduced_motion: Optional[bool]
    """If the web panel cuts animation that isn't needed or not.
    - It adds to the browser's own reduced motion setting, and either one turns it on.
    - `None` or `False` follows the browser's setting alone."""
    analytics_enabled: Optional[bool]
    """If the logged in user agreed to anonymous product analytics or not.
    - `None` or `False` means no analytics."""
    streamer_mode: Optional[bool]
    """If the web panel blurs each IP address it shows or not, for streaming or recording the screen.
    - Console and log text is shown as it is."""
    time_format: Optional[Union[TimeFormat, str]]
    """How the web panel writes clock times, 12 or 24 hour.
    - `None` reads as `TimeFormat.system`, which follows the logged in user's language.
    - A name the library doesn't know stays a plain str."""


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
    # TODO: Check a failed run's `error` against a live capture; typed from AMP 3.0.2's OpenAPI `JobExecution` alone (#3-65).
    # The one run read succeeded, with `error` `None`.
    error: Optional[CodedErrorResponse]
    "Why the run failed, as its first error that no step handled; `None` for a run without such an error."
    step_outcomes: list[ScheduleStepOutcome]
    duration: Optional[str]
    "`None` while it runs."


class ShardInfra(AMPObject):
    """How a shard runs and what its spire and template allow, from ``GET /api/shards/{id}/infra``.

    :meth:`ShardModule.update_shard_infra` changes the `settings`.

    .. versionadded:: 6.0.0
    """

    settings: ShardInfraSettings
    spire_name: str
    "The name of the spire the shard runs on."
    spire_is_linux: bool
    "If the shard's spire runs Linux or not."
    container_policy: int
    """The template's container support and preference for each system, as flags, eg. 6.
    - It only recommends a `ShardInfraSettings.container_mode`."""
    logical_cores: int
    "The number of logical CPU cores on the shard's spire."
    template_os: int
    "The systems the template runs on, as flags: 1 Windows, 2 Linux."
    supports_sleep: bool
    """If the shard's template can sleep or not.
    - `ShardInfraSettings.sleep_mode` does nothing on a template that can't sleep."""
    tracks_users: bool
    """If the game reports players connecting or not.
    - Analytics and geo filtering do nothing on a game that doesn't report players."""
    reports_addresses: bool
    """If the game also reports the address a player connected from or not.
    - Geo filtering and the analytics country breakdown need the address."""
    disk_enforce_percent: int
    """How far into `ShardInfraSettings.disk_limit_mb` a disk scan counts the shard as over its limit, in percent,
    eg. 105.
    - Past it, AMP also refuses an upload to the shard, from AMP's docs and not seen live."""
    max_minimum_session_seconds: int
    "The most `ShardInfraSettings.minimum_session_time_for_retention` can be set to, in seconds, eg. 6000."


class ShardInfraSettings(AMPObject):
    """A shard's settings for how it runs: container, limits, start up, analytics and geo filtering.

    - `ShardInfra.settings` holds them, from :meth:`ShardModule.get_shard_infra`.
    - :attr:`Shard.infra_settings` holds the settings a shard was made with.
    - :meth:`ShardModule.update_shard_infra` changes them.

    .. versionadded:: 6.0.0
    """

    shard_id: str
    tenant_id: str
    start_on_boot: bool
    """If the shard starts when its spire's machine starts or not.
    - With it on, the shard starts whether it was running or stopped when the machine went down.
    - With it off, the shard stays stopped, even if it was running when the machine went down.
    - A restart of AMP alone starts no shard."""
    auto_restart_on_crash: bool
    """If AMP restarts the game when it exits without a stop being asked for or not.
    - Only a game that was ready and ran for at least 5 minutes is restarted."""
    startup_order: int
    """The order shards start in when their spire's machine starts, lowest first, 100 by default.
    - It orders only the shards with `start_on_boot` on.
    - The shards start one at a time, each once the shard before it is running.
    - Shards with the same order start by name."""
    sleep_mode: bool
    """If the shard sleeps while no player is connected or not.
    - While asleep, AMP stops the game and holds its ports, so the shard still shows online.
    - AMP starts the game again when a player tries to connect.
    - It does nothing unless the template can sleep, see `ShardInfra.supports_sleep`.
    - A change takes effect when the shard next starts."""
    advertised_address: str
    """The address players are given for the shard, eg. ``"play.example.com"`` or ``"play.example.com:25565"``.
    - ``""`` lets AMP work out the address itself.
    - AMP hands the address out as it's given, eg. for a domain, an SRV record or a proxy in front of the shard."""
    advertised_address_includes_port: bool
    """If AMP adds the shard's port to `advertised_address` or not.
    - `False` suits an SRV record or a proxy, where players connect to the host alone.
    - AMP ignores it when `advertised_address` already has a port."""
    container_mode: Union[ShardContainerMode, str]
    """How the shard runs, straight on its spire or in a container.
    - `ShardContainerMode` says what each mode does.
    - A name the library doesn't know stays a plain str."""
    container_image_override: Optional[str]
    """The container image to run instead of the template's, `None` for the template's image.
    - An image from AMP's own repository, ``cubecoders/amp3base``, has to name a tag AMP builds, eg.
      ``"docker.io/cubecoders/amp3base:java-25"``.
    - An image from AMP's own repository that AMP doesn't build, eg. a retired tag or a digest, is stored, but the shard
      fails at its next start.
    - AMP pulls an image from any other repository and runs it as given.
    - An image that isn't built for AMP, eg. ``"docker.io/library/debian:trixie-slim"``, fails to start."""
    allow_lan_access: bool
    """If the shard's container can reach the spire's local network or not, `False` by default.
    - With it off, a Podman container on a Linux spire reaches only the internet, AMP's bus and the spire's DNS
      resolvers. AMP refuses the private, carrier-grade NAT and link-local address ranges, and the spire's own IPv6
      networks.
    - With it on, the container can reach the other machines on the spire's local network, eg. for a game that needs a
      service there.
    - A change takes effect when the shard's container is made again, at a start after a stop. A restart keeps the
      container, so it keeps the old setting.
    - With it off, AMP applies the filter before anything runs in the container, with the `nft` of the shard's image
      when it's one of AMP's, and of AMP's default image otherwise. If that fails, the update or start is refused with
      `shards.error.containerLanFilterFailed` and the shard isn't started.
    - A native shard isn't filtered, from AMP's docs and not seen live."""
    memory_limit_mb: int
    """The shard's memory limit in MiB, 0 for no limit.
    - AMP sets the limit on the container, or on a native shard's systemd unit.
    - AMP stores a negative number without complaint.
    - A container with a negative memory limit runs with no memory limit."""
    memory_reservation_mb: int
    """The container's soft memory limit in MiB, 0 for none.
    - AMP refuses a reservation above `memory_limit_mb`.
    - A native shard has no soft memory limit."""
    memory_swap_mb: int
    """The container's memory and swap together in MiB.
    - -1 for no limit.
    - 0 for the container runtime's default, about twice `memory_limit_mb`.
    - AMP refuses any other number below `memory_limit_mb`.
    - AMP ignores the swap while `memory_limit_mb` is 0.
    - A native shard has no swap limit."""
    cpu_limit: float
    """The shard's CPU limit in cores, eg. 1.5, 0 for no limit.
    - AMP sets the limit on the container, or on a native shard's systemd unit."""
    max_users_cap: int
    """The most players AMP lets in at once, whatever the shard's `$MaxUsers` setting says, 0 for no cap.
    - A cap below `$MaxUsers` lowers `$MaxUsers` at once, with the shard running or stopped.
    - A running game's config file keeps the old number, eg. ``max-players`` in a Minecraft ``server.properties``.
    - A cap above `$MaxUsers` leaves `$MaxUsers` as it is.
    - AMP refuses a `$MaxUsers` above the cap, see :meth:`ShardModule.set_shard_settings`.
    - A cap suits hosting that sells a set number of player slots."""
    enable_analytics: bool
    """If AMP collects analytics on the players who join or not, where the game reports them.
    - With it off, the shard adds no sessions to analytics."""
    user_specific_data: bool
    """If analytics keeps data on each player or not, eg. who plays the most.
    - The players have to be told that analytics is in use.
    - With it off, AMP doesn't look up a player's address, so each session has an unknown country.
    - With it off, player names and IDs are left out too.
    - Turning it on doesn't change the sessions already recorded."""
    minimum_session_time_for_retention: int
    "The shortest session in seconds that analytics keeps, to leave out very short sessions."
    enable_geo_filtering: bool
    """If AMP blocks players from certain countries or not.
    - AMP sends `geo_filter_kick_command` to the game's console for a player from a country the shard doesn't accept.
    - It needs a game that logs connections with an address and takes a kick command."""
    blocked_countries: list[str]
    """The countries to block, as ISO 3166-1 alpha-2 codes, eg. ``["US"]``."""
    allowed_countries: list[str]
    """The countries to allow, as ISO 3166-1 alpha-2 codes.
    - An empty list allows every country that isn't in `blocked_countries`."""
    block_unknown_countries: bool
    """If AMP also blocks players whose country can't be worked out or not.
    - That includes every player who comes through a published port without a gateway, as the game sees the tunnel's
      address."""
    geo_filter_kick_message: str
    """The message a player blocked by geo filtering gets.
    - ``{CountryCode}`` and ``{CountryName}`` are replaced with the player's country."""
    geo_filter_kick_command: str
    """The console command that disconnects a player blocked by geo filtering, eg. ``'kick "{UserName}" "{Reason}"'``.
    - ``{UserName}``, ``{UserID}``, ``{Reason}``, ``{CountryCode}`` and ``{CountryName}`` are replaced.
    - ``{Reason}`` is `geo_filter_kick_message`."""
    disk_limit_mb: int
    """The disk limit in MB for the shard's folder, 0 for no limit.
    - It holds for a shard in a container and a native shard alike.
    - AMP checks the limit at the spire's disk scans, so the shard can go over it between scans.
    - Near the limit, the shard's `limitLevel` reads ``"Critical"`` in :meth:`ShardModule.get_shard_disk` and
      :meth:`SpireModule.get_spire_usage`.
    - AMP gives no other warning, neither a platform warning nor an entry in :meth:`Panel.get_shards_awaiting_action`.
    - AMP stops the shard at the first disk scan that finds it over the limit.
    - A scan counts the shard as over the limit at `ShardInfra.disk_enforce_percent` of it, from AMP's docs."""
    import_config_files_from_sftp: bool
    """If AMP reads a config file it manages back into the shard's settings when the file is written over SFTP or not.
    - With it on, the change shows in the shard's settings within seconds.
    - With it off, AMP writes the shard's settings over the file's change at the shard's next start."""
    extra_environment: dict[str, str]
    """Extra environment variables for the game's process or container, by name.
    - They're added to the template's variables, and these win where both have a name."""
    updated_at: str
    "When the settings last changed, an ISO 8601 time."
    updated_by_user_id: str
    "The ID of the user who last changed the settings."


class ShardInfraSaveResult(ShardInfraSettings):
    """A shard's settings for how it runs as AMP saved them, from ``PATCH /api/shards/{id}/infra``.

    .. versionadded:: 6.0.0
    """

    # TODO: Check against a live capture; typed from AMP's OpenAPI `ShardInfraSaveResult` alone (#3-56.1z).
    # Every capture has it `None`; it needs a game that refuses to lower its `$MaxUsers`.
    clamp_refused: Optional[CodedErrorResponse]
    """Why the game's `$MaxUsers` wasn't lowered to a new `max_users_cap`, eg. ``"shards.error.maxUsersClampRefused"``.
    - `None` when `$MaxUsers` was lowered, or didn't need to be.
    - AMP saves the cap either way."""


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
    sign_in_url: Optional[str]
    """The https address a game's sign-in prompt asks a person to visit, while the shard waits on the sign-in.
    - AMP sets it only for an address on a host the template names for its sign-in, eg. a ``"hytale"`` shard's update.
    - `None` once the shard stops waiting, and for any other prompt."""
    status_message: Optional[str]
    status_code: Optional[str]
    """eg. ``"shards.msg.launchStage.container"``."""
    status_params: Optional[dict[str, str]]
    started_at: Optional[str]
    # TODO: Reword the field doc once a running shard's state says if the shard can sleep (U18b).
    # AMP 3.0.0 sent `available` False and the reason.
    # AMP 3.0.1 sends `None` on a running `minecraft-java` shard.
    sleep: Optional[ShardSleepStatus]
    """If the shard can sleep, and why not.
    - `None` doesn't mean the shard can sleep, as AMP 3.0.1 sends `None` for a running shard that can't."""
    is_running: bool
    is_stopped: bool
    awaits_licence: bool
    """If the shard is held waiting on its game's licence or not.

    - A start no person was waiting on, eg. a scheduled start, is held before anything launches.
    - A restart of the stopped shard is held too, though AMP answers the restart with 409.
    - A person's start is refused with 409 and isn't held, so the shard stays stopped.
    - While the shard is held, its `status` reads `ShardState.awaiting_user_action`.
    - `ShardModule.accept_shard_eula` or `ShardModule.decline_shard_eula` sets `status` back to `ShardState.stopped`.
      Accepting doesn't start the shard.
    """
    awaits_settings: bool
    """If the shard is held waiting for its required settings to be given a value or not.
    - A start no person was waiting on, eg. a scheduled start, is held before anything launches.
    - A person's start and a restart are refused with 409 and aren't held, so the shard stays stopped.
    - While the shard is held, its `status` reads `ShardState.awaiting_user_action`, and its `last_error_code` reads
      ``"shards.error.settingRequiredBeforeStart"`` with the settings in `last_error_params`.
    - `ShardModule.set_shard_settings` giving each required setting a value sets `status` back to
      `ShardState.stopped`. It doesn't start the shard."""
    awaits_person: bool
    """If the shard is held waiting on a person or not, for its licence (`awaits_licence`) or its required settings
    (`awaits_settings`).
    - A held shard is listed by `Panel.get_shards_awaiting_action`.
    - It stays `False` while a game's sign-in prompt waits, see `sign_in_url`."""
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
    # TODO: Check a failed snapshot's `failure` against a live capture; typed from AMP 3.0.2's OpenAPI `ShardSnapshot` alone (#3-65).
    # Every snapshot captured succeeded, with `failure` `None`.
    failure: Optional[CodedErrorResponse]
    "Why the snapshot failed, when its `status` is `SnapshotState.failed`; `None` for a snapshot that didn't fail."
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
    last_seen_age_seconds: Optional[float]
    "How many whole seconds ago the spire was last seen, by the panel's clock; `None` if it never was."


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
    report_age_seconds: Optional[float]
    """How many seconds ago the panel that answered received the spire's full report, which these figures come from,
    by that panel's clock; `None` before the panel has received a report."""
    report_stale: bool
    """If the spire's latest full report is older than the panel allows or not.
    - With it `True`, the figures and `platform` may be out of date."""
