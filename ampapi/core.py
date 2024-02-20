from __future__ import annotations
from typing import Union
from dataclass_wizard import fromdict
from .types import *
from .base import Base

__all__ = ("Core",)


class Core(Base):
    async def login(self, amp_user: str, amp_password: str, token: str = "", rememberME: bool = False) -> LoginResults | None | bool | int | str:
        """
        AMP API login function. \n

        Args:
            amp_user (str): The username for logging into the AMP Panel
            amp_password (str): The password for logging into the AMP Panel
            token (str, optional): AMP 2 Factor auth code; typically using `TOTP.now()`. Defaults to "".
            rememberME (bool, optional): Remember me token.. Defaults to False.

        Returns:
            LoginResults | None | bool | int | str: On success returns a LoginResult dataclass.
                See `types.py -> LoginResult`
        """
        parameters = {
            'username': amp_user,
            'password': amp_password,
            'token': token,
            'rememberMe': rememberME}
        result = await self._call_api('Core/Login', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return fromdict(LoginResults, result)  # type:ignore

    async def getUpdates(self) -> Updates | str | bool | int | None:
        """
        Requests the recent entries of the Instance Updates; will acquire all updates from previous API call of `getUpdate()`

        Returns:
            Updates | str | bool | int | None: On success returns a Updates dataclass.
                See `types.py -> Updates`
        """
        await self._connect()
        result = await self._call_api('Core/GetUpdates')
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return fromdict(Updates, result)  # type:ignore

    async def sendConsoleMessage(self, msg: str) -> None:
        """
        Sends a string to the Console. (eg `/list`)

        Returns:
            None: ""
        """
        await self._connect()
        parameters = {'message': msg}
        await self._call_api('Core/SendConsoleMessage', parameters)
        return

    async def startInstance(self) -> str | dict | list | bool | int | None:
        """
        Starts the AMP Server/Instance

        Returns:
            ActionResult | str | bool | int | None: Results from the API call.
                See `types.py -> ActionResult`
        """
        await self._connect()
        result = await self._call_api('Core/Start')
        return ActionResult(**result)  # type:ignore

    async def stopInstance(self) -> None:
        """
        Stops the AMP Server/Instance

        Returns:
            None: ""
        """
        await self._connect()
        await self._call_api('Core/Stop')
        return

    async def restartInstance(self) -> str | dict | list | bool | int | None:
        """
        Restarts the AMP Server/Instance

        Returns:
            ActionResult | str | bool | int | None: Results from the API call.
                See `types.py -> ActionResult`
        """
        await self._connect()
        result = await self._call_api('Core/Restart')
        return ActionResult(**result)  # type:ignore

    async def killInstance(self) -> None:
        """
        Kills the AMP Server/Instance

        Returns:
            None: ""
        """
        await self._connect()
        await self._call_api('Core/Kill')
        return

    async def getStatus(self) -> Status | str | bool | int | None:
        """
        Gets the AMP Server/Instance Status information.

        Returns:
            Status | str | bool | int | None: On success returns a Status dataclass.
                See `types.py -> Status`
        """
        await self._connect()
        result = await self._call_api('Core/GetStatus')
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return fromdict(Status, result)  # type:ignore

    async def getUserList(self) -> Players | str | bool | int | None:
        """
        Returns a dictionary of the connected Users to the Server.

        Returns:
            Players | str | bool | int | None: on success returns a Player dataclass.
                See `types.py -> Players`
        """
        await self._connect()
        result = await self._call_api('Core/GetUserList')
        if isinstance(result, Union[None, bool, int, str]):
            return result
        # TODO- Needs to be validated.
        return Players(data=result)  # type:ignore

    async def getScheduleData(self) -> ScheduleData | str | bool | int | None:
        """
        Returns a dictionary of the Server/Instance Schedule events and triggers.

        Returns:
            ScheduleData | str | bool | int | None: On success returns a ScheduleData dataclass.
                See `types.py -> ScheduleData`
        """
        await self._connect()
        result = await self._call_api('Core/GetScheduleData')
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return fromdict(ScheduleData, result)  # type:ignore

    async def endUserSession(self, session_id: str) -> str | None:
        """
        Closes the specified User's session ID to AMP.\n
        **Requires ADS**

        Args:
            session_id (str): session ID to end.

        Returns:
            None: ""
        """
        if not isinstance(self, Controller):
            return self.ADS_ONLY

        await self._connect()
        parameters = {
            'Id': session_id
        }
        await self._call_api('Core/EndUserSession', parameters)
        return

    async def getActiveAMPSessions(self) -> Session | str | bool | int | None:
        """
        Returns currently active AMP Sessions.\n
        **Requires ADS**

        Returns:
            Session | str | bool | int | None: Returns a dataclass Session.
                See `types.py -> Session`
        """
        if not isinstance(self, Controller):
            return self.ADS_ONLY

        await self._connect()
        result = await self._call_api('Core/GetActiveAMPSessions')
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return Session(**result)  # type:ignore

    async def getAMPUserInfo(self, name: str) -> User | str | bool | dict | None:
        """
        Retrieves the AMP User information for the provided username.\n

        Args:
            name (str): AMP User name.

        Returns:
            User | str | bool | dict: On success returns a User dataclass. 
                See `types.py -> User`
        """

        await self._connect()
        parameters = {
            'Username': name
        }
        result = await self._call_api('Core/GetAMPUserInfo', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return User(**result)  # type:ignore

    async def currentSessionHasPermission(self, permission_node: str) -> str | bool | dict | list | None:
        """
        Retrieves the current Session IDs permissions. This will differ between the ADS and a Server/Instance.

        Args:
            permission_node (str): The permission node to check for. eg `Core.RoleManagement.DeleteRoles` \n
            Supports looking for a blocked permisson node simply by appending `-` in front of the permission node. eg `-Core.RoleManagement.DeleteRoles`\n
            Supports wildcards `*`. eg `Core.RoleManagement.*`

        Returns:
            str | bool | dict | list | None: On success returns a bool.
        """
        await self._connect()
        parameters = {
            'PermissionNode': permission_node
        }
        result = await self._call_api('Core/CurrentSessionHasPermission', parameters)
        return result

    async def getAMPRolePermissions(self, role_id: str) -> str | bool | dict | list | None:
        """
        Retrieves the AMP Role permission nodes for the provided role ID.

        Args:
            role_id (str): The role ID. eg `5d6566e0-fae2-41d7-bfb6-d21033247f2e`

        Returns:
            str | bool | dict | list | None: On success returns a list containing all the permission nodes for the provided role ID.
        """
        await self._connect()
        parameters = {
            'RoleId': role_id
        }
        result = await self._call_api("Core/GetAMPRolePermissions", parameters)
        return result

    async def getPermissionsSpec(self) -> str | bool | dict | list | None:
        """
        Retrieves the AMP Permissions node tree.

        Returns:
            str | bool | dict | list | None: On success returns a dictionary containing all the permission nodes, descriptions and other attributes.
        """
        await self._connect()
        result = await self._call_api("Core/GetPermissionsSpec")
        return result

    async def getRoleIds(self) -> str | bool | dict | list | None:
        """
        Retrieves all the Roles AMP currently has and the role IDs.

        Returns:
            Roles | str | bool | dict | list | None: On success returns a Roles dataclass containing all the roles and their IDs. Example below. \n
        """
        await self._connect()
        result = await self._call_api('Core/GetRoleIds')
        return result

    async def createRole(self, name: str, as_common_role: bool = False) -> ActionResult | str | bool | dict | list | None:
        """
        Creates an AMP Role.

        Args:
            name (str): The name of the role.
            as_common_role (bool, optional): A role that everyone has. Defaults to False.

        Returns:
            ActionResult | str | bool | dict | list | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`

        """
        await self._connect()
        parameters = {
            'Name': name,
            'AsCommonRole': as_common_role
        }
        result = await self._call_api('Core/CreateRole', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def getRole(self, role_id: str) -> Role | str | bool | dict | list | None:
        """
        Retrieves the AMP Role information for the provided role ID.

        Args:
            role_id (str): The role ID to get information for.

        Returns:
            str | bool | dict: On success returns a Role dataclass.
                See `types.py -> Role`

        """
        await self._connect()
        parameters = {
            'RoleId': role_id
        }
        result = await self._call_api('Core/GetRole', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return Role(**result)  # type:ignore

    async def setAMPUserRoleMembership(self, user_id: str, role_id: str, is_member: bool) -> ActionResult | str | bool | dict | list | None:
        """
        Adds a user to an AMP role.

        Args:
            user_id (str): User ID to add to the role.
            role_id (str): Role ID to add the user to.
            is_member (bool): `True` to add the user to the role, `False` to remove the user from the role.

        Returns:
            ActionResult | str | bool | dict | list | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'UserId': user_id,
            'RoleId': role_id,
            'IsMember': is_member
        }
        result = await self._call_api('Core/SetAMPUserRoleMembership', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def setAMPRolePermission(self, role_id: str, permission_node: str, enabled: Union[None, bool]) -> ActionResult | str | bool | dict | list | None:
        """
        Set a permission node to `True` or `False` for the provided AMP role.

        Args:
            role_id (str): AMP role id.
            permission_node (str): AMP permission node. eg `Core.RoleManagement.DeleteRoles`
            enabled (Union[None, bool]): Set a permission to `True`, `False` or `None` depending on the results you can disable or enable an entire tree node of permissions.

        Returns:
            ActionResult | str | bool | dict | list | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'RoleId': role_id,
            'PermissionNode': permission_node,
            'Enabled': enabled
        }
        result = await self._call_api('Core/SetAMPRolePermission', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def getSettingsSpec(self) -> str | bool | dict | list | None:
        """
        Retrieves a Server/Instance nodes list.
        See `util.getNodespec` for a list of possible nodes.

        Returns:
            str | bool | dict: On success returns a dictionary containing all of the Server/Instance nodes and there information.
        """
        await self._connect()
        result = await self._call_api('Core/GetSettingsSpec')
        return result

    async def getConfig(self, node: str) -> Node | str | bool | dict | list | None:
        # TODO - Need to figure out how this command works entirely. Possible need a new node list
        """
        Returns the config settings for a specific node.

        Args:
            node (str): The AMP node to inspect eg `ADSModule.Networking.BaseURL`

        Returns:
            str | bool | dict: On success returns a dictionary containing the following. \n
        """
        await self._connect()
        parameters = {
            "node": node
        }
        result = await self._call_api("Core/GetConfig", parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return Node(**result)  # type:ignore

    async def getConfigs(self, nodes: list[str]) -> list[Node] | str | bool | dict | list | None:
        # TODO - Need to figure out how this command works entirely. Possible need a new node list
        """
        Returns the config settings for each node in the list.

        Args:
            node (list[str]): List of nodes to look at.

        Returns:
            str | bool | dict: On success returns a list of Node dataclasses.
                See `types.py -> Node`
        """
        await self._connect()
        parameters = {
            "nodes": nodes
        }
        result = await self._call_api("Core/GetConfigs", parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return list(Node(**node) for node in result)

    async def getUpdateInfo(self) -> UpdateInfo | str | int | bool | None:
        """
        Returns a data class `UpdateInfo` and `UpdateInfo.Build = AMP_Version` to access Version information for AMP.

        Returns:
            UpdateInfo | str | int | bool | None: On success returns a UpdateInfo dataclass.
                See `types.py -> UpdateInfo`
        """
        await self._connect()
        result = await self._call_api("Core/GetUpdateInfo")
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return UpdateInfo(**result)  # type:ignore

    async def getAllAMPUserInfo(self) -> list[User] | str | int | bool | None:
        """
        Represents all the AMP User info.

        Returns:
            list[User] | str | int | bool | None: On success returns a list of User dataclasses.
                See `types.py -> User`
        """
        await self._connect()
        result = await self._call_api("Core/GetAllAMPUserInfo")
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return list(User(**user) for user in result)
