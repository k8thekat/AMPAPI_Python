"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMPAPI_Python.

AMPAPI_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMPAPI_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMPAPI_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Optional, Union, Unpack

from pyotp import TOTP
from typing_extensions import deprecated

from ._types import (
    ACTION_RESULT_EXCLUDED_KEYS,
    ACTION_RESULT_REQUIRED_KEYS,
    LICENCE_INFO_EXCLUDED_KEYS,
    LICENCE_INFO_REQUIRED_KEYS,
    RUNNING_TASK_EXCLUDED_KEYS,
    RUNNING_TASK_REQUIRED_KEYS,
    SCHEDULE_DATA_EXCLUDED_KEYS,
    SCHEDULE_DATA_REQUIRED_KEYS,
    SECURITY_CHECK_EXCLUDED_KEYS,
    SECURITY_CHECK_REQUIRED_KEYS,
    SETTINGS_SPEC_PARENT_EXCLUDED_KEYS,
    SETTINGS_SPEC_PARENT_REQUIRED_KEYS,
    STATUS_EXCLUDED_KEYS,
    STATUS_REQUIRED_KEYS,
    TIMED_TRIGGER_EXCLUDED_KEYS,
    TIMED_TRIGGER_REQUIRED_KEYS,
    TWO_FACTOR_SETUP_INFO_EXCLUDED_KEYS,
    TWO_FACTOR_SETUP_INFO_REQUIRED_KEYS,
    USER_APPLICATION_DATA_EXCLUDED_KEYS,
    USER_APPLICATION_DATA_REQUIRED_KEYS,
    WEBAUTHN_CREDENTIAL_IDS_EXCLUDED_KEYS,
    WEBAUTHN_CREDENTIAL_IDS_REQUIRED_KEYS,
    ActionResultResponse,
    LicenceInfoResponse,
    LicenceResultResponse,
    RunningTaskResponse,
    ScheduleDataResponse,
    SecurityCheckResponse,
    SettingsSpecParentResponse,
    StatusResponse,
    TimedTriggerResponse,
    TwoFactorSetupInfoResponse,
    TwoFactorSetupResultResponse,
    UserApplicationDataResponse,
    WebauthnCredentialIDsResponse,
    is_response_list,
    is_response_type,
)
from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPIKeyError, AMPAPITypeError
from .modules import (
    ActionResult,
    AuditLogEntry,
    BuildInfo,
    Diagnostics,
    LicenceInfo,
    LoginResults,
    LoginUserInfo,
    Module,
    PermissionNode,
    Players,
    Port,
    Role,
    RunningTask,
    ScheduleData,
    SecurityCheck,
    Session,
    SettingSpec,
    SettingsSpecParent,
    Status,
    StructuredDiagnostics,
    TimedTrigger,
    TriggerID,
    TwoFactorSetupInfo,
    UpdateInfo,
    Updates,
    UserApplicationData,
    UserInfo,
)

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

    from . import modules
    from ._types import (
        ActionSpec,
        APISpec,
        AuditLogEntryResponse,
        DiagnosticsResponse,
        LoginResultsResponse,
        LoginUserInfoResponse,
        ModuleResponse,
        PermissionNodeResponse,
        PortResponse,
        RoleResponse,
        SessionResponse,
        SettingSpecResponse,
        StructuredDiagnosticsResponse,
        TriggersResponse,
        UpdateInfoResponse,
        UpdatesResponse,
        UserInfoResponse,
    )

__all__ = ("Core",)


class Core(Base):
    """Contains the functions for any ``/API/Core/`` AMP API endpoints.

    .. note::
        If the ``format_data`` parameter is None on any function; the global ``FORMAT_DATA`` will be used instead.


    """

    @property
    def triggers(self) -> TriggerID:
        """You can access all the trigger IDs an Instance has via this attribute. See :class:`TriggerID` for more information."""
        try:
            return self._triggers
        except AttributeError:
            err = "You need to first call function <Core.get_triggers()> before accessing this attribute."
            raise AttributeError(err) from AttributeError

    async def _create_test_task(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        **DEV**: Creates a non-ending task with 50% progress for testing purposes

        Endpoint: `Core/CreateTestTask`

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
            None: ""

        """
        await self._reauth()
        return await self._post(url="Core/CreateTestTask", no_data=True, request_params=request_params, **response_params)

    async def _async_test(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> str:
        """|coro|

        **DEV**: Async test method

        Endpoint: `Core/AsyncTest`

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`str`
            Returns a string.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(url="Core/AsyncTest", request_params=request_params, **response_params)
        if isinstance(result, str):
            return result
        raise AMPAPITypeError(end_point="Core/AsyncTest", cur_type=result, expec_type=str)

    async def acknowledge_amp_update(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Approve an AMP update.

        Endpoint: `Core/AcknowledgeAMPUpdate`

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
        return await self._post(url="Core/AcknowledgeAMPUpdate", no_data=True, request_params=request_params, **response_params)

    async def activate_amp_license(
        self,
        license_key: str,
        query_only: bool = False,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> LicenceInfo | LicenceInfoResponse:
        """|coro|

        Activate an AMP License key.

        Endpoint: `Core/ActivateAMPLicence`

        .. warning::
            AMP sends the licence key back in the answer.

        .. versionchanged:: 5.0.0
            Returns the :class:`LicenceInfo` AMP sends, not the :class:`ActionResult` around it.

        Parameters
        ----------
        license_key : :class:`str`
            Your AMP License key.
        query_only : bool, optional
            UNK, by default False.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`LicenceInfo`
            On success returns a :class:`LicenceInfo` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str | bool] = {"LicenceKey": license_key, "QueryOnly": query_only}
        result: ResponseAliasFull = await self._post(
            url="Core/ActivateAMPLicence",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/ActivateAMPLicence", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, LicenceResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/ActivateAMPLicence", cur_type=result, expec_type=dict)

        # The spec types this `ActionResult<JObject>`. The licence is in `result`, and a failure has already raised.
        licence: Any = result.get("result")
        if not is_response_type(licence, LicenceInfoResponse, LICENCE_INFO_REQUIRED_KEYS, LICENCE_INFO_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/ActivateAMPLicence", cur_type=licence, expec_type=dict)
        if format_data is True:
            return LicenceInfo.from_response(licence)
        return licence

    async def add_event_trigger(
        self,
        trigger_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Add an Event Trigger to an Instance.

        Endpoint: `Core/AddEventTrigger`

        .. note::
            See :attr:`Triggers.id`; which you can get a list of triggers from the documentation.


        Parameters
        ----------
        trigger_id : :class:`str`
            The Trigger ID.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"TriggerId": trigger_id}
        result: ResponseAliasFull = await self._post(
            url="Core/AddEventTrigger",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/AddEventTrigger", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/AddEventTrigger", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def add_interval_trigger(
        self,
        months: list[int],
        days: list[int],
        hours: list[int],
        minutes: list[int],
        days_of_month: list[int],
        description: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Add an Interval Trigger to an Instance.

        Endpoint: `Core/AddIntervalTrigger`

        .. note::
            Requires the ``Core.Scheduler.CreateTrigger`` permission.
            See :meth:`edit_interval_trigger` for the same fields on an existing trigger.


        Parameters
        ----------
        months : list[:class:`int`]
            The months of the year the trigger runs in. Range 1 to 12.
        days : list[:class:`int`]
            The days of the week the trigger runs on, the first day of the week is Monday. Range is 0 to 7.
        hours : list[:class:`int`]
            The hours of the day the trigger runs at. Range is 0 to 23.
        minutes : list[:class:`int`]
            The minutes of the hour the trigger runs at. Range is 0 to 59.
        days_of_month : list[:class:`int`]
            The days of the month the trigger runs on. Range is 1 to 31.
        description : :class:`str`
            The description of the Interval Trigger.
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
        parameters: dict[str, Any] = {
            "months": months,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "daysOfMonth": days_of_month,
            "description": description,
        }
        result: ResponseAliasFull = await self._post(
            url="Core/AddIntervalTrigger",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/AddIntervalTrigger", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/AddIntervalTrigger", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def add_task(
        self,
        trigger_id: str,
        method_id: str,
        parameter_mapping: dict[str, str],
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Add a task.

        Endpoint: `Core/AddTask`

        This requires knowing the structure of the Method IDs
        - See http://ampapi-python.readthedocs.io/en/latest/events/method_events.html

        .. note::
            Example -> ``parameter_mapping = { "Subtitle": "Hello World", Title: "Hello {@UserID}" }``


        Parameters
        ----------
        trigger_id : class:`str`
            The ID of the trigger to add.
        method_id : class:`str`
            The Task method name. eg. ```Event.MinecraftModule.SendGlobalTitle``
        parameter_mapping : :class:dict[:class:`str`, :class:`str`]
            The parameters to be populated related to the trigger_id/method_id.\n
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"TriggerID": trigger_id, "MethodID": method_id, "ParameterMapping": parameter_mapping}
        result: ResponseAliasFull = await self._post(
            url="Core/AddTask",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/AddTask", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/AddTask", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def cancel_task(
        self,
        task_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Cancel an existing Task.

        Endpoint: `Core/CancelTask`

        Parameters
        ----------
        task_id : :class:`str`
            The ID of the Task.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"TaskId": task_id}
        result: ResponseAliasFull = await self._post(
            url="Core/CancelTask",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/CancelTask", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/CancelTask", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def change_user_password(
        self,
        username: str,
        old_password: str,
        new_password: str,
        two_factor_pin: str = "",
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Change a AMP Users password.

        Endpoint: `Core/ChangeUserPassword`

        .. note::
            Requires having the old password.

        Parameters
        ----------
        username : :class:`str`
            The AMP user name.
        old_password : :class:`str`
            Current AMP user password.
        new_password : :class:`str`
             New AMP user password.
        two_factor_pin : :class:`str`
            Two Factor PIN, if enabled. Defaults to "".
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {
            "Username": username,
            "OldPassword": old_password,
            "NewPassword": new_password,
            "TwoFactorPIN": two_factor_pin,
        }
        result: ResponseAliasFull = await self._post(
            url="Core/ChangeUserPassword",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/ChangeUserPassword", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/ChangeUserPassword", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def change_task_order(
        self,
        trigger_id: str,
        task_id: str,
        new_order: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Change the order of a task.

        Endpoint: `Core/ChangeTaskOrder`

        Parameters
        ----------
        trigger_id : :class:`str`
            The ID of the Trigger you want to change the order of a task.
        task_id : :class:`str`
            The ID of the task to modify. See :meth:`get_schedule_data` to get IDs
        new_order : :class:`int`
            The new task position.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"TriggerID": trigger_id, "TaskID": task_id, "NewOrder": new_order}
        result: ResponseAliasFull = await self._post(
            url="Core/ChangeTaskOrder",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/ChangeTaskOrder", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/ChangeTaskOrder", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def confirm_two_factor_setup(
        self,
        username: str,
        two_factor_code: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Completes two-factor setup by supplying a valid two factor code based on the secret provided by EnableTwoFactor.

        Endpoint: `Core/ConfirmTwoFactorSetup`

        Parameters
        ----------
        username : :class:`str`
            The AMP User name to confirm 2FA setup.
        two_factor_code : :class:`str`
            Two factor code.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Username": username, "TwoFactorCode": two_factor_code}
        result: ResponseAliasFull = await self._post(
            url="Core/ConfirmTwoFactorSetup",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/ConfirmTwoFactorSetup", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/ConfirmTwoFactorSetup", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def convert_user_to_oidc(
        self,
        username: str,
        oidc_sub: Union[str, None] = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Convert an AMP User to sign in through OIDC.

        Endpoint: `Core/ConvertUserToOIDC`

        .. note::
            Requires the ``Core.UserManagement.UpdateUserInfo`` permission.


        Parameters
        ----------
        username : :class:`str`
            The AMP User name.
        oidc_sub : Union[:class:`str`, None], optional
            The OIDC subject to link to the AMP User, by default None.
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
        parameters: dict[str, Any] = {"Username": username}
        if oidc_sub is not None:
            parameters["OIDCSub"] = oidc_sub
        result: ResponseAliasFull = await self._post(
            url="Core/ConvertUserToOIDC",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/ConvertUserToOIDC", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/ConvertUserToOIDC", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def create_role(
        self,
        role_name: str,
        as_common_role: bool = False,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Creates an AMP Role.

        Endpoint: `Core/CreateRole`

        Parameters
        ----------
        role_name : :class:`str`
            The name you want for the AMP role.
        as_common_role : :class:`bool`, optional
            A role that everyone has, defaults to False.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"Name": role_name, "AsCommonRole": as_common_role}
        result: ResponseAliasFull = await self._post(
            url="Core/CreateRole",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/CreateRole", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/CreateRole", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def create_user(
        self,
        username: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Create an AMP user.

        Endpoint: `Core/CreateUser`

        Parameters
        ----------
        username : :class:`str`
            The AMP User name.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Username": username}
        result: ResponseAliasFull = await self._post(
            url="Core/CreateUser",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/CreateUser", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/CreateUser", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def current_session_has_permission(
        self,
        node: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> bool:
        """|coro|

        Retrieves the current Session IDs permissions. This will differ between the ADS and a Server/Instance.

        Endpoint: `Core/CurrentSessionHasPermission`

        .. note::
            Supports looking for a blocked permission node simply by appending ``-`` in front of the permission node.
            - eg ``-Core.RoleManagement.DeleteRoles``, also supports wildcards ``*``. eg ``Core.RoleManagement.*``



        Parameters
        ----------
        node : :class:`str`
            The permission node to check for. eg ``Core.RoleManagement.DeleteRoles``. \n
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`bool`

        """
        await self._reauth()
        parameters: dict[str, str] = {"PermissionNode": node}
        result: ResponseAliasFull = await self._post(
            url="Core/CurrentSessionHasPermission",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, bool):
            raise AMPAPITypeError(end_point="Core/CurrentSessionHasPermission", cur_type=result, expec_type=bool)
        return result

    async def delete_instance_users(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete an Instances User list.

        Endpoint: `Core/DeleteInstanceUsers`

        Parameters
        ----------
        instance_id : :class:`str`
            The AMP Instance ID.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"InstanceId": instance_id}
        result: ResponseAliasFull = await self._post(
            url="Core/DeleteInstanceUsers",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/DeleteInstanceUsers", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/DeleteInstanceUsers", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def delete_role(
        self,
        role_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Deletes a role.

        Endpoint: `Core/DeleteRole`

        Parameters
        ----------
        role_id : :class:`str`
            The ID of the role to delete.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"RoleId": role_id}
        result: ResponseAliasFull = await self._post(
            url="Core/DeleteRole",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/DeleteRole", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/DeleteRole", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def delete_task(
        self,
        trigger_id: str,
        task_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete a task.

        Endpoint: `Core/DeleteTask`

        Parameters
        ----------
        trigger_id : :class:`str`
            The ID of the trigger to delete.
        task_id : :class:`str`
            The ID of the task to delete. See :meth:`get_schedule_data` and check the :class:`Tasks` class to get IDs.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"TriggerID": trigger_id, "TaskID": task_id}
        result: ResponseAliasFull = await self._post(
            url="Core/DeleteTask",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/DeleteTask", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/DeleteTask", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def delete_trigger(
        self,
        trigger_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete a trigger.

        Endpoint: `Core/DeleteTrigger`

        Parameters
        ----------
        trigger_id : :class:`str`
            The ID of the trigger to delete.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"TriggerID": trigger_id}
        result: ResponseAliasFull = await self._post(
            url="Core/DeleteTrigger",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/DeleteTrigger", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/DeleteTrigger", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def delete_user(
        self,
        username: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete an AMP user.

        Endpoint: `Core/DeleteUser`

        Parameters
        ----------
        username : :class:`str`
            The AMP User name.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Username": username}
        result: ResponseAliasFull = await self._post(
            url="Core/DeleteUser",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/DeleteUser", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/DeleteUser", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def disable_two_factor(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Disables two-factor authentication for the currently logged in AMP User.

        Endpoint: `Core/DisableTwoFactor`

        .. warning::
            This applies to the AMP User name supplied to interact with the API.

        .. note::
            This will use the pre-existing :class:`Bridge` password and token.


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
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Password": self._bridge.password, "TwoFactorCode": TOTP(self._bridge.token).now()}
        result: ResponseAliasFull = await self._post(
            url="Core/DisableTwoFactor",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/DisableTwoFactor", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/DisableTwoFactor", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def dismiss_all_tasks(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Dismiss all task notifications.

        Endpoint: `Core/DismissAllTasks`

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
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/DismissAllTasks",
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/DismissAllTasks", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/DismissAllTasks", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def dismiss_task(
        self,
        task_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Dismiss a task notification.

        Endpoint: `Core/DismissTask`

        Parameters
        ----------
        task_id : :class:`str`
            The ID of the task to delete. See :meth:`get_schedule_data` and check the :class:`Tasks` class to get IDs.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"TaskId": task_id}
        result: ResponseAliasFull = await self._post(
            url="Core/DismissTask",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/DismissTask", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/DismissTask", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
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
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Edits an interval trigger.

        Endpoint: `Core/EditIntervalTrigger`

        Parameters
        ----------
        trigger_id : :class:`str`
            The ID of the interval trigger to edit.
        months : :class:`int`
            The number of the month you want the trigger to run. Range 1 to 12.
        days : :class:`int`
            The days of the interval trigger to edit, the first day of the week is Monday. Range is 0 to 7.
        hours : :class:`int`
            The hours of the interval trigger to edit. Range is 0 to 23.
        minutes : :class:`int`
            The minutes of the interval trigger to edit. Range is 0 to 59.
        days_of_month : :class:`int`
            The days of the month of the interval trigger to edit. Range is 1 to 31.
        description : :class:`str`
            The description of the interval trigger to edit.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default ``None``.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        if months < 1 or months > 12:
            msg = "Months must be between 1 and 12."
            raise ValueError(msg)
        if days < 0 or days > 7:
            msg = "Days must be between 0 and 7."
            raise ValueError(msg)
        if hours < 0 or hours > 23:
            msg = "Hours must be between 0 and 23."
            raise ValueError(msg)
        if minutes < 0 or minutes > 59:
            msg = "Minutes must be between 0 and 59."
            raise ValueError(msg)
        if days_of_month < 1 or days_of_month > 31:
            msg = "Days of month must be between 1 and 31."
            raise ValueError(msg)

        parameters: dict[str, Any] = {
            "Id": trigger_id,
            "months": months,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "daysOfMonth": days_of_month,
            "description": description,
        }
        result: ResponseAliasFull = await self._post(
            url="Core/EditIntervalTrigger",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/EditIntervalTrigger", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/EditIntervalTrigger", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def edit_task(
        self,
        trigger_id: str,
        task_id: str,
        parameter_mapping: dict[str, str],
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Edit a task.

        Endpoint: `Core/EditTask`

        Parameters
        ----------
        trigger_id : :class:`str`
             The ID of the trigger to edit.
        task_id : :class:`str`
            The ID of the task to edit. See :meth:`get_schedule_data` to get IDs.
        parameter_mapping : dict[:class:`str`, :class:`str`]:
            The parameters to be updated on the task.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"TriggerID": trigger_id, "TaskID": task_id, "ParameterMapping": parameter_mapping}
        result: ResponseAliasFull = await self._post(
            url="Core/EditTask",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/EditTask", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/EditTask", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def enable_two_factor(
        self,
        username: str,
        password: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> TwoFactorSetupInfo | TwoFactorSetupInfoResponse:
        """|coro|

        Sets up two-factor authentication for the given user.

        Endpoint: `Core/EnableTwoFactor`

        .. warning::
            ConfirmTwoFactorSetup must be invoked to complete setup.

        .. versionchanged:: 5.0.0
            Returns the :class:`TwoFactorSetupInfo` AMP sends, not the :class:`ActionResult` around it.


        Parameters
        ----------
        username : :class:`str`
            The AMP User name.
        password : :class:`str`
            The AMP Users password.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`TwoFactorSetupInfo`
            On success returns a :class:`TwoFactorSetupInfo` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Username": username, "Password": password}
        result: ResponseAliasFull = await self._post(
            url="Core/EnableTwoFactor",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/EnableTwoFactor", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, TwoFactorSetupResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/EnableTwoFactor", cur_type=result, expec_type=dict)

        # The spec types this `ActionResult<TwoFactorSetupInfo>`. The setup data is in `result`, and a failure has already raised.
        setup: Any = result.get("result")
        if not is_response_type(
            setup,
            TwoFactorSetupInfoResponse,
            TWO_FACTOR_SETUP_INFO_REQUIRED_KEYS,
            TWO_FACTOR_SETUP_INFO_EXCLUDED_KEYS,
        ):
            raise AMPAPITypeError(end_point="Core/EnableTwoFactor", cur_type=setup, expec_type=dict)
        if format_data is True:
            return TwoFactorSetupInfo.from_response(setup)
        return setup

    @Base.ads_only
    async def end_user_session(
        self,
        session_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Closes the specified User's session ID to AMP.

        Endpoint: `Core/EndUserSession`

        .. warning::
            The Instance must be an ADS or Controller.


        Parameters
        ----------
        session_id : :class:`str`
            The AMP Session ID to close.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"Id": session_id}
        return await self._post(
            url="Core/EndUserSession",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @Base.ads_only
    async def get_active_amp_sessions(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Session] | list[SessionResponse]:
        """|coro|

        Returns currently active AMP Sessions.

        Endpoint: `Core/GetActiveAMPSessions`

        .. warning::
            The Instance must be an ADS or Controller.



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
        list[:class:`Session`]
            On success returns a list of :class:`Session` dataclasses.

        """
        await self._reauth()
        result = await self._post(
            url="Core/GetActiveAMPSessions",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetActiveAMPSessions", cur_type=result, expec_type=list)

        if format_data is None:
            format_data = self.format_data

        if format_data is True:
            return [Session.from_response(entry) for entry in result]
        return result

    async def get_all_amp_user_info(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[UserInfo] | list[UserInfoResponse]:
        """|coro|

        Retrieves all AMP Users and their information.

        Endpoint: `Core/GetAllAMPUserInfo`

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
        list[:class:`UserInfo`]
            On success returns a list of :class:`UserInfo` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetAllAMPUserInfo",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetAllAMPUserInfo", cur_type=result, expec_type=list)

        if format_data is None:
            format_data = self.format_data

        if format_data is True:
            return [UserInfo.from_response(entry) for entry in result]
        return result

    async def get_amp_role_permissions(
        self,
        role_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[str]:
        """|coro|

        Retrieves the AMP Role permission nodes for the provided role ID.

        Endpoint: `Core/GetAMPRolePermissions`

        Parameters
        ----------
        role_id : :class:`str`
            The role ID. eg "5d6566e0-fae2-41d7-bfb6-d21033247f2e"
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`str`]
            On success returns a list of strings containing all the permission nodes for the provided role ID.

        """
        await self._reauth()
        parameters: dict[str, str] = {"RoleId": role_id}
        result: ResponseAliasFull = await self._post(
            url="Core/GetAMPRolePermissions",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetAMPRolePermissions", cur_type=result, expec_type=list)
        return result

    async def get_amp_user_info(
        self,
        name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> UserInfo | UserInfoResponse:
        """|coro|

        Retrieves the AMP User information for the provided username.\n

        Endpoint: `Core/GetAMPUserInfo`

        Parameters
        ----------
        name : :class:`str`
            The AMP User name.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`UserInfo`
            On success returns a :class:`UserInfo` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Username": name}
        result: ResponseAliasFull = await self._post(
            url="Core/GetAMPUserInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetAMPUserInfo", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if "is_super_user" not in result:  # 'is_super_user' uniquely identifies UserInfoResponse in the union
            raise AMPAPITypeError(end_point="Core/GetAMPUserInfo", cur_type=result, expec_type=dict)
        if format_data is True:
            return UserInfo.from_response(result)
        return result

    async def get_amp_users_summary(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[LoginUserInfo] | list[LoginUserInfoResponse]:
        """|coro|

        Get all AMP users summary.

        Endpoint: `Core/GetAMPUsersSummary`

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
        list[:class:`LoginUserInfo`]
            On success returns a list of :class:`LoginUserInfo` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetAMPUsersSummary",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetAMPUsersSummary", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [LoginUserInfo.from_response(item) for item in result]
        return result

    async def get_api_spec(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> APISpec:
        """|coro|

        Get's all the API specs for the Instance.

        Endpoint: `Core/GetAPISpec`

        .. note::
            See :ref:`API Reference <Documentation>` for more information.

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :data:`APISpec`
            On success returns a dictionary with all of the API specs, their parameters and return types for the Instance.
            Each key is a module name, holding a dictionary of its methods as :class:`APISpecEndpointData`.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetAPISpec",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetAPISpec", cur_type=result, expec_type=dict)
        return result  # pyright: ignore[reportReturnType]

    async def get_audit_log_entries(
        self,
        before: float = datetime.datetime.now(tz=datetime.UTC).timestamp(),
        count: int = 10,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[AuditLogEntry] | list[AuditLogEntryResponse]:
        """|coro|

        Returns the last ``count`` number of audit log entries.

        Endpoint: `Core/GetAuditLogEntries`

        .. note::
            These are anything in the Console of the Controller/ADS such as login events or API calls.


        Parameters
        ----------
        before : :class:`float`
            A POSIX timestamp, defaults to datetime.now(tz=timezone.utc).timestamp().
        count : :class:`int`
            Number of entries to return, default is 10.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`AuditLogEntry`]
            On success returns a list of :class:`AuditLogEntry` dataclasses.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"Before": before, "Count": count}
        result: ResponseAliasFull = await self._post(
            url="Core/GetAuditLogEntries",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetAuditLogEntries", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [AuditLogEntry.from_response(item) for item in result]
        return result

    async def get_authentication_requirements(
        self,
        username: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Any]:
        """|coro|

        Get a list of Authentication requirements for the AMP user.

        Endpoint: `Core/GetAuthenticationRequirements`

        Parameters
        ----------
        username : :class:`str`
            The AMP username.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[Any]
            On success returns a list of Authentication requirements.

        """
        await self._reauth()
        parameters: dict[str, str] = {"username": username}
        result: ResponseAliasFull = await self._post(
            url="Core/GetAuthenticationRequirements",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetAuthenticationRequirements", cur_type=result, expec_type=list)
        return result

    async def get_config(
        self,
        node: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> SettingSpec | SettingSpecResponse:
        """|coro|

        Returns the config settings for a specific node.

        Endpoint: `Core/GetConfig`

        .. note::
            See :ref:`Setting Nodes <Documentation>` for more information.


        Parameters
        ----------
        node : :class:`str`
            The AMP node to inspect. eg "ADSModule.Networking.BaseURL"
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`SettingSpec`
            On success returns a :class:`SettingSpec` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"node": node}
        result: ResponseAliasFull = await self._post(
            url="Core/GetConfig",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetConfig", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if "subcategory" in result:
            if format_data is True:
                return SettingSpec.from_response(result)
            return result

        raise AMPAPIKeyError("subcategory", "Core/GetConfig", result)  # noqa: EM101

    async def get_configs(
        self,
        nodes: list[str],
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[SettingSpec] | list[SettingSpecResponse]:
        """|coro|

        Returns the config settings for each node in the list.

        Endpoint: `Core/GetConfigs`

        .. note::
            See :ref:`Setting Nodes <Documentation>` for more information.


        Parameters
        ----------
        nodes : list[:class:`str`]
            The list of setting nodes to look at.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`SettingSpec`]
            On success returns a list of :class:`SettingSpec` dataclasses.

        """
        await self._reauth()
        parameters: dict[str, list[str]] = {"nodes": nodes}
        result: ResponseAliasFull = await self._post(
            url="Core/GetConfigs",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetConfigs", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [SettingSpec.from_response(item) for item in result]
        return result

    async def get_diagnostics_info(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Diagnostics | DiagnosticsResponse:
        """|coro|

        Get's the system diagnostics information.

        Endpoint: `Core/GetDiagnosticsInfo`

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
        :class:`Diagnostics`
            On success returns a :class:`Diagnostics` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetDiagnosticsInfo",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetDiagnosticsInfo", cur_type=result, expec_type=dict)

        if "cpu_model" not in result:  # 'cpu_model' uniquely identifies DiagnosticsResponse in the union
            raise AMPAPITypeError(end_point="Core/GetDiagnosticsInfo", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if format_data is True:
            return Diagnostics.from_response(result)
        return result

    async def get_module_info(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> modules.Module | ModuleResponse:
        """|coro|

        Returns the module information.

        Endpoint: `Core/GetModuleInfo`

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
        :class:`~ampapi.modules.Module`
            On success returns a :class:`~ampapi.modules.Module` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetModuleInfo",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetModuleInfo", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if "app_name" not in result:  # 'app_name' uniquely identifies ModuleResponse in the union
            raise AMPAPITypeError(end_point="Core/GetModuleInfo", cur_type=result, expec_type=dict)
        if format_data is True:
            return Module.from_response(result)
        return result

    async def get_new_guid(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> str:
        """|coro|

        Get a new GUID for the Instance.

        Endpoint: `Core/GetNewGuid`

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`str`
            On success returns the new GUID.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetNewGuid",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, str):
            raise AMPAPITypeError(end_point="Core/GetNewGuid", cur_type=result, expec_type=str)
        return result

    async def get_oidc_login_url(
        self,
        redirect_uri: Union[str, None] = None,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> str:
        """|coro|

        Interacts with OIDC credentials.

        Endpoint: `Core/GetOIDCLoginURL`

        __Endpoint__: "Core/GetOIDCLoginURL"

        Parameters
        ----------
        redirect_uri : Union[:class:`str`, None], optional
            UNK, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`str`
            The OIDC login URL.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"redirect_uri": redirect_uri}
        result: ResponseAliasFull = await self._post(
            url="Core/GetOIDCLoginURL",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, str):
            raise AMPAPITypeError(end_point="Core/GetOIDCLoginURL", cur_type=result, expec_type=str)
        return result

    async def get_oidc_logout_url(
        self,
        redirect_uri: str | None = None,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> str:
        """|coro|

        Interacts with OIDC credentials.

        Endpoint: `Core/GetOIDCLogoutUrl`

        __Endpoint__: "Core/GetOIDCLogoutUrl"

        Parameters
        ----------
        redirect_uri : :class:`str | None`, optional
            UNK, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`str`
            The OIDC logout URL.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"redirect_uri": redirect_uri}
        result: ResponseAliasFull = await self._post(
            url="Core/GetOIDCLogoutUrl",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, str):
            raise AMPAPITypeError(end_point="Core/GetOIDCLogoutUrl", cur_type=result, expec_type=str)
        return result

    async def get_permissions_spec(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[PermissionNode] | list[PermissionNodeResponse]:
        """|coro|

        Retrieves the AMP Permissions node tree.

        Endpoint: `Core/GetPermissionsSpec`

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
        list[:class:`PermissionNode`]
            On success returns a list of :class:`PermissionNode` dataclasses, each holding its children.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetPermissionsSpec",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetPermissionsSpec", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [PermissionNode.from_response(item) for item in result]
        return result

    async def get_port_summaries(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Port] | list[PortResponse]:
        """|coro|

        Get a summary of the Instance's open ports.

        Endpoint: `Core/GetPortSummaries`

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
        list[:class:`Port`]
            On success returns a list of :class:`Port` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetPortSummaries",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetPortSummaries", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [Port.from_response(port) for port in result]
        return result

    async def get_provision_spec(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[SettingSpec] | list[SettingSpecResponse]:
        """|coro|

        Returns the provisioning spec.

        Endpoint: `Core/GetProvisionSpec`

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
        list[:class:`SettingSpec`]
            On success returns a list of :class:`SettingSpec` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetProvisionSpec",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetProvisionSpec", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [SettingSpec.from_response(item) for item in result]
        return result

    async def get_remote_login_token(
        self,
        description: Union[str, None] = None,
        is_temporary: Union[bool, None] = None,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> str:
        """|coro|

        Get the remote login token.

        Endpoint: `Core/GetRemoteLoginToken`

        Parameters
        ----------
        description : Union[:class:`str`, None], optional
            You can set a description of what the token is for, defaults to None.
        is_temporary : Union[:class:`bool`, None], optional
            If the token should be temporary, defaults to None.

            .. versionchanged:: 5.0.0
                Left out of the request when None, which AMP takes as its default. AMP rejects a null.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`str`
            On success returns a :class:`str`.

        """
        await self._reauth()
        # parameters: dict[str, Any] = {"Description": description, "IsTemporary": is_temporary}
        # Both are optional to AMP, but a null `IsTemporary` fails, so a parameter left as None isn't sent.
        parameters: dict[str, Any] = {}
        if description is not None:
            parameters["Description"] = description
        if is_temporary is not None:
            parameters["IsTemporary"] = is_temporary
        result: ResponseAliasFull = await self._post(
            url="Core/GetRemoteLoginToken",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, str):
            raise AMPAPITypeError(end_point="Core/GetRemoteLoginToken", cur_type=result, expec_type=str)
        return result

    async def get_role(
        self,
        role_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Role | RoleResponse:
        """|coro|

        Retrieves the AMP Role information for the provided role ID.

        Endpoint: `Core/GetRole`

        Parameters
        ----------
        role_id : :class:`str`
            The role ID to get information for.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`Role`
            On success returns a :class:`Role` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"RoleId": role_id}
        result: ResponseAliasFull = await self._post(
            url="Core/GetRole",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetRole", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if "is_common_role" not in result:  # 'is_common_role' uniquely identifies RoleResponse in the union
            raise AMPAPITypeError(end_point="Core/GetRole", cur_type=result, expec_type=dict)
        if format_data is True:
            return Role.from_response(result)
        return result

    async def get_role_data(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Role] | list[RoleResponse]:
        """|coro|

        Get's a list of all the roles.

        Endpoint: `Core/GetRoleData`

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
        list[:class:`Role`]
            On success returns a list of :class:`Role` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetRoleData",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetRoleData", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [Role.from_response(item) for item in result]
        return result

    async def get_role_ids(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> dict[str, str]:
        """|coro|

        Retrieves all the Roles AMP currently has and the role IDs.

        Endpoint: `Core/GetRoleIds`

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        dict[:class:`str`, :class:`str`]
            On success returns a dictionary containing all the roles and their IDs.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetRoleIds",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetRoleIds", cur_type=result, expec_type=dict)
        # Not going to write a logic check for having "keys" of other responses. This returns unique ID keys to a user defined str mapping.
        #  Unable to type define properly.
        return result  # pyright: ignore[reportReturnType]

    async def get_schedule_data(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ScheduleData | ScheduleDataResponse:
        """|coro|

        Returns an Instances scheduled Events and Triggers.

        Endpoint: `Core/GetScheduleData`

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
        :class:`ScheduleData` | :class:`ScheduleDataResponse`
            On success returns a :class:`ScheduleData` class, unless format_data is False which returns the raw dict.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(url="Core/GetScheduleData", request_params=request_params, **response_params)

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetScheduleData", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ScheduleDataResponse, SCHEDULE_DATA_REQUIRED_KEYS, SCHEDULE_DATA_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/GetScheduleData", cur_type=result, expec_type=dict)

        # ScheduleData takes the whole response; it converts the three nested lists itself.
        if format_data is True:
            return ScheduleData(data=result)
        return result

    async def get_setting_spec(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> SettingsSpecParent | SettingsSpecParentResponse:
        """|coro|

        Retrieves a list of settings specifications that can be changed.

        Endpoint: `Core/GetSettingsSpec`

        .. note::
            See :ref:`Setting Nodes <Documentation>` for more information.

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
        :class:`SettingsSpecParent` | :class:`SettingsSpecParentResponse`
            On success returns a :class:`SettingsSpecParent` dataclass, unless format_data is False which returns the raw dict.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetSettingsSpec",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetSettingsSpec", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(
            result,
            SettingsSpecParentResponse,
            SETTINGS_SPEC_PARENT_REQUIRED_KEYS,
            SETTINGS_SPEC_PARENT_EXCLUDED_KEYS,
        ):
            raise AMPAPITypeError(end_point="Core/GetSettingsSpec", cur_type=result, expec_type=dict)
        if format_data is True:
            # Module categories have a colon in their name (eg. `valheim:stadiacontroller`) and go into `modules`.
            categories = {name: entries for name, entries in result.items() if ":" not in name}
            modules = {name: entries for name, entries in result.items() if ":" in name}
            return SettingsSpecParent.from_response({**categories, "modules": modules})
        return result

    async def get_setting_values(
        self,
        setting_node: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> dict[str, str] | dict[str, Any]:
        """|coro|

        Returns the setting values.

        Endpoint: `Core/GetSettingValues`

        .. note::
            See :ref:`Setting Nodes <Documentation>` for more information.


        Parameters
        ----------
        setting_node : :class:`str`
            The setting node name.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        dict[:class:`str`, :class:`str`]
            On success returns a dictionary of setting values.

        """
        await self._reauth()
        parameters: dict[str, str] = {"SettingNode": setting_node}
        result: ResponseAliasFull = await self._post(
            url="Core/GetSettingValues",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetSettingValues", cur_type=result, expec_type=dict)
        # No TypedDict models this response, so it comes back as a plain dict.
        return dict(result)

    async def get_status(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Status | StatusResponse:
        """|coro|

        Gets the AMP Instance application status information. Such as active users, cpu usage, memory usage, state and uptime.

        Endpoint: `Core/GetStatus`

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
        :class:`Status`
            On success returns a :class:`Status` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetStatus",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetStatus", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, StatusResponse, STATUS_REQUIRED_KEYS, STATUS_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/GetStatus", cur_type=result, expec_type=dict)
        if format_data is True:
            return Status.from_response(result)
        return result

    async def get_structured_diagnostics(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> StructuredDiagnostics | StructuredDiagnosticsResponse:
        """|coro|

        Retrieves the structured diagnostics of the Instance.

        Endpoint: `Core/GetStructuredDiagnostics`

        .. note::
            Requires the ``Core.Special.Diagnostics`` permission.


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
        :class:`StructuredDiagnostics`
            On success returns a :class:`StructuredDiagnostics` dataclass with the `core` and the module specific `application` diagnostics.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetStructuredDiagnostics",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetStructuredDiagnostics", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return StructuredDiagnostics.from_response(result)
        return result  # pyright: ignore[reportReturnType]

    async def get_tasks(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[RunningTask] | list[RunningTaskResponse]:
        """|coro|

        Get a list of running tasks on the Instance.

        Endpoint: `Core/GetTasks`

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
        list[:class:`RunningTask`] | list[:class:`RunningTaskResponse`]
            On success returns a list of :class:`RunningTask` dataclasses, or the raw dictionaries when `format_data` is False.

        Raises
        ------
        :exc:`AMPAPITypeError`
            If AMP did not answer with a list of tasks.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetTasks",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetTasks", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        tasks: list[RunningTaskResponse] = []
        for item in result:
            if not is_response_type(item, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
                raise AMPAPITypeError(end_point="Core/GetTasks", cur_type=item, expec_type=dict)
            tasks.append(item)
        if format_data is True:
            return [RunningTask.from_response(task) for task in tasks]
        return tasks

    async def get_time_interval_trigger(
        self,
        trigger_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> TimedTrigger | TimedTriggerResponse:
        """|coro|

        Gets a time interval trigger information.

        Endpoint: `Core/GetTimeIntervalTrigger`

        Parameters
        ----------
        trigger_id : :class:`str`
            The ID of the time interval trigger to get.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`TimedTrigger` | :class:`TimedTriggerResponse`
            On success returns a :class:`TimedTrigger` dataclass, unless format_data is False which returns the raw dict.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Id": trigger_id}
        result: ResponseAliasFull = await self._post(
            url="Core/GetTimeIntervalTrigger",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetTimeIntervalTrigger", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, TimedTriggerResponse, TIMED_TRIGGER_REQUIRED_KEYS, TIMED_TRIGGER_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/GetTimeIntervalTrigger", cur_type=result, expec_type=dict)
        if format_data is True:
            return TimedTrigger.from_response(result)
        return result

    async def get_triggers(self) -> TriggerID:
        """|coro|

        Retrieves the available trigger IDs for the Instance and sets them as attributes tied to :attr:`triggers`.

        .. note::
            Each Instance has unique Trigger IDs.
            - You can simply access the correct ID for the Trigger via :attr:`~Core.triggers.a_backup_has_started` as an example.
            - This would return the ID string to be passed into a function that requires a Trigger ID value.

        Returns
        -------
        :class:`TriggerID`
            A class containing the Trigger Description as attributes referencing the Trigger ID tied to the Instance.

        """
        await self._reauth()
        data: ScheduleData | ScheduleDataResponse = await self.get_schedule_data(format_data=False)
        # format_data=False always returns the raw dict; the isinstance check is what tells pyright that.
        if not isinstance(data, dict):
            raise AMPAPITypeError(end_point="Core/GetScheduleData", cur_type=data, expec_type=dict)
        triggers: list[TriggersResponse] = data.get("available_triggers", [])
        for entry in triggers:
            entry["description"] = self.sanitize_json(json=entry["description"])
        self._triggers = TriggerID(data=triggers)
        return self._triggers

    async def get_update_info(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> UpdateInfo | UpdateInfoResponse:
        """|coro|

        Gets the Update Version information for AMP.

        Endpoint: `Core/GetUpdateInfo`

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
        :class:`UpdateInfo`
            On success returns a :class:`UpdateInfo` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetUpdateInfo",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetUpdateInfo", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if "update_available" not in result:  # 'update_available' uniquely identifies UpdateInfoResponse in the union
            raise AMPAPITypeError(end_point="Core/GetUpdateInfo", cur_type=result, expec_type=dict)
        if format_data is True:
            return UpdateInfo.from_response(result)
        return result

    async def get_updates(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Updates | UpdatesResponse:
        """|coro|

        Gets changes to the server status, in addition to any notifications or console output that have occurred
        since the last time meth:`get_updates` was called by the current session.

        Endpoint: `Core/GetUpdates`

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
        :class:`Updates`
            On success returns a :class:`Updates` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetUpdates",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetUpdates", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        # UpdatesResponse shares the 'status' key with ActionResultResponse, so 'console_entries' tells them apart;
        # the ActionResult endpoints exclude it with `"console_entries" not in result`.
        if "console_entries" not in result:
            raise AMPAPITypeError(end_point="Core/GetUpdates", cur_type=result, expec_type=dict)
        if format_data is True:
            return Updates.from_response(result)
        return result

    async def get_user_action_spec(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionSpec:
        """|coro|

        Get a specification of the user actions.

        Endpoint: `Core/GetUserActionsSpec`

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :data:`ActionSpec`
            On success returns a dictionary keyed by module name, each holding its method names and captions.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetUserActionsSpec",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetUserActionsSpec", cur_type=result, expec_type=dict)
        return result  # pyright: ignore[reportReturnType]

    async def get_user_info(
        self,
        user_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> UserApplicationData | UserApplicationDataResponse:
        """|coro|

        Provides information about a given in-application user (as opposed to AMP Users).

        Endpoint: `Core/GetUserInfo`

        Parameters
        ----------
        user_id : :class:`str`
            The Application User ID. See :meth:`get_user_list`.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`UserApplicationData` | :class:`UserApplicationDataResponse`
            On success returns a :class:`UserApplicationData` class, unless format_data is False which returns the raw dict.

        """
        await self._reauth()
        parameters: dict[str, str] = {"UID": user_id}
        result: ResponseAliasFull = await self._post(
            url="Core/GetUserInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetUserInfo", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(
            result,
            UserApplicationDataResponse,
            USER_APPLICATION_DATA_REQUIRED_KEYS,
            USER_APPLICATION_DATA_EXCLUDED_KEYS,
        ):
            raise AMPAPITypeError(end_point="Core/GetUserInfo", cur_type=result, expec_type=dict)
        if format_data is True:
            # return UserApplicationData(**result)
            return UserApplicationData.from_response(result)
        return result

    async def get_user_list(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Players | dict[str, Any]:
        """|coro|

        Returns the list of the connected users to the Application.

        Endpoint: `Core/GetUserList`

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
        :class:`Players`
            On success returns a :class:`Players` dataclass, with no players when AMP answers an empty list.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetUserList",
            request_params=request_params,
            **response_params,
        )
        # AMP answers an empty list instead of an empty object when no one is connected.
        if isinstance(result, list) and len(result) == 0:
            users: dict[str, Any] = {}
        elif isinstance(result, dict):
            users = dict(result)
        else:
            raise AMPAPITypeError(end_point="Core/GetUserList", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        # A UUID -> name map that no TypedDict models; Players takes it as a plain dict.
        if format_data is True:
            return Players(data=users)
        return users

    async def get_webauthn_challenge(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Get a webauthn challenge.

        Endpoint: `Core/GetWebauthnChallenge`

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
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetWebauthnChallenge",
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetWebauthnChallenge", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/GetWebauthnChallenge", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def get_webauthn_credential_ids(
        self,
        username: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> WebauthnCredentialIDsResponse:
        """|coro|

        Get a webauthn credential IDs.

        Endpoint: `Core/GetWebauthnCredentialIDs`

        .. versionchanged:: 5.0.0
            Returns the `ids` and `challenge` dict AMP sends, not a list.

        Parameters
        ----------
        username : :class:`str`
            Username.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`WebauthnCredentialIDsResponse`
            On success returns the dict holding the webauthn credential IDs and the challenge.

        """
        await self._reauth()
        parameters: dict[str, str] = {"username": username}
        result: ResponseAliasFull = await self._post(
            url="Core/GetWebauthnCredentialIDs",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetWebauthnCredentialIDs", cur_type=result, expec_type=dict)
        if not is_response_type(
            result,
            WebauthnCredentialIDsResponse,
            WEBAUTHN_CREDENTIAL_IDS_REQUIRED_KEYS,
            WEBAUTHN_CREDENTIAL_IDS_EXCLUDED_KEYS,
        ):
            raise AMPAPITypeError(end_point="Core/GetWebauthnCredentialIDs", cur_type=result, expec_type=dict)
        return result

    async def get_webauthn_credential_summary(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Any]:
        """|coro|

        Get the webauthn credential summaries.

        Endpoint: `Core/GetWebauthnCredentialSummaries`

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[Any]
            On success returns a list of webauthn credential summaries.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/GetWebauthnCredentialSummaries",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/GetWebauthnCredentialSummaries", cur_type=result, expec_type=list)
        return result

    @deprecated("This was removed in `2.6.0.0`", stacklevel=2)
    async def get_webserver_metrics(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Any:
        """|coro|

        Gets the webserver metrics.

        Endpoint: `Core/GetWebserverMetrics`

        .. versionremoved:: AMP-2.6.0.0

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Any
            UNK data returned by the API.

        Raises
        ------
        :exc:`RuntimeError`
            The AMP version no longer has this endpoint. (AMP 2.6.0.0 and newer)

        """
        await self._reauth()
        await self.version_validation(
            version=BuildInfo(major=2, minor=6, revision=0, minor_revision=0),
            endpoint="Core/GetWebserverMetrics",
        )

        result: ResponseAliasFull = await self._post(
            url="Core/GetWebserverMetrics",
            request_params=request_params,
            **response_params,
        )
        return result

    async def kill_application(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Kills the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Endpoint: `Core/Kill`

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
        return await self._post(url="Core/Kill", no_data=True, request_params=request_params, **response_params)

    async def login(
        self,
        amp_user: str,
        amp_password: str,
        token: str = "",
        remember_me: bool = False,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> LoginResults | LoginResultsResponse | None:
        """|coro|

        AMP API login function.

        Endpoint: `Core/Login`

        Parameters
        ----------
        amp_user : :class:`str`
            The username for logging into the AMP Control Panel.
        amp_password : :class:`str`
            The password for logging into the AMP Control Panel.
        token : :class:`str` , optional
            Your Two-Factor token string, defaults to "".
            - Uses :meth:`TOTP.now()` on the provided token.
        remember_me : :class:`bool` , optional
            Remember me token, defaults to ``False``.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Union[:class:`LoginResults`, None]
            On success returns a :class:`LoginResults` dataclass, None if AMP sent no login token.

        """
        # No token means no 2FA, so send an empty code rather than one generated from an empty secret.
        code: str = TOTP(token).now() if token else ""
        parameters: dict[str, str | bool] = {"username": amp_user, "password": amp_password, "token": code, "rememberMe": remember_me}
        result: ResponseAliasFull = await self._post(
            url="Core/Login",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        # Unpack the data into our Dataclass.
        if isinstance(result, dict) and "remember_me_token" in result:
            return LoginResults.from_response(result)
        return None

    async def logout(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Logout from AMP.

        Endpoint: `Core/Logout`

        .. versionchanged:: 5.0.0
            The stored session is cleared, and the next call logs in again.

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
        # return await self._post(url="Core/Logout", no_data=True, request_params=request_params, **response_params)
        await self._post(url="Core/Logout", no_data=True, request_params=request_params, **response_params)
        # AMP ended the session. The stored one is no use to the next call.
        self._reset_session()

    # AMP restarts the AMP process of whichever Instance gets the call, an ADS or not.
    # The application inside an Instance is `restart_application`.
    # @Base.ads_only
    async def restart_amp(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Restart the AMP process of this Instance.

        Endpoint: `Core/RestartAMP`

        .. note::
            A running application is stopped and is not started again. The session ends with the process. This
            Instance's stored session is reset and the next call logs in again by itself.

        .. note::
            This restarts AMP itself, not the application it runs. To restart the application (eg. a Minecraft server),
            use :meth:`restart_application`.

        .. versionchanged:: 5.0.0
            Returns an :class:`ActionResult` and takes `format_data`.
            Runs on any Instance, not only an ADS.

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
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(url="Core/RestartAMP", request_params=request_params, **response_params)

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/RestartAMP", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/RestartAMP", cur_type=result, expec_type=dict)
        # The restart ended our session. Resetting it lets the next call log in instead of sending one that fails.
        self._reset_session()
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def resume_instance(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Allows the service to be re-started after previously being suspended.

        Endpoint: `Core/Resume`

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
        return await self._post(url="Core/Resume", no_data=True, request_params=request_params, **response_params)

    # TODO: Verify data structure.
    async def oidc_login(
        self,
        code: str,
        redirect_uri: str,
        instance_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Any:
        """|coro|

        Related to OIDC credentials. Return type is UNKNOWN as of v`3.0.0`.

        Endpoint: `Core/OIDCLogin`

        __EndPoint__: /API/Core/OIDCLogin

        Parameters
        ----------
        code : :class:`str`
            UNK.
        redirect_uri : :class:`str`
            UNK.
        instance_id : :class:`str`
            The Instance ID, see :attr:`~Instance.instance_id`
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`Any`
            UNK.

        """
        await self._reauth()
        parameters: dict[str, str] = {"code": code, "redirect_uri": redirect_uri, "serverId": instance_id}
        result: ResponseAliasFull = await self._post(
            url="Core/OIDCLogin",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/OIDCLogin", cur_type=result, expec_type=dict)
        return result

    async def refresh_setting_value_list(
        self,
        node: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Refreshes a setting nodes values.

        Endpoint: `Core/RefreshSettingValueList`

        Parameters
        ----------
        node : :class:`str`
            The setting node name.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Name": node}
        result: ResponseAliasFull = await self._post(
            url="Core/RefreshSettingValueList",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/RefreshSettingValueList", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/RefreshSettingValueList", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def refresh_settings_source_cache(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Refreshes the settings source cache.

        Endpoint: `Core/RefreshSettingsSourceCache`

        .. versionchanged:: 5.0.0
            Returns None and no longer takes `format_data`.

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
        return await self._post(url="Core/RefreshSettingsSourceCache", no_data=True, request_params=request_params, **response_params)

    async def rename_role(
        self,
        role_id: str,
        new_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Renames a role.

        Endpoint: `Core/RenameRole`

        Parameters
        ----------
        role_id : :class:`str`
            The ID of the role to rename.
        new_name : :class:`str`
            The new name for the role.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"RoleId": role_id, "NewName": new_name}
        result: ResponseAliasFull = await self._post(
            url="Core/RenameRole",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/RenameRole", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/RenameRole", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def restart_application(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Restarts the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Endpoint: `Core/Restart`

        Parameters
        ----------
        format_data : Union[bool, None], optional
            Format the JSON response data. (Uses `FORMAT_DATA` global constant if None), by default None
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/Restart",
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/Restart", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/Restart", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def reset_user_password(
        self,
        username: str,
        new_password: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """For administrative users to alter the password of another user.

        Endpoint: `Core/ResetUserPassword`

        Parameters
        ----------
        username : :class:`str`
            Username.
        new_password : :class:`str`
            New password.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Username": username, "NewPassword": new_password}
        result: ResponseAliasFull = await self._post(
            url="Core/ResetUserPassword",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/ResetUserPassword", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/ResetUserPassword", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def revert_user_from_oidc(
        self,
        username: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Revert an AMP User from OIDC back to a local sign in.

        Endpoint: `Core/RevertUserFromOIDC`

        .. note::
            Requires the ``Core.UserManagement.UpdateUserInfo`` permission.


        Parameters
        ----------
        username : :class:`str`
            The AMP User name.
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
        parameters: dict[str, Any] = {"Username": username}
        result: ResponseAliasFull = await self._post(
            url="Core/RevertUserFromOIDC",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/RevertUserFromOIDC", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/RevertUserFromOIDC", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def revoke_webauthn_credential(
        self,
        auth_id: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Revoke a webauthn credential.

        Endpoint: `Core/RevokeWebauthnCredential`

        Parameters
        ----------
        auth_id : :class:`int`
            The Web auth ID.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, int] = {"ID": auth_id}
        result: ResponseAliasFull = await self._post(
            url="Core/RevokeWebauthnCredential",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/RevokeWebauthnCredential", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/RevokeWebauthnCredential", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def run_security_check(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[SecurityCheck] | list[SecurityCheckResponse]:
        """|coro|

        Run a security check on the Instance.

        Endpoint: `Core/RunSecurityCheck`

        .. versionchanged:: 5.0.0
            Returns a list of :class:`SecurityCheck` and takes `format_data`.

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
        list[:class:`SecurityCheck`]
            On success returns a list of :class:`SecurityCheck` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/RunSecurityCheck",
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="Core/RunSecurityCheck", cur_type=result, expec_type=list)

        if format_data is None:
            format_data = self.format_data

        if not is_response_list(result, SecurityCheckResponse, SECURITY_CHECK_REQUIRED_KEYS, SECURITY_CHECK_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/RunSecurityCheck", cur_type=result, expec_type=list)
        if format_data is True:
            return [SecurityCheck.from_response(entry) for entry in result]
        return result

    async def run_event_trigger_immediately(
        self,
        trigger_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Runs an event trigger immediately.

        Endpoint: `Core/RunEventTriggerImmediately`

        Parameters
        ----------
        trigger_id : :class:`str`
             The ID of the event trigger to run.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"TriggerId": trigger_id}
        result: ResponseAliasFull = await self._post(
            url="Core/RunEventTriggerImmediately",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/RunEventTriggerImmediately", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/RunEventTriggerImmediately", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def set_amp_user_role_membership(
        self,
        user_id: str,
        role_id: str,
        is_member: bool,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Adds a user to an AMP role.

        Endpoint: `Core/SetAMPUserRoleMembership`

        Parameters
        ----------
        user_id : :class:`str`
            User ID to add to the role.
        role_id : :class:`str`
            Role ID to add the user to.
        is_member : :class:`bool`
            "True" to add the user to the role, "False" to remove the user from the role.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"UserId": user_id, "RoleId": role_id, "IsMember": is_member}
        result: ResponseAliasFull = await self._post(
            url="Core/SetAMPUserRoleMembership",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/SetAMPUserRoleMembership", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/SetAMPUserRoleMembership", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def set_amp_role_permission(
        self,
        role_id: str,
        permission_node: str,
        enabled: Union[bool, None],
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Set a permission node to "True" or "False" for the provided AMP role.

        Endpoint: `Core/SetAMPRolePermission`

        Parameters
        ----------
        role_id : :class:`str`
            Role ID to add the user to.
        permission_node : :class:`str`
            AMP permission node. eg "Core.RoleManagement.DeleteRoles"
        enabled : Union[None, :class:`bool`], optional
            Set a permission to "True", "False" or "None"; depending on the results you can disable or enable an
            entire tree node of permissions.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"RoleId": role_id, "PermissionNode": permission_node, "Enabled": enabled}
        result: ResponseAliasFull = await self._post(
            url="Core/SetAMPRolePermission",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/SetAMPRolePermission", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/SetAMPRolePermission", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def set_trigger_enabled(
        self,
        trigger_id: str,
        enabled: bool,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Sets the enabled state of a trigger.

        Endpoint: `Core/SetTriggerEnabled`

        Parameters
        ----------
        trigger_id : :class:`str`
            The ID of the trigger to edit.
        enabled : :class:`bool`
            The enabled state of the trigger to edit.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"Id": trigger_id, "Enabled": enabled}
        result: ResponseAliasFull = await self._post(
            url="Core/SetTriggerEnabled",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/SetTriggerEnabled", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/SetTriggerEnabled", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def send_console_message(
        self,
        msg: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Sends a message or command to the Console. (eg `/list`)

        Endpoint: `Core/SendConsoleMessage`

        .. note::
            Calling :meth:`Core.get_updates` directly after this function will not have the console output,
            best practice is to delay ~ 1 sec to catch results.

        Parameters
        ----------
        msg : :class:`str`
            The message or command to send to the Console.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"message": msg}
        return await self._post(
            url="Core/SendConsoleMessage",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    # TODO: Look into sanitizing data structure for array style key/value pairs.
    # - "value":[\"asd\"]
    # I am already calling JSON.dumps, look into structure and see what is (possibly) failing.
    async def set_configs(
        self,
        data: dict[str, str],
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> bool:
        """|coro|

        Set multiple Setting Nodes values.

        Endpoint: `Core/SetConfigs`

        Parameters
        ----------
        data : dict[:class:`str`, :class:`str`]
            Dictionary of Setting Nodes to set.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`bool`
            On success returns a boolean.

        """
        await self._reauth()
        parameters: dict[str, dict[str, str]] = {"data": data}
        result: ResponseAliasFull = await self._post(
            url="Core/SetConfigs",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, bool):
            raise AMPAPITypeError(end_point="Core/SetConfigs", cur_type=result, expec_type=bool)
        return result

    async def set_config(
        self,
        node: str,
        value: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Set a Setting Node value.

        Endpoint: `Core/SetConfig`

        Parameters
        ----------
        node : :class:`str`
            Setting node name.
        value : :class:`str`
            Config node value.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"node": node, "value": value}
        result: ResponseAliasFull = await self._post(
            url="Core/SetConfig",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/SetConfig", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/SetConfig", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def sleep(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Put the application to sleep.

        Endpoint: `Core/Sleep`

        .. note::
            Requires the ``Core.AppManagement.StopApplication`` permission.


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
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(url="Core/Sleep", request_params=request_params, **response_params)

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/Sleep", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/Sleep", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def start_application(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Starts the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Endpoint: `Core/Start`

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
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/Start",
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/Start", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/Start", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def stop_application(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Stops the Instances Application (eg. Minecraft Server, Source Server, Palworld Server, etc.)

        Endpoint: `Core/Stop`

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
        return await self._post(url="Core/Stop", no_data=True, request_params=request_params, **response_params)

    async def suspend_instance(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Prevents the current Instance from being started, and stops it if it's currently running.

        Endpoint: `Core/Suspend`

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
        return await self._post(url="Core/Suspend", no_data=True, request_params=request_params, **response_params)

    async def update_account_info(
        self,
        email_address: str,
        two_factor_pin: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update account info.

        Endpoint: `Core/UpdateAccountInfo`

        .. note::
            All these settings take affect on the account logged in via the API.


        Parameters
        ----------
        email_address : :class:`str`
            The new Email address.
        two_factor_pin : :class:`str`
            Two factor PIN.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"EmailAddress": email_address, "TwoFactorPIN": two_factor_pin}
        result: ResponseAliasFull = await self._post(
            url="Core/UpdateAccountInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/UpdateAccountInfo", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/UpdateAccountInfo", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    @Base.ads_only
    async def upgrade_amp(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Upgrade the current AMP Instance.

        Endpoint: `Core/UpgradeAMP`

        .. note::
            AMP restarts, which ends the session. This Instance's stored session is reset and the next call logs in again.

        .. warning::
            The Instance must be an ADS or Controller.

        .. versionchanged:: 5.0.0
            Returns an :class:`ActionResult` and takes `format_data`.

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
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(url="Core/UpgradeAMP", request_params=request_params, **response_params)

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/UpgradeAMP", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/UpgradeAMP", cur_type=result, expec_type=dict)
        # The upgrade restarts AMP and ends our session.
        self._reset_session()
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    @Base.ads_only
    async def update_amp_instance(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Updates the ADS Instance.

        Endpoint: `Core/UpdateAMPInstance`

        .. note::
            AMP restarts, which ends the session. This Instance's stored session is reset and the next call logs in again.

        .. warning::
            The Instance must be an ADS or Controller.

        .. versionchanged:: 5.0.0
            Returns an :class:`ActionResult` and takes `format_data`.

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
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(url="Core/UpdateAMPInstance", request_params=request_params, **response_params)

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/UpdateAMPInstance", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/UpdateAMPInstance", cur_type=result, expec_type=dict)
        # The update restarts AMP and ends our session.
        self._reset_session()
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def update_application(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update the Instance application.

        Endpoint: `Core/UpdateApplication`

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
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="Core/UpdateApplication",
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/UpdateApplication", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/UpdateApplication", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def update_oidc_sub(
        self,
        username: str,
        oidc_sub: Union[str, None] = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update the OIDC subject linked to an AMP User.

        Endpoint: `Core/UpdateOIDCSub`

        .. note::
            Requires the ``Core.UserManagement.UpdateUserInfo`` permission.


        Parameters
        ----------
        username : :class:`str`
            The AMP User name.
        oidc_sub : Union[:class:`str`, None], optional
            The OIDC subject to link to the AMP User, by default None.
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
        parameters: dict[str, Any] = {"Username": username}
        if oidc_sub is not None:
            parameters["OIDCSub"] = oidc_sub
        result: ResponseAliasFull = await self._post(
            url="Core/UpdateOIDCSub",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/UpdateOIDCSub", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/UpdateOIDCSub", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def update_public_key(
        self,
        pub_key: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """Update a public key.

        Endpoint: `Core/UpdatePublicKey`

        Parameters
        ----------
        pub_key : :class:`str`
            The public key.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
             On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"PubKey": pub_key}
        result: ResponseAliasFull = await self._post(
            url="Core/UpdatePublicKey",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/UpdatePublicKey", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/UpdatePublicKey", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def update_tools(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update the AMP system tools (ampinstmgr) to the latest release.

        Endpoint: `Core/UpdateTools`

        .. note::
            Requires the ``Core.Special.UpgradeAMP`` permission.


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
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(url="Core/UpdateTools", request_params=request_params, **response_params)

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/UpdateTools", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/UpdateTools", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def update_user_info(
        self,
        username: str,
        disabled: bool = False,
        password_expires: bool = False,
        cannot_change_password: bool = False,
        must_change_password: bool = False,
        email_address: str = "",
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update an AMP user.

        Endpoint: `Core/UpdateUserInfo`

        Parameters
        ----------
        username : :class:`str`
            The AMP user to update.
        disabled : :class:`bool`, optional
            If the AMP user should be disabled, defaults to False.
        password_expires : :class:`bool`, optional
            If the AMP user password should expire, defaults to False.
        cannot_change_password : :class:`bool`, optional
            The AMP user cannot change their password, defaults to False.
        must_change_password : :class:`bool`, optional
            The AMP user must change password upon next login, defaults to False.
        email_address : :class:`str`, optional
            The email address to set for the AMP user, defaults to "".
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {
            "Username": username,
            "Disabled": disabled,
            "PasswordExpires": password_expires,
            "CannotChangePassword": cannot_change_password,
            "MustChangePassword": must_change_password,
            "EmailAddress": email_address,
        }
        result: ResponseAliasFull = await self._post(
            url="Core/UpdateUserInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/UpdateUserInfo", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/UpdateUserInfo", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def webauthn_register(
        self,
        attestation_object: str,
        client_data_json: str,
        description: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Webauthn register.

        Endpoint: `Core/WebauthnRegister`

        .. note::
            Unknown usage.


        Parameters
        ----------
        attestation_object : :class:`str`
            Attestation object.
        client_data_json : :class:`str`
            Client data JSON.
        description : :class:`str`
            Description.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {
            "attestationObject": attestation_object,
            "clientDataJSON": client_data_json,
            "description": description,
        }
        result: ResponseAliasFull = await self._post(
            url="Core/WebauthnRegister",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/WebauthnRegister", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="Core/WebauthnRegister", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result
