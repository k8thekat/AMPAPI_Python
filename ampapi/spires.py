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

# from .hubs import PanelHub, SpireHub
from .objects import SpireStatus

if TYPE_CHECKING:
    from ._types import (
        DatastoreRequest,
        DatastoreResponse,
        PortClaimResponse,
        SettingsManifestResponse,
        SettingValues,
        SpireExpiredPurgeResponse,
        SpireImportItem,
        SpireImportRequest,
        SpireImportScanRequest,
        SpireImportScanResponse,
        SpireIPOptionResponse,
        SpirePortResponse,
        SpireResponse,
        SpireStartupEntry,
        SpireStartupResponse,
        SpireStorageResponse,
        SpireUsageIntervalResponse,
        SpireUsageResponse,
    )
    from .panel import Panel
    from .session import Session
    from .shards import Shard

__all__ = (
    "Spire",
    "SpireModule",
)

LOGGER: logging.Logger = logging.getLogger(__name__)


# class Spire(SpireHub):
class Spire:
    """A spire, AMP 3's name for an ADS or Target, with the calls that act on it.

    :meth:`Panel.get_spires` and :meth:`Panel.get_spire` make these, of the panel's `spire_class`, and the panel keeps
    one for each spire. Each method calls the :class:`SpireModule` one with this spire's ID, eg. :meth:`get_state` is
    :meth:`SpireModule.get_spire_state`. The shards on it come from :meth:`get_shards`.

    A spire that joined serves the whole panel API too, so a :class:`Panel` can talk to any of them. The data's
    `isLocal` is relative to the machine that answered, not a property of the spire.

    Two spire objects are equal, and hash the same, when they have the same ID, so they work in sets and as dict keys.
    They sort by `display_name`.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    module : :class:`Panel`
        The panel the calls go through.
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
        The panel brings it up to date each time it hands this object out again.
    session : :class:`Session`
        The panel's session.

    """

    # A subclass can declare listeners and subscribe shards; see :class:`SpireHub`.
    # auto_state : Union[:class:`bool`, None], optional
    #     If `state` follows the spire's state events from the hub or not; read back with the property. By default None
    #     for the panel's `auto_state` (False unless the panel was made with True), or False with no panel.

    data: SpireResponse
    display_name: str
    id: str
    session: Session
    # _module: SpireModule
    _module: Panel

    # def __init__(self, module: SpireModule, data: SpireResponse, *, auto_state: Optional[bool] = None) -> None:
    def __init__(self, module: Panel, data: SpireResponse) -> None:  # noqa: D107
        # super().__init__(session=module.session, panel=module if isinstance(module, PanelHub) else None, auto_state=auto_state)
        self.session = module.session
        self._module = module
        self.data = data
        self.id = data["id"]
        self.display_name = data["displayName"]

        # if self._panel is not None:
        #     self._panel._register_spire(spire=self)

    def __hash__(self) -> int:  # noqa: D105
        return hash(self.id)

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, Spire) and self.id == other.id

    def __lt__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, Spire) and self.display_name < other.display_name

    def __repr__(self) -> str:  # noqa: D105
        return f"<{type(self).__name__} id={self.id!r} display_name={self.display_name!r}>"

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

    async def create_shard(
        self,
        template_slug: str,
        display_name: str,
        *,
        description: str = "",
        start_now: bool = False,
        start_on_boot: bool = False,
        credential_id: Optional[str] = None,
    ) -> Shard:
        """Make a shard on this spire from a template, see :meth:`Panel.create_shard`.

        |coro|

        Parameters
        ----------
        template_slug : :class:`str`
            The template, eg. ``"minecraft-java"``; see :meth:`TemplateModule.get_templates`.
        display_name : :class:`str`
            The shard's name. An empty one gets the template's name.
        description : :class:`str`, optional
            A description, by default "".
        start_now : :class:`bool`, optional
            If the shard should start once made or not, by default False.
        start_on_boot : :class:`bool`, optional
            If the shard starts when this spire boots or not, by default False.
        credential_id : Union[:class:`str`, None], optional
            A stored secret for the game's download, eg. a Steam login, by default None.

        Returns
        -------
        :class:`Shard`
            The new shard, with the calls that act on it.

        """
        return await self._module.create_shard(
            template_slug=template_slug,
            display_name=display_name,
            spire_id=self.id,
            description=description,
            start_now=start_now,
            start_on_boot=start_on_boot,
            credential_id=credential_id,
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

    async def get_shards(self, *, include_deleted: bool = False) -> list[Shard]:
        """Get the shards on this spire, from :meth:`Panel.get_shards`.

        |coro|

        Endpoint: ``GET /api/shards``

        AMP has no route for one spire's shards, so we list every shard the logged in user can see and keep this
        spire's.

        Parameters
        ----------
        include_deleted : :class:`bool`, optional
            If deleted shards that aren't purged yet are listed too or not, by default False.
            A deleted one answers only :meth:`Shard.restore` and :meth:`Shard.purge`.

        Returns
        -------
        list[:class:`Shard`]
            The shards on this spire, each with the calls that act on it.

        """
        shards: list[Shard] = await self._module.get_shards(include_deleted=include_deleted)
        return [shard for shard in shards if shard.data["spireId"] == self.id]

    async def get_startup(self) -> list[SpireStartupResponse]:
        """Get this spire's shard start order, see :meth:`SpireModule.get_spire_startup`.

        |coro|

        Returns
        -------
        list[:class:`SpireStartupResponse`]
            The shards, in their start order.

        """
        return await self._module.get_spire_startup(spire_id=self.id)

    async def get_state(self) -> SpireStatus:
        """Get this spire's live load, see :meth:`SpireModule.get_spire_state`.

        |coro|

        Returns
        -------
        :class:`SpireStatus`
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
    """The calls for one spire, AMP 3's name for an ADS or Target, each taking its ID: datastores, ports, start order
    and disk use.

    The calls over all of the panel's spires, eg. :meth:`Panel.get_spires` and :meth:`Panel.get_spire_roster`, are on
    the :class:`Panel`. Joining a new spire to the panel is :class:`EnrollmentModule`.

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

    async def get_spire_state(self, spire_id: str) -> SpireStatus:
        """Get a spire's live load and the machine it runs on.

        |coro|

        Endpoint: ``GET /api/spires/{spire_id}/state``

        Parameters
        ----------
        spire_id : :class:`str`
            The spire's ID. An unknown one gets an offline state, not an error.

        Returns
        -------
        :class:`SpireStatus`
            The spire's load, memory, network and machine details.

        """
        result: dict[str, Any] = await self._request(method="GET", path=f"/api/spires/{spire_id}/state")
        return SpireStatus(data=result)

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
