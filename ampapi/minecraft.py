from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, Union

from .base import Base
from .dataclass import ActionResult, BukkitPlugin, MCUser, OPList, OPWhitelist, RunningTask


if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Concatenate

    from typing_extensions import ParamSpec, TypeVar

    from .types_ import BukkitCategories

    D = TypeVar("D", bound="Base")
    T = ParamSpec("T")
    F = TypeVar("F")

__all__ = ("MinecraftModule",)


class MinecraftModule(Base):
    """
    Contains all Endpoints for `/API/MinecraftModule/`.

    """

    @staticmethod
    def mc_only(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """
        Checks the :attr:`~Base.module` property and raises ConnectionError if the Instance is ``Offline or Stopped``.

        Raises
        -------
        :exc:`RuntimeError`
            This API call is only available on ADS instances.
        """

        @functools.wraps(wrapped=func)
        def wrapper_mc_only(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            if self.module == "Minecraft":
                return func(self, *args, **kwargs)
            else:
                raise RuntimeError(self._minecraft_only)

        return wrapper_mc_only

    @mc_only
    async def mc_accept_eula(self) -> bool:
        """
        Accept the EULA summary.

        Returns
        -------
        :class:`bool`
            On success returns a Bool.
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/AcceptEULA")
        return result

    @mc_only
    async def mc_add_op_entry(self, user_or_uuid: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Add an entry to the OP list.

        Parameters
        -----------
        user_or_uuid: :class:`str`
            The Minecraft UUID or Username.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"UserOrUUID": user_or_uuid}

        result = await self._call_api(
            api="MinecraftModule/AddOPEntry", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @mc_only
    async def mc_add_to_whitelist(self, user_or_uuid: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Add a user to the whitelist.

        Parameters
        -----------
        user_or_uuid: :class:`str`
            The Minecraft UUID or Username.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"UserOrUUID": user_or_uuid}
        result: Any = await self._call_api(
            api="MinecraftModule/AddToWhitelist", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @mc_only
    async def mc_buk_get_categories(self) -> list[BukkitCategories]:
        """
        Get Bukkit categories.

        .. note::
            CATEGORIES: 'Bungee - Spigot', 'Bungee - Proxy', 'Spigot', 'Transportation', 'Chat', 'Tools and Utilities', 'Misc', 'Libraries / APIs'


        Returns
        --------
        list[:class:`BukkitCategories`]
            On success returns a list of :class:`BukkitCategories` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/BukGetCategories")
        return result

    @mc_only
    async def mc_buk_get_installed_plugins(self, format_data: Union[bool, None] = None) -> list[BukkitPlugin]:
        """
        Get Bukkit installed plugins.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`BukkitPlugin`]
            On success returns a list of :class:`BukkitPlugin` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="MinecraftModule/BukGetInstalledPlugins", format_data=format_data, format_=BukkitPlugin
        )
        return result

    @mc_only
    async def mc_buk_get_install_update_plugin(self, plugin_id: int, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Get update for Bukkit plugin.

        Parameters
        -----------
        plugin_id: :class:`int`
            The plugin ID. See :class:`BukkitPlugin` for the ID value.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.
        """

        await self._connect()
        parameters: dict[str, int] = {"pluginId": plugin_id}
        result: Any = await self._call_api(
            api="MinecraftModule/BukGetInstallUpdatePlugin",
            parameters=parameters,
            format_data=format_data,
            format_=RunningTask,
        )
        return result

    @mc_only
    async def mc_buk_get_plugin_info(self, plugin_id: int, format_data: Union[bool, None] = None) -> Any:
        """
        Get Bukkit plugin info.


        Parameters
        -----------
        plugin_id: :class:`int`
            The plugin ID. See :class:`BukkitPlugin` for the ID value.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        Any
            UNK data returned by the API.
        """

        await self._connect()
        parameters: dict[str, int] = {"PluginId": plugin_id}
        result: Any = await self._call_api(
            api="MinecraftModule/BukGetPluginInfo", parameters=parameters, format_data=format_data
        )
        return result

    @mc_only
    async def mc_buk_get_plugins_for_category(
        self, category_id: str, page_number: int = 1, page_size: int = 10, format_data: Union[bool, None] = None
    ) -> list[BukkitPlugin]:
        """
        Get Bukkit plugins from category.

        Parameters
        -----------
        category_id: :class:`str`
            The plugin category ID. See -> :meth:`mc_buk_get_categories`
        page_number: :class:`int`
            The page number, default is 1.
        page_size: :class:`int`
            The number of entries per page, default is 10.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.


        Returns
        --------
        list[:class:`BukkitPlugin`]
            On success returns a list of :class:`BukkitPlugin` dataclasses.
        """

        await self._connect()
        parameters: dict[str, Any] = {"CategoryId": category_id, "PageNumber": page_number, "PageSize": page_size}

        result: Any = await self._call_api(
            api="MinecraftModule/BukGetPluginsForCategory",
            parameters=parameters,
            format_data=format_data,
            format_=BukkitPlugin,
        )
        return result

    @mc_only
    async def mc_buk_get_popular_plugins(self, format_data: Union[bool, None] = None) -> list[BukkitPlugin]:
        """
        Get Bukkit popular plugins.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`BukkitPlugin`]
            On success returns a list of :class:`BukkitPlugin` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="MinecraftModule/BukGetPopularPlugins", format_data=format_data, format_=BukkitPlugin
        )
        return result

    @mc_only
    async def mc_buk_get_remove_plugin(self, plugin_id: int) -> None:
        """
        Remove Bukkit plugin.

        Parameters
        -----------
        plugin_id: :class:`int`
            The plugin ID. See :class:`BukkitPlugin` for the ID value.

        Returns
        -------
        None
        """

        await self._connect()
        parameters: dict[str, int] = {"PluginId": plugin_id}
        await self._call_api(api="MinecraftModule/BukGetRemovePlugin", parameters=parameters, _no_data=True)
        return

    @mc_only
    async def mc_buk_get_search(
        self, query: str, page_number: int = 0, page_size: int = 10, format_data: Union[bool, None] = None
    ) -> list[BukkitPlugin]:
        """
        Search for Bukkit plugins.

        Parameters
        -----------
        query: :class:`str`
            The search query.
        page_number: :class:`int`
            The page number, default is 1.
        page_size: :class:`int`
            The number of entries per page, default is 10.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`BukkitPlugin`]
            On success returns a list of :class:`BukkitPlugin` dataclasses.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Query": query, "PageNumber": page_number, "PageSize": page_size}
        result: Any = await self._call_api(
            api="MinecraftModule/BukGetSearch", parameters=parameters, format_data=format_data, format_=BukkitPlugin
        )
        return result

    @mc_only
    async def mc_ban_user_by_id(self, user_id: str) -> None:
        """
        Ban the specified Minecraft UUID.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        -----------
        user_id: :class:`str`
            The Minecraft Users UUID.

        Returns
        --------
        None
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": user_id}
        await self._call_api(api="MinecraftModule/BanUserByID", parameters=parameters, _no_data=True)
        return

    @mc_only
    async def mc_clear_inventory_by_id(self, user_id: str) -> None:
        """
        Clear a players inventory.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        -----------
        user_id: :class:`str`
            The Minecraft Users UUID.

        Returns
        --------
        None
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": user_id}
        await self._call_api(api="MinecraftModule/ClearInventoryByID", parameters=parameters, _no_data=True)
        return

    @mc_only
    async def mc_get_failure_reason(self) -> str:
        """
        Get the Server failure reason, if any.

        Returns
        --------
        :class:`str`
            On success returns a string representation of the failure reason.
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/GetFailureReason")
        return result

    @mc_only
    async def mc_get_head_by_uuid(self, user_id: str) -> str:
        """
        Get a skin as a base64 string.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        -----------
        user_id: :class:`str`
            The Minecraft Users UUID.

        Returns
        --------
        :class:`str`
            :class:`base64` string. eg. (data:image/gif;base64, data)
        """

        await self._connect()
        parameters: dict[str, str] = {"id": user_id}
        result: Any = await self._call_api(api="MinecraftModule/GetHeadByUUID", parameters=parameters)
        return result

    @mc_only
    async def mc_get_op_whitelist(self, format_data: Union[bool, None] = None) -> OPWhitelist:
        """
        Get the OP whitelist.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`OPWhitelist`
            On success returns a :class:`OPWhitelist` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="MinecraftModule/GetOPWhitelist", format_data=format_data, format_=OPWhitelist
        )
        return result

    @mc_only
    async def mc_get_whitelist(self, format_data: Union[bool, None] = None) -> list[MCUser]:
        """
        Get the whitelist.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
        list[:class:`MCUser`]
            On success returns a list of :class:`MCUser` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/GetWhitelist", format_data=format_data, format_=MCUser)
        return result

    @mc_only
    async def mc_kick_user_by_id(self, user_id: str) -> None:
        """
        Kick the specified Minecraft Users UUID.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        -----------
        user_id: :class:`str`
            The Minecraft Users UUID.

        Returns
        --------
        None
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": user_id}
        await self._call_api(api="MinecraftModule/KickUserByID", parameters=parameters, _no_data=True)
        return

    @mc_only
    async def mc_kill_by_id(self, user_id: str) -> None:
        """
        Kill the Minecraft player.

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        -----------
        user_id: :class:`str`
            The Minecraft Users UUID.

        Returns
        --------
        None
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": user_id}
        await self._call_api(api="MinecraftModule/KillByID", parameters=parameters, _no_data=True)
        return

    @mc_only
    async def mc_load_op_list(self, format_data: Union[bool, None] = None) -> list[OPList]:
        """
        Get the OP list.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`OPList`]
            On success returns a list of :class:`OPList` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/LoadOPList", format_data=format_data, format_=OPList)
        return result

    @mc_only
    async def mc_remove_op_entry(self, user: str) -> None:
        """
        Remove an entry from the OP list.

        .. note::
            You can supply a Minecraft UUID (non-trimmed) or Username.


        Parameters
        -----------
        user: :class:`str`
            The Minecraft UUID or Username.
        """

        await self._connect()
        parameters: dict[str, str] = {"UserOrUUID": user}
        await self._call_api(api="MinecraftModule/RemoveOPEntry", parameters=parameters, _no_data=True)
        return

    @mc_only
    async def mc_remove_whitelist_entry(self, user: str) -> None:
        """
        Remove a user from the whitelist.

        .. note::
            You can supply a Minecraft UUID (non-trimmed) or Username.


        Parameters
        -----------
        user: :class:`str`
            The Minecraft UUID or Username.
        """

        await self._connect()
        parameters: dict[str, str] = {"UserOrUUID": user}
        await self._call_api(api="MinecraftModule/RemoveWhitelistEntry", parameters=parameters, _no_data=True)
        return

    @mc_only
    async def mc_smite_by_id(self, user_id: str) -> None:
        """
        Strike a player with lightning

        .. note::
            This requires the full UUID of the user with the ``-`` chars included.


        Parameters
        -----------
        user_id: :class:`str`
            The Minecraft Users UUID.

        Returns
        --------
        None
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": user_id}
        await self._call_api(api="MinecraftModule/SmiteByID", parameters=parameters, _no_data=True)
        return
