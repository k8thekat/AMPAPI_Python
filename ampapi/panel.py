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

# from typing import TYPE_CHECKING, ClassVar, Optional, Self
from typing import TYPE_CHECKING, Any, Optional, Self

from .accounts import AccountModule
from .analytics import AnalyticsModule
from .audit import AuditModule
from .credentials import CredentialModule
from .enrollments import EnrollmentModule

# from .hubs import PanelHub
from .networking import NetworkModule
from .objects import SpirePresence
from .platform import PlatformModule
from .shards import Shard, ShardModule
from .spires import Spire, SpireModule
from .tasks import TaskModule
from .templates import TemplateModule

if TYPE_CHECKING:
    from types import TracebackType

    from ._types import ShardCreatedResponse, ShardCreateRequest, ShardEndpointResponse, ShardResponse, SpireResponse
    from .session import Session

__all__ = ("Panel",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Panel(
    # PanelHub,
    AccountModule,
    AnalyticsModule,
    AuditModule,
    CredentialModule,
    EnrollmentModule,
    NetworkModule,
    PlatformModule,
    ShardModule,
    SpireModule,
    TaskModule,
    TemplateModule,
):
    """An AMP 3 panel, with every call this library wraps.

    The calls come from the `...Module` classes it is built from, and each one logs in through the :class:`Session` when
    it needs to. The calls over all of the panel's shards or spires are its own, eg. :meth:`get_shards`.

    It keeps the shard and spire objects it hands out, one for each ID, so ``panel.get_shard(shard_id=...)`` gives back
    the same object each time, with its `data` and `display_name` brought up to date.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session to send calls through.
        Leaving an ``async with`` block, or :meth:`clean_up`, logs it out and closes it.
    shard_class : type[:class:`Shard`], optional
        The class `get_shard` and `get_shards` make, eg. a subclass of your own, by default :class:`Shard`.
    spire_class : type[:class:`Spire`], optional
        The class `get_spire` and `get_spires` make, by default :class:`Spire`.

    """

    # An AMP 3 panel, with every call this library wraps, and the panel level of the hubs.
    # A subclass can declare listeners, eg. ``@PanelHub.listener(name="console")``; see :class:`PanelHub`.
    # auto_state : :class:`bool`, optional
    #     The `auto_state` a shard or spire object gets when it's made with `None`, by default False. That's the default
    #     of `get_shard`, `get_shards`, `get_spire`, `get_spires`, and of a :class:`Shard` or :class:`Spire` made by hand.

    shard_class: type[Shard]
    spire_class: type[Spire]
    _shards: dict[str, Shard]
    _spires: dict[str, Spire]

    def __init__(  # noqa: D107
        self,
        session: Session,
        *,
        shard_class: type[Shard] = Shard,
        spire_class: type[Spire] = Spire,
        # auto_state: bool = False,
    ) -> None:
        # super().__init__(session=session, auto_state=auto_state)
        super().__init__(session=session)
        self.shard_class = shard_class
        self.spire_class = spire_class
        self._shards = {}
        self._spires = {}

    async def __aenter__(self) -> Self:  # noqa: D105
        return self

    async def __aexit__(  # noqa: D105
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.clean_up()

    async def clean_up(self) -> None:
        """Log out and close the session, as :meth:`Session.clean_up` does.

        |coro|

        Endpoint: ``POST /api/auth/logout``

        """
        # await self.stop_listening()
        await self.session.clean_up()

    def _make_shard(self, data: ShardResponse, created: Optional[ShardCreatedResponse] = None) -> Shard:
        """The shard object we keep for `data`'s ID, brought up to date, or a new `shard_class` one we keep from now on.

        `created` only reaches a new object. A listing that raced `create_shard` could have kept the shard first, and
        that object keeps `None` for the creation reply.
        """
        shard: Optional[Shard] = self._shards.get(data["id"])
        if shard is None:
            shard = self.shard_class(module=self, data=data, created=created)
            self._shards[shard.id] = shard
        else:
            shard.data = data
            shard.display_name = data["displayName"]
        return shard

    # TODO: Remove the note once AMP refuses to start a shard that was never updated (U15).
    # AMP 3.0.0.6 answers the start with 202, then the start fails after pulling its container.
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
    ) -> Shard:
        """Make a shard from a template. It installs nothing until :meth:`ShardModule.update_shard`.

        |coro|

        Endpoint: ``POST /api/shards``

        .. note::
            A shard that was never updated still starts, then fails after pulling its container.

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
            If the shard should start once made or not, by default False.
        start_on_boot : :class:`bool`, optional
            If the shard starts when its spire boots or not, by default False.
        credential_id : Union[:class:`str`, None], optional
            A stored secret for the game's download, eg. a Steam login, by default None.

        Returns
        -------
        :class:`Shard`
            The new shard, with the calls that act on it. The rest of AMP's reply is on its :attr:`Shard.infra_settings`,
            :attr:`Shard.app_config`, :attr:`Shard.port_assignments`, :attr:`Shard.port_outcomes` and
            :attr:`Shard.over_licence_limit`.

        Raises
        ------
        AMPAPIRequestError
            If the template doesn't exist (400, ``"shards.error.createFailed"``, which doesn't name the cause).

        """
        data: ShardCreateRequest = {
            "templateSlug": template_slug,
            "displayName": display_name,
            "description": description,
            "spireId": spire_id,
            "startNow": start_now,
            "startOnBoot": start_on_boot,
        }

        if credential_id is not None:
            data["credentialId"] = credential_id

        result: ShardCreatedResponse = await self._request(method="POST", path="/api/shards", data=data)
        return self._make_shard(data=result["shard"], created=result)

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

    # auto_state : Union[:class:`bool`, None], optional
    #     The `auto_state` a new shard object is made with, by default None for the panel's (False unless the panel
    #     was made with True). A shard the panel already holds an object for keeps that object's own `auto_state`.
    # async def get_shard(self, shard_id: str, *, auto_state: Optional[bool] = None) -> Shard:
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
        # return self._make_shard(data=result, auto_state=auto_state)
        return self._make_shard(data=result)

    # auto_state : Union[:class:`bool`, None], optional
    #     The `auto_state` each new shard object is made with, by default None for the panel's (False unless the
    #     panel was made with True). A shard the panel already holds an object for keeps that object's own.
    # async def get_shards(self, *, include_deleted: bool = False, auto_state: Optional[bool] = None) -> list[Shard]:
    async def get_shards(self, *, include_deleted: bool = False) -> list[Shard]:
        """Get every shard the logged in user can see.

        |coro|

        Endpoint: ``GET /api/shards``

        .. note::
            A deleted shard answers only :meth:`Shard.restore` and :meth:`Shard.purge`. Any other call on it gets
            409 ``"shards.error.deleted"``.

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
        # return [self._make_shard(data=entry, auto_state=auto_state) for entry in result]
        return [self._make_shard(data=entry) for entry in result]

    # TODO: Type the items once AMP is seen listing one live (#3-47.7).
    # The item shape isn't known yet; the web panel reads `shardId`, `name` and `message` from each.
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

    def _make_spire(self, data: SpireResponse) -> Spire:
        """The spire object we keep for `data`'s ID, brought up to date, or a new `spire_class` one we keep from now on."""
        spire: Optional[Spire] = self._spires.get(data["id"])
        if spire is None:
            spire = self.spire_class(module=self, data=data)
            self._spires[spire.id] = spire
        else:
            spire.data = data
            spire.display_name = data["displayName"]
        return spire

    # auto_state : Union[:class:`bool`, None], optional
    #     The `auto_state` a new spire object is made with, by default None for the panel's (False unless the panel
    #     was made with True). A spire the panel already holds an object for keeps that object's own `auto_state`.
    # async def get_spire(self, spire_id: str, *, auto_state: Optional[bool] = None) -> Spire:
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
        # return self._make_spire(data=result, auto_state=auto_state)
        return self._make_spire(data=result)

    # auto_state : Union[:class:`bool`, None], optional
    #     The `auto_state` each new spire object is made with, by default None for the panel's (False unless the
    #     panel was made with True). A spire the panel already holds an object for keeps that object's own.
    # async def get_spires(self, *, auto_state: Optional[bool] = None) -> list[Spire]:
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
        # return [self._make_spire(data=entry, auto_state=auto_state) for entry in result]
        return [self._make_spire(data=entry) for entry in result]

    async def get_spire_roster(self) -> list[SpirePresence]:
        """Get every spire with if it's online and its AMP version.

        |coro|

        Endpoint: ``GET /api/spires/roster``

        Returns
        -------
        list[:class:`SpirePresence`]
            The spires.

        """
        result: list[dict[str, Any]] = await self._request(method="GET", path="/api/spires/roster")
        return [SpirePresence(data=entry) for entry in result]
