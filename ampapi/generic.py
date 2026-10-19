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

from ._types import (
    ACTION_RESULT_EXCLUDED_KEYS,
    ACTION_RESULT_REQUIRED_KEYS,
    IMPORT_CONFIG_EXCLUDED_KEYS,
    IMPORT_CONFIG_REQUIRED_KEYS,
    ActionResultResponse,
    ImportConfigResponse,
    is_response_type,
)
from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPITypeError
from .modules import ActionResult, ImportConfig

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

__all__ = ("GenericModule",)


class GenericModule(Base):
    """Contains all Endpoints for `/API/GenericModule/`."""

    @Base.generic_only
    async def import_config(
        self,
        filename: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ImportConfig | ImportConfigResponse:
        """|coro|

        Imports the settings from a config file in the Instance's files, `GenericModule/ImportConfig`.

        Parameters
        ----------
        filename : :class:`str`
            The name of the config file to import.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ImportConfig`
            On success returns an :class:`ImportConfig` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"filename": filename}
        result: ResponseAliasFull = await self._post(
            url="GenericModule/ImportConfig",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="GenericModule/ImportConfig", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ImportConfigResponse, IMPORT_CONFIG_REQUIRED_KEYS, IMPORT_CONFIG_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="GenericModule/ImportConfig", cur_type=result, expec_type=dict)
        if format_data is True:
            return ImportConfig(**result)
        return result

    @Base.generic_only
    async def refresh_remote_options(
        self,
        field_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Refreshes the remote options of a setting field, `GenericModule/RefreshRemoteOptions`.

        Parameters
        ----------
        field_name : :class:`str`
            The name of the setting field to refresh.
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
        parameters: dict[str, str] = {"fieldName": field_name}
        result: ResponseAliasFull = await self._post(
            url="GenericModule/RefreshRemoteOptions",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="GenericModule/RefreshRemoteOptions", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="GenericModule/RefreshRemoteOptions", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult(**result)
        return result

    @Base.generic_only
    async def refresh_tool_discovery(
        self,
        field_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Refreshes the tool discovery of a setting field, `GenericModule/RefreshToolDiscovery`.

        Parameters
        ----------
        field_name : :class:`str`
            The name of the setting field to refresh.
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
        parameters: dict[str, str] = {"fieldName": field_name}
        result: ResponseAliasFull = await self._post(
            url="GenericModule/RefreshToolDiscovery",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="GenericModule/RefreshToolDiscovery", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="GenericModule/RefreshToolDiscovery", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult(**result)
        return result

    @Base.generic_only
    async def reload_generic_config(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Reloads the Generic config of the Instance, `GenericModule/ReloadGenericConfig`.

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
            url="GenericModule/ReloadGenericConfig",
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @Base.generic_only
    async def request_server_info(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Requests the server info from the Instance, `GenericModule/RequestServerInfo`.

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
            url="GenericModule/RequestServerInfo",
            no_data=True,
            request_params=request_params,
            **response_params,
        )
