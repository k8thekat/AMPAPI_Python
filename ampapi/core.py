import warnings
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
    VersionInfo,
)
from .modules import TriggerID, UserApplicationData
from .types_ import ActionSpec, APISpec, PermissionNode, ScheduleDataData, TriggersData

__all__: tuple[Literal["Core"]] = ("Core",)


class Core(Base):
    """
    Contains the functions for any ``/API/Core/`` AMP API endpoints.

    .. note::
        If the ``format_data`` parameter is None on any function; the global ``FORMAT_DATA`` will be used instead.


    Attributes
    -----------
    triggers: :class:`TriggerID`
        You can access all the trigger IDs an instance has via this attribute. See :class:`TriggerID` for more information.
    """

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
            See :attr:`Triggers.id`; which you can get a list of triggers from the documentation.


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
            The days of the interval trigger to edit, the first day of the week is Monday.
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
        if months < 1 or months > 12:
            raise ValueError("Months must be between 1 and 12.")
        if days < 0 or days > 7:
            raise ValueError("Days must be between 0 and 7.")
        if hours < 0 or hours > 23:
            raise ValueError("Hours must be between 0 and 23.")
        if minutes < 0 or minutes > 59:
            raise ValueError("Minutes must be between 0 and 59.")
        if days_of_month < 1 or days_of_month > 31:
            raise ValueError("Days of month must be between 1 and 31.")

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
        """|coro|

        Edit a task.

        Parameters
        -----------
        trigger_id: :class:`str`
             The ID of the trigger to edit.
        task_id: :class:`str`
            The ID of the task to edit. See :meth:`get_schedule_data` to get IDs.
        parameter_mapping: dict[:class:`str`, :class:`str`]:
            The parameters to be updated on the task.
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
        """|coro|

        Sets up two-factor authentication for the given user.

        .. warning::
            ConfirmTwoFactorSetup must be invoked to complete setup.


        Parameters
        -----------
        username: :class:`str`
            The AMP User name.
        password: :class:`str`
            The AMP Users password.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Username": username, "Password": password}
        result: Any = await self._call_api(
            api="Core/EnableTwoFactor", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def end_user_session(self, session_id: str) -> None:
        """|coro|

        Closes the specified User's session ID to AMP.

        .. warning::
            The Instance must be an ADS or Controller.


        Parameters
        -----------
        session_id: :class:`str`
            The AMP Session ID to close.
        """
        await self._connect()
        parameters: dict[str, str] = {"Id": session_id}
        await self._call_api(api="Core/EndUserSession", parameters=parameters, _no_data=True)
        return

    @Base.ads_only
    async def get_active_amp_sessions(self, format_data: Union[bool, None] = None) -> list[Session]:
        """|coro|

        Returns currently active AMP Sessions.

        .. warning::
            The Instance must be an ADS or Controller.



        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`Session`
            On success returns a :class:`Session` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetActiveAMPSessions", format_data=format_data, format_=Session, _use_from_dict=False
        )
        return result

    async def get_all_amp_user_info(self, format_data: Union[bool, None] = None) -> list[User]:
        """|coro|

        Retrieves all AMP Users and their information.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        ---------
        list[:class:`User`]
            On success returns a list of :class:`User` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetAllAMPUserInfo", format_data=format_data, format_=User, _use_from_dict=False
        )
        return result

    async def get_amp_role_permissions(self, role_id: str) -> list[str]:
        """|coro|

        Retrieves the AMP Role permission nodes for the provided role ID.

        Parameters
        -----------
        role_id: :class:`str`
            The role ID. eg "5d6566e0-fae2-41d7-bfb6-d21033247f2e"

        Returns
        --------
        list[:class:`str`]:
            On success returns a list of strings containing all the permission nodes for the provided role id.
        """

        await self._connect()
        parameters: dict[str, str] = {"RoleId": role_id}
        result: Any = await self._call_api(api="Core/GetAMPRolePermissions", parameters=parameters)
        return result

    async def get_amp_user_info(self, name: str, format_data: Union[bool, None] = None) -> User:
        """|coro|

        Retrieves the AMP User information for the provided username.\n

        Parameters
        -----------
        name: :class:`str`
            The AMP User name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`User`
            On success returns a :class:`User` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Username": name}
        result: Any = await self._call_api(
            api="Core/GetAMPUserInfo", parameters=parameters, format_data=format_data, format_=User, _use_from_dict=False
        )
        return result

    async def get_amp_users_summary(self, format_data: Union[bool, None] = None) -> list[LoginUserInfo]:
        """|coro|

        Get all AMP users summary.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`UserInfoSummary`]
            On success returns a list of :class:`UserInfoSummary` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetAMPUsersSummary", format_data=format_data, format_=LoginUserInfo)
        return result

    async def get_api_spec(self, sanitize_json: bool = False) -> APISpec:
        """|coro|

        Get's all the API specs for the Instance.

        .. note::
            See :ref:`API Reference <Documentation>` for more information.


        Returns
        --------
        :class:`APISpec`
            On success returns a dictionary with all of the API specs, their parameters and return types for the Instance.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetAPISpec", sanitize_json=sanitize_json)
        return result

    async def get_audit_log_entries(
        self, before: float = datetime.now().timestamp(), count: int = 10, format_data: Union[bool, None] = None
    ) -> list[AuditLogEntry]:
        """|coro|

        Returns the last ``count`` number of audit log entries.

        .. note::
            These are anything in the Console of the Controller/ADS such as login events or API calls.


        Parameters
        -----------
        before: :class:`float`
            A POSIX timestamp, defaults to datetime.now().timestamp().
        count: :class:`int`
            Number of entries to return, default is 10.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`AuditLogEntry`]
            On success returns a list of :class:`AuditLogEntry` dataclasses.
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
        """|coro|

        Get a list of Authentication requirements for the AMP user.

        Parameters
        -----------
        username: :class:`str`
            The AMP username.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[Any]
            On success returns a list of Authentication requirements.
        """
        await self._connect()
        parameters: dict[str, str] = {"username": username}
        result: Any = await self._call_api(
            api="Core/GetAuthenticationRequirements", parameters=parameters, format_data=format_data
        )
        return result

    async def get_config(self, node: str, format_data: Union[bool, None] = None) -> SettingSpec:
        """|coro|

        Returns the config settings for a specific node.

        .. note::
            See :ref:`Setting Nodes <Documentation>` for more information.


        Parameters
        -----------
        node: :class:`str`
            The AMP node to inspect. eg "ADSModule.Networking.BaseURL"
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`SettingSpec`
            On success returns a :class:`SettingSpec` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"node": node}
        result: Any = await self._call_api(
            api="Core/GetConfig", parameters=parameters, format_data=format_data, format_=SettingSpec
        )
        return result

    async def get_configs(self, nodes: list[str], format_data: Union[bool, None] = None) -> list[SettingSpec]:
        """|coro|

        Returns the config settings for each node in the list.

        .. note::
            See :ref:`Setting Nodes <Documentation>` for more information.


        Parameters
        -----------
        node: list[:class:`str`]
            The list of setting nodes to look at.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`SettingSpec`]
            On success returns a list of :class:`SettingSpec` dataclasses.
        """

        await self._connect()
        parameters: dict[str, list[str]] = {"nodes": nodes}
        result: Any = await self._call_api(
            api="Core/GetConfigs", parameters=parameters, format_data=format_data, format_=SettingSpec
        )
        return result

    async def get_diagnostics_info(self, format_data: Union[bool, None] = None) -> Diagnostics:
        """|coro|

        Get's the system diagnostics information.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`Diagnostics`
            On success returns a :class:`Diagnostics` dataclass.

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
        """|coro|

        Returns the module information.


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`Module`
            On success returns a :class:`Module` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetModuleInfo", format_data=format_data, format_=Module)
        return result

    async def get_new_guid(self, format_data: Union[bool, None] = None) -> dict[str, Any]:
        """|coro|

        Get a new GUID for the Instance.

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
        """|coro|

        Retrieves the AMP Permissions node tree.

        Returns
        --------
        list[:class:`PermissionNode`]
            On success returns a :class:`PermissionNode` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetPermissionsSpec")
        return result

    async def get_port_summaries(self, format_data: Union[bool, None] = None) -> list[Port]:
        """|coro|

        Get a summary of the Instance's open ports.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`Port`]
            On success returns a list of :class:`Port` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetPortSummaries", format_data=format_data, format_=Port)
        if format_data is None:
            format_data = self.format_data

        if format_data is False:
            return result

        elif isinstance(result, list):
            return [Port(**port) for port in result]
        return result

    async def get_provision_spec(self, format_data: Union[bool, None] = None) -> list[SettingSpec]:
        """|coro|

        Returns the provisioning spec.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`SettingSpec`]
            On success returns a list of :class:`SettingSpec` dataclasses.
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
        """|coro|

        Get the remote login token.

        Parameters
        -----------
        description: Union[:class:`str`, None], optional
            You can set a description of what the token is for, defaults to None.
        is_temporary:  Union[:class:`bool`, None], optional
            If the token should be temporary, defaults to None.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`str`
            On success returns a :class:`str`.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Description": description, "IsTemporary": is_temporary}
        result: Any = await self._call_api(api="Core/GetRemoteLoginToken", parameters=parameters, format_data=format_data)
        return result

    async def get_role(self, role_id: str, format_data: Union[bool, None] = None) -> Role:
        """|coro|

        Retrieves the AMP Role information for the provided role ID.

        Parameters
        -----------
        role_id: :class:`str`
            The role ID to get information for.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`Role`
            On success returns a :class:`Role` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"RoleId": role_id}
        result: Any = await self._call_api(api="Core/GetRole", parameters=parameters, format_data=format_data, format_=Role)
        return result

    async def get_role_data(self, format_data: Union[bool, None] = None) -> list[Role]:
        """|coro|

        Get's a list of all the roles.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`Role`]
            On success returns a list of :class:`Role` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetRoleData", format_data=format_data, format_=Role)
        return result

    async def get_role_ids(self) -> dict[str, str]:
        """|coro|

        Retrieves all the Roles AMP currently has and the role IDs.

        Returns
        --------
        dict[str, str]
            On success returns a dictionary containing all the roles and their IDs.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetRoleIds")
        return result

    @overload
    async def get_schedule_data(self, format_data: Union[Literal[False], None]) -> ScheduleDataData: ...
    @overload
    async def get_schedule_data(self, format_data: Union[Literal[True], None]) -> ScheduleData: ...

    async def get_schedule_data(self, format_data: Union[bool, None] = None) -> ScheduleData | ScheduleDataData:
        """|coro|

        Returns a dictionary of the Server/Instance Schedule events and triggers.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ScheduleData` | :class:`ScheduleDataData`
            On success returns a :class:`ScheduleData` dataclass, unless format_data is False which it will return :class:`ScheduleDataData`.

        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetScheduleData", format_data=format_data, format_=ScheduleData)
        return result

    async def get_setting_spec(self, format_data: Union[bool, None] = None) -> SettingsSpecParent:
        """|coro|

        Retrieves a list of settings specifications that can be changed.

        .. note::
            See :ref:`Setting Nodes <Documentation>` for more information.

        Parameters
        ---------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`SettingSpecParent`
            On success returns a :class:`SettingSpecParent` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetSettingsSpec", format_data=format_data, format_=SettingsSpecParent, sanitize_json=True
        )
        return result

    async def get_setting_values(self, setting_node: str) -> dict[str, str]:
        """|coro|

        Returns the setting values.

        .. note::
            See :ref:`Setting Nodes <Documentation>` for more information.


        Parameters
        ----------
        setting_node: :class:`str`
            The setting node name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        dict[:class:`str`, :class:`str`]
            On success returns a dictionary of setting values.
        """

        await self._connect()
        parameters: dict[str, str] = {"SettingNode": setting_node}
        result: Any = await self._call_api(api="Core/GetSettingValues", parameters=parameters)
        return result

    async def get_status(self, format_data: Union[bool, None] = None) -> InstanceStatus:
        """|coro|

        Gets the AMP Instance/Application Status information.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`InstanceStatus`
            On success returns a :class:`InstanceStatus` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetStatus", format_data=format_data, format_=InstanceStatus)
        return result

    async def get_tasks(self, format_data: Union[bool, None] = None) -> list[RunningTask]:
        """|coro|

        Get a list of running tasks on the Instance.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`RunningTask`]
            On success returns a list of :class:`RunningTask` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetTasks", format_data=format_data, format_=RunningTask)
        return result

    async def get_time_interval_trigger(self, trigger_id: str, format_data: Union[bool, None] = None) -> TimedTrigger:
        """|coro|

        Gets a time interval trigger information.

        Parameters
        -----------
        trigger_id: :class:`str`
            The ID of the time interval trigger to get.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`TimedTrigger`
            On success returns a :class:`TimedTrigger` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Id": trigger_id}
        result: Any = await self._call_api(
            api="Core/GetTimeIntervalTrigger", parameters=parameters, format_data=format_data, format_=TimedTrigger
        )
        return result

    async def get_triggers(self) -> TriggerID:
        """|coro|

        Retrieves the available trigger IDs for the Instance and sets them as attributes tied to :attr:`triggers`.

        .. note::
            Each Instance has unique Trigger IDs. You can simply access the correct ID for the Trigger via :attr:`~Core.triggers.a_backup_has_started` as an example.
            This would return the ID string to be passed into a function that requires a Trigger ID value.

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
        """|coro|

        Gets the Update Version information for AMP.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`UpdateInfo`
            On success returns a :class:`UpdateInfo` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetUpdateInfo", format_data=format_data, format_=UpdateInfo)
        return result

    async def get_updates(self, format_data: Union[bool, None] = None) -> Updates:
        """|coro|

        Gets changes to the server status, in addition to any notifications or console output that have occurred since the last time meth:`get_updates` was called by the current session.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`Updates`
            On success returns a :class:`Updates` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetUpdates", format_data=format_data, format_=Updates)
        return result

    async def get_user_action_spec(self, format_data: Union[bool, None] = None) -> ActionSpec:
        """|coro|

        Get a specification of the user actions.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionSpec`
            On success returns a :class:`ActionSpec`.
        """
        await self._connect()
        result: Any = await self._call_api(api="Core/GetUserActionsSpec", format_data=format_data)
        return result

    async def get_user_info(self, user_id: str, format_data: Union[bool, None] = None) -> UserApplicationData:
        """|coro|

        Provides information about a given in-application user (as opposed to AMP Users).

        Parameters
        -----------
        user_id: :class:`str`
            The Application User id. See :meth:`get_user_list`
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`UserApplicationData`
            On success returns a :class:`UserApplicationData` class.
        """

        await self._connect()
        parameters: dict[str, str] = {"UID": user_id}
        result: Any = await self._call_api(
            api="Core/GetUserInfo", parameters=parameters, format_data=format_data, format_=UserApplicationData
        )
        return result

    async def get_user_list(self, format_data: Union[bool, None] = None) -> Players:
        """|coro|Players

        Returns the list of the connected users to the Application.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`Players`
            On success returns a :class:`Players` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="Core/GetUserList", format_data=format_data, format_=Players, _use_from_dict=False, _auto_unpack=False
        )
        return result

    async def get_webauthn_challenge(self, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

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
        """|coro|

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
        """|coro|

        Get the webauthn credential summaries.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[Any] : List of webauthn credential summaries.
        """

        await self._connect()
        result: Any = await self._call_api(api="Core/GetWebauthnCredentialSummaries", format_data=format_data)
        return result

    @deprecated("This was removed in `2.6.0.0`", stacklevel=2)
    async def get_webserver_metrics(self, format_data: Union[bool, None] = None) -> Any:
        """|coro|

        Gets the webserver metrics.


        .. versionremoved::  "2.6.0.0"


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        Any
            UNK data returned by the API.
        """

        await self._connect()
        try:
            await self.version_validation(version=VersionInfo(2, 6, 0, 0))
        except RuntimeError as e:
            return e

        result: Any = await self._call_api(api="Core/GetWebserverMetrics", format_data=format_data)
        return result

    async def kill_application(self) -> None:
        """|coro|

        Kills the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Returns
        --------
        None
        """

        await self._connect()
        await self._call_api(api="Core/Kill", _no_data=True)
        return

    @deprecated(
        "Function overlap with `ADSModule.kill_instance()`, please use `Core.kill_application()` instead.", stacklevel=2
    )
    async def kill_instance(self) -> None:
        """|coro|

        Kills the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Returns
        --------
        None
        """

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
        """|coro|

        AMP API login function.


        Parameters
        -----------
        amp_user: :class:`str`
            The username for logging into the AMP Panel
        amp_password: :class:`str`
            The password for logging into the AMP Panel
        token: :class:`str` , optional
            AMP 2 Factor auth code; typically using :meth:`TOTP.now`, defaults to "".
        rememberME: :class:`bool` , optional
            Remember me token, defaults to False.

        Returns
        --------
        :class:`LoginResults`
            On success returns a :class:`LoginResults` dataclass.

        """
        parameters = {"username": amp_user, "password": amp_password, "token": token, "rememberMe": rememberME}
        result: Any = await self._call_api(
            api="Core/Login", parameters=parameters, format_data=format_data, format_=LoginResults
        )
        return result

    async def logout(self) -> None:
        """|coro|

        Logout from AMP.

        Returns
        --------
        None
        """
        await self._connect()
        await self._call_api(api="Core/Logout", _no_data=True)
        return

    @Base.ads_only
    async def restart_amp(self) -> None:
        """|coro|

        Restart the AMP Instance

        Returns
        --------
        None
        """

        await self._connect()
        await self._call_api(api="Core/RestartAMP", _no_data=True)
        return

    async def resume_instance(self) -> None:
        """|coro|

        Allows the service to be re-started after previously being suspended.

        Returns
        --------
        None
        """
        await self._connect()
        await self._call_api(api="Core/Resume", _no_data=True)
        return

    async def refresh_setting_value_list(self, node: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Refreshes a setting nodes values.

        Parameters
        -----------
        name: :class:`str`
            The setting node name.
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
        """|coro|

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
        """|coro|

        Renames a role.

        Parameters
        -----------
        role_id: :class:`str`
            The ID of the role to rename.
        new_name: :class:`str`
            The new name for the role.
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
        """|coro|

        Restarts the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        warnings.warn(
            message="Core.restart_instance() is deprecated and scheduled for "
            "removal in a future version. Use Core.restart_application() instead to restart your Instance application.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return await self.restart_application(format_data=format_data)

    async def restart_application(self, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Restarts the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Parameters
        ----------
        format_data : Union[bool, None], optional
            Format the JSON response data. (Uses `FORMAT_DATA` global constant if None), by default None

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
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
        new_password: :class:`str`
            New password.
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

    async def revoke_webauthn_credential(self, auth_id: int, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Revoke a webauthn credential.

        Parameters
        -----------
        auth_id: :class:`int`
            The Web auth ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, int] = {"ID": auth_id}
        result: Any = await self._call_api(
            api="Core/RevokeWebauthnCredential", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def run_security_check(self, format_data: Union[bool, None] = None) -> Any:
        """|coro|

        Run a security check on the Instance.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        Any
        """
        # TODO - Need to get Proper data back.
        await self._connect()
        result: Any = await self._call_api(api="Core/RunSecurityCheck", format_data=format_data)
        return result

    async def run_event_trigger_immediately(self, trigger_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

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
        """|coro|

        Adds a user to an AMP role.

        Parameters
        -----------
        user_id: :class:`str`
            User ID to add to the role.
        role_id: :class:`str`
            Role ID to add the user to.
        is_member: :class:`bool`
            "True" to add the user to the role, "False" to remove the user from the role.
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
        """|coro|

        Set a permission node to "True" or "False" for the provided AMP role.

        Parameters
        -----------
        role_id: :class:`str`
            Role ID to add the user to.
        permission_node: :class:`str`
            AMP permission node. eg "Core.RoleManagement.DeleteRoles"
        enabled: Union[None, :class:`bool`], optional
            Set a permission to "True", "False" or "None" depending on the results you can disable or enable an entire tree node of permissions.
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

    async def set_trigger_enabled(
        self, trigger_id: str, enabled: bool, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Sets the enabled state of a trigger.

        Parameters
        -----------
        trigger_id: :class:`str`
            The ID of the trigger to edit.
        enabled: :class:`bool`
            The enabled state of the trigger to edit.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Id": trigger_id, "Enabled": enabled}
        result: Any = await self._call_api(
            api="Core/SetTriggerEnabled", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def send_console_message(self, msg: str) -> None:
        """|coro|

        Sends a message or command to the Console. (eg `/list`)

        Returns
        --------
        None
        """

        await self._connect()
        parameters: dict[str, str] = {"message": msg}
        await self._call_api(api="Core/SendConsoleMessage", parameters=parameters, _no_data=True)
        return

    async def set_configs(self, data: dict[str, str], format_data: Union[bool, None] = None) -> bool:
        """|coro|

        Set multiple Setting Nodes values.

        Parameters
        -----------
        data: dict[:class:`str`, :class:`str`]
            Dictionary of Setting Nodes to set.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        ---------
        :class:`bool`
            On success returns a boolean.
        """

        await self._connect()
        parameters: dict[str, dict[str, str]] = {"data": data}
        result: Any = await self._call_api(api="Core/SetConfigs", parameters=parameters, format_data=format_data)
        return result

    async def set_config(self, node: str, value: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Set a Setting Node value.

        Parameters
        -----------
        name: :class:`str`
            Setting node name.
        value: :class:`str`
            Config node value.
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
        """|coro|

        Starts the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

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
        result: Any = await self._call_api(api="Core/Start", format_data=format_data, format_=ActionResult)
        return result

    async def stop_application(self) -> None:
        """|coro|

        Stops the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Returns
        --------
        None
        """

        await self._connect()
        await self._call_api(api="Core/Stop", _no_data=True)
        return

    async def suspend_instance(self) -> None:
        """|coro|

        Prevents the current instance from being started, and stops it if it's currently running.

        Returns
        --------
        None
        """

        await self._connect()
        await self._call_api(api="Core/Suspend")
        return

    async def update_account_info(
        self, email_address: str, two_factor_pin: str, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Update account info.

        .. note::
            All these settings take affect on the account logged in via the API.


        Parameters
        -----------
        email_address: :class:`str`
            The new Email address.
        two_factor_pin: :class:`str`
            Two factor PIN.
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
        """|coro|

        Upgrade the current AMP Instance.

         .. warning::
            The Instance must be an ADS or Controller.


        Returns
        --------
        None
        """

        await self._connect()
        await self._call_api(api="Core/UpgradeAMP", _no_data=True)
        return

    @Base.ads_only
    async def update_amp_instance(self) -> None:
        """|coro|

        Updates the ADS Instance.

        .. warning::
            The Instance must be an ADS or Controller.


        Returns
        --------
        None
        """

        await self._connect()
        await self._call_api(api="Core/UpdateAMPInstance", _no_data=True)
        return

    async def update_application(self, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

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
        username: str,
        disabled: bool = False,
        password_expires: bool = False,
        cannot_change_password: bool = False,
        must_change_password: bool = False,
        email_address: str = "",
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Update an AMP user.

        Parameters
        -----------
        username: :class:`str`
            The AMP user to update.
        disabled: :class:`bool`, optional
            If the AMP user should be disabled, defaults to False.
        password_expires: :class:`bool`, optional
            If the AMP user password should expire, defaults to False.
        cannot_change_password: :class:`bool`, optional
            The AMP user cannot change their password, defaults to False.
        must_change_password: :class:`bool`, optional
            The AMP user must change password upon next login, defaults to False.
        email_address: :class:`str`, optional
            The email address to set for the AMP user, defaults to "".
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {
            "Username": username,
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
        """|coro|

        Webauthn register.

        .. note::
            Unknown usage.


        Parameters
        -----------
        attestation_object: :class:`str`
            Attestation object.
        client_data_json: :class:`str`
            Client data JSON.
        description: :class:`str`
            Description.
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
