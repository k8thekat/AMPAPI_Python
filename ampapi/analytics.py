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

from dataclasses import asdict
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Optional, Union, Unpack

from ._types import ANALYTICS_SUMMARY_EXCLUDED_KEYS, ANALYTICS_SUMMARY_REQUIRED_KEYS, AnalyticsSummaryResponse, is_response_type
from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPITypeError
from .modules import AnalyticsFilter, AnalyticsSummary

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

__all__ = ("AnalyticsPlugin",)


class AnalyticsPlugin(Base):
    """Contains the base functions for any `/API/AnalyticsPlugin/` AMP API endpoints.

    .. note::
        If the ``format_data`` parameter is None on any function; the global ``FORMAT_DATA`` will be used instead.


    """

    async def get_analytics_summary(
        self,
        period_days: int = 30,
        start_date: Optional[datetime] = None,
        filters: Union[AnalyticsFilter, None] = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> AnalyticsSummary | AnalyticsSummaryResponse:
        """|coro|

        Retrieves the Analytics data for the Instance. \n
        See data such as how many people are playing, how long they've been playing, and where they are from.

        Endpoint: `AnalyticsPlugin/GetAnalyticsSummary`

        Parameters
        ----------
        period_days : :class:`int`, optional
            How far back in days to go, by default 30.
        start_date : :class:`datetime` | None, optional
            The date to start from, by default None which uses :meth:`~datetime.datetime.now`.
        filters : Union[:class:`AnalyticsFilter`, None], optional
            Filters results based upon the supplied dataclass values. See :class:`AnalyticsFilter`, by default None.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`AnalyticsSummary`
            On success returns an :class:`AnalyticsSummary` dataclass.

        """
        await self._reauth()
        if start_date is None:
            start_date = datetime.now(tz=UTC)

        parameters: dict[str, Any] = {
            "PeriodDays": period_days,
            "StartDate": start_date.timestamp(),
            "Filters": asdict(filters) if filters is not None else {},
        }
        result: ResponseAliasFull = await self._post(
            url="AnalyticsPlugin/GetAnalyticsSummary",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="AnalyticsPlugin/GetAnalyticsSummary", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, AnalyticsSummaryResponse, ANALYTICS_SUMMARY_REQUIRED_KEYS, ANALYTICS_SUMMARY_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="AnalyticsPlugin/GetAnalyticsSummary", cur_type=result, expec_type=dict)
        if format_data is True:
            return AnalyticsSummary(**result)
        return result

    async def get_user_details(
        self,
        username: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[dict[str, Any], None]:
        """|coro|

        Retrieves the Analytics details of a user.

        Endpoint: `AnalyticsPlugin/GetUserDetails`

        .. note::
            Requires the ``Analytics.Analytics.AccessUserDetails`` permission.


        .. note::
            AMP answers with JSON null when it has no data for the player. This method returns None for that,
            through the `allow_null` response option. Every other error is raised as normal.


        Parameters
        ----------
        username : :class:`str`
            The user name to retrieve the details of.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Union[dict[:class:`str`, Any], None]
            On success returns the raw dictionary of the user's details, or None when AMP has no data for the player.

        """
        await self._reauth()
        # AMP answers JSON null when it has no data for the player, which is not an error here.
        response_params["allow_null"] = True
        parameters: dict[str, str] = {"Username": username}
        result: ResponseAliasFull = await self._post(
            url="AnalyticsPlugin/GetUserDetails",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if result is None:
            return None

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="AnalyticsPlugin/GetUserDetails", cur_type=result, expec_type=dict)
        # TODO: Confirm the shape of the response with a player who has played.
        # AMP answers null when the player has no data, so no TypedDict until the keys are seen.
        return result  # pyright: ignore[reportReturnType]
