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

from typing import TYPE_CHECKING, Optional, Union, Unpack

from ._types import ACTION_RESULT_EXCLUDED_KEYS, ACTION_RESULT_REQUIRED_KEYS, ActionResultResponse, is_response_type
from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPITypeError
from .modules import ActionResult, build

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

__all__ = ("EmailSenderPlugin",)


class EmailSenderPlugin(Base):
    """Contains the functions for any ``/API/EmailSenderPlugin/`` API endpoints."""

    async def test_SMTP_settings(  # noqa: N802 # Mirrors the AMP `TestSMTPSettings` endpoint name, renaming it would break the public API.
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Test SMTP Settings.

        Endpoint: `EmailSenderPlugin/TestSMTPSettings`

        .. note::
            This is a development endpoint.

        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="EmailSenderPlugin/TestSMTPSettings",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="EmailSenderPlugin/TestSMTPSettings", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="EmailSenderPlugin/TestSMTPSettings", cur_type=result, expec_type=dict)
        if format_data is True:
            return build(ActionResult, result)
        return result
