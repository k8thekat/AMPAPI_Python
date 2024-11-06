from __future__ import annotations

import functools
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Union

from .base import Base
from .dataclass import ActionResult, BukkitPlugin, MCUser, OPList, OPWhitelist, RunningTask
from .enums import *

if TYPE_CHECKING:
    from collections.abc import Coroutine
    from typing import Concatenate

    from typing_extensions import ParamSpec, TypeVar

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
        Checks the `Base.Module` property and raises ConnectionError if the Instance is `Offline or Stopped`.

        Raises:
        ---
            RuntimeError: This API call is only available on ADS instances.
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

        Returns:
        ---
        bool:
            On success returns a Bool.
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/AcceptEULA")
        return result

    @mc_only
    async def mc_add_op_entry(self, user_or_uuid: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Add an entry to the OP list.

        Args:
        ---
            user_or_uuid (str): Minecraft UUID or Username.

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
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

        Args:
        ---
            user_or_uuid (str): Minecraft UUID or Username.

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        parameters: dict[str, str] = {"UserOrUUID": user_or_uuid}
        result: Any = await self._call_api(
            api="MinecraftModule/AddToWhitelist", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @mc_only
    async def mc_buk_get_categories(self) -> list[dict[str, Any]]:
        """
        Get Bukkit categories.

        Returns:
        ---
            list[dict[str, Any]]: Returns a list of dictionaries containing plugin categories.\n

        ### CATEGORIES:
        {'id': 2, 'name': 'Bungee - Spigot'}
        {'id': 3, 'name': 'Bungee - Proxy'}
        {'id': 4, 'name': 'Spigot'}
        {'id': 5, 'name': 'Transportation'}
        {'id': 6, 'name': 'Chat'}
        {'id': 7, 'name': 'Tools and Utilities'}
        {'id': 8, 'name': 'Misc'}
        {'id': 9, 'name': 'Libraries / APIs'}
        {'id': 10, 'name': 'Transportation'}
        {'id': 11, 'name': 'Chat'}
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/BukGetCategories")
        return result

    @mc_only
    async def mc_buk_get_installed_plugins(self, format_data: Union[bool, None] = None) -> list[BukkitPlugin]:
        """
        Get Bukkit installed plugins.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[BukkitPlugin]: On success returns a list of BukkitPlugin dataclasses.
            * See `types.py -> BukkitPlugin`
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

        Args:
        ---
            plugin_id (int): The plugin ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            RunningTask: On success returns a RunningTask dataclass.
            * See `types.py -> RunningTask`
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


        Args:
        ---
            plugin_id (int): The plugin ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            Any: UNK data returned by the API.
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

        Args:
        ---
            category_id (str): Plugin category ID. See -> `mc_buk_get_categories()`
            page_number (int): Page Number. Default: 1
            page_size (int): Page Size. Default: 10
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)


        Returns:
        ---
            list[BukkitPlugin]: On success returns a list of BukkitPlugin dataclasses.
            * See `types.py -> BukkitPlugin`
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

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[BukkitPlugin]: Returns a list of BukkitPlugin dataclasses.
            * See `types.py -> BukkitPlugin`
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

        Args:
        ---
            plugin_id (int): The plugin ID.

        Returns:
        ---
            None: ""
        """

        await self._connect()
        parameters: dict[str, int] = {"PluginId": plugin_id}
        await self._call_api(api="MinecraftModule/BukGetRemovePlugin", parameters=parameters)
        return

    @mc_only
    async def mc_buk_get_search(
        self, query: str, page_number: int = 0, page_size: int = 10, format_data: Union[bool, None] = None
    ) -> list[BukkitPlugin]:
        """
        Search for Bukkit plugins.

        Args:
        ---
            Query (str): Search string.
            PageNumber (int): Page number. Defaults to 0.
            PageSize (int): Page size. Defaults to 10.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[BukkitPlugin]: On success returns a list of BukkitPlugin dataclasses.
            * See `types.py -> BukkitPlugin`
        """

        await self._connect()
        parameters: dict[str, Any] = {"Query": query, "PageNumber": page_number, "PageSize": page_size}
        result: Any = await self._call_api(
            api="MinecraftModule/BukGetSearch", parameters=parameters, format_data=format_data, format_=BukkitPlugin
        )
        return result

    @mc_only
    async def mc_ban_user_by_id(self, id_: str) -> None:
        """
        Ban the specified Minecraft UUID.

        Args:
        ---
            id_ (str): Minecraft UUID.

        Returns:
        ---
            None: ""
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": id_}
        await self._call_api(api="MinecraftModule/BanUserByID", parameters=parameters)
        return

    @mc_only
    async def mc_clear_inventory_by_id(self, id_: str) -> None:
        """
        Clear a players inventory.

        Args:
        ---
            id_ (str): Minecraft UUID.

        Returns:
        ---
            None
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": id_}
        await self._call_api(api="MinecraftModule/ClearInventoryByID", parameters=parameters)
        return

    @mc_only
    async def mc_get_failure_reason(self) -> str:
        """
        Get the failure reason.

        Returns:
        ---
            str: On success returns a string representation of the failure reason.
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/GetFailureReason")
        return result

    @mc_only
    async def mc_get_head_by_uuid(self, id_: str) -> str:
        """
        Get a skin as a base64 string.

        Args:
        ---
            id_ (str): Minecraft UUID.

        Returns:
        ---
            str: base64 string. eg. (data:image/gif;base64, data)
        """

        await self._connect()
        parameters: dict[str, str] = {"id": id_}
        result: Any = await self._call_api(api="MinecraftModule/GetHeadByUUID", parameters=parameters)
        return result

    @mc_only
    async def mc_get_op_whitelist(self, format_data: Union[bool, None] = None) -> OPWhitelist:
        """
        Get the OP whitelist.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            OPWhitelist: On success returns an OPWhitelist dataclass.
            * See `types.py -> OPWhitelist`
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

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[Whitelist]: Returns a list of strings containing Minecraft UUIDs.
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/GetWhitelist", format_data=format_data, format_=MCUser)
        return result

    @mc_only
    async def mc_kick_user_by_id(self, id_: str) -> None:
        """
        Kick the specified User ID.

        Args:
        ---
            id_ (str): Minecraft UUID.

        Returns:
        ---
            None

        """

        await self._connect()
        parameters: dict[str, str] = {"ID": id_}
        await self._call_api(api="MinecraftModule/KickUserByID", parameters=parameters)
        return

    @mc_only
    async def mc_kill_by_id(self, id_: str) -> None:
        """
        Kill the Minecraft player.

        Args:
        ---
            id_ (str): Minecraft UUID.

        Returns:
        ----
            None
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": id_}
        await self._call_api(api="MinecraftModule/KillByID", parameters=parameters)
        return

    @mc_only
    async def mc_load_op_list(self, format_data: Union[bool, None] = None) -> list[OPList]:
        """
        Get the OP list.

        Returns:
        ---
            list[OPList]: On success returns a list of OPList dataclasses.
            * See `types.py -> OPList`
        """

        await self._connect()
        result: Any = await self._call_api(api="MinecraftModule/LoadOPList", format_data=format_data, format_=OPList)
        return result

    @mc_only
    async def mc_remove_op_entry(self, user_or_uuid: str) -> None:
        """
        Remove an entry from the OP list.

        Args:
        ---
            user_or_uuid (str): Minecraft UUID or Username.
        """

        await self._connect()
        parameters: dict[str, str] = {"UserOrUUID": user_or_uuid}
        await self._call_api(api="MinecraftModule/RemoveOPEntry", parameters=parameters)
        return

    @mc_only
    async def mc_remove_whitelist_entry(self, user_or_uuid: str) -> None:
        """
        Remove a user from the whitelist.

        Args:
        ---
            user_or_uuid (str): Minecraft UUID or Username.
        """

        await self._connect()
        parameters: dict[str, str] = {"UserOrUUID": user_or_uuid}
        await self._call_api(api="MinecraftModule/RemoveWhitelistEntry", parameters=parameters)
        return

    @mc_only
    async def mc_smite_by_id(self, id_: str) -> None:
        """
        Strike a player with lightning

        Args:
        ---
            id_ (str): Minecraft UUID.
        """

        await self._connect()
        parameters: dict[str, str] = {"ID": id_}
        await self._call_api(api="MinecraftModule/SmiteByID", parameters=parameters)
        return
