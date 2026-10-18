from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, Optional, Union, Unpack

from typing_extensions import deprecated

from ._types import (
    ACTION_RESULT_EXCLUDED_KEYS,
    ACTION_RESULT_REQUIRED_KEYS,
    OP_WHITELIST_EXCLUDED_KEYS,
    OP_WHITELIST_REQUIRED_KEYS,
    ActionResultResponse,
    OPWhitelistResponse,
    is_response_type,
)
from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPITypeError
from .modules import ActionResult, BukkitPlugin, MCUser, OPList, OPWhitelist, RunningTask

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Concatenate

    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]
    from typing_extensions import ParamSpec, TypeVar

    from ._types import BukkitCategories, RunningTaskResponse

    D = TypeVar("D", bound="Base")
    T = ParamSpec("T")
    F = TypeVar("F")

__all__ = ("MinecraftModule",)


class MinecraftModule(Base):
    """Contains all Endpoints for `/API/MinecraftModule/`."""

    @staticmethod
    def mc_only(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """Checks the :attr:`~Base.module` property and raises ConnectionError if the Instance is ``Offline or Stopped``.

        Raises
        ------
        :exc:`RuntimeError`
            This API call is only available on ADS instances.

        """

        @functools.wraps(wrapped=func)
        def wrapper_mc_only(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            if self.module == "Minecraft":
                return func(self, *args, **kwargs)
            raise RuntimeError(self._minecraft_only)

        return wrapper_mc_only

    @mc_only
    async def mc_accept_eula(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> bool:
        """|coro|

        Accept the EULA summary.

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`bool`
            On success returns a Bool.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/AcceptEULA",
            request_params=request_params,
            **response_params,
        )
        if isinstance(result, bool):
            return result
        raise AMPAPITypeError(end_point="MinecraftModule/AcceptEULA", cur_type=result, expec_type=bool)

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_add_op_entry(
        self,
        user_or_uuid: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Add an entry to the OP list.

        Parameters
        ----------
        user_or_uuid : :class:`str`
            The Minecraft UUID or Username.
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
        parameters: dict[str, str] = {"UserOrUUID": user_or_uuid}
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/AddOPEntry",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="MinecraftModule/AddOPEntry", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="MinecraftModule/AddOPEntry", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult(**result)
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_add_to_whitelist(
        self,
        user_or_uuid: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Add a user to the whitelist.

        Parameters
        ----------
        user_or_uuid : :class:`str`
            The Minecraft UUID or Username.
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
        parameters: dict[str, str] = {"UserOrUUID": user_or_uuid}
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/AddToWhitelist",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="MinecraftModule/AddToWhitelist", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="MinecraftModule/AddToWhitelist", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult(**result)
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_buk_get_categories(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[BukkitCategories]:
        """|coro|

        Get Bukkit categories.

        .. note::
            CATEGORIES: 'Bungee - Spigot', 'Bungee - Proxy', 'Spigot', 'Transportation', 'Chat', 'Tools and Utilities', 'Misc', 'Libraries / APIs'


        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`BukkitCategories`]
            On success returns a list of :class:`BukkitCategories` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/BukGetCategories",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="MinecraftModule/BukGetCategories", cur_type=result, expec_type=list)
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_buk_get_installed_plugins(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[BukkitPlugin] | list[dict[str, Any]]:
        """|coro|

        Get Bukkit installed plugins.

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
        list[:class:`BukkitPlugin`]
            On success returns a list of :class:`BukkitPlugin` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/BukGetInstalledPlugins",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="MinecraftModule/BukGetInstalledPlugins", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [BukkitPlugin(**item) for item in result]
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_buk_get_install_update_plugin(
        self,
        plugin_id: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Get update for Bukkit plugin.

        Parameters
        ----------
        plugin_id : :class:`int`
            The plugin ID. See :class:`BukkitPlugin` for the ID value.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        parameters: dict[str, int] = {"pluginId": plugin_id}
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/BukGetInstallUpdatePlugin",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="MinecraftModule/BukGetInstallUpdatePlugin", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if "is_primary_task" not in result:
            raise AMPAPITypeError(end_point="MinecraftModule/BukGetInstallUpdatePlugin", cur_type=result, expec_type=dict)
        if format_data is True:
            return RunningTask(**result)
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_buk_get_plugin_info(
        self,
        plugin_id: int,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Any:
        """|coro|

        Get Bukkit plugin info.


        Parameters
        ----------
        plugin_id : :class:`int`
            The plugin ID. See :class:`BukkitPlugin` for the ID value.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Any
            UNK data returned by the API.

        """
        await self._reauth()
        parameters: dict[str, int] = {"PluginId": plugin_id}
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/BukGetPluginInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_buk_get_plugins_for_category(
        self,
        category_id: str,
        page_number: int = 1,
        page_size: int = 10,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[BukkitPlugin] | list[dict[str, Any]]:
        """|coro|

        Get Bukkit plugins from category.

        Parameters
        ----------
        category_id : :class:`str`
            The plugin category ID. See -> :meth:`mc_buk_get_categories`
        page_number : :class:`int`
            The page number, default is 1.
        page_size : :class:`int`
            The number of entries per page, default is 10.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.


        Returns
        -------
        list[:class:`BukkitPlugin`]
            On success returns a list of :class:`BukkitPlugin` dataclasses.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"CategoryId": category_id, "PageNumber": page_number, "PageSize": page_size}
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/BukGetPluginsForCategory",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="MinecraftModule/BukGetPluginsForCategory", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [BukkitPlugin(**item) for item in result]
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_buk_get_popular_plugins(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[BukkitPlugin] | list[dict[str, Any]]:
        """|coro|

        Get Bukkit popular plugins.

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
        list[:class:`BukkitPlugin`]
            On success returns a list of :class:`BukkitPlugin` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/BukGetPopularPlugins",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="MinecraftModule/BukGetPopularPlugins", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [BukkitPlugin(**item) for item in result]
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_buk_get_remove_plugin(
        self,
        plugin_id: int,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Remove Bukkit plugin.

        Parameters
        ----------
        plugin_id : :class:`int`
            The plugin ID. See :class:`BukkitPlugin` for the ID value.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, int] = {"PluginId": plugin_id}
        return await self._post(
            url="MinecraftModule/BukGetRemovePlugin",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_buk_get_search(
        self,
        query: str,
        page_number: int = 0,
        page_size: int = 10,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[BukkitPlugin] | list[dict[str, Any]]:
        """|coro|

        Search for Bukkit plugins.

        Parameters
        ----------
        query : :class:`str`
            The search query.
        page_number : :class:`int`
            The page number, default is 1.
        page_size : :class:`int`
            The number of entries per page, default is 10.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`BukkitPlugin`]
            On success returns a list of :class:`BukkitPlugin` dataclasses.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"Query": query, "PageNumber": page_number, "PageSize": page_size}
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/BukGetSearch",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="MinecraftModule/BukGetSearch", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [BukkitPlugin(**item) for item in result]
        return result

    @mc_only
    async def mc_ban_user_by_id(
        self,
        user_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Ban the specified Minecraft UUID.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        ----------
        user_id : :class:`str`
            The Minecraft Users UUID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"ID": user_id}
        return await self._post(
            url="MinecraftModule/BanUserByID",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @mc_only
    async def mc_clear_inventory_by_id(
        self,
        user_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Clear a players inventory.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        ----------
        user_id : :class:`str`
            The Minecraft Users UUID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"ID": user_id}
        return await self._post(
            url="MinecraftModule/ClearInventoryByID",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @mc_only
    async def mc_get_failure_reason(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> str:
        """|coro|

        Get the Server failure reason, if any.

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`str`
            On success returns a string representation of the failure reason.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/GetFailureReason",
            request_params=request_params,
            **response_params,
        )
        if isinstance(result, str):
            return result
        raise AMPAPITypeError(end_point="MinecraftModule/GetFailureReason", cur_type=result, expec_type=str)

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_get_head_by_uuid(
        self,
        user_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> str:
        """|coro|

        Get a skin as a base64 string.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        ----------
        user_id : :class:`str`
            The Minecraft Users UUID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`str`
            :class:`base64` string. eg. (data:image/gif;base64, data)

        """
        await self._reauth()
        parameters: dict[str, str] = {"id": user_id}
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/GetHeadByUUID",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if isinstance(result, str):
            return result
        raise AMPAPITypeError(end_point="MinecraftModule/GetHeadByUUID", cur_type=result, expec_type=str)

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_get_op_whitelist(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> OPWhitelist | OPWhitelistResponse:
        """|coro|

        Get the OP whitelist.

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
        :class:`OPWhitelist`
            On success returns a :class:`OPWhitelist` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/GetOPWhitelist",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="MinecraftModule/GetOPWhitelist", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, OPWhitelistResponse, OP_WHITELIST_REQUIRED_KEYS, OP_WHITELIST_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="MinecraftModule/GetOPWhitelist", cur_type=result, expec_type=dict)
        if format_data is True:
            return OPWhitelist(**result)
        return result

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_get_whitelist(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[MCUser] | list[dict[str, Any]]:
        """|coro|

        Get the whitelist.

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
        list[:class:`MCUser`]
            On success returns a list of :class:`MCUser` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/GetWhitelist",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="MinecraftModule/GetWhitelist", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [MCUser(**item) for item in result]
        return result

    @mc_only
    async def mc_kick_user_by_id(
        self,
        user_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Kick the specified Minecraft Users UUID.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        ----------
        user_id : :class:`str`
            The Minecraft Users UUID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"ID": user_id}
        return await self._post(
            url="MinecraftModule/KickUserByID",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @mc_only
    async def mc_kill_by_id(
        self,
        user_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Kill the Minecraft player.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        ----------
        user_id : :class:`str`
            The Minecraft Users UUID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"ID": user_id}
        return await self._post(
            url="MinecraftModule/KillByID",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_load_op_list(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[OPList] | list[dict[str, Any]]:
        """|coro|

        Get the OP list.

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
        list[:class:`OPList`]
            On success returns a list of :class:`OPList` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="MinecraftModule/LoadOPList",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="MinecraftModule/LoadOPList", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [OPList(**item) for item in result]
        return result

    @mc_only
    async def mc_reject_eula(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Reject the EULA agreement.

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
            url="MinecraftModule/RejectEULA",
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_remove_op_entry(
        self,
        user: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Remove an entry from the OP list.

        .. note::
            You can supply a Minecraft UUID (non-trimmed) or Username.


        Parameters
        ----------
        user : :class:`str`
            The Minecraft UUID or Username.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        """
        await self._reauth()
        parameters: dict[str, str] = {"UserOrUUID": user}
        return await self._post(
            url="MinecraftModule/RemoveOPEntry",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    # TODO: Removed in AMP API 2.6.5.0
    @deprecated("Removed in AMP API 2.6.5.0")
    @mc_only
    async def mc_remove_whitelist_entry(
        self,
        user: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Remove a user from the whitelist.

        .. note::
            You can supply a Minecraft UUID (non-trimmed) or Username.


        Parameters
        ----------
        user : :class:`str`
            The Minecraft UUID or Username.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        """
        await self._reauth()
        parameters: dict[str, str] = {"UserOrUUID": user}
        return await self._post(
            url="MinecraftModule/RemoveWhitelistEntry",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @mc_only
    async def mc_smite_by_id(
        self,
        user_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Strike a player with lightning

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        ----------
        user_id : :class:`str`
            The Minecraft Users UUID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"ID": user_id}
        return await self._post(
            url="MinecraftModule/SmiteByID",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )
