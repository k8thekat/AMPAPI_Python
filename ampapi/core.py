from __future__ import annotations
from typing import Any, Union
from dataclass_wizard import fromdict
from .types import *
from .base import Base

__all__ = ("Core",)


class Core(Base):
    """
    Contains the base functions for any `/API/Core/` AMP API endpoints.

    """
    async def login(self, amp_user: str, amp_password: str, token: str = "", rememberME: bool = False) -> LoginResults | str | dict[str, Any] | list | bool | int | None:
        """
        AMP API login function. \n

        Args:
            amp_user (str): The username for logging into the AMP Panel
            amp_password (str): The password for logging into the AMP Panel
            token (str, optional): AMP 2 Factor auth code; typically using `TOTP.now()`. Defaults to "".
            rememberME (bool, optional): Remember me token.. Defaults to False.

        Returns:
            LoginResults | str | dict[str, Any] | list | bool | int | None: On success returns a LoginResult dataclass.
                See `types.py -> LoginResult`
        """
        parameters = {
            'username': amp_user,
            'password': amp_password,
            'token': token,
            'rememberMe': rememberME}
        result = await self._call_api('Core/Login', parameters)
        if isinstance(result, dict):
            return fromdict(LoginResults, result)
        return result

    async def get_api_spec(self) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Get's all the API specs for the ADS or Instance.
        See `docs/api_spec.md`

        Returns:
            None | str | bool | dict[str, Any] | list[Any]: A dictionary containing all of the API specs, their parameters and return types for the ADS or Instance.
        """

        await self._connect()
        result = await self._call_api('Core/GetAPISpec')
        return result

    async def get_updates(self) -> Updates | str | dict[str, Any] | list | bool | int | None:
        """
        Requests the recent entries of the Instance Updates; will acquire all updates from previous API call of `getUpdate()`

        Returns:
            Updates | str | dict[str, Any] | list | bool | int | None None: On success returns a Updates dataclass.
                See `types.py -> Updates`
        """

        await self._connect()
        result = await self._call_api('Core/GetUpdates')
        if isinstance(result, dict):
            return fromdict(Updates, result)
        return result

    async def send_console_message(self, msg: str) -> None:
        """
        Sends a string to the Console. (eg `/list`)

        Returns:
            None: ""
        """

        await self._connect()
        parameters = {'message': msg}
        await self._call_api('Core/SendConsoleMessage', parameters)
        return

    async def start_instance(self) -> ActionResult | str | dict[str, Any] | list | bool | int | None:
        """
        Starts the AMP Server/Instance

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: Results from the API call.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api('Core/Start')
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    async def stop_instance(self) -> None:
        """
        Stops the AMP Server/Instance

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api('Core/Stop')
        return

    async def restart_instance(self) -> ActionResult | str | dict[str, Any] | list | bool | int | None:
        """
        Restarts the AMP Server/Instance

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: Results from the API call.
                See `types.py -> ActionResult`
        """

        await self._connect()
        result = await self._call_api('Core/Restart')
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    async def kill_instance(self) -> None:
        """
        Kills the AMP Server/Instance

        Returns:
            None: ""
        """

        await self._connect()
        await self._call_api('Core/Kill')
        return

    async def get_status(self) -> Status | str | dict[str, Any] | list | bool | int | None:
        """
        Gets the AMP Server/Instance Status information.

        Returns:
            Status | str | dict[str, Any] | list | bool | int | None: On success returns a Status dataclass.
                See `types.py -> Status`
        """

        await self._connect()
        result = await self._call_api('Core/GetStatus')
        if isinstance(result, dict):
            return fromdict(Status, result)
        return result

    async def get_user_list(self) -> Players | str | dict[str, Any] | list | bool | int | None:
        """
        Returns a dictionary of the connected Users to the Server.

        Returns:
            Players | str | dict[str, Any] | list | bool | int | None: on success returns a Player dataclass.
                See `types.py -> Players`
        """

        await self._connect()
        result = await self._call_api('Core/GetUserList')
        if isinstance(result, list):
            # TODO- Needs to be validated.
            return list(Players(data=player) for player in result)
            # return Players(data=result)
        return result

    async def get_schedule_data(self) -> ScheduleData | str | dict[str, Any] | list | bool | int | None:
        """
        Returns a dictionary of the Server/Instance Schedule events and triggers.

        Returns:
            ScheduleData | str | dict[str, Any] | list | bool | int | None: On success returns a ScheduleData dataclass.
                See `types.py -> ScheduleData`
        """

        await self._connect()
        result = await self._call_api('Core/GetScheduleData')
        if isinstance(result, dict):
            return fromdict(ScheduleData, result)
        return result

    async def end_user_session(self, session_id: str) -> str | None:
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
        await self._call_api('Core/EndUserSession', parameters)
        return

    async def get_active_amp_sessions(self) -> list[Session] | str | dict[str, Any] | list | bool | int | None:
        """
        Returns currently active AMP Sessions.\n
        **Requires ADS**

        Returns:
            Session | str | dict[str, Any] | list | bool | int | None: Returns a dataclass Session.
                See `types.py -> Session`
        """

        if self.Module != "ADS":
            raise RuntimeError(self.ADS_ONLY)

        await self._connect()
        result = await self._call_api('Core/GetActiveAMPSessions')
        if isinstance(result, list):
            return list(fromdict(Session, user) for user in result)
        return result

    async def get_amp_user_info(self, name: str) -> User | str | dict[str, Any] | list | bool | int | None:
        """
        Retrieves the AMP User information for the provided username.\n

        Args:
            name (str): AMP User name.

        Returns:
            User | str | dict[str, Any] | list | bool | int | None: On success returns a User dataclass. 
                See `types.py -> User`
        """

        await self._connect()
        parameters = {
            'Username': name
        }
        result = await self._call_api('Core/GetAMPUserInfo', parameters)
        if isinstance(result, dict):
            return User(**result)
        return result

    async def current_session_has_permission(self, permission_node: str) -> str | dict[str, Any] | list | bool | int | None:
        """
        Retrieves the current Session IDs permissions. This will differ between the ADS and a Server/Instance.

        Args:
            permission_node (str): The permission node to check for. eg `Core.RoleManagement.DeleteRoles` \n
            Supports looking for a blocked permisson node simply by appending `-` in front of the permission node. eg `-Core.RoleManagement.DeleteRoles`\n
            Supports wildcards `*`. eg `Core.RoleManagement.*`

        Returns:
            str | dict[str, Any] | list | bool | int | None: On success returns a bool.
        """

        await self._connect()
        parameters = {
            'PermissionNode': permission_node
        }
        result = await self._call_api('Core/CurrentSessionHasPermission', parameters)
        if isinstance(result, bool):
            return result
        return result

    async def get_amp_role_permissions(self, role_id: str) -> str | dict[str, Any] | list | bool | int | None:
        """
        Retrieves the AMP Role permission nodes for the provided role ID.

        Args:
            role_id (str): The role ID. eg `5d6566e0-fae2-41d7-bfb6-d21033247f2e`

        Returns:
            str | dict[str, Any] | list | bool | int | None: On success returns a list containing all the permission nodes for the provided role ID.
        """

        await self._connect()
        parameters = {
            'RoleId': role_id
        }
        result = await self._call_api("Core/GetAMPRolePermissions", parameters)
        if isinstance(result, list):
            return result
        return result

    async def get_permissions_spec(self) -> str | dict[str, Any] | list | bool | int | None:
        """
        Retrieves the AMP Permissions node tree.

        Returns:
            str | dict[str, Any] | list | bool | int | None: On success returns a dictionary containing all the permission nodes, descriptions and other attributes.
        """

        await self._connect()
        result = await self._call_api("Core/GetPermissionsSpec")
        if isinstance(result, dict):
            return result
        return result

    async def get_role_ids(self) -> str | dict[str, Any] | list | bool | int | None:
        """
        Retrieves all the Roles AMP currently has and the role IDs.

        Returns:
            Roles | str | dict[str, Any] | list | bool | int | None: On success returns a dictionary containing all the roles and their IDs. \n
            *Example*
            `{'00000000-0000-0000-0000-000000000000': 'Default','cb984b09-a1c6-4cc0-b005-df8907f06590': 'Super Admins'}`
        """

        await self._connect()
        result = await self._call_api('Core/GetRoleIds')
        if isinstance(result, dict):
            return result
        return result

    async def create_role(self, name: str, as_common_role: bool = False) -> ActionResult | str | dict[str, Any] | list | bool | int | None:
        """
        Creates an AMP Role.

        Args:
            name (str): The name of the role.
            as_common_role (bool, optional): A role that everyone has. Defaults to False.

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`

        """

        await self._connect()
        parameters = {
            'Name': name,
            'AsCommonRole': as_common_role
        }
        result = await self._call_api('Core/CreateRole', parameters)
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    async def get_role(self, role_id: str) -> Role | str | dict[str, Any] | list | bool | int | None:
        """
        Retrieves the AMP Role information for the provided role ID.

        Args:
            role_id (str): The role ID to get information for.

        Returns:
            Role | str | dict[str, Any] | list | bool | int | None: On success returns a Role dataclass.
                See `types.py -> Role`

        """

        await self._connect()
        parameters = {
            'RoleId': role_id
        }
        result = await self._call_api('Core/GetRole', parameters)
        if isinstance(result, dict):
            return Role(**result)
        return result

    async def set_amp_user_role_membership(self, user_id: str, role_id: str, is_member: bool) -> ActionResult | str | dict[str, Any] | list | bool | int | None:
        """
        Adds a user to an AMP role.

        Args:
            user_id (str): User ID to add to the role.
            role_id (str): Role ID to add the user to.
            is_member (bool): `True` to add the user to the role, `False` to remove the user from the role.

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'UserId': user_id,
            'RoleId': role_id,
            'IsMember': is_member
        }
        result = await self._call_api('Core/SetAMPUserRoleMembership', parameters)
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    async def set_amp_role_permission(self, role_id: str, permission_node: str, enabled: Union[None, bool]) -> ActionResult | str | dict[str, Any] | list | bool | int | None:
        """
        Set a permission node to `True` or `False` for the provided AMP role.

        Args:
            role_id (str): AMP role id.
            permission_node (str): AMP permission node. eg `Core.RoleManagement.DeleteRoles`
            enabled (Union[None, bool]): Set a permission to `True`, `False` or `None` depending on the results you can disable or enable an entire tree node of permissions.

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'RoleId': role_id,
            'PermissionNode': permission_node,
            'Enabled': enabled
        }
        result = await self._call_api('Core/SetAMPRolePermission', parameters)
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    async def get_settings_spec(self) -> str | dict[str, Any] | list | bool | int | None:
        """
        Retrieves a Server/Instance nodes list.
        See `util.getNodespec` for a list of possible nodes.

        Returns:
            str | dict[str, Any] | list | bool | int | None: On success returns a dictionary containing all of the Server/Instance nodes and there information.
        """

        await self._connect()
        result = await self._call_api('Core/GetSettingsSpec')
        if isinstance(result, dict):
            return result
        return result

    async def get_config(self, node: str) -> Node | str | dict[str, Any] | list | bool | int | None:
        # TODO - Need to figure out how this command works entirely. Possible need a new node list
        """
        Returns the config settings for a specific node.

        Args:
            node (str): The AMP node to inspect eg `ADSModule.Networking.BaseURL`

        Returns:
            Node | str | dict[str, Any] | list | bool | int | None: On success returns a dictionary containing the following. \n
        """

        await self._connect()
        parameters = {
            "node": node
        }
        result = await self._call_api("Core/GetConfig", parameters)
        if isinstance(result, dict):
            return Node(**result)
        return result

    async def get_configs(self, nodes: list[str]) -> list[Node] | str | dict[str, Any] | list | bool | int | None:
        # TODO - Need to figure out how this command works entirely. Possible need a new node list
        """
        Returns the config settings for each node in the list.

        Args:
            node (list[str]): List of nodes to look at.

        Returns:
            list[Node] | str | dict[str, Any] | list | bool | int | None: On success returns a list of Node dataclasses.
                See `types.py -> Node`
        """

        await self._connect()
        parameters = {
            "nodes": nodes
        }
        result = await self._call_api("Core/GetConfigs", parameters)
        if isinstance(result, list):
            return list(Node(**node) for node in result)
        return result

    async def get_update_info(self) -> UpdateInfo | str | dict[str, Any] | list | bool | int | None:
        """
        Returns a data class `UpdateInfo` and `UpdateInfo.Build = AMP_Version` to access Version information for AMP.

        Returns:
            UpdateInfo | str | dict[str, Any] | list | bool | int | None: On success returns a UpdateInfo dataclass.
                See `types.py -> UpdateInfo`
        """

        await self._connect()
        result = await self._call_api("Core/GetUpdateInfo")
        if isinstance(result, dict):
            return UpdateInfo(**result)
        return result

    async def get_all_amp_user_info(self) -> list[User] | str | dict[str, Any] | list | bool | int | None:
        """
        Represents all the AMP User info.

        Returns:
            list[User] | str | dict[str, Any] | list | bool | int | None: On success returns a list of User dataclasses.
                See `types.py -> User`
        """

        await self._connect()
        result = await self._call_api("Core/GetAllAMPUserInfo")
        if isinstance(result, list):
            return list(User(**user) for user in result)
        return result
