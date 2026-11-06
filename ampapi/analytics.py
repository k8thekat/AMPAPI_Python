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
from typing import TYPE_CHECKING, Any, Optional, Union

from .base import Base

if TYPE_CHECKING:
    from ._types import (
        AnalyticsAddressUsersResponse,
        AnalyticsProfilesResponse,
        AnalyticsSessionsResponse,
        AnalyticsUserAddressesResponse,
        AnalyticsUserSessionsResponse,
        AnalyticsUsersResponse,
        AuditFacetsResponse,
        AuditPageResponse,
        AuditRootsPageResponse,
        AuditTreeResponse,
    )

__all__ = ("AnalyticsModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class AnalyticsModule(Base):
    """The calls for player analytics and the audit log.

    The analytics calls were only seen on a panel with no players, so most of their lists have no known item shape.
    Each takes `demo`, which the web panel uses for a demo mode; it changed nothing on the test panel.

    .. versionadded:: 6.0.0

    """

    # TODO: The player skin and avatar images, which come back as bytes (#47.7's raw replies).

    async def delete_analytics_user_sessions(self, user_key: str, *, demo: bool = False) -> Any:
        """Erase everything the analytics hold about one player.

        |coro|

        Endpoint: ``DELETE /api/analytics/sessions/users/{user_key}``

        .. warning::
            Not yet seen live, so the shape of AMP's reply is unknown.

        Parameters
        ----------
        user_key : :class:`str`
            The player's key.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        parameters: Optional[dict[str, str]] = {"demo": "true"} if demo is True else None
        return await self._request(method="DELETE", path=f"/api/analytics/sessions/users/{user_key}", parameters=parameters)

    async def get_analytics_address_users(self, address: str, *, demo: bool = False) -> AnalyticsAddressUsersResponse:
        """Get the players seen at one address.

        |coro|

        Endpoint: ``GET /api/analytics/addresses/users``

        Parameters
        ----------
        address : :class:`str`
            A whole IP address, eg. ``"192.0.2.1"``.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        :class:`AnalyticsAddressUsersResponse`
            The address, its network and its players.

        """
        parameters: dict[str, str] = {"address": address}
        if demo is True:
            parameters["demo"] = "true"
        return await self._request(method="GET", path="/api/analytics/addresses/users", parameters=parameters)

    async def get_analytics_addresses(self, search: str, *, demo: bool = False) -> Any:
        """Search the addresses players were seen at.

        |coro|

        Endpoint: ``GET /api/analytics/addresses``

        .. warning::
            Not yet seen live working: part of an address is refused (400, ``"analytics.error.badAddress"``), so the
            shape of AMP's reply is unknown.

        Parameters
        ----------
        search : :class:`str`
            The address to look for.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        parameters: dict[str, str] = {"q": search}
        if demo is True:
            parameters["demo"] = "true"
        return await self._request(method="GET", path="/api/analytics/addresses", parameters=parameters)

    async def get_analytics_connected_users(self, user_key: str, *, user: Optional[str] = None) -> Any:
        """Get the players connected to one player, as far as the web panel shows.

        |coro|

        Endpoint: ``GET /api/analytics/connected/{user_key}``

        .. warning::
            Not yet seen live working (an unknown player gave 404), so the shape of AMP's reply is unknown, and so is
            what the `user` query value means.

        Parameters
        ----------
        user_key : :class:`str`
            The player's key.
        user : Union[:class:`str`, None], optional
            The web panel's `user` query value, by default None.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        parameters: Optional[dict[str, str]] = {"user": user} if user is not None else None
        return await self._request(method="GET", path=f"/api/analytics/connected/{user_key}", parameters=parameters)

    async def get_analytics_profiles(self, user_keys: list[str], *, demo: bool = False) -> AnalyticsProfilesResponse:
        """Get players' Steam and Minecraft profiles.

        |coro|

        Endpoint: ``GET /api/analytics/profiles``

        Parameters
        ----------
        user_keys : list[:class:`str`]
            The players' keys.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        :class:`AnalyticsProfilesResponse`
            The profiles, by service.

        """
        parameters: dict[str, Union[str, list[str]]] = {"key": user_keys}
        if demo is True:
            parameters["demo"] = "true"
        return await self._request(method="GET", path="/api/analytics/profiles", parameters=parameters)

    async def get_analytics_sessions(
        self,
        *,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        shard_ids: Optional[list[str]] = None,
        country: Optional[str] = None,
        user: Optional[str] = None,
        top_users: Optional[int] = None,
        demo: bool = False,
    ) -> AnalyticsSessionsResponse:
        """Get the player summary the analytics page shows.

        |coro|

        Endpoint: ``GET /api/analytics/sessions``

        Parameters
        ----------
        from_time : Union[:class:`str`, None], optional
            The start of the window, ISO 8601 like ``"2026-11-01T00:00:00Z"``, by default None.
            Without `from_time` and `to_time` it's the last 30 days.
        to_time : Union[:class:`str`, None], optional
            The end of the window, ISO 8601, by default None.
        shard_ids : Union[list[:class:`str`], None], optional
            Only these shards, by default None.
        country : Union[:class:`str`, None], optional
            Only players from this country code, eg. ``"US"``, by default None.
        user : Union[:class:`str`, None], optional
            Only this player, by default None. Not yet seen live.
        top_users : Union[:class:`int`, None], optional
            How many top players to list, by default None.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        :class:`AnalyticsSessionsResponse`
            The totals, daily activity and busiest times.

        """
        filters: dict[str, Optional[Union[str, int, list[str]]]] = {
            "from": from_time,
            "to": to_time,
            "shard": shard_ids,
            "country": country,
            "user": user,
            "topUsers": top_users,
            "demo": "true" if demo is True else None,
        }
        # We only send the filters that are set, as the web panel does.
        parameters: dict[str, Union[str, int, list[str]]] = {key: value for key, value in filters.items() if value is not None}
        return await self._request(method="GET", path="/api/analytics/sessions", parameters=parameters)

    async def get_analytics_user_addresses(self, user_key: str, *, demo: bool = False) -> AnalyticsUserAddressesResponse:
        """Get the addresses one player was seen at.

        |coro|

        Endpoint: ``GET /api/analytics/users/{user_key}/addresses``

        Parameters
        ----------
        user_key : :class:`str`
            The player's key.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        :class:`AnalyticsUserAddressesResponse`
            The addresses.

        """
        parameters: Optional[dict[str, str]] = {"demo": "true"} if demo is True else None
        return await self._request(method="GET", path=f"/api/analytics/users/{user_key}/addresses", parameters=parameters)

    async def get_analytics_user_sessions(
        self,
        user_key: str,
        *,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        demo: bool = False,
    ) -> AnalyticsUserSessionsResponse:
        """Get one player's history. An unknown player gets an empty one, not an error.

        |coro|

        Endpoint: ``GET /api/analytics/sessions/users/{user_key}``

        Parameters
        ----------
        user_key : :class:`str`
            The player's key.
        from_time : Union[:class:`str`, None], optional
            The start of the window, ISO 8601, by default None.
        to_time : Union[:class:`str`, None], optional
            The end of the window, ISO 8601, by default None.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        :class:`AnalyticsUserSessionsResponse`
            The player's totals and sessions.

        """
        filters: dict[str, Optional[str]] = {"from": from_time, "to": to_time, "demo": "true" if demo is True else None}
        parameters: dict[str, str] = {key: value for key, value in filters.items() if value is not None}
        return await self._request(method="GET", path=f"/api/analytics/sessions/users/{user_key}", parameters=parameters)

    async def get_analytics_users(
        self,
        *,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        demo: bool = False,
    ) -> AnalyticsUsersResponse:
        """Search the players the analytics have seen.

        |coro|

        Endpoint: ``GET /api/analytics/users``

        Parameters
        ----------
        search : Union[:class:`str`, None], optional
            Part of a player's name, by default None.
        limit : Union[:class:`int`, None], optional
            The most players to get, by default None. The web panel asks for 12.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        :class:`AnalyticsUsersResponse`
            The players found.

        """
        filters: dict[str, Optional[Union[str, int]]] = {"q": search, "limit": limit, "demo": "true" if demo is True else None}
        parameters: dict[str, Union[str, int]] = {key: value for key, value in filters.items() if value is not None}
        return await self._request(method="GET", path="/api/analytics/users", parameters=parameters)

    async def get_audit_events(
        self,
        *,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        origin: Optional[str] = None,
        min_severity: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        search: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> AuditPageResponse:
        """Get one page of the audit log.

        |coro|

        Endpoint: ``GET /api/audit``

        .. note::
            AMP ignores a filter it doesn't know, so a misspelt one gives the whole log rather than an error.

        Parameters
        ----------
        user_id : Union[:class:`str`, None], optional
            Only events by this user's ID, by default None.
        action : Union[:class:`str`, None], optional
            Only this action, eg. ``"ShardCreated"`` (any case), by default None.
            See :meth:`get_audit_facets` for the actions logged so far.
        origin : Union[:class:`str`, None], optional
            ``"System"``, ``"User"``, ``"UserFlow"``, ``"Scheduled"`` or ``"Impersonation"``, by default None.
        min_severity : Union[:class:`str`, None], optional
            ``"Info"``, ``"Warning"`` or ``"Security"``, by default None.
        target_type : Union[:class:`str`, None], optional
            Only events about this kind of thing, eg. ``"Shard"``, by default None.
        target_id : Union[:class:`str`, None], optional
            Only events about the thing with this ID, by default None.
        search : Union[:class:`str`, None], optional
            Text to look for, by default None.
        from_time : Union[:class:`str`, None], optional
            The earliest time, ISO 8601 like ``"2026-11-01T00:00:00Z"``, by default None.
        to_time : Union[:class:`str`, None], optional
            The latest time, ISO 8601, by default None.
        page : Union[:class:`int`, None], optional
            The page, from 1, by default None.
        page_size : Union[:class:`int`, None], optional
            Events a page, by default None. AMP gives 50 unless asked, and at most 200.
        sort : Union[:class:`str`, None], optional
            ``"asc"`` for oldest first, by default None (newest first).

        Returns
        -------
        :class:`AuditPageResponse`
            The page of events and the total that match.

        """
        filters: dict[str, Optional[Union[str, int]]] = {
            "userId": user_id,
            "action": action,
            "origin": origin,
            "minSeverity": min_severity,
            "targetType": target_type,
            "targetId": target_id,
            "search": search,
            "from": from_time,
            "to": to_time,
            "page": page,
            "pageSize": page_size,
            "sort": sort,
        }
        # We only send the filters that are set, as the web panel does.
        parameters: dict[str, Union[str, int]] = {key: value for key, value in filters.items() if value is not None}
        return await self._request(method="GET", path="/api/audit", parameters=parameters)

    async def get_audit_facets(self) -> AuditFacetsResponse:
        """Get what the audit log's filters can choose from, with how often each was logged.

        |coro|

        Endpoint: ``GET /api/audit/facets``

        Returns
        -------
        :class:`AuditFacetsResponse`
            The actions, users, target types and origins seen so far.

        """
        return await self._request(method="GET", path="/api/audit/facets")

    async def get_audit_roots(
        self,
        *,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        origin: Optional[str] = None,
        min_severity: Optional[str] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        search: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> AuditRootsPageResponse:
        """Get one page of the audit log grouped into flows, each led by the event that started it.

        |coro|

        Endpoint: ``GET /api/audit/roots``

        The filters are the same as :meth:`get_audit_events`.

        Parameters
        ----------
        user_id : Union[:class:`str`, None], optional
            Only events by this user's ID, by default None.
        action : Union[:class:`str`, None], optional
            Only this action, eg. ``"ShardCreated"`` (any case), by default None.
        origin : Union[:class:`str`, None], optional
            ``"System"``, ``"User"``, ``"UserFlow"``, ``"Scheduled"`` or ``"Impersonation"``, by default None.
        min_severity : Union[:class:`str`, None], optional
            ``"Info"``, ``"Warning"`` or ``"Security"``, by default None.
        target_type : Union[:class:`str`, None], optional
            Only events about this kind of thing, eg. ``"Shard"``, by default None.
        target_id : Union[:class:`str`, None], optional
            Only events about the thing with this ID, by default None.
        search : Union[:class:`str`, None], optional
            Text to look for, by default None.
        from_time : Union[:class:`str`, None], optional
            The earliest time, ISO 8601, by default None.
        to_time : Union[:class:`str`, None], optional
            The latest time, ISO 8601, by default None.
        page : Union[:class:`int`, None], optional
            The page, from 1, by default None.
        page_size : Union[:class:`int`, None], optional
            Flows a page, by default None.
        sort : Union[:class:`str`, None], optional
            ``"asc"`` for oldest first, by default None (newest first).

        Returns
        -------
        :class:`AuditRootsPageResponse`
            The page of flows and the total that match.

        """
        filters: dict[str, Optional[Union[str, int]]] = {
            "userId": user_id,
            "action": action,
            "origin": origin,
            "minSeverity": min_severity,
            "targetType": target_type,
            "targetId": target_id,
            "search": search,
            "from": from_time,
            "to": to_time,
            "page": page,
            "pageSize": page_size,
            "sort": sort,
        }
        parameters: dict[str, Union[str, int]] = {key: value for key, value in filters.items() if value is not None}
        return await self._request(method="GET", path="/api/audit/roots", parameters=parameters)

    async def get_audit_tree(self, correlation_id: str) -> AuditTreeResponse:
        """Get every event in one flow, as a tree.

        |coro|

        Endpoint: ``GET /api/audit/tree/{correlation_id}``

        Parameters
        ----------
        correlation_id : :class:`str`
            The flow's `correlationId` from :meth:`get_audit_roots`; the root event's own `id` gives 404.

        Returns
        -------
        :class:`AuditTreeResponse`
            The flow, from its first event down.

        Raises
        ------
        AMPAPIRequestError
            If no events carry that ID (404, ``"audit.error.flowNotFound"``).

        """
        return await self._request(method="GET", path=f"/api/audit/tree/{correlation_id}")
