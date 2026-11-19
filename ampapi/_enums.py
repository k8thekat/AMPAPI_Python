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

from enum import IntEnum, IntFlag, StrEnum

__all__ = (
    "AuditOrigin",
    "AuditSeverity",
    "CloneContent",
    "GatewayState",
    "LifecycleKind",
    "MigrationStatus",
    "PublicationState",
    "ShardState",
    "SnapshotContent",
    "SnapshotKind",
    "SnapshotStage",
    "SnapshotState",
    "TaskState",
)


class AuditOrigin(IntEnum):
    """How an audit event came about, named as the web panel names it. AMP sends the number.

    An audit event's `origin` and an origin count's `origin` hold the number. The `origin` filter of
    :meth:`AuditModule.get_audit_events` takes the name instead, eg. ``"UserFlow"`` (see `AuditOriginName`).

    - `system`: AMP acted by itself. An event written before AMP kept an origin reads `system` too.
    - `user`: a user acted directly, eg. through a click in the web panel.
    - `user_flow`: AMP acted inside a flow that a user's request started, eg. the steps of an update.
    - `scheduled`: a schedule acted.
    - `impersonation`: a user acted as another user.

    .. versionadded:: 6.0.0
    """

    system = 0
    user = 1
    user_flow = 2
    scheduled = 3
    impersonation = 4


class AuditSeverity(IntEnum):
    """How much an audit event matters, named as the web panel names it. AMP sends the number.

    An audit event's `severity` and a flow's `maxSeverity` hold the number. The `min_severity` filter of
    :meth:`AuditModule.get_audit_events` takes the name instead, eg. ``"Warning"`` (see `AuditSeverityName`).

    .. versionadded:: 6.0.0
    """

    info = 0
    warning = 1
    security = 2


class CloneContent(IntFlag):
    """What :meth:`Panel.clone_shard` copies, named as the web panel's clone dialog names them.

    AMP also took 7 (every snapshot flag set) and copied everything, so the server may read it as `SnapshotContent`.

    .. versionadded:: 6.0.0
    """

    configuration = 1
    data = 2
    both = 3


# TODO: Drop `fault` from the order once a connecting gateway's `state` reads `Connecting` rather than `Fault` (U26b).
# AMP 3.0.0.6 reads `Fault` while a new gateway's tunnel still connects.
class GatewayState(StrEnum):
    """A gateway's `state`, named as the web panel names it. AMP sends the name, which each member equals.

    A new gateway's `state` reads `provisioning`, then `fault` while the gateway's tunnel connects, then
    `awaiting_shard` until a shard that was running restarts, then `connecting` and `active`. The web panel's code also
    has `disabled`.

    .. versionadded:: 6.0.0
    """

    active = "Active"
    awaiting_shard = "AwaitingShard"
    connecting = "Connecting"
    disabled = "Disabled"
    fault = "Fault"
    provisioning = "Provisioning"


# TODO: Check kinds 4, 6 and 8 once a capture shows one (#3-47.2.1).
# Their names are the web panel's; every other kind was seen live.
class LifecycleKind(IntEnum):
    """A shard hub `Lifecycle` event's `kind`, named as the web panel names it. AMP sends the number.

    .. versionadded:: 6.0.0
    """

    state_changed = 0
    update_progress = 1
    update_complete = 2
    error = 3
    user_action_required = 4
    gateway_key_published = 5
    sleep_status = 6
    startup_progress = 7
    notice = 8
    information = 9


class MigrationStatus(IntEnum):
    """A shard move's `status`, named as the web panel's `ShardMigrationStatus` names it. AMP sends the number.

    - A move's `status` reads `copying` while the shard's files copy.
    - The `status` reads `awaiting_cleanup` once the move is done. A move can be done within one round trip.
    - The `status` reads `failed` once the move has failed, or once :meth:`ShardModule.cancel_shard_migration` stopped
      the move. A cancelled move's `error` reads ``"Cancelled."``.
    - The record stays until :meth:`ShardModule.delete_shard_migration`.

    The other members are from the web panel's code.

    .. versionadded:: 6.0.0
    """

    copying = 0
    validating = 1
    awaiting_cleanup = 2
    failed = 3
    interrupted = 4
    complete = 5


# TODO: Drop the first publication sentence once AMP stops reading `TunnelFault` while the tunnel is set up (U26a).
# AMP 3.0.0.6 reads `TunnelFault` "The file does not exist." for about a minute on a first publication.
class PublicationState(StrEnum):
    """A port forward's `state`, named as the web panel names it. AMP sends the name, which each member equals.

    AMP sends `tunnel_provisioning`, `active`, `disabled` and `shard_stopped`. A first publication's `state` reads
    `tunnel_fault` for about a minute, then `active`. The other members are from the web panel's code.

    .. versionadded:: 6.0.0
    """

    active = "Active"
    disabled = "Disabled"
    error = "Error"
    pending = "Pending"
    port_conflict = "PortConflict"
    port_private = "PortPrivate"
    port_ref_missing = "PortRefMissing"
    shard_missing = "ShardMissing"
    shard_stopped = "ShardStopped"
    tunnel_down = "TunnelDown"
    tunnel_fault = "TunnelFault"
    tunnel_provisioning = "TunnelProvisioning"
    tunnel_unavailable = "TunnelUnavailable"


class ShardState(IntEnum):
    """A shard's `status`, named as the web panel names it. AMP sends the number.

    ``GET /api/shards/{id}/state`` sends eg. 0, 3, 20, 25 and 30, and the console's markers eg. 15 and 100.

    .. versionadded:: 6.0.0
    """

    stopped = 0
    launching_agent = 3
    pre_start = 5
    configuring = 10
    starting = 15
    running_not_ready = 20
    running_ready = 25
    stopping = 30
    preparing_sleep = 50
    sleeping = 55
    installing_updating = 100
    awaiting_user_action = 110
    failed_install = 200
    failed_startup = 300


class SnapshotContent(IntFlag):
    """What a snapshot holds, named as the web panel names it; the flags add up, eg. 7 is all three.

    .. versionadded:: 6.0.0
    """

    none = 0
    game_state = 1
    base_data = 2
    amp_config = 4


class SnapshotKind(IntEnum):
    """A snapshot's `kind`, named as the web panel names it.

    .. versionadded:: 6.0.0
    """

    full = 0
    partial = 1


class SnapshotStage(IntEnum):
    """How far a snapshot or a restore has got, named as the web panel names it.

    .. versionadded:: 6.0.0
    """

    none = 0
    gathering = 1
    processing = 2
    finalizing = 3


class SnapshotState(IntEnum):
    """A snapshot's `status`, named as the web panel names it.

    .. versionadded:: 6.0.0
    """

    pending = 0
    running = 1
    complete = 2
    failed = 3


# TODO: Drop the cancelled clone sentence once AMP honours a clone's cancel (U25).
# AMP 3.0.0.6 answers the cancel with 202, and the clone carries on copying.
class TaskState(IntEnum):
    """A running task's `state`, named as the web panel names it.

    - A task's `state` reads `waiting` while an update downloads, and `running` while a clone or a move copies.
    - The `state` reads `succeeded` when the task is finished, `failed` for a failed move or update, and `cancelled`
      for a cancelled move.
    - A cancelled clone's `state` reads `cancelling`, then `running` again, and the clone finishes anyway.

    .. versionadded:: 6.0.0
    """

    running = 0
    waiting = 1
    user_action_required = 2
    succeeded = 3
    failed = 4
    cancelling = 5
    cancelled = 6
