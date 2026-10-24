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

import contextlib
import logging
from typing import TYPE_CHECKING, Any, Optional, Union, Unpack

from ._types import (
    ACTION_RESULT_EXCLUDED_KEYS,
    ACTION_RESULT_REQUIRED_KEYS,
    APP_SUMMARY_EXCLUDED_KEYS,
    APP_SUMMARY_REQUIRED_KEYS,
    APPLICATION_EXCLUDED_KEYS,
    APPLICATION_REQUIRED_KEYS,
    CONTROLLER_EXCLUDED_KEYS,
    CONTROLLER_REQUIRED_KEYS,
    DEPLOYMENT_TEMPLATE_EXCLUDED_KEYS,
    DEPLOYMENT_TEMPLATE_REQUIRED_KEYS,
    ENDPOINTS_EXCLUDED_KEYS,
    ENDPOINTS_REQUIRED_KEYS,
    INSTANCE_DATASTORE_EXCLUDED_KEYS,
    INSTANCE_DATASTORE_REQUIRED_KEYS,
    INSTANCE_EXCLUDED_KEYS,
    INSTANCE_REQUIRED_KEYS,
    INSTANCE_STATUS_EXCLUDED_KEYS,
    INSTANCE_STATUS_REQUIRED_KEYS,
    PORT_INFO_EXCLUDED_KEYS,
    PORT_INFO_REQUIRED_KEYS,
    PROVISION_EXCLUDED_KEYS,
    PROVISION_REQUIRED_KEYS,
    PROVISION_SETTING_INFO_EXCLUDED_KEYS,
    PROVISION_SETTING_INFO_REQUIRED_KEYS,
    REMOTE_TARGET_INFO_EXCLUDED_KEYS,
    REMOTE_TARGET_INFO_REQUIRED_KEYS,
    RUNNING_TASK_EXCLUDED_KEYS,
    RUNNING_TASK_REQUIRED_KEYS,
    ActionResultResponse,
    ApplicationResponse,
    AppSummaryResponse,
    ControllerResponse,
    DeploymentTemplateResponse,
    EndpointsResponse,
    InstanceDatastoreResponse,
    InstanceResponse,
    InstanceStatusResponse,
    PortInfoResponse,
    ProvisionResponse,
    ProvisionSettingInfoResponse,
    RemoteTargetInfoResponse,
    RunningTaskResponse,
    is_response_list,
    is_response_type,
)
from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPIKeyError, AMPAPITypeError
from .modules import (
    ActionResult,
    ADSModeState,
    Application,
    CreateInstance,
    DeploymentTemplate,
    Endpoints,
    InstanceDatastore,
    InstanceInfo,
    InstanceStatus,
    PortInfo,
    PostCreateState,
    Provision,
    ProvisionSettingInfo,
    RemoteTargetInfo,
    RunningTask,
    Template,
)

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

    from .instance import Instance

__all__ = ("ADSModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class ADSModule(Base):
    """Contains the functions for any ``/API/ADSModule/`` API endpoints.

    .. warning::
        Do not change the :attr:`~ADSModule.module` attribute for any reason.


    .. note::
        Every function in this class requires the Instance type be of either :class:`TargetADS`,
        :class:`ADSModule` or the :attr:`~ADSModule.module` attribute to be "ADS".\n
        If the `format_data` parameter is None on any function; the global `FORMAT_DATA` will be used instead.


    """

    _module = "ADS"

    @Base.ads_only
    async def add_datastore(
        self,
        new_datastore: InstanceDatastore,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Add a new datastore.

        Endpoint: `ADSModule/AddDatastore`

        Parameters
        ----------
        new_datastore : :class:`InstanceDatastore`
            Your pre-created data structure to be parsed for the required API parameters.
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

        data: dict[str, Any] = new_datastore.to_dict()

        parameters: dict[str, Any] = {"newDatastore": data}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/AddDatastore",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/AddDatastore", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)

            return result

        raise AMPAPIKeyError("status", "ADSModule/AddDatastore", result)  # noqa: EM101

    @Base.ads_only
    async def apply_instance_configuration(
        self,
        instance_id: str,
        args: dict[str, str],
        rebuild_configuration: bool = False,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Apply settings to an Instance's own configuration, through the ADS that holds it.

        Endpoint: `ADSModule/ApplyInstanceConfiguration`

        .. note::
            `args` takes setting nodes, eg. `{"Core.Login.UseAuthServer": "True", "Core.Login.AuthServerURL": url}`
            points an Instance at its Controller for logins, which is what `ampinstmgr --RepairAuth` does
            (tested on AMP 2.8.0.8). Send it through the :class:`TargetADS` for a Target's Instance.

        .. warning::
            `rebuild_configuration` is untested.


        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
        args : dict[:class:`str`, :class:`str`]
            The setting nodes and the values to apply.
        rebuild_configuration : :class:`bool`, optional
            Rebuild the Instance's configuration, by default False.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask` | :class:`RunningTaskResponse`
            On success returns a :class:`RunningTask` dataclass, or the raw dictionary when `format_data` is False.
            AMP 2.8 answers with a running task that also carries the :class:`ActionResult` keys.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"InstanceID": instance_id, "Args": args, "RebuildConfiguration": rebuild_configuration}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/ApplyInstanceConfiguration",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/ApplyInstanceConfiguration", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)

            return result

        raise AMPAPITypeError(end_point="ADSModule/ApplyInstanceConfiguration", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def apply_template(
        self,
        instance_id: str,
        template_id: int,
        *,
        new_friendly_name: Union[str, None] = None,
        secret: Union[str, None] = None,
        restart_if_previously_running: Union[bool, None] = None,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Overlays an existing template on an existing Instance, used to perform package reconfigurations.

        Endpoint: `ADSModule/ApplyTemplate`

        .. warning::
            Do not use this to "transform" an existing application into another.
            The Instance should be deleted and re-created in that situation.

        .. note::
            If you need to get an AMP Templates ID, use :meth:`get_deployment_templates` and
            access the :attr:`DeploymentTemplate.id` attribute.


        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID to apply the template to.
        template_id : :class:`int`
            The Template ID to apply.
        new_friendly_name : Union[:class:`str`, None], optional
            The new friendly name for the Instance, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
        secret : Union[:class:`str`, None], optional
            The secret AMP uses when applying the template, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
        restart_if_previously_running : Union[:class:`bool`, None], optional
            Restart the Instance after applying the template if it was running before, by default None, which leaves
            AMP's default.

            .. versionadded:: 5.0.0
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
        parameters: dict[str, Any] = {"InstanceID": instance_id, "TemplateID": template_id}

        if new_friendly_name is not None:
            parameters["NewFriendlyName"] = new_friendly_name

        if secret is not None:
            parameters["Secret"] = secret

        if restart_if_previously_running is not None:
            parameters["RestartIfPreviouslyRunning"] = restart_if_previously_running

        result: ResponseAliasFull = await self._post(
            url="ADSModule/ApplyTemplate",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/ApplyTemplate", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)

            return result

        raise AMPAPIKeyError("status", "ADSModule/ApplyTemplate", result)  # noqa: EM101

    @Base.ads_only
    async def attach_ads(
        self,
        friendly_name: str,
        is_https: bool,
        host: str,
        port: int,
        instance_id: str,
        pairing_code: str | None = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Attach an AMP Instance to the ADS calling the API endpoint with the passed in parameters using either a pairing code or not.

        Endpoints: `ADSModule/AttachADSWithPairingCode`, `ADSModule/AttachADS`

        .. note::
            This Endpoint is also encapsulating `AttachADSWithPairingCode`;
            simply provide a "pairing_code" parameter to use the respective endpoint.


        .. note::
            When using the parameter "pairing_code" the API does not need to Authenticate.


        Parameters
        ----------
        friendly_name : :class:`str`
            The friendly name to be associated with the Instance when it is attached to the ADS.
        is_https : :class:`bool`
            If the Instance uses HTTPS or not.
        host : :class:`str`
            The URL/URi to access the Instance.
        port : :class:`int`
            The Port you want to attach the Instance to.
        instance_id : :class:`str`
            The Instance ID of the Instance you want to attach to the ADS.
        pairing_code : :class:`str | None`, optional
            The pairing code generated via :meth:`get_target_pairing_code`, by default None.
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
        parameters: dict[str, Any] = {
            "Friendly": friendly_name,
            "IsHTTPS": is_https,
            "Host": host,
            "Port": port,
            "InstanceID": instance_id,
        }
        if pairing_code is not None:
            parameters["PairingCode"] = pairing_code
            result: ResponseAliasFull = await self._post(
                url="ADSModule/AttachADSWithPairingCode",
                parameters=parameters,
                request_params=request_params,
                **response_params,
            )
        else:
            await self._reauth()
            result = await self._post(
                url="ADSModule/AttachADS",
                parameters=parameters,
                request_params=request_params,
                **response_params,
            )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/AttachADS", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/AttachADS", result)  # noqa: EM101

    @Base.ads_only
    async def cancel_pairing(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Cancel an ongoing ADS Pairing session.

        Endpoint: `ADSModule/CancelPairing`

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
        return await self._post(url="ADSModule/CancelPairing", no_data=True, request_params=request_params, **response_params)

    @Base.ads_only
    async def clone_instance(
        self,
        source_instance_id: str,
        target_ads_instance_id: str,
        new_friendly_name: Union[str, None] = None,
        post_create: Union[PostCreateState, None] = None,
        start_on_boot: Union[bool, None] = None,
        target_datastore: Union[int, None] = None,
        licence_key: Union[str, None] = None,
        new_instance_username: Union[str, None] = None,
        new_instance_password: Union[str, None] = None,
        delete_source: Union[bool, None] = None,
        copy_files: Union[bool, None] = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Clone an Instance onto a Target.

        Endpoint: `ADSModule/CloneInstance`

        .. note::
            Requires the ``ADS.InstanceManagement.CreateInstance`` permission.


        Parameters
        ----------
        source_instance_id : :class:`str`
            The ID of the Instance to clone.
        target_ads_instance_id : :class:`str`
            The ID of the Target ADS Instance that will hold the clone.
        new_friendly_name : Union[:class:`str`, None], optional
            The friendly name of the clone, by default None.
        post_create : Union[:class:`PostCreateState`, None], optional
            The action the clone takes after creation, by default None.
        start_on_boot : Union[:class:`bool`, None], optional
            If the clone should start when the Target boots, by default None.
        target_datastore : Union[:class:`int`, None], optional
            The ID of the Datastore to place the clone in, by default None.
        licence_key : Union[:class:`str`, None], optional
            The licence key for the clone, by default None.
        new_instance_username : Union[:class:`str`, None], optional
            The administrator user name of the clone, by default None.
        new_instance_password : Union[:class:`str`, None], optional
            The administrator password of the clone, by default None.
        delete_source : Union[:class:`bool`, None], optional
            If the source Instance is deleted once cloned, by default None.
        copy_files : Union[:class:`bool`, None], optional
            If the source Instance's files are copied to the clone, by default None.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask` | :class:`RunningTaskResponse`
            On success returns a :class:`RunningTask` dataclass, or the raw dictionary when `format_data` is False.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"SourceInstanceId": source_instance_id, "TargetADSInstance": target_ads_instance_id}
        if new_friendly_name is not None:
            parameters["NewFriendlyName"] = new_friendly_name
        if post_create is not None:
            parameters["PostCreate"] = post_create.value
        if start_on_boot is not None:
            parameters["StartOnBoot"] = start_on_boot
        if target_datastore is not None:
            parameters["TargetDatastore"] = target_datastore
        if licence_key is not None:
            parameters["LicenceKey"] = licence_key
        if new_instance_username is not None:
            parameters["NewInstanceUsername"] = new_instance_username
        if new_instance_password is not None:
            parameters["NewInstancePassword"] = new_instance_password
        if delete_source is not None:
            parameters["DeleteSource"] = delete_source
        if copy_files is not None:
            parameters["CopyFiles"] = copy_files
        result: ResponseAliasFull = await self._post(
            url="ADSModule/CloneInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/CloneInstance", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/CloneInstance", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def clone_template(
        self,
        template_id: int,
        name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Clone an existing AMP Deployment Template.

        Endpoint: `ADSModule/CloneTemplate`

        .. note::
            If you need to get an AMP Templates ID, use :meth:`get_deployment_templates` and
            access the :attr:`DeploymentTemplate.id` attribute.


        Parameters
        ----------
        template_id : :class:`int`
            The Template ID to copy.
        name : :class:`str`
            The name for the newly cloned Template.
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
        parameters: dict[str, Any] = {"Id": template_id, "NewName": name}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/CloneTemplate",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/CloneTemplate", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/CloneTemplate", result)  # noqa: EM101

    @Base.ads_only
    async def create_deployment_template(
        self,
        template_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Create a new Deployment Template. Typically used in conjunction with :meth:`update_deployment_template`.

        Endpoint: `ADSModule/CreateDeploymentTemplate`

        Parameters
        ----------
        template_name : :class:`str`
            The name for the newly created Template.
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
        parameters: dict[str, str] = {"Name": template_name}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/CreateDeploymentTemplate",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/CreateDeploymentTemplate", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/CreateDeploymentTemplate", result)  # noqa: EM101

    @Base.ads_only
    async def create_instance(
        self,
        instance: CreateInstance,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Create an AMP Instance.

        Endpoint: `ADSModule/CreateInstance`

        .. note::
            See the :class:`CreateInstance` for more details on how to configure the Instance when creating.


        Parameters
        ----------
        instance : :class:`CreateInstance`
            Your pre-created data structure to be parsed for the required API parameters.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask` | :class:`RunningTaskResponse`
            On success returns a :class:`RunningTask` dataclass, or the raw dictionary when `format_data` is False.
            AMP 2.8 answers with a running task that also carries the :class:`ActionResult` keys.

        """
        await self._reauth()
        # if isinstance(instance, CreateInstance):
        parameters: dict[Any, Any] = instance.to_dict()

        result: ResponseAliasFull = await self._post(
            url="ADSModule/CreateInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/CreateInstance", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/CreateInstance", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def create_instance_from_spec(
        self,
        spec_id: str,
        target_ads: str,
        friendly_name: str,
        post_create: Union[PostCreateState, None] = None,
        start_on_boot: bool | None = None,
        # target_datastore: str | None = None,
        target_datastore: Union[int, None] = None,
        group: str | None = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Create an Instance based upon the Spec ID provided.

        Endpoint: `ADSModule/CreateInstanceFromSpec`

        .. versionchanged:: 5.0.0
            `target_datastore` is an :class:`int`. 4.x annotated it as a :class:`str`, but AMP's `TargetDatastore` is an
            Int32.

        Parameters
        ----------
        spec_id : :class:`str`
            The Spec GUID.
        target_ads : :class:`str`
            The Target ADS Instance ID.
        friendly_name : :class:`str`
            The friendly name of the Instance.
        post_create : Union[:class:`PostCreateState`, None], optional
            The action the Instance will take after creation, by default None.
        start_on_boot : :class:`bool | None`, optional
            If the Instance should start on PC boot, by default None.
        target_datastore : Union[:class:`int`, None], optional
            The Datastore ID if any to attach the Instance to, by default None.
        group : :class:`str | None`, optional
            The Group ID, by default None.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask` | :class:`RunningTaskResponse`
            On success returns a :class:`RunningTask` dataclass, or the raw dictionary when `format_data` is False.
            AMP 2.8 answers with a running task that also carries the :class:`ActionResult` keys.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"SpecId": spec_id, "TargetADSInstance": target_ads, "FriendlyName": friendly_name}
        if post_create is not None:
            parameters["PostCreate"] = post_create.value
        if start_on_boot is not None:
            parameters["StartOnBoot"] = start_on_boot
        if target_datastore is not None:
            parameters["TargetDatastore"] = target_datastore
        if group is not None:
            parameters["Group"] = group
        result: ResponseAliasFull = await self._post(
            url="ADSModule/CreateInstanceFromSpec",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/CreateInstanceFromSpec", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/CreateInstanceFromSpec", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def delete_datastore(
        self,
        datastore_id: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete the specified Datastore by ID.

        Endpoint: `ADSModule/DeleteDatastore`

        .. note::
            You will need to know the Datastore ID you want to delete. See :meth:`get_datastores` as a means to get the IDs.


        Parameters
        ----------
        datastore_id : :class:`int`
            The datastore ID.
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
        parameters: dict[str, int] = {"id": datastore_id}

        result: ResponseAliasFull = await self._post(
            url="ADSModule/DeleteDatastore",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/DeleteDatastore", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/DeleteDatastore", result)  # noqa: EM101

    @Base.ads_only
    async def delete_deployment_template(
        self,
        template_id: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete an existing Deployment Template.

        Endpoint: `ADSModule/DeleteDeploymentTemplate`

        .. note::
            If you need to get an AMP Templates ID, use :meth:`get_deployment_templates` and
            access the :attr:`DeploymentTemplate.id` attribute.


        Parameters
        ----------
        template_id : :class:`int`
            The Template ID.
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
        parameters: dict[str, int] = {"Id": template_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/DeleteDeploymentTemplate",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/DeleteDeploymentTemplate", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/DeleteDeploymentTemplate", result)  # noqa: EM101

    @Base.ads_only
    async def delete_instance(
        self,
        instance_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Delete an Instance.

        Endpoint: `ADSModule/DeleteInstance`

        .. note::
            The `instance_name` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name : :class:`str`
            The Instance name.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"InstanceName": instance_name}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/DeleteInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/DeleteInstance", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/DeleteInstance", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def delete_instance_users(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete all Users from an Instance.

        Endpoint: `ADSModule/DeleteInstanceUsers`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
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
            url="ADSModule/DeleteInstanceUsers",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/DeleteInstanceUsers", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/DeleteInstanceUsers", result)  # noqa: EM101

    @Base.ads_only
    async def deploy_template(
        self,
        template: Template,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Deploy an Instance template.

        Endpoint: `ADSModule/DeployTemplate`

        .. versionchanged:: 5.0.0
            Returns a :class:`RunningTask`, and sends AMP's parameter names through :meth:`Template.to_dict`.

        Parameters
        ----------
        template : :class:`Template`
            Your pre-created data structure to be parsed for the required API parameters.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask` | :class:`RunningTaskResponse`
            On success returns a :class:`RunningTask` dataclass, or the raw dictionary when `format_data` is False.

        """
        await self._reauth()
        parameters: dict[str, Any] = template.to_dict()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/DeployTemplate",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/DeployTemplate", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        # The spec names a RunningTask for this endpoint, not an ActionResult.
        # if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
        #     if format_data is True:
        #         return ActionResult.from_response(result)
        #     return result
        # raise AMPAPIKeyError("status", "ADSModule/DeployTemplate", result)
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/DeployTemplate", result)  # noqa: EM101

    @Base.ads_only
    async def detach_target(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        De-tach an Instance from the ADS.

        Endpoint: `ADSModule/DetachTarget`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
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
        parameters: dict[str, str] = {"Id": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/DetachTarget",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/DetachTarget", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/DetachTarget", result)  # noqa: EM101

    @Base.ads_only
    async def extract_everywhere(
        self,
        source_archive: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Extracts everything from an archive.

        Endpoint: `ADSModule/ExtractEverywhere`

        .. note::
            The parameter `source_archive` will be sanitized. See :meth:`~Base.sanitize_path`.


        Parameters
        ----------
        source_archive : :class:`str`
            The source archive, typically a path to the archive.
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
        parameters: dict[str, str] = {"SourceArchive": self.sanitize_path(path=source_archive)}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/ExtractEverywhere",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/ExtractEverywhere", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/ExtractEverywhere", result)  # noqa: EM101

    @Base.ads_only
    async def get_application_endpoints(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Endpoints] | list[EndpointsResponse]:
        """|coro|

        Get the application endpoints for the specified Instance.

        Endpoint: `ADSModule/GetApplicationEndpoints`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`Endpoints`]
            Returns a list of endpoints for the specified Instance.

        """
        await self._reauth()
        parameters: dict[str, str] = {"instanceId": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetApplicationEndpoints",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetApplicationEndpoints", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if is_response_list(result, EndpointsResponse, ENDPOINTS_REQUIRED_KEYS, ENDPOINTS_EXCLUDED_KEYS):
            if format_data is True:
                return [Endpoints.from_response(entry) for entry in result]
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetApplicationEndpoints", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_datastore(
        self,
        datastore_id: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> InstanceDatastore | InstanceDatastoreResponse:
        """|coro|

        Get the information for the specified datastore.

        Endpoint: `ADSModule/GetDatastore`

        .. note::
            You will need to know the Datastore ID you want to retrieve. See :meth:`get_datastores` as a means to get the IDs.


        Parameters
        ----------
        datastore_id : :class:`int`
            The datastore ID.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`InstanceDatastore`
            On success returns an :class:`InstanceDatastore` dataclass.

        """
        await self._reauth()
        parameters: dict[str, int] = {"id": datastore_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetDatastore",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/GetDatastore", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, InstanceDatastoreResponse, INSTANCE_DATASTORE_REQUIRED_KEYS, INSTANCE_DATASTORE_EXCLUDED_KEYS):
            if format_data is True:
                return InstanceDatastore.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetDatastore", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def get_datastores(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[InstanceDatastore] | list[InstanceDatastoreResponse]:
        """|coro|

        Get a list of Datastores.

        Endpoint: `ADSModule/GetDatastores`

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
        list[:class:`InstanceDatastore`]
            On success returns a list of :class:`InstanceDatastore` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(url="ADSModule/GetDatastores", request_params=request_params, **response_params)
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetDatastores", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if is_response_list(result, InstanceDatastoreResponse, INSTANCE_DATASTORE_REQUIRED_KEYS, INSTANCE_DATASTORE_EXCLUDED_KEYS):
            if format_data is True:
                return [InstanceDatastore.from_response(entry) for entry in result]
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetDatastores", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_datastore_instances(
        self,
        datastore_id: int,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[InstanceResponse]:
        """|coro|

        Get a list of Instances tied to the specified datastore.

        Endpoint: `ADSModule/GetDatastoreInstances`

        .. note::
            You will need to know the Datastore ID you want to query. See :meth:`get_datastores` as a means to get the IDs.


        Parameters
        ----------
        datastore_id : :class:`int`
            The datastore ID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`InstanceResponse`]
            On success returns a list of raw Instance dicts. No :class:`Instance` is built from them.

        """
        await self._reauth()
        parameters: dict[str, int] = {"datastoreId": datastore_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetDatastoreInstances",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetDatastoreInstances", cur_type=result, expec_type=list)
        if is_response_list(result, InstanceResponse, INSTANCE_REQUIRED_KEYS, INSTANCE_EXCLUDED_KEYS):
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetDatastoreInstances", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_deployment_templates(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[DeploymentTemplate] | list[DeploymentTemplateResponse]:
        """|coro|

        Gets a list of Deployment Templates.

        Endpoint: `ADSModule/GetDeploymentTemplates`

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
        list[:class:`DeploymentTemplate`]
            On success returns a list of :class:`DeploymentTemplate` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetDeploymentTemplates",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetDeploymentTemplates", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if is_response_list(result, DeploymentTemplateResponse, DEPLOYMENT_TEMPLATE_REQUIRED_KEYS, DEPLOYMENT_TEMPLATE_EXCLUDED_KEYS):
            if format_data is True:
                # return [DeploymentTemplate(**entry) for entry in result]
                return [DeploymentTemplate.from_response(entry) for entry in result]
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetDeploymentTemplates", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_group(
        self,
        group_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[ControllerResponse, None]:
        """|coro|

        Get the specified group.

        Endpoint: `ADSModule/GetGroup`

        .. note::
            AMP answers with the Target item for the ID, the same shape as one entry of :meth:`get_instances`.
            JSON null means the Target is gone, and this method returns None for it.


        Parameters
        ----------
        group_id : :class:`str`
            The ADS ID of the Target, the `instance_id` of a :meth:`get_instances` entry.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Union[:class:`ControllerResponse`, None]
            On success returns the Target dictionary, or None when AMP answers with JSON null.

        """
        await self._reauth()
        # AMP answers JSON null when the Target is gone, which is not an error here.
        response_params["allow_null"] = True
        parameters: dict[str, str] = {"groupId": group_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetGroup",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if result is None:
            return None

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/GetGroup", cur_type=result, expec_type=dict)
        if is_response_type(result, ControllerResponse, CONTROLLER_REQUIRED_KEYS, CONTROLLER_EXCLUDED_KEYS):
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetGroup", cur_type=result, expec_type=dict)

    async def get_instance(
        self,
        instance_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> InstanceResponse:
        """|coro|

        Returns the Instance information for the provided Instance ID.

        Endpoint: `ADSModule/GetInstance`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`InstanceResponse`
            On success returns a raw Instance dict.

        """
        await self._reauth()
        parameters: dict[str, str] = {"InstanceId": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/GetInstance", cur_type=result, expec_type=dict)
        if is_response_type(result, InstanceResponse, INSTANCE_REQUIRED_KEYS, INSTANCE_EXCLUDED_KEYS):
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetInstance", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def get_instances(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[ControllerResponse]:
        """|coro|

        Returns a list of all Instances the Target ADS or Controller and AMP User has permission to access.

        Endpoint: `ADSModule/GetInstances`

        .. note::
            AMP's `ForceIncludeSelf` is always sent as True, so the ADS's own Target is in the list.


        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`ControllerResponse`]
            On success returns a raw list of Target dicts.

        """
        await self._reauth()
        parameters: dict[str, bool] = {"ForceIncludeSelf": True}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetInstances",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetInstances", cur_type=result, expec_type=list)
        if is_response_list(result, ControllerResponse, CONTROLLER_REQUIRED_KEYS, CONTROLLER_EXCLUDED_KEYS):
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetInstances", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_instance_live_settings(
        self,
        instance_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> dict[str, str]:
        """|coro|

        Get the live settings of an Instance, keyed by setting node name.

        Endpoint: `ADSModule/GetInstanceLiveSettings`

        .. note::
            Requires the `ADS.InstanceManagement.CreateInstance` permission.


        Parameters
        ----------
        instance_id : :class:`str`
            The ID of the Instance.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        dict[:class:`str`, :class:`str`]
            On success returns a dictionary of setting node names and their values.

        """
        await self._reauth()
        parameters: dict[str, str] = {"instanceId": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetInstanceLiveSettings",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/GetInstanceLiveSettings", cur_type=result, expec_type=dict)
        # The keys are AMP setting node names, a user defined mapping that cannot be typed any further.
        return result  # pyright: ignore[reportReturnType]

    @Base.ads_only
    async def get_instance_network_info(
        self,
        instance_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[PortInfo] | list[PortInfoResponse]:
        """|coro|

        Get the Port and or Network information of an Instance.

        Endpoint: `ADSModule/GetInstanceNetworkInfo`

        .. note::
            The `instance_name` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name : :class:`str`
            The name of the Instance we are targeting.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`PortInfo`]
            On success returns a list of :class:`PortInfo` dataclasses.

        """
        await self._reauth()
        parameters: dict[str, str] = {"instanceName": instance_name}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetInstanceNetworkInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetInstanceNetworkInfo", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if is_response_list(result, PortInfoResponse, PORT_INFO_REQUIRED_KEYS, PORT_INFO_EXCLUDED_KEYS):
            if format_data is True:
                return [PortInfo.from_response(entry) for entry in result]
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetInstanceNetworkInfo", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_instance_statuses(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[InstanceStatus] | list[InstanceStatusResponse]:
        """|coro|

        Returns a list of the AMP Instance statuses.

        Endpoint: `ADSModule/GetInstanceStatuses`

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
        list[:class:`InstanceStatus`]
            On success returns a list of :class:`InstanceStatus` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetInstanceStatuses",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetInstanceStatuses", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if is_response_list(result, InstanceStatusResponse, INSTANCE_STATUS_REQUIRED_KEYS, INSTANCE_STATUS_EXCLUDED_KEYS):
            if format_data is True:
                return [InstanceStatus.from_response(entry) for entry in result]
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetInstanceStatuses", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_local_instances(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Instance] | list[InstanceResponse]:
        """|coro|

        Gets the local Instances related to the ADS or Controller.

        Endpoint: `ADSModule/GetLocalInstances`

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`Instance`]
            On success returns a raw list of Instance dicts.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetLocalInstances",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetLocalInstances", cur_type=result, expec_type=list)
        if is_response_list(result, InstanceResponse, INSTANCE_REQUIRED_KEYS, INSTANCE_EXCLUDED_KEYS):
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetLocalInstances", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_mode(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ADSModeState:
        """|coro|

        Gets the role of the ADS this object logs in to (Controller, Target, hybrid or standalone).

        Endpoint: `Core/GetConfig`

        .. note::
            This reads the `ADSModule.ADS.Mode` setting, so any logged in user can read it on the ADS they log in to.

        .. note::
            The mode is not cached, so every call asks AMP.

        Parameters
        ----------
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ADSModeState`
            The ADS mode, or `ADSModeState.not_set` (with a warning logged) when AMP sends a value the enum lacks.

        """
        await self._reauth()
        parameters: dict[str, str] = {"node": "ADSModule.ADS.Mode"}
        result: ResponseAliasFull = await self._post(
            url="Core/GetConfig",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="Core/GetConfig", cur_type=result, expec_type=dict)
        if "subcategory" not in result:
            raise AMPAPIKeyError("subcategory", "Core/GetConfig", result)  # noqa: EM101

        mode_value = result["current_value"]
        # A value the enum lacks raises ValueError, whether an unknown number or not a number at all.
        with contextlib.suppress(ValueError):
            return ADSModeState(mode_value)

        LOGGER.warning(
            "<%s.%s> | Unknown ADSModule.ADS.Mode value: %r | Returning ADSModeState.not_set",
            __class__.__name__,
            "get_mode",
            mode_value,
        )
        return ADSModeState.not_set

    @Base.ads_only
    async def get_provision_arguments(
        self,
        module_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[ProvisionSettingInfo] | list[ProvisionSettingInfoResponse]:
        """|coro|

        Get Provision Arguments.

        Endpoint: `ADSModule/GetProvisionArguments`

        Parameters
        ----------
        module_name : :class:`str`
            The Module Name (eg. "Minecraft").
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`ProvisionSettingInfo`]
            On success returns a list of :class:`ProvisionSettingInfo` dataclasses.

        """
        await self._reauth()
        parameters: dict[str, str] = {"ModuleName": module_name}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetProvisionArguments",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetProvisionArguments", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if is_response_list(
            result,
            ProvisionSettingInfoResponse,
            PROVISION_SETTING_INFO_REQUIRED_KEYS,
            PROVISION_SETTING_INFO_EXCLUDED_KEYS,
        ):
            if format_data is True:
                return [ProvisionSettingInfo.from_response(entry) for entry in result]
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetProvisionArguments", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_provision_fitness(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Provision | ProvisionResponse | None:
        """|coro|

        Get the provision fitness of the ADS or Controller.

        Endpoint: `ADSModule/GetProvisionFitness`

        .. note::
            AMP answers with JSON `null` when it has no fitness data.

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
        :class:`Provision` | None
            On success returns a :class:`Provision` dataclass, or None when AMP answers with JSON null.

        """
        await self._reauth()
        # AMP answers JSON null when it has no fitness data, which is not an error here.
        response_params["allow_null"] = True
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetProvisionFitness",
            request_params=request_params,
            **response_params,
        )
        if result is None:
            return None

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/GetProvisionFitness", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ProvisionResponse, PROVISION_REQUIRED_KEYS, PROVISION_EXCLUDED_KEYS):
            if format_data is True:
                return Provision.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetProvisionFitness", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def get_supported_app_summaries(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Application] | list[AppSummaryResponse]:
        """|coro|

        Get a condensed summary of every application that can be deployed. See :meth:`get_supported_applications` for the full entries.

        Endpoint: `ADSModule/GetSupportedAppSummaries`

        .. note::
            Each entry is an :class:`Application` that leaves out `module_name`, `settings` and `is_multi_ip_aware`.


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
        list[:class:`Application`]
            On success returns a list of :class:`Application` dataclasses.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetSupportedAppSummaries",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetSupportedAppSummaries", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if is_response_list(result, AppSummaryResponse, APP_SUMMARY_REQUIRED_KEYS, APP_SUMMARY_EXCLUDED_KEYS):
            if format_data is True:
                return [Application.from_response(entry) for entry in result]
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetSupportedAppSummaries", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_supported_applications(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Application] | list[ApplicationResponse]:
        """|coro|

        Get supported applications, such as :class:`Template` information and the list of :class:`Application` when creating an Instance.

        Endpoint: `ADSModule/GetSupportedApplications`

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
        list[:class:`Application`]
            Returns a list of all applications that can be deployed.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetSupportedApplications",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="ADSModule/GetSupportedApplications", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if is_response_list(result, ApplicationResponse, APPLICATION_REQUIRED_KEYS, APPLICATION_EXCLUDED_KEYS):
            if format_data is True:
                return [Application.from_response(entry) for entry in result]
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetSupportedApplications", cur_type=result, expec_type=list)

    @Base.ads_only
    async def get_target_info(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RemoteTargetInfo | RemoteTargetInfoResponse:
        """|coro|

        Get target info.

        Endpoint: `ADSModule/GetTargetInfo`

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
        :class:`RemoteTargetInfo`
            On success returns a :class:`RemoteTargetInfo` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/GetTargetInfo",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/GetTargetInfo", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, RemoteTargetInfoResponse, REMOTE_TARGET_INFO_REQUIRED_KEYS, REMOTE_TARGET_INFO_EXCLUDED_KEYS):
            if format_data is True:
                return RemoteTargetInfo.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/GetTargetInfo", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def get_target_pairing_code(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Get the ADS/Target pairing code. Used with :meth:`attach_ads` using the "pairing_code" parameter.

        Endpoint: `ADSModule/GetTargetPairingCode`

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
            url="ADSModule/GetTargetPairingCode",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/GetTargetPairingCode", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/GetTargetPairingCode", result)  # noqa: EM101

    @Base.ads_only
    async def handout_instance_configs(
        self,
        module: str,
        setting_node: str,
        values: list[str],
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Handout Instance Configuration.

        Endpoint: `ADSModule/HandoutInstanceConfigs`

        Parameters
        ----------
        module : :class:`str`
            The Module Name. eg. "Minecraft".
        setting_node : :class:`str`
            A setting node. See :ref:`Setting Nodes <Documentation>` for more information.
        values : list[:class:`str`]
            The values for the setting node.
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
        parameters: dict[str, Any] = {"ForModule": module, "SettingNode": setting_node, "Values": values}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/HandoutInstanceConfigs",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/HandoutInstanceConfigs", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/HandoutInstanceConfigs", result)  # noqa: EM101

    @Base.ads_only
    async def manage_instance(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Manage the specified Instance.

        Endpoint: `ADSModule/ManageInstance`

        .. note::
            Actual usage unknown, may be used for AMP Instance management via the web interface.


        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
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
        parameters: dict[str, str] = {"instanceId": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/ManageInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/ManageInstance", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/ManageInstance", result)  # noqa: EM101

    @Base.ads_only
    async def modify_custom_firewall_rule(
        self,
        instance_id: str,
        port_number: int,
        range_: int,
        protocol: int,
        description: str,
        open_: bool = True,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Modify the Firewall Rule of the specified Instance.

        Endpoint: `ADSModule/ModifyCustomFirewallRule`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
        port_number : :class:`int`
            Port number.
        range_ : :class:`int`
            Port range.
        protocol : :class:`int`
            UDP/TCP/Both.
        description : :class:`str`
            Description for which the rule is applied.
        open_ : :class:`bool`, optional
            Open or close the port mapping, by default True.
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
            "instanceId": instance_id,
            "portNumber": port_number,
            "range": range_,
            "protocol": protocol,
            "description": description,
            "open": open_,
        }
        result: ResponseAliasFull = await self._post(
            url="ADSModule/ModifyCustomFirewallRule",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/ModifyCustomFirewallRule", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/ModifyCustomFirewallRule", result)  # noqa: EM101

    @Base.ads_only
    async def move_instance_datastore(
        self,
        instance_id: str,
        datastore_id: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Move an Instance to a different Datastore.

        Endpoint: `ADSModule/MoveInstanceDatastore`

        .. note::
            You will need to know the Datastore ID you want to move the Instance to. See :meth:`get_datastores` as a means to get the IDs.


        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID to move.
        datastore_id : :class:`int`
            The ID of the datastore to move the Instance to.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"instanceId": instance_id, "datastoreId": datastore_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/MoveInstanceDatastore",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/MoveInstanceDatastore", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/MoveInstanceDatastore", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def prepare_file_transfer(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Prepare an Instance for a file transfer.

        Endpoint: `ADSModule/PrepareFileTransfer`

        .. note::
            Requires the `ADS.InstanceManagement.CreateInstance` permission.


        Parameters
        ----------
        instance_id : :class:`str`
            The ID of the Instance.
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
        parameters: dict[str, str] = {"instanceId": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/PrepareFileTransfer",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/PrepareFileTransfer", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/PrepareFileTransfer", result)  # noqa: EM101

    async def reactivate_instance(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Reactivate a specific Instance.

        Endpoint: `ADSModule/ReactivateInstance`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"instanceId": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/ReactivateInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/ReactivateInstance", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/ReactivateInstance", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def reactivate_local_instances(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Reactivate local Instances.

        Endpoint: `ADSModule/ReactivateLocalInstances`

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
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/ReactivateLocalInstances",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/ReactivateLocalInstances", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/ReactivateLocalInstances", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def refresh_app_cache(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Refresh the application cache.

        Endpoint: `ADSModule/RefreshAppCache`

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
        return await self._post(
            url="ADSModule/RefreshAppCache",
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @Base.ads_only
    async def refresh_group(
        self,
        group_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Refresh the specified group.

        Endpoint: `ADSModule/RefreshGroup`

        Parameters
        ----------
        group_id : :class:`str`
            The Group ID to refresh.
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
        parameters: dict[str, str] = {"groupId": group_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/RefreshGroup",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/RefreshGroup", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/RefreshGroup", result)  # noqa: EM101

    @Base.ads_only
    async def refresh_instance_config(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Refresh an Instance Configuration.

        Endpoint: `ADSModule/RefreshInstanceConfig`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
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
            url="ADSModule/RefreshInstanceConfig",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/RefreshInstanceConfig", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/RefreshInstanceConfig", result)  # noqa: EM101

    @Base.ads_only
    async def refresh_remote_config_stores(
        self,
        force: bool = False,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Refresh remote config stores.

        Endpoint: `ADSModule/RefreshRemoteConfigStores`

        Parameters
        ----------
        force : :class:`bool`, optional
            Force refresh, by default False.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, bool] = {"force": force}
        return await self._post(
            url="ADSModule/RefreshRemoteConfigStores",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @Base.ads_only
    async def register_target(
        self,
        controller_url: str,
        my_url: str,
        username: str,
        password: str,
        friendly_name: str,
        two_factor_token: str = "",
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Registers a Target to a Controller.

        Endpoint: `ADSModule/RegisterTarget`

        Parameters
        ----------
        controller_url : :class:`str`
            The Controller panel URL.
        my_url : :class:`str`
            The Target AMP panel URL.
        username : :class:`str`
            The username for logging into the Target AMP panel.
        password : :class:`str`
            The password for logging into the Target AMP panel.
        friendly_name : :class:`str`
            Instance Friendly Name.
        two_factor_token : :class:`str`, optional
            The two-factor authentication token for the username, by default "".
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
            "controllerUrl": controller_url,
            "myUrl": my_url,
            "username": username,
            "password": password,
            "twoFactorToken": two_factor_token,
            "friendlyName": friendly_name,
        }
        result: ResponseAliasFull = await self._post(
            url="ADSModule/RegisterTarget",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/RegisterTarget", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/RegisterTarget", result)  # noqa: EM101

    @Base.ads_only
    async def register_target_with_code(
        self,
        controller_url: str,
        my_url: str,
        code: str,
        friendly_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Registers an Instance to a Controller/Target with pairing code.

        Endpoint: `ADSModule/RegisterTargetWithCode`

        Parameters
        ----------
        controller_url : :class:`str`
            The Controller panel URL.
        my_url : :class:`str`
            The Target AMP panel URL.
        code : :class:`str`
            The pairing code from :meth:`get_target_pairing_code`.
        friendly_name : :class:`str`
            Instance Friendly Name.
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
            "controllerUrl": controller_url,
            "myUrl": my_url,
            "code": code,
            "friendlyName": friendly_name,
        }
        result: ResponseAliasFull = await self._post(
            url="ADSModule/RegisterTargetWithCode",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/RegisterTargetWithCode", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/RegisterTargetWithCode", result)  # noqa: EM101

    @Base.ads_only
    async def repair_datastore(
        self,
        datastore_id: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Repair the specified datastore.

        Endpoint: `ADSModule/RepairDatastore`

        .. note::
            You will need to know the Datastore ID you want to repair. See :meth:`get_datastores` as a means to get the IDs.


        Parameters
        ----------
        datastore_id : :class:`int`
            The datastore ID.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        parameters: dict[str, int] = {"id": datastore_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/RepairDatastore",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/RepairDatastore", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/RepairDatastore", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def request_datastore_size_calculation(
        self,
        datastore_id: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Request a calculation of the size of the specified Datastore.

        Endpoint: `ADSModule/RequestDatastoreSizeCalculation`

        .. note::
            You will need to know the Datastore ID you want to query. See :meth:`get_datastores` as a means to get the IDs.


        Parameters
        ----------
        datastore_id : :class:`int`
            The datastore ID.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        parameters: dict[str, int] = {"datastoreId": datastore_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/RequestDatastoreSizeCalculation",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/RequestDatastoreSizeCalculation", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/RequestDatastoreSizeCalculation", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def restart_instance(
        self,
        instance_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Restart an Instance.

        Endpoint: `ADSModule/RestartInstance`

        .. note::
            The `instance_name` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name : :class:`str`
            The Instance Name.
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
        parameters: dict[str, str] = {"InstanceName": instance_name}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/RestartInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/RestartInstance", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/RestartInstance", result)  # noqa: EM101

    # TODO: Returns Any; build a dataclass and TypedDict once the response shape has been confirmed.
    @Base.ads_only
    async def servers(
        self,
        id_: str,
        req_rawjson: str = "application/json",
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Any:
        """|coro|

        Used for proxy authentication.

        Endpoint: `ADSModule/Servers`

        .. warning::
            This Endpoint has not been fully tested, multiple parameters are unknown, or functionality is unknown.


        .. warning::
            `ADSModule/Servers` is AMP's proxy route, the one the library uses as a URL path in `ADSModule/Servers/<ID>/API/...`.
            Calling it as an endpoint fails, AMP 2.8.0.8 answers "Index was outside the bounds of the array".


        Parameters
        ----------
        id_ : :class:`str`
            The Instance ID.
        req_rawjson : :class:`str`, optional
            The data type, by default "application/json".
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Any
            UNK.

        """
        await self._reauth()
        parameters: dict[str, str] = {"id": id_, "REQ_RAWJSON": req_rawjson}
        return await self._post(
            url="ADSModule/Servers",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

    @Base.ads_only
    async def set_instance_config(
        self,
        instance_name: str,
        setting_node: str,
        value: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Set an :class:`Instance` Setting Node setting.

        Endpoint: `ADSModule/SetInstanceConfig`

        .. note::
            See :ref:`Setting Nodes <Documentation>` for possible `setting_node` values.


        .. note::
            The `instance_name` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name : :class:`str`
            The Instance name.
        setting_node : :class:`str`
            The setting node name.
        value : :class:`str`
            The value for the setting node.
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
        parameters: dict[str, str] = {"InstanceName": instance_name, "SettingNode": setting_node, "Value": value}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/SetInstanceConfig",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/SetInstanceConfig", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/SetInstanceConfig", result)  # noqa: EM101

    @Base.ads_only
    async def set_instance_network_info(
        self,
        instance_id: str,
        port_mappings: dict[str, int],
        application_ip: str | None = None,
        must_stop: bool | None = None,
        *,
        advertised_address: Union[str, None] = None,
        advertised_address_includes_port: Union[bool, None] = None,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Set the Port mappings for an Instance.

        Endpoint: `ADSModule/SetInstanceNetworkInfo`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID.
        port_mappings : dict[:class:`str`, :class:`int`]
            Port ranges and protocols to map.
        application_ip : :class:`str | None`, optional
            The IP the application will be bound to, by default None.
        must_stop : :class:`bool | None`, optional
            UNK, by default None.
        advertised_address : Union[:class:`str`, None], optional
            The address AMP advertises for the Instance, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
        advertised_address_includes_port : Union[:class:`bool`, None], optional
            If `advertised_address` already includes the port, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
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
        parameters: dict[str, Any] = {"InstanceId": instance_id, "PortMappings": port_mappings}
        if application_ip is not None:
            parameters["ApplicationIP"] = application_ip
        if must_stop is not None:
            parameters["mustStop"] = must_stop
        if advertised_address is not None:
            parameters["AdvertisedAddress"] = advertised_address
        if advertised_address_includes_port is not None:
            parameters["AdvertisedAddressIncludesPort"] = advertised_address_includes_port
        result: ResponseAliasFull = await self._post(
            url="ADSModule/SetInstanceNetworkInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/SetInstanceNetworkInfo", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/SetInstanceNetworkInfo", result)  # noqa: EM101

    @Base.ads_only
    async def set_instance_suspended(
        self,
        instance_name: str,
        suspended: bool = False,
        *,
        suspend_reason: Union[str, None] = None,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Set an Instance's suspended state.

        Endpoint: `ADSModule/SetInstanceSuspended`

        .. note::
            The `instance_name` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name : :class:`str`
            The Instance name.
        suspended : :class:`bool`, optional
            Set the Instance to be suspended, by default False.
        suspend_reason : Union[:class:`str`, None], optional
            The reason the Instance is suspended, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
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
        parameters: dict[str, Any] = {"InstanceName": instance_name, "Suspended": suspended}
        if suspend_reason is not None:
            parameters["SuspendReason"] = suspend_reason
        result: ResponseAliasFull = await self._post(
            url="ADSModule/SetInstanceSuspended",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/SetInstanceSuspended", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/SetInstanceSuspended", result)  # noqa: EM101

    @Base.ads_only
    async def start_all_instances(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Start all Instances.

        Endpoint: `ADSModule/StartAllInstances`

        Parameters
        ----------
        instance_id : :class:`str`
            The Target ADS Instance ID.
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
        parameters: dict[str, str] = {"TargetADSInstance": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/StartAllInstances",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/StartAllInstances", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/StartAllInstances", result)  # noqa: EM101

    @Base.ads_only
    async def start_instance(
        self,
        instance_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Start an Instance.

        Endpoint: `ADSModule/StartInstance`

        .. note::
            The `instance_name` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name : :class:`str`
            The Instance name.
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
        parameters: dict[str, str] = {"InstanceName": instance_name}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/StartInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/StartInstance", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/StartInstance", result)  # noqa: EM101

    @Base.ads_only
    async def stop_all_instances(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Stop all Instances.

        Endpoint: `ADSModule/StopAllInstances`

        Parameters
        ----------
        instance_id : :class:`str`
            The Target ADS Instance ID.
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
        parameters: dict[str, str] = {"TargetADSInstance": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/StopAllInstances",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/StopAllInstances", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/StopAllInstances", result)  # noqa: EM101

    @Base.ads_only
    async def stop_instance(
        self,
        instance_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Stop an Instance.

        Endpoint: `ADSModule/StopInstance`

        .. note::
            The `instance_name` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name : :class:`str`
            The Instance name.
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
        parameters: dict[str, str] = {"InstanceName": instance_name}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/StopInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/StopInstance", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/StopInstance", result)  # noqa: EM101

    @Base.ads_only
    async def update_datastore(
        self,
        updated_datastore: InstanceDatastore | InstanceDatastoreResponse,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update an existing datastore.

        Endpoint: `ADSModule/UpdateDatastore`

        Parameters
        ----------
        updated_datastore : :class:`InstanceDatastore`
            Your pre-created data structure to be parsed for the required API parameters.
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
        # Accepts the dataclass or the raw InstanceDatastoreResponse; the TypedDict is already a dict.
        data: dict[str, Any] = updated_datastore.to_dict() if isinstance(updated_datastore, InstanceDatastore) else dict(updated_datastore)
        parameters: dict[str, Any] = {"updatedDatastore": data}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/UpdateDatastore",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/UpdateDatastore", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/UpdateDatastore", result)  # noqa: EM101

    @Base.ads_only
    async def update_deployment_template(
        self,
        template_to_update: DeploymentTemplate,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update an existing Deployment Template.

        Endpoint: `ADSModule/UpdateDeploymentTemplate`

        Parameters
        ----------
        template_to_update : :class:`DeploymentTemplate`
            Your pre-created data structure to be parsed for the required API parameters.
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
        data: dict[str, Any] = template_to_update.to_dict()
        parameters: dict[str, Any] = {"templateToUpdate": data}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/UpdateDeploymentTemplate",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/UpdateDeploymentTemplate", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/UpdateDeploymentTemplate", result)  # noqa: EM101

    @Base.ads_only
    async def update_instance_info(
        self,
        instance_info: InstanceInfo,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Update an Instance's info.

        Endpoint: `ADSModule/UpdateInstanceInfo`

        .. versionchanged:: 5.0.0
            Returns a :class:`RunningTask`, and sends AMP's parameter names through :meth:`InstanceInfo.to_dict`.

        Parameters
        ----------
        instance_info : :class:`InstanceInfo`
            Your pre-created data structure to be parsed for the required API parameters.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask` | :class:`RunningTaskResponse`
            On success returns a :class:`RunningTask` dataclass, or the raw dictionary when `format_data` is False.
            AMP 2.8 answers with a "Reconfiguring Instance" task that also carries the :class:`ActionResult` keys.

        """
        await self._reauth()
        parameters: dict[str, Any] = instance_info.to_dict()
        result: ResponseAliasFull = await self._post(
            url="ADSModule/UpdateInstanceInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/UpdateInstanceInfo", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        # AMP 2.8.0.8 answers with a RunningTask, not the ActionResult its spec names (vm1, 2026-10-24).
        # if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
        #     if format_data is True:
        #         return ActionResult.from_response(result)
        #     return result
        # raise AMPAPIKeyError("status", "ADSModule/UpdateInstanceInfo", result)
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result
        raise AMPAPITypeError(end_point="ADSModule/UpdateInstanceInfo", cur_type=result, expec_type=dict)

    @Base.ads_only
    async def update_target(
        self,
        target_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Update Target ADS Instance.

        Endpoint: `ADSModule/UpdateTarget`

        .. note::
            Typically this will be used on Instances with the :attr:`~Instance.module` == "ADS".


        Parameters
        ----------
        target_id : :class:`str`
            The Target Instance ID.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"TargetID": target_id}
        return await self._post(
            url="ADSModule/UpdateTarget",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    @Base.ads_only
    async def update_target_info(
        self,
        instance_id: str,
        friendly_name: str,
        url: str,
        description: str,
        tags: list[str],
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update a target Instance information.

        Endpoint: `ADSModule/UpdateTargetInfo`

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID for the Instance you want to update.
        friendly_name : :class:`str`
            The Instance friendly name you want to set.
        url : :class:`str`
            The Instance URL you want to set.
        description : :class:`str`
            The description for the Instance.
        tags : list[:class:`str`]
            The tags you want to add to the Instance.
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
            "id": instance_id,
            "friendlyName": friendly_name,
            "url": url,
            "description": description,
            "tags": tags,
        }
        result: ResponseAliasFull = await self._post(
            url="ADSModule/UpdateTargetInfo",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/UpdateTargetInfo", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/UpdateTargetInfo", result)  # noqa: EM101

    @Base.ads_only
    async def upgrade_all_instances(
        self,
        instance_id: str,
        restart_running: bool = False,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Upgrade all Instances.

        Endpoint: `ADSModule/UpgradeAllInstances`

        Parameters
        ----------
        instance_id : :class:`str`
            The Target ADS Instance ID.
        restart_running : :class:`bool`, optional
            Restart any running Instances, by default False.
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
        parameters: dict[str, Any] = {"RestartRunning": restart_running, "TargetADSInstance": instance_id}
        result: ResponseAliasFull = await self._post(
            url="ADSModule/UpgradeAllInstances",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/UpgradeAllInstances", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/UpgradeAllInstances", result)  # noqa: EM101

    @Base.ads_only
    async def upgrade_instance(
        self,
        instance_name: str,
        *,
        restart_if_running: Union[bool, None] = None,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Update or Upgrade the Instance.

        Endpoint: `ADSModule/UpgradeInstance`

        .. note::
            The `instance_name` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name : :class:`str`
            The Instance name.
        restart_if_running : Union[:class:`bool`, None], optional
            Restart the Instance after the upgrade if it is running, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
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
        # parameters: dict[str, str] = {"InstanceName": instance_name}
        # `RestartIfRunning` is a Boolean, so the values are no longer all strings.
        parameters: dict[str, Any] = {"InstanceName": instance_name}
        if restart_if_running is not None:
            parameters["RestartIfRunning"] = restart_if_running
        result: ResponseAliasFull = await self._post(
            url="ADSModule/UpgradeInstance",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="ADSModule/UpgradeInstance", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPIKeyError("status", "ADSModule/UpgradeInstance", result)  # noqa: EM101
