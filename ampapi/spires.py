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

from .base import Base

if TYPE_CHECKING:
    from ._types import (
        DatastoreRequest,
        DatastoreResponse,
        PortClaimResponse,
        SettingsManifestResponse,
        SettingValues,
        SpireEnrollmentCreatedResponse,
        SpireEnrollmentHostResponse,
        SpireEnrollmentRequest,
        SpireEnrollmentResponse,
        SpireEnrollmentRevokeRequest,
        SpireExpiredPurgeResponse,
        SpireImportItem,
        SpireImportRequest,
        SpireImportScanRequest,
        SpireImportScanResponse,
        SpireIPOptionResponse,
        SpirePortResponse,
        SpireResponse,
        SpireRosterResponse,
        SpireStartupEntry,
        SpireStartupResponse,
        SpireStateResponse,
        SpireStorageResponse,
        SpireUsageIntervalResponse,
        SpireUsageResponse,
    )

__all__ = (
    "Spire",
    "SpireModule",
)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Spire:
    """A spire, AMP 3's name for an ADS or Target, with the calls that act on it.

    :meth:`SpireModule.get_spires` and :meth:`SpireModule.get_spire` make these. Each method calls the
    :class:`SpireModule` one with this spire's ID, eg. :meth:`get_state` is :meth:`SpireModule.get_spire_state`.

    A spire that joined serves the whole panel API too, so a :class:`Panel` can talk to any of them. The data's
    `isLocal` is relative to the machine that answered, not a property of the spire.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    module : :class:`SpireModule`
        The module (usually the :class:`Panel`) the calls go through.
    data : :class:`SpireResponse`
        The spire as AMP sent it.

    Attributes
    ----------
    id : :class:`str`
        The spire's ID.
    display_name : :class:`str`
        The spire's name.
    data : :class:`SpireResponse`
        The spire as AMP sent it, when this object was made.

    """

    data: SpireResponse
    display_name: str
    id: str
    _module: SpireModule

    def __init__(self, module: SpireModule, data: SpireResponse) -> None:  # noqa: D107
        self._module = module
        self.data = data
        self.id = data["id"]
        self.display_name = data["displayName"]

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # It comes from `SpireModule.apply_spire_update`.
    async def apply_update(self) -> Any:
        """Update this spire's AMP, see :meth:`SpireModule.apply_spire_update`.

        |coro|

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._module.apply_spire_update(spire_id=self.id)

    async def create_datastore(self, name: str, path: str, *, is_default: bool = False, enabled: bool = True) -> list[DatastoreResponse]:
        """Add a datastore to this spire, see :meth:`SpireModule.create_spire_datastore`.

        |coro|

        Parameters
        ----------
        name : :class:`str`
            The datastore's name.
        path : :class:`str`
            The folder on the spire, eg. ``"/opt/cubecoders/amp3/data/my_store"``.
        is_default : :class:`bool`, optional
            If new shards go here or not, by default False.
        enabled : :class:`bool`, optional
            If the datastore can be used or not, by default True.

        Returns
        -------
        list[:class:`DatastoreResponse`]
            Every datastore on the spire.

        """
        return await self._module.create_spire_datastore(
            spire_id=self.id,
            name=name,
            path=path,
            is_default=is_default,
            enabled=enabled,
        )

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # It comes from `SpireModule.delete_spire`.
    async def delete(self, *, force: bool = False) -> Any:
        """Remove this spire from the panel, see :meth:`SpireModule.delete_spire`.

        |coro|

        Parameters
        ----------
        force : :class:`bool`, optional
            If AMP should remove it even when it would rather not or not, by default False.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._module.delete_spire(spire_id=self.id, force=force)

    async def delete_datastore(self, datastore_id: str) -> list[DatastoreResponse]:
        """Remove a datastore from this spire, see :meth:`SpireModule.delete_spire_datastore`.

        |coro|

        Parameters
        ----------
        datastore_id : :class:`str`
            The datastore's ID.

        Returns
        -------
        list[:class:`DatastoreResponse`]
            Every datastore left on the spire.

        """
        return await self._module.delete_spire_datastore(spire_id=self.id, datastore_id=datastore_id)

    async def get_datastores(self) -> list[DatastoreResponse]:
        """Get this spire's datastores, see :meth:`SpireModule.get_spire_datastores`.

        |coro|

        Returns
        -------
        list[:class:`DatastoreResponse`]
            The datastores.

        """
        return await self._module.get_spire_datastores(spire_id=self.id)

    async def get_ip_options(self, *, include_auto: bool = False) -> list[SpireIPOptionResponse]:
        """Get the addresses a shard on this spire can bind to, see :meth:`SpireModule.get_spire_ip_options`.

        |coro|

        Parameters
        ----------
        include_auto : :class:`bool`, optional
            If the list should start with AMP's ``"@auto-pool"`` choice or not, by default False.

        Returns
        -------
        list[:class:`SpireIPOptionResponse`]
            The addresses.

        """
        return await self._module.get_spire_ip_options(spire_id=self.id, include_auto=include_auto)

    async def get_port_claims(self) -> list[PortClaimResponse]:
        """Get the ports held on this spire, see :meth:`SpireModule.get_spire_port_claims`.

        |coro|

        Returns
        -------
        list[:class:`PortClaimResponse`]
            The ports and what holds each one.

        """
        return await self._module.get_spire_port_claims(spire_id=self.id)

    async def get_ports(self) -> list[SpirePortResponse]:
        """Get the ports this spire's shards use, see :meth:`SpireModule.get_spire_ports`.

        |coro|

        Returns
        -------
        list[:class:`SpirePortResponse`]
            The ports.

        """
        return await self._module.get_spire_ports(spire_id=self.id)

    async def get_settings_manifest(self) -> SettingsManifestResponse:
        """Get this spire's settings with their current values, see :meth:`SpireModule.get_spire_settings_manifest`.

        |coro|

        Returns
        -------
        :class:`SettingsManifestResponse`
            The settings and their values.

        """
        return await self._module.get_spire_settings_manifest(spire_id=self.id)

    async def get_startup(self) -> list[SpireStartupResponse]:
        """Get this spire's shard start order, see :meth:`SpireModule.get_spire_startup`.

        |coro|

        Returns
        -------
        list[:class:`SpireStartupResponse`]
            The shards, in their start order.

        """
        return await self._module.get_spire_startup(spire_id=self.id)

    async def get_state(self) -> SpireStateResponse:
        """Get this spire's live load, see :meth:`SpireModule.get_spire_state`.

        |coro|

        Returns
        -------
        :class:`SpireStateResponse`
            The spire's load, memory, network and machine details.

        """
        return await self._module.get_spire_state(spire_id=self.id)

    async def get_usage(self) -> Optional[SpireUsageResponse]:
        """Get this spire's disk use from its last scan, see :meth:`SpireModule.get_spire_usage`.

        |coro|

        Returns
        -------
        Union[:class:`SpireUsageResponse`, None]
            The disk use per datastore, `None` before the first scan.

        """
        return await self._module.get_spire_usage(spire_id=self.id)

    async def get_usage_interval(self) -> SpireUsageIntervalResponse:
        """Get how often this spire measures its disk use, see :meth:`SpireModule.get_spire_usage_interval`.

        |coro|

        Returns
        -------
        :class:`SpireUsageIntervalResponse`
            The interval in minutes.

        """
        return await self._module.get_spire_usage_interval(spire_id=self.id)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # It comes from `SpireModule.import_spire_servers`.
    async def import_servers(self, items: list[SpireImportItem], *, enter_other_volumes: bool = False) -> Any:
        """Import game servers found by :meth:`scan_imports`, see :meth:`SpireModule.import_spire_servers`.

        |coro|

        Parameters
        ----------
        items : list[:class:`SpireImportItem`]
            The servers to import.
        enter_other_volumes : :class:`bool`, optional
            If AMP may go into other volumes for them or not, by default False.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._module.import_spire_servers(spire_id=self.id, items=items, enter_other_volumes=enter_other_volumes)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # It comes from `SpireModule.preflight_spire_import`.
    async def preflight_import(self, items: list[SpireImportItem]) -> Any:
        """Check game servers can be imported, see :meth:`SpireModule.preflight_spire_import`.

        |coro|

        Parameters
        ----------
        items : list[:class:`SpireImportItem`]
            The servers to check.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._module.preflight_spire_import(spire_id=self.id, items=items)

    async def purge_expired_shards(self) -> SpireExpiredPurgeResponse:
        """Remove for good this spire's deleted shards that are past keeping, see :meth:`SpireModule.purge_spire_expired_shards`.

        |coro|

        Returns
        -------
        :class:`SpireExpiredPurgeResponse`
            How many shards AMP is purging.

        """
        return await self._module.purge_spire_expired_shards(spire_id=self.id)

    async def purge_orphan_directories(self, datastore_id: str) -> SpireUsageResponse:
        """Delete every orphan folder in a datastore, see :meth:`SpireModule.purge_spire_orphan_directories`.

        |coro|

        Parameters
        ----------
        datastore_id : :class:`str`
            The datastore's ID.

        Returns
        -------
        :class:`SpireUsageResponse`
            This spire's disk use after.

        """
        return await self._module.purge_spire_orphan_directories(spire_id=self.id, datastore_id=datastore_id)

    async def purge_orphan_directory(self, datastore_id: str, name: str) -> SpireUsageResponse:
        """Delete one orphan folder in a datastore, see :meth:`SpireModule.purge_spire_orphan_directory`.

        |coro|

        Parameters
        ----------
        datastore_id : :class:`str`
            The datastore's ID.
        name : :class:`str`
            The folder's name.

        Returns
        -------
        :class:`SpireUsageResponse`
            This spire's disk use after.

        """
        return await self._module.purge_spire_orphan_directory(spire_id=self.id, datastore_id=datastore_id, name=name)

    async def rescan_usage(self) -> Optional[SpireUsageResponse]:
        """Measure this spire's disk use now, see :meth:`SpireModule.rescan_spire_usage`.

        |coro|

        Returns
        -------
        Union[:class:`SpireUsageResponse`, None]
            The disk use per datastore.

        """
        return await self._module.rescan_spire_usage(spire_id=self.id)

    async def scan_imports(self, roots: list[str], *, automatic: bool = False) -> SpireImportScanResponse:
        """Look for game servers from other panels on this spire, see :meth:`SpireModule.scan_spire_imports`.

        |coro|

        Parameters
        ----------
        roots : list[:class:`str`]
            The folders to look in.
        automatic : :class:`bool`, optional
            If AMP should pick the folders itself or not, by default False.

        Returns
        -------
        :class:`SpireImportScanResponse`
            What AMP found.

        """
        return await self._module.scan_spire_imports(spire_id=self.id, roots=roots, automatic=automatic)

    async def set_settings(self, values: SettingValues) -> None:
        """Change some of this spire's settings, see :meth:`SpireModule.set_spire_settings`.

        |coro|

        Parameters
        ----------
        values : :class:`SettingValues`
            Each setting's `fieldName` to its new value, eg. ``{"spire.sftpEnabled": "false"}``.

        """
        await self._module.set_spire_settings(spire_id=self.id, values=values)

    async def set_startup(self, entries: list[SpireStartupEntry]) -> list[SpireStartupResponse]:
        """Set this spire's shard start order, see :meth:`SpireModule.set_spire_startup`.

        |coro|

        Parameters
        ----------
        entries : list[:class:`SpireStartupEntry`]
            The shards in the order they start.

        Returns
        -------
        list[:class:`SpireStartupResponse`]
            The start order AMP saved.

        """
        return await self._module.set_spire_startup(spire_id=self.id, entries=entries)

    async def set_usage_interval(self, minutes: int) -> SpireStorageResponse:
        """Set how often this spire measures its disk use, see :meth:`SpireModule.set_spire_usage_interval`.

        |coro|

        Parameters
        ----------
        minutes : :class:`int`
            The interval in minutes.

        Returns
        -------
        :class:`SpireStorageResponse`
            The spire's storage settings.

        """
        return await self._module.set_spire_usage_interval(spire_id=self.id, minutes=minutes)


class SpireModule(Base):
    """The calls for spires, AMP 3's name for an ADS or Target: datastores, ports, start order, disk use and joining.

    .. versionadded:: 6.0.0

    """

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # The body comes from the web panel's code; no capture shows the response yet.
    async def apply_spire_update(self, spire_id: str) -> Any:
        """Update a spire's AMP to the panel's version.

        |coro|

        Endpoint: ``POST /api/updates/spires/{spire_id}``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path=f"/api/updates/spires/{spire_id}", data={})

    async def approve_spire_enrollment(self, enrollment_id: str) -> SpireEnrollmentResponse:
        """Let a machine that used a join file become a spire.

        |coro|

        Endpoint: ``POST /api/spires/enrollments/{enrollment_id}/approve``

        Check the enrolment's `admission` first: its `fingerprint` should match the one the joining machine shows in
        its `HealthStatusResponse.messageParams`. The machine then joins within seconds, and the enrolment's `status`
        goes from ``"approved"`` to ``"redeemed"``.

        Parameters
        ----------
        enrollment_id : :class:`str`
            The enrolment's ID, once its `status` is ``"awaitingapproval"``.

        Returns
        -------
        :class:`SpireEnrollmentResponse`
            The enrolment, with `status` ``"approved"``.

        Raises
        ------
        AMPAPIRequestError
            If no machine is waiting on the enrolment (409, ``"spire.enroll.error.nothingToApprove"``).

        """
        return await self._request(method="POST", path=f"/api/spires/enrollments/{enrollment_id}/approve")

    async def create_spire_datastore(
        self,
        spire_id: str,
        name: str,
        path: str,
        *,
        is_default: bool = False,
        enabled: bool = True,
    ) -> list[DatastoreResponse]:
        """Add a datastore, a folder shards are kept in, to a spire.

        |coro|

        Endpoint: ``POST /api/spires/{spire_id}/datastores``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        name : :class:`str`
            The datastore's name.
        path : :class:`str`
            The folder on the spire, eg. ``"/opt/cubecoders/amp3/data/my_store"``. AMP doesn't check it exists.
        is_default : :class:`bool`, optional
            If new shards go here or not, by default False.
        enabled : :class:`bool`, optional
            If the datastore can be used or not, by default True.

        Returns
        -------
        list[:class:`DatastoreResponse`]
            Every datastore on the spire.

        """
        data: DatastoreRequest = {"name": name, "path": path, "isDefault": is_default, "enabled": enabled}
        return await self._request(method="POST", path=f"/api/spires/{spire_id}/datastores", data=data)

    async def create_spire_enrollment(
        self,
        label: str,
        *,
        expires_in_hours: Optional[int] = None,
        hosts: Optional[list[str]] = None,
    ) -> SpireEnrollmentCreatedResponse:
        """Make a join file, so another machine can join the panel as a spire.

        |coro|

        Endpoint: ``POST /api/spires/enrollments``

        .. warning::
            AMP refuses it with ``"spire.enroll.error.busNotPublic"`` until the message bus is opened to other machines
            (:meth:`PlatformModule.expand_message_bus`).

        The new machine's first-run setup takes the `joinBlob`, then waits in :meth:`PlatformModule.get_health_status`
        until :meth:`approve_spire_enrollment`.

        Parameters
        ----------
        label : :class:`str`
            A name for the enrolment; the spire it becomes takes it as its `displayName`.
        expires_in_hours : Union[:class:`int`, None], optional
            How long the join file works for, by default None.
        hosts : Union[list[:class:`str`], None], optional
            The addresses the new machine should reach the panel on, by default None.
            See :meth:`get_spire_enrollment_hosts`.

        Returns
        -------
        :class:`SpireEnrollmentCreatedResponse`
            The enrolment (201), with `status` ``"pending"``, and the join file, which AMP sends only here.

        """
        data: SpireEnrollmentRequest = {"label": label, "hosts": hosts if hosts is not None else []}
        if expires_in_hours is not None:
            data["expiresInHours"] = expires_in_hours

        return await self._request(method="POST", path="/api/spires/enrollments", data=data)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # The path comes from the web panel's code; no capture shows the response yet.
    async def delete_spire(self, spire_id: str, *, force: bool = False) -> Any:
        """Remove a spire from the panel.

        |coro|

        Endpoint: ``DELETE /api/spires/{spire_id}``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        force : :class:`bool`, optional
            If AMP should remove it even when it would rather not or not, by default False.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        parameters: Optional[dict[str, str]] = {"force": "true"} if force is True else None
        return await self._request(method="DELETE", path=f"/api/spires/{spire_id}", parameters=parameters)

    # TODO: Reword the warning once AMP refuses a datastore that still holds an orphan folder (U23).
    # AMP 3.0.0.6 accepts it, and the folder drops out of the API's sight.
    async def delete_spire_datastore(self, spire_id: str, datastore_id: str) -> list[DatastoreResponse]:
        """Remove a datastore from a spire.

        |coro|

        Endpoint: ``DELETE /api/spires/{spire_id}/datastores/{datastore_id}``

        .. warning::
            AMP accepts it while the datastore still holds an orphan folder. The folder stays on disk, and with
            the datastore gone the API can't reach it to purge it; adding a datastore at the same path again lists it
            once more. Purge the orphans first, see :meth:`purge_spire_orphan_directory`.

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        datastore_id : :class:`str`
            The datastore's ID.

        Returns
        -------
        list[:class:`DatastoreResponse`]
            Every datastore left on the spire.

        """
        return await self._request(method="DELETE", path=f"/api/spires/{spire_id}/datastores/{datastore_id}")

    async def delete_spire_enrollment(self, enrollment_id: str, *, reason: Optional[str] = None) -> None:
        """Revoke a join file.

        |coro|

        Endpoint: ``DELETE /api/spires/enrollments/{enrollment_id}``

        The enrolment stays in :meth:`get_spire_enrollments` with `status` ``"revoked"``. Revoking it again is fine too.

        Parameters
        ----------
        enrollment_id : :class:`str`
            The enrolment's ID.
        reason : Union[:class:`str`, None], optional
            Why it was revoked, by default None. It's kept as the enrolment's `revokedReason`.

        """
        data: Optional[SpireEnrollmentRevokeRequest] = {"reason": reason} if reason is not None else None
        await self._request(method="DELETE", path=f"/api/spires/enrollments/{enrollment_id}", data=data)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # Only refusals are known; the reply for a machine waiting on a join file isn't.
    async def deny_spire_enrollment(self, enrollment_id: str) -> Any:
        """Refuse a machine that used a join file.

        |coro|

        Endpoint: ``POST /api/spires/enrollments/{enrollment_id}/deny``

        Parameters
        ----------
        enrollment_id : :class:`str`
            The enrolment's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If no machine is waiting on the enrolment, eg. it is pending or revoked
            (409, ``"spire.enroll.error.nothingToApprove"``), or there's no such enrolment (404).

        """
        return await self._request(method="POST", path=f"/api/spires/enrollments/{enrollment_id}/deny")

    async def get_spire(self, spire_id: str) -> Spire:
        """Get one spire.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        :class:`Spire`
            The spire, with the calls that act on it.

        """
        result: SpireResponse = await self._request(method="GET", path=f"/api/spires/{spire_id}")
        return Spire(module=self, data=result)

    async def get_spires(self) -> list[Spire]:
        """Get every spire the logged in user can see.

        |coro|

        Endpoint: ``GET /api/spires``

        Returns
        -------
        list[:class:`Spire`]
            The spires, each with the calls that act on it.

        """
        result: list[SpireResponse] = await self._request(method="GET", path="/api/spires")
        return [Spire(module=self, data=entry) for entry in result]

    async def get_spire_datastores(self, spire_id: str) -> list[DatastoreResponse]:
        """Get a spire's datastores, the folders shards are kept in.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}/datastores``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        list[:class:`DatastoreResponse`]
            The datastores.

        """
        return await self._request(method="GET", path=f"/api/spires/{spire_id}/datastores")

    async def get_spire_enrollment_hosts(self) -> list[SpireEnrollmentHostResponse]:
        """Get the addresses a new spire could reach the panel on.

        |coro|

        Endpoint: ``GET /api/spires/enrollments/hosts``

        Returns
        -------
        list[:class:`SpireEnrollmentHostResponse`]
            The addresses, the public one included.

        """
        return await self._request(method="GET", path="/api/spires/enrollments/hosts")

    async def get_spire_enrollments(self) -> list[SpireEnrollmentResponse]:
        """Get the join files that were made, and their state.

        |coro|

        Endpoint: ``GET /api/spires/enrollments``

        Returns
        -------
        list[:class:`SpireEnrollmentResponse`]
            The enrolments, newest first. Revoked and redeemed ones stay in the list.

        """
        return await self._request(method="GET", path="/api/spires/enrollments")

    async def get_spire_ip_options(self, spire_id: str, *, include_auto: bool = False) -> list[SpireIPOptionResponse]:
        """Get the addresses a shard on a spire can bind to.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}/ip-options``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        include_auto : :class:`bool`, optional
            If the list should start with AMP's ``"@auto-pool"`` choice or not, by default False.

        Returns
        -------
        list[:class:`SpireIPOptionResponse`]
            The addresses, eg. ``"0.0.0.0"``, ``"127.0.0.1"`` and the spire's own.

        """
        parameters: Optional[dict[str, str]] = {"includeAuto": "true"} if include_auto is True else None
        return await self._request(method="GET", path=f"/api/spires/{spire_id}/ip-options", parameters=parameters)

    async def get_spire_port_claims(self, spire_id: str) -> list[PortClaimResponse]:
        """Get every port held on a spire, by AMP's own services as well as shards.

        |coro|

        Endpoint: ``GET /api/networking/spires/{spire_id}/port-claims``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        list[:class:`PortClaimResponse`]
            The ports and what holds each one.

        """
        return await self._request(method="GET", path=f"/api/networking/spires/{spire_id}/port-claims")

    async def get_spire_ports(self, spire_id: str) -> list[SpirePortResponse]:
        """Get the ports a spire's shards use.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}/ports``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        list[:class:`SpirePortResponse`]
            The ports, empty with no shards.

        """
        return await self._request(method="GET", path=f"/api/spires/{spire_id}/ports")

    async def get_spire_roster(self) -> list[SpireRosterResponse]:
        """Get every spire with if it's online and its AMP version.

        |coro|

        Endpoint: ``GET /api/spires/roster``

        Returns
        -------
        list[:class:`SpireRosterResponse`]
            The spires.

        """
        return await self._request(method="GET", path="/api/spires/roster")

    async def get_spire_settings_manifest(self, spire_id: str) -> SettingsManifestResponse:
        """Get a spire's settings with their current values.

        |coro|

        Endpoint: ``GET /api/settings/spire/{spire_id}/manifest``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        :class:`SettingsManifestResponse`
            The settings and their values; a spire's have no actions.

        """
        return await self._request(method="GET", path=f"/api/settings/spire/{spire_id}/manifest")

    async def get_spire_startup(self, spire_id: str) -> list[SpireStartupResponse]:
        """Get the order a spire starts its shards in when it boots.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}/startup``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        list[:class:`SpireStartupResponse`]
            The shards, in their start order.

        """
        return await self._request(method="GET", path=f"/api/spires/{spire_id}/startup")

    async def get_spire_state(self, spire_id: str) -> SpireStateResponse:
        """Get a spire's live load and the machine it runs on.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}/state``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID. An unknown one gets an offline state, not an error.

        Returns
        -------
        :class:`SpireStateResponse`
            The spire's load, memory, network and machine details.

        """
        return await self._request(method="GET", path=f"/api/spires/{spire_id}/state")

    async def get_spire_usage(self, spire_id: str) -> Optional[SpireUsageResponse]:
        """Get a spire's disk use per datastore, from its last scan.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}/usage``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        Union[:class:`SpireUsageResponse`, None]
            The disk use, `None` before the first scan. The web panel reads a 204 that way, and a spire scans when it
            starts.

        """
        return await self._request(method="GET", path=f"/api/spires/{spire_id}/usage")

    async def get_spire_usage_interval(self, spire_id: str) -> SpireUsageIntervalResponse:
        """Get how often a spire measures its disk use.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}/usage/interval``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        :class:`SpireUsageIntervalResponse`
            The interval in minutes, 5 by default.

        """
        return await self._request(method="GET", path=f"/api/spires/{spire_id}/usage/interval")

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # The web panel reads a `taskId` from it; the rest of the reply isn't known yet.
    async def import_spire_servers(self, spire_id: str, items: list[SpireImportItem], *, enter_other_volumes: bool = False) -> Any:
        """Import game servers from other panels into a spire as shards.

        |coro|

        Endpoint: ``POST /api/spires/{spire_id}/import``

        The web panel follows the import in :meth:`TaskModule.get_running_tasks`.

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        items : list[:class:`SpireImportItem`]
            The servers to import, from :meth:`scan_spire_imports`.
        enter_other_volumes : :class:`bool`, optional
            If AMP may go into other volumes for them or not, by default False.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        data: SpireImportRequest = {"items": items, "enterOtherVolumes": enter_other_volumes}
        return await self._request(method="POST", path=f"/api/spires/{spire_id}/import", data=data)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.8).
    # The web panel reads a `blocked` list from it; the rest of the reply isn't known yet.
    async def preflight_spire_import(self, spire_id: str, items: list[SpireImportItem]) -> Any:
        """Check game servers can be imported into a spire, before :meth:`import_spire_servers`.

        |coro|

        Endpoint: ``POST /api/spires/{spire_id}/import/preflight``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        items : list[:class:`SpireImportItem`]
            The servers to check, from :meth:`scan_spire_imports`.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path=f"/api/spires/{spire_id}/import/preflight", data={"items": items})

    async def purge_spire_expired_shards(self, spire_id: str) -> SpireExpiredPurgeResponse:
        """Remove for good a spire's deleted shards that are past keeping.

        |coro|

        Endpoint: ``POST /api/spires/{spire_id}/purge-expired-shards``

        A shard deleted but not yet past its keeping time stays; use :meth:`ShardModule.purge_shard` for one now.

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        :class:`SpireExpiredPurgeResponse`
            How many shards AMP is purging.

        """
        return await self._request(method="POST", path=f"/api/spires/{spire_id}/purge-expired-shards")

    async def purge_spire_orphan_directories(self, spire_id: str, datastore_id: str) -> SpireUsageResponse:
        """Delete every folder in a datastore that no shard owns.

        |coro|

        Endpoint: ``POST /api/spires/{spire_id}/datastores/{datastore_id}/purge-orphans``

        AMP measures the disk use again for the reply, so it needs no :meth:`rescan_spire_usage` after. A datastore
        with no orphans gets the same reply.

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        datastore_id : :class:`str`
            The datastore's ID.

        Returns
        -------
        :class:`SpireUsageResponse`
            The spire's disk use after.

        Raises
        ------
        AMPAPIRequestError
            If the spire has no such datastore (409, ``"datastore.error.notFound"``).

        """
        return await self._request(method="POST", path=f"/api/spires/{spire_id}/datastores/{datastore_id}/purge-orphans")

    async def purge_spire_orphan_directory(self, spire_id: str, datastore_id: str, name: str) -> SpireUsageResponse:
        """Delete one folder in a datastore that no shard owns.

        |coro|

        Endpoint: ``POST /api/spires/{spire_id}/datastores/{datastore_id}/purge-orphan``

        This is how the copy a move leaves behind goes, from :meth:`ShardModule.migrate_shard_to_spire` or a move between
        datastores with :meth:`ShardModule.start_shard_migration`. Call it on the old spire and datastore, with the
        shard's `workingDirName` as `name`. The orphan is only listed once the spire's disk use is measured again, see
        :meth:`rescan_spire_usage`.

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        datastore_id : :class:`str`
            The datastore's ID.
        name : :class:`str`
            The folder's name, an ``"Orphan"`` entry's `name` in :meth:`get_spire_usage`.

        Returns
        -------
        :class:`SpireUsageResponse`
            The spire's disk use after.

        Raises
        ------
        AMPAPIRequestError
            If the datastore has no such folder, eg. it was purged already (409, ``"datastore.error.purgeMissing"``).

        """
        path: str = f"/api/spires/{spire_id}/datastores/{datastore_id}/purge-orphan"
        return await self._request(method="POST", path=path, data={"name": name})

    async def rescan_spire_usage(self, spire_id: str) -> Optional[SpireUsageResponse]:
        """Measure a spire's disk use now.

        |coro|

        Endpoint: ``POST /api/spires/{spire_id}/usage/rescan``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.

        Returns
        -------
        Union[:class:`SpireUsageResponse`, None]
            The disk use per datastore, `None` for a 204, which the web panel allows for here too.

        """
        return await self._request(method="POST", path=f"/api/spires/{spire_id}/usage/rescan")

    async def scan_spire_imports(self, spire_id: str, roots: list[str], *, automatic: bool = False) -> SpireImportScanResponse:
        """Look for game servers from other panels on a spire, eg. Pterodactyl, LinuxGSM or AMP 2.

        |coro|

        Endpoint: ``POST /api/spires/{spire_id}/import/scan``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        roots : list[:class:`str`]
            The folders to look in. AMP refuses an empty list (``"import.error.noRoots"``) unless `automatic` is set.
        automatic : :class:`bool`, optional
            If AMP should pick the folders itself or not, by default False.

        Returns
        -------
        :class:`SpireImportScanResponse`
            What AMP found.

        """
        data: SpireImportScanRequest = {"roots": roots}
        if automatic is True:
            data["automatic"] = True

        return await self._request(method="POST", path=f"/api/spires/{spire_id}/import/scan", data=data)

    async def set_spire_settings(self, spire_id: str, values: SettingValues) -> None:
        """Change some of a spire's settings.

        |coro|

        Endpoint: ``POST /api/settings/spire/{spire_id}/values``

        AMP answers 204. There's no call that reads the values back on their own; they're in
        :meth:`get_spire_settings_manifest`'s `values`.

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        values : :class:`SettingValues`
            Each setting's `fieldName` from :meth:`get_spire_settings_manifest` to its new value, a string like the
            manifest's values. eg. ``{"spire.publicHost": "amp.example.com"}`` lets the spire front a publication or a
            gateway through it: it reads `isPubliclyRoutable` `True` at once.

        Raises
        ------
        AMPAPIRequestError
            If the spire has no such setting (400, ``"settings.error.unknownNode"``).

        """
        await self._request(method="POST", path=f"/api/settings/spire/{spire_id}/values", data=values)

    async def set_spire_startup(self, spire_id: str, entries: list[SpireStartupEntry]) -> list[SpireStartupResponse]:
        """Set the order a spire starts its shards in when it boots, and which ones start.

        |coro|

        Endpoint: ``PUT /api/spires/{spire_id}/startup``

        .. note::
            Only the shards sent change: each one's place in the list becomes its `order`, and the rest keep theirs.
            An empty list changes nothing, so take a shard off by sending it with `startOnBoot` `False`. AMP drops a
            shard ID it doesn't know.

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        entries : list[:class:`SpireStartupEntry`]
            The shards in the order they start, eg. ``[{"shardId": "...", "startOnBoot": True}]``.

        Returns
        -------
        list[:class:`SpireStartupResponse`]
            The entries AMP saved, only those sent; :meth:`get_spire_startup` has the whole order.

        """
        return await self._request(method="PUT", path=f"/api/spires/{spire_id}/startup", data=entries)

    async def set_spire_usage_interval(self, spire_id: str, minutes: int) -> SpireStorageResponse:
        """Set how often a spire measures its disk use.

        |coro|

        Endpoint: ``PUT /api/spires/{spire_id}/usage/interval``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID.
        minutes : :class:`int`
            The interval in minutes. AMP turns 0 into 1.

        Returns
        -------
        :class:`SpireStorageResponse`
            The spire's storage settings, the new interval included.

        """
        return await self._request(method="PUT", path=f"/api/spires/{spire_id}/usage/interval", data={"minutes": minutes})
