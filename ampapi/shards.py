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

import logging
from typing import TYPE_CHECKING, Any, Optional

from ._enums import CloneContent, MigrationStatus, ShardState, SnapshotContent, SnapshotKind, SnapshotStage, SnapshotState
from ._types import ShardInfraSettings
from .base import Base

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ._types import (
        ScheduleCatalogResponse,
        ScheduleExecutionResponse,
        ScheduleRunResponse,
        ScheduleStep,
        ScheduleTrigger,
        ShardAgentResponse,
        ShardArchiveInfoResponse,
        ShardCloneResponse,
        ShardConfigImportResponse,
        ShardConsoleHistoryResponse,
        ShardCreatedResponse,
        ShardCredentialResponse,
        ShardEndpointResponse,
        ShardExtractResponse,
        ShardFileACLResponse,
        ShardFileContentResponse,
        ShardFileIgnoresResponse,
        ShardFileResponse,
        ShardInfraResponse,
        ShardInfraUpdateResponse,
        ShardMetricResponse,
        ShardMigrationResponse,
        ShardMigrationTargetResponse,
        ShardPortResponse,
        ShardResponse,
        ShardScheduleResponse,
        ShardSettingCandidatesResponse,
        ShardSettingResponse,
        ShardSFTPResponse,
        ShardSnapshotsResponse,
        ShardStateResponse,
        ShardUpdateResponse,
        ShardUploadChunkResponse,
        ShardUploadSessionResponse,
        SnapshotResponse,
        SnapshotSettingsResponse,
        SpireIPOptionResponse,
    )

__all__ = (
    "Shard",
    "ShardModule",
)

LOGGER: logging.Logger = logging.getLogger(__name__)

# The web panel sends a chunked upload in 8 MiB slices.
UPLOAD_CHUNK_SIZE: int = 8 * 1024 * 1024


class Shard:
    """A shard, AMP 3's name for an Instance, with the calls that act on it.

    :meth:`ShardModule.get_shards` and :meth:`ShardModule.get_shard` make these. Each method calls the
    :class:`ShardModule` one with this shard's ID, eg. :meth:`start` is :meth:`ShardModule.start_shard`; its
    parameters, reply and errors are documented there.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    module : :class:`ShardModule`
        The module (usually the :class:`Panel`) the calls go through.
    data : :class:`ShardResponse`
        The shard as AMP sent it.

    Attributes
    ----------
    id : :class:`str`
        The shard's ID.
    display_name : :class:`str`
        The shard's name.
    data : :class:`ShardResponse`
        The shard as AMP sent it, when this object was made.

    """

    data: ShardResponse
    display_name: str
    id: str
    _module: ShardModule

    def __init__(self, module: ShardModule, data: ShardResponse) -> None:  # noqa: D107
        self._module = module
        self.data = data
        self.id = data["id"]
        self.display_name = data["displayName"]

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # It comes from `ShardModule.abort_shard_update`.
    async def abort_update(self) -> Any:
        """Stop this shard's update, see :meth:`ShardModule.abort_shard_update`.

        |coro|

        .. warning::
            AMP 3.0.0.6 answers 404, as the route isn't there yet, so this doesn't work (U12).

        """
        return await self._module.abort_shard_update(shard_id=self.id)

    async def accept_eula(self) -> None:
        """Accept the game's licence for this shard, see :meth:`ShardModule.accept_shard_eula`.

        |coro|

        """
        await self._module.accept_shard_eula(shard_id=self.id)

    async def acknowledge_disk_warning(self) -> ShardResponse:
        """Dismiss this shard's disk warning, see :meth:`ShardModule.acknowledge_shard_disk_warning`.

        |coro|

        """
        return await self._module.acknowledge_shard_disk_warning(shard_id=self.id)

    async def archive_files(self, paths: list[str], destination: str) -> None:
        """Zip files and folders into an archive in this shard, see :meth:`ShardModule.archive_shard_files`.

        |coro|

        """
        await self._module.archive_shard_files(shard_id=self.id, paths=paths, destination=destination)

    async def cancel_migration(self) -> None:
        """Stop this shard's move, see :meth:`ShardModule.cancel_shard_migration`.

        |coro|

        """
        await self._module.cancel_shard_migration(shard_id=self.id)

    async def clone(
        self,
        new_name: str,
        *,
        content: CloneContent = CloneContent.both,
        target_spire_id: Optional[str] = None,
    ) -> ShardCloneResponse:
        """Copy this shard into a new one, see :meth:`ShardModule.clone_shard`.

        |coro|

        """
        return await self._module.clone_shard(shard_id=self.id, new_name=new_name, content=content, target_spire_id=target_spire_id)

    async def commit_file_upload(self, session_id: str) -> None:
        """Finish a chunked upload to this shard, see :meth:`ShardModule.commit_shard_file_upload`.

        |coro|

        """
        await self._module.commit_shard_file_upload(shard_id=self.id, session_id=session_id)

    async def copy_file(self, source: str, destination: str) -> None:
        """Copy a file or folder in this shard, see :meth:`ShardModule.copy_shard_file`.

        |coro|

        """
        await self._module.copy_shard_file(shard_id=self.id, source=source, destination=destination)

    async def create_custom_port(self, name: str, protocol: str, port: int) -> list[ShardPortResponse]:
        """Add a port to this shard, see :meth:`ShardModule.create_shard_custom_port`.

        |coro|

        """
        return await self._module.create_shard_custom_port(shard_id=self.id, name=name, protocol=protocol, port=port)

    async def create_folder(self, path: str) -> None:
        """Make a folder in this shard, see :meth:`ShardModule.create_shard_folder`.

        |coro|

        """
        await self._module.create_shard_folder(shard_id=self.id, path=path)

    async def create_schedule(
        self,
        name: str,
        trigger: ScheduleTrigger,
        steps: list[ScheduleStep],
        *,
        description: Optional[str] = None,
        run_timeout: Optional[str] = None,
        enabled: bool = False,
    ) -> ShardScheduleResponse:
        """Make a schedule for this shard, see :meth:`ShardModule.create_shard_schedule`.

        |coro|

        """
        return await self._module.create_shard_schedule(
            shard_id=self.id,
            name=name,
            trigger=trigger,
            steps=steps,
            description=description,
            run_timeout=run_timeout,
            enabled=enabled,
        )

    async def delete(self) -> ShardResponse:
        """Delete this shard, which it can come back from until it's purged, see :meth:`ShardModule.delete_shard`.

        |coro|

        """
        return await self._module.delete_shard(shard_id=self.id)

    async def delete_credential(self) -> None:
        """Take the stored secret off this shard, see :meth:`ShardModule.delete_shard_credential`.

        |coro|

        """
        await self._module.delete_shard_credential(shard_id=self.id)

    async def delete_custom_port(self, port_reference: str) -> list[ShardPortResponse]:
        """Remove one of this shard's custom ports, see :meth:`ShardModule.delete_shard_custom_port`.

        |coro|

        """
        return await self._module.delete_shard_custom_port(shard_id=self.id, port_reference=port_reference)

    async def delete_file(self, path: str) -> None:
        """Delete a file or folder in this shard, see :meth:`ShardModule.delete_shard_file`.

        |coro|

        """
        await self._module.delete_shard_file(shard_id=self.id, path=path)

    async def delete_migration(self) -> None:
        """Dismiss this shard's finished move, see :meth:`ShardModule.delete_shard_migration`.

        |coro|

        """
        await self._module.delete_shard_migration(shard_id=self.id)

    async def delete_schedule(self, schedule_id: str) -> None:
        """Delete one of this shard's schedules, see :meth:`ShardModule.delete_shard_schedule`.

        |coro|

        """
        await self._module.delete_shard_schedule(shard_id=self.id, schedule_id=schedule_id)

    async def delete_snapshot(self, snapshot_id: str) -> None:
        """Delete one of this shard's snapshots, see :meth:`ShardModule.delete_shard_snapshot`.

        |coro|

        """
        await self._module.delete_shard_snapshot(shard_id=self.id, snapshot_id=snapshot_id)

    async def download_file(self, path: str) -> bytes:
        """Download a file from this shard, see :meth:`ShardModule.download_shard_file`.

        |coro|

        """
        return await self._module.download_shard_file(shard_id=self.id, path=path)

    async def download_files(self, paths: list[str]) -> bytes:
        """Download files and folders from this shard as one zip, see :meth:`ShardModule.download_shard_files`.

        |coro|

        """
        return await self._module.download_shard_files(shard_id=self.id, paths=paths)

    async def download_snapshot(self, snapshot_id: str) -> bytes:
        """Download one of this shard's snapshots as a zip, see :meth:`ShardModule.download_shard_snapshot`.

        |coro|

        """
        return await self._module.download_shard_snapshot(shard_id=self.id, snapshot_id=snapshot_id)

    async def extract_archive(self, path: str, destination: str, *, overwrite: bool = False) -> ShardExtractResponse:
        """Unpack an archive in this shard, see :meth:`ShardModule.extract_shard_archive`.

        |coro|

        """
        return await self._module.extract_shard_archive(shard_id=self.id, path=path, destination=destination, overwrite=overwrite)

    async def get_agent(self) -> ShardAgentResponse:
        """Get the AMP agent that runs this shard, see :meth:`ShardModule.get_shard_agent`.

        |coro|

        """
        return await self._module.get_shard_agent(shard_id=self.id)

    async def get_archive_info(self, path: str) -> ShardArchiveInfoResponse:
        """Get what an archive in this shard holds, see :meth:`ShardModule.get_shard_archive_info`.

        |coro|

        """
        return await self._module.get_shard_archive_info(shard_id=self.id, path=path)

    async def get_console_history(self, *, limit: Optional[int] = None, before_seq: Optional[int] = None) -> ShardConsoleHistoryResponse:
        """Get this shard's console lines, see :meth:`ShardModule.get_shard_console_history`.

        |coro|

        """
        return await self._module.get_shard_console_history(shard_id=self.id, limit=limit, before_seq=before_seq)

    async def get_credential(self) -> ShardCredentialResponse:
        """Get the stored secret this shard uses, see :meth:`ShardModule.get_shard_credential`.

        |coro|

        """
        return await self._module.get_shard_credential(shard_id=self.id)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # It comes from `ShardModule.get_shard_disk`.
    async def get_disk(self) -> Optional[dict[str, Any]]:
        """Get this shard's disk use, see :meth:`ShardModule.get_shard_disk`.

        |coro|

        """
        return await self._module.get_shard_disk(shard_id=self.id)

    async def get_endpoints(self) -> list[ShardEndpointResponse]:
        """Get where players reach this shard, see :meth:`ShardModule.get_shard_endpoints`.

        |coro|

        """
        return await self._module.get_shard_endpoints(shard_id=self.id)

    async def get_file_acl(self, path: str) -> ShardFileACLResponse:
        """Get who may do what to a path in this shard, see :meth:`ShardModule.get_shard_file_acl`.

        |coro|

        """
        return await self._module.get_shard_file_acl(shard_id=self.id, path=path)

    async def get_file_content(self, path: str) -> ShardFileContentResponse:
        """Get a text file's content from this shard, see :meth:`ShardModule.get_shard_file_content`.

        |coro|

        """
        return await self._module.get_shard_file_content(shard_id=self.id, path=path)

    async def get_file_ignores(self, path: str) -> ShardFileIgnoresResponse:
        """Get the ignored entries in one of this shard's folders, see :meth:`ShardModule.get_shard_file_ignores`.

        |coro|

        """
        return await self._module.get_shard_file_ignores(shard_id=self.id, path=path)

    async def get_file_info(self, path: str) -> ShardFileResponse:
        """Get one file's details from this shard, see :meth:`ShardModule.get_shard_file_info`.

        |coro|

        """
        return await self._module.get_shard_file_info(shard_id=self.id, path=path)

    async def get_files(self, path: str = "") -> list[ShardFileResponse]:
        """Get the files and folders in one of this shard's folders, see :meth:`ShardModule.get_shard_files`.

        |coro|

        """
        return await self._module.get_shard_files(shard_id=self.id, path=path)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # It comes from `ShardModule.get_shard_import`.
    async def get_import(self) -> Optional[dict[str, Any]]:
        """Get how this shard's import went, see :meth:`ShardModule.get_shard_import`.

        |coro|

        """
        return await self._module.get_shard_import(shard_id=self.id)

    async def get_infra(self) -> ShardInfraResponse:
        """Get how this shard runs, see :meth:`ShardModule.get_shard_infra`.

        |coro|

        """
        return await self._module.get_shard_infra(shard_id=self.id)

    async def get_ip_options(self) -> list[SpireIPOptionResponse]:
        """Get the addresses this shard can bind to, see :meth:`ShardModule.get_shard_ip_options`.

        |coro|

        """
        return await self._module.get_shard_ip_options(shard_id=self.id)

    # TODO: Type the items once AMP is seen listing one live (#3-47.7).
    # It comes from `ShardModule.get_shard_managed_files`.
    async def get_managed_files(self, path: str) -> list[dict[str, Any]]:
        """Get which files under a path AMP writes itself, see :meth:`ShardModule.get_shard_managed_files`.

        |coro|

        """
        return await self._module.get_shard_managed_files(shard_id=self.id, path=path)

    async def get_metrics(self, *, minutes: Optional[int] = None) -> list[ShardMetricResponse]:
        """Get this shard's recent load, see :meth:`ShardModule.get_shard_metrics`.

        |coro|

        """
        return await self._module.get_shard_metrics(shard_id=self.id, minutes=minutes)

    async def get_migration(self) -> Optional[ShardMigrationResponse]:
        """Get this shard's latest move, see :meth:`ShardModule.get_shard_migration`.

        |coro|

        """
        return await self._module.get_shard_migration(shard_id=self.id)

    async def get_migration_targets(self) -> list[ShardMigrationTargetResponse]:
        """Get the other datastores on this shard's spire it could move to, see :meth:`ShardModule.get_shard_migration_targets`.

        |coro|

        """
        return await self._module.get_shard_migration_targets(shard_id=self.id)

    async def get_ports(self) -> list[ShardPortResponse]:
        """Get this shard's ports, see :meth:`ShardModule.get_shard_ports`.

        |coro|

        """
        return await self._module.get_shard_ports(shard_id=self.id)

    async def get_schedule_catalog(self) -> ScheduleCatalogResponse:
        """Get the triggers and tasks this shard's schedules can use, see :meth:`ShardModule.get_shard_schedule_catalog`.

        |coro|

        """
        return await self._module.get_shard_schedule_catalog(shard_id=self.id)

    async def get_schedule_history(self, schedule_id: str, *, limit: Optional[int] = None) -> list[ScheduleExecutionResponse]:
        """Get the runs of one of this shard's schedules, see :meth:`ShardModule.get_shard_schedule_history`.

        |coro|

        """
        return await self._module.get_shard_schedule_history(shard_id=self.id, schedule_id=schedule_id, limit=limit)

    async def get_schedules(self) -> list[ShardScheduleResponse]:
        """Get this shard's schedules, see :meth:`ShardModule.get_shard_schedules`.

        |coro|

        """
        return await self._module.get_shard_schedules(shard_id=self.id)

    async def get_setting_candidates(self, field_name: str, *, refresh: bool = False) -> ShardSettingCandidatesResponse:
        """Get the values one of this shard's settings can take, see :meth:`ShardModule.get_shard_setting_candidates`.

        |coro|

        """
        return await self._module.get_shard_setting_candidates(shard_id=self.id, field_name=field_name, refresh=refresh)

    async def get_settings(self) -> list[ShardSettingResponse]:
        """Get this shard's game settings, see :meth:`ShardModule.get_shard_settings`.

        |coro|

        """
        return await self._module.get_shard_settings(shard_id=self.id)

    async def get_settings_locale(self) -> dict[str, dict[str, str]]:
        """Get the text for this shard's settings, see :meth:`ShardModule.get_shard_settings_locale`.

        |coro|

        """
        return await self._module.get_shard_settings_locale(shard_id=self.id)

    async def get_sftp(self) -> ShardSFTPResponse:
        """Get how to reach this shard's files over SFTP, see :meth:`ShardModule.get_shard_sftp`.

        |coro|

        """
        return await self._module.get_shard_sftp(shard_id=self.id)

    async def get_snapshot_settings(self) -> SnapshotSettingsResponse:
        """Get this shard's snapshot limits, see :meth:`ShardModule.get_shard_snapshot_settings`.

        |coro|

        """
        return await self._module.get_shard_snapshot_settings(shard_id=self.id)

    async def get_snapshots(self) -> ShardSnapshotsResponse:
        """Get this shard's snapshots, see :meth:`ShardModule.get_shard_snapshots`.

        |coro|

        """
        return await self._module.get_shard_snapshots(shard_id=self.id)

    async def get_state(self) -> ShardStateResponse:
        """Get this shard's live state, see :meth:`ShardModule.get_shard_state`.

        |coro|

        """
        return await self._module.get_shard_state(shard_id=self.id)

    # TODO: Type the items once AMP is seen listing one live (#3-47.7).
    # It comes from `ShardModule.get_shard_users`.
    async def get_users(self) -> list[dict[str, Any]]:
        """Get the players on this shard, see :meth:`ShardModule.get_shard_users`.

        |coro|

        """
        return await self._module.get_shard_users(shard_id=self.id)

    async def import_config(self, path: str, *, content: Optional[str] = None) -> ShardConfigImportResponse:
        """Read this shard's settings back from a config file, see :meth:`ShardModule.import_shard_config`.

        |coro|

        """
        return await self._module.import_shard_config(shard_id=self.id, path=path, content=content)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # It comes from `ShardModule.kill_shard`.
    async def kill(self) -> Any:
        """End this shard's game at once, see :meth:`ShardModule.kill_shard`.

        |coro|

        .. warning::
            AMP 3.0.0.6 answers 404, as the route isn't there yet, so this doesn't work (U12).

        """
        return await self._module.kill_shard(shard_id=self.id)

    async def migrate_to_spire(self, target_spire_id: str, target_datastore_id: str, *, bring_backups: bool, stop_if_running: bool) -> None:
        """Move this shard to another spire, see :meth:`ShardModule.migrate_shard_to_spire`.

        |coro|

        """
        await self._module.migrate_shard_to_spire(
            shard_id=self.id,
            target_spire_id=target_spire_id,
            target_datastore_id=target_datastore_id,
            bring_backups=bring_backups,
            stop_if_running=stop_if_running,
        )

    async def move_file(self, source: str, destination: str) -> None:
        """Move or rename a file or folder in this shard, see :meth:`ShardModule.move_shard_file`.

        |coro|

        """
        await self._module.move_shard_file(shard_id=self.id, source=source, destination=destination)

    async def preview_schedule_firings(self, trigger: ScheduleTrigger) -> list[str]:
        """Get when a trigger would next fire for this shard, see :meth:`ShardModule.preview_shard_schedule_firings`.

        |coro|

        """
        return await self._module.preview_shard_schedule_firings(shard_id=self.id, trigger=trigger)

    async def purge(self) -> None:
        """Remove this deleted shard for good, see :meth:`ShardModule.purge_shard`.

        |coro|

        """
        await self._module.purge_shard(shard_id=self.id)

    async def restart(self) -> None:
        """Restart this shard's game, see :meth:`ShardModule.restart_shard`.

        |coro|

        """
        await self._module.restart_shard(shard_id=self.id)

    async def restore(self) -> ShardResponse:
        """Bring this deleted shard back, see :meth:`ShardModule.restore_shard`.

        |coro|

        """
        return await self._module.restore_shard(shard_id=self.id)

    async def restore_snapshot(self, snapshot_id: str) -> SnapshotResponse:
        """Put this shard back to one of its snapshots, see :meth:`ShardModule.restore_shard_snapshot`.

        |coro|

        """
        return await self._module.restore_shard_snapshot(shard_id=self.id, snapshot_id=snapshot_id)

    async def run_schedule(self, schedule_id: str) -> ScheduleRunResponse:
        """Run one of this shard's schedules now, see :meth:`ShardModule.run_shard_schedule`.

        |coro|

        """
        return await self._module.run_shard_schedule(shard_id=self.id, schedule_id=schedule_id)

    async def send_console(self, command: str, *, prompt_reply: bool = False) -> None:
        """Send a command to this shard's console, see :meth:`ShardModule.send_shard_console`.

        |coro|

        """
        await self._module.send_shard_console(shard_id=self.id, command=command, prompt_reply=prompt_reply)

    async def send_file_chunk(self, session_id: str, chunk: bytes) -> ShardUploadChunkResponse:
        """Send one piece of a chunked upload to this shard, see :meth:`ShardModule.send_shard_file_chunk`.

        |coro|

        """
        return await self._module.send_shard_file_chunk(shard_id=self.id, session_id=session_id, chunk=chunk)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # It comes from `ShardModule.set_shard_credential`.
    async def set_credential(self, credential_id: str) -> Any:
        """Give this shard a stored secret to use, see :meth:`ShardModule.set_shard_credential`.

        |coro|

        """
        return await self._module.set_shard_credential(shard_id=self.id, credential_id=credential_id)

    async def set_details(
        self,
        *,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> ShardResponse:
        """Change this shard's name, description or tags, see :meth:`ShardModule.set_shard_details`.

        |coro|

        """
        return await self._module.set_shard_details(shard_id=self.id, display_name=display_name, description=description, tags=tags)

    # TODO: Type the change items once AMP is seen taking one live (#3-47.7).
    # It comes from `ShardModule.set_shard_file_acl`.
    async def set_file_acl(self, path: str, changes: list[dict[str, Any]]) -> ShardFileACLResponse:
        """Change who may do what to a path in this shard, see :meth:`ShardModule.set_shard_file_acl`.

        |coro|

        """
        return await self._module.set_shard_file_acl(shard_id=self.id, path=path, changes=changes)

    async def set_file_content(self, path: str, content: str) -> None:
        """Write a text file in this shard, see :meth:`ShardModule.set_shard_file_content`.

        |coro|

        """
        await self._module.set_shard_file_content(shard_id=self.id, path=path, content=content)

    async def set_file_ignored(self, paths: list[str], ignored: bool) -> None:
        """Ignore files in this shard, or stop ignoring them, see :meth:`ShardModule.set_shard_file_ignored`.

        |coro|

        """
        await self._module.set_shard_file_ignored(shard_id=self.id, paths=paths, ignored=ignored)

    async def set_infra(self, settings: ShardInfraSettings) -> ShardInfraUpdateResponse:
        """Replace how this shard runs with the whole of `settings`, see :meth:`ShardModule.set_shard_infra`.

        |coro|

        """
        return await self._module.set_shard_infra(shard_id=self.id, settings=settings)

    async def set_port_access(self, port_reference: str, public: bool) -> list[ShardPortResponse]:
        """Make one of this shard's ports public or private, see :meth:`ShardModule.set_shard_port_access`.

        |coro|

        """
        return await self._module.set_shard_port_access(shard_id=self.id, port_reference=port_reference, public=public)

    async def set_ports(self, ports: dict[str, int]) -> None:
        """Move this shard's ports to other numbers, see :meth:`ShardModule.set_shard_ports`.

        |coro|

        """
        await self._module.set_shard_ports(shard_id=self.id, ports=ports)

    async def set_schedule_enabled(self, schedule_id: str, enabled: bool) -> None:
        """Turn one of this shard's schedules on or off, see :meth:`ShardModule.set_shard_schedule_enabled`.

        |coro|

        """
        await self._module.set_shard_schedule_enabled(shard_id=self.id, schedule_id=schedule_id, enabled=enabled)

    async def set_settings(self, values: dict[str, str]) -> None:
        """Change some of this shard's game settings, see :meth:`ShardModule.set_shard_settings`.

        |coro|

        """
        await self._module.set_shard_settings(shard_id=self.id, values=values)

    async def set_snapshot_settings(
        self,
        max_backup_size_mb: int,
        max_total_storage_mb: int,
        stop_when_no_quiesce: bool,
    ) -> SnapshotSettingsResponse:
        """Set this shard's snapshot limits, see :meth:`ShardModule.set_shard_snapshot_settings`.

        |coro|

        """
        return await self._module.set_shard_snapshot_settings(
            shard_id=self.id,
            max_backup_size_mb=max_backup_size_mb,
            max_total_storage_mb=max_total_storage_mb,
            stop_when_no_quiesce=stop_when_no_quiesce,
        )

    async def sleep(self) -> None:
        """Put this shard to sleep, see :meth:`ShardModule.sleep_shard`.

        |coro|

        """
        await self._module.sleep_shard(shard_id=self.id)

    async def start(self) -> None:
        """Start this shard's game, see :meth:`ShardModule.start_shard`.

        |coro|

        """
        await self._module.start_shard(shard_id=self.id)

    async def start_file_upload(self, path: str, size: int) -> ShardUploadSessionResponse:
        """Start a chunked upload to this shard, see :meth:`ShardModule.start_shard_file_upload`.

        |coro|

        """
        return await self._module.start_shard_file_upload(shard_id=self.id, path=path, size=size)

    async def start_migration(self, target_datastore_id: str) -> None:
        """Move this shard to another datastore on its spire, see :meth:`ShardModule.start_shard_migration`.

        |coro|

        """
        await self._module.start_shard_migration(shard_id=self.id, target_datastore_id=target_datastore_id)

    async def stop(self) -> None:
        """Stop this shard's game, see :meth:`ShardModule.stop_shard`.

        |coro|

        """
        await self._module.stop_shard(shard_id=self.id)

    async def suspend(self) -> ShardResponse:
        """Suspend this shard, so it can't be started, see :meth:`ShardModule.suspend_shard`.

        |coro|

        """
        return await self._module.suspend_shard(shard_id=self.id)

    async def take_snapshot(
        self,
        name: str,
        kind: SnapshotKind,
        content: SnapshotContent,
        *,
        description: str = "",
        sticky: bool = False,
    ) -> SnapshotResponse:
        """Take a snapshot (a backup) of this shard, see :meth:`ShardModule.take_shard_snapshot`.

        |coro|

        """
        return await self._module.take_shard_snapshot(
            shard_id=self.id,
            name=name,
            kind=kind,
            content=content,
            description=description,
            sticky=sticky,
        )

    async def unsuspend(self) -> ShardResponse:
        """Let this suspended shard start again, see :meth:`ShardModule.unsuspend_shard`.

        |coro|

        """
        return await self._module.unsuspend_shard(shard_id=self.id)

    async def update(self) -> ShardUpdateResponse:
        """Install or update this shard's game, see :meth:`ShardModule.update_shard`.

        |coro|

        """
        return await self._module.update_shard(shard_id=self.id)

    async def update_infra(self, changes: dict[str, Any]) -> ShardInfraUpdateResponse:
        """Change a few of this shard's infra settings, keeping the rest, see :meth:`ShardModule.update_shard_infra`.

        |coro|

        """
        return await self._module.update_shard_infra(shard_id=self.id, changes=changes)

    async def update_schedule(
        self,
        schedule_id: str,
        name: str,
        trigger: ScheduleTrigger,
        steps: list[ScheduleStep],
        *,
        description: Optional[str] = None,
        run_timeout: Optional[str] = None,
        enabled: bool = False,
    ) -> ShardScheduleResponse:
        """Replace one of this shard's schedules, see :meth:`ShardModule.update_shard_schedule`.

        |coro|

        """
        return await self._module.update_shard_schedule(
            shard_id=self.id,
            schedule_id=schedule_id,
            name=name,
            trigger=trigger,
            steps=steps,
            description=description,
            run_timeout=run_timeout,
            enabled=enabled,
        )

    async def update_snapshot(self, snapshot_id: str, name: str, description: str, sticky: bool) -> None:
        """Change one of this shard's snapshot's name, description or stickiness, see :meth:`ShardModule.update_shard_snapshot`.

        |coro|

        """
        await self._module.update_shard_snapshot(
            shard_id=self.id,
            snapshot_id=snapshot_id,
            name=name,
            description=description,
            sticky=sticky,
        )

    async def upload_file(self, path: str, content: bytes, *, chunk_size: int = UPLOAD_CHUNK_SIZE) -> None:
        """Upload one file to this shard in chunks, see :meth:`ShardModule.upload_shard_file`.

        |coro|

        """
        await self._module.upload_shard_file(shard_id=self.id, path=path, content=content, chunk_size=chunk_size)

    async def upload_files(self, folder: str, files: Mapping[str, bytes]) -> None:
        """Upload files to a folder in this shard in one request, see :meth:`ShardModule.upload_shard_files`.

        |coro|

        """
        await self._module.upload_shard_files(shard_id=self.id, folder=folder, files=files)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # It comes from `ShardModule.wake_shard`.
    async def wake(self) -> Any:
        """Wake this sleeping shard, see :meth:`ShardModule.wake_shard`.

        |coro|

        """
        return await self._module.wake_shard(shard_id=self.id)


class ShardModule(Base):
    """The calls for shards, AMP 3's name for an Instance: lifecycle, power, console, settings, ports, files, schedules,
    snapshots and moves.

    .. versionadded:: 6.0.0

    """

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # AMP 3.0.0.6 has no such route; the panel's code sends `{}` and ignores the reply.
    async def abort_shard_update(self, shard_id: str) -> Any:
        """Stop a shard's update.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/update/abort``

        .. warning::
            AMP 3.0.0.6 answers 404, as the route isn't there yet, so this doesn't work (U12).

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/update/abort", data={})

    async def accept_shard_eula(self, shard_id: str) -> None:
        """Accept the game's licence for a shard, eg. Minecraft's EULA, which it needs before it starts.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/eula/accept``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/eula/accept")

    async def acknowledge_shard_disk_warning(self, shard_id: str) -> ShardResponse:
        """Dismiss a shard's disk warning.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/disk-warning/ack``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardResponse`
            The shard, `diskWarningAcked` set.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/disk-warning/ack", data={})

    async def archive_shard_files(self, shard_id: str, paths: list[str], destination: str) -> None:
        """Zip files and folders into an archive inside a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/archive``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        paths : list[:class:`str`]
            The files and folders to put in it.
        destination : :class:`str`
            The archive's path, eg. ``"backup.zip"``.

        """
        data: dict[str, Any] = {"paths": paths, "destination": destination}
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/archive", data=data)

    async def cancel_shard_migration(self, shard_id: str) -> None:
        """Stop a shard's move.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/migration/cancel``

        AMP answers 202, and :meth:`get_shard_migration` then reads `MigrationStatus.failed` with `error`
        ``"Cancelled."``; the shard stays where it was. A cancel sent straight after the start was taken. Dismiss the
        record with :meth:`delete_shard_migration` as for any other.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Raises
        ------
        AMPAPIRequestError
            If no move is running (409, ``"shards.migration.notRunning"``), eg. there's none, or it's done, failed,
            cancelled or dismissed.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/migration/cancel")

    async def clone_shard(
        self,
        shard_id: str,
        new_name: str,
        *,
        content: CloneContent = CloneContent.both,
        target_spire_id: Optional[str] = None,
    ) -> ShardCloneResponse:
        """Copy a shard into a new one.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/clone``

        A ``"ShardClone"`` task copies the files, see :meth:`TaskModule.get_running_tasks`. The copy's ports are free
        ones on its spire, so they can differ from the original's.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard to copy.
        new_name : :class:`str`
            The copy's display name.
        content : :class:`CloneContent`, optional
            What to copy, by default `CloneContent.both`.
        target_spire_id : Union[:class:`str`, None], optional
            The spire to put the copy on, by default None (the same one).

        Returns
        -------
        :class:`ShardCloneResponse`
            The copy's ID. The copy is there at once, but its `installedAt` is `None` even when the original was
            installed, so run :meth:`update_shard` on it before starting it.

        Raises
        ------
        AMPAPIRequestError
            If `content` is 0 (400, ``"shards.error.cloneNothing"``) or there's no such spire
            (400, ``"shards.error.spireNotFound"``).

        """
        data: dict[str, Any] = {"newName": new_name, "content": content, "targetSpireId": target_spire_id}
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/clone", data=data)

    async def commit_shard_file_upload(self, shard_id: str, session_id: str) -> None:
        """Finish a chunked upload, which writes the file.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/upload-commit``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        session_id : :class:`str`
            The upload's `sessionId` from :meth:`start_shard_file_upload`.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/upload-commit", parameters={"session": session_id})

    async def copy_shard_file(self, shard_id: str, source: str, destination: str) -> None:
        """Copy a file or folder inside a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/copy``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        source : :class:`str`
            The path to copy.
        destination : :class:`str`
            The copy's path.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/copy", data={"from": source, "to": destination})

    async def create_shard(
        self,
        template_slug: str,
        display_name: str,
        spire_id: str,
        *,
        description: str = "",
        start_now: bool = False,
        start_on_boot: bool = False,
        credential_id: Optional[str] = None,
    ) -> ShardCreatedResponse:
        """Make a shard from a template. It installs nothing until :meth:`update_shard`.

        |coro|

        Endpoint: ``POST /api/shards``

        .. note::
            A shard that was never updated still starts, then fails after pulling its container (U15).

        Parameters
        ----------
        template_slug : :class:`str`
            The template, eg. ``"minecraft-java"``; see :meth:`TemplateModule.get_templates`.
        display_name : :class:`str`
            The shard's name. An empty one gets the template's name.
        spire_id : :class:`str`
            The spire to put it on.
        description : :class:`str`, optional
            A description, by default "".
        start_now : :class:`bool`, optional
            If the shard should start once made or not, by default False. Not yet seen live with `True`.
        start_on_boot : :class:`bool`, optional
            If the shard starts when its spire boots or not, by default False.
        credential_id : Union[:class:`str`, None], optional
            A stored secret for the game's download, eg. a Steam login, by default None.

        Returns
        -------
        :class:`ShardCreatedResponse`
            The shard with its first settings and ports. ``Shard(module=panel, data=result["shard"])`` makes it an object.

        Raises
        ------
        AMPAPIRequestError
            If the template doesn't exist (400, ``"shards.error.createFailed"``, which doesn't name the cause).

        """
        data: dict[str, Any] = {
            "templateSlug": template_slug,
            "displayName": display_name,
            "description": description,
            "spireId": spire_id,
            "startNow": start_now,
            "startOnBoot": start_on_boot,
        }
        if credential_id is not None:
            data["credentialId"] = credential_id

        return await self._request(method="POST", path="/api/shards", data=data)

    async def create_shard_custom_port(self, shard_id: str, name: str, protocol: str, port: int) -> list[ShardPortResponse]:
        """Add a port of your own to a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/ports/custom``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        name : :class:`str`
            The port's name; its `ref` becomes ``"Custom"`` and the name without spaces.
        protocol : :class:`str`
            ``"TCP"``, ``"UDP"`` or ``"Both"``. AMP stores anything else as ``"TCP"``.
        port : :class:`int`
            The port number.

        Returns
        -------
        list[:class:`ShardPortResponse`]
            All of the shard's ports.

        Raises
        ------
        AMPAPIRequestError
            If the port is taken (400, ``"shards.error.portConflict"``) or out of range (400, ``"shards.error.invalidPort"``).

        """
        data: dict[str, Any] = {"name": name, "protocol": protocol, "port": port}
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/ports/custom", data=data)

    async def create_shard_folder(self, shard_id: str, path: str) -> None:
        """Make a folder inside a shard. One that's already there is fine.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/folder``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The folder's path.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/folder", data={"path": path})

    async def create_shard_schedule(
        self,
        shard_id: str,
        name: str,
        trigger: ScheduleTrigger,
        steps: list[ScheduleStep],
        *,
        description: Optional[str] = None,
        run_timeout: Optional[str] = None,
        enabled: bool = False,
    ) -> ShardScheduleResponse:
        """Make a schedule for a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/schedules``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        name : :class:`str`
            The schedule's name.
        trigger : :class:`ScheduleTrigger`
            When it runs, eg. ``{"type": "interval", "interval": "01:00:00"}``.
        steps : list[:class:`ScheduleStep`]
            What it does, in order; can be empty. See :meth:`get_shard_schedule_catalog` for the tasks.
        description : Union[:class:`str`, None], optional
            A description, by default None.
        run_timeout : Union[:class:`str`, None], optional
            How long a run may take, as a time span, by default None (AMP uses ``"00:30:00"``). AMP calls it `timeout`.
        enabled : :class:`bool`, optional
            If it runs on its trigger or not, by default False.

        Returns
        -------
        :class:`ShardScheduleResponse`
            The schedule.

        Raises
        ------
        AMPAPIRequestError
            If a step or the trigger has an unknown `type` (400). A step with no `type` at all gets a 500 (U16).

        """
        data: dict[str, Any] = {
            "name": name,
            "description": description,
            "trigger": trigger,
            "steps": steps,
            "timeout": run_timeout,
            "enabled": enabled,
        }
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/schedules", data=data)

    async def delete_shard(self, shard_id: str) -> ShardResponse:
        """Delete a shard. It stays, marked deleted, until :meth:`purge_shard`; :meth:`restore_shard` brings it back.

        |coro|

        Endpoint: ``DELETE /api/shards/{shard_id}``

        Most calls on a deleted shard answer 409 (``"shards.error.deleted"``).

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardResponse`
            The shard, `deleted` set.

        """
        return await self._request(method="DELETE", path=f"/api/shards/{shard_id}")

    async def delete_shard_credential(self, shard_id: str) -> None:
        """Take the stored secret off a shard.

        |coro|

        Endpoint: ``DELETE /api/shards/{shard_id}/credential``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        """
        await self._request(method="DELETE", path=f"/api/shards/{shard_id}/credential")

    async def delete_shard_custom_port(self, shard_id: str, port_reference: str) -> list[ShardPortResponse]:
        """Remove one of a shard's custom ports.

        |coro|

        Endpoint: ``DELETE /api/shards/{shard_id}/ports/custom/{port_reference}``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        port_reference : :class:`str`
            The port's `ref`, eg. ``"CustomMyPort"``. A template's port can't be removed.

        Returns
        -------
        list[:class:`ShardPortResponse`]
            The shard's ports left.

        """
        return await self._request(method="DELETE", path=f"/api/shards/{shard_id}/ports/custom/{port_reference}")

    async def delete_shard_file(self, shard_id: str, path: str) -> None:
        """Delete a file or folder inside a shard. A path that isn't there is fine.

        |coro|

        Endpoint: ``DELETE /api/shards/{shard_id}/files``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The path to delete.

        """
        await self._request(method="DELETE", path=f"/api/shards/{shard_id}/files", parameters={"path": path})

    async def delete_shard_migration(self, shard_id: str) -> None:
        """Dismiss a shard's done or failed move, so :meth:`get_shard_migration` has none.

        |coro|

        Endpoint: ``DELETE /api/shards/{shard_id}/migration``

        It only clears the record. The copy a move leaves on the old spire stays until
        :meth:`SpireModule.purge_spire_orphan_directory`, and a failed move's task until
        :meth:`TaskModule.delete_running_task` (U22c).

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Raises
        ------
        AMPAPIRequestError
            If the move is still copying or was only just started (500, ``"common.error.unexpected"``) (U22a). The move
            carries on unharmed.

        """
        await self._request(method="DELETE", path=f"/api/shards/{shard_id}/migration")

    async def delete_shard_schedule(self, shard_id: str, schedule_id: str) -> None:
        """Delete one of a shard's schedules.

        |coro|

        Endpoint: ``DELETE /api/shards/{shard_id}/schedules/{schedule_id}``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        schedule_id : :class:`str`
            The schedule's ID.

        """
        await self._request(method="DELETE", path=f"/api/shards/{shard_id}/schedules/{schedule_id}")

    async def delete_shard_snapshot(self, shard_id: str, snapshot_id: str) -> None:
        """Delete one of a shard's snapshots. A sticky one is deleted too.

        |coro|

        Endpoint: ``DELETE /api/shards/{shard_id}/snapshots/{snapshot_id}``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        snapshot_id : :class:`str`
            The snapshot's ID.

        Raises
        ------
        AMPAPIRequestError
            If other snapshots build on it (400, ``"snapshots.error.hasDependents"``).

        """
        await self._request(method="DELETE", path=f"/api/shards/{shard_id}/snapshots/{snapshot_id}")

    async def download_shard_file(self, shard_id: str, path: str) -> bytes:
        """Download a file from a shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/download``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's path.

        Returns
        -------
        :class:`bytes`
            The file as it came, all of it in memory.

        Raises
        ------
        AMPAPIRequestError
            If the path is missing or a folder (400, ``"files.error.notFound"``).

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/download", parameters={"path": path}, raw_bytes=True)

    async def download_shard_files(self, shard_id: str, paths: list[str]) -> bytes:
        """Download files and folders from a shard as one zip.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/zip``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        paths : list[:class:`str`]
            The files and folders; a folder comes with everything in it.

        Returns
        -------
        :class:`bytes`
            The zip as it came, all of it in memory.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/files/zip", data={"paths": paths}, raw_bytes=True)

    async def download_shard_snapshot(self, shard_id: str, snapshot_id: str) -> bytes:
        """Download one of a shard's snapshots as a zip.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/snapshots/{snapshot_id}/download``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        snapshot_id : :class:`str`
            The snapshot's ID.

        Returns
        -------
        :class:`bytes`
            The zip as it came, all of it in memory; a full Minecraft snapshot was about 125 MB.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/snapshots/{snapshot_id}/download", raw_bytes=True)

    async def extract_shard_archive(self, shard_id: str, path: str, destination: str, *, overwrite: bool = False) -> ShardExtractResponse:
        """Unpack an archive inside a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/extract``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The archive's path.
        destination : :class:`str`
            The folder to unpack it into.
        overwrite : :class:`bool`, optional
            If files already there should be replaced or not, by default False.

        Returns
        -------
        :class:`ShardExtractResponse`
            How many files came out, and how many were skipped.

        """
        data: dict[str, Any] = {"path": path, "destination": destination, "overwrite": overwrite}
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/files/extract", data=data)

    async def get_all_shard_endpoints(self) -> dict[str, list[ShardEndpointResponse]]:
        """Get where players reach every shard.

        |coro|

        Endpoint: ``GET /api/shards/endpoints``

        Returns
        -------
        dict[:class:`str`, list[:class:`ShardEndpointResponse`]]
            Each shard's ID to its public ports and addresses.

        """
        return await self._request(method="GET", path="/api/shards/endpoints")

    async def get_shard(self, shard_id: str) -> Shard:
        """Get one shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`Shard`
            The shard, with the calls that act on it.

        Raises
        ------
        AMPAPIRequestError
            If the shard is deleted (409, ``"shards.error.deleted"``) or purged (404).

        """
        result: ShardResponse = await self._request(method="GET", path=f"/api/shards/{shard_id}")
        return Shard(module=self, data=result)

    async def get_shards(self, *, include_deleted: bool = False) -> list[Shard]:
        """Get every shard the logged in user can see.

        |coro|

        Endpoint: ``GET /api/shards``

        Parameters
        ----------
        include_deleted : :class:`bool`, optional
            If deleted shards that aren't purged yet are listed too or not, by default False.

        Returns
        -------
        list[:class:`Shard`]
            The shards, each with the calls that act on it.

        """
        parameters: dict[str, str] = {"includeDeleted": "true" if include_deleted is True else "false"}
        result: list[ShardResponse] = await self._request(method="GET", path="/api/shards", parameters=parameters)
        return [Shard(module=self, data=entry) for entry in result]

    # TODO: Type the items once AMP is seen listing one live (#3-47.7).
    # Only seen empty; the web panel reads `shardId`, `name` and `message` from each.
    async def get_shards_awaiting_action(self) -> list[dict[str, Any]]:
        """Get the shards waiting on a user, eg. for a sign-in prompt.

        |coro|

        Endpoint: ``GET /api/shards/attention``

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The shards and what they wait for.

        """
        return await self._request(method="GET", path="/api/shards/attention")

    async def get_shard_agent(self, shard_id: str) -> ShardAgentResponse:
        """Get the AMP agent that runs a shard, and if it's out of date.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/agent``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardAgentResponse`
            The agent's version and its spire's.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/agent")

    async def get_shard_archive_info(self, shard_id: str, path: str) -> ShardArchiveInfoResponse:
        """Get what an archive inside a shard holds.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/archive-info``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The archive's path.

        Returns
        -------
        :class:`ShardArchiveInfoResponse`
            How many entries it has, and their size.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/archive-info", parameters={"path": path})

    async def get_shard_console_history(
        self,
        shard_id: str,
        *,
        limit: Optional[int] = None,
        before_seq: Optional[int] = None,
    ) -> ShardConsoleHistoryResponse:
        """Get a shard's console lines, oldest first.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/console/history``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        limit : Union[:class:`int`, None], optional
            The most lines to get, by default None. The web panel asks for 300; 0 still gives one.
        before_seq : Union[:class:`int`, None], optional
            Only lines before this `seq`, for paging back, by default None.

        Returns
        -------
        :class:`ShardConsoleHistoryResponse`
            The lines, each marker's `state` a :class:`ShardState`.

        """
        filters: dict[str, Optional[int]] = {"limit": limit, "beforeSeq": before_seq}
        parameters: dict[str, int] = {key: value for key, value in filters.items() if value is not None}
        result: ShardConsoleHistoryResponse = await self._request(
            method="GET",
            path=f"/api/shards/{shard_id}/console/history",
            parameters=parameters,
        )
        for line in result["lines"]:
            if line["state"] is not None:
                line["state"] = self._to_enum(ShardState, line["state"])
        return result

    async def get_shard_credential(self, shard_id: str) -> ShardCredentialResponse:
        """Get the stored secret a shard uses, eg. a Steam login, and the ones it could use.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/credential``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardCredentialResponse`
            If it needs one, the one it has and the ones usable.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/credential")

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # Always a 204 so far, running or stopped, even with files in the shard.
    async def get_shard_disk(self, shard_id: str) -> Optional[dict[str, Any]]:
        """Get a shard's disk use.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/disk``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        Union[dict[:class:`str`, Any], None]
            The disk use, `None` when AMP has none (a 204).

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/disk")

    async def get_shard_endpoints(self, shard_id: str) -> list[ShardEndpointResponse]:
        """Get where players reach a shard, one entry for each public port.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/endpoints``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`ShardEndpointResponse`]
            The public ports and their addresses.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/endpoints")

    async def get_shard_file_acl(self, shard_id: str, path: str) -> ShardFileACLResponse:
        """Get who may read, write and delete a path inside a shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/acl``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The path, empty for the shard's folder.

        Returns
        -------
        :class:`ShardFileACLResponse`
            The users and roles, with what each may do.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/acl", parameters={"path": path})

    async def get_shard_file_content(self, shard_id: str, path: str) -> ShardFileContentResponse:
        """Get a text file's content from a shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/content``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's path.

        Returns
        -------
        :class:`ShardFileContentResponse`
            The text.

        Raises
        ------
        AMPAPIRequestError
            If the file isn't there (400, ``"files.error.notFound"``).

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/content", parameters={"path": path})

    async def get_shard_file_ignores(self, shard_id: str, path: str) -> ShardFileIgnoresResponse:
        """Get the ignored entries among a folder's children in a shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/ignore``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The folder, empty for the shard's own. A file's path gives empty lists.

        Returns
        -------
        :class:`ShardFileIgnoresResponse`
            The entries AMP ignores and the ones a user does.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/ignore", parameters={"path": path})

    async def get_shard_file_info(self, shard_id: str, path: str) -> ShardFileResponse:
        """Get one file's details from a shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/stat``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's path. A folder gets 404, so list its parent with :meth:`get_shard_files` instead.

        Returns
        -------
        :class:`ShardFileResponse`
            The file's size and when it changed.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/stat", parameters={"path": path})

    async def get_shard_files(self, shard_id: str, path: str = "") -> list[ShardFileResponse]:
        """Get the files and folders in one of a shard's folders.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`, optional
            The folder, by default "" (the shard's own). One that isn't there gives an empty list.

        Returns
        -------
        list[:class:`ShardFileResponse`]
            The entries, each `path` relative to the shard's folder.

        Raises
        ------
        AMPAPIRequestError
            If the path leaves the shard's folder, eg. ``"../.."`` (403).

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files", parameters={"path": path})

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # Only a 204 was captured; the web panel reads a `left` list from the import record.
    async def get_shard_import(self, shard_id: str) -> Optional[dict[str, Any]]:
        """Get how the import that made a shard went.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/import``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        Union[dict[:class:`str`, Any], None]
            The import record, `None` for a shard that wasn't imported (a 204).

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/import")

    async def get_shard_infra(self, shard_id: str) -> ShardInfraResponse:
        """Get how a shard runs: container, limits, boot and analytics, and what its spire allows.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/infra``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardInfraResponse`
            The settings, which :meth:`set_shard_infra` takes back whole, and the spire's limits.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/infra")

    async def get_shard_ip_options(self, shard_id: str) -> list[SpireIPOptionResponse]:
        """Get the addresses a shard can bind to.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/ip-options``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`SpireIPOptionResponse`]
            The addresses, the same shape as a spire's.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/ip-options")

    # TODO: Type the items once AMP is seen listing one live (#3-47.7).
    # Only seen empty, for server.properties as well as a file of our own.
    async def get_shard_managed_files(self, shard_id: str, path: str) -> list[dict[str, Any]]:
        """Get which files under a path AMP writes itself from the settings.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/managed``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The path.

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The managed files.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/managed", parameters={"path": path})

    async def get_shard_metrics(self, shard_id: str, *, minutes: Optional[int] = None) -> list[ShardMetricResponse]:
        """Get a running shard's recent load, one sample every few seconds.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/metrics``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        minutes : Union[:class:`int`, None], optional
            How far back to go, by default None.

        Returns
        -------
        list[:class:`ShardMetricResponse`]
            The samples, empty while stopped.

        """
        parameters: Optional[dict[str, int]] = {"minutes": minutes} if minutes is not None else None
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/metrics", parameters=parameters)

    async def get_shard_migration(self, shard_id: str) -> Optional[ShardMigrationResponse]:
        """Get a shard's latest move, running or done.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/migration``

        A move copies (`MigrationStatus.copying`) for a few seconds between two spires on one network, then waits at
        `MigrationStatus.awaiting_cleanup` until :meth:`delete_shard_migration`.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        Union[:class:`ShardMigrationResponse`, None]
            The move, its `status` a :class:`MigrationStatus`; `None` when there's none (a 204).

        """
        result: Optional[ShardMigrationResponse] = await self._request(method="GET", path=f"/api/shards/{shard_id}/migration")
        if result is not None:
            result["status"] = self._to_enum(MigrationStatus, result["status"])
        return result

    async def get_shard_migration_targets(self, shard_id: str) -> list[ShardMigrationTargetResponse]:
        """Get the other datastores on a shard's own spire it could move to, for :meth:`start_shard_migration`.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/migration/targets``

        It doesn't list other spires. To move a shard to another spire, pick one from :meth:`SpireModule.get_spires`
        and a datastore from :meth:`SpireModule.get_spire_datastores`, for :meth:`migrate_shard_to_spire`.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`ShardMigrationTargetResponse`]
            The spire's other datastores, without the one the shard is in; empty when the spire has one datastore.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/migration/targets")

    async def get_shard_ports(self, shard_id: str) -> list[ShardPortResponse]:
        """Get a shard's ports.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/ports``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`ShardPortResponse`]
            The ports, the template's and any custom ones.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/ports")

    async def get_shard_schedule_catalog(self, shard_id: str) -> ScheduleCatalogResponse:
        """Get the triggers and tasks a shard's schedules can use.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/schedules/catalog``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ScheduleCatalogResponse`
            The triggers, with the game's own events, and the tasks.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/schedules/catalog")

    async def get_shard_schedule_history(
        self,
        shard_id: str,
        schedule_id: str,
        *,
        limit: Optional[int] = None,
    ) -> list[ScheduleExecutionResponse]:
        """Get the runs of one of a shard's schedules.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/schedules/{schedule_id}/history``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        schedule_id : :class:`str`
            The schedule's ID.
        limit : Union[:class:`int`, None], optional
            The most runs to get, by default None. The web panel asks for 50.

        Returns
        -------
        list[:class:`ScheduleExecutionResponse`]
            The runs.

        """
        parameters: Optional[dict[str, int]] = {"limit": limit} if limit is not None else None
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/schedules/{schedule_id}/history", parameters=parameters)

    async def get_shard_schedules(self, shard_id: str) -> list[ShardScheduleResponse]:
        """Get a shard's schedules.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/schedules``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`ShardScheduleResponse`]
            The schedules, with how each last ran.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/schedules")

    async def get_shard_setting_candidates(
        self,
        shard_id: str,
        field_name: str,
        *,
        refresh: bool = False,
    ) -> ShardSettingCandidatesResponse:
        """Get the values one of a shard's settings can take, eg. the game versions.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/settings/{field_name}/candidates``

        Only a setting with a `valueSourceId` has them; an enum lists its values in `enumValues` instead.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        field_name : :class:`str`
            The setting's `fieldName`, eg. ``"MinecraftVersion"``.
        refresh : :class:`bool`, optional
            If AMP should fetch the list again rather than use its copy or not, by default False.

        Returns
        -------
        :class:`ShardSettingCandidatesResponse`
            The values, and when the list was fetched.

        Raises
        ------
        AMPAPIRequestError
            If the setting has no list (404, ``"shards.error.noValueSource"``).

        """
        parameters: Optional[dict[str, str]] = {"refresh": "true"} if refresh is True else None
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/settings/{field_name}/candidates", parameters=parameters)

    async def get_shard_settings(self, shard_id: str) -> list[ShardSettingResponse]:
        """Get a shard's game settings with their values.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/settings``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`ShardSettingResponse`]
            The settings, each value a string. A setting whose `conditionSetting` doesn't match isn't always listed.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/settings")

    async def get_shard_settings_locale(self, shard_id: str) -> dict[str, dict[str, str]]:
        """Get the text for a shard's settings: their names, descriptions and choices.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/settings/locale``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        dict[:class:`str`, dict[:class:`str`, :class:`str`]]
            A language, eg. ``"en"``, to each translation key's text, eg. ``"setting.motd.name"``.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/settings/locale")

    async def get_shard_sftp(self, shard_id: str) -> ShardSFTPResponse:
        """Get how to reach a shard's files over SFTP.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/sftp``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardSFTPResponse`
            The host, port, username and folder.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/sftp")

    async def get_shard_snapshot_settings(self, shard_id: str) -> SnapshotSettingsResponse:
        """Get a shard's snapshot limits.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/snapshots/settings``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`SnapshotSettingsResponse`
            The size limits, 0 for none.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/snapshots/settings")

    def _snapshot_enums(self, snapshot: SnapshotResponse) -> SnapshotResponse:
        snapshot["kind"] = self._to_enum(SnapshotKind, snapshot["kind"])
        snapshot["content"] = self._to_enum(SnapshotContent, snapshot["content"])
        snapshot["status"] = self._to_enum(SnapshotState, snapshot["status"])
        snapshot["stage"] = self._to_enum(SnapshotStage, snapshot["stage"])
        return snapshot

    async def get_shard_snapshots(self, shard_id: str) -> ShardSnapshotsResponse:
        """Get a shard's snapshots (backups) as a tree, with any restore in progress.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/snapshots``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardSnapshotsResponse`
            The snapshots, their numbers as the library's enums, eg. `SnapshotKind`.

        """
        result: ShardSnapshotsResponse = await self._request(method="GET", path=f"/api/shards/{shard_id}/snapshots")
        for snapshot in result["nodes"]:
            self._snapshot_enums(snapshot=snapshot)
        result["restoreStage"] = self._to_enum(SnapshotStage, result["restoreStage"])
        return result

    async def get_shard_state(self, shard_id: str) -> ShardStateResponse:
        """Get a shard's live state.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/state``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardStateResponse`
            The state, its `status` a :class:`ShardState`.

        """
        result: ShardStateResponse = await self._request(method="GET", path=f"/api/shards/{shard_id}/state")
        result["status"] = self._to_enum(ShardState, result["status"])
        return result

    # TODO: Type the items once AMP is seen listing one live (#3-47.7).
    # Only seen empty, as no player joined; the web panel reads `id`, `name` and `sessionId` from each.
    async def get_shard_users(self, shard_id: str) -> list[dict[str, Any]]:
        """Get the players on a shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/users``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The players.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/users")

    async def import_shard_config(self, shard_id: str, path: str, *, content: Optional[str] = None) -> ShardConfigImportResponse:
        """Read a shard's settings back from one of its config files.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/config/import``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The config file's path, eg. ``"server.properties"``.
        content : Union[:class:`str`, None], optional
            The file's text to read instead of the file on disk, by default None. Not yet seen live with text.

        Returns
        -------
        :class:`ShardConfigImportResponse`
            The settings set from the file, those AMP keeps for itself and those the file lacks.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/config/import", data={"path": path, "content": content})

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # AMP 3.0.0.6 has no such route; the panel's code sends `{}` and ignores the reply.
    async def kill_shard(self, shard_id: str) -> Any:
        """End a shard's game at once, without the clean stop.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/kill``

        .. warning::
            AMP 3.0.0.6 answers 404, as the route isn't there yet, so this doesn't work (U12).

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/kill", data={})

    async def migrate_shard_to_spire(
        self,
        shard_id: str,
        target_spire_id: str,
        target_datastore_id: str,
        *,
        bring_backups: bool,
        stop_if_running: bool,
    ) -> None:
        """Move a shard to another spire.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/migration/spire``

        AMP answers at once (202) and a ``"ShardMigration"`` task copies the files; follow it with
        :meth:`get_shard_migration`. The shard's `spireId` and `datastoreId` change straight away.

        .. note::
            The copy on the old spire stays, as an ``"Orphan"`` in :meth:`SpireModule.get_spire_usage`, until
            :meth:`SpireModule.purge_spire_orphan_directory` is called on the **old** spire's datastore with the
            shard's `workingDirName`. :meth:`delete_shard_migration` doesn't remove it.

        The shard's ports become free ones on the target spire, eg. 8303 became 8305, and they stay so if it moves
        back. A failed move's task stays in :meth:`TaskModule.get_running_tasks` until it is deleted (U22c). A shard
        that was running starts again on the target by itself, once that spire has its container image, although the
        move's record reads `startAfterMove` `False` (U22d).

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        target_spire_id : :class:`str`
            The spire to move it to.
        target_datastore_id : :class:`str`
            A datastore on that spire, see :meth:`SpireModule.get_spire_datastores`.
        bring_backups : :class:`bool`
            If its snapshots move too or not.
        stop_if_running : :class:`bool`
            If AMP may stop a running shard for the move or not. It works when the game stops cleanly (Minecraft); on
            teeworlds, whose stops end in a kill (U18a), the move failed and left the shard stopped on its old spire.

        Raises
        ------
        AMPAPIRequestError
            If the shard already lives on that spire (400, an English sentence in `message` and no `code`), there's
            no such spire (400, ``"shards.error.spireNotFound"``), or the shard is running and `stop_if_running` is
            `False` (409, ``"shards.error.moveNeedsStop"``). A datastore of another spire gets 409
            ``"spire.error.internal"`` (U22b).

        """
        data: dict[str, Any] = {
            "targetSpireId": target_spire_id,
            "targetDatastoreId": target_datastore_id,
            "bringBackups": bring_backups,
            "stopIfRunning": stop_if_running,
        }
        await self._request(method="POST", path=f"/api/shards/{shard_id}/migration/spire", data=data)

    async def move_shard_file(self, shard_id: str, source: str, destination: str) -> None:
        """Move or rename a file or folder inside a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/move``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        source : :class:`str`
            The path to move.
        destination : :class:`str`
            The new path.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/move", data={"from": source, "to": destination})

    async def preview_shard_schedule_firings(self, shard_id: str, trigger: ScheduleTrigger) -> list[str]:
        """Get when a trigger would next fire, before saving a schedule with it.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/schedules/preview-firings``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        trigger : :class:`ScheduleTrigger`
            The trigger, eg. ``{"type": "cron", "expression": "0 3 * * *", "timeZoneId": "UTC"}``.

        Returns
        -------
        list[:class:`str`]
            The next five times, ISO 8601; empty for an event trigger.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/schedules/preview-firings", data={"trigger": trigger})

    async def purge_shard(self, shard_id: str) -> None:
        """Remove a deleted shard for good, its files included. AMP finishes it within a few seconds.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/purge``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID, deleted with :meth:`delete_shard` first.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/purge")

    async def restart_shard(self, shard_id: str) -> None:
        """Restart a shard's game.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/restart``

        Follow it with :meth:`get_shard_state`; AMP answers before the game is back.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/restart")

    async def restore_shard(self, shard_id: str) -> ShardResponse:
        """Bring a deleted shard back.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/restore``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardResponse`
            The shard, `deleted` cleared.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/restore")

    async def restore_shard_snapshot(self, shard_id: str, snapshot_id: str) -> SnapshotResponse:
        """Put a shard back to one of its snapshots. It works on a running shard too.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/snapshots/{snapshot_id}/restore``

        AMP takes a snapshot named ``"Before restore"`` first, so the restore can be undone.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        snapshot_id : :class:`str`
            The snapshot's ID.

        Returns
        -------
        :class:`SnapshotResponse`
            The snapshot being restored; follow the restore with :meth:`get_shard_snapshots`.

        """
        path: str = f"/api/shards/{shard_id}/snapshots/{snapshot_id}/restore"
        result: SnapshotResponse = await self._request(method="POST", path=path, data={})
        return self._snapshot_enums(snapshot=result)

    async def run_shard_schedule(self, shard_id: str, schedule_id: str) -> ScheduleRunResponse:
        """Run one of a shard's schedules now. A disabled one is logged as skipped.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/schedules/{schedule_id}/run``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        schedule_id : :class:`str`
            The schedule's ID.

        Returns
        -------
        :class:`ScheduleRunResponse`
            The run's ID, for :meth:`get_shard_schedule_history`.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/schedules/{schedule_id}/run", data={})

    async def send_shard_console(self, shard_id: str, command: str, *, prompt_reply: bool = False) -> None:
        """Send a command to a shard's console. The game's answer shows in :meth:`get_shard_console_history`.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/console``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        command : :class:`str`
            The command, eg. ``"say hello"``.
        prompt_reply : :class:`bool`, optional
            If it answers a prompt the game is waiting on rather than being a command or not, by default False.
            With no prompt waiting it's sent as a command.

        """
        data: dict[str, Any] = {"command": command, "promptReply": prompt_reply}
        await self._request(method="POST", path=f"/api/shards/{shard_id}/console", data=data)

    async def send_shard_file_chunk(self, shard_id: str, session_id: str, chunk: bytes) -> ShardUploadChunkResponse:
        """Send the next piece of a chunked upload.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/upload-chunk``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        session_id : :class:`str`
            The upload's `sessionId` from :meth:`start_shard_file_upload`.
        chunk : :class:`bytes`
            The bytes that follow the ones AMP holds; the web panel sends 8 MiB at a time.

        Returns
        -------
        :class:`ShardUploadChunkResponse`
            How many bytes AMP holds now.

        """
        path: str = f"/api/shards/{shard_id}/files/upload-chunk"
        return await self._request(method="POST", path=path, data=chunk, parameters={"session": session_id})

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # Only the 400 for an unknown credential was captured, as none existed.
    async def set_shard_credential(self, shard_id: str, credential_id: str) -> Any:
        """Give a shard a stored secret to use, eg. a Steam login for its downloads.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/credential``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        credential_id : :class:`str`
            The credential's ID; see :meth:`CredentialModule.get_credentials`.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If the user can't use that credential (400, ``"shards.error.credentialUnknown"``).

        """
        return await self._request(method="PUT", path=f"/api/shards/{shard_id}/credential", data={"credentialId": credential_id})

    async def set_shard_details(
        self,
        shard_id: str,
        *,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> ShardResponse:
        """Change a shard's name, description or tags. Anything left as `None` stays as it is.

        |coro|

        Endpoint: ``PATCH /api/shards/{shard_id}``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        display_name : Union[:class:`str`, None], optional
            The new name, by default None. AMP refuses an empty one (``"shards.error.displayNameRequired"``).
        description : Union[:class:`str`, None], optional
            The new description, by default None.
        tags : Union[list[:class:`str`], None], optional
            The tags, which replace the old ones, by default None.

        Returns
        -------
        :class:`ShardResponse`
            The shard. Its short `name` doesn't change with the display name.

        """
        data: dict[str, Any] = {"displayName": display_name, "description": description, "tags": tags}
        # We only send what changes, AMP keeps a value that's left out.
        data = {key: value for key, value in data.items() if value is not None}
        return await self._request(method="PATCH", path=f"/api/shards/{shard_id}", data=data)

    # TODO: Type the change items once AMP is seen taking one live (#3-47.7).
    # Only an empty list was sent; a 400 named `PrincipalId`, `Verb` and `State` as the fields of a change.
    async def set_shard_file_acl(self, shard_id: str, path: str, changes: list[dict[str, Any]]) -> ShardFileACLResponse:
        """Change who may read, write and delete a path inside a shard.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/files/acl``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The path.
        changes : list[dict[:class:`str`, Any]]
            The changes, each naming a principal, a verb and a state.

        Returns
        -------
        :class:`ShardFileACLResponse`
            Who may do what to the path now.

        """
        return await self._request(
            method="PUT",
            path=f"/api/shards/{shard_id}/files/acl",
            data={"changes": changes},
            parameters={"path": path},
        )

    async def set_shard_file_content(self, shard_id: str, path: str, content: str) -> None:
        """Write a text file inside a shard, making it and its folders when they aren't there.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/files/content``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's path.
        content : :class:`str`
            The text, which replaces the file's.

        """
        await self._request(
            method="PUT",
            path=f"/api/shards/{shard_id}/files/content",
            data={"content": content},
            parameters={"path": path},
        )

    async def set_shard_file_ignored(self, shard_id: str, paths: list[str], ignored: bool) -> None:
        """Ignore files in a shard, or stop ignoring them.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/ignore``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        paths : list[:class:`str`]
            The files and folders.
        ignored : :class:`bool`
            If they're ignored or not.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/ignore", data={"paths": paths, "ignored": ignored})

    async def set_shard_infra(self, shard_id: str, settings: ShardInfraSettings) -> ShardInfraUpdateResponse:
        """Replace how a shard runs with the whole of `settings`: container, limits, boot and analytics.

        |coro|

        Endpoint: ``PATCH /api/shards/{shard_id}/infra``

        .. warning::
            AMP resets every field the body leaves out, so a partial body changes the rest too; one switched a
            container shard to Native (U13). So we refuse `settings` with any field missing. Take them from
            :meth:`get_shard_infra`'s `settings`, or use :meth:`update_shard_infra` to change a few. A change takes
            effect when the shard next starts.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        settings : :class:`ShardInfraSettings`
            Every infra setting. AMP doesn't check the values, eg. a negative memory limit.

        Returns
        -------
        :class:`ShardInfraUpdateResponse`
            The settings as AMP saved them.

        Raises
        ------
        ValueError
            If `settings` is missing a field, before anything is sent.

        """
        missing: list[str] = sorted(ShardInfraSettings.__required_keys__ - settings.keys())
        if missing:
            msg = f"The infra settings are missing {', '.join(missing)}, which AMP would reset. Start from get_shard_infra's settings."
            raise ValueError(msg)

        return await self._request(method="PATCH", path=f"/api/shards/{shard_id}/infra", data={**settings})

    async def set_shard_port_access(self, shard_id: str, port_reference: str, public: bool) -> list[ShardPortResponse]:
        """Make one of a shard's ports public or private.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/ports/{port_reference}/access``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        port_reference : :class:`str`
            The port's `ref`, eg. ``"RemoteAdminPort"``.
        public : :class:`bool`
            If players can reach it or not.

        Returns
        -------
        list[:class:`ShardPortResponse`]
            All of the shard's ports.

        Raises
        ------
        AMPAPIRequestError
            If the port is the one players connect to, which stays public (400, ``"shards.error.primaryPortIsPublic"``),
            or there's no such port (400, ``"shards.error.unknownPortRef"``).

        """
        path: str = f"/api/shards/{shard_id}/ports/{port_reference}/access"
        return await self._request(method="PUT", path=path, data={"public": public})

    async def set_shard_ports(self, shard_id: str, ports: dict[str, int]) -> None:
        """Move a shard's ports to other numbers.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/ports``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        ports : dict[:class:`str`, :class:`int`]
            Each port's `ref` to its new number, eg. ``{"RemoteAdminPort": 25576}``; a port left out stays as it is.

        """
        await self._request(method="PUT", path=f"/api/shards/{shard_id}/ports", data={**ports})

    async def set_shard_schedule_enabled(self, shard_id: str, schedule_id: str, enabled: bool) -> None:
        """Turn one of a shard's schedules on or off.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/schedules/{schedule_id}/enabled``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        schedule_id : :class:`str`
            The schedule's ID.
        enabled : :class:`bool`
            If it runs on its trigger or not.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/schedules/{schedule_id}/enabled", data={"enabled": enabled})

    async def set_shard_settings(self, shard_id: str, values: dict[str, str]) -> None:
        """Change some of a shard's game settings; AMP rewrites the game's config files to match.

        |coro|

        Endpoint: ``PATCH /api/shards/{shard_id}/settings``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        values : dict[:class:`str`, :class:`str`]
            Each setting's `fieldName` to its new value, always a string, eg. ``{"motd": "Hello", "MaxMemory": "2048"}``.
            AMP checks an enum's value, but not a number's, and ignores a name it doesn't know.

        Raises
        ------
        AMPAPIRequestError
            If an enum value isn't one the setting allows (400, ``"shards.error.valueNotAllowed"``).

        """
        await self._request(method="PATCH", path=f"/api/shards/{shard_id}/settings", data=values)

    async def set_shard_snapshot_settings(
        self,
        shard_id: str,
        max_backup_size_mb: int,
        max_total_storage_mb: int,
        stop_when_no_quiesce: bool,
    ) -> SnapshotSettingsResponse:
        """Set a shard's snapshot limits.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/snapshots/settings``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        max_backup_size_mb : :class:`int`
            The largest snapshot, 0 for no limit.
        max_total_storage_mb : :class:`int`
            The most all of them may take, 0 for no limit.
        stop_when_no_quiesce : :class:`bool`
            If AMP should stop the game for a snapshot when it can't pause its saving or not.

        Returns
        -------
        :class:`SnapshotSettingsResponse`
            The limits as AMP saved them.

        """
        data: dict[str, Any] = {
            "maxBackupSizeMb": max_backup_size_mb,
            "maxTotalStorageMb": max_total_storage_mb,
            "stopWhenNoQuiesce": stop_when_no_quiesce,
        }
        return await self._request(method="PUT", path=f"/api/shards/{shard_id}/snapshots/settings", data=data)

    async def sleep_shard(self, shard_id: str) -> None:
        """Put a shard to sleep, so it wakes when a player connects.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/sleep``

        See `ShardStateResponse.sleep` for if it can; a template whose sleep port doesn't exist can't (U18b).

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Raises
        ------
        AMPAPIRequestError
            If sleep mode is off (400, ``"shards.error.sleepDisabled"``) or the shard can't sleep
            (400, ``"shards.error.sleepUnavailable"``).

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/sleep")

    async def start_shard(self, shard_id: str) -> None:
        """Start a shard's game.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/start``

        Follow it with :meth:`get_shard_state`; AMP answers before the game is up. A shard never updated starts too,
        then fails after pulling its container (U15), so run :meth:`update_shard` first.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Raises
        ------
        AMPAPIRequestError
            If the game's licence isn't accepted (409, ``"shards.error.eulaRequired"``, see :meth:`accept_shard_eula`), a
            setting it needs is empty (409, ``"shards.error.settingRequiredBeforeStart"``) or the shard is suspended
            (400, ``"shards.error.suspended"``).

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/start")

    async def start_shard_file_upload(self, shard_id: str, path: str, size: int) -> ShardUploadSessionResponse:
        """Start a chunked upload, for a file too big for :meth:`upload_shard_files`.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/upload-start``

        Send the bytes with :meth:`send_shard_file_chunk`, then :meth:`commit_shard_file_upload`;
        :meth:`upload_shard_file` does all three.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's path, its name included.
        size : :class:`int`
            The file's size in bytes.

        Returns
        -------
        :class:`ShardUploadSessionResponse`
            The upload's ID and how many bytes AMP already holds.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/files/upload-start", data={"path": path, "size": size})

    async def start_shard_migration(self, shard_id: str, target_datastore_id: str) -> None:
        """Move a shard to another datastore on its spire.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/migration``

        AMP answers at once (202); follow it with :meth:`get_shard_migration`. The shard's `datastoreId` changes
        straight away. A shard with files leaves its old folder as an ``"Orphan"`` in the old datastore, until
        :meth:`SpireModule.purge_spire_orphan_directory`. To move it to another spire, use :meth:`migrate_shard_to_spire`.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        target_datastore_id : :class:`str`
            The datastore to move it to; see :meth:`get_shard_migration_targets`.

        Raises
        ------
        AMPAPIRequestError
            If `target_datastore_id` is the shard's own datastore or an unknown one (409, ``"spire.error.internal"``)
            (U22b).

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/migration", data={"targetDatastoreId": target_datastore_id})

    async def stop_shard(self, shard_id: str) -> None:
        """Stop a shard's game cleanly.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/stop``

        Follow it with :meth:`get_shard_state`; AMP answers before the game has stopped.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/stop")

    async def suspend_shard(self, shard_id: str) -> ShardResponse:
        """Suspend a shard, so it can't be started until :meth:`unsuspend_shard`.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/suspend``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardResponse`
            The shard, `suspended` set.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/suspend", data={})

    async def take_shard_snapshot(
        self,
        shard_id: str,
        name: str,
        kind: SnapshotKind,
        content: SnapshotContent,
        *,
        description: str = "",
        sticky: bool = False,
    ) -> SnapshotResponse:
        """Take a snapshot (a backup) of a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/snapshots``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        name : :class:`str`
            The snapshot's name.
        kind : :class:`SnapshotKind`
            A full snapshot, or a partial one that builds on the newest.
        content : :class:`SnapshotContent`
            What it holds, eg. ``SnapshotContent.game_state | SnapshotContent.amp_config``. AMP refuses none.
        description : :class:`str`, optional
            A description, by default "". AMP writes one when it's empty.
        sticky : :class:`bool`, optional
            If it's marked to keep or not, by default False. It doesn't stop a delete.

        Returns
        -------
        :class:`SnapshotResponse`
            The snapshot, still running; follow it with :meth:`get_shard_snapshots`.

        """
        data: dict[str, Any] = {"kind": kind, "content": content, "name": name, "description": description, "sticky": sticky}
        result: SnapshotResponse = await self._request(method="POST", path=f"/api/shards/{shard_id}/snapshots", data=data)
        return self._snapshot_enums(snapshot=result)

    async def unsuspend_shard(self, shard_id: str) -> ShardResponse:
        """Let a suspended shard start again.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/unsuspend``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardResponse`
            The shard, `suspended` cleared.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/unsuspend", data={})

    async def update_shard(self, shard_id: str) -> ShardUpdateResponse:
        """Install or update a shard's game, from its template's update steps.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/update``

        A running shard is stopped for the update and left stopped.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardUpdateResponse`
            The update's task ID; follow it with :meth:`TaskModule.get_running_tasks`.

        Raises
        ------
        AMPAPIRequestError
            If the download needs a Steam login the shard doesn't have (409, ``"shards.error.steamLoginRequired"``, from
            the web panel's code), see :meth:`set_shard_credential`.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/update")

    async def update_shard_infra(self, shard_id: str, changes: dict[str, Any]) -> ShardInfraUpdateResponse:
        """Change a few of how a shard runs, keeping the rest: we read the settings, change them and send them whole.

        |coro|

        Endpoints: ``GET /api/shards/{shard_id}/infra``, then ``PATCH /api/shards/{shard_id}/infra``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        changes : dict[:class:`str`, Any]
            The settings to change, named as in :class:`ShardInfraSettings`, eg. ``{"startOnBoot": True}``.

        Returns
        -------
        :class:`ShardInfraUpdateResponse`
            The settings as AMP saved them.

        Raises
        ------
        ValueError
            If a name in `changes` isn't an infra setting, before anything is sent.

        """
        unknown: list[str] = sorted(changes.keys() - ShardInfraSettings.__required_keys__)
        if unknown:
            msg = f"{', '.join(unknown)} aren't infra settings; see ShardInfraSettings for the names."
            raise ValueError(msg)

        current: ShardInfraResponse = await self.get_shard_infra(shard_id=shard_id)
        settings: dict[str, Any] = {**current["settings"], **changes}
        return await self._request(method="PATCH", path=f"/api/shards/{shard_id}/infra", data=settings)

    async def update_shard_schedule(
        self,
        shard_id: str,
        schedule_id: str,
        name: str,
        trigger: ScheduleTrigger,
        steps: list[ScheduleStep],
        *,
        description: Optional[str] = None,
        run_timeout: Optional[str] = None,
        enabled: bool = False,
    ) -> ShardScheduleResponse:
        """Replace one of a shard's schedules with a new definition.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/schedules/{schedule_id}``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        schedule_id : :class:`str`
            The schedule's ID.
        name : :class:`str`
            The schedule's name.
        trigger : :class:`ScheduleTrigger`
            When it runs.
        steps : list[:class:`ScheduleStep`]
            What it does, in order.
        description : Union[:class:`str`, None], optional
            A description, by default None.
        run_timeout : Union[:class:`str`, None], optional
            How long a run may take, as a time span, by default None (AMP uses ``"00:30:00"``). AMP calls it `timeout`.
        enabled : :class:`bool`, optional
            If it runs on its trigger or not, by default False.

        Returns
        -------
        :class:`ShardScheduleResponse`
            The schedule.

        """
        data: dict[str, Any] = {
            "name": name,
            "description": description,
            "trigger": trigger,
            "steps": steps,
            "timeout": run_timeout,
            "enabled": enabled,
        }
        return await self._request(method="PUT", path=f"/api/shards/{shard_id}/schedules/{schedule_id}", data=data)

    async def update_shard_snapshot(self, shard_id: str, snapshot_id: str, name: str, description: str, sticky: bool) -> None:
        """Change a snapshot's name, description and stickiness.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/snapshots/{snapshot_id}/meta``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        snapshot_id : :class:`str`
            The snapshot's ID.
        name : :class:`str`
            The new name.
        description : :class:`str`
            The new description.
        sticky : :class:`bool`
            If it's marked to keep or not.

        Raises
        ------
        AMPAPIRequestError
            If there's no such snapshot (400, ``"snapshots.error.notFound"``).

        """
        data: dict[str, Any] = {"name": name, "description": description, "sticky": sticky}
        await self._request(method="PUT", path=f"/api/shards/{shard_id}/snapshots/{snapshot_id}/meta", data=data)

    async def upload_shard_file(self, shard_id: str, path: str, content: bytes, *, chunk_size: int = UPLOAD_CHUNK_SIZE) -> None:
        """Upload one file to a shard in chunks, as the web panel does for a big file.

        |coro|

        Endpoints: ``POST /api/shards/{shard_id}/files/upload-start``, ``.../upload-chunk`` and ``.../upload-commit``

        AMP may already hold part of the file from an earlier try, so we carry on from where it is.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's path, its name included.
        content : :class:`bytes`
            The file.
        chunk_size : :class:`int`, optional
            How many bytes to send at a time, by default 8 MiB like the web panel.

        Raises
        ------
        RuntimeError
            If AMP stops taking the chunks, rather than sending the same one forever.

        """
        upload: ShardUploadSessionResponse = await self.start_shard_file_upload(shard_id=shard_id, path=path, size=len(content))
        received: int = upload["received"]
        while received < len(content):
            reply: ShardUploadChunkResponse = await self.send_shard_file_chunk(
                shard_id=shard_id,
                session_id=upload["sessionId"],
                chunk=content[received : received + chunk_size],
            )
            if reply["received"] <= received:
                msg = f"AMP stopped taking the upload at {received} of {len(content)} bytes. | Path: {path}"
                raise RuntimeError(msg)
            received = reply["received"]

        await self.commit_shard_file_upload(shard_id=shard_id, session_id=upload["sessionId"])

    async def upload_shard_files(self, shard_id: str, folder: str, files: Mapping[str, bytes]) -> None:
        """Upload small files to a folder in a shard, all in one request.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/upload``

        Use :meth:`upload_shard_file` for a big file.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        folder : :class:`str`
            The folder they go in, empty for the shard's own.
        files : Mapping[:class:`str`, :class:`bytes`]
            Each file's path within `folder` to its content, eg. ``{"notes.txt": b"hello"}``.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/upload", files=files, parameters={"path": folder})

    # TODO: Type the reply once AMP is seen answering it live (#3-47.7).
    # The test template can't sleep (U18b), so only the 400 for a shard that isn't asleep was captured.
    async def wake_shard(self, shard_id: str) -> Any:
        """Wake a sleeping shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/wake``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If the shard isn't asleep (400, ``"shards.error.notAsleep"``).

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/wake")
