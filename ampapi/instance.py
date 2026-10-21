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

import asyncio
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
from .generic import GenericModule
from .minecraft import MinecraftModule
from .modules import ActionResult, BuildInfo, Endpoints, InstanceState, Metrics, PlatformInfo, Status, TargetDatastore, Updates, build
from .steamcmd import SteamCMDPlugin

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable, Coroutine
    from typing import Concatenate, Unpack

    import aiohttp
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]
    from typing_extensions import ParamSpec, TypeVar

    from ._types import ActionResultResponse, ControllerResponse, InstanceResponse, StatusResponse, UpdatesResponse
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
    GenericModule,
    SteamCMDPlugin,
    Updates,
):
    """:class:`Instance` represents an entire Instance from AMP that is not Controller, Target/ADS or Minecraft.\n
    This is similar to what you get when selecting 'Manage' an Instance from the Web GUI.

    .. note::
        Generic Instances (module `GenericModule` for a game template, `Generic` for a Custom Application) also serve
        the :class:`GenericModule` and :class:`SteamCMDPlugin` endpoints. Those methods are here for every Instance,
        and raise :exc:`RuntimeError` on any other module (see :meth:`Base.generic_only`).

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
    application_endpoints : list[:class:`Endpoints`]
        The list of application endpoints for the Instance.
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
    metrics : Union[:class:`Metrics`, None]
        The metrics of the Instance, None when AMP sends none (eg. a stopped Instance), default is None.
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
    url : Union[:class:`str`, None]
        The URL of the Instance. AMP doesn't send one, by default None.

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

    amp_version: dict[str, int] | str | BuildInfo | None
    application_endpoints: list[Endpoints]
    metrics: Union[Metrics, None]
    _app_state: InstanceState | int
    # AMP doesn't send a URL for an Instance, a TargetADS gets its Target's.
    url: Union[str, None] = None
    _controller: Union[Controller, None]
    # What a field holds when AMP sends null for it, as documented above. Every other field falls back to None.
    _null_defaults: ClassVar[dict[str, str]] = {"description": "", "display_image_source": "", "module_display_name": ""}
    _ads: Union[Controller, TargetADS, None] = None

    @property
    def ads(self) -> Union[Controller, TargetADS, None]:
        """The ADS that holds this Instance, the :class:`Controller` or the :class:`TargetADS` of a remote Target.

        .. note::
            :meth:`start_instance`, :meth:`stop_instance`, :meth:`restart_instance`, :meth:`update_instance` and
            :meth:`get_instance_status` go through this ADS. An Instance built without one falls back to its
            :class:`Controller`.


        Returns
        -------
        Union[:class:`Controller`, :class:`TargetADS`, None]
            The ADS holding this Instance, or None if neither it nor a :class:`Controller` was set.

        """
        if self._ads is not None:
            return self._ads
        return self._controller

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
        ads: Optional[Union[Controller, TargetADS]] = None,
        **kwargs: Any,
    ) -> None:
        """Build an Instance, unpacking an API response onto its attributes.

        Parameters
        ----------
        data : :class:`InstanceResponse`
            The Instance data to unpack onto this class.
        controller : :class:`Controller` | None, optional
            The Controller used to make ADSModule specific API calls, by default None.
        ads : Union[:class:`Controller`, :class:`TargetADS`, None], optional
            The ADS that holds this Instance, None means the Controller, by default None.
        **kwargs : Any
            Keyword arguments forwarded to :meth:`Base.__init__`.

        """
        # LOGGER.debug("DEBUG %s __init__ %s", type(self).__name__, id(self))
        super().__init__(**kwargs)
        self._parse_instance_data(data=data)

        # We use the Controller class to call ADSModule specific Endpoints as a
        # typical Instance will not have the :py:class:`ADSModule` API Endpoints.
        self._controller = controller
        self._ads = ads
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
        # Every field gets set, even when AMP sends null.
        for key in self.__slots__:
            value = data.get(key)
            # if value is None:
            #     continue
            if value is None:
                value = self._null_defaults.get(key)
            setattr(self, key, value)

        # AMP sends an empty object for the metrics of an Instance that is stopped.
        metrics = data.get("metrics")
        self.metrics = build(Metrics, metrics) if metrics else None
        self.application_endpoints = [build(Endpoints, entry) for entry in data.get("application_endpoints") or []]

        # This is only used for older versions of AMP v ``>2.6.0.0``  and earlier.
        # Per Mike and Developers of AMP state they will be using string versions from `2.6.0.0` and this handles that.
        if isinstance(data["amp_version"], dict):
            try:
                # reveal_type(data["amp_version"])
                self.amp_version = build(BuildInfo, data["amp_version"])
            except (RuntimeError, TypeError, ValueError) as e:
                LOGGER.warning("We attempted to unpack <self.amp_version> and failed %s", e)
                self.amp_version = data["amp_version"]
        if isinstance(data["amp_version"], str):
            self.amp_version = BuildInfo.to_dataclass(data["amp_version"])

        self._app_state = data["app_state"]
        # Base defaults this to "0" (the Controller), our session and endpoint URL need the real Instance ID.
        self._instance_id = data["instance_id"]

    @online
    async def get_application_status(
        self,
        format_data: Union[bool, None] = None,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Status | StatusResponse:
        """|coro|

        Similar to :meth:`Core.get_status` but with the added benefit of updating our ``self`` object reference.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Raises
        ------
        :exc:`ConnectionError`:
            The requested Instance is not available at this time if the Instance is not running.

        Returns
        -------
        :class:`Status | StatusResponse`
            :class:`Status` if `format_data = True` else :class:`StatusResponse`.

        """
        result: Status | StatusResponse = await super().get_status(
            format_data=format_data,
            request_params=request_params,
            **response_params,
        )
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

        .. note::
            The call goes to :attr:`ads`, the ADS that holds this Instance.


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
        assert self.ads is not None  # noqa: S101
        result: InstanceResponse = await self.ads.get_instance(
            instance_id=self._instance_id,
            format_data=False,
        )
        self._parse_instance_data(data=result)
        return self

    @online
    async def get_updates(
        self,
        format_data: Union[bool, None] = None,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Updates | UpdatesResponse:
        """|coro|

        Requests the recent Console entries of the Instance, will acquire all updates from previous API call of :meth:`get_updates`
        and updates parses the information setting it to ``self``. See :class:`Updates` for attribute access.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        Parameters
        ----------
        format_data : Union[:class:`bool`, :class:`None`], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if :class:`None`), by default :class:`None`
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

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
        result: Updates | UpdatesResponse = await super().get_updates(
            format_data=format_data,
            request_params=request_params,
            **response_params,
        )
        if isinstance(result, Updates):
            self.parse_data(data=result)
        return result

    @has_controller
    async def start_instance(
        self,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Start the Instance.

        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`Controller` generated and set to :attr:`_controller` first. See ``__init__()``



        .. note::
            The call goes to :attr:`ads`, the ADS that holds this Instance.

        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Raises
        ------
        :exc:`RuntimeError`
            If the :attr:`_controller` attribute has not been set.


        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        # This function is to mimic the `ADSModule.start_instance()` which we call on the ADS holding this Instance.
        assert self.ads is not None  # noqa: S101
        return await self.ads.start_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @online
    @has_controller
    async def stop_instance(
        self,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Stops the Instance.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`Controller` generated and set to :attr:`_controller` first. See ``__init__()``


        .. note::
            The call goes to :attr:`ads`, the ADS that holds this Instance.

        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

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
        # This function is to mimic the `ADSModule.stop_instance()` which we call on the ADS holding this Instance.
        assert self.ads is not None  # noqa: S101
        return await self.ads.stop_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @online
    @has_controller
    async def restart_instance(
        self,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Restart the Instance.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`

        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`Controller` generated and set to :attr:`_controller` first. See ``__init__()``


        .. note::
            The call goes to :attr:`ads`, the ADS that holds this Instance.

        Parameters
        ----------
        format_data : Union[bool, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

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
        # This function is to mimic the `ADSModule.restart_instance()` which we call on the ADS holding this Instance.
        assert self.ads is not None  # noqa: S101
        return await self.ads.restart_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @has_controller
    async def update_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|
        Update the AMP Instance.

        .. note::
            The call goes to :attr:`ads`, the ADS that holds this Instance.

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
        # This function is to mimic the `ADSModule.update_instance()` which we call on the ADS holding this Instance.
        assert self.ads is not None  # noqa: S101
        return await self.ads.upgrade_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.


class MinecraftInstance(MinecraftModule, Instance):
    """Represents a Minecraft Instance from AMP containing all relevant API Endpoints specific to Minecraft Instances.

    Attributes
    ----------
    amp_version : Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    application_endpoints : list[:class:`Endpoints`]
        The list of application endpoints for the Instance.
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
    metrics : Union[:class:`Metrics`, None]
        The metrics of the Instance, None when AMP sends none (eg. a stopped Instance), default is None.
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
    url : Union[:class:`str`, None]
        The URL of the Instance. AMP doesn't send one, by default None.

    """

    module: str = "Minecraft"


class ADSData(Base):
    """The Target data of an ADS, kept flat on the object. Shared by :class:`Controller` and :class:`TargetADS`.

    .. note::
        Each subclass sets `__cached__` to the Target fields it holds. Reading one before :meth:`_parse_target_data`
        has run raises :exc:`AttributeError`, and reading one after the cache timeout logs a warning.
        A :class:`TargetADS` leaves out `friendly_name`, `description` and `tags`, which keep the Instance's values.

    """

    # These stay unset until `get_instances()` populates them, see __getattribute__ below.
    id: int
    disabled: bool
    is_remote: bool
    platform: PlatformInfo
    datastores: list[TargetDatastore]
    creates_in_containers: bool
    can_create: bool
    available_instances: list[InstanceResponse]
    available_ips: list[str]
    url: Union[str, None]
    last_updated: datetime.datetime | str
    state: InstanceState
    fitness: Union[dict[str, Any], None]
    state_reason: Union[str, None]
    tags_list: Union[str, None]

    __cached__: ClassVar[tuple[str, ...]] = ()

    # O(1) membership for the __getattribute__ guard, which runs on every attribute access.
    _cached_names: ClassVar[frozenset[str]] = frozenset()

    # What the cache messages tell a user to call. Anything populated by a different endpoint gets an
    # entry in `_cache_sources`, everything else falls back to `_cache_source`.
    _cache_source: ClassVar[str] = "get_instances()"
    _cache_sources: ClassVar[dict[str, str]] = {}

    def __getattribute__(self, name: str) -> Any:
        """Guard the cached attributes, raising when unpopulated and warning when stale.

        .. note::
            This has to be `__getattribute__` rather than `__getattr__`, so the stale warning also fires on
            populated attributes.

        """
        # Cheap frozenset test first so uncached names and every method call fall straight through.
        # `_is_cached` only flips in `_parse_target_data`, so it alone says if our own data was applied.
        cls: type[ADSData] = type(self)
        if name in cls._cached_names:
            if not object.__getattribute__(self, "_is_cached"):
                raise AttributeError(Base._no_cache % (cls.__name__, name, cls.__name__, cls._cache_hint(name)))

            # Inlined staleness check. Monotonic subtraction keeps this off the datetime path.
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

    def _parse_target_data(self, data: ControllerResponse) -> None:
        # Only the names this class guards get set. A TargetADS keeps the Instance's own values for the rest.
        # Every one of them is set, even when AMP sends null.
        for key in self.__cached__:
            setattr(self, key, data.get(key))

        # The Target's platform and datastores are held as dataclasses.
        if "platform" in self.__cached__:
            self.platform = build(PlatformInfo, data["platform"])
        if "datastores" in self.__cached__:
            self.datastores = [build(TargetDatastore, entry) for entry in data.get("datastores") or []]

        # AMP sends last_updated as an ISO string, so we convert it here.
        self.last_updated = self.timestamp_converter(timestamp=data["last_updated"])
        try:
            self.state = InstanceState(data["state"])
        except ValueError:
            self.state = InstanceState.undefined
        self._mark_cached()


class TargetADS(ADSData, ADSModule, Instance):
    """Typically referred to the "Target ADS", the ADS Instance of a remote Target held by the :class:`Controller`
    in :attr:`~Controller.targets`.

    .. note::
        The Instances this Target holds belong to it, see :attr:`instances`. Each one has this object as its
        :attr:`~Instance.ads`, so its start, stop, restart and update calls go through this Target.

    .. note::
        A Target ADS serves the ADSModule endpoints, so this class is an :class:`Instance` that also has every
        :class:`ADSModule` method. Those calls go to this Target and act on the Instances it holds.

    .. note::
        :meth:`start_instance`, :meth:`stop_instance`, :meth:`restart_instance` and :meth:`delete_instance_users`
        take the :class:`ADSModule` signature (an `instance_name` or `instance_id`) and act on an Instance of this
        Target, not on the Target ADS itself.

    .. note::
        The Target's own data is kept flat on this object, the same as :class:`Controller`. Reading it before
        :meth:`~Controller.get_instances` has run raises :exc:`AttributeError`. `friendly_name`, `description` and `tags`
        keep the Instance's values.


    Attributes
    ----------
    amp_version : Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    application_endpoints : list[:class:`Endpoints`]
        The list of application endpoints for the Instance.
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
    metrics : Union[:class:`Metrics`, None]
        The metrics of the Instance, None when AMP sends none (eg. a stopped Instance), default is None.
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
    url : Union[:class:`str`, None]
        The URL of the Target.
    id : :class:`int`
        The Target's ID.
    disabled : :class:`bool`
        If the Target is Disabled or not.
    is_remote : :class:`bool`
        If the Target is remote or not.
    platform : :class:`PlatformInfo`
        Platform information related to the Target.
    datastores : list[:class:`TargetDatastore`]
        The Datastores that the Target has access to.
    creates_in_containers : :class:`bool`
        The Target will create the Instances in containers.
    can_create : :class:`bool`
        If the Target can create Instances or not.
    available_instances : list[:class:`InstanceResponse`]
        The raw Instances the Target lists.
    available_ips : list[:class:`str`]
        The list of available IPs the Target has.
    last_updated : Union[:class:`str`, :class:`datetime`]
        When the Target last updated, converted into a datetime object.
    state : :class:`InstanceState`
        The state the Target is in.
    fitness : Union[dict[:class:`str`, Any], None]
        UNK.
    state_reason : Union[:class:`str`, None]
        UNK.
    tags_list : Union[:class:`str`, None]
        The tags related to the Target if any.

    """

    module: str = "ADS"

    _instances: set[InstanceTypeAliases]

    # The Target fields minus `friendly_name`, `description` and `tags`, which stay the Instance's values.
    __cached__ = (
        "available_instances",
        "available_ips",
        "can_create",
        "creates_in_containers",
        "datastores",
        "disabled",
        "fitness",
        "id",
        "is_remote",
        "last_updated",
        "platform",
        "state",
        "state_reason",
        "tags_list",
        "url",
    )
    _cached_names: ClassVar[frozenset[str]] = frozenset(__cached__)

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
        ads: Optional[Union[Controller, TargetADS]] = None,
        **kwargs: Any,
    ) -> None:
        """Build a Target ADS, unpacking an API response onto its attributes.

        Parameters
        ----------
        data : :class:`InstanceResponse`
            The Instance data to unpack onto this class.
        controller : Union[:class:`Controller`, None], optional
            The Controller that holds this Target, used to convert the Instances this Target returns, by default None.
        ads : Union[:class:`Controller`, :class:`TargetADS`, None], optional
            The ADS that holds this Target ADS, None means the Controller, by default None.
        **kwargs : Any
            Keyword arguments forwarded to :meth:`Instance.__init__`.

        """
        super().__init__(data=data, controller=controller, ads=ads, **kwargs)
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

        .. versionchanged:: 5.0.0
            Takes an `instance_name` and started that Instance of this Target. 4.x's `AMPADSInstance.start_instance`
            started the Target ADS itself.

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

        .. versionchanged:: 5.0.0
            Takes an `instance_name` and stopped that Instance of this Target. 4.x's `AMPADSInstance.stop_instance`
            stopped the Target ADS itself.

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

        .. versionchanged:: 5.0.0
            Takes an `instance_name` and restarted that Instance of this Target. 4.x's `AMPADSInstance.restart_instance`
            restarted the Target ADS itself.

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
            This Target's own ADS ID returns `self`, refreshed with the Target's own data. AMP answers null for an ID
            that is not on this Target.

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
            self._parse_instance_data(data=result)
            return self

        # The Controller builds every Instance object, so these match the ones `Controller.get_instances` returns.
        if self._controller is None:
            raise RuntimeError(self._no_controller)
        return self._controller.instance_conversion(instances=result, ads=self)

    @overload
    async def get_instances(
        self,
        *,
        format_data: Literal[True],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> set[InstanceTypeAliases]: ...

    @overload
    async def get_instances(
        self,
        *,
        format_data: Literal[False],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[ControllerResponse]: ...

    # None falls back to the global `format_data`, which we can't know until runtime.
    @overload
    async def get_instances(
        self,
        *,
        format_data: None = ...,
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[set[InstanceTypeAliases], list[ControllerResponse]]: ...

    @override
    async def get_instances(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[set[InstanceTypeAliases], list[ControllerResponse]]:
        """|coro|

        Returns the Instances this Target holds as a set of converted :class:`Instance` and :class:`MinecraftInstance`
        objects, and keeps them on :attr:`instances`.

        .. note::
            This Target's own ADS Instance is `self`, so it is left out of the set. The Target's own data from the
            response is copied onto `self`. The Instances in the set have `self` as their :attr:`~Instance.ads`.

        .. note::
            The set is :attr:`instances`, updated in place by Instance ID. Instances already in it are refreshed and
            keep their identity, new ones are added and the ones this Target no longer lists are dropped.

        .. note::
            If `format_data` is False this will return the raw list of Target dicts instead and nothing is stored.

        Parameters
        ----------
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

        available_instances: list[InstanceResponse] = []
        for target in result:
            # Our own view of the Target is the entry whose ID is ours, and it wins over the Controller's copy.
            if target["instance_id"] == self.instance_id:
                # From the Target itself `url` is localhost, `is_remote` is False and `id` is its own numbering.
                # We keep the Controller's for those three once we have them.
                own_view: ControllerResponse = target.copy()
                if object.__getattribute__(self, "_is_cached") is True:
                    if self.url is not None:
                        own_view["url"] = self.url
                    own_view["is_remote"] = self.is_remote
                    own_view["id"] = self.id
                self._parse_target_data(data=own_view)

            for instance in target["available_instances"]:
                # The Target lists its own ADS Instance, that is us, so we refresh ourselves from it.
                if instance["instance_id"] == self.instance_id:
                    self._parse_instance_data(data=instance)
                    continue
                available_instances.append(instance)

        # Updated in place, matched by ID.
        self._controller._sync_instances(current=self._instances, available=available_instances, ads=self)  # pyright: ignore[reportPrivateUsage]
        return self._instances


class Controller(ADSData, ADSModule, Core, EmailSenderPlugin, FileManagerPlugin):
    """Represents an AMP Controller Instance.

    .. note::
        :meth:`~Controller.get_instances` copies this Controller's own data onto `self` and leaves its own ADS Instance
        (eg. `ADS01`) out of :attr:`Controller.instances`. The ADS Instances of remote Targets come back as
        :class:`TargetADS` in :attr:`Controller.targets`, and each one holds its own Instances.


    .. note::
        Similar to what you see when you log into AMP web GUI and see the Instances list.
        This attribute is cached and will require calling :meth:`~ADSModule.get_instances` to access the API converted class objects.
        * See the :attr:`Controller.instances` and :attr:`Controller.targets` attributes.


    Attributes
    ----------
    id : :class:`int`
        UNK
    disabled : :class:`bool`
        If the Controller is Disabled or not.
    is_remote : :class:`bool`
        If the Controller is remote or not.
    platform : :class:`PlatformInfo`
        Platform information related to the Instance.
    datastores : list[:class:`TargetDatastore`]
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

    # These three are the Controller's own, a TargetADS keeps the Instance's values instead.
    friendly_name: str
    description: str
    tags: list[str]

    _instances: set[InstanceTypeAliases]
    # The remote Targets keyed by their ADS ID, updated in place by `get_instances`.
    _targets: dict[str, TargetADS]
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

    _cached_names: ClassVar[frozenset[str]] = frozenset(__cached__)

    # __slots__ = ()

    @property
    def instances(self) -> set[InstanceTypeAliases]:
        """Represents the Instances the :class:`Controller` itself holds (its local Target),
        these are transferred from :attr:`~Controller.available_instance`.\n

        .. note::
            Similar to :attr:`~Controller.available_instance` but converted into a type of :class:`Instance` classes that
            have API functions.\n
            The Instances of remote Targets are not in here, they belong to their :class:`TargetADS` in :attr:`targets`.

        .. versionchanged:: 5.0.0
            Holds only the Controller's own Instances. 4.x held every Target's Instances here, with each ADS Instance
            as an `AMPADSInstance`.


        Returns
        -------
        set[Union[:class:`InstanceTypeAliases`]]
            A set of converted :class:`Instance` classes, empty until :meth:`get_instances` has run.

        """
        return self._instances

    @property
    def targets(self) -> dict[str, TargetADS]:
        """The remote Targets this :class:`Controller` can see, keyed by the Target's ADS ID.

        .. note::
            Each :class:`TargetADS` holds the Instances of its Target in :attr:`TargetADS.instances`, and
            :meth:`get_instances` fills them all.

        .. versionadded:: 5.0.0


        Returns
        -------
        dict[:class:`str`, :class:`TargetADS`]
            The Target ADS objects from the last :meth:`get_instances` call, empty until it has run.

        """
        return self._targets

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
        self._targets = {}
        self._ads_instance_id = None

        if data is not None:
            self._parse_target_data(data=data)

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

    async def __adel__(self) -> None:
        """Close any open connection when the Controller is discarded."""
        await self.clean_up()

    @overload
    def instance_conversion(
        self,
        instances: InstanceResponse,
        ads: Optional[Union[Controller, TargetADS]] = None,
    ) -> InstanceTypeAliases: ...
    @overload
    def instance_conversion(
        self,
        instances: list[InstanceResponse],
        ads: Optional[Union[Controller, TargetADS]] = None,
    ) -> set[InstanceTypeAliases]: ...

    def instance_conversion(
        self,
        instances: Union[list[InstanceResponse], InstanceResponse],
        ads: Optional[Union[Controller, TargetADS]] = None,
    ) -> Union[set[InstanceTypeAliases], InstanceTypeAliases]:
        """Takes the raw Instance data and turns it into :class:`Instance`, :class:`MinecraftInstance` and or
        :class:`TargetADS` respectively to facilitate API function accessibility.

        Parameters
        ----------
        instances : Union[list[:class:`InstanceResponse`], :class:`InstanceResponse`]
            A list of raw Instance dicts or a single one.
        ads : Union[:class:`Controller`, :class:`TargetADS`, None], optional
            The ADS that holds the Instances, None means this Controller, by default None.

        Returns
        -------
        Union[set[Union[:class:`InstanceTypeAliases`]], Union[:class:`InstanceTypeAliases`]]
            The set of converted Instance objects or a single converted object.

        """
        # We essentially call ourselves in a loop via a list check.
        if isinstance(instances, list):
            conv_instances: set[InstanceTypeAliases] = set()
            for instance in instances:
                conv_instances.add(self.instance_conversion(instances=instance, ads=ads))
            return conv_instances

        # An ADS Instance here is a remote Target's. Our own is left out by get_instances, and get_instance returns
        # self for it once our ADS ID is known. We hand them ourselves so they can still reach ADSModule endpoints.
        if instances["module"] == "ADS":
            return TargetADS(data=instances, controller=self, ads=ads, bridge=self._bridge, session=self.session)

        if instances["module"] == "Minecraft":
            return MinecraftInstance(data=instances, controller=self, ads=ads, bridge=self._bridge, session=self.session)

        return Instance(data=instances, controller=self, ads=ads, bridge=self._bridge, session=self.session)

    def _sync_instances(
        self,
        current: set[InstanceTypeAliases],
        available: list[InstanceResponse],
        ads: Optional[Union[Controller, TargetADS]] = None,
    ) -> None:
        """Update `current` in place from the raw Instance data, matched by Instance ID.

        Existing Instances are refreshed, new ones are converted and added, and the ones missing from `available`
        are dropped. An Instance whose module changed is replaced.

        Parameters
        ----------
        current : set[Union[:class:`InstanceTypeAliases`]]
            The set to update, kept as the same object.
        available : list[:class:`InstanceResponse`]
            The raw Instance data AMP listed.
        ads : Union[:class:`Controller`, :class:`TargetADS`, None], optional
            The ADS that holds the Instances, None means this Controller, by default None.

        """
        known: dict[str, InstanceTypeAliases] = {instance.instance_id: instance for instance in current}
        listed: set[str] = set()
        for data in available:
            instance_id: str = data["instance_id"]
            listed.add(instance_id)
            existing: Union[InstanceTypeAliases, None] = known.get(instance_id)
            if existing is not None and existing.module == data["module"]:
                existing._parse_instance_data(data=data)  # pyright: ignore[reportPrivateUsage]
                continue

            # A new Instance, or one whose module changed and so needs another class.
            if existing is not None:
                current.discard(existing)
            converted: InstanceTypeAliases = self.instance_conversion(instances=data, ads=ads)
            current.add(converted)
            known[instance_id] = converted

        for instance_id, stale in known.items():
            if instance_id not in listed:
                current.discard(stale)

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

        .. note::
            A Target's ADS ID returns the cached :class:`TargetADS` from :attr:`targets`, refreshed from the Target.
            With `format_data` False that is the Target's own raw dict.

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

        Raises
        ------
        :exc:`ValueError`
            If the ID is an Instance held by a cached :class:`TargetADS`. Use :meth:`TargetADS.get_instance` for it.

        Returns
        -------
        Union[:class:`Instance`, :class:`MinecraftInstance`, :class:`TargetADS`, :class:`Controller`, :class:`InstanceResponse`]
            On success returns the converted Instance, `self` for this Controller's own ADS, the cached
            :class:`TargetADS` for a Target's ADS ID, or the raw Instance dict if `format_data` is False.

        """
        cached_target = self._targets.get(instance_id)
        if cached_target is not None:
            return await cached_target.get_instance(
                instance_id=instance_id,
                format_data=format_data,
                request_params=request_params,
                **response_params,
            )

        # The Controller's copy of a Target's Instance differs from the Target's own data, so we refuse to build one.
        for target_ads in self._targets.values():
            for known_instance in target_ads.instances:
                if known_instance.instance_id == instance_id:
                    msg = (
                        f"The Instance {instance_id} is held by the Target {target_ads.friendly_name} ({target_ads.instance_id}). "
                        "Use `TargetADS.get_instance` on it instead."
                    )
                    raise ValueError(msg)

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

    @overload
    async def get_instances(
        self,
        *,
        format_data: Literal[True],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> set[InstanceTypeAliases]: ...

    @overload
    async def get_instances(
        self,
        *,
        format_data: Literal[False],
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[ControllerResponse]: ...

    # None falls back to the global `format_data`, which we can't know until runtime.
    @overload
    async def get_instances(
        self,
        *,
        format_data: None = ...,
        request_params: Optional[AioHTTPRequestOptions] = ...,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[set[InstanceTypeAliases], list[ControllerResponse]]: ...

    async def get_instances(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> Union[set[InstanceTypeAliases], list[ControllerResponse]]:
        """|coro|

        Returns a set of converted :class:`Instance` and :class:`MinecraftInstance` objects
        and updates our ``self`` object with the Controller's data.

        .. note::
            The set holds only the Instances the Controller itself holds (its local Target), and the Controller's own
            ADS Instance (eg. `ADS01`) is `self`, so it is left out. The local Target's `instance_id` is also kept as the
            Controller's own ADS ID, for :meth:`get_instance`.

        .. note::
            Each remote Target becomes a :class:`TargetADS` in :attr:`targets`, and every one of them runs its own
            :meth:`TargetADS.get_instances` at the same time. A Target that fails logs a warning and keeps an empty
            :attr:`TargetADS.instances`. A Target whose own ADS Instance is missing from the reply is skipped.

        .. note::
            The Instances and Targets are updated in place by Instance ID. :attr:`instances` and :attr:`targets` stay
            the same objects, existing Instances and :class:`TargetADS` objects are refreshed and keep their identity,
            new ones are added and the ones AMP no longer lists are dropped.

        .. note::
            If ``format_data`` is False this will return the raw list of Target dicts instead and nothing is updated.


        .. warning::
            This will be only Instances the AMP Controller and AMP User has permission to access.


        Parameters
        ----------
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

        # AMP sends one Target per ADS. The local one is us, so its data lands on our self object and its Instances
        # are ours. A remote Target becomes a TargetADS and gets its Instances from the Target itself, not our copy of them.
        # Everything is updated in place, matched by ID.
        local_instances: list[InstanceResponse] = []
        remote_ids: set[str] = set()
        for target in result:
            available_instances: list[InstanceResponse] = target["available_instances"]
            LOGGER.debug(
                "<%s.%s> | Target: %s | Remote: %s | Instances: %s",
                __class__.__name__,
                "get_instances",
                target["friendly_name"],
                target["is_remote"],
                len(available_instances),
            )
            if target["is_remote"] is False:
                self._parse_target_data(data=target)
                # Each Target lists its own ADS Instance, the one whose instance_id matches the Target's. In the local
                # Target that Instance is us, so it stays out of `instances`.
                local_instances.extend(instance for instance in available_instances if instance["instance_id"] != target["instance_id"])
                continue

            # The Target's own ADS Instance is the one we build the TargetADS from.
            own_ads_data: Union[InstanceResponse, None] = None
            for instance in available_instances:
                if instance["instance_id"] == target["instance_id"]:
                    own_ads_data = instance
                    break

            if own_ads_data is None:
                LOGGER.warning(
                    "<%s.%s> | The Target %s (%s) did not list its own ADS Instance, skipping it.",
                    __class__.__name__,
                    "get_instances",
                    target["friendly_name"],
                    target["instance_id"],
                )
                continue

            target_ads: Union[TargetADS, None] = self._targets.get(target["instance_id"])
            if target_ads is None or own_ads_data["module"] != target_ads.module:
                target_ads = TargetADS(
                    data=own_ads_data,
                    controller=self,
                    bridge=self._bridge,
                    session=self.session,
                )
                self._targets[target["instance_id"]] = target_ads
            else:
                target_ads._parse_instance_data(data=own_ads_data)  # pyright: ignore[reportPrivateUsage]

            # Our copy of the Target's data goes on first, so a Target that is down still has some.
            target_ads._parse_target_data(data=target)
            remote_ids.add(target["instance_id"])

        # The Targets AMP no longer lists are dropped.
        for target_id in [target_id for target_id in self._targets if target_id not in remote_ids]:
            del self._targets[target_id]
        self._sync_instances(current=self._instances, available=local_instances)

        # Every Target answers on its own, so we ask them all at once.
        target_list: list[TargetADS] = list(self._targets.values())
        outcomes = await asyncio.gather(
            *(target_ads.get_instances(format_data=True, request_params=request_params, **response_params) for target_ads in target_list),
            return_exceptions=True,
        )
        for target_ads, outcome in zip(target_list, outcomes, strict=True):
            if isinstance(outcome, BaseException):
                LOGGER.warning(
                    "<%s.%s> | Failed to get the Instances of the Target %s (%s) | Error: %s",
                    __class__.__name__,
                    "get_instances",
                    target_ads.friendly_name,
                    target_ads.instance_id,
                    outcome,
                )

        return self._instances
