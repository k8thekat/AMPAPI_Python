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
from typing import TYPE_CHECKING, Optional, Union

from .base import Base

if TYPE_CHECKING:
    from ._types import (
        AnalyticsAddressSearchResponse,
        AnalyticsAddressUsersResponse,
        AnalyticsConnectedResponse,
        AnalyticsForgetResponse,
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

    Players are keyed by a `userKey` (see :meth:`get_analytics_users`). A shard only keeps names, countries, addresses
    and profiles for its players with its `userSpecificData` setting on; without it a player has a key and sessions
    only. Most calls take `demo`, which the web panel uses for a demo mode. The audit log is :class:`AuditModule`.

    .. versionadded:: 6.0.0

    """

    async def delete_analytics_user_sessions(self, user_key: str, *, demo: bool = False) -> AnalyticsForgetResponse:
        """Erase everything the analytics hold about one player.

        |coro|

        Endpoint: ``DELETE /api/analytics/sessions/users/{user_key}``

        The player's own record reads empty straight after, but :meth:`get_analytics_sessions`' summary still listed
        them about 11 minutes later on AMP 3.0.0.6.

        Parameters
        ----------
        user_key : :class:`str`
            The player's key.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        :class:`AnalyticsForgetResponse`
            How many records, over how many days, were erased; 0 and 0 when there was nothing.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `user_key` isn't a player key AMP would make `analytics.error.badUserKey`.

        """
        return await self._request(method="DELETE", path=f"/api/analytics/sessions/users/{user_key}", parameters={"demo": demo})

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
        return await self._request(method="GET", path="/api/analytics/addresses/users", parameters={"address": address, "demo": demo})

    # TODO: Reword the warning once AMP answers a range search (#3-54).
    # AMP 3.0.0.6 answers 500 for every range, from an error in its address service.
    async def get_analytics_addresses(self, search: str, *, demo: bool = False) -> AnalyticsAddressSearchResponse:
        """Search the addresses players were seen at.

        |coro|

        Endpoint: ``GET /api/analytics/addresses``

        .. warning::
            AMP 3.0.0.6 answers a range (eg. ``"203.0.113.0/24"``, ``"203.0.113."`` or ``"198.51.*"``) with a 500, so
            only a whole address works for now.

        Parameters
        ----------
        search : :class:`str`
            The address to look for, IPv4 or IPv6, a whole address only.
        demo : :class:`bool`, optional
            If the call is for the demo data or not, by default False.

        Returns
        -------
        :class:`AnalyticsAddressSearchResponse`
            The address, if it's private or public, and the matching addresses and their players.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `search` is a bare fragment such as ``"192"`` `analytics.error.badAddress`.\n
            **500** - If `search` is a range, eg. ``"203.0.113.0/24"``, see the warning above.

        """
        return await self._request(method="GET", path="/api/analytics/addresses", parameters={"q": search, "demo": demo})

    async def get_analytics_avatar(self, avatar_hash: str, *, full: bool = False) -> bytes:
        """Get a Steam player's avatar image.

        |coro|

        Endpoint: ``GET /api/analytics/avatars/{avatar_hash}``

        Parameters
        ----------
        avatar_hash : :class:`str`
            The avatar's hash, 40 lower-case hex digits, which AMP's docs place in the player's Steam profile from
            :meth:`get_analytics_profiles`. It isn't the player's key.
        full : :class:`bool`, optional
            If AMP should send the full size image or not, by default False.

        Returns
        -------
        :class:`bytes`
            The image, a JPEG.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `avatar_hash` isn't 40 hex digits `analytics.error.badAvatar`.\n
            **404** - If Steam has no avatar with that hash.

        """
        return await self._request(method="GET", path=f"/api/analytics/avatars/{avatar_hash}", parameters={"full": full}, raw_bytes=True)

    async def get_analytics_connected_users(self, shard_id: str, user: str) -> AnalyticsConnectedResponse:
        """Get what a shard knows about one player connected to it now.

        |coro|

        Endpoint: ``GET /api/analytics/connected/{shard_id}``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard the player is on.
        user : :class:`str`
            The player's `id` as :meth:`ShardModule.get_shard_users` gives it. Their name isn't taken.

        Returns
        -------
        :class:`AnalyticsConnectedResponse`
            The player as the shard lists them, their profile and their analytics key.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the player isn't connected to the shard `analytics.error.notConnected`.\n
            **404** - If `user` is the player's name rather than their `id` `analytics.error.notConnected`.

        """
        return await self._request(method="GET", path=f"/api/analytics/connected/{shard_id}", parameters={"user": user})

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
        return await self._request(method="GET", path="/api/analytics/profiles", parameters={"key": user_keys, "demo": demo})

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
        filters: dict[str, Optional[Union[bool, str, int, list[str]]]] = {
            "from": from_time,
            "to": to_time,
            "shard": shard_ids,
            "country": country,
            "user": user,
            "topUsers": top_users,
            "demo": demo,
        }

        # We only send the filters that are set, as the web panel does.
        parameters: dict[str, Union[bool, str, int, list[str]]] = self._without_none(mapping=filters)

        return await self._request(method="GET", path="/api/analytics/sessions", parameters=parameters)

    async def get_analytics_skin(self, texture_hash: str) -> bytes:
        """Get a Minecraft player's skin image.

        |coro|

        Endpoint: ``GET /api/analytics/skins/{texture_hash}``

        Parameters
        ----------
        texture_hash : :class:`str`
            The `skinHash` from the player's Minecraft profile in :meth:`get_analytics_profiles`, 64 hex digits. It
            isn't the player's key.

        Returns
        -------
        :class:`bytes`
            The image, a PNG.

        Raises
        ------
        AMPAPIRequestError
            **404** - If AMP has no skin for the hash.

        """
        return await self._request(method="GET", path=f"/api/analytics/skins/{texture_hash}", raw_bytes=True)

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
        return await self._request(method="GET", path=f"/api/analytics/users/{user_key}/addresses", parameters={"demo": demo})

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
        filters: dict[str, Optional[Union[bool, str]]] = {"from": from_time, "to": to_time, "demo": demo}
        parameters: dict[str, Union[bool, str]] = self._without_none(mapping=filters)
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
        filters: dict[str, Optional[Union[bool, str, int]]] = {"q": search, "limit": limit, "demo": demo}
        parameters: dict[str, Union[bool, str, int]] = self._without_none(mapping=filters)
        return await self._request(method="GET", path="/api/analytics/users", parameters=parameters)
