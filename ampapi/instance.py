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

import functools
import logging
import time
from pprint import pformat
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Optional, Self, Union, overload, override

from .adsmodule import ADSModule
from .analytics import AnalyticsPlugin
from .base import Base
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin
from .minecraft import MinecraftModule
from .modules import ActionResult, BuildInfo, InstanceState, Status, Updates

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable, Coroutine
    from typing import Concatenate, Unpack

    import aiohttp
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]
    from typing_extensions import ParamSpec, TypeVar

    from ._types import (
        ActionResultResponse,
        ControllerResponse,
        InstanceResponse,
        PlatformInfoResponse,
        StatusResponse,
        TargetDatastoreResponse,
        UpdatesResponse,
    )
    from .base import ResponseHandlerOptions
    from .bridge import Bridge

    D = TypeVar("D", bound="Instance")
    T = ParamSpec("T")
    F = TypeVar("F")

__all__ = ("Controller", "Instance", "MinecraftInstance", "TargetADS")


LOGGER: logging.Logger = logging.getLogger(__name__)
InstanceTypeAliases = Union["Instance", "MinecraftInstance", "TargetADS"]


class Instance(
    Core,
    EmailSenderPlugin,
    LocalFileBackupPlugin,
    FileManagerPlugin,
    AnalyticsPlugin,
    Updates,
):
    """:class:`Instance` represents an entire Instance from AMP that is not Controller, Target/ADS or Minecraft.\n
    This is similar to what you get when selecting 'Manage' an Instance from the Web GUI.

    .. note::
        - Do *NOT* change the :attr:`~Instance.module` attribute.
        - Attributes are cached! Please call the respective Endpoints to get current information.
        - To Update the attributes call :meth:`get_instance_status` or :meth:`get_updates`.
        - To check if the Instance is running, check the :attr:`running` property.
        - To check if the Application is running, check the :attr:`app_state` property.


    Parameters
    ----------
    data : Union[:class:`Instance`, None]
        The Instance data to be unpacked and set as attributes of this class to execute API calls.
    controller : Union[:class:`Controller`, None]
        The :class:`Controller` to be used to execute specific API calls.

    Attributes
    ----------
    amp_version : Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    application_endpoints : list[dict[str, str]]
        The list of application endpoints for the Instance.
    app_state : :class:`InstanceState`
        The state of the application.
    container_cpus : :class:`float`
        The amount of CPU cores allocated to the container, default is 0.0.
    container_memory_mb : :class:`int`
        The amount of memory allocated to the container in MB.
    container_memory_policy : :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance.
    daemon : :class:`bool`
        If the Instance is a daemon.
    daemon_autostart : :class:`bool`
        If the Instance should be autostart on boot.
    deployment_args : dict[:class:`str`, :class:`str`]
        The deployment arguments of the Instance.
    description : :class:`str`
        The description of the Instance, default is "".
    disk_usage_mb : :class:`int`
        The disk usage of the Instance in MB.
    display_image_source : :class:`str`
        The source of the display image, default is "".
    exclude_from_firewall : :class:`bool`
        If the Instance should be excluded from the firewall.
    friendly_name : :class:`str`
        The friendly name of the Instance.
    ip : :class:`str`
        The IP address of the Instance.
    instance_id : :class:`str`
        The Instance GUID.
    instance_name : :class:`str`
        The Instance name.
    is_container_instance : :class:`bool`
        If the Instance is a container Instance.
    is_https : :class:`bool`
        If the Instance is using HTTPS.
    management_mode : :class:`int`
        The management mode of the Instance.
    metrics : Union[dict[:class:`str`, :class:`MetricsKeyResponse`], None]
        The metrics of the Instance keyed by metric name, default is None.
    module : :class:`str`
        The module of the Instance.
    module_display_name : :class:`str`
        The display name of the module, default is "".
    port : :class:`str`
        The port of the Instance.
    release_stream : :class:`int`
        The release stream of the Instance.
    running : :class:`bool`
        If the Instance is running. *Not the application the Instance is managing,* see :attr:`app_state`.
    suspended : :class:`bool`
        If the Instance is suspended.
    tags : Union[:class:`None`, :class:`list`]
        The list of tags of the Instance, default is None.
    target_id : :class:`str`
        The target ID of the Instance.
    url : :class:`str`
        The API URL.

    """

    __slots__ = (
        "amp_version",
        # "app_state",
        "application_endpoints",
        "container_cpus",
        "container_memory_mb",
        "container_memory_policy",
        "daemon",
        "daemon_autostart",
        "deployment_args",
        "description",
        "disk_usage_mb",
        "display_image_source",
        "exclude_from_firewall",
        "friendly_name",
        "instance_id",
        "instance_name",
        "ip",
        "is_container_instance",
        "is_https",
        "management_mode",
        "metrics",
        "module",
        "module_display_name",
        "port",
        "release_stream",
        "running",
        "suspended",
        "tags",
        "target_id",
    )

    amp_version: dict[str, int] | str | BuildInfo
    _app_state: InstanceState | int
    url: str
    _controller: Union[Controller, None]

    @property
    def app_state(self) -> InstanceState:
        """The state of the application."""
        if isinstance(self._app_state, int):
            try:
                self._app_state = InstanceState(self._app_state)
            except (RuntimeError, TypeError, ValueError):
                return InstanceState.undefined

        return self._app_state

    def __init__(
        self,
        data: InstanceResponse,
        controller: Optional[Controller] = None,
        **kwargs: Any,
    ) -> None:
        """Build an Instance, unpacking an API response onto its attributes.

        Parameters
        ----------
        data : :class:`InstanceResponse`
            The Instance data to unpack onto this class.
        controller : :class:`Controller` | None, optional
            The Controller used to make ADSModule specific API calls, by default None.
        **kwargs : Any
            Keyword arguments forwarded to :meth:`Base.__init__`.

        """
        # LOGGER.debug("DEBUG %s __init__ %s", type(self).__name__, id(self))
        super().__init__(**kwargs)
        self._parse_instance_data(data=data)

        # We use the Controller class to call ADSModule specific Endpoints as a
        # typical Instance will not have the :py:class:`ADSModule` API Endpoints.
        self._controller = controller
        self._endpoint_url = f"{self._bridge.url}/API/ADSModule/Servers/{self._instance_id}"

    def __hash__(self) -> int:  # noqa: D105
        return hash(self.instance_id)

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.instance_id == other.instance_id

    def __lt__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.instance_id < other.instance_id

    def __repr__(self) -> str:  # noqa: D105
        res: str = f"Type: {type(self)} | ID: {id(self)}\n"
        res += f"Name: {self.instance_name}\nInstance ID: {self.instance_id}\n"
        res += f"Application State: {self.app_state.name}\nInstance Running: {self.running}\nModule: {self.module}\nPort: {self.port}\n"
        return res

    @staticmethod
    def has_controller(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """Checks the class :attr:`._controller` is not equal to None.

        Parameters
        ----------
        func : Callable[Concatenate[D, T], Coroutine[None, None, F]]
            The function the decorator is wrapping.

        Raises
        ------
        :exc:`RuntimeError`
            The API call is only allowed to be run on a type(:class:`Controller`).

        Returns
        -------
        :class:`Callable`[class:`Concatenate`[D, T], :class:`Coroutine`[None, None, F]]
            The function the decorator is wrapping.

        """

        @functools.wraps(wrapped=func)
        def wrapper_has_controller(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            if self._controller is not None:
                return func(self, *args, **kwargs)
            raise RuntimeError(self._no_controller)

        return wrapper_has_controller

    @staticmethod
    def online(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """Checks the :attr:`running` property and raises :exc:`ConnectionError` if the attribute is equal to "False".

        Raises
        ------
        :exc:`ConnectionError`
            The requested Instance is not currently running at this time.

        """

        @functools.wraps(wrapped=func)
        def wrapper_online(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            if self.running is True:
                return func(self, *args, **kwargs)
            raise ConnectionError(self._instance_offline)

        return wrapper_online

    def _parse_instance_data(self, data: InstanceResponse) -> None:
        for key in self.__slots__:
            value = data.get(key)
            if value is None:
                continue
            setattr(self, key, value)

        # This is only used for older versions of AMP v ``>2.6.0.0``  and earlier.
        # Per Mike and Developers of AMP state they will be using string versions from `2.6.0.0` and this handles that.
        if isinstance(data["amp_version"], dict):
            try:
                # reveal_type(data["amp_version"])
                self.amp_version = BuildInfo(**data["amp_version"])
            except (RuntimeError, TypeError, ValueError) as e:
                LOGGER.warning("We attempted to unpack <self.amp_version> and failed %s", e)
                self.amp_version = data["amp_version"]
        if isinstance(data["amp_version"], str):
            self.amp_version = BuildInfo.to_dataclass(data["amp_version"])

        self._app_state = data["app_state"]
        # Base defaults this to "0" (the Controller), our session and endpoint URL need the real Instance ID.
        self._instance_id = data["instance_id"]

    @online
    async def get_application_status(self, format_data: Union[bool, None] = None) -> Status | StatusResponse:
        """|coro|

        Similar to :meth:`Core.get_status` but with the added benefit of updating our ``self`` object reference.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Raises
        ------
        :exc:`ConnectionError`:
            The requested Instance is not available at this time if the Instance is not running.

        Returns
        -------
        :class:`Status | StatusResponse`
            :class:`Status` if `format_data = True` else :class:`StatusResponse`.

        """
        result: Status | StatusResponse = await super().get_status(format_data=format_data)
        if isinstance(result, Status):
            self.parse_data(data=result)
        return result

    @has_controller
    async def get_instance_status(self) -> Union[Instance, MinecraftInstance]:
        """|coro|

        Requests the recent changes to the Instance, updates our ``self`` object and returns the updated object.

        .. note::
            Typical usage is to get current information pertaining to an Instance and keeping it updated.


        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`Controller` generated and set to :attr:`_controller` first. See ``__init__()``

        .. warning::
            This will fail if you attempt to call it on the Target or Controller type Instance.



        Raises
        ------
        :exc:`RuntimeError`:
            If the :attr:`_controller` attribute has not been set.

        Returns
        -------
        Union[:class:`Instance`, :class:`MinecraftInstance`]
            Returns an updated ``self`` object.

        """
        # We want the raw dict here, so we can update ourselves instead of building a new Instance.
        assert self._controller is not None  # noqa: S101
        result: InstanceResponse = await self._controller.get_instance(
            instance_id=self._instance_id,
            format_data=False,
        )
        self._parse_instance_data(data=result)
        return self

    @online
    async def get_updates(self, format_data: Union[bool, None] = None) -> Updates | UpdatesResponse:
        """|coro|

        Requests the recent Console entries of the Instance, will acquire all updates from previous API call of :meth:`get_updates`
        and updates parses the information setting it to ``self``. See :class:`Updates` for attribute access.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        Parameters
        ----------
        format_data : Union[:class:`bool`, :class:`None`], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if :class:`None`), by default :class:`None`

        Raises
        ------
        :exc:`ConnectionError`
            If the :attr:`running` is False.
        :exc:`RuntimeError`
            If the :attr:`_controller` attribute has not been set.

        Returns
        -------
        :class:`Updates | UpdatesResponse`
            :class:`Updates` if `format_data = True` else :class:`UpdatesResponse`.

        """
        result: Updates | UpdatesResponse = await super().get_updates(format_data=format_data)
        if isinstance(result, Updates):
            self.parse_data(data=result)
        return result

    async def _routed_ads(self, route_by_target: Union[bool, None] = None) -> ADSModule:
        """|coro|

        Pick the ADS that start, stop and restart should be sent to for this Instance.

        AMP looks the Instance name up on whichever ADS receives the call, so a Target's Instance has to be
        called through its own :class:`TargetADS`. Instance names repeat across Targets (every ADS is ``ADS01``),
        so the :class:`Controller` would find the wrong Instance or none at all.

        Parameters
        ----------
        route_by_target : Union[:class:`bool`, None], optional
            Send the call to the Target that holds this Instance. (Uses :attr:`route_by_target` if None), by default None.

        Returns
        -------
        :class:`ADSModule`
            The :class:`Controller` or the :class:`TargetADS` holding this Instance.

        """
        assert self._controller is not None  # noqa: S101
        if route_by_target is None:
            route_by_target = self.route_by_target
        if route_by_target is False:
            return self._controller

        own_ads_id = await self._controller._learn_ads_instance_id()  # pyright: ignore[reportPrivateUsage]
        # A missing target_id or our own ADS ID means the Controller holds this Instance.
        if self.target_id is None or self.target_id == own_ads_id:
            return self._controller

        for known_instance in self._controller.instances:
            if isinstance(known_instance, TargetADS) and known_instance.instance_id == self.target_id:
                return known_instance

        target_ads = await self._controller.get_instance(instance_id=self.target_id)
        if isinstance(target_ads, TargetADS):
            return target_ads
        return self._controller

    @has_controller
    async def start_instance(
        self,
        format_data: Union[bool, None] = None,
        *,
        route_by_target: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Start the Instance.

        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`Controller` generated and set to :attr:`_controller` first. See ``__init__()``



        .. note::
            By default the call goes to the Target that holds this Instance (see :attr:`route_by_target`),
            as AMP looks the Instance name up on the ADS that receives the call.

        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.
        route_by_target : Union[:class:`bool`, None], optional
            Send the call to the Target that holds this Instance instead of the :class:`Controller`.
            AMP looks the Instance name up on the ADS that receives the call, and names repeat across Targets.
            (Uses :attr:`route_by_target` if None), by default None.

        Raises
        ------
        :exc:`RuntimeError`
            If the :attr:`_controller` attribute has not been set.


        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        # This function is to mimic the `ADSModule.start_instance()` which we use the self._controller attribute to access.
        ads_module = await self._routed_ads(route_by_target=route_by_target)
        return await ads_module.start_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @online
    @has_controller
    async def stop_instance(
        self,
        format_data: Union[bool, None] = None,
        *,
        route_by_target: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Stops the Instance.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`Controller` generated and set to :attr:`_controller` first. See ``__init__()``


        .. note::
            By default the call goes to the Target that holds this Instance (see :attr:`route_by_target`),
            as AMP looks the Instance name up on the ADS that receives the call.

        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.
        route_by_target : Union[:class:`bool`, None], optional
            Send the call to the Target that holds this Instance instead of the :class:`Controller`.
            AMP looks the Instance name up on the ADS that receives the call, and names repeat across Targets.
            (Uses :attr:`route_by_target` if None), by default None.

        Raises
        ------
        :exc:`ConnectionError`
            If the :attr:`running` is False.
        :exc:`RuntimeError`
            If the :attr:`_controller` attribute has not been set.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        # This function is to mimic the `ADSModule.stop_instance()` which we use the self._controller attribute to access.
        ads_module = await self._routed_ads(route_by_target=route_by_target)
        return await ads_module.stop_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @online
    @has_controller
    async def restart_instance(
        self,
        format_data: Union[bool, None] = None,
        *,
        route_by_target: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Restart the Instance.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`

        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`Controller` generated and set to :attr:`_controller` first. See ``__init__()``


        .. note::
            By default the call goes to the Target that holds this Instance (see :attr:`route_by_target`),
            as AMP looks the Instance name up on the ADS that receives the call.

        Parameters
        ----------
        format_data : Union[bool, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.
        route_by_target : Union[:class:`bool`, None], optional
            Send the call to the Target that holds this Instance instead of the :class:`Controller`.
            AMP looks the Instance name up on the ADS that receives the call, and names repeat across Targets.
            (Uses :attr:`route_by_target` if None), by default None.

        Raises
        ------
        :exc:`ConnectionError`:
            The requested Instance is not available at this time if the Instance is offline.
        :exc:`RuntimeError`:
            If the :attr:`_controller` attribute has not been set.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        # This function is to mimic the `ADSModule.restart_instance()` which we use the self._controller attribute to access.
        ads_module = await self._routed_ads(route_by_target=route_by_target)
        return await ads_module.restart_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @has_controller
    async def update_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|
        Update the AMP Instance.

        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`Controller` generated and set to :attr:`_controller` first. See ``__init__()``


        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        # This function is to mimic the `ADSModule.update_instance()` which we use the self._controller attribute to access.
        return await self._controller.upgrade_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.


class MinecraftInstance(MinecraftModule, Instance):
    """Represents a Minecraft Instance from AMP containing all relevant API Endpoints specific to Minecraft Instances.

    Attributes
    ----------
    amp_version : Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    application_endpoints : list[dict[str, str]]
        The list of application endpoints for the Instance.
    app_state : :class:`InstanceState`
        The state of the application.
    container_cpus : :class:`float`
        The amount of CPU cores allocated to the container, default is 0.0.
    container_memory_mb : :class:`int`
        The amount of memory allocated to the container in MB.
    container_memory_policy : :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance.
    daemon : :class:`bool`
        If the Instance is a daemon.
    daemon_autostart : :class:`bool`
        If the Instance should be autostart on boot.
    deployment_args : dict[:class:`str`, :class:`str`]
        The deployment arguments of the Instance.
    description : :class:`str`
        The description of the Instance, default is "".
    disk_usage_mb : :class:`int`
        The disk usage of the Instance in MB.
    display_image_source : :class:`str`
        The source of the display image, default is "".
    exclude_from_firewall : :class:`bool`
        If the Instance should be excluded from the firewall.
    friendly_name : :class:`str`
        The friendly name of the Instance.
    ip : :class:`str`
        The IP address of the Instance.
    instance_id : :class:`str`
        The Instance GUID.
    instance_name : :class:`str`
        The Instance name.
    is_container_instance : :class:`bool`
        If the Instance is a container Instance.
    is_https : :class:`bool`
        If the Instance is using HTTPS.
    management_mode : :class:`int`
        The management mode of the Instance.
    metrics : Union[dict[:class:`str`, :class:`MetricsKeyResponse`], None]
        The metrics of the Instance keyed by metric name, default is None.
    module : :class:`str`
        The module of the Instance, default is "Minecraft".
    module_display_name : :class:`str`
        The display name of the module, default is "".
    port : :class:`str`
        The port of the Instance.
    release_stream : :class:`int`
        The release stream of the Instance.
    running : :class:`bool`
        If the Instance is running.
    suspended : :class:`bool`
        If the Instance is suspended.
    tags : Union[:class:`None`, :class:`list`]
        The list of tags of the Instance, default is None.
    target_id : :class:`str`
        The target ID of the Instance.
    url : :class:`str`
        The API URL.

    """

    module: str = "Minecraft"


class TargetADS(ADSModule, Instance):
    """Typically referred to the "Target ADS" which is apart of the available Instances of the :class:`Controller`
    via :attr:`~Controller.instances`.

    .. note::
        A Target ADS serves the ADSModule endpoints, so this class is an :class:`Instance` that also has every
        :class:`ADSModule` method. Those calls go to this Target and act on the Instances it holds.

    .. note::
        :meth:`start_instance`, :meth:`stop_instance`, :meth:`restart_instance` and :meth:`delete_instance_users`
        take the :class:`ADSModule` signature (an `instance_name` or `instance_id`) and act on an Instance of this
        Target. They no longer act on the Target ADS itself like the :class:`Instance` versions did.


    Attributes
    ----------
    amp_version : Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    application_endpoints : list[dict[str, str]]
        The list of application endpoints for the Instance.
    app_state : :class:`InstanceState`
        The state of the application.
    container_cpus : :class:`float`
        The amount of CPU cores allocated to the container, default is 0.0.
    container_memory_mb : :class:`int`
        The amount of memory allocated to the container in MB.
    container_memory_policy : :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance.
    daemon : :class:`bool`
        If the Instance is a daemon.
    daemon_autostart : :class:`bool`
        If the Instance should be autostart on boot.
    deployment_args : dict[:class:`str`, :class:`str`]
        The deployment arguments of the Instance.
    description : :class:`str`
        The description of the Instance, default is "".
    disk_usage_mb : :class:`int`
        The disk usage of the Instance in MB.
    display_image_source : :class:`str`
        The source of the display image, default is "".
    exclude_from_firewall : :class:`bool`
        If the Instance should be excluded from the firewall.
    friendly_name : :class:`str`
        The friendly name of the Instance.
    ip : :class:`str`
        The IP address of the Instance.
    instance_id : :class:`str`
        The Instance GUID.
    instance_name : :class:`str`
        The Instance name.
    is_container_instance : :class:`bool`
        If the Instance is a container Instance.
    is_https : :class:`bool`
        If the Instance is using HTTPS.
    management_mode : :class:`int`
        The management mode of the Instance.
    metrics : Union[dict[:class:`str`, :class:`MetricsKeyResponse`], None]
        The metrics of the Instance keyed by metric name, default is None.
    module : :class:`str`
        The module of the Instance, default is "ADS".
    module_display_name : :class:`str`
        The display name of the module, default is "".
    port : :class:`str`
        The port of the Instance.
    release_stream : :class:`int`
        The release stream of the Instance.
    running : :class:`bool`
        If the Instance is running.
    suspended : :class:`bool`
        If the Instance is suspended.
    tags : Union[:class:`None`, :class:`list`]
        The list of tags of the Instance, default is None.
    target_id : :class:`str`
        The target ID of the Instance.
    url : :class:`str`
        The API URL.

    """

    module: str = "ADS"

    _instances: set[InstanceTypeAliases]

    @property
    def instances(self) -> set[InstanceTypeAliases]:
        """The Instances this Target holds, set by :meth:`get_instances`.

        .. note::
            This Target's own ADS Instance is left out, since that Instance is this object.


        Returns
        -------
        set[Union[:class:`InstanceTypeAliases`]]
            The converted Instances from the last :meth:`get_instances` call, empty until it has run.

        """
        return self._instances

    def __init__(
        self,
        data: InstanceResponse,
        controller: Optional[Controller] = None,
        **kwargs: Any,
    ) -> None:
        """Build a Target ADS, unpacking an API response onto its attributes.

        Parameters
        ----------
        data : :class:`InstanceResponse`
            The Instance data to unpack onto this class.
        controller : Union[:class:`Controller`, None], optional
            The Controller that holds this Target, used to convert the Instances this Target returns, by default None.
        **kwargs : Any
            Keyword arguments forwarded to :meth:`Instance.__init__`.

        """
        super().__init__(data=data, controller=controller, **kwargs)
        self._instances = set()

    @override
    async def start_instance(
        self,
        instance_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Start an Instance of this Target, picked by its name on this Target.

        Parameters
        ----------
        instance_name : :class:`str`
            The name of the Instance on this Target.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        return await ADSModule.start_instance(
            self,
            instance_name=instance_name,
            format_data=format_data,
            request_params=request_params,
            **response_params,
        )

    @override
    async def stop_instance(
        self,
        instance_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Stop an Instance of this Target, picked by its name on this Target.

        Parameters
        ----------
        instance_name : :class:`str`
            The name of the Instance on this Target.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        return await ADSModule.stop_instance(
            self,
            instance_name=instance_name,
            format_data=format_data,
            request_params=request_params,
            **response_params,
        )

    @override
    async def restart_instance(
        self,
        instance_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Restart an Instance of this Target, picked by its name on this Target.

        Parameters
        ----------
        instance_name : :class:`str`
            The name of the Instance on this Target.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        return await ADSModule.restart_instance(
            self,
            instance_name=instance_name,
            format_data=format_data,
            request_params=request_params,
            **response_params,
        )

    @override
    async def delete_instance_users(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete all Users from an Instance of this Target, picked by its ID on this Target.

        Parameters
        ----------
        instance_id : :class:`str`
            The ID of the Instance on this Target.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        return await ADSModule.delete_instance_users(
            self,
            instance_id=instance_id,
            format_data=format_data,
            request_params=request_params,
            **response_params,
        )

    @overload
    async def get_instance(
        self,
        instance_id: str,
        *,
        format_data: Literal[True],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[InstanceTypeAliases, Self]: ...
    @overload
    async def get_instance(
        self,
        instance_id: str,
        *,
        format_data: Literal[False],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> InstanceResponse: ...

    # None falls back to the global `format_data`, which we can't know until runtime.
    @overload
    async def get_instance(
        self,
        instance_id: str,
        *,
        format_data: None = ...,
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[InstanceTypeAliases, InstanceResponse, Self]: ...

    @override
    async def get_instance(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[InstanceTypeAliases, InstanceResponse, Self]:
        """|coro|

        Retrieve a single Instance of this Target by ID and convert the Instance.

        .. note::
            This Target's own ADS ID returns `self`. AMP answers null for an ID that is not on this Target.

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID to retrieve.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Raises
        ------
        :exc:`RuntimeError`
            If the Instance needs converting and the :attr:`_controller` attribute has not been set.

        Returns
        -------
        Union[:class:`Instance`, :class:`MinecraftInstance`, :class:`TargetADS`, :class:`InstanceResponse`]
            On success returns the converted Instance, `self` for this Target's own ADS, or the raw Instance dict
            if `format_data` is False.

        """
        result: InstanceResponse = await ADSModule.get_instance(
            self,
            instance_id=instance_id,
            request_params=request_params,
            **response_params,
        )
        if format_data is None:
            format_data = self.format_data
        if format_data is False:
            return result
        if result["instance_id"] == self.instance_id:
            return self

        # The Controller builds every Instance object, so these match the ones `Controller.get_instances` returns.
        if self._controller is None:
            raise RuntimeError(self._no_controller)
        return self._controller.instance_conversion(instances=result)

    @overload
    async def get_instances(
        self,
        include_self: bool = ...,
        *,
        format_data: Literal[True],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> set[InstanceTypeAliases]: ...

    @overload
    async def get_instances(
        self,
        include_self: bool = ...,
        *,
        format_data: Literal[False],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[ControllerResponse]: ...

    # None falls back to the global `format_data`, which we can't know until runtime.
    @overload
    async def get_instances(
        self,
        include_self: bool = ...,
        *,
        format_data: None = ...,
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[set[InstanceTypeAliases], list[ControllerResponse]]: ...

    @override
    async def get_instances(
        self,
        include_self: bool = True,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[set[InstanceTypeAliases], list[ControllerResponse]]:
        """|coro|

        Returns the Instances this Target holds as a set of converted :class:`Instance`, :class:`MinecraftInstance`
        and :class:`TargetADS` objects, and keeps them on :attr:`instances`.

        .. note::
            This Target's own ADS Instance is `self`, so it is left out of the set. The Target's data from the
            response is not copied onto `self`.

        .. note::
            If `format_data` is False this will return the raw list of Target dicts instead and nothing is stored.

        Parameters
        ----------
        include_self : :class:`bool`, optional
            Force include this Target ADS Instance in the results, by default True.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Raises
        ------
        :exc:`RuntimeError`
            If `format_data` is True and the :attr:`_controller` attribute has not been set.

        Returns
        -------
        Union[set[Union[:class:`Instance`, :class:`MinecraftInstance`, :class:`TargetADS`]], list[:class:`ControllerResponse`]]
            On success returns the set of converted Instances, or the raw list of Target dicts if `format_data` is False.

        """
        result: list[ControllerResponse] = await ADSModule.get_instances(
            self,
            include_self=include_self,
            request_params=request_params,
            **response_params,
        )
        if format_data is None:
            format_data = self.format_data
        if format_data is False:
            return result

        # The Controller builds every Instance object, so these match the ones `Controller.get_instances` returns.
        if self._controller is None:
            raise RuntimeError(self._no_controller)

        converted_instances: set[InstanceTypeAliases] = set()
        for target in result:
            available_instances: list[InstanceResponse] = [
                instance for instance in target["available_instances"] if instance["instance_id"] != self.instance_id
            ]
            converted_instances.update(self._controller.instance_conversion(instances=available_instances))

        self._instances = converted_instances
        return self._instances


class Controller(ADSModule, Core, EmailSenderPlugin, FileManagerPlugin):
    """Represents an AMP Controller Instance.

    .. note::
        :meth:`~Controller.get_instances` copies this Controller's own data onto `self` and leaves its own ADS Instance
        (eg. `ADS01`) out of :attr:`Controller.instances`. The ADS Instances of remote Targets come back as
        :class:`TargetADS`.


    .. note::
        Similar to what you see when you log into AMP web GUI and see the Instances list.
        This attribute is cached and will require calling :meth:`~ADSModule.get_instances` to access the API converted class objects.
        * See the :attr:`Controller.instances` attribute.


    Attributes
    ----------
    id : :class:`int`
        UNK
    disabled : :class:`bool`
        If the Controller is Disabled or not.
    is_remote : :class:`bool`
        If the Controller is remote or not.
    platform : :class:`PlatformInfoResponse`
        Platform information related to the Instance.
    datastores : list[:class:`TargetDatastoreResponse`]
        The Datastores that the Controller has access to.
    creates_in_containers : :class:`bool`
        The Controller will create the Instances in containers.
    can_create : :class:`bool`
        If the Controller can create Instances or not.
    available_instances : list[:class:`InstanceResponse`]
        A list of AMP Instances the Controller/ADS has permissions to see.
    available_ips : list[:class:`str`]
        The list of available IPs the Controller/Instance has.
    tags : list[:class:`str`]
        The tags related to the Controller/Instance.
    url : :class:`str`
        The URL for the Controller/Instance.
    last_updated : Union[:class:`str`, :class:`datetime`]
        The last_updated comes in as  ISO format and :meth:`Controller`__post_init__` converts it into a datetime object.
    instance_id : :class:`str`
        The Controller/Instance ID tied to the Instance, default is "0".
    state : :py:class:`InstanceState`
        The state the Controller/Instance is in. See enum :py:class:`InstanceState`, default is ``InstanceState.UNDEFINED``.
    fitness : Union[dict[:class:`str`, Any], None]
        UNK.
    friendly_name : :class:`str`
        The Controller/Instance friendly name.
    state_reason : Union[:class:`str`, None]
        UNK.
    description : :class:`str`
        Controller/Instance description.
    tags_list : Union[:class:`str`, None]
        The tags related to the Controller/Instance if any.

    """

    # These stay unset until `get_instances()` populates them, see __getattribute__ below.
    id: int
    disabled: bool
    is_remote: bool
    platform: PlatformInfoResponse
    datastores: list[TargetDatastoreResponse]
    creates_in_containers: bool
    can_create: bool
    available_instances: list[InstanceResponse]
    available_ips: list[str]
    tags: list[str]
    url: str
    last_updated: datetime.datetime | str
    # instance_id: str = "0"
    state: InstanceState
    fitness: Union[dict[str, Any], None]
    friendly_name: str
    state_reason: Union[str, None]
    description: str
    tags_list: Union[str, None]

    _instances: set[InstanceTypeAliases]
    # The Controller's own ADS ID. `instance_id` is the session key, so AMP's real ID lives here until known.
    _ads_instance_id: Union[str, None]

    __cached__ = (
        "available_instances",
        "available_ips",
        "can_create",
        "creates_in_containers",
        "datastores",
        "description",
        "disabled",
        "fitness",
        "friendly_name",
        "id",
        "is_remote",
        "last_updated",
        "platform",
        "state",
        "state_reason",
        "tags",
        "tags_list",
        "url",
    )

    # O(1) membership for the __getattribute__ guard, which runs on every attribute access.
    _cached_names: ClassVar[frozenset[str]] = frozenset(__cached__)

    #  What the cache messages tell a user to call. Anything populated by a different endpoint gets an
    # entry in `_cache_sources`; everything else falls back to `_cache_source`.
    _cache_source: ClassVar[str] = "get_instances()"
    _cache_sources: ClassVar[dict[str, str]] = {}

    # __slots__ = ()

    @property
    def instances(self) -> set[InstanceTypeAliases]:
        """Represents all Instances the :class:`Controller` can see,
        these are transferred from :attr:`~Controller.available_instance`.\n

        .. note::
            Similar to :attr:`~Controller.available_instance` but converted into a type of :class:`Instance` classes that
            have API functions.\n
            The set of :class:`Instance` types will be ordered by :attr:`~Instance.instance_id`.


        Returns
        -------
        set[Union[:class:`InstanceTypeAliases`]]
            A set of converted :class:`Instance` classes sorted by :class:`~Instance.instance_id`.

        """
        return self._instances

    def __init__(
        self,
        data: Optional[ControllerResponse] = None,
        *,
        bridge: Optional[Bridge] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        """Build a Controller, optionally unpacking an API response onto its attributes.

        Parameters
        ----------
        data : Union[:class:`ControllerResponse`, None], optional
            The target data to unpack onto this class, by default None.
        bridge : Union[:class:`Bridge`, None], optional
            The Bridge to connect through, uses the Singleton <Bridge> if None, by default None.
        session : Union[:class:`aiohttp.ClientSession`, None], optional
            A static Session to use, otherwise the class will generate its own as needed, by default None.

        """
        super().__init__(bridge=bridge, session=session)
        self._module = "ADS"
        self._instances = set()
        self._ads_instance_id = None

        if data is not None:
            self._parse_controller_data(data=data)

    def __hash__(self) -> int:
        """Hash the Controller by its Instance ID."""
        return hash(self.instance_id)

    def __eq__(self, other: object) -> bool:
        """Compare two Controllers by their Instance ID."""
        return isinstance(other, self.__class__) and self.instance_id == other.instance_id

    def __repr__(self) -> str:
        """Pretty print the Controller, omitting any private attributes."""
        new_vars: dict[str, Any] = {}
        for key, value in vars(self).items():
            # We do this to avoid any private attributes such as the _controller attribute or _logger.
            if key.startswith("_"):
                continue
            new_vars[key] = value
        return pformat(new_vars)

    def __getattribute__(self, name: str) -> Any:
        """Guard the cached attributes, raising when unpopulated and warning when stale.

        .. note::
            This has to be ``__getattribute__`` rather than ``__getattr__``, so the stale warning also fires on
            populated attributes.

        """
        # Cheap frozenset test first so uncached names and every method call fall straight through.
        # `_is_cached` only flips in `_parse_controller_data`, so it alone says if our own data was applied.
        if name in Controller._cached_names:
            cls: type[Controller] = type(self)
            if not object.__getattribute__(self, "_is_cached"):
                raise AttributeError(Base._no_cache % (cls.__name__, name, cls.__name__, cls._cache_hint(name)))

            # Inlined staleness check; monotonic subtraction keeps this off the datetime path.
            stamped: Optional[float] = object.__getattribute__(self, "_cached_monotonic")
            timeout: int = object.__getattribute__(self, "_cache_timeout")
            if stamped is not None:
                age: float = time.monotonic() - stamped
                if age > timeout:
                    LOGGER.warning(
                        Base._stale_cache,
                        cls.__name__,
                        name,
                        int(age),
                        timeout,
                        cls.__name__,
                        cls._cache_hint(name),
                    )
        return object.__getattribute__(self, name)

    async def __adel__(self) -> None:
        """Close any open connection when the Controller is discarded."""
        await self.clean_up()

    @overload
    def instance_conversion(self, instances: InstanceResponse) -> InstanceTypeAliases: ...
    @overload
    def instance_conversion(self, instances: list[InstanceResponse]) -> set[InstanceTypeAliases]: ...

    def instance_conversion(
        self,
        instances: Union[list[InstanceResponse], InstanceResponse],
    ) -> Union[set[InstanceTypeAliases], InstanceTypeAliases]:
        """Takes the raw Instance data and turns it into :class:`Instance`, :class:`MinecraftInstance` and or
        :class:`TargetADS` respectively to facilitate API function accessibility.

        Parameters
        ----------
        instances : Union[list[:class:`InstanceResponse`], :class:`InstanceResponse`]
            A list of raw Instance dicts or a single one.

        Returns
        -------
        Union[set[Union[:class:`InstanceTypeAliases`]], Union[:class:`InstanceTypeAliases`]]
            The set of converted Instance objects or a single converted object.

        """
        # We essentially call ourselves in a loop via a list check.
        if isinstance(instances, list):
            conv_instances: set[InstanceTypeAliases] = set()
            for instance in instances:
                conv_instances.add(self.instance_conversion(instances=instance))
            return conv_instances

        # An ADS Instance here is a remote Target's. Our own is left out by get_instances, and get_instance returns
        # self for it once our ADS ID is known. We hand them ourselves so they can still reach ADSModule endpoints.
        if instances["module"] == "ADS":
            return TargetADS(data=instances, controller=self, bridge=self._bridge, session=self.session)

        if instances["module"] == "Minecraft":
            return MinecraftInstance(data=instances, controller=self, bridge=self._bridge, session=self.session)

        return Instance(data=instances, controller=self, bridge=self._bridge, session=self.session)

    @overload
    async def get_instance(
        self,
        instance_id: str,
        *,
        format_data: Literal[True],
        auto_detect: bool = ...,
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[InstanceTypeAliases, Self]: ...
    @overload
    async def get_instance(
        self,
        instance_id: str,
        *,
        format_data: Literal[False],
        auto_detect: bool = ...,
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> InstanceResponse: ...

    # None falls back to the global `format_data`, which we can't know until runtime.
    @overload
    async def get_instance(
        self,
        instance_id: str,
        *,
        format_data: None = ...,
        auto_detect: bool = ...,
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[InstanceTypeAliases, InstanceResponse, Self]: ...

    async def get_instance(
        self,
        instance_id: str,
        *,
        format_data: Union[bool, None] = None,
        auto_detect: bool = False,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[InstanceTypeAliases, InstanceResponse, Self]:
        """|coro|

        Retrieve a single Instance by ID and convert the Instance.

        .. note::
            This Controller's own ADS Instance comes back as `self`. The Controller only knows its own ADS ID once
            :meth:`get_instances` has run, or when `auto_detect` is True.

        .. note::
            With the ID unknown and `auto_detect` False, an ADS Instance logs a warning and comes back as a
            :class:`TargetADS`. Other Instances never need the ID, and `format_data=False` never looks it up.

        Parameters
        ----------
        instance_id : :class:`str`
            The Instance ID to retrieve.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        auto_detect : :class:`bool`, optional
            Look up this Controller's own ADS ID with one extra API call when it is unknown and the Instance is an
            ADS, by default False.
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Union[:class:`Instance`, :class:`MinecraftInstance`, :class:`TargetADS`, :class:`Controller`, :class:`InstanceResponse`]
            On success returns the converted Instance, `self` for this Controller's own ADS, or the raw Instance dict
            if `format_data` is False.

        """
        result: InstanceResponse = await super().get_instance(
            instance_id=instance_id,
            request_params=request_params,
            **response_params,
        )
        if format_data is None:
            format_data = self.format_data
        if format_data is False:
            return result

        # Only an ADS Instance can be us, so every other module skips the ID question.
        if result["module"] == "ADS":
            if auto_detect:
                await self._learn_ads_instance_id(request_params=request_params, **response_params)

            if self._ads_instance_id is None:
                LOGGER.warning(
                    "<%s.%s> | Cannot tell if the ADS Instance %s is this Controller, as its own ADS ID is unknown. "
                    "Call `get_instances()` first or pass `auto_detect=True`. | Returning a TargetADS",
                    __class__.__name__,
                    "get_instance",
                    result["instance_id"],
                )
            elif result["instance_id"] == self._ads_instance_id:
                return self
        return self.instance_conversion(instances=result)

    async def _learn_ads_instance_id(
        self,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[str, None]:
        """|coro|

        Learn this Controller's own ADS ID with one :meth:`get_module_info` call, only when it is not known yet.

        Parameters
        ----------
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Union[:class:`str`, None]
            The ADS ID stored on :attr:`_ads_instance_id`, or None if it could not be learned.

        """
        if self._ads_instance_id is None:
            module_info = await self.get_module_info(
                format_data=False,
                request_params=request_params,
                **response_params,
            )
            if isinstance(module_info, dict):
                self._ads_instance_id = module_info["instance_id"]
        return self._ads_instance_id

    def _parse_controller_data(self, data: ControllerResponse) -> None:
        # Every cached name gets set, even when AMP sends null, so a populated attribute never raises.
        for key in self.__cached__:
            setattr(self, key, data.get(key))

        # AMP sends last_updated as an ISO string, so we convert it here.
        self.last_updated = self.timestamp_converter(timestamp=data["last_updated"])
        try:
            self.state = InstanceState(data["state"])
        except ValueError:
            self.state = InstanceState.undefined
        self._mark_cached()

    @overload
    async def get_instances(
        self,
        include_self: bool = ...,
        *,
        format_data: Literal[True],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> set[InstanceTypeAliases]: ...

    @overload
    async def get_instances(
        self,
        include_self: bool = ...,
        *,
        format_data: Literal[False],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[ControllerResponse]: ...

    # None falls back to the global `format_data`, which we can't know until runtime.
    @overload
    async def get_instances(
        self,
        include_self: bool = ...,
        *,
        format_data: None = ...,
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[set[InstanceTypeAliases], list[ControllerResponse]]: ...

    async def get_instances(
        self,
        include_self: bool = True,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[set[InstanceTypeAliases], list[ControllerResponse]]:
        """|coro|

        Returns a set of converted :class:`Instance`, :class:`MinecraftInstance` and :class:`TargetADS` objects
        and updates our ``self`` object with the Controller's data.

        .. note::
            The Controller's own ADS Instance (eg. `ADS01`) is `self`, so it is left out of the set.
            The local Target's `instance_id` is also kept as the Controller's own ADS ID, for :meth:`get_instance`.

        .. note::
            On a Controller, `include_self=False` makes AMP drop the local Target, so `self` is not updated. Its
            cached attributes raise until a call with `include_self=True`.

        .. note::
            If ``format_data`` is False this will return the raw list of Target dicts instead and nothing is updated.


        .. warning::
            This will be only Instances the AMP Controller and AMP User has permission to access.


        Parameters
        ----------
        include_self : :class:`bool`, optional
            Force include the Controller or Target ADS Instance in the results, by default True.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : Union[:class:`AioHTTPRequestOptions`, None], optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        Union[set[Union[:class:`Instance`, :class:`MinecraftInstance`, :class:`TargetADS`]], list[:class:`ControllerResponse`]]
            On success returns the set of converted Instances, or the raw list of Target dicts if ``format_data`` is False.

        """
        # result: list[Union[Controller, Instance]] = await super().get_instances(
        #     include_self=include_self,
        #     format_data=format_data,
        # )
        # # if isinstance(result ):
        # # return result

        # if isinstance(result[0], Controller):
        #     LOGGER.debug(
        #         "Updating %s, with Controller dataclass: %s |\nObject:\n%s",
        #         __class__.__name__,
        #         id(result[0]),
        #         result[0],
        #     )
        #     # We make the first Controller dataclass our AMPControllerInstance and transfer all the information from
        #     # the Controller to Self.
        #     _url = self._endpoint_url
        #     self.parse_data(data=result[0])
        #     self._controller_exists = True
        #     self._endpoint_url = _url
        #     # Since we populated all the attributes from result[0] onto ourselves;
        #     # we can convert Controller.available_instances dynamically by
        #     # setting it to our self.instances attribute using the @setter for instances attribute.
        #     self.instances = self.available_instances
        #     # Then we remove the Controller from the list as we converted that object and don't want to re-add those instances again.
        #     result.pop(0)
        #     # Now we are going to go through and find any other Controllers and place all those Instances under our self object.
        #     for i in result:
        #         # If we have another Controller, we want to get it's available_instances and convert them into proper objects to be used.
        #         if isinstance(i, Controller):
        #             LOGGER.debug("Found an additional Controller dataclass: %s | %s", id(i), i)
        #             # after the conversion we are updating our instance attribute; we cannot overwrite the attribute as we
        #             # just updated the attribute above.
        #             res: set[InstanceTypeAliases] = self.instance_conversion(instances=i.available_instances)
        #             if isinstance(res, InstanceTypeAliases):
        #                 self.instances.add(res)
        #             elif isinstance(res, set):
        #                 self.instances.update(res)

        #     return self.instances

        # return result
        result: list[ControllerResponse] = await super().get_instances(
            include_self=include_self,
            request_params=request_params,
            **response_params,
        )
        # The local Target's ID is our own ADS ID. Stored before the raw return so that path learns it too.
        for target in result:
            if target["is_remote"] is False:
                self._ads_instance_id = target["instance_id"]

        if format_data is None:
            format_data = self.format_data
        if format_data is False:
            return result

        # AMP sends one Target per ADS. The local one is us, so its data lands on our self object,
        # and every Target's Instances get converted and placed under us.
        conv_instances: set[InstanceTypeAliases] = set()
        for target in result:
            available_instances: list[InstanceResponse] = target["available_instances"]
            if target["is_remote"] is False:
                self._parse_controller_data(data=target)
                # Each Target lists its own ADS Instance, the one whose instance_id matches the Target's. In the local
                # Target that Instance is us, so it stays out of `instances`. A remote Target's own one is a TargetADS.
                available_instances = [instance for instance in available_instances if instance["instance_id"] != target["instance_id"]]
            LOGGER.debug(
                "<%s.%s> | Target: %s | Remote: %s | Instances: %s",
                __class__.__name__,
                "get_instances",
                target["friendly_name"],
                target["is_remote"],
                len(available_instances),
            )
            conv_instances.update(self.instance_conversion(instances=available_instances))

        self._instances = conv_instances
        return self._instances
