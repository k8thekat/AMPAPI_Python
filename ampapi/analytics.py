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
    )

__all__ = ("AnalyticsModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class AnalyticsModule(Base):
    """The calls for player analytics: the players a panel's shards have seen, their sessions and addresses.

    Most of the analytics lists have no known item shape yet. Each call takes `demo`, which the web panel uses for a
    demo mode. The audit log is :class:`AuditModule`.

    .. versionadded:: 6.0.0

    """

    # TODO: Type the reply once AMP is seen answering it live (#3-47.11).
    # The path comes from the web panel's code; no capture shows the response yet.
    async def delete_analytics_user_sessions(self, user_key: str, *, demo: bool = False) -> Any:
        """Erase everything the analytics hold about one player.

        |coro|

        Endpoint: ``DELETE /api/analytics/sessions/users/{user_key}``

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

    # TODO: Type the reply once AMP is seen answering it live (#3-47.11).
    # Only the 400 for part of an address is known; the shape of a match isn't.
    async def get_analytics_addresses(self, search: str, *, demo: bool = False) -> Any:
        """Search the addresses players were seen at.

        |coro|

        Endpoint: ``GET /api/analytics/addresses``

        Parameters
        ----------
        search : :class:`str`
            The address to look for. AMP refuses part of one (400, ``"analytics.error.badAddress"``).
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

    # TODO: Confirm the image once AMP is seen sending one live (#3-47.11).
    # Only the 400 for an unknown key is known; the web panel reads the image as a blob.
    async def get_analytics_avatar(self, user_key: str, *, full: bool = False) -> bytes:
        """Get a player's avatar image.

        |coro|

        Endpoint: ``GET /api/analytics/avatars/{user_key}``

        Parameters
        ----------
        user_key : :class:`str`
            The player's key.
        full : :class:`bool`, optional
            If AMP should send the full size image or not, by default False.

        Returns
        -------
        :class:`bytes`
            The image as it came.

        Raises
        ------
        AMPAPIRequestError
            If AMP doesn't know the key (400, ``"analytics.error.badAvatar"``).

        """
        parameters: Optional[dict[str, str]] = {"full": "true"} if full is True else None
        return await self._request(method="GET", path=f"/api/analytics/avatars/{user_key}", parameters=parameters, raw_bytes=True)

    # TODO: Type the reply once AMP is seen answering it live (#3-47.11).
    # An unknown player answers 404 with no body, and what the `user` query value means isn't known yet.
    async def get_analytics_connected_users(self, user_key: str, *, user: Optional[str] = None) -> Any:
        """Get the players connected to one player, as far as the web panel shows.

        |coro|

        Endpoint: ``GET /api/analytics/connected/{user_key}``

        Parameters
        ----------
        user_key : :class:`str`
            The player's key.
        user : Union[:class:`str`, None], optional
            The web panel's `user` query value, by default None. What it means isn't known yet.

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
            Only this player, by default None.
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
        parameters: dict[str, Union[str, int, list[str]]] = self._without_none(mapping=filters)

        return await self._request(method="GET", path="/api/analytics/sessions", parameters=parameters)

    # TODO: Confirm the image once AMP is seen sending one live (#3-47.11).
    # Only the 400 for an unknown key is known; the web panel reads the image as a blob.
    async def get_analytics_skin(self, user_key: str) -> bytes:
        """Get a Minecraft player's skin image.

        |coro|

        Endpoint: ``GET /api/analytics/skins/{user_key}``

        Parameters
        ----------
        user_key : :class:`str`
            The player's key.

        Returns
        -------
        :class:`bytes`
            The image as it came.

        Raises
        ------
        AMPAPIRequestError
            If AMP doesn't know the key (400, ``"analytics.error.badAvatar"``).

        """
        return await self._request(method="GET", path=f"/api/analytics/skins/{user_key}", raw_bytes=True)

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
        parameters: dict[str, str] = self._without_none(mapping=filters)
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
        parameters: dict[str, Union[str, int]] = self._without_none(mapping=filters)
        return await self._request(method="GET", path="/api/analytics/users", parameters=parameters)
