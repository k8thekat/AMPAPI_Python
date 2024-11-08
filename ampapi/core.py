from datetime import datetime
from typing import Any, Literal, Union, overload

from pyotp import TOTP
from typing_extensions import deprecated

from .base import Base
from .dataclass import (
    ActionResult,
    AuditLogEntry,
    Diagnostics,
    InstanceStatus,
    LoginResults,
    LoginUserInfo,
    Module,
    Players,
    Port,
    Role,
    RunningTask,
    ScheduleData,
    Session,
    SettingSpec,
    SettingsSpecParent,
    TimedTrigger,
    UpdateInfo,
    Updates,
    User,
)
from .enums import *
from .types_ import Consumes, ParameterMapping, PermissionNode, ScheduleDataData, TriggerID, TriggersData, TriggerTasksData

__all__: tuple[Literal["Core"]] = ("Core",)


class Core(Base):
    """
    Contains the functions for any ``/API/Core/`` AMP API endpoints.

    .. note::
        If the ``format_data`` parameter is None on any function; the global ``FORMAT_DATA`` will be used instead.


    """

    @property
    def events(self) -> None:
        print()

    @property
    def triggers(self) -> TriggerID:
        try:
            return self._triggers
        except AttributeError:
            raise AttributeError("You need to first call function <Core.get_triggers()> before accessing this attribute.")

    async def _create_test_task(self) -> None:
        """|coro|

        **DEV**: Creates a non-ending task with 50% progress for testing purposes

        Returns:
        ---
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/CreateTestTask")
        return

    async def _async_test(self) -> str:
        """|coro|

        **DEV**: Async test method


        Returns:
        ---
        :class:`str`
            Returns a string.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/AsyncTest")
        return result

    async def acknowledge_amp_update(self) -> None:
        """|coro|

        Approve an AMP update.

        Returns
        --------
        None
        """
        await self._connect()
        await self._call_api(api="Core/AcknowledgeAMPUpdate", _no_data=True)
        return None

    async def activate_amp_license(
        self, license_key: str, query_only: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Activate an AMP License key.

        Parameters
        -----------
        license_key: :class:`str`
            Your AMP License key.
        query_only: bool, optional
            UNK, by default False.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"LicenceKey": license_key, "QueryOnly": query_only}
        result: Any = await self._call_api(
            api="Core/ActivateAMPLicence", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def add_event_trigger(self, trigger_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Add an Event Trigger to an Instance.

        .. note::
            See :attr:`Triggers.id`; which you can get a list of triggers from |triggers|.


        # todo - find out how to get a list of all available triggers to get their IDs. Generate a document.
        Parameters
        -----------
        trigger_id: :class:`str`
            The Trigger ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"TriggerId": trigger_id}
        result: Any = await self._call_api(
            api="Core/AddEventTrigger", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def add_task(
        self, trigger_id: str, method_id: str, parameter_mapping: dict[str, str], format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Add a task.

        .. note::
            Example -> ``parameter_mapping = { "Subtitle": "Hello World", Title: "Hello {@UserID}" }``


        Parameters
        -----------
        trigger_id: class:`str`
            The ID of the trigger to add.
        method_id: class:`str`
            The Task method name. eg. ```Event.MinecraftModule.SendGlobalTitle``
        parameter_mapping: :class:dict[:class:`str`, :class:`str`]
            The parameters to be populated related to the trigger_id/method_id.\n
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"TriggerID": trigger_id, "MethodID": method_id, "ParameterMapping": parameter_mapping}
        result: Any = await self._call_api(
            api="Core/AddTask", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def cancel_task(self, task_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Cancel an existing Task.

        Parameters
        -----------
        task_id: :class:`str`
            The ID of the Task.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"TaskId": task_id}
        result: Any = await self._call_api(
            api="Core/CancelTask", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def change_user_password(
        self,
        username: str,
        old_password: str,
        new_password: str,
        two_factor_pin: str = "",
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        For a user to change their own password, requires knowing the old password.

        Parameters
        -----------
        username: :class:`str`
            The AMP user name.
        old_password: :class:`str`
            Current AMP user password.
        new_password: :class:`str`
             New AMP user password.
        two_factor_pin: :class:`str`
            Two Factor PIN, if enabled. Defaults to "".
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {
            "Username": username,
            "OldPassword": old_password,
            "NewPassword": new_password,
            "TwoFactorPIN": two_factor_pin,
        }

        results: Any = await self._call_api(
            api="Core/ChangeUserPassword", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return results

    async def change_task_order(
        self, trigger_id: str, task_id: str, new_order: int, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Change the order of a task.

        Parameters
        -----------
        trigger_id: :class:`str`
            The ID of the Trigger you want to change the order of a task.
        task_id: :class:`str`
            The ID of the task to modify. See :meth:`get_schedule_data` to get IDs
        new_order: :class:`int`
            The new task position.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"TriggerID": trigger_id, "TaskID": task_id, "NewOrder": new_order}
        result: Any = await self._call_api(
            api="Core/ChangeTaskOrder", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def confirm_two_factor_setup(
        self, username: str, two_factor_code: str, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Completes two-factor setup by supplying a valid two factor code based on the secret provided by EnableTwoFactor.

        Parameters
        -----------
        username: :class:`str`
            The AMP User name to confirm 2FA setup.
        two_factor_code: :class:`str`
            Two factor code.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Username": username, "TwoFactorCode": two_factor_code}
        result: Any = await self._call_api(
            api="Core/ConfirmTwoFactorSetup", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def create_role(
        self, role_name: str, as_common_role: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Creates an AMP Role.

        Parameters
        -----------
        role_name: :class:`str`
            The name you want for the AMP role.
        as_common_role: :class:`bool`, optional
            A role that everyone has, defaults to False.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Name": role_name, "AsCommonRole": as_common_role}
        result: Any = await self._call_api(
            api="Core/CreateRole", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def create_user(self, username: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Create an AMP user.

        Parameters
        -----------
        username: :class:`str`
            The AMP User name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Username": username}
        result: Any = await self._call_api(
            api="Core/CreateUser", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def current_session_has_permission(self, node: str) -> bool:
        """|coro|

        Retrieves the current Session IDs permissions. This will differ between the ADS and a Server/Instance.

        .. note::
            Supports looking for a blocked permission node simply by appending `-` in front of the permission node. eg `-Core.RoleManagement.DeleteRoles`, also supports wildcards `*`. eg `Core.RoleManagement.*`



        Parameters
        -----------
        node: :class:`str`
            The permission node to check for. eg `Core.RoleManagement.DeleteRoles`. \n

        Returns
        --------
        :class:`bool`
        """

        await self._connect()
        parameters: dict[str, str] = {"PermissionNode": node}
        result: Any = await self._call_api(api="Core/CurrentSessionHasPermission", parameters=parameters)
        return result

    async def delete_instance_users(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Delete an Instances User list.

        Parameters
        -----------
        instance_id: :class:`str`
            The AMP Instance ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"InstanceId": instance_id}

        results: Any = await self._call_api(
            api="Core/DeleteInstanceUsers", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return results

    async def delete_role(self, role_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Deletes a role.

        Parameters
        -----------
        role_id: :class:`str`
            The ID of the role to delete.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"RoleId": role_id}
        result: Any = await self._call_api(
            api="Core/DeleteRole", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def delete_task(self, trigger_id: str, task_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Delete a task.


        Parameters
        ------------
        trigger_id: :class:`str`
            The ID of the trigger to delete.
        task_id: :class:`str`
            The ID of the task to delete. See :meth:`get_schedule_data` and check the :class:`Tasks` class to get IDs.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"TriggerID": trigger_id, "TaskID": task_id}
        result: Any = await self._call_api(
            api="Core/DeleteTask", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def delete_trigger(self, trigger_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Delete a trigger.

        Parameters
        -----------
        trigger_id: :class:`str`
            The ID of the trigger to delete.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"TriggerID": trigger_id}
        result: Any = await self._call_api(
            api="Core/DeleteTrigger", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def delete_user(self, username: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Delete an AMP user.

        Parameters
        -----------
        username: :class:`str`
            The AMP User name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Username": username}
        result: Any = await self._call_api(
            api="Core/DeleteUser", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def disable_two_factor(self, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Disables two-factor authentication for the currently logged in AMP User.

        .. warning::
            This applies to the AMP User name supplied to interact with the API.


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"Password": self._bridge.password, "TwoFactorCode": TOTP(self._bridge.token).now()}
        result: Any = await self._call_api(
            api="Core/DisableTwoFactor", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def dismiss_all_tasks(self, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Dismiss all task notifications.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/DismissAllTasks", format_data=format_data, format_=ActionResult)
        return result

    async def dismiss_task(self, task_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Dismiss a task notification.

        Parameters
        -----------
        task_id: :class:`str`
            The ID of the task to delete. See :meth:`get_schedule_data` and check the :class:`Tasks` class to get IDs.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"TaskId": task_id}
        result: Any = await self._call_api(
            api="Core/DismissTask", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    # todo - test function/parameters
    async def edit_interval_trigger(
        self,
        trigger_id: str,
        months: int,
        days: int,
        hours: int,
        minutes: int,
        days_of_month: int,
        description: str,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Edits an interval trigger.

        Parameters
        -----------
        trigger_id: :class:`str`
            The ID of the interval trigger to edit.
        months: :class:`int`
            The number of the month you want the trigger to run.
        days: :class:`int`
            The days of the interval trigger to edit.
        hours: :class:`int`
            The hours of the interval trigger to edit.
        minutes: :class:`int`
            The minutes of the interval trigger to edit.
        days_of_month: :class:`int`
            The days of the month of the interval trigger to edit.
        description: :class:`str`
            The description of the interval trigger to edit.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {
            "Id": trigger_id,
            "months": months,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "daysOfMonth": days_of_month,
            "description": description,
        }
        result: Any = await self._call_api(
            api="Core/EditIntervalTrigger", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def edit_task(
        self, trigger_id: str, task_id: str, parameter_mapping: dict[str, str], format_data: Union[bool, None] = None
    ) -> ActionResult:
        """
        Edit a task.

        Parameters
        -----------
        trigger_id: :class:`str`
             The ID of the trigger to edit.
        task_id: :class:`str` The ID of the task to edit. See `get_schedule_data().Tasks` to get IDs
            parameter_mapping (dict[str, str]): The parameters to be updated on the task.\n
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"TriggerID": trigger_id, "TaskID": task_id, "ParameterMapping": parameter_mapping}
        result: Any = await self._call_api(
            api="Core/EditTask", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def enable_two_factor(self, username: str, password: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Sets up two-factor authentication for the given user. \n
        `**WARNING**` ConfirmTwoFactorSetup must be invoked to complete setup.

        Parameters
        -----------
        username: :class:`str`
            Username.
            password (str): Password.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            ActionResult: On success returns an dictionary with the structure \n
            `{"Result" : {"ManualKey" : str, "Url" : str}, "Status": bool}`.
        """

        await self._connect()
        parameters: dict[str, str] = {"Username": username, "Password": password}
        result: Any = await self._call_api(
            api="Core/EnableTwoFactor", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def end_user_session(self, session_id: str) -> None:
        """
        Closes the specified User's session ID to AMP.\n
        **Requires ADS**

        Parameters
        -----------
            session_id (str): session ID to end.

        Returns:
        ---
            None: ""
        """
        if self.module != "ADS":
            raise RuntimeError(self._ads_only)

        await self._connect()
        parameters: dict[str, str] = {"Id": session_id}
        await self._call_api(api="Core/EndUserSession", parameters=parameters)
        return

    async def get_active_amp_sessions(self, format_data: Union[bool, None] = None) -> list[Session]:
        """
        Returns currently active AMP Sessions.\n
        **Requires ADS**

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Session: Returns a dataclass Session.
            * See `types.py -> Session`
        """

        if self.module != "ADS":
            raise RuntimeError(self._ads_only)

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetActiveAMPSessions", format_data=format_data, format_=Session, _use_from_dict=False
        )
        return result

    async def get_all_amp_user_info(self, format_data: Union[bool, None] = None) -> list[User]:
        """
        Retrieves all AMP Users and their information.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[User]: On success returns a list of User dataclasses.
            * See `types.py -> User`
        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetAllAMPUserInfo", format_data=format_data, format_=User, _use_from_dict=False
        )
        return result

    async def get_amp_role_permissions(self, role_id: str) -> list[Any]:
        """
        Retrieves the AMP Role permission nodes for the provided role ID.

        Parameters
        -----------
            role_id: :class:`str` The role ID. eg `5d6566e0-fae2-41d7-bfb6-d21033247f2e`

        Returns:
        ---
            list[Any]: On success returns a list containing all the permission nodes for the provided role ID.
        """

        await self._connect()
        parameters: dict[str, str] = {"RoleId": role_id}
        result: Any = await self._call_api(api="Core/GetAMPRolePermissions", parameters=parameters)
        return result

    async def get_amp_user_info(self, name: str, format_data: Union[bool, None] = None) -> User:
        """
        Retrieves the AMP User information for the provided username.\n

        Parameters
        -----------
            name (str): AMP User name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            User: On success returns a User dataclass.
            * See `types.py -> User`
        """

        await self._connect()
        parameters: dict[str, str] = {"Username": name}
        result: Any = await self._call_api(
            api="Core/GetAMPUserInfo", parameters=parameters, format_data=format_data, format_=User, _use_from_dict=False
        )
        return result

    async def get_amp_users_summary(self, format_data: Union[bool, None] = None) -> list[LoginUserInfo]:
        """
        Get all AMP users summary.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[UserInfoSummary]: On success returns a list of UserInfoSummary dataclass.
            * See `types.py -> UserInfoSummary`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetAMPUsersSummary", format_data=format_data, format_=LoginUserInfo)
        return result

    async def get_api_spec(self, sanitize_json: bool = False) -> dict[Any, Any]:
        """
        Get's all the API specs for the ADS or Instance.
        * See `docs/api_spec.md`

        Returns:
        ---
            dict: A dictionary containing all of the API specs, their parameters and return types for the ADS or Instance.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetAPISpec", sanitize_json=sanitize_json)
        return result

    async def get_audit_log_entries(
        self, before: float = datetime.now().timestamp(), count: int = 10, format_data: Union[bool, None] = None
    ) -> list[AuditLogEntry]:
        """
        Returns the last :parameter:`count` number of audit log entries.
        - These are anything in the Console of the Controller such as login events

        Parameters
        ----------
        before : float
            A POSIX timestamp. Defaults to a datetime.now().timestamp().
        count : int
            Number of entries to return. Default is 10.
        format_data : Union[bool, None], optional
            Format the JSON response data. Defaults to None.
            - Uses ``FORMAT_DATA`` global constant if None

        Returns
        --------
        list[:py:class:`AuditLogEntry`]
            A list of :py:class:`AuditLogEntry` dataclasses.

        """

        await self._connect()
        parameters: dict[str, Any] = {"Before": before, "Count": count}
        result: Any = await self._call_api(
            api="Core/GetAuditLogEntries",
            parameters=parameters,
            format_data=format_data,
            format_=AuditLogEntry,
            _use_from_dict=False,
        )
        return result

    async def get_authentication_requirements(self, username: str, format_data: Union[bool, None] = None) -> list[Any]:
        """
        Get a list of Authentication Requirements for the AMP user.

        Parameters
        -----------
        username: :class:`str`
            AMP username.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[Any]: Returns a list of Authentication Requirements.
        """
        await self._connect()
        parameters: dict[str, str] = {"username": username}
        result: Any = await self._call_api(
            api="Core/GetAuthenticationRequirements", parameters=parameters, format_data=format_data
        )
        return result

    async def get_config(self, node: str, format_data: Union[bool, None] = None) -> SettingSpec:
        """
        Returns the config settings for a specific node.\n

        Parameters
        -----------
            node (str): The AMP node to inspect eg `ADSModule.Networking.BaseURL`
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Node: On success returns a dictionary containing the following. \n
        """

        await self._connect()
        parameters: dict[str, str] = {"node": node}
        result: Any = await self._call_api(
            api="Core/GetConfig", parameters=parameters, format_data=format_data, format_=SettingSpec
        )
        return result

    async def get_configs(self, nodes: list[str], format_data: Union[bool, None] = None) -> list[SettingSpec]:
        """
        Returns the config settings for each node in the list.\n

        Parameters
        -----------
            node (list[str]): List of nodes to look at.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[Node]: On success returns a list of Node dataclasses.
            * See `types.py -> Node`
        """

        await self._connect()
        parameters: dict[str, list[str]] = {"nodes": nodes}
        result: Any = await self._call_api(
            api="Core/GetConfigs", parameters=parameters, format_data=format_data, format_=SettingSpec
        )
        return result

    async def get_diagnostics_info(self, format_data: Union[bool, None] = None) -> Diagnostics:
        """
        Get's the system diagnostics information.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Diagnostics: On success returns a dictionary.\n

        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetDiagnosticsInfo",
            format_data=format_data,
            format_=Diagnostics,
            _use_from_dict=False,
            _auto_unpack=True,
        )
        return result

    async def get_module_info(self, format_data: Union[bool, None] = None) -> Module:
        """
        Returns the module information.


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Module: On success returns a Module dataclass.
            * See `types.py -> Module`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetModuleInfo", format_data=format_data, format_=Module)
        return result

    async def get_new_guid(self, format_data: Union[bool, None] = None) -> dict[str, Any]:
        """
        Get a new GUID.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetNewGuid", format_data=format_data)
        return result

    async def get_permissions_spec(self) -> list[PermissionNode]:
        """
        Retrieves the AMP Permissions node tree.

        Returns:
        ---
            dict[str, Any]: On success returns a dictionary containing all the permission nodes, descriptions and other attributes.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetPermissionsSpec")
        return result

    async def get_port_summaries(self, format_data: Union[bool, None] = None) -> list[Port]:
        """
        Get a summary of the instance's open ports.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[Port]: On success returns a list of Port dataclass.
            * See `types.py -> Port`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetPortSummaries", format_data=format_data, format_=Port)
        if format_data is None:
            format_data = self.format_data

        if format_data == False:
            return result

        elif isinstance(result, list):
            return [Port(**port) for port in result]
        return result

    async def get_provision_spec(self, format_data: Union[bool, None] = None) -> list[SettingSpec]:
        """
        Returns the provisioning spec.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[SettingSpec]: On success returns a list of provisioning spec.
            * See `types.py -> JObject`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetProvisionSpec", format_data=format_data, format_=SettingSpec)
        return result

    async def get_remote_login_token(
        self,
        description: Union[str, None] = None,
        is_temporary: Union[bool, None] = None,
        format_data: Union[bool, None] = None,
    ) -> str:
        """
        Get the remote login token.

        Parameters
        -----------
            description (Union[str, None], optional): Description. Defaults to None.
            is_temporary (Union[bool, None], optional): Is temporary. Defaults to None.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            str: On success returns a str.
            * See `types.py -> str`
        """

        await self._connect()
        parameters: dict[str, Any] = {"Description": description, "IsTemporary": is_temporary}
        result: Any = await self._call_api(api="Core/GetRemoteLoginToken", parameters=parameters, format_data=format_data)
        return result

    async def get_role(self, role_id: str, format_data: Union[bool, None] = None) -> Role:
        """
        Retrieves the AMP Role information for the provided role ID.

        Parameters
        -----------
            role_id: :class:`str` The role ID to get information for.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Role: On success returns a Role dataclass.
            * See `types.py -> Role`

        """

        await self._connect()
        parameters: dict[str, str] = {"RoleId": role_id}
        result: Any = await self._call_api(api="Core/GetRole", parameters=parameters, format_data=format_data, format_=Role)
        return result

    async def get_role_data(self, format_data: Union[bool, None] = None) -> list[Role]:
        """
        Get's a list of all the roles.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[Role]: On success returns a list of Role dataclasses.
            * See `types.py -> Role`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetRoleData", format_data=format_data, format_=Role)
        return result

    async def get_role_ids(self) -> dict[str, Any]:
        """
        Retrieves all the Roles AMP currently has and the role IDs.

        Returns:
        ---
            Roles: On success returns a dictionary containing all the roles and their IDs. \n
            *Example*
            `{'00000000-0000-0000-0000-000000000000': 'Default','cb984b09-a1c6-4cc0-b005-df8907f06590': 'Super Admins'}`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetRoleIds")
        return result

    @overload
    async def get_schedule_data(self, format_data: Union[bool, None] = False) -> ScheduleDataData: ...
    @overload
    async def get_schedule_data(self, format_data: Union[bool, None] = True) -> ScheduleData: ...

    async def get_schedule_data(self, format_data: Union[bool, None] = None) -> ScheduleData | ScheduleDataData:
        """
        Returns a dictionary of the Server/Instance Schedule events and triggers.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            ScheduleData: On success returns a ScheduleData dataclass.
            * See `types.py -> ScheduleData`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetScheduleData", format_data=format_data, format_=ScheduleData)
        return result

    async def get_setting_spec(self, format_data: Union[bool, None] = None) -> SettingsSpecParent:
        """
        Retrieves a list of settings that can be changed.

        Parameters
        ---------
        format_data : Union[bool, None], optional
            Format the JSON response data. (Uses `FORMAT_DATA` global constant if None),  Defaults to None.

        Returns
        --------
        SettingSpecParent :
            On success returns a list of :class:SettingSpecParent.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetSettingsSpec", format_data=format_data, format_=SettingsSpecParent, sanitize_json=True
        )
        return result

    async def get_setting_values(self, setting_node: str) -> dict[str, str]:
        """
        Returns the setting values.
        - See ``./docs/setting_notes.md`` for possible :param:`setting_node` values.

        Parameters
        ----------
        setting_node : str
            Setting Node name.
        format_data : Union[bool, None], optional
            Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            dict[str, str]: On success returns a dictionary of setting values.
        """

        await self._connect()
        parameters: dict[str, str] = {"SettingNode": setting_node}
        result: Any = await self._call_api(api="Core/GetSettingValues", parameters=parameters)
        return result

    async def get_status(self, format_data: Union[bool, None] = None) -> InstanceStatus:
        """
        Gets the AMP Instance/Application Status information.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Status: On success returns a AppStatus dataclass.
            * See `types.py -> AppStatus`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetStatus", format_data=format_data, format_=InstanceStatus)
        return result

    async def get_tasks(self, format_data: Union[bool, None] = None) -> list[RunningTask]:
        """
        Get all :py:class:`RunningTask`.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[RunningTask]: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetTasks", format_data=format_data, format_=RunningTask)
        return result

    async def get_time_interval_trigger(self, id_: str, format_data: Union[bool, None] = None) -> TimedTrigger:
        """
        Gets a time interval trigger information.

        Parameters
        -----------
            id_ (str): The ID of the time interval trigger to get.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            JObject: On success returns a JObject dataclass.
            * See `types.py -> JObject`
        """

        await self._connect()
        parameters: dict[str, str] = {"Id": id_}
        result: Any = await self._call_api(
            api="Core/GetTimeIntervalTrigger", parameters=parameters, format_data=format_data, format_=TimedTrigger
        )
        return result

    async def get_triggers(self) -> TriggerID:
        """
        Retrieves the available trigger IDs for the Instance and sets them as attributes tied to :attr:`triggers`.

        .. note::
            Each Instance has unique Trigger IDs. You can simply access the correct ID for the Trigger via :attr:`~Core.triggers.a_backup_has_started` as an example.
            This would return the ID str to be passed into a function that requires a Trigger ID value.

        Returns
        --------
        :class:`TriggerID`
            A class containing the Trigger Description as attributes referencing the Trigger ID tied to the Instance.
        """
        await self._connect()
        data: ScheduleDataData = await self.get_schedule_data(format_data=False)
        triggers: list[TriggersData] = data.get("available_triggers")
        for entry in triggers:
            entry["description"] = self.sanitize_json(json=entry["description"])
        self._triggers = TriggerID(data=triggers)
        return self._triggers

    async def get_update_info(self, format_data: Union[bool, None] = None) -> UpdateInfo:
        """
        Gets the Version information for AMP. \n
        Returns a dataclass `UpdateInfo` and `UpdateInfo.Build = AMP_Version` to

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            UpdateInfo: On success returns a `UpdateInfo` dataclass.
            * See `types.py -> UpdateInfo`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetUpdateInfo", format_data=format_data, format_=UpdateInfo)
        return result

    async def get_updates(self, format_data: Union[bool, None] = None) -> Updates:
        """
        Gets changes to the server status, in addition to any notifications or console output that have occurred since the last time GetUpdates() was called by the current session.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Updates: On success returns a Updates dataclass.
            * See `types.py -> Updates`
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetUpdates", format_data=format_data, format_=Updates)
        return result

    async def get_user_action_spec(self, format_data: Union[bool, None] = None) -> dict[str, Any]:
        """
        Get a specification of the user actions.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            dict[str, Any]: On success returns a dict.\n
                - {'ADSModule': {},'CommonCorePlugin': {},'Core': {},'EmailSenderPlugin': {},'FileManagerPlugin': {},'LocalFileBackupPlugin': {}}
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetUserActionsSpec", format_data=format_data)
        return result

    async def get_user_info(self, uid: str, format_data: Union[bool, None] = None) -> dict:
        """
        Provides information about a given in-application user (as opposed to AMP system users).

        Parameters
        -----------
            uid (str): _description_
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            dict: On success returns a dict.
        """

        await self._connect()
        parameters: dict[str, str] = {"UID": uid}
        result: Any = await self._call_api(api="Core/GetUserInfo", parameters=parameters, format_data=format_data)
        return result

    async def get_user_list(self, format_data: Union[bool, None] = None) -> list[Players]:
        """
        Returns a dictionary of the connected Users to the Server.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Players: on success returns a Player dataclass.
            * See `types.py -> list[Players]`
        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetUserList", format_data=format_data, format_=Players, _use_from_dict=False, _auto_unpack=False
        )
        return result

    async def get_webauthn_challenge(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Get a webauthn challenge.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetWebauthnChallenge", format_data=format_data, format_=ActionResult)
        return result

    async def get_webauthn_credential_ids(self, username: str, format_data: Union[bool, None] = None) -> list[Any]:
        """
        Get a webauthn credential IDs.

        Parameters
        -----------
        username: :class:`str`
            Username.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"username": username}
        result: Any = await self._call_api(
            api="Core/GetWebauthnCredentialIDs", parameters=parameters, format_data=format_data
        )
        return result

    async def get_webauthn_credential_summary(self, format_data: Union[bool, None] = None) -> list[Any]:
        """
        Get the webauthn credential summaries.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            list[Any] : List of webauthn credential summaries.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetWebauthnCredentialSummaries", format_data=format_data)
        return result

    @deprecated("This was removed in `2.6.0.0`", stacklevel=2)
    async def get_webserver_metrics(self, format_data: Union[bool, None] = None) -> Any:
        """
        Gets the webserver metrics.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            Any: UNK data returned by the API.
        """
        # TODO - Possibly create a version parser to handle this deprecated.
        await self._connect()
        result: Any = await self._call_api(api="Core/GetWebserverMetrics", format_data=format_data)
        return result

    async def kill_application(self) -> None:
        """
        Kills the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Returns:
        ---
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/Kill")
        return

    @deprecated(
        "Function overlap with `ADSModule.kill_instance()`, please use `Core.kill_application()` instead.", stacklevel=2
    )
    async def kill_instance(self) -> None:
        """
        Kills the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Returns:
        ---
            None: ""
        """
        import warnings

        warnings.warn(
            message="Core.kill_instance() is deprecated and scheduled for "
            "removal in a future version. Use Core.kill_application() instead to kill your Instance application.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return await self.kill_application()

    async def login(
        self,
        amp_user: str,
        amp_password: str,
        token: str = "",
        rememberME: bool = False,
        format_data: Union[bool, None] = None,
    ) -> LoginResults:
        """
        AMP API login function. \n

        Parameters
        -----------
            amp_user (str): The username for logging into the AMP Panel
            amp_password (str): The password for logging into the AMP Panel
            token (str, optional): AMP 2 Factor auth code; typically using `TOTP.now()`. Defaults to "".
            rememberME (bool, optional): Remember me token.. Defaults to False.

        Returns:
        ---
            LoginResults: On success returns a LoginResult dataclass.
            * See `types.py -> LoginResult`
        """
        parameters = {"username": amp_user, "password": amp_password, "token": token, "rememberMe": rememberME}
        result: Any = await self._call_api(
            api="Core/Login", parameters=parameters, format_data=format_data, format_=LoginResults
        )
        return result

    async def logout(self) -> None:
        """
        Logout from AMP.

        Returns:
        ---
            None
        """
        await self._connect()
        await self._call_api(api="Core/Logout")
        return

    @Base.ads_only
    async def restart_amp(self) -> None:
        """
        restart_amp

        Returns:
        ---
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/RestartAMP", _no_data=True)
        return

    async def resume_instance(self) -> None:
        """
        Allows the service to be re-started after previously being suspended.

        Returns:
        ---
            None: ""
        """
        await self._connect()
        await self._call_api(api="Core/Resume")
        return

    async def refresh_setting_value_list(self, node: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Refreshes a setting's value list.

        Parameters
        -----------
            name (str): Setting name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {
            "Name": node,
        }
        result: Any = await self._call_api(
            api="Core/RefreshSettingValueList", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def refresh_settings_source_cache(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Refreshes the settings source cache.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/RefreshSettingsSourceCache", format_data=format_data, format_=ActionResult
        )
        return result

    async def rename_role(self, role_id: str, new_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Renames a role.

        Parameters
        -----------
            role_id: :class:`str` The ID of the role to rename.
            new_name (str): The new name for the role.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"RoleId": role_id, "NewName": new_name}
        result: Any = await self._call_api(
            api="Core/RenameRole", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @deprecated(
        "Function overlap with `ADSModule.restart_instance()`, please use `restart_application()` instead.", stacklevel=2
    )
    async def restart_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Restarts the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            ActionResult: Results from the API call.
            * See `types.py -> ActionResult`
        """
        import warnings

        warnings.warn(
            message="Core.restart_instance() is deprecated and scheduled for "
            "removal in a future version. Use Core.restart_application() instead to restart your Instance application.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return await self.restart_application(format_data=format_data)

    async def restart_application(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Restarts the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Parameters
        ----------
        format_data : Union[bool, None], optional
            Format the JSON response data. (Uses `FORMAT_DATA` global constant if None), by default None

        Returns
        -------
        ActionResult : Returns an :py:class:`ActionResult` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/Restart", format_data=format_data, format_=ActionResult)
        return result

    async def reset_user_password(
        self, username: str, new_password: str, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """
        For administrative users to alter the password of another user.

        Parameters
        -----------
        username: :class:`str`
            Username.
            new_password (str): New password.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Username": username, "NewPassword": new_password}
        result: Any = await self._call_api(
            api="Core/ResetUserPassword", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def revoke_webauthn_credential(self, id_: int, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Revoke a webauthn credential.

        Parameters
        -----------
            id_ (int): ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, int] = {"ID": id_}
        result: Any = await self._call_api(
            api="Core/RevokeWebauthnCredential", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def run_security_check(self, format_data: Union[bool, None] = None) -> Any:
        """
        run_security_check _summary_

        Parameters
            format--------_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Any: UNK
        """
        # TODO - Need to get Proper data back.
        await self._connect()
        result: Any = await self._call_api(api="Core/RunSecurityCheck", format_data=format_data)
        return result

    async def run_event_trigger_immediately(self, trigger_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Runs an event trigger immediately.

        Parameters
        -----------
        trigger_id: :class:`str`
             The ID of the event trigger to run.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"TriggerId": trigger_id}
        result: Any = await self._call_api(
            api="Core/RunEventTriggerImmediately", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def set_amp_user_role_membership(
        self, user_id: str, role_id: str, is_member: bool, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """
        Adds a user to an AMP role.

        Parameters
        -----------
            user_id (str): User ID to add to the role.
            role_id: :class:`str` Role ID to add the user to.
            is_member (bool): `True` to add the user to the role, `False` to remove the user from the role.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"UserId": user_id, "RoleId": role_id, "IsMember": is_member}
        result: Any = await self._call_api(
            api="Core/SetAMPUserRoleMembership", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def set_amp_role_permission(
        self, role_id: str, permission_node: str, enabled: Union[None, bool], format_data: Union[bool, None] = None
    ) -> ActionResult:
        """
        Set a permission node to `True` or `False` for the provided AMP role.

        Parameters
        -----------
            role_id: :class:`str` AMP role id.
            permission_node (str): AMP permission node. eg `Core.RoleManagement.DeleteRoles`
            enabled (Union[None, bool]): Set a permission to `True`, `False` or `None` depending on the results you can disable or enable an entire tree node of permissions.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"RoleId": role_id, "PermissionNode": permission_node, "Enabled": enabled}
        result: Any = await self._call_api(
            api="Core/SetAMPRolePermission", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def set_trigger_enabled(self, id_: str, enabled: bool, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Sets the enabled state of a trigger.

        Parameters
        -----------
            id_ (str): The ID of the trigger to edit.
            enabled (bool): The enabled state of the trigger to edit.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Id": id_, "Enabled": enabled}
        result: Any = await self._call_api(
            api="Core/SetTriggerEnabled", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def send_console_message(self, msg: str) -> None:
        """
        Sends a string to the Console. (eg `/list`)

        Returns:
        ---
            None: ""
        """

        await self._connect()
        parameters: dict[str, str] = {"message": msg}
        await self._call_api(api="Core/SendConsoleMessage", parameters=parameters)
        return

    async def set_configs(self, data: dict[str, str], format_data: Union[bool, None] = None) -> bool:
        """
        Set's multiple config node values.

        Parameters
        -----------
            data (dict[str, str]): Dictionary of configs to set.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns:
        ---
            bool: On success returns a boolean.
        """

        await self._connect()
        parameters: dict[str, dict[str, str]] = {"data": data}
        result: Any = await self._call_api(api="Core/SetConfigs", parameters=parameters)
        return result

    async def set_config(self, node: str, value: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Set a config node value.

        Parameters
        -----------
            name (str): Config node name.
            value (str): Config node value.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"node": node, "value": value}
        result: Any = await self._call_api(
            api="Core/SetConfig", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def start_application(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Starts the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Parameters
        -----------
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to `None`. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: Results from the API call.
            * See `types.py -> ActionResult`
        """
        await self._connect()
        result: Any = await self._call_api(api="Core/Start", format_data=format_data, format_=ActionResult)
        return result

    async def stop_application(self) -> None:
        """
        Stops the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Returns:
        ---
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/Stop")
        return

    async def suspend_instance(self) -> None:
        """
        Prevents the current instance from being started, and stops it if it's currently running.

        Returns:
        ---
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/Suspend")
        return

    async def update_account_info(
        self, email_address: str, two_factor_pin: str, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """
        Update account info.

        Parameters
        -----------
            email_address (str): Email address.
            two_factor_pin (str): Two factor PIN.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"EmailAddress": email_address, "TwoFactorPIN": two_factor_pin}
        result: Any = await self._call_api(
            api="Core/UpdateAccountInfo", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def upgrade_amp(self) -> None:
        """
        Upgrade the current AMP Instance.
        **Requires ADS**

        Returns:
        ---
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/UpgradeAMP", _no_data=True)
        return

    @Base.ads_only
    async def update_amp_instance(self) -> None:
        """
        Updates the ADS Instance.
        - **Requires ADS** - :attribute:`module` must be equal to "ADS".

        Returns:
        ---
            None: ""
        """

        await self._connect()
        await self._call_api(api="Core/UpdateAMPInstance", _no_data=True)
        return

    async def update_application(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update the Instance application.


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/UpdateApplication", format_data=format_data, format_=ActionResult)
        return result

    async def update_user_info(
        self,
        user_name: str,
        disabled: bool = False,
        password_expires: bool = False,
        cannot_change_password: bool = False,
        must_change_password: bool = False,
        email_address: str = "",
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """
        Update an AMP user.

        Parameters
        -----------
            user_name (str): Username.
            disabled (bool, optional): Disabled. Defaults to False.
            password_expires (bool, optional): User password expires. Defaults to False.
            cannot_change_password (bool, optional): User cannot change password. Defaults to False.
            must_change_password (bool, optional): User must change password upon next login. Defaults to False.
            email_address (str, optional): Email address. Defaults to "".
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {
            "Username": user_name,
            "Disabled": disabled,
            "PasswordExpires": password_expires,
            "CannotChangePassword": cannot_change_password,
            "MustChangePassword": must_change_password,
            "EmailAddress": email_address,
        }
        result: Any = await self._call_api(
            api="Core/UpdateUserInfo", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def webauthn_register(
        self, attestation_object: str, client_data_json: str, description: str, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """
        Webauthn register.

        Parameters
        -----------
            attestation_object (str): Attestation object.
            client_data_json (str): Client data JSON.
            description (str): Description.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {
            "attestationObject": attestation_object,
            "clientDataJSON": client_data_json,
            "description": description,
        }
        result: Any = await self._call_api(
            api="Core/WebauthnRegister", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result
