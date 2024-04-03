from __future__ import annotations

from typing import Any, Union

from dataclass_wizard import fromdict

from .base import FORMAT_DATA, Base
from .types import *

__all__ = ("MinecraftModule",)


class MinecraftModule(Base):
    """
    Contains the base functions for any `/API/MinecraftModule/` AMP API endpoints.

    """

    # MinecraftModule.BukGetCategories: ({'Parameters': [], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def mc_buk_get_categories(self) -> list[dict[str, Any]]:
        """
        Get Bukkit categories.

        Returns:
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

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        result = await self._call_api(api='MinecraftModule/BukGetCategories')
        return result

    # MinecraftModule.BukGetPopularPlugins: ({'Parameters': [], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def mc_buk_get_popular_plugins(self, format_data: Union[bool, None] = None) -> list[BukkitPlugin]:
        """
        Get Bukkit popular plugins.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[BukkitPlugin]: Returns a list of BukkitPlugin dataclasses.
                See `types.py -> BukkitPlugin`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        result = await self._call_api(api='MinecraftModule/BukGetPopularPlugins', format_data=format_data, format=BukkitPlugin)
        return result

    # MinecraftModule.BukGetPluginsForCategory: ({'Parameters': [{'Name': 'CategoryId', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'PageNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'PageSize', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def mc_buk_get_plugins_for_category(self, category_id: str, page_number: int = 1, page_size: int = 10, format_data: Union[bool, None] = None) -> list[BukkitPlugin]:
        """
        Get Bukkit plugins from category.

        Args:
            category_id (str): Plugin category ID. See -> `mc_buk_get_categories()`
            page_number (int): Page Number. Default: 1
            page_size (int): Page Size. Default: 10
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)


        Returns:
            list[BukkitPlugin]: On success returns a list of BukkitPlugin dataclasses.
                See `types.py -> BukkitPlugin`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "CategoryId": category_id,
            "PageNumber": page_number,
            "PageSize": page_size
        }

        result = await self._call_api(api='MinecraftModule/BukGetPluginsForCategory', parameters=parameters, format_data=format_data, format=BukkitPlugin)
        return result

    # MinecraftModule.BukGetPluginInfo: ({'Parameters': [{'Name': 'PluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def mc_buk_get_plugin_info(self, plugin_id: int, format_data: Union[bool, None] = None) -> Any:
        """
        Get Bukkit plugin info.


        Args:
            plugin_id (int): The plugin ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Any: UNK data returned by the API.
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "PluginId": plugin_id
        }
        result = await self._call_api(api='MinecraftModule/BukGetPluginInfo', parameters=parameters, format_data=format_data)
        return result

    # MinecraftModule.BukGetInstalledPlugins: ({'Parameters': [], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def mc_buk_get_installed_plugins(self, format_data: Union[bool, None] = None) -> list[BukkitPlugin]:
        """
        Get Bukkit installed plugins.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)        

        Returns:
            list[BukkitPlugin]: On success returns a list of BukkitPlugin dataclasses.
                See `types.py -> BukkitPlugin`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        result = await self._call_api(api='MinecraftModule/BukGetInstalledPlugins', format_data=format_data, format=BukkitPlugin)
        return result

    # MinecraftModule.BukGetRemovePlugin: ({'Parameters': [{'Name': 'PluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def mc_buk_get_remove_plugin(self, plugin_id: int) -> None:
        """
        Remove Bukkit plugin.

        Args:
            plugin_id (int): The plugin ID.

        Returns:
            None: ""
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "PluginId": plugin_id
        }
        await self._call_api(api='MinecraftModule/BukGetRemovePlugin', parameters=parameters)
        return

    # MinecraftModule.BukGetInstallUpdatePlugin: ({'Parameters': [{'Name': 'pluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    async def mc_buk_get_install_update_plugin(self, plugin_id: int, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Get update for Bukkit plugin.

        Args:
            plugin_id (int): The plugin ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            RunningTask: On success returns a RunningTask dataclass.
                See `types.py -> RunningTask`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "pluginId": plugin_id
        }
        result = await self._call_api(api='MinecraftModule/BukGetInstallUpdatePlugin', parameters=parameters, format_data=format_data, format=RunningTask)
        return result

    # MinecraftModule.BukGetSearch: ({'Parameters': [{'Name': 'Query', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'PageNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'PageSize', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def mc_buk_get_search(self, query: str, page_number: int = 0, page_size: int = 10, format_data: Union[bool, None] = None) -> list[BukkitPlugin]:
        """
        Search for Bukkit plugins.

        Args:
            Query (str): Search string.
            PageNumber (int): Page number. Defaults to 0.
            PageSize (int): Page size. Defaults to 10.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[BukkitPlugin]: On success returns a list of BukkitPlugin dataclasses.
                See `types.py -> BukkitPlugin`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "Query": query,
            "PageNumber": page_number,
            "PageSize": page_size

        }
        result = await self._call_api(api='MinecraftModule/BukGetSearch', parameters=parameters, format_data=format_data, format=BukkitPlugin)
        return result

    # MinecraftModule.GetHeadByUUID: ({'Description': 'Get a skin as a base64 string', 'Returns': '', 'Parameters': [{'Name': 'id', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'String', 'IsComplexType': False})
    async def mc_get_head_by_uuid(self, id: str) -> str:
        """
        Get a skin as a base64 string.

        Args:
            id (str): Minecraft UUID.

        Returns:
            str: base64 string. eg. (data:image/gif;base64, data)
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "id": id
        }
        result = await self._call_api(api='MinecraftModule/GetHeadByUUID', parameters=parameters)
        return result

    # MinecraftModule.GetFailureReason: ({'Parameters': [], 'ReturnTypeName': 'String', 'IsComplexType': False})
    async def mc_get_failure_reason(self) -> str:
        """
        Get the failure reason.

        Returns:
            str: On success returns a string representation of the failure reason.
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        result = await self._call_api(api='MinecraftModule/GetFailureReason')
        return result

    # MinecraftModule.AcceptEULA: ({'Parameters': [], 'ReturnTypeName': 'Boolean', 'IsComplexType': False})
    async def mc_accept_eula(self) -> bool:
        """
        Accept the EULA summary.

        Returns:
            bool: On success returns a Bool.
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        result = await self._call_api(api='MinecraftModule/AcceptEULA')
        return result

    # MinecraftModule.BanUserByID: ({'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def mc_ban_user_by_id(self, id: str) -> None:
        """
        Ban the specified Minecraft UUID.

        Args:
            id (str): Minecraft UUID.

        Returns:
            None: ""
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "ID": id
        }
        await self._call_api(api='MinecraftModule/BanUserByID', parameters=parameters)
        return

    # MinecraftModule.KickUserByID: ({'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def mc_kick_user_by_id(self, id: str) -> None:
        """
        Kick the specified User ID.

        Args:
            id (str): Minecraft UUID.

        Returns:
            None

        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "ID": id
        }
        await self._call_api(api='MinecraftModule/KickUserByID', parameters=parameters)
        return

    # MinecraftModule.ClearInventoryByID: ({'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def mc_clear_inventory_by_id(self, id: str) -> None:
        """
        Clear a players inventory. 

        Args:
            id (str): Minecraft UUID.

        Returns:
            None
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "ID": id
        }
        await self._call_api(api='MinecraftModule/ClearInventoryByID', parameters=parameters)
        return

    # MinecraftModule.KillByID: ({'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def mc_kill_by_id(self, id: str) -> None:
        """
        Kill the Minecraft player.

        Args:
            id (str): Minecraft UUID.

        Returns:
            None
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "ID": id
        }
        await self._call_api(api='MinecraftModule/KillByID', parameters=parameters)
        return

    # MinecraftModule.SmiteByID: ({'Description': 'Strike a player with lightning', 'Returns': '', 'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def mc_smite_by_id(self, id: str) -> None:
        """
        Strike a player with lightning

        Args:
            id (str): Minecraft UUID.
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "ID": id
        }
        await self._call_api(api='MinecraftModule/SmiteByID', parameters=parameters)
        return

    # MinecraftModule.GetOPWhitelist: ({'Parameters': [], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    async def mc_get_op_whitelist(self, format_data: Union[bool, None] = None) -> OPWhitelist:
        """
        Get the OP whitelist.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            OPWhitelist: On success returns an OPWhitelist dataclass.
                See `types.py -> OPWhitelist`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        result = await self._call_api(api='MinecraftModule/GetOPWhitelist', format_data=format_data, format=OPWhitelist)
        return result

    # MinecraftModule.GetWhitelist: ({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    async def mc_get_whitelist(self, format_data: Union[bool, None] = None) -> list[MCUser]:
        """
        Get the whitelist.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Whitelist]: Returns a list of strings containing Minecraft UUIDs.
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        result = await self._call_api(api='MinecraftModule/GetWhitelist', format_data=format_data, format=MCUser)
        return result

    # MinecraftModule.LoadOPList: ({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    async def mc_load_op_list(self, format_data: Union[bool, None] = None) -> list[OPList]:
        """
        Get the OP list.

        Returns:
            list[OPList]: On success returns a list of OPList dataclasses.
                See `types.py -> OPList`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        result = await self._call_api(api='MinecraftModule/LoadOPList', format_data=format_data, format=OPList)
        return result

    # MinecraftModule.AddOPEntry: ({'Parameters': [{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def mc_add_op_entry(self, user_or_uuid: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Add an entry to the OP list.

        Args:
            user_or_uuid (str): Minecraft UUID or Username.

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "UserOrUUID": user_or_uuid
        }

        result = await self._call_api(api='MinecraftModule/AddOPEntry', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # MinecraftModule.RemoveOPEntry: ({'Parameters': [{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def mc_remove_op_entry(self, user_or_uuid: str) -> None:
        """
        Remove an entry from the OP list.

        Args:
            user_or_uuid (str): Minecraft UUID or Username.
        """
        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "UserOrUUID": user_or_uuid
        }
        await self._call_api(api='MinecraftModule/RemoveOPEntry', parameters=parameters)
        return

    # MinecraftModule.AddToWhitelist: ({'Parameters': [{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def mc_add_to_whitelist(self, user_or_uuid: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Add a user to the whitelist.

        Args:
            user_or_uuid (str): Minecraft UUID or Username.

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "UserOrUUID": user_or_uuid
        }
        result = await self._call_api(api='MinecraftModule/AddToWhitelist', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # MinecraftModule.RemoveWhitelistEntry: ({'Parameters': [{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def mc_remove_whitelist_entry(self, user_or_uuid: str) -> None:
        """
        Remove a user from the whitelist.

        Args:
            user_or_uuid (str): Minecraft UUID or Username.
        """
        if self.Module != "Minecraft":
            raise RuntimeError(self.MINECRAFT_ONLY)

        await self._connect()
        parameters = {
            "UserOrUUID": user_or_uuid
        }
        await self._call_api(api='MinecraftModule/RemoveWhitelistEntry', parameters=parameters)
        return
