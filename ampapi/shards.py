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
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Self, Unpack

from ._enums import CloneContent, SnapshotContent, SnapshotKind
from ._types import ShardInfraChanges
from .base import Base
from .errors import AMPAPIRequestError, AMPAPIUploadError

# from .hubs import PanelHub, ShardHub
from .objects import (
    ConsoleHistory,
    ScheduleExecution,
    ShardInfra,
    ShardInfraSaveResult,
    ShardInfraSettings,
    ShardMetrics,
    ShardMigration,
    ShardPlayer,
    ShardSnapshots,
    ShardStatus,
    Snapshot,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ._types import (
        DownloadTicketResponse,
        FileACLChange,
        GatewayPreflightResponse,
        GatewayResponse,
        PortProtocol,
        PublicationResponse,
        ScheduleCatalogResponse,
        ScheduleDefinition,
        ScheduleRunResponse,
        ScheduleStep,
        ScheduleTrigger,
        SettingValues,
        ShardAgentResponse,
        ShardAppConfig,
        ShardArchiveInfoResponse,
        ShardArchiveRequest,
        ShardConfigImportResponse,
        ShardConsoleRequest,
        ShardCreatedResponse,
        ShardCredentialResponse,
        ShardCustomPortRequest,
        ShardDetailsRequest,
        ShardEndpointResponse,
        ShardExtractRequest,
        ShardExtractResponse,
        ShardFileACLResponse,
        ShardFileContentResponse,
        ShardFileIgnoresResponse,
        ShardFileResponse,
        ShardFileStartResponse,
        ShardImportResponse,
        ShardManagedFileResponse,
        ShardMigrationRequest,
        ShardMigrationTargetResponse,
        ShardPortAssignments,
        ShardPortOutcome,
        ShardPortResponse,
        ShardResponse,
        ShardScheduleRequest,
        ShardScheduleResponse,
        ShardSettingCandidatesResponse,
        ShardSettingResponse,
        ShardSFTPResponse,
        ShardUpdateResponse,
        ShardUploadChunkResponse,
        ShardUploadSessionResponse,
        ShardUsage,
        SnapshotMetaRequest,
        SnapshotRequest,
        SnapshotSettingsRequest,
        SnapshotSettingsResponse,
        SpireIPOptionResponse,
    )
    from .panel import Panel
    from .session import Session

__all__ = (
    "Shard",
    "ShardModule",
)

LOGGER: logging.Logger = logging.getLogger(__name__)

# The web panel sends a chunked upload in 8 MiB slices.
UPLOAD_CHUNK_SIZE: int = 8 * 1024 * 1024


# class Shard(ShardHub):
class Shard:
    """A shard, AMP 3's name for an Instance, with the calls that act on it.

    The panel makes these shard objects, of its `shard_class`, from :meth:`Panel.get_shards`, :meth:`Panel.get_shard`,
    :meth:`Panel.create_shard`, :meth:`clone` and a spire's :meth:`Spire.get_shards`, and keeps one object for each
    shard. Each method calls the panel's method of the same purpose with this shard's ID, eg. :meth:`start` is
    :meth:`ShardModule.start_shard` and :meth:`create_gateway` is :meth:`NetworkModule.create_gateway`; the panel's
    method documents the parameters, reply and errors.

    Two shard objects are equal, and hash the same, when they have the same ID, so they work in sets and as dict keys.
    They sort by `display_name`.

    A shard :meth:`Panel.create_shard` made also keeps the rest of that reply, read through :attr:`infra_settings`,
    :attr:`app_config`, :attr:`port_assignments`, :attr:`port_outcomes` and :attr:`over_licence_limit`. They are
    `None` on any other shard, and nothing can set them after the object is made.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    module : :class:`Panel`
        The panel the calls go through.
    data : :class:`ShardResponse`
        The shard as AMP sent it.
    created : Union[:class:`ShardCreatedResponse`, None], optional
        The whole reply of :meth:`Panel.create_shard` when that made this shard, by default None.

    Attributes
    ----------
    id : :class:`str`
        The shard's ID.
    display_name : :class:`str`
        The shard's name.
    data : :class:`ShardResponse`
        The data response as AMP sent it, when this object was made.
        - The panel brings `data` up to date each time the panel hands this object out again.
    session : :class:`Session`
        The panel's session.

    """

    # A subclass can declare listeners, eg. ``@ShardHub.listener(name="console")``; see :class:`ShardHub`. Made by hand,
    # eg. ``MyShard(module=panel, data=record)``, it listens once the panel does, as long as you keep a reference to it.
    # auto_state : Union[:class:`bool`, None], optional
    #     If `state` follows the shard's state events from the hub or not; read back with the property. By default None
    #     for the panel's `auto_state` (False unless the panel was made with True), or False with no panel.

    data: ShardResponse
    display_name: str
    id: str
    session: Session
    # _module: ShardModule
    _module: Panel
    # The whole `create_shard` reply, or None for a shard that didn't come from it; only the properties read it.
    _created: Optional[ShardCreatedResponse]

    # def __init__(self, module: ShardModule, data: ShardResponse, *, auto_state: Optional[bool] = None) -> None:
    def __init__(self, module: Panel, data: ShardResponse, *, created: Optional[ShardCreatedResponse] = None) -> None:  # noqa: D107
        # super().__init__(session=module.session, panel=module if isinstance(module, PanelHub) else None, auto_state=auto_state)
        self.session = module.session
        self._module = module
        self.data = data
        self.id = data["id"]
        self.display_name = data["displayName"]
        self._created = created

        # if self._panel is not None:
        #     self._panel._register_shard(shard=self)

    @property
    def app_config(self) -> Optional[ShardAppConfig]:
        """The game settings AMP gave the shard when :meth:`Panel.create_shard` made it, or `None` for any other shard.

        :meth:`get_settings` gives the current values.
        """
        return self._created["appConfig"] if self._created is not None else None

    @property
    def infra_settings(self) -> Optional[ShardInfraSettings]:
        """How the shard ran when :meth:`Panel.create_shard` made it, or `None` for any other shard.

        :meth:`get_infra` gives the current settings, as its `ShardInfra.settings`.
        """
        return ShardInfraSettings(data=self._created["infraSettings"]) if self._created is not None else None

    @property
    def over_licence_limit(self) -> Optional[bool]:
        """If making the shard took the panel over its licence's shard limit or not.

        `None` for a shard :meth:`Panel.create_shard` didn't make, as AMP only says so in that reply.
        """
        return self._created["overLicenceLimit"] if self._created is not None else None

    @property
    def port_assignments(self) -> Optional[ShardPortAssignments]:
        """The ports AMP gave the shard when :meth:`Panel.create_shard` made it, or `None` for any other shard.

        :meth:`get_ports` gives the current ports.
        """
        return self._created["ports"] if self._created is not None else None

    @property
    def port_outcomes(self) -> Optional[list[ShardPortOutcome]]:
        """How each port was given out when :meth:`Panel.create_shard` made the shard, eg. one moved off a port in use.

        `None` for any other shard, as AMP only says so in that reply.
        """
        return self._created["portOutcomes"] if self._created is not None else None

    def __hash__(self) -> int:  # noqa: D105
        return hash(self.id)

    def __eq__(self, other: object) -> bool:  # noqa: D105
        # Another type answers `NotImplemented`, so Python asks the other side, and sorting a mixed list raises (#3-51.3h)
        if not isinstance(other, Shard):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, Shard):
            return NotImplemented
        return self.display_name < other.display_name

    def __repr__(self) -> str:  # noqa: D105
        return f"<{type(self).__name__} id={self.id!r} display_name={self.display_name!r}>"

    def _update_data(self, data: ShardResponse) -> None:
        """Take in the shard as AMP sent it again, from the panel or from one of this shard's own calls.

        A subclass overrides it, calling it through `super()`, to refresh anything it works out from `data`.
        """
        self.data = data
        self.display_name = data["displayName"]

    async def accept_eula(self) -> None:
        """Accept the game's licence for this shard, see :meth:`ShardModule.accept_shard_eula`.

        |coro|

        """
        await self._module.accept_shard_eula(shard_id=self.id)

    async def decline_eula(self) -> None:
        """Decline the game's licence for this shard, see :meth:`ShardModule.decline_shard_eula`.

        |coro|

        """
        await self._module.decline_shard_eula(shard_id=self.id)

    async def acknowledge_disk_warning(self) -> ShardResponse:
        """Dismiss this shard's disk warning, see :meth:`ShardModule.acknowledge_shard_disk_warning`.

        |coro|

        """
        result: ShardResponse = await self._module.acknowledge_shard_disk_warning(shard_id=self.id)
        self._update_data(data=result)
        return result

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
    ) -> Shard:
        """Copy this shard into a new one, see :meth:`Panel.clone_shard`.

        |coro|

        """
        return await self._module.clone_shard(shard_id=self.id, new_name=new_name, content=content, target_spire_id=target_spire_id)

    async def commit_file_upload(self, session_id: str) -> None:
        """Finish a chunked upload to this shard, see :meth:`ShardModule.commit_shard_file_upload`.

        |coro|

        """
        await self._module.commit_shard_file_upload(shard_id=self.id, session_id=session_id)

    async def copy_file(self, source: str, destination: str) -> Optional[ShardExtractResponse]:
        """Copy a file or folder in this shard, see :meth:`ShardModule.copy_shard_file`.

        |coro|

        """
        return await self._module.copy_shard_file(shard_id=self.id, source=source, destination=destination)

    async def create_custom_port(self, name: str, protocol: PortProtocol, port: Optional[int] = None) -> list[ShardPortResponse]:
        """Add a port to this shard, see :meth:`ShardModule.create_shard_custom_port`.

        |coro|

        """
        return await self._module.create_shard_custom_port(shard_id=self.id, name=name, protocol=protocol, port=port)

    async def create_file_download_ticket(self, path: str) -> DownloadTicketResponse:
        """Get a browser's download ticket for a file in this shard, see :meth:`ShardModule.create_shard_file_download_ticket`.

        |coro|

        """
        return await self._module.create_shard_file_download_ticket(shard_id=self.id, path=path)

    async def create_folder(self, path: str) -> None:
        """Make a folder in this shard, see :meth:`ShardModule.create_shard_folder`.

        |coro|

        """
        await self._module.create_shard_folder(shard_id=self.id, path=path)

    async def create_gateway(self, front_spire_id: str) -> GatewayResponse:
        """Route this shard through a front spire, see :meth:`NetworkModule.create_gateway`.

        |coro|

        """
        return await self._module.create_gateway(shard_id=self.id, front_spire_id=front_spire_id)

    async def create_publication(
        self,
        front_spire_id: str,
        public_port: int,
        port_reference: str,
        *,
        front_public_host: Optional[str] = None,
    ) -> PublicationResponse:
        """Forward a public port on a front spire to one of this shard's ports, see :meth:`NetworkModule.create_publication`.

        |coro|

        """
        return await self._module.create_publication(
            front_spire_id=front_spire_id,
            public_port=public_port,
            shard_id=self.id,
            port_reference=port_reference,
            front_public_host=front_public_host,
        )

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

    async def create_snapshot_download_ticket(self, snapshot_id: str) -> DownloadTicketResponse:
        """Get a browser's download ticket for a snapshot of this shard, see :meth:`ShardModule.create_shard_snapshot_download_ticket`.

        |coro|

        """
        return await self._module.create_shard_snapshot_download_ticket(shard_id=self.id, snapshot_id=snapshot_id)

    async def delete(self) -> ShardResponse:
        """Delete this shard, which it can come back from until it's purged, see :meth:`ShardModule.delete_shard`.

        |coro|

        """
        result: ShardResponse = await self._module.delete_shard(shard_id=self.id)
        self._update_data(data=result)
        return result

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

    async def extract_archive(self, path: str, destination: Optional[str] = None, *, overwrite: bool = False) -> ShardExtractResponse:
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

    async def get_console_history(self, *, limit: Optional[int] = None, before_seq: Optional[int] = None) -> ConsoleHistory:
        """Get this shard's console lines, see :meth:`ShardModule.get_shard_console_history`.

        |coro|

        """
        return await self._module.get_shard_console_history(shard_id=self.id, limit=limit, before_seq=before_seq)

    async def get_credential(self) -> ShardCredentialResponse:
        """Get the stored secret this shard uses, see :meth:`ShardModule.get_shard_credential`.

        |coro|

        """
        return await self._module.get_shard_credential(shard_id=self.id)

    async def get_disk(self) -> Optional[ShardUsage]:
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
        """Get one file's or folder's details from this shard, see :meth:`ShardModule.get_shard_file_info`.

        |coro|

        """
        return await self._module.get_shard_file_info(shard_id=self.id, path=path)

    async def get_file_start(self) -> ShardFileStartResponse:
        """Get the folder in this shard the web panel's file manager opens at, see :meth:`ShardModule.get_shard_file_start`.

        |coro|

        """
        return await self._module.get_shard_file_start(shard_id=self.id)

    async def get_files(self, path: str = "") -> list[ShardFileResponse]:
        """Get the files and folders in one of this shard's folders, see :meth:`ShardModule.get_shard_files`.

        |coro|

        """
        return await self._module.get_shard_files(shard_id=self.id, path=path)

    async def get_import(self) -> Optional[ShardImportResponse]:
        """Get how this shard's import went, see :meth:`ShardModule.get_shard_import`.

        |coro|

        """
        return await self._module.get_shard_import(shard_id=self.id)

    async def get_infra(self) -> ShardInfra:
        """Get how this shard runs, see :meth:`ShardModule.get_shard_infra`.

        |coro|

        """
        return await self._module.get_shard_infra(shard_id=self.id)

    async def get_ip_options(self) -> list[SpireIPOptionResponse]:
        """Get the addresses this shard can bind to, see :meth:`ShardModule.get_shard_ip_options`.

        |coro|

        """
        return await self._module.get_shard_ip_options(shard_id=self.id)

    async def get_managed_files(self, path: str) -> list[ShardManagedFileResponse]:
        """Get which files under a path AMP writes itself, see :meth:`ShardModule.get_shard_managed_files`.

        |coro|

        """
        return await self._module.get_shard_managed_files(shard_id=self.id, path=path)

    async def get_metrics(self, *, minutes: Optional[int] = None) -> list[ShardMetrics]:
        """Get this shard's recent load, see :meth:`ShardModule.get_shard_metrics`.

        |coro|

        """
        return await self._module.get_shard_metrics(shard_id=self.id, minutes=minutes)

    async def get_migration(self) -> Optional[ShardMigration]:
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

    async def get_schedule(self, schedule_id: str) -> ShardScheduleResponse:
        """Get one of this shard's schedules, see :meth:`ShardModule.get_shard_schedule`.

        |coro|

        """
        return await self._module.get_shard_schedule(shard_id=self.id, schedule_id=schedule_id)

    async def get_schedule_catalog(self) -> ScheduleCatalogResponse:
        """Get the triggers and tasks this shard's schedules can use, see :meth:`ShardModule.get_shard_schedule_catalog`.

        |coro|

        """
        return await self._module.get_shard_schedule_catalog(shard_id=self.id)

    async def get_schedule_history(self, schedule_id: str, *, limit: Optional[int] = None) -> list[ScheduleExecution]:
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

    async def get_snapshots(self) -> ShardSnapshots:
        """Get this shard's snapshots, see :meth:`ShardModule.get_shard_snapshots`.

        |coro|

        """
        return await self._module.get_shard_snapshots(shard_id=self.id)

    async def get_state(self) -> ShardStatus:
        """Get this shard's live state, see :meth:`ShardModule.get_shard_state`.

        |coro|

        """
        return await self._module.get_shard_state(shard_id=self.id)

    async def get_users(self) -> list[ShardPlayer]:
        """Get the players on this shard, see :meth:`ShardModule.get_shard_users`.

        |coro|

        """
        return await self._module.get_shard_users(shard_id=self.id)

    async def import_config(self, path: str, *, content: Optional[str] = None) -> ShardConfigImportResponse:
        """Read this shard's settings back from a config file, see :meth:`ShardModule.import_shard_config`.

        |coro|

        """
        return await self._module.import_shard_config(shard_id=self.id, path=path, content=content)

    async def migrate_to_spire(
        self,
        target_spire_id: str,
        target_datastore_id: str,
        *,
        bring_backups: bool = False,
        stop_if_running: bool = False,
        start_after_move: Optional[bool] = None,
    ) -> None:
        """Move this shard to another spire, see :meth:`ShardModule.migrate_shard_to_spire`.

        |coro|

        """
        await self._module.migrate_shard_to_spire(
            shard_id=self.id,
            target_spire_id=target_spire_id,
            target_datastore_id=target_datastore_id,
            bring_backups=bring_backups,
            stop_if_running=stop_if_running,
            start_after_move=start_after_move,
        )

    async def move_file(self, source: str, destination: str) -> None:
        """Move or rename a file or folder in this shard, see :meth:`ShardModule.move_shard_file`.

        |coro|

        """
        await self._module.move_shard_file(shard_id=self.id, source=source, destination=destination)

    async def preflight_gateway(self, front_spire_id: str) -> GatewayPreflightResponse:
        """Check a gateway for this shard can be made, see :meth:`NetworkModule.preflight_gateway`.

        |coro|

        """
        return await self._module.preflight_gateway(shard_id=self.id, front_spire_id=front_spire_id)

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

    async def refresh(self) -> Self:
        """Read this shard from AMP again, so `data` and `display_name` are current, see :meth:`Panel.get_shard`.

        |coro|

        Returns
        -------
        Self
            This shard.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the shard is purged.\n
            **409** - If the shard is deleted `shards.error.deleted`.

        """
        current: Shard = await self._module.get_shard(shard_id=self.id)
        # A shard object made by hand isn't the object the panel keeps, so it copies the fresh data from the panel's object
        if current is not self:
            self._update_data(data=current.data)

        return self

    async def restart(self) -> None:
        """Restart this shard's game, see :meth:`ShardModule.restart_shard`.

        |coro|

        """
        await self._module.restart_shard(shard_id=self.id)

    async def restore(self) -> ShardResponse:
        """Bring this deleted shard back, see :meth:`ShardModule.restore_shard`.

        |coro|

        """
        result: ShardResponse = await self._module.restore_shard(shard_id=self.id)
        self._update_data(data=result)
        return result

    async def restore_snapshot(self, snapshot_id: str) -> Snapshot:
        """Restore this shard to one of its snapshots, see :meth:`ShardModule.restore_shard_snapshot`.

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

    async def set_credential(self, credential_id: str) -> ShardCredentialResponse:
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
        result: ShardResponse = await self._module.set_shard_details(
            shard_id=self.id,
            display_name=display_name,
            description=description,
            tags=tags,
        )
        self._update_data(data=result)
        return result

    async def set_file_acl(self, path: str, changes: list[FileACLChange]) -> ShardFileACLResponse:
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

    async def set_settings(self, values: SettingValues) -> None:
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
        result: ShardResponse = await self._module.suspend_shard(shard_id=self.id)
        self._update_data(data=result)
        return result

    async def take_snapshot(
        self,
        name: Optional[str],
        kind: SnapshotKind,
        content: SnapshotContent,
        *,
        description: Optional[str] = None,
        sticky: bool = False,
    ) -> Snapshot:
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
        result: ShardResponse = await self._module.unsuspend_shard(shard_id=self.id)
        self._update_data(data=result)
        return result

    async def update(self) -> ShardUpdateResponse:
        """Install or update this shard's game, see :meth:`ShardModule.update_shard`.

        |coro|

        """
        return await self._module.update_shard(shard_id=self.id)

    async def update_infra(
        self,
        settings: Optional[ShardInfraSettings] = None,
        **changes: Unpack[ShardInfraChanges],
    ) -> ShardInfraSaveResult:
        """Change any available settings for how this shard runs, keeping the rest, see :meth:`ShardModule.update_shard_infra`.

        |coro|

        """
        return await self._module.update_shard_infra(shard_id=self.id, settings=settings, **changes)

    async def update_schedule(
        self,
        schedule_id: str,
        name: Optional[str] = None,
        trigger: Optional[ScheduleTrigger] = None,
        steps: Optional[list[ScheduleStep]] = None,
        *,
        description: Optional[str] = None,
        run_timeout: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> ShardScheduleResponse:
        """Change one of this shard's schedules, see :meth:`ShardModule.update_shard_schedule`.

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

    async def upload_file(self, path: str, content: bytes, *, chunk_size: int = UPLOAD_CHUNK_SIZE, resume: bool = False) -> None:
        """Upload one file to this shard in chunks, see :meth:`ShardModule.upload_shard_file`.

        |coro|

        """
        await self._module.upload_shard_file(shard_id=self.id, path=path, content=content, chunk_size=chunk_size, resume=resume)

    async def upload_files(self, folder: str, files: Mapping[str, bytes]) -> None:
        """Upload files to a folder in this shard in one request, see :meth:`ShardModule.upload_shard_files`.

        |coro|

        """
        await self._module.upload_shard_files(shard_id=self.id, folder=folder, files=files)

    async def wake(self) -> None:
        """Wake this sleeping shard, see :meth:`ShardModule.wake_shard`.

        |coro|

        """
        await self._module.wake_shard(shard_id=self.id)


class ShardModule(Base):
    """The calls for one shard, AMP 3's name for an Instance, each taking its ID: lifecycle, power, console, settings,
    ports, files, schedules, snapshots and moves.

    The calls over all of the panel's shards, eg. :meth:`Panel.get_shards` and :meth:`Panel.create_shard`, are on the
    :class:`Panel`.

    .. versionadded:: 6.0.0

    """

    async def accept_shard_eula(self, shard_id: str) -> None:
        """Accept the game's licence for a shard, eg. Minecraft's EULA, which the shard needs before it can start.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/eula/accept``

        - AMP records the acceptance in the game's own settings, eg. Minecraft's ``eula.txt``, and in the audit log.
        - A shard held waiting on its licence (see :meth:`decline_shard_eula`) has its `ShardStatus.status` set back to
          `ShardState.stopped`, from AMP's docs and not seen live. Accepting doesn't start the shard, so call
          :meth:`start_shard` after.
        - For a game with no licence, the call changes nothing, from AMP's docs and not seen live.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/eula/accept")

    async def decline_shard_eula(self, shard_id: str) -> None:
        """Decline the game's licence for a shard that's waiting on the licence.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/eula/decline``

        A start no person was waiting on, eg. a scheduled start or a start on boot, holds a shard whose licence isn't
        accepted. While the shard is held, its `ShardStatus.status` reads `ShardState.awaiting_user_action` and its
        `ShardStatus.awaits_licence` is `True`.

        - Declining sets the shard's `ShardStatus.status` back to `ShardState.stopped`. Nothing is accepted.
        - The next start asks for the licence again.
        - A shard that isn't waiting on its licence is left as it is, with no error.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/eula/decline")

    async def acknowledge_shard_disk_warning(self, shard_id: str) -> ShardResponse:
        """Dismiss a shard's disk warning.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/disk-warning/ack``

        It silences only the first, advisory level, and AMP clears it once a scan finds the shard back under the limit.

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
        data: ShardArchiveRequest = {"paths": paths, "destination": destination}
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
            **409** - If no move is running `shards.migration.notRunning`. The shard may have had no move, or its last
            move is done, failed, cancelled or dismissed.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/migration/cancel")

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

        Raises
        ------
        AMPAPIRequestError
            **400** - If AMP holds fewer bytes than the `size` the upload started with `files.error.uploadIncomplete`.
            The error's `params` holds the `expected` and `received` byte counts as strings.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/upload-commit", parameters={"session": session_id})

    async def copy_shard_file(self, shard_id: str, source: str, destination: str) -> Optional[ShardExtractResponse]:
        """Copy a file or folder inside a shard, or out of an archive in it.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/copy``

        A `source` inside an archive, eg. ``"backup.zip/world/level.dat"``, copies that entry out of it, and overwrites a
        file already at `destination`. An entry the archive doesn't have isn't an error: every count reads 0.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        source : :class:`str`
            The path to copy.
        destination : :class:`str`
            The copy's path.

        Returns
        -------
        Union[:class:`ShardExtractResponse`, None]
            How many files came out of the archive, for a copy out of one (a 200); `None` for any other copy (a 204).

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/files/copy", data={"from": source, "to": destination})

    async def create_shard_custom_port(
        self,
        shard_id: str,
        name: str,
        protocol: PortProtocol,
        port: Optional[int] = None,
    ) -> list[ShardPortResponse]:
        """Add a port of your own to a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/ports/custom``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        name : :class:`str`
            The port's name; its `ref` becomes ``"Custom"`` and the name without spaces.
        protocol : :class:`PortProtocol`
            ``"TCP"``, ``"UDP"`` or ``"Both"``. AMP stores anything else as ``"TCP"``.
        port : Union[:class:`int`, None], optional
            The port number, by default None for AMP to pick a free port.

        Returns
        -------
        list[:class:`ShardPortResponse`]
            All of the shard's ports.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the port is taken `shards.error.portConflict`.\n
            **400** - If the port is out of range `shards.error.invalidPort`.\n
            **400** - If AMP uses the port itself, eg. 4222 for its message bus `shards.error.portReservedByAmp`.

        """
        data: ShardCustomPortRequest = {"name": name, "protocol": protocol, "port": port}
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/ports/custom", data=data)

    async def create_shard_file_download_ticket(self, shard_id: str, path: str) -> DownloadTicketResponse:
        """Get a download ticket for a file in a shard, for a browser link to the file.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/download-ticket``

        A browser follows a link with no `Authorization` header, so the web panel puts a ticket in the link instead:
        ``GET /api/shards/{shard_id}/files/download?path=...&ticket=...``. Hand a ticket to a person's browser, eg. from
        a bot. :meth:`download_shard_file` needs no ticket.

        - AMP takes the ticket once, within 60 seconds.
        - The ticket works only for the logged in user's session, this shard and this `path`.
        - AMP runs the download's checks when it makes the ticket, and again when the ticket is used.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's path.

        Returns
        -------
        :class:`DownloadTicketResponse`
            The ticket and when it runs out.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the logged in user may not read the file, from AMP's docs and not seen live.\n
            **403** - If the panel's file type rules block the download, from AMP's docs and not seen live.\n
            **404** - If there's no file at the path `files.error.notFound`.\n
            **404** - If the path is a folder `files.error.notFound`, from AMP's docs and not seen live.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/files/download-ticket", data={"path": path})

    async def create_shard_folder(self, shard_id: str, path: str) -> None:
        """Make a folder inside a shard. A folder that's already there is fine.

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

    # TODO: Drop the 500 from Raises once AMP answers a step with no `type` with a 400 (U16).
    # AMP 3.0.0 and 3.0.1 answer 500 to a schedule step that has no `type` key.
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

        The user who makes it is the one its runs act as, its `runAsUserId`.

        An enabled ``"interval"`` schedule runs once within seconds of being made, for the time slot just past. Eg. an
        hourly schedule made at 07:07 runs straight away for the 07:00 slot (its `canonicalFireTime`), then at 08:00.

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
            A description, by default None. AMP trims it.
        run_timeout : Union[:class:`str`, None], optional
            How long a run may take, as a time span, by default None (AMP uses ``"00:30:00"``). AMP calls it `timeout`,
            and keeps it between 1 minute and 2 hours.
        enabled : :class:`bool`, optional
            If it runs on its trigger or not, by default False.

        Returns
        -------
        :class:`ShardScheduleResponse`
            The schedule.

        Raises
        ------
        AMPAPIRequestError
            **400** - If a step or the trigger has an unknown `type`.\n
            **500** - If a step has no `type` at all.

        """
        data: ShardScheduleRequest = {
            "name": name,
            "description": description,
            "trigger": trigger,
            "steps": steps,
            "timeout": run_timeout,
            "enabled": enabled,
        }

        return await self._request(method="POST", path=f"/api/shards/{shard_id}/schedules", data=data)

    async def create_shard_snapshot_download_ticket(self, shard_id: str, snapshot_id: str) -> DownloadTicketResponse:
        """Get a download ticket for one of a shard's snapshots, for a browser link to the snapshot's zip.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/snapshots/{snapshot_id}/download-ticket``

        A browser follows a link with no `Authorization` header, so the web panel puts a ticket in the link instead:
        ``GET /api/shards/{shard_id}/snapshots/{snapshot_id}/download?ticket=...``. Hand a ticket to a person's
        browser, eg. from a bot. :meth:`download_shard_snapshot` needs no ticket.

        - AMP takes the ticket once, within 60 seconds.
        - The ticket works only for the logged in user's session, this shard and this snapshot.
        - AMP runs the download's checks when it makes the ticket, and again when the ticket is used.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        snapshot_id : :class:`str`
            The snapshot's ID.

        Returns
        -------
        :class:`DownloadTicketResponse`
            The ticket and when it runs out.

        Raises
        ------
        AMPAPIRequestError
            **404** - If there's no snapshot with that ID, from AMP's docs and not seen live.\n
            **404** - If the snapshot's zip is missing, from AMP's docs and not seen live.\n
            **409** - If the snapshot is stored on another spire, from AMP's docs and not seen live.

        """
        path: str = f"/api/shards/{shard_id}/snapshots/{snapshot_id}/download-ticket"
        return await self._request(method="POST", path=path)

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

        A shard with no stored secret is fine too.

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

        Raises
        ------
        AMPAPIRequestError
            **409** - If a publication still forwards to the port. Remove the publication first, see
            :meth:`NetworkModule.delete_publication`.

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

        Raises
        ------
        AMPAPIRequestError
            If the delete reached a folder another disk is mounted at (``"shards.error.deleteStoppedAtMount"``); the
            rest of `path` is deleted.
            If `path` is a folder another disk is mounted at (``"shards.error.deleteIsMount"``); nothing is deleted.

        """
        await self._request(method="DELETE", path=f"/api/shards/{shard_id}/files", parameters={"path": path})

    # TODO: Reword Raises once AMP refuses an early dismissal cleanly (U22a).
    # AMP 3.0.0 and 3.0.1 answer 500 to a dismissal while the move is starting or copying.
    async def delete_shard_migration(self, shard_id: str) -> None:
        """Dismiss a shard's done or failed move, so :meth:`get_shard_migration` has no move to show.

        |coro|

        Endpoint: ``DELETE /api/shards/{shard_id}/migration``

        Dismissing only clears the move's record. The copy a move leaves on the old spire stays until
        :meth:`SpireModule.purge_spire_orphan_directory`, and a failed move's task stays in
        :meth:`TaskModule.get_running_tasks` for about 30 minutes, or until :meth:`TaskModule.delete_running_task`.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Raises
        ------
        AMPAPIRequestError
            **500** - If the move is still copying or was only just started `common.error.unexpected`. The move
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
            **400** - If other snapshots build on the snapshot `snapshots.error.hasDependents`.\n
            **409** - If the shard's spire refuses the delete, from AMP's docs and not seen live.\n
            **503** - If the shard's spire doesn't answer, from AMP's docs and not seen live.

        """
        await self._request(method="DELETE", path=f"/api/shards/{shard_id}/snapshots/{snapshot_id}")

    # TODO: Reword Raises once AMP refuses a folder's download with its own error (U17).
    # AMP 3.0.1 answers a folder's download with 404 "files.error.notFound", saying the folder no longer exists.
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
            **404** - If there's no file at the path `files.error.notFound`.\n
            **404** - If the path is a folder `files.error.notFound`. AMP's message says the folder no longer exists,
            though the folder is there.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/download", parameters={"path": path}, raw_bytes=True)

    async def download_shard_files(self, shard_id: str, paths: list[str]) -> bytes:
        """Download files and folders from a shard as one zip.

        |coro|

        Endpoints: ``POST /api/shards/{shard_id}/files/zip-ticket``, then ``GET /api/shards/{shard_id}/files/zip``

        AMP zips through a ticket. This call asks for a ticket that names the paths, then sends the ticket as the zip
        request's `ticket` query parameter at once, as a ticket works only once and only for 60 seconds.

        - The zip skips any path the logged in user may not read.
        - Entry names in the zip are relative to the folder that holds the first path.

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

        Raises
        ------
        AMPAPIRequestError
            **400** - If `paths` is empty `files.error.nothingSelected`.\n
            **400** - If `paths` holds more than a ticket takes `files.error.tooManySelected`, from AMP's docs and not
            seen live.\n
            **403** - If the logged in user may not read the first path, from AMP's docs and not seen live.\n
            **404** - If there's no shard with that ID, from AMP's docs and not seen live.

        """
        ticket: DownloadTicketResponse = await self._request(
            method="POST",
            path=f"/api/shards/{shard_id}/files/zip-ticket",
            data={"paths": paths},
        )
        path: str = f"/api/shards/{shard_id}/files/zip"
        return await self._request(method="GET", path=path, parameters={"ticket": ticket["ticket"]}, raw_bytes=True)

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
            The zip as it came, all of it in memory.

        Raises
        ------
        AMPAPIRequestError
            **409** - If the snapshot is stored on another spire, from AMP's docs and not seen live.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/snapshots/{snapshot_id}/download", raw_bytes=True)

    async def extract_shard_archive(
        self,
        shard_id: str,
        path: str,
        destination: Optional[str] = None,
        *,
        overwrite: bool = False,
    ) -> ShardExtractResponse:
        """Unpack an archive inside a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/extract``

        A file the logged in user may not write, or a file AMP writes itself from the settings, is skipped rather than
        failing the rest of the archive.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The archive's path, or a folder or file inside it to unpack only that.
        destination : Union[:class:`str`, None], optional
            The folder to unpack it into, by default None for the archive's own folder.
        overwrite : :class:`bool`, optional
            If files already there should be replaced or not, by default False.

        Returns
        -------
        :class:`ShardExtractResponse`
            How many files came out, and how many were skipped.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `path` isn't an archive.

        """
        data: ShardExtractRequest = {"path": path, "destination": destination, "overwrite": overwrite}
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/files/extract", data=data)

    async def get_shard_agent(self, shard_id: str) -> ShardAgentResponse:
        """Get the AMP agent that runs a shard, and if it's out of date.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/agent``

        It only means something for a running shard, as a stopped one starts with the newest agent anyway.

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
    ) -> ConsoleHistory:
        """Get a shard's console lines, oldest first.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/console/history``

        To page back, pass the first line's `seq` as `before_seq` while `has_more` is True.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        limit : Union[:class:`int`, None], optional
            The most lines to get, by default None (AMP's 300). 0 still gives one.
        before_seq : Union[:class:`int`, None], optional
            Only lines before this `seq`, for paging back, by default None for the newest.

        Returns
        -------
        :class:`ConsoleHistory`
            The lines, each marker's `state` a :class:`ShardState`.

        """
        filters: dict[str, Optional[int]] = {"limit": limit, "beforeSeq": before_seq}
        parameters: dict[str, int] = self._without_none(mapping=filters)
        result: dict[str, Any] = await self._request(
            method="GET",
            path=f"/api/shards/{shard_id}/console/history",
            parameters=parameters,
        )
        return ConsoleHistory(data=result)

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

    async def get_shard_disk(self, shard_id: str) -> Optional[ShardUsage]:
        """Get a shard's disk use against its disk limit.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/disk``

        AMP only answers it for a shard with a disk limit, its `ShardInfraSettings.disk_limit_mb`; for any other
        it is a 204, running or stopped and even after :meth:`SpireModule.rescan_spire_usage`. It is the spire's last
        disk scan, not measured on the call. An exceeded limit doesn't list the shard in
        :meth:`Panel.get_shards_awaiting_action`. AMP stops the shard at the first disk scan that finds it over the limit.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        Union[:class:`ShardUsage`, None]
            The shard's entry from :meth:`SpireModule.get_spire_usage`, its `limitLevel` ``"Critical"`` near the limit and
            ``"Exceeded"`` once the use passes the limit; `None` (a 204) with no disk limit, before a scan has covered the
            shard or when the scan didn't find its folder. Read `None` as unknown, never as under the limit.

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
            **404** - If there's no file at the path `files.error.notFound`.

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
        """Get one file's or folder's details from a shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/stat``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's or folder's path.

        Returns
        -------
        :class:`ShardFileResponse`
            The file's size and when it changed. A folder's `isDirectory` is `True`.

        Raises
        ------
        AMPAPIRequestError
            **404** - If there's no file at the path `files.error.notFound`.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/stat", parameters={"path": path})

    async def get_shard_file_start(self, shard_id: str) -> ShardFileStartResponse:
        """Get the folder in a shard the web panel's file manager opens at for the logged in user.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/start``

        AMP answers the shard's own folder when the logged in user may read that folder. Otherwise AMP walks down from
        the shard's folder toward the paths the logged in user was granted, and stops at the first folder the logged in
        user may read or where the grants branch.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardFileStartResponse`
            The folder, its `path` empty for the shard's own folder.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the logged in user may read no path in the shard, from AMP's docs and not seen live.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/start")

    async def get_shard_files(self, shard_id: str, path: str = "") -> list[ShardFileResponse]:
        """Get the files and folders in one of a shard's folders.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`, optional
            The folder, by default "" (the shard's own folder). A folder that isn't there gives an empty list.

        Returns
        -------
        list[:class:`ShardFileResponse`]
            The entries, each `path` relative to the shard's folder. AMP's own ``.amp`` folder and anything the logged in
            user may not read are left out.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the path leaves the shard's folder, eg. ``"../.."`` `files.error.pathInvalid`. The error's
            `params` holds the `reason` ``"shards.error.pathEscapesShard"``.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files", parameters={"path": path})

    async def get_shard_import(self, shard_id: str) -> Optional[ShardImportResponse]:
        """Get how the import that made the shard went, see :meth:`SpireModule.import_spire_servers`.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/import``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        Union[:class:`ShardImportResponse`, None]
            The import record, `None` for a shard that wasn't imported (a 204).

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/import")

    async def get_shard_infra(self, shard_id: str) -> ShardInfra:
        """Get how a shard runs, and what its spire and template allow.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/infra``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardInfra`
            The shard's `ShardInfra.settings`, which :meth:`update_shard_infra` changes, and what its spire and template
            allow.

        """
        result: dict[str, Any] = await self._request(method="GET", path=f"/api/shards/{shard_id}/infra")
        return ShardInfra(data=result)

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

    async def get_shard_managed_files(self, shard_id: str, path: str) -> list[ShardManagedFileResponse]:
        """Get which files under a path AMP writes itself from the settings.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/files/managed``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The path. Only the shard's root (``""`` or ``"/"``) has listed anything; a folder or a file gives an empty
            list, even ``"server.properties"`` itself.

        Returns
        -------
        list[:class:`ShardManagedFileResponse`]
            The managed files, eg. a Minecraft shard's ``"server.properties"`` and ``"eula.txt"``.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/files/managed", parameters={"path": path})

    async def get_shard_metrics(self, shard_id: str, *, minutes: Optional[int] = None) -> list[ShardMetrics]:
        """Get a running shard's recent load, one sample every few seconds.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/metrics``

        AMP keeps about the last 2 hours in memory.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        minutes : Union[:class:`int`, None], optional
            How far back to go, by default None. 0 or less gives all AMP keeps.

        Returns
        -------
        list[:class:`ShardMetrics`]
            The samples, empty while stopped.

        """
        parameters: dict[str, int] = self._without_none(mapping={"minutes": minutes})
        result: list[dict[str, Any]] = await self._request(method="GET", path=f"/api/shards/{shard_id}/metrics", parameters=parameters)
        return [ShardMetrics(data=entry) for entry in result]

    async def get_shard_migration(self, shard_id: str) -> Optional[ShardMigration]:
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
        Union[:class:`ShardMigration`, None]
            The move, its `status` a :class:`MigrationStatus`; `None` when there's none (a 204).

        """
        result: Optional[dict[str, Any]] = await self._request(method="GET", path=f"/api/shards/{shard_id}/migration")
        return ShardMigration(data=result) if result is not None else None

    async def get_shard_migration_targets(self, shard_id: str) -> list[ShardMigrationTargetResponse]:
        """Get the other datastores on a shard's own spire it could move to, for :meth:`start_shard_migration`.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/migration/targets``

        It doesn't list other spires. To move a shard to another spire, pick one from :meth:`Panel.get_spires`
        and a datastore from :meth:`SpireModule.get_spire_datastores`, for :meth:`migrate_shard_to_spire`.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`ShardMigrationTargetResponse`]
            The spire's other datastores, without the datastore the shard is in; empty when the spire has a single
            datastore.

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

    async def get_shard_schedule(self, shard_id: str, schedule_id: str) -> ShardScheduleResponse:
        """Get one of a shard's schedules.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/schedules/{schedule_id}``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        schedule_id : :class:`str`
            The schedule's ID.

        Returns
        -------
        :class:`ShardScheduleResponse`
            The schedule, with how it last ran; the same as its entry in :meth:`get_shard_schedules`.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the shard has no schedule with that ID.

        """
        return await self._request(method="GET", path=f"/api/shards/{shard_id}/schedules/{schedule_id}")

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
    ) -> list[ScheduleExecution]:
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
            The most runs to get, by default None (AMP's 50). AMP keeps it between 1 and 200.

        Returns
        -------
        list[:class:`ScheduleExecution`]
            The runs.

        """
        parameters: dict[str, int] = self._without_none(mapping={"limit": limit})
        path: str = f"/api/shards/{shard_id}/schedules/{schedule_id}/history"
        result: list[dict[str, Any]] = await self._request(method="GET", path=path, parameters=parameters)
        return [ScheduleExecution(data=entry) for entry in result]

    async def get_shard_schedules(self, shard_id: str) -> list[ShardScheduleResponse]:
        """Get a shard's schedules.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/schedules``

        A user who can read the schedules but not change them gets a webhook step's `url` and `body` as
        ``"[withheld]"``, listed in each schedule's `withheld`.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`ShardScheduleResponse`]
            The schedules, oldest first, with how each last ran.

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
            **404** - If the setting has no list `shards.error.noValueSource`.

        """
        return await self._request(
            method="GET",
            path=f"/api/shards/{shard_id}/settings/{field_name}/candidates",
            parameters={"refresh": refresh},
        )

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

    async def get_shard_snapshots(self, shard_id: str) -> ShardSnapshots:
        """Get a shard's snapshots (backups) as a tree, with any restore in progress.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/snapshots``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardSnapshots`
            The snapshots, their numbers as the library's enums, eg. `SnapshotKind`.

        """
        result: dict[str, Any] = await self._request(method="GET", path=f"/api/shards/{shard_id}/snapshots")
        return ShardSnapshots(data=result)

    async def get_shard_state(self, shard_id: str) -> ShardStatus:
        """Get a shard's live state.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/state``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardStatus`
            The state, its `status` a :class:`ShardState`. A shard that has never reported gets an empty default state,
            not a 404.

        """
        result: dict[str, Any] = await self._request(method="GET", path=f"/api/shards/{shard_id}/state")
        return ShardStatus(data=result)

    async def get_shard_users(self, shard_id: str) -> list[ShardPlayer]:
        """Get the players on a shard.

        |coro|

        Endpoint: ``GET /api/shards/{shard_id}/users``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        list[:class:`ShardPlayer`]
            The players online, the same objects the shard hub's `players` event carries. Empty while stopped, or when
            the template doesn't track players.

        """
        result: list[dict[str, Any]] = await self._request(method="GET", path=f"/api/shards/{shard_id}/users")
        return [ShardPlayer(data=entry) for entry in result]

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
            The file's text to read instead of the file on disk, by default None.

        Returns
        -------
        :class:`ShardConfigImportResponse`
            The settings set from the file, those AMP keeps for itself and those the file lacks.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/config/import", data={"path": path, "content": content})

    # TODO: Trim the move notes once AMP refuses another spire's datastore with its own error (U22b).
    # AMP 3.0.0 and 3.0.1 answer 409 to another spire's datastore.
    async def migrate_shard_to_spire(
        self,
        shard_id: str,
        target_spire_id: str,
        target_datastore_id: str,
        *,
        bring_backups: bool = False,
        stop_if_running: bool = False,
        start_after_move: Optional[bool] = None,
    ) -> None:
        """Move a shard to another spire.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/migration/spire``

        AMP answers at once (202) and a ``"ShardMigration"`` task copies the files; follow it with
        :meth:`get_shard_migration`. The shard's `spireId` and `datastoreId` change straight away.

        .. note::
            The copy on the old spire stays, as an ``"Orphan"`` in :meth:`SpireModule.get_spire_usage`, until
            :meth:`SpireModule.purge_spire_orphan_directory` is called on the **old** spire's datastore with the
            shard's `workingDirName`. :meth:`delete_shard_migration` doesn't remove the old copy.

        The shard's ports become free ports on the target spire. A shard that moves back keeps those new ports. A failed
        move's task stays in :meth:`TaskModule.get_running_tasks` for about 30 minutes, unless the task is dismissed.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        target_spire_id : :class:`str`
            The spire to move the shard to.
        target_datastore_id : :class:`str`
            A datastore on the target spire, see :meth:`SpireModule.get_spire_datastores`.
        bring_backups : :class:`bool`, optional
            If the shard's snapshots move too or not, by default False. Snapshots left behind stay on the old spire and
            can't be restored from the new spire.
        stop_if_running : :class:`bool`, optional
            If AMP may stop a running shard for the move or not, by default False. AMP waits for the stop, the shard's
            grace period and a little more, before it sends the move.
        start_after_move : Union[:class:`bool`, None], optional
            If AMP starts the shard on the target once the move is done or not, by default None for AMP's own default,
            `stop_if_running`. So a running shard the move stopped starts again, and False keeps the shard stopped.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the shard already lives on the target spire. AMP's `message` is an English sentence, and
            there's no `code`.\n
            **400** - If there's no spire with that ID `shards.error.spireNotFound`.\n
            **400** - If the target spire can't take the shard, eg. a Windows spire for a game that needs a Linux
            container `shards.error.needsLinuxSpire`.\n
            **409** - If the shard is running and `stop_if_running` is `False` `shards.error.moveNeedsStop`.\n
            **409** - If the shard didn't stop in time `shards.error.moveStopTimedOut`.\n
            **409** - If the datastore belongs to another spire `spire.error.internal`.

        """
        data: ShardMigrationRequest = {
            "targetSpireId": target_spire_id,
            "targetDatastoreId": target_datastore_id,
            "bringBackups": bring_backups,
            "stopIfRunning": stop_if_running,
        }

        # Left out, AMP starts the shard when `stopIfRunning` is set
        if start_after_move is not None:
            data["startAfterMove"] = start_after_move

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

        Raises
        ------
        AMPAPIRequestError
            **400** - If the trigger is bad, eg. a wrong cron expression, an interval under a minute or an unknown
            event.

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

        Raises
        ------
        AMPAPIRequestError
            **400** - If the shard isn't deleted.

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

    async def restore_shard_snapshot(self, shard_id: str, snapshot_id: str) -> Snapshot:
        """Restore a shard to one of its snapshots. A running shard can be restored too.

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
        :class:`Snapshot`
            The snapshot being restored; follow the restore with :meth:`get_shard_snapshots`.

        Raises
        ------
        AMPAPIRequestError
            **409** - If the shard's spire refuses the restore, from AMP's docs and not seen live.\n
            **503** - If the shard's spire doesn't answer, from AMP's docs and not seen live.

        """
        path: str = f"/api/shards/{shard_id}/snapshots/{snapshot_id}/restore"
        result: dict[str, Any] = await self._request(method="POST", path=path, data={})
        return Snapshot(data=result)

    async def run_shard_schedule(self, shard_id: str, schedule_id: str) -> ScheduleRunResponse:
        """Run one of a shard's schedules now. A disabled one is logged as skipped.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/schedules/{schedule_id}/run``

        The user who sends it becomes the one the schedule's runs act as, this one and those after.

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
            If `command` answers a prompt the game is waiting on rather than being a command or not, by default False.
            - With no prompt waiting, `command` is sent as a command.

        """
        data: ShardConsoleRequest = {"command": command, "promptReply": prompt_reply}
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
            The bytes that follow the ones AMP holds, at most 16 MB; the web panel sends 8 MiB at a time.

        Returns
        -------
        :class:`ShardUploadChunkResponse`
            How many bytes AMP holds now.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the upload is over, eg. already committed `files.error.uploadSessionGone`.\n
            **409** - If the chunk takes the upload past its declared size and the shard past its disk budget
            `files.error.uploadExceedsBudget`, from AMP's docs and not seen live. AMP drops the upload.

        """
        path: str = f"/api/shards/{shard_id}/files/upload-chunk"
        return await self._request(method="POST", path=path, data=chunk, parameters={"session": session_id})

    async def set_shard_credential(self, shard_id: str, credential_id: str) -> ShardCredentialResponse:
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
        :class:`ShardCredentialResponse`
            As :meth:`get_shard_credential` reads it after, with the credential set.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the logged in user can't use that credential `shards.error.credentialUnknown`.

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
            The new name, by default None. AMP refuses an empty name (``"shards.error.displayNameRequired"``).
        description : Union[:class:`str`, None], optional
            The new description, by default None.
        tags : Union[list[:class:`str`], None], optional
            The tags, which replace the shard's old tags, by default None.

        Returns
        -------
        :class:`ShardResponse`
            The shard. Its short `name` doesn't change with the display name.

        """
        data: ShardDetailsRequest = {"displayName": display_name, "description": description, "tags": tags}
        # We only send what changes, AMP keeps a value that's left out.
        return await self._request(method="PATCH", path=f"/api/shards/{shard_id}", data=self._without_none(mapping=data))

    # TODO: Reword the warning and Raises once AMP lets a deny be undone and answers a bad `state` with a 400 (U24a, U24b).
    # AMP 3.0.0 and 3.0.1 answer the undo of a deny with 403 "files.acl.error.notYoursToGrant".
    # AMP 3.0.1 answers a bad `state` with 200 and ignores it, on a path where no deny is in the way.
    async def set_shard_file_acl(self, shard_id: str, path: str, changes: list[FileACLChange]) -> ShardFileACLResponse:
        """Change who may read, write and delete a path inside a shard.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/files/acl``

        .. warning::
            - A user who denies themself a verb can't undo the deny: sending ``"inherit"`` or ``"allow"`` back answers
              403 ``"files.acl.error.notYoursToGrant"``, even for the admin, and the deny stays until the shard is
              deleted. The deny itself takes effect, eg. writing the file then gets 403.
            - AMP answers a `state` other than ``"allow"``, ``"deny"`` or ``"inherit"`` with 200 and ignores the
              change, so the path's rules stay as they were. Check the rules in the reply.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The path.
        changes : list[:class:`FileACLChange`]
            The changes, each a principal, a verb and the state to give it; ``"inherit"`` clears an explicit state.

        Returns
        -------
        :class:`ShardFileACLResponse`
            Who may do what to the path now.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the change needs access the logged in user doesn't hold `files.acl.error.notYoursToGrant`.\n
            **409** - If the change takes away the logged in user's read of the path.

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
            If players can reach the port or not.

        Returns
        -------
        list[:class:`ShardPortResponse`]
            All of the shard's ports.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the port is the port players connect to, which stays public `shards.error.primaryPortIsPublic`.\n
            **400** - If the shard has no port with that `ref` `shards.error.unknownPortRef`.

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
            Each port's `ref` to its new number, eg. ``{"RemoteAdminPort": 25576}``.
            - A port left out stays as it is.
            - The new numbers take effect when the shard next starts.

        Raises
        ------
        AMPAPIRequestError
            **400** - If a port is outside the spire's range.\n
            **400** - If a port clashes with another shard's port on the same spire.

        """
        await self._request(method="PUT", path=f"/api/shards/{shard_id}/ports", data={**ports})

    async def set_shard_schedule_enabled(self, shard_id: str, schedule_id: str, enabled: bool) -> None:
        """Turn one of a shard's schedules on or off.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/schedules/{schedule_id}/enabled``

        The user who sends it becomes the one its runs act as. Turning it on clears the reason AMP turned it off, its
        status's `turnedOff`.

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

    async def set_shard_settings(self, shard_id: str, values: SettingValues) -> None:
        """Change some of a shard's game settings; AMP rewrites the game's config files to match.

        |coro|

        Endpoint: ``PATCH /api/shards/{shard_id}/settings``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        values : :class:`SettingValues`
            Each setting's `fieldName` to its new value, always a string, eg. ``{"motd": "Hello", "MaxMemory": "2048"}``.
            - AMP checks an enum's value, but not a number's.
            - AMP ignores a setting name it doesn't know.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the setting doesn't allow an enum value `shards.error.valueNotAllowed`.\n
            **400** - If `$MaxUsers` is above the shard's `ShardInfraSettings.max_users_cap` `shards.error.maxUsersAboveCap`.

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
        data: SnapshotSettingsRequest = {
            "maxBackupSizeMb": max_backup_size_mb,
            "maxTotalStorageMb": max_total_storage_mb,
            "stopWhenNoQuiesce": stop_when_no_quiesce,
        }

        return await self._request(method="PUT", path=f"/api/shards/{shard_id}/snapshots/settings", data=data)

    # TODO: Reword the docstring once a running shard's state says if the shard can sleep (U18b).
    # AMP 3.0.1 sends the state's `sleep` as `None`, and answers the sleep with 202 for a shard that can't sleep.
    async def sleep_shard(self, shard_id: str) -> None:
        """Put a shard to sleep, so it wakes when a player connects.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/sleep``

        A shard whose template names a sleep port that doesn't exist can't sleep.

        - With sleep mode on, AMP answers 202 for a shard that can't sleep. The shard's console then says the server
          can't be put to sleep.
        - `ShardStatus.sleep` doesn't tell beforehand if the shard can sleep, as AMP 3.0.1 sends `None` for a running
          shard.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Raises
        ------
        AMPAPIRequestError
            **400** - If sleep mode is off `shards.error.sleepDisabled`.\n
            **400** - If the shard can't sleep `shards.error.sleepUnavailable`.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/sleep")

    # TODO: Remove the second sentence once AMP refuses to start a shard that was never updated (U15).
    # AMP 3.0.0 and 3.0.1 answer the start with 202, then the start fails after pulling its container.
    async def start_shard(self, shard_id: str) -> None:
        """Start a shard's game.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/start``

        Follow the start with :meth:`get_shard_state`; AMP answers before the game is up. A shard that was never updated
        starts too, then fails after pulling its container, so run :meth:`update_shard` first.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the shard is suspended `shards.error.suspended`.\n
            **409** - If the game's licence isn't accepted `shards.error.eulaRequired`. See :meth:`accept_shard_eula`.
            The error's `params` holds the game's name as `app`, the licence's `url` and the shard `setting` that keeps
            the acceptance, eg. ``"eula"``.\n
            **409** - If a setting the game needs is empty `shards.error.settingRequiredBeforeStart`.\n
            **409** - If the shard is already running.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/start")

    async def start_shard_file_upload(self, shard_id: str, path: str, size: int) -> ShardUploadSessionResponse:
        """Start a chunked upload, for a file too big for :meth:`upload_shard_files`.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/files/upload-start``

        Send the bytes with :meth:`send_shard_file_chunk`, then :meth:`commit_shard_file_upload`;
        :meth:`upload_shard_file` does all three.

        A start for a path that has an unfinished upload hands back that upload's session and `received`, whatever
        `size` says.

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

        Raises
        ------
        AMPAPIRequestError
            **409** - If `path` is inside an archive, from AMP's docs and not seen live.\n
            **409** - If `path` is a file AMP writes itself, from AMP's docs and not seen live.\n
            **409** - If `size` would take the shard past its disk budget `files.error.uploadExceedsBudget`. This is from
            AMP's docs and not seen live.\n
            **409** - If no scan has measured the shard yet and `size` alone is over the disk budget
            `files.error.uploadExceedsBudgetUnmeasured`, from AMP's docs and not seen live.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/files/upload-start", data={"path": path, "size": size})

    # TODO: Reword Raises once AMP refuses a bad target datastore with its own error (U22b).
    # AMP 3.0.0 and 3.0.1 answer 409 "spire.error.internal" to the shard's own datastore or an unknown one.
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
            **409** - If `target_datastore_id` is the shard's own datastore `spire.error.internal`.\n
            **409** - If no datastore has the ID `target_datastore_id` `spire.error.internal`.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/migration", data={"targetDatastoreId": target_datastore_id})

    async def stop_shard(self, shard_id: str) -> None:
        """Stop a shard's game cleanly, or kill it once it outlasts its grace period.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/stop``

        Follow it with :meth:`get_shard_state`; AMP answers before the game has stopped. A game still running after its
        template's `TemplateLifecycle.exitTimeout` is killed (``"shards.msg.stopGraceExpired"``). On a shard that is
        updating, it aborts the update (``"Update aborted"``); it is the only call that does, as
        :meth:`TaskModule.cancel_task` doesn't.

        AMP 3.0.0 and 3.0.1 have no call that kills a game at once. A schedule step of the task ``"power.kill"`` does,
        run with :meth:`run_shard_schedule` (``"shards.msg.forciblyKilled"``).

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

        A running shard is stopped. A suspended one also refuses a restart, a wake and an update.

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
        name: Optional[str],
        kind: SnapshotKind,
        content: SnapshotContent,
        *,
        description: Optional[str] = None,
        sticky: bool = False,
    ) -> Snapshot:
        """Take a snapshot (a backup) of a shard.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/snapshots``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        name : Union[:class:`str`, None]
            The snapshot's name, or None for AMP's, eg. ``"Manual Backup - admin"``.
        kind : :class:`SnapshotKind`
            A full snapshot, or a partial one that builds on the newest.
        content : :class:`SnapshotContent`
            What it holds, eg. ``SnapshotContent.game_state | SnapshotContent.amp_config``. AMP refuses none.
        description : Union[:class:`str`, None], optional
            A description, by default None. AMP writes one when it's None or empty.
        sticky : :class:`bool`, optional
            If it's kept out of AMP's automatic clean-up or not, by default False. It doesn't stop a delete.

        Returns
        -------
        :class:`Snapshot`
            The snapshot, still running; follow it with :meth:`get_shard_snapshots`.

        Raises
        ------
        AMPAPIRequestError
            **409** - If the shard's spire refuses the snapshot, from AMP's docs and not seen live.\n
            **503** - If the shard's spire doesn't answer, from AMP's docs and not seen live.

        """
        data: SnapshotRequest = {"kind": kind, "content": content, "name": name, "description": description, "sticky": sticky}
        result: dict[str, Any] = await self._request(method="POST", path=f"/api/shards/{shard_id}/snapshots", data=data)
        return Snapshot(data=result)

    async def unsuspend_shard(self, shard_id: str) -> ShardResponse:
        """Let a suspended shard start again. It doesn't start it.

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

        A running shard is stopped for the update and left stopped. :meth:`stop_shard` aborts an update.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Returns
        -------
        :class:`ShardUpdateResponse`
            The update's task ID; follow the task with :meth:`TaskModule.get_running_tasks`, or with
            :meth:`TaskModule.get_task` for each step.

        Raises
        ------
        AMPAPIRequestError
            **409** - If an update is already running.\n
            **409** - If the download needs a Steam login the shard doesn't have `shards.error.steamLoginRequired`.
            See :meth:`set_shard_credential`. The code is from the web panel's source, not seen live.

        """
        return await self._request(method="POST", path=f"/api/shards/{shard_id}/update")

    async def update_shard_infra(
        self,
        shard_id: str,
        settings: Optional[ShardInfraSettings] = None,
        **changes: Unpack[ShardInfraChanges],
    ) -> ShardInfraSaveResult:
        """Change any available settings for how a shard runs, keeping the rest.

        |coro|

        Endpoint: ``PATCH /api/shards/{shard_id}/infra``

        - A setting left out stays as it is.
        - Most changes take effect when the shard next starts.
        - A lower `max_users_cap` lowers the shard's `$MaxUsers` setting at once.

        :meth:`get_shard_infra` reads the settings, and :class:`ShardInfraSettings` describes each setting further.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        settings : Union[:class:`ShardInfraSettings`, None], optional
            The shard's settings to send whole, eg. :meth:`get_shard_infra`'s `ShardInfra.settings` with an attribute
            changed, by default None.
            - Each setting is sent from the object's attributes, so an attribute changed on the object is sent too.
            - A keyword argument wins over the object's value for the same setting.
            - The object overwrites any change made to the shard's settings since the object was read.
            - A :class:`ShardInfraSaveResult` works too.
        start_on_boot : :class:`bool`, optional
            If the shard starts when its spire's machine starts or not.
        auto_restart_on_crash : :class:`bool`, optional
            If AMP restarts the game when it exits without a stop being asked for or not.
            - Only a game that was ready and ran for at least 5 minutes is restarted.
        startup_order : :class:`int`, optional
            The order the shard starts in when its spire's machine starts, lowest first.
            - AMP gives a new shard 100.
        sleep_mode : :class:`bool`, optional
            If the shard sleeps while no player is connected or not.
            - It does nothing unless the template can sleep, see `ShardInfra.supports_sleep`.
        advertised_address : :class:`str`, optional
            The address players are given for the shard, eg. ``"play.example.com"``.
            - ``""`` lets AMP work out the address itself.
        advertised_address_includes_port : :class:`bool`, optional
            If AMP adds the shard's port to the advertised address or not.
        container_mode : :class:`ShardContainerMode`, optional
            How the shard runs, straight on its spire or in a container.
            - `ShardContainerMode` says what each mode does.
        container_image_override : :class:`str`, optional
            The container image to run instead of the template's.
            - ``""`` goes back to the template's image.
            - An image from AMP's own repository that AMP doesn't build is stored, but the shard fails at its next start.
        memory_limit_mb : :class:`int`, optional
            The shard's memory limit in MiB, 0 for no limit.
            - A native shard takes the limit too.
            - AMP stores a negative number without complaint.
        memory_reservation_mb : :class:`int`, optional
            The container's soft memory limit in MiB, 0 for none.
            - It can't be above the shard's memory limit.
        memory_swap_mb : :class:`int`, optional
            The container's memory and swap together in MiB.
            - -1 for no limit.
            - 0 for the container runtime's default, about twice the memory limit.
            - Any other number can't be below the shard's memory limit.
        cpu_limit : :class:`float`, optional
            The shard's CPU limit in cores, eg. 1.5, 0 for no limit.
            - A native shard takes the limit too.
        max_users_cap : :class:`int`, optional
            The most players AMP lets in at once, whatever the shard's `$MaxUsers` setting says, 0 for no cap.
            - A lower cap lowers `$MaxUsers` at once, see `ShardInfraSaveResult.clamp_refused`.
            - A running game's config file keeps the old number.
        enable_analytics : :class:`bool`, optional
            If AMP collects analytics on the players who join or not.
        user_specific_data : :class:`bool`, optional
            If analytics keeps data on each player or not, eg. who plays the most.
            - The players have to be told that analytics is in use.
        minimum_session_time_for_retention : :class:`int`, optional
            The shortest session in seconds that analytics keeps.
        enable_geo_filtering : :class:`bool`, optional
            If AMP blocks players from certain countries or not.
        blocked_countries : list[:class:`str`], optional
            The countries to block, as ISO 3166-1 alpha-2 codes, eg. ``["US"]``.
            - The list replaces the stored list.
        allowed_countries : list[:class:`str`], optional
            The countries to allow, as ISO 3166-1 alpha-2 codes.
            - The list replaces the stored list.
            - An empty list allows every country that isn't blocked.
        block_unknown_countries : :class:`bool`, optional
            If AMP also blocks players whose country can't be worked out or not.
        geo_filter_kick_message : :class:`str`, optional
            The message a player blocked by geo filtering gets.
            - ``{CountryCode}`` and ``{CountryName}`` are replaced with the player's country.
        geo_filter_kick_command : :class:`str`, optional
            The console command that disconnects a player blocked by geo filtering.
            - ``{UserName}``, ``{UserID}``, ``{Reason}``, ``{CountryCode}`` and ``{CountryName}`` are replaced.
        disk_limit_mb : :class:`int`, optional
            The disk limit in MB for the shard's folder, 0 for no limit.
            - AMP checks the limit at the spire's disk scans.
            - AMP stops the shard at the first disk scan that finds it over the limit.
        import_config_files_from_sftp : :class:`bool`, optional
            If AMP reads a config file it manages back into the shard's settings when the file is written over SFTP or
            not.
        extra_environment : dict[:class:`str`, :class:`str`], optional
            Extra environment variables for the game's process or container, by name.
            - The dict replaces the stored variables, and ``{}`` removes them all.

        Returns
        -------
        :class:`ShardInfraSaveResult`
            The settings as AMP saved them.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `container_mode` isn't a mode AMP knows.\n
            **400** - If the memory reservation is above the shard's memory limit
            `shards.error.memoryReservationExceedsLimit`.\n
            **400** - If the memory and swap limit is below the shard's memory limit `shards.error.memorySwapLessThanLimit`.
        TypeError
            If a keyword argument isn't a setting. Nothing is sent.
        ValueError
            If neither `settings` nor a setting is given. Nothing is sent.

        """
        # The same refusal Python gives a keyword argument the signature doesn't have, before anything is sent
        for name in changes:
            if name not in ShardInfraChanges.__optional_keys__:
                msg = f"ShardModule.update_shard_infra() got an unexpected keyword argument '{name}'"
                raise TypeError(msg)

        values: dict[str, Any] = {}
        if settings is not None:
            # We send every setting from the object's attributes, as they may have been changed since the read.
            # AMP's own `shard_id`, `tenant_id`, `updated_*` and a save's `clamp_refused` aren't settings, so they stay out.
            values = {name: getattr(settings, name) for name in ShardInfraChanges.__optional_keys__ if hasattr(settings, name)}
            # The object's `None` means the template's image, and AMP reads `None` as "keep", so we send `""`
            if "container_image_override" in values and values["container_image_override"] is None:
                values["container_image_override"] = ""

        values.update(changes)
        # A `None` is left out, so AMP keeps that setting
        body: dict[str, Any] = {
            self._key_name(name=name): value.value if isinstance(value, Enum) else value
            for name, value in self._without_none(mapping=values).items()
        }
        if not body:
            msg = "At least one infra setting must be given."
            raise ValueError(msg)
        result: dict[str, Any] = await self._request(method="PATCH", path=f"/api/shards/{shard_id}/infra", data=body)
        return ShardInfraSaveResult(data=result)

    async def update_shard_schedule(
        self,
        shard_id: str,
        schedule_id: str,
        name: Optional[str] = None,
        trigger: Optional[ScheduleTrigger] = None,
        steps: Optional[list[ScheduleStep]] = None,
        *,
        description: Optional[str] = None,
        run_timeout: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> ShardScheduleResponse:
        """Change one of a shard's schedules. Anything left as `None` stays as it is.

        |coro|

        Endpoints: ``GET /api/shards/{shard_id}/schedules/{schedule_id}`` for the schedule as it is, then
        ``PUT /api/shards/{shard_id}/schedules/{schedule_id}``

        AMP replaces the whole schedule on a PUT, eg. a `timeout` left out goes back to 30 minutes, so we read the
        schedule first and send the rest of it back as it was. Two calls at once on one schedule can still undo each
        other. The user who changes it becomes the one its runs act as, and AMP clears a refusal it recorded (and,
        saved enabled, the reason it turned the schedule off).

        A webhook step's `url` or `body` sent back as ``"[withheld]"`` keeps what AMP holds, so a user who can't read
        them can still save the schedule.

        An ``"interval"`` schedule this update enables runs once within seconds, for the time slot just past, the same
        way a new enabled schedule does (see :meth:`create_shard_schedule`).

        .. note::
            AMP ignores a schedule's `retryPolicy` and `misfirePolicy` here, so they keep what AMP gave them.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        schedule_id : :class:`str`
            The schedule's ID.
        name : Union[:class:`str`, None], optional
            The schedule's name, by default None.
        trigger : Union[:class:`ScheduleTrigger`, None], optional
            When it runs, by default None.
        steps : Union[list[:class:`ScheduleStep`], None], optional
            What it does, in order, by default None.
        description : Union[:class:`str`, None], optional
            A description, by default None.
        run_timeout : Union[:class:`str`, None], optional
            How long a run may take, as a time span, by default None. AMP calls it `timeout`, and keeps it between 1
            minute and 2 hours.
        enabled : Union[:class:`bool`, None], optional
            If it runs on its trigger or not, by default None.

        Returns
        -------
        :class:`ShardScheduleResponse`
            The schedule.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the shard has no schedule with that ID. The PUT is never sent.

        """
        schedule: ShardScheduleResponse = await self.get_shard_schedule(shard_id=shard_id, schedule_id=schedule_id)
        current: ScheduleDefinition = schedule["definition"]
        data: ShardScheduleRequest = {
            "name": name if name is not None else current["name"],
            "description": description if description is not None else current["description"],
            "trigger": trigger if trigger is not None else current["trigger"],
            "steps": steps if steps is not None else current["steps"],
            "timeout": run_timeout if run_timeout is not None else current["timeout"],
            "enabled": enabled if enabled is not None else current["enabled"],
        }

        return await self._request(method="PUT", path=f"/api/shards/{shard_id}/schedules/{schedule_id}", data=data)

    async def update_shard_snapshot(self, shard_id: str, snapshot_id: str, name: str, description: str, sticky: bool) -> None:
        """Change a snapshot's name, description and stickiness.

        |coro|

        Endpoint: ``PUT /api/shards/{shard_id}/snapshots/{snapshot_id}/meta``

        AMP replaces all three, so pass the ones to keep as they are, eg. from :meth:`get_shard_snapshots`; ``""``
        clears the name or description.

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
            **400** - If there's no snapshot with that ID `snapshots.error.notFound`.

        """
        data: SnapshotMetaRequest = {"name": name, "description": description, "sticky": sticky}
        await self._request(method="PUT", path=f"/api/shards/{shard_id}/snapshots/{snapshot_id}/meta", data=data)

    # TODO: Drop the warning once AMP keeps the old file until the commit (U30a).
    # AMP 3.0.0 and 3.0.1 on a remote spire resize the file at `upload-start`.
    # A failed upload then leaves the file padded with zeros.
    async def upload_shard_file(
        self,
        shard_id: str,
        path: str,
        content: bytes,
        *,
        chunk_size: int = UPLOAD_CHUNK_SIZE,
        resume: bool = False,
    ) -> None:
        """Upload one file to a shard in chunks, as the web panel does for a big file.

        |coro|

        Endpoints: ``POST /api/shards/{shard_id}/files/upload-start``, ``.../upload-chunk`` and ``.../upload-commit``

        A start for a path with an unfinished upload hands back that upload, whatever size the start asks for, and AMP
        keeps the upload for 24 hours. No call cancels it. Finishing the upload with another file's bytes splices the
        held upload and the new file into one, so we refuse to carry on an upload AMP already holds part of unless
        `resume` is True.

        .. warning::
            On a shard on a remote spire (`via` ``"agent"``), AMP resizes the file at `path` as the upload starts, so a
            failed upload leaves the file it was replacing padded with zero bytes. Upload under a new name when the old
            file matters.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        path : :class:`str`
            The file's path, its name included.
        content : :class:`bytes`
            The file.
        chunk_size : :class:`int`, optional
            How many bytes to send at a time, by default 8 MiB like the web panel. AMP takes at most 16 MB in one chunk.
        resume : :class:`bool`, optional
            If we carry on an upload to `path` that AMP already holds part of, by default False.
            - Only pass True when the upload is this same file, eg. after this call failed partway.

        Raises
        ------
        ValueError
            If `chunk_size` is less than 1. Nothing is sent.
        AMPAPIUploadError
            If AMP already holds part of an upload to `path` and `resume` is False, or holds more bytes than `content`
            has whatever `resume` says. No chunk is sent then. It is also raised when AMP stops taking the chunks,
            rather than sending the same one forever.
        AMPAPIRequestError
            If AMP refuses a chunk or the commit. A note on it names the upload's session ID and the bytes AMP holds,
            and `resume=True` carries on from there.

        """
        if chunk_size < 1:
            msg = f"The chunk size has to be at least 1 byte, not {chunk_size}. | Path: {path}"
            raise ValueError(msg)

        upload: ShardUploadSessionResponse = await self.start_shard_file_upload(shard_id=shard_id, path=path, size=len(content))
        session_id: str = upload["sessionId"]
        received: int = upload["received"]
        # AMP hands back any unfinished upload to this path, so the bytes it holds may be another file's
        if received > len(content):
            raise AMPAPIUploadError(
                path=path,
                session_id=session_id,
                received=received,
                size=len(content),
                reason="AMP holds more of an earlier upload to this path than the file has.",
            )
        if received > 0 and resume is False:
            raise AMPAPIUploadError(
                path=path,
                session_id=session_id,
                received=received,
                size=len(content),
                reason="AMP already holds part of an earlier upload to this path. Pass resume=True only when it is this same file.",
            )

        try:
            while received < len(content):
                reply: ShardUploadChunkResponse = await self.send_shard_file_chunk(
                    shard_id=shard_id,
                    session_id=session_id,
                    chunk=content[received : received + chunk_size],
                )
                if reply["received"] <= received:
                    raise AMPAPIUploadError(
                        path=path,
                        session_id=session_id,
                        received=received,
                        size=len(content),
                        reason="AMP stopped taking the upload.",
                    )
                received = reply["received"]

            await self.commit_shard_file_upload(shard_id=shard_id, session_id=session_id)
        except AMPAPIRequestError as error:
            note: str = (
                f"AMP holds {received} of {len(content)} bytes of the upload to {path}. Pass resume=True to carry on from there."
                f" | Session ID: {session_id}"
            )
            error.add_note(note)
            raise

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

        Raises
        ------
        AMPAPIRequestError
            **409** - If a file's path is a file AMP writes itself, from AMP's docs and not seen live.\n
            **409** - If the files together would take the shard past its disk budget `files.error.uploadExceedsBudget`,
            from AMP's docs and not seen live. Nothing is written.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/files/upload", files=files, parameters={"path": folder})

    # TODO: Check the reply against a live capture; AMP's OpenAPI alone says the 202 has no body (#3-47.7, #3-56.1w).
    # Only the 400 for a shard that isn't asleep is known. Only `minecraft-java` claims sleep, and AMP refused to put
    # it to sleep on the test VMs: it took longer to start than AMP's 25 second limit (#3-54), then U18b.
    async def wake_shard(self, shard_id: str) -> None:
        """Wake a sleeping shard, before a player's connection would.

        |coro|

        Endpoint: ``POST /api/shards/{shard_id}/wake``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the shard isn't asleep `shards.error.notAsleep`.\n
            **400** - If the shard is suspended.

        """
        await self._request(method="POST", path=f"/api/shards/{shard_id}/wake")
