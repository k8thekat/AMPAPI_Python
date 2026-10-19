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

from typing import TYPE_CHECKING, Optional, Unpack

from .base import Base, ResponseHandlerOptions

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

__all__ = ("SteamCMDPlugin",)


# AMP names this module in lowercase (`steamcmdplugin`), so the URLs below are lowercase as well.
# `SteamCMDPlugin/...` fails with "No such module loaded".
class SteamCMDPlugin(Base):
    """Contains all Endpoints for `/API/steamcmdplugin/`."""

    async def cancel_steam_guard(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Cancels a pending Steam Guard login, `steamcmdplugin/CancelSteamGuard`.

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        return await self._post(
            url="steamcmdplugin/CancelSteamGuard",
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    async def steam_guard_code(
        self,
        code: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Sends the Steam Guard code to a pending Steam login, `steamcmdplugin/SteamGuardCode`.

        Parameters
        ----------
        code : :class:`str`
            The Steam Guard code.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"code": code}
        return await self._post(
            url="steamcmdplugin/SteamGuardCode",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    async def steam_username_password(
        self,
        username: str,
        password: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Sets the Steam username and password the Instance logs in with, `steamcmdplugin/SteamUsernamePassword`.

        Parameters
        ----------
        username : :class:`str`
            The Steam username.
        password : :class:`str`
            The Steam password.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"username": username, "password": password}
        return await self._post(
            url="steamcmdplugin/SteamUsernamePassword",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )
