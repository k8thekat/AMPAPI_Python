from __future__ import annotations

from typing import Any, Union

from .base import Base
from .types import *

__all__ = ("Core",)


class Core(Base):
    """
    Contains the base functions for any `/API/Core/` AMP API endpoints.

    """
    async def login(self, amp_user: str, amp_password: str, token: str = "", rememberME: bool = False, format_data: Union[bool, None] = None) -> LoginResults:
        """
        AMP API login function. \n

        Args:
            amp_user (str): The username for logging into the AMP Panel
            amp_password (str): The password for logging into the AMP Panel
            token (str, optional): AMP 2 Factor auth code; typically using `TOTP.now()`. Defaults to "".
            rememberME (bool, optional): Remember me token.. Defaults to False.

        Returns:
            LoginResults: On success returns a LoginResult dataclass.
                See `types.py -> LoginResult`
        """
        parameters = {
            'username': amp_user,
            'password': amp_password,
            'token': token,
            'rememberMe': rememberME}
        result = await self._call_api(api='Core/Login', parameters=parameters, format_data=format_data, format=LoginResults)
        return result

    # Core.Logout:({'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def logout(self) -> None:
        """
        Logout from AMP. 

        Returns:
            None
        """
        await self._connect()
        await self._call_api(api='Core/Logout')
        return

    async def get_api_spec(self) -> dict:
        """
        Get's all the API specs for the ADS or Instance.
         - See `docs/api_spec.md`

        Returns:
            dict: A dictionary containing all of the API specs, their parameters and return types for the ADS or Instance.
        """

        await self._connect()
        result = await self._call_api(api='Core/GetAPISpec')
        return result

    async def get_updates(self, format_data: Union[bool, None] = None) -> Updates:
        """
        Requests the recent entries of the Instance Updates; will acquire all updates from previous API call of `getUpdate()`

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Updates: On success returns a Updates dataclass.
                See `types.py -> Updates`
        """

        await self._connect()
        result = await self._call_api(api='Core/GetUpdates', format_data=format_data, format=Updates)
        return result

    async def send_console_message(self, msg: str) -> None:
        """
        Sends a string to the Console. (eg `/list`)

        Returns:
            None: ""
        """

        await self._connect()
        parameters = {'message': msg}
        await self._call_api(api='Core/SendConsoleMessage', parameters=parameters)
        return

    async def start_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Starts the AMP Server/Instance

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: Results from the API call.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api(api='Core/Start', format_data=format_data, format=ActionResult)
        return result

    async def stop_instance(self) -> None:
        """
        Stops the AMP Server/Instance

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api(api='Core/Stop')
        return

    async def restart_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Restarts the AMP Server/Instance

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: Results from the API call.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api(api='Core/Restart', format_data=format_data, format=ActionResult)
        return result

    async def kill_instance(self) -> None:
        """
        Kills the AMP Server/Instance

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api(api='Core/Kill')
        return

    # Core.Suspend:({'Description': "Prevents the current instance from being started, and stops it if it's currently running.", 'Returns': '', 'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def suspend_instance(self) -> None:
        """
        Prevents the current instance from being started, and stops it if it's currently running.

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api(api='Core/Suspend')
        return

    # Core.Resume:({'Description': 'Allows the service to be re-started after previously being suspended.', 'Returns': '', 'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def resume_instance(self) -> None:
        """
        Allows the service to be re-started after previously being suspended.

        Returns:
            None: ""
        """
        await self._connect()
        await self._call_api(api='Core/Resume')
        return

    async def get_status(self, format_data: Union[bool, None] = None) -> AppStatus:
        """
        Gets the AMP Server/Instance Status information.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Status: On success returns a Status dataclass.
                See `types.py -> Status`
        """

        await self._connect()
        result = await self._call_api(api='Core/GetStatus', format_data=format_data, format=AppStatus)
        return result

    async def get_user_list(self, format_data: Union[bool, None] = None) -> list[Players]:
        """
        Returns a dictionary of the connected Users to the Server.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Players: on success returns a Player dataclass.
                See `types.py -> list[Players]`
        """

        await self._connect()
        result = await self._call_api(api='Core/GetUserList', format_data=format_data, format=Players, _use_from_dict=False, _auto_unpack=False)
        return result

    async def get_schedule_data(self, format_data: Union[bool, None] = None) -> ScheduleData:
        """
        Returns a dictionary of the Server/Instance Schedule events and triggers.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ScheduleData: On success returns a ScheduleData dataclass.
                See `types.py -> ScheduleData`
        """

        await self._connect()
        result = await self._call_api(api='Core/GetScheduleData', format_data=format_data, format=ScheduleData)
        return result

    async def end_user_session(self, session_id: str) -> None:
        """
        Closes the specified User's session ID to AMP.\n
        **Requires ADS**

        Args:
            session_id (str): session ID to end.

        Returns:
            None: ""
        """
        if self.Module != "ADS":
            raise RuntimeError(self.ADS_ONLY)

        await self._connect()
        parameters = {
            'Id': session_id
        }
        await self._call_api(api='Core/EndUserSession', parameters=parameters)
        return

    async def get_active_amp_sessions(self, format_data: Union[bool, None] = None) -> list[Session]:
        """
        Returns currently active AMP Sessions.\n
        **Requires ADS**

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Session: Returns a dataclass Session.
                See `types.py -> Session`
        """

        if self.Module != "ADS":
            raise RuntimeError(self.ADS_ONLY)

        await self._connect()
        result = await self._call_api(api='Core/GetActiveAMPSessions', format_data=format_data, format=Session, _use_from_dict=False)
        return result

    async def get_amp_user_info(self, name: str, format_data: Union[bool, None] = None) -> User:
        """
        Retrieves the AMP User information for the provided username.\n

        Args:
            name (str): AMP User name.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            User: On success returns a User dataclass. 
                See `types.py -> User`
        """

        await self._connect()
        parameters = {
            'Username': name
        }
        result = await self._call_api(api='Core/GetAMPUserInfo', parameters=parameters, format_data=format_data, format=User, _use_from_dict=False)
        return result

    async def current_session_has_permission(self, permission_node: str) -> bool:
        """
        Retrieves the current Session IDs permissions. This will differ between the ADS and a Server/Instance.

        Args:
            permission_node (str): The permission node to check for. eg `Core.RoleManagement.DeleteRoles` \n
                - Supports looking for a blocked permission node simply by appending `-` in front of the permission node. eg `-Core.RoleManagement.DeleteRoles`\n
                - Supports wildcards `*`. eg `Core.RoleManagement.*`


        Returns:
            str | dict[str, Any] | list | bool | int | None: On success returns a bool.
        """

        await self._connect()
        parameters = {
            'PermissionNode': permission_node
        }
        result = await self._call_api(api='Core/CurrentSessionHasPermission', parameters=parameters)
        return result

    async def get_amp_role_permissions(self, role_id: str) -> list[Any]:
        """
        Retrieves the AMP Role permission nodes for the provided role ID.

        Args:
            role_id (str): The role ID. eg `5d6566e0-fae2-41d7-bfb6-d21033247f2e`

        Returns:
            list[Any]: On success returns a list containing all the permission nodes for the provided role ID.
        """

        await self._connect()
        parameters = {
            'RoleId': role_id
        }
        result = await self._call_api(api="Core/GetAMPRolePermissions", parameters=parameters)
        return result

    async def get_permissions_spec(self) -> dict[str, Any]:
        """
        Retrieves the AMP Permissions node tree.

        Returns:
            dict[str, Any]: On success returns a dictionary containing all the permission nodes, descriptions and other attributes.
        """

        await self._connect()
        result = await self._call_api(api="Core/GetPermissionsSpec")
        return result

    async def get_role_ids(self) -> dict[str, Any]:
        """
        Retrieves all the Roles AMP currently has and the role IDs.

        Returns:
            Roles: On success returns a dictionary containing all the roles and their IDs. \n
            *Example*
            `{'00000000-0000-0000-0000-000000000000': 'Default','cb984b09-a1c6-4cc0-b005-df8907f06590': 'Super Admins'}`
        """

        await self._connect()
        result = await self._call_api(api='Core/GetRoleIds')
        return result

    async def create_role(self, name: str, as_common_role: bool = False, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Creates an AMP Role.

        Args:
            name (str): The name of the role.
            as_common_role (bool, optional): A role that everyone has. Defaults to False.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`

        """

        await self._connect()
        parameters = {
            'Name': name,
            'AsCommonRole': as_common_role
        }
        result = await self._call_api(api='Core/CreateRole', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    async def get_role(self, role_id: str, format_data: Union[bool, None] = None) -> Role:
        """
        Retrieves the AMP Role information for the provided role ID.

        Args:
            role_id (str): The role ID to get information for.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Role: On success returns a Role dataclass.
                See `types.py -> Role`

        """

        await self._connect()
        parameters = {
            'RoleId': role_id
        }
        result = await self._call_api(api='Core/GetRole', parameters=parameters, format_data=format_data, format=Role)
        return result

    async def set_amp_user_role_membership(self, user_id: str, role_id: str, is_member: bool, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Adds a user to an AMP role.

        Args:
            user_id (str): User ID to add to the role.
            role_id (str): Role ID to add the user to.
            is_member (bool): `True` to add the user to the role, `False` to remove the user from the role.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'UserId': user_id,
            'RoleId': role_id,
            'IsMember': is_member
        }
        result = await self._call_api(api='Core/SetAMPUserRoleMembership', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    async def set_amp_role_permission(self, role_id: str, permission_node: str, enabled: Union[None, bool], format_data: Union[bool, None] = None) -> ActionResult:
        """
        Set a permission node to `True` or `False` for the provided AMP role.

        Args:
            role_id (str): AMP role id.
            permission_node (str): AMP permission node. eg `Core.RoleManagement.DeleteRoles`
            enabled (Union[None, bool]): Set a permission to `True`, `False` or `None` depending on the results you can disable or enable an entire tree node of permissions.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'RoleId': role_id,
            'PermissionNode': permission_node,
            'Enabled': enabled
        }
        result = await self._call_api(api='Core/SetAMPRolePermission', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    async def get_settings_spec(self) -> dict[str, Any]:
        """
        Retrieves a Server/Instance nodes list.
            - See `util.getNodespec` for a list of possible nodes.

        Returns:
            dict[str, Any]: On success returns a dictionary containing all of the Server/Instance nodes and there information.
        """

        await self._connect()
        result = await self._call_api(api='Core/GetSettingsSpec')
        return result

    async def get_config(self, node: str, format_data: Union[bool, None] = None) -> SettingSpec:
        """
        Returns the config settings for a specific node.\n

        Args:
            node (str): The AMP node to inspect eg `ADSModule.Networking.BaseURL`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Node: On success returns a dictionary containing the following. \n
        """

        await self._connect()
        parameters = {
            "node": node
        }
        result = await self._call_api(api="Core/GetConfig", parameters=parameters, format_data=format_data, format=SettingSpec)
        return result

    async def get_configs(self, nodes: list[str], format_data: Union[bool, None] = None) -> list[SettingSpec]:
        """
        Returns the config settings for each node in the list.\n

        Args:
            node (list[str]): List of nodes to look at.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Node]: On success returns a list of Node dataclasses.
                See `types.py -> Node`
        """

        await self._connect()
        parameters = {
            "nodes": nodes
        }
        result = await self._call_api(api="Core/GetConfigs", parameters=parameters, format_data=format_data, format=SettingSpec)
        return result

    async def get_update_info(self, format_data: Union[bool, None] = None) -> UpdateInfo:
        """
        Returns a data class `UpdateInfo` and `UpdateInfo.Build = AMP_Version` to access Version information for AMP.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            UpdateInfo: On success returns a UpdateInfo dataclass.
                See `types.py -> UpdateInfo`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetUpdateInfo", format_data=format_data, format=UpdateInfo)
        return result

    async def get_all_amp_user_info(self, format_data: Union[bool, None] = None) -> list[User]:
        """
        Represents all the AMP User info.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[User]: On success returns a list of User dataclasses.
                See `types.py -> User`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetAllAMPUserInfo", format_data=format_data, format=User, _use_from_dict=False)
        return result

    # Core.GetAuditLogEntries:({'Parameters': [{'Name': 'Before', 'TypeName': 'Nullable<DateTime>', 'Description': '', 'Optional': False}, {'Name': 'Count', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'IEnumerable<IAuditLogEntry>', 'IsComplexType': True})
    async def get_audit_log_entries(self, before: float, count: int, format_data: Union[bool, None] = None) -> list[AuditLogEntry]:
        """
        Returns the last X number of audit log entries.

        Args:
            before (float): A POSIX timestamp.
            count (int): Number of entries to return.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[AuditLogEntry]: On success returns a list of AuditLogEntry dataclasses.
                See `types.py -> AuditLogEntry`
        """

        await self._connect()
        parameters = {
            "Before": before,
            "Count": count
        }
        result = await self._call_api(api="Core/GetAuditLogEntries", parameters=parameters, format_data=format_data, format=AuditLogEntry, _use_from_dict=False)
        return result

    # Core.GetSettingsSpec:({'Parameters': [], 'ReturnTypeName': 'Dictionary<String, IEnumerable<JObject>>', 'IsComplexType': True})
    async def get_setting_spec(self, format_data: Union[bool, None] = None) -> list[SettingSpec]:
        """
        Returns a list of settings that can be changed.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[SettingSpec]: On success returns a list of Setting dataclasses.
                See `types.py -> Setting`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetSettingsSpec", format_data=format_data, format=SettingSpec)
        return result

    # Core.RefreshSettingValueList:({'Parameters': [{'Name': 'Node', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def refresh_setting_value_list(self, node: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Refreshes a setting's value list.

        Args:
            name (str): Setting name.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Name": node,
        }
        result = await self._call_api(api="Core/RefreshSettingValueList", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.RefreshSettingsSourceCache:({'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def refresh_settings_source_cache(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Refreshes the settings source cache.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api(api="Core/RefreshSettingsSourceCache", format_data=format_data, format=ActionResult)
        return result

    # Core.GetSettingValues:({'Parameters': [{'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'WithRefresh', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'IDictionary<String, String>', 'IsComplexType': False})
    async def get_setting_values(self, setting_node: str) -> dict[str, str]:
        """
        Returns the setting values.

        Args:
            name (str): Setting name.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            dict[str, str]: On success returns a dictionary of setting values.
        """

        await self._connect()
        parameters = {
            "SettingNode": setting_node
        }
        result = await self._call_api(api="Core/GetSettingValues", parameters=parameters)
        return result

    # Core.GetProvisionSpec:({'Parameters': [], 'ReturnTypeName': 'List<JObject>', 'IsComplexType': True})
    async def get_provision_spec(self, format_data: Union[bool, None] = None) -> list[SettingSpec]:
        """
        Returns the provisioning spec.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[SettingSpec]: On success returns a list of provisioning spec.
                See `types.py -> JObject`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetProvisionSpec", format_data=format_data, format=SettingSpec)
        return result

    # Core.SetConfigs:({'Parameters': [{'Name': 'data', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Boolean', 'IsComplexType': False})
    async def set_configs(self, data: dict[str, str], format_data: Union[bool, None] = None) -> bool:
        """
        Set's multiple config node values.

        Args:
            data (dict[str, str]): Dictionary of configs to set.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            bool: On success returns a boolean.
        """

        await self._connect()
        parameters = {
            "data": data
        }
        result = await self._call_api(api="Core/SetConfigs", parameters=parameters)
        return result

    # Core.SetConfig:({'Parameters': [{'Name': 'node', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'value', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def set_config(self, node: str, value: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Set a config node value.

        Args:
            name (str): Config node name.
            value (str): Config node value.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "node": node,
            "value": value
        }
        result = await self._call_api(api="Core/SetConfig", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.ActivateAMPLicence:({'Parameters': [{'Name': 'LicenceKey', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'QueryOnly', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult<JObject>', 'IsComplexType': True})
    async def activate_amp_license(self, license_key: str, query_only: bool = False, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Activates an AMP license key.

        Args:
            license_key (str): The license key to activate.
            query_only (bool, optional): Whether to query only. Defaults to False.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "LicenceKey": license_key,
            "QueryOnly": query_only
        }
        result = await self._call_api(api="Core/ActivateAMPLicence", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.GetRoleData:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<AuthRoleSummary>', 'IsComplexType': True})
    async def get_role_data(self, format_data: Union[bool, None] = None) -> list[Role]:
        """
        Get's a list of all the roles.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Role]: On success returns a list of Role dataclasses.
                See `types.py -> Role`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetRoleData", format_data=format_data, format=Role)
        return result

    # Core.DeleteRole:({'Parameters': [{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def delete_role(self, role_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Deletes a role.

        Args:
            role_id (str): The ID of the role to delete.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "RoleId": role_id
        }
        result = await self._call_api(api="Core/DeleteRole", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.RenameRole:({'Parameters': [{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'NewName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def rename_role(self, role_id: str, new_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Renames a role.

        Args:
            role_id (str): The ID of the role to rename.
            new_name (str): The new name for the role.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "RoleId": role_id,
            "NewName": new_name
        }
        result = await self._call_api(api="Core/RenameRole", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.AddEventTrigger:({'Parameters': [{'Name': 'triggerId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def add_event_trigger(self, trigger_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Adds an event trigger.

        Args:
            trigger_id (str): The ID of the event trigger to add.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TriggerId": trigger_id
        }
        result = await self._call_api(api="Core/AddEventTrigger", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.RunEventTriggerImmediately:({'Parameters': [{'Name': 'triggerId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def run_event_trigger_immediately(self, trigger_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Runs an event trigger immediately.

        Args:
            trigger_id (str): The ID of the event trigger to run.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TriggerId": trigger_id
        }
        result = await self._call_api(api="Core/RunEventTriggerImmediately", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.GetTimeIntervalTrigger:({'Parameters': [{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    async def get_time_interval_trigger(self, id: str, format_data: Union[bool, None] = None) -> TimedTrigger:
        """
        Gets a time interval trigger information.

        Args:
            id (str): The ID of the time interval trigger to get.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            JObject: On success returns a JObject dataclass.
                See `types.py -> JObject`
        """

        await self._connect()
        parameters = {
            "Id": id
        }
        result = await self._call_api(api="Core/GetTimeIntervalTrigger", parameters=parameters, format_data=format_data, format=TimedTrigger)
        return result

    # Core.EditIntervalTrigger:({'Parameters': [{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'months', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}, {'Name': 'days', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}, {'Name': 'hours', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}, {'Name': 'minutes', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}, {'Name': 'daysOfMonth', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}, {'Name': 'description', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def edit_interval_trigger(self, id: str, months: int, days: int, hours: int, minutes: int, days_of_month: int,
                                    description: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Edits an interval trigger.
        Args:
            id (str): The ID of the interval trigger to edit.
            months (int): The months of the interval trigger to edit.
            days (int): The days of the interval trigger to edit.
            hours (int): The hours of the interval trigger to edit.
            minutes (int): The minutes of the interval trigger to edit.
            days_of_month (int): The days of the month of the interval trigger to edit.
            description (str): The description of the interval trigger to edit.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Id": id,
            "months": months,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "daysOfMonth": days_of_month,
            "description": description
        }
        result = await self._call_api(api="Core/EditIntervalTrigger", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.SetTriggerEnabled:({'Parameters': [{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'Enabled', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def set_trigger_enabled(self, id: str, enabled: bool, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Sets the enabled state of a trigger.

        Args:
            id (str): The ID of the trigger to edit.
            enabled (bool): The enabled state of the trigger to edit.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Id": id,
            "Enabled": enabled
        }
        result = await self._call_api(api="Core/SetTriggerEnabled", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.AddTask:({'Parameters': [{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'MethodID', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'ParameterMapping', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def add_task(self, trigger_id: str, method_id: str, parameter_mapping: dict[str, str], format_data: Union[bool, None] = None) -> ActionResult:
        """
        Add a task.\n


        Args:
            trigger_id (str): The ID of the trigger to add.
            method_id (str): The Task Method Name. eg. `Event.MinecraftModule.SendGlobalTitle`
            parameter_mapping (dict[str, str]): The parameters to be populated related to the trigger_id/method_id.\n
                - Example: `{ "Subtitle": "Hello World", Title: "Hello {@UserID}" }`

            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TriggerID": trigger_id,
            "MethodID": method_id,
            "ParameterMapping": parameter_mapping
        }
        result = await self._call_api(api="Core/AddTask", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.EditTask:({'Parameters': [{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'ParameterMapping', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def edit_task(self, trigger_id: str, task_id: str, parameter_mapping: dict[str, str], format_data: Union[bool, None] = None) -> ActionResult:
        """
        Edit a task.

        Args:
            trigger_id (str): The ID of the trigger to edit.
            task_id (str): The ID of the task to edit. See `get_schedule_data().Tasks` to get IDs
            parameter_mapping (dict[str, str]): The parameters to be updated on the task.\n
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TriggerID": trigger_id,
            "TaskID": task_id,
            "ParameterMapping": parameter_mapping
        }
        result = await self._call_api(api="Core/EditTask", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.ChangeTaskOrder:({'Parameters': [{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'NewOrder', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def change_task_order(self, trigger_id: str, task_id: str, new_order: int, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Change the order of a task.

        Args:
            trigger_id (str): The ID of the trigger to modify.
            task_id (str): The ID of the task to modify. See `get_schedule_data().Tasks` to get IDs
            new_order (int): The new task position.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TriggerID": trigger_id,
            "TaskID": task_id,
            "NewOrder": new_order
        }
        result = await self._call_api(api="Core/ChangeTaskOrder", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.DeleteTask:({'Parameters': [{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def delete_task(self, trigger_id: str, task_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete a task.


        Args:
            trigger_id (_type_): The ID of the trigger to delete.
            task_id (str): The ID of the task to delete. See `get_schedule_data().Tasks` to get IDs
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TriggerID": trigger_id,
            "TaskID": task_id
        }
        result = await self._call_api(api="Core/DeleteTask", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.DeleteTrigger:({'Parameters': [{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def delete_trigger(self, trigger_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete a trigger.

        Args:
            trigger_id (str): The ID of the trigger to delete.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TriggerID": trigger_id
        }
        result = await self._call_api(api="Core/DeleteTrigger", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.GetAMPUsersSummary:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<UserInfoSummary>', 'IsComplexType': True})
    async def get_amp_users_summary(self, format_data: Union[bool, None] = None) -> list[Login_UserInfo]:
        """
        Get all AMP users summary.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[UserInfoSummary]: On success returns a list of UserInfoSummary dataclass.
                See `types.py -> UserInfoSummary`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetAMPUsersSummary", format_data=format_data, format=Login_UserInfo)
        return result

    # Core.CreateUser:({'Parameters': [{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult<Guid>', 'IsComplexType': True})
    async def create_user(self, username: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Create an AMP user.

        Args:
            username (str): Username.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = parameters = parameters = parameters = {
            "Username": username
        }
        result = await self._call_api(api="Core/CreateUser", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.DeleteUser:({'Parameters': [{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def delete_user(self, username: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete an AMP user.

        Args:
            username (str): Username.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Username": username
        }
        result = await self._call_api(api="Core/DeleteUser", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.UpdateUserInfo:({'Parameters': [{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False},
    # {'Name': 'Disabled', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}, {'Name': 'PasswordExpires', 'TypeName': 'Boolean', 'Description': '', 'Optional': False},
    # {'Name': 'CannotChangePassword', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}, {'Name': 'MustChangePassword', 'TypeName': 'Boolean', 'Description': '', 'Optional': False},
    # {'Name': 'EmailAddress', 'TypeName': 'String', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def update_user_info(self, user_name: str, disabled: bool = False, password_expires: bool = False, cannot_change_password: bool = False,
                               must_change_password: bool = False, email_address: str = "", format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update an AMP user.

        Args:
            user_name (str): Username.
            disabled (bool, optional): Disabled. Defaults to False.
            password_expires (bool, optional): User password expires. Defaults to False.
            cannot_change_password (bool, optional): User cannot change password. Defaults to False.
            must_change_password (bool, optional): User must change password upon next login. Defaults to False.
            email_address (str, optional): Email address. Defaults to "".
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Username": user_name,
            "Disabled": disabled,
            "PasswordExpires": password_expires,
            "CannotChangePassword": cannot_change_password,
            "MustChangePassword": must_change_password,
            "EmailAddress": email_address
        }
        result = await self._call_api(api="Core/UpdateUserInfo", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.GetWebauthnChallenge:({'Parameters': [], 'ReturnTypeName': 'ActionResult<String>', 'IsComplexType': True})
    async def get_webauthn_challenge(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Get a webauthn challenge.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetWebauthnChallenge", format_data=format_data, format=ActionResult)
        return result

    # Core.GetWebauthnCredentialIDs:({'Parameters': [{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    async def get_webauthn_credential_ids(self, username: str, format_data: Union[bool, None] = None) -> list[Any]:
        """
        Get a webauthn credential IDs.

        Args:
            username (str): Username.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "username": username
        }
        result = await self._call_api(api="Core/GetWebauthnCredentialIDs", parameters=parameters, format_data=format_data)
        return result

    # Core.WebauthnRegister:({'Parameters': [{'Name': 'attestationObject', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'clientDataJSON', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'description', 'TypeName': 'String', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def webauthn_register(self, attestation_object: str, client_data_json: str, description: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Webauthn register.

        Args:
            attestation_object (str): Attestation object.
            client_data_json (str): Client data JSON.
            description (str): Description.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "attestationObject": attestation_object,
            "clientDataJSON": client_data_json,
            "description": description
        }
        result = await self._call_api(api="Core/WebauthnRegister", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.GetWebauthnCredentialSummaries:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<WebauthnCredentialSummary>', 'IsComplexType': True})
    async def get_webauthn_credential_summary(self, format_data: Union[bool, None] = None) -> list[Any]:
        """
        Get the webauthn credential summaries.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Any] : List of webauthn credential summaries.
        """

        await self._connect()
        result = await self._call_api(api="Core/GetWebauthnCredentialSummaries", format_data=format_data)
        return result

    # Core.RevokeWebauthnCredential:({'Parameters': [{'Name': 'ID', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def revoke_webauthn_credential(self, id: int, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Revoke a webauthn credential.

        Args:
            id (int): ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "ID": id
        }
        result = await self._call_api(api="Core/RevokeWebauthnCredential", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.UpdateAccountInfo:({'Parameters': [{'Name': 'EmailAddress', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'TwoFactorPIN', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def update_account_info(self, email_address: str, two_factor_pin: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update account info.

        Args:
            email_address (str): Email address.
            two_factor_pin (str): Two factor PIN.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "EmailAddress": email_address,
            "TwoFactorPIN": two_factor_pin
        }
        result = await self._call_api(api="Core/UpdateAccountInfo", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.EnableTwoFactor:({'Description': 'Sets up two-factor authentication for the given user. ConfirmTwoFactorSetup must be invoked to complete setup.', 'Returns': 'Data container the URI for a QR code that should be scanned by a mobile authenticator.', 'Parameters': [{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Password', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult<TwoFactorSetupInfo>', 'IsComplexType': True})
    async def enable_two_factor(self, username: str, password: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Sets up two-factor authentication for the given user. \n 
        `**WARNING**` ConfirmTwoFactorSetup must be invoked to complete setup.

        Args:
            username (str): Username.
            password (str): Password.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an dictionary with the structure \n
            `{"Result" : {"ManualKey" : str, "Url" : str}, "Status": bool}`.
        """

        await self._connect()
        parameters = {
            "Username": username,
            "Password": password
        }
        result = await self._call_api(api="Core/EnableTwoFactor", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.ConfirmTwoFactorSetup:({'Description': 'Completes two-factor setup by supplying a valid two factor code based on the secret provided by EnableTwoFactor', 'Returns': '', 'Parameters': [{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'TwoFactorCode', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def confirm_two_factor_setup(self, username: str, two_factor_code: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Completes two-factor setup by supplying a valid two factor code based on the secret provided by EnableTwoFactor.

        Args:
            username (str): Username.
            two_factor_code (str): Two factor code.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Username": username,
            "TwoFactorCode": two_factor_code
        }
        result = await self._call_api(api="Core/ConfirmTwoFactorSetup", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.DisableTwoFactor:({'Parameters': [{'Name': 'Password', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'TwoFactorCode', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def disable_two_factor(self, password: str, two_factor_code: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Disables two-factor authentication for the given user.

        Args:
            password (str): Password.
            two_factor_code (str): Two factor code.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Password": password,
            "TwoFactorCode": two_factor_code
        }
        result = await self._call_api(api="Core/DisableTwoFactor", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.ResetUserPassword:({'Description': 'For administrative users to alter the password of another user', 'Returns': '', 'Parameters': [{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'NewPassword', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def reset_user_password(self, username: str, new_password: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        For administrative users to alter the password of another user.

        Args:
            username (str): Username.
            new_password (str): New password.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Username": username,
            "NewPassword": new_password
        }
        result = await self._call_api(api="Core/ResetUserPassword", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.DeleteInstanceUsers:({'Parameters': [{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def delete_instance_users(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete an Instances User list.

        Args:
            instance_id (str): The AMP Instance ID
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "InstanceId": instance_id
        }

        results = await self._call_api(api="Core/DeleteInstanceUsers", parameters=parameters, format_data=format_data, format=ActionResult)
        return results

    # Core.ChangeUserPassword:({'Description': 'For a user to change their own password, requires knowing the old password', 'Returns': '', 'Parameters': [{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'OldPassword', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'NewPassword', 'TypeName': 'String', 'Description': '', 'Optional': False},
    # {'Name': 'TwoFactorPIN', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def change_user_password(self, username: str, old_password: str, new_password: str, two_factor_pin: str = "", format_data: Union[bool, None] = None) -> ActionResult:
        """
        For a user to change their own password, requires knowing the old password.

        Args:
            username (str): AMP user name.
            old_password (str): Current AMP user password.
            new_password (str): New AMP user password.
            two_factor_pin (str): Two Factor PIN, if enabled. Defaults to "".
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Username": username,
            "OldPassword": old_password,
            "NewPassword": new_password,
            "TwoFactorPIN": two_factor_pin
        }

        results = await self._call_api(api="Core/ChangeUserPassword", parameters=parameters, format_data=format_data, format=ActionResult)
        return results

    # Core.GetNewGuid:({'Parameters': [], 'ReturnTypeName': 'Guid', 'IsComplexType': False})
    async def get_new_guid(self, format_data: Union[bool, None] = None) -> dict[str, Any]:
        """
        Get a new GUID.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a GUID.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetNewGuid", format_data=format_data)
        return result

    # Core.GetTasks:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<RunningTask>', 'IsComplexType': True})
    async def get_tasks(self, format_data: Union[bool, None] = None) -> list[RunningTask]:
        """
        Get all tasks.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[RunningTask]: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetTasks", format_data=format_data, format=RunningTask)
        return result

    # Core.GetPortSummaries:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<ListeningPortSummary>', 'IsComplexType': True})
    async def get_port_summaries(self, format_data: Union[bool, None] = None) -> list[Port]:
        """
        Get a summary of the instance's open ports.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Port]: On success returns a list of Port dataclass.
                See `types.py -> Port`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetPortSummaries", format_data=format_data, format=Port)
        if format_data is None:
            format_data = self.format_data

        if format_data == False:
            return result

        elif isinstance(result, list):
            return list(Port(**port) for port in result)
        return result

    # Core.CancelTask:({'Parameters': [{'Name': 'TaskId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def cancel_task(self, task_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Cancel a task.

        Args:
            task_id (str): _description_
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a GUID.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TaskId": task_id
        }
        result = await self._call_api(api="Core/CancelTask", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.DismissTask:({'Parameters': [{'Name': 'TaskId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def dismiss_task(self, task_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Dismiss a task notification.

        Args:
            task_id (str): _description_
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a GUID.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "TaskId": task_id
        }
        result = await self._call_api(api="Core/DismissTask", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # Core.DismissAllTasks:({'Parameters': [], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def dismiss_all_tasks(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Dismiss all task notifications.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a GUID.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api(api="Core/DismissAllTasks", format_data=format_data, format=ActionResult)
        return result

    # Core.GetUserInfo:({'Description': 'Provides information about a given in-application user (as opposed to AMP system users)', 'Returns': '', 'Parameters': [{'Name': 'UID', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'SimpleUser', 'IsComplexType': True})
    async def get_user_info(self, uid: str, format_data: Union[bool, None] = None) -> dict:
        """
        Provides information about a given in-application user (as opposed to AMP system users).

        Args:
            uid (str): _description_
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            dict: On success returns a dict.
        """

        await self._connect()
        parameters = {
            "UID": uid
        }
        result = await self._call_api(api="Core/GetUserInfo", parameters=parameters, format_data=format_data)
        return result

    # Core.UpdateApplication:({'Parameters': [], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def update_application(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update the Instance application.


        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a GUID.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api(api="Core/UpdateApplication", format_data=format_data, format=ActionResult)
        return result

    # Core.AcknowledgeAMPUpdate:({'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def acknowledge_amp_update(self) -> None:
        """
        Approves an AMP update.

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/AcknowledgeAMPUpdate")
        return

    # Core.GetModuleInfo:({'Parameters': [], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    async def get_module_info(self, format_data: Union[bool, None] = None) -> Module:
        """
        Returns the module information.


        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Module: On success returns a Module dataclass.
                See `types.py -> Module`
        """

        await self._connect()
        result = await self._call_api(api="Core/GetModuleInfo", format_data=format_data, format=Module)
        return result

    # Core.GetUserActionsSpec:({'Parameters': [], 'ReturnTypeName': 'Object', 'IsComplexType': False})
    async def get_user_action_spec(self, format_data: Union[bool, None] = None) -> dict[str, Any]:
        """
        Get a specification of the user actions.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            dict[str, Any]: On success returns a dict.\n
                - {'ADSModule': {},'CommonCorePlugin': {},'Core': {},'EmailSenderPlugin': {},'FileManagerPlugin': {},'LocalFileBackupPlugin': {}}
        """

        await self._connect()
        result = await self._call_api(api="Core/GetUserActionsSpec", format_data=format_data)
        return result

    # Core.GetRemoteLoginToken:({'Parameters': [{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': True}, {'Name': 'IsTemporary', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'String', 'IsComplexType': False})
    async def get_remote_login_token(self, description: Union[str, None] = None, is_temporary: Union[bool, None] = None, format_data: Union[bool, None] = None) -> str:
        """
        Get the remote login token.

        Args:
            description (Union[str, None], optional): Description. Defaults to None.
            is_temporary (Union[bool, None], optional): Is temporary. Defaults to None.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            str: On success returns a str.
                See `types.py -> str`
        """

        await self._connect()
        parameters = {
            "Description": description,
            "IsTemporary": is_temporary
        }
        result = await self._call_api(api="Core/GetRemoteLoginToken", parameters=parameters, format_data=format_data)
        return result

    # Core.UpdateAMPInstance:({'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def update_amp_instance(self) -> None:
        """
        update_amp_instance 

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/UpdateAMPInstance")
        return

    # Core.RestartAMP:({'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def restart_amp(self) -> None:
        """
        restart_amp 

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/RestartAMP")
        return

    # Core.UpgradeAMP:({'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def upgrade_amp(self) -> None:
        """
        upgrade_amp 

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/UpgradeAMP")
        return

    # Core.GetDiagnosticsInfo:({'Parameters': [], 'ReturnTypeName': 'Dictionary<String, String>', 'IsComplexType': False})
    async def get_diagnostics_info(self, format_data: Union[bool, None] = None) -> Diagnostics:
        """
        Get's the system diagnostics information.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Diagnostics: On success returns a dictionary.\n

        """

        await self._connect()
        result = await self._call_api(api="Core/GetDiagnosticsInfo", format_data=format_data, format=Diagnostics, _use_from_dict=False, _auto_unpack=False)
        return result

    # Core.GetWebserverMetrics:({'Parameters': [], 'ReturnTypeName': 'Object', 'IsComplexType': False})
    async def get_webserver_metrics(self, format_data: Union[bool, None] = None) -> Any:
        """
        Gets the webserver metrics.

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Any: UNK data returned by the API.
        """

        await self._connect()
        result = await self._call_api(api="Core/GetWebserverMetrics", format_data=format_data)
        return result

    # Core.CreateTestTask:({'Description': 'DEV: Creates a non-ending task with 50% progress for testing purposes', 'Returns': '', 'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def create_test_task(self) -> None:
        """
        **DEV**: Creates a non-ending task with 50% progress for testing purposes


        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/CreateTestTask")
        return

    # Core.AsyncTest:({'Description': 'DEV: Async test method', 'Returns': '', 'Parameters': [], 'ReturnTypeName': 'String', 'IsComplexType': False})
    async def async_test(self) -> str:
        """
        **DEV**: Async test method


        Returns:
            str: Returns a string.
        """

        await self._connect()
        result = await self._call_api(api="Core/AsyncTest")
        return result
