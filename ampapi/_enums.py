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
    "CloneContent",
    "GatewayState",
    "MigrationStatus",
    "PublicationState",
    "ShardState",
    "SnapshotContent",
    "SnapshotKind",
    "SnapshotStage",
    "SnapshotState",
    "TaskState",
)


class CloneContent(IntFlag):
    """What :meth:`ShardModule.clone_shard` copies, named as the web panel's clone dialog names them.

    AMP also took 7 (every snapshot flag set) and copied everything, so the server may read it as `SnapshotContent`.

    .. versionadded:: 6.0.0
    """

    configuration = 1
    data = 2
    both = 3


# TODO: Drop `fault` from the order once AMP reads a connecting tunnel as connecting (U26b).
# AMP 3.0.0.6 reads `Fault` while a new gateway's tunnel still connects.
class GatewayState(StrEnum):
    """A gateway's `state`, named as the web panel names it. AMP sends the name, which each member equals.

    A new gateway reads `provisioning`, `fault` while its tunnel connects, `awaiting_shard` until a shard that was
    running restarts, then `connecting` and `active`. The web panel's code also has `disabled`.

    .. versionadded:: 6.0.0
    """

    active = "Active"
    awaiting_shard = "AwaitingShard"
    connecting = "Connecting"
    disabled = "Disabled"
    fault = "Fault"
    provisioning = "Provisioning"


class MigrationStatus(IntEnum):
    """A shard move's `status`, named as the web panel's `ShardMigrationStatus` names it. AMP sends the number.

    A move reads 0 while copying, 2 once it is done, and 3 for a failed one or one
    :meth:`ShardModule.cancel_shard_migration` stopped (its `error` reads ``"Cancelled."``). A move can be done within
    one round trip. The record stays until :meth:`ShardModule.delete_shard_migration`. The rest are from the web
    panel's code.

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

    AMP sends `tunnel_provisioning`, `active`, `disabled` and `shard_stopped`, and a first publication reads
    `tunnel_fault` for about a minute before it turns active. The rest are from the web panel's code.

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

    A task reads 1 while an update downloads, 0 while a clone or move copies, 3 when finished, 4 for a failed move or
    update and 6 for a cancelled move. A cancelled clone reads 5, then goes back to 0 and finishes anyway.

    .. versionadded:: 6.0.0
    """

    running = 0
    waiting = 1
    user_action_required = 2
    succeeded = 3
    failed = 4
    cancelling = 5
    cancelled = 6
