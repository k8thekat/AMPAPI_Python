from __future__ import annotations
from typing import Any, Union
from dataclass_wizard import fromdict
from .types import *
from .base import Base


class MinecraftModule(Base):
    """
    Contains the base functions for any `/API/MinecraftModule/` AMP API endpoints.

    """

    # MinecraftModule.BukGetCategories: ({'Parameters': [], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def buk_get_categories(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get Bukkit categories.
        #TODO - What does it return.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        result = await self._call_api('MinecraftModule/BukGetCategories')
        return result

    # MinecraftModule.BukGetPopularPlugins: ({'Parameters': [], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def buk_get_popular_plugins(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get Bukkit popular plugins.
        #TODO - What does it return.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        result = await self._call_api('MinecraftModule/BukGetPopularPlugins')
        return result

    # MinecraftModule.BukGetPluginsForCategory: ({'Parameters': [{'Name': 'CategoryId', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'PageNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'PageSize', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def buk_get_plugins_for_category(self, CategoryId: str, PageNumber: int, PageSize: int) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get Bukkit plugins from category.
        #TODO - What does it return.

        Args:
            CategoryId (str): Plugin category ID.
            PageNumber (int): Page Number
            PageSize (int): Page Size


        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        parameters = {
            "CategoryId": CategoryId,
            "PageNumber": PageNumber,
            "PageSize": PageSize
        }
        result = await self._call_api('MinecraftModule/BukGetPluginsForCategory', parameters)
        return result

    # MinecraftModule.BukGetPluginInfo: ({'Parameters': [{'Name': 'PluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def buk_get_plugin_info(self, PluginId: int) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get Bukkit plugin info.

        Args:
            PluginId (int): The plugin ID.
        #TODO - What does it return.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        parameters = {
            "PluginId": PluginId
        }
        result = await self._call_api('MinecraftModule/BukGetPluginInfo', parameters)
        return result

    # MinecraftModule.BukGetInstalledPlugins: ({'Parameters': [], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def buk_get_installed_plugins(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get Bukkit installed plugins.
        #TODO - What does it return.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        result = await self._call_api('MinecraftModule/BukGetInstalledPlugins')
        return result

    # MinecraftModule.BukGetRemovePlugin: ({'Parameters': [{'Name': 'PluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def buk_get_remove_plugin(self, PluginId: int) -> None:
        """
        Remove Bukkit plugin.
        #TODO - What does it return.

        Args:
            PluginId (int): The plugin ID.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        parameters = {
            "PluginId": PluginId
        }
        await self._call_api('MinecraftModule/BukGetRemovePlugin', parameters)
        return

    # MinecraftModule.BukGetInstallUpdatePlugin: ({'Parameters': [{'Name': 'pluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    async def buk_get_install_update_plugin(self, PluginId: int) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get update for Bukkit plugin.
        #TODO - What does it return.

        Args:
            PluginId (int): The plugin ID.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        parameters = {
            "pluginId": PluginId
        }
        result = await self._call_api('MinecraftModule/BukGetInstallUpdatePlugin', parameters)
        return result

    # MinecraftModule.BukGetSearch: ({'Parameters': [{'Name': 'Query', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'PageNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'PageSize', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    async def buk_get_search(self, Query: str, PageNumber: int, PageSize: int) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Search for Bukkit plugins.
        #TODO - What does it return.

        Args:
            Query (str): Search string.
            PageNumber (int): Page number.
            PageSize (int): Page size.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        parameters = {
            "Query": Query,
            "PageNumer": PageNumber,
            "PageSize": PageSize

        }
        result = await self._call_api('MinecraftModule/BukGetSearch', parameters)
        return result

    # MinecraftModule.GetHeadByUUID: ({'Description': 'Get a skin as a base64 string', 'Returns': '', 'Parameters': [{'Name': 'id', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'String', 'IsComplexType': False})
    async def get_head_by_uuid(self, id: str):
        """
        Get a skin as a base64 string.
        #TODO - What does it return.

        Args:
            id (str): Minecraft UUID.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        parameters = {
            "id": id
        }
        result = await self._call_api('MinecraftModule/GetHeadByUUID', parameters)
        return result

    # MinecraftModule.GetFailureReason: ({'Parameters': [], 'ReturnTypeName': 'String', 'IsComplexType': False})
    async def get_failure_reason(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        UNKNOWN
        #TODO - What does it return.

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """
        result = await self._call_api('MinecraftModule/GetFailureReason')
        return result

    # MinecraftModule.AcceptEULA: ({'Parameters': [], 'ReturnTypeName': 'Boolean', 'IsComplexType': False})
    async def accept_eula(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Accept the EULA summary.
        #TODO - Need to be Validated

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: On success returns a Bool.
        """
        result = await self._call_api('MinecraftModule/AcceptEULA')
        return result

    # MinecraftModule.BanUserByID: ({'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def ban_user_by_id(self, ID: str) -> None:
        """
        Ban the specified Minecraft UUID.

        Args:
            ID (str): Minecraft UUID.

        Returns:
            None
        """
        parameters = {
            "ID": ID
        }
        await self._call_api('MinecraftModule/BanUserByID', parameters)
        return

    # MinecraftModule.KickUserByID: ({'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def kick_user_by_id(self, ID: str) -> None:
        """
        Kick the specified User ID.

        Args:
            ID (str): Minecraft UUID.

        Returns:
            None

        """
        parameters = {
            "ID": ID
        }
        await self._call_api('MinecraftModule/KickUserByID', parameters)
        return

    # MinecraftModule.ClearInventoryByID: ({'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def clear_inventory_by_id(self, ID: str) -> None:
        """
        Clear a players inventory. 
        #TODO - Need to be Validated

        Args:
            ID (str): Minecraft UUID.

        Returns:
            None
        """
        parameters = {
            "ID": ID
        }
        await self._call_api('MinecraftModule/ClearInventoryByID', parameters)
        return

    # MinecraftModule.KillByID: ({'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def kill_by_id(self, ID: str) -> None:
        """
        kill_by_id _summary_

        Args:
            ID (str): Minecraft UUID.

        Returns:
            None
        """
        parameters = {
            "ID": ID
        }
        await self._call_api('MinecraftModule/KillByID', parameters)
        return

    # MinecraftModule.SmiteByID: ({'Description': 'Strike a player with lightning', 'Returns': '', 'Parameters': [{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def smite_by_id(self, ID: str) -> None:
        """
        Strike a player with lightning

        Args:
            ID (str): Minecraft UUID.
        """
        parameters = {
            "ID": ID
        }
        await self._call_api('MinecraftModule/SmiteByID', parameters)
        return

    # MinecraftModule.GetOPWhitelist: ({'Parameters': [], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    async def get_op_whitelist(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get the OP whitelist.
        #TODO - See what it returns. (create dataclass)

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: 
        """

        result = await self._call_api('MinecraftModule/GetOPWhitelist')
        return result

    # MinecraftModule.GetWhitelist: ({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    async def get_whitelist(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get the whitelist.
        #TODO - See what it returns (create dataclass)

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: _description_
        """

        result = await self._call_api('MinecraftModule/GetWhitelist')
        return result

    # MinecraftModule.LoadOPList: ({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    async def load_op_list(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get the OP list.
        #TODO - See what it reutrns (create dataclass)

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: _description_
        """

        result = await self._call_api('MinecraftModule/LoadOPList')
        return result

    # MinecraftModule.AddOPEntry: ({'Parameters': [{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def add_op_entry(self, UserOrUUID: str) -> ActionResult | None | str | bool | dict[str, Any] | list[Any]:
        """
        Add an entry to the OP list.

        Args:
            UserOrUUID (str): Minecraft UUID or Username.

        Returns:
            ActionResult | None | str | bool | dict[str, Any] | list[Any]: On success returns an ActionResult dataclass.
        """
        parameters = {
            "UserOrUUID": UserOrUUID
        }

        result = await self._call_api('MinecraftModule/AddOPEntry', parameters)
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    # MinecraftModule.RemoveOPEntry: ({'Parameters': [{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def remove_op_entry(self, UserOrUUID: str) -> None:
        """
        Remove an entry from the OP list.

        Args:
            UserOrUUID (str): Minecraft UUID or Username.
        """
        parameters = {
            "UserOrUUID": UserOrUUID
        }
        await self._call_api('MinecraftModule/RemoveOPEntry', parameters)
        return

    # MinecraftModule.AddToWhitelist: ({'Parameters': [{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def add_to_whitelist(self, UserOrUUID: str) -> ActionResult | None | str | bool | dict[str, Any] | list[Any]:
        """
        Add a user to the whitelist.

        Args:
            UserOrUUID (str): Minecraft UUID or Username.

        Returns:
            ActionResult | None | str | bool | dict[str, Any] | list[Any]: On success returns an ActionResult dataclass.
        """
        parameters = {
            "UserOrUUID": UserOrUUID
        }
        result = await self._call_api('MinecraftModule/AddToWhitelist', parameters)
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    # MinecraftModule.RemoveWhitelistEntry: ({'Parameters': [{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def remove_whitelist_entry(self, UserOrUUID: str) -> None:
        """
        Remove a user from the whitelist.

        Args:
            UserOrUUID (str): Minecraft UUID or Username.
        """
        parameters = {
            "UserOrUUID": UserOrUUID
        }
        await self._call_api('MinecraftModule/RemoveWhitelistEntry', parameters)
        return
