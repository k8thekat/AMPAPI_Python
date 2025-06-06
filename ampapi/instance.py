from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Any, Union

from .analytics import AnalyticsPlugin
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin
from .minecraft import MinecraftModule
from .modules import ActionResult, ActionResultError, Instance, InstanceStatus, Status, Updates

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Concatenate

    from typing_extensions import ParamSpec, TypeVar

    from .controller import AMPControllerInstance

    D = TypeVar("D", bound="AMPInstance")
    T = ParamSpec("T")
    F = TypeVar("F")

__all__ = ("AMPADSInstance", "AMPInstance", "AMPMinecraftInstance")


class AMPInstance(
    Core, EmailSenderPlugin, LocalFileBackupPlugin, FileManagerPlugin, AnalyticsPlugin, Instance, InstanceStatus, Updates
):
    """
    :class:`AMPInstance` represents an entire Instance from AMP that is not AMP Controller, AMP Target/ADS or Minecraft.\n
    This is similar to what you get when selecting 'Manage' an instance from the Web GUI.

    .. note::
        - Do *NOT* change the :attr:`~Instance.module` attribute.
        - Attributes are cached! Please call the respective Endpoints to get current information.
        - To Update the attributes call :meth:`get_instance_status` or :meth:`get_updates`.
        - To check if the Instance is running, check the :attr:`running` property.
        - To check if the Application is running, check the :attr:`app_state` property.


    Parameters
    -----------
    data: Union[:class:`Instance`, None]
        The Instance data to be unpacked and set as attributes of this class to execute API calls.
    controller: Union[:class:`AMPControllerInstance`, None]
        The :class:`AMPControllerInstance` to be used to execute specific API calls.

    Attributes
    -----------
    amp_version: Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    application_endpoints: list[dict[str, str]]
        The list of application endpoints for the Instance.
    app_state: :class:`AMPInstanceState`
        The state of the application.
    container_cpus: :class:`float`
        The amount of CPU cores allocated to the container, default is 0.0.
    container_memory_mb: :class:`int`
        The amount of memory allocated to the container in MB.
    container_memory_policy: :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance.
    daemon: :class:`bool`
        If the Instance is a daemon.
    daemon_autostart: :class:`bool`
        If the Instance should be autostart on boot.
    deployment_args: dict[:class:`str`, :class:`str`]
        The deployment arguments of the Instance.
    description: :class:`str`
        The description of the Instance, default is "".
    disk_usage_mb: :class:`int`
        The disk usage of the Instance in MB.
    display_image_source: :class:`str`
        The source of the display image, default is "".
    exclude_from_firewall: :class:`bool`
        If the Instance should be excluded from the firewall.
    friendly_name: :class:`str`
        The friendly name of the Instance.
    ip: :class:`str`
        The IP address of the Instance.
    instance_id: :class:`str`
        The Instance GUID.
    instance_name: :class:`str`
        The Instance name.
    is_container_instance: :class:`bool`
        If the Instance is a container instance.
    is_https: :class:`bool`
        If the Instance is using HTTPS.
    management_mode: :class:`int`
        The management mode of the Instance.
    metrics: Union[:class:`Metric`, None]
        The metrics of the Instance, default is None.
    module: :class:`str`
        The module of the Instance.
    module_display_name: :class:`str`
        The display name of the module, default is "".
    port: :class:`str`
        The port of the Instance.
    release_stream: :class:`int`
        The release stream of the Instance.
    running: :class:`bool`
        If the Instance is running.
    suspended: :class:`bool`
        If the Instance is suspended.
    tags: Union[:class:`None`, :class:`list`]
        The list of tags of the Instance, default is None.
    target_id: :class:`str`
        The target ID of the Instance.
    url: :class:`str`
        The API url.
    """

    url: str
    _controller: Union[AMPControllerInstance, None]

    def __init__(
        self, data: Union[Instance, None], controller: Union[AMPControllerInstance, None] = None, **kwargs: Any
    ) -> None:
        # self.logger.debug("DEBUG %s __init__ %s", type(self).__name__, id(self))
        super().__init__(**kwargs)

        if isinstance(data, Instance):
            self.parse_data(data=data)

        # We use the AMPControllerInstance class to call ADSModule specific Endpoints as a
        # typical AMP Instance will not have the :py:class:`ADSModule` API Endpoints.
        self._controller = controller

        self.url = f"{self._bridge.url}/API/ADSModule/Servers/{self.instance_id}"

    def __hash__(self) -> int:
        return hash(self.instance_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.instance_id == other.instance_id

    def __repr__(self) -> str:
        return super().__repr__() + f"Url: {self.url}"

    @staticmethod
    def has_controller(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """
        Checks the class :attr:`._controller` is not equal to None.

        Parameters
        -----------
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]]
            The function the decorator is wrapping.

        Raises
        -------
        :exc:`RuntimeError`
            The API call is only allowed to be run on a type(:class:`AMPControllerInstance`).

        Returns
        --------
        :class:`Callable`[class:`Concatenate`[D, T], :class:`Coroutine`[None, None, F]]
            The function the decorator is wrapping.
        """

        @functools.wraps(wrapped=func)
        def wrapper_has_controller(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            if self._controller is not None:
                return func(self, *args, **kwargs)
            else:
                raise RuntimeError(self._no_controller)

        return wrapper_has_controller

    @Instance.online
    async def get_application_status(self, format_data: Union[bool, None] = None) -> Status | ActionResultError:
        """|coro|

        Similar to :meth:`Core.get_status` but with the added benefit of updating our ``self`` object reference.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Raises
        -------
        :exc:`ConnectionError`:
            The requested instance is not available at this time if the Instance is not running.

        Returns
        --------
        :class:`AppStatus`
            On success returns a :class:`AppStatus` dataclass.
        """
        result: Status | ActionResultError = await super().get_status(format_data=format_data)
        if isinstance(result, ActionResultError):
            return result
        self.parse_data(data=result)
        return result

    @has_controller
    async def get_instance_status(self) -> Union[AMPInstance, AMPMinecraftInstance] | ActionResultError:
        """|coro|

        Requests the recent changes to the Instance, updates our ``self`` object and returns the updated object.

        .. note::
            Typical usage is to get current information pertaining to an Instance and keeping it updated.


        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`AMPControllerInstance` generated and set to :attr:`_controller` first. See ``__init__()``

        .. warning::
            This will fail if you attempt to call it on the Target or Controller type Instance, returning an :class:`ActionResultError`



        Raises
        -------
        :exc:`RuntimeError`:
            If the :attr:`_controller` attribute has not been set.

        Returns
        --------
        Union[:class:`AMPInstance`, :class:`AMPMinecraftInstance`]
            Returns an updated ``self`` object.
        """

        result: Instance | ActionResultError = await self._controller.get_instance(instance_id=self.instance_id)  # type: ignore -- See the @has_controller decorator.
        if isinstance(result, ActionResultError):
            self.logger.warning(
                "Failed to retrieved updated Instance information. | Instance ID: %s | Result: %s",
                self.instance_id,
                result,
            )
            return result
        self.parse_data(data=result)
        return self

    @Instance.online
    async def get_updates(self, format_data: Union[bool, None] = None) -> Updates | ActionResultError:
        """|coro|

        Requests the recent Console entries of the Instance, will acquire all updates from previous API call of :meth:`get_updates`
        and updates parses the information setting it to ``self``. See :class:`Updates` for attribute access.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        Parameters
        -----------
        format_data: Union[:class:`bool`, :class:`None`], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if :class:`None`), by default :class:`None`

        Raises
        -------
        :exc:`ConnectionError`
            If the :attr:`running` is False.
        :exc:`RuntimeError`
            If the :attr:`_controller` attribute has not been set.

        Returns
        --------
        :class:`Updates`
            On success returns a :class:`Updates` dataclass.
        """

        result: Updates | ActionResultError = await super().get_updates(format_data=format_data)
        if isinstance(result, ActionResultError):
            self.logger.warning(
                "Failed to retrieved updated Instance information. | Instance ID: %s | Result: %s",
                self.instance_id,
                result,
            )
            return result
        self.parse_data(data=result)
        return result

    @has_controller
    async def start_instance(self, format_data: Union[bool, None] = None) -> ActionResult | ActionResultError:
        """|coro|

        Start the Instance.

        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`AMPControllerInstance` generated and set to :attr:`_controller` first. See ``__init__()``



        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Raises
        -------
        :exc:`RuntimeError`
            If the :attr:`_controller` attribute has not been set.


        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """

        # This function is to mimic the `ADSModule.start_instance()` which we use the self._controller attribute to access.
        return await self._controller.start_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @Instance.online
    @has_controller
    async def stop_instance(self, format_data: Union[bool, None] = None) -> ActionResult | ActionResultError:
        """|coro|

        Stops the Instance.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`


        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`AMPControllerInstance` generated and set to :attr:`_controller` first. See ``__init__()``


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Raises
        -------
        :exc:`ConnectionError`
            If the :attr:`running` is False.
        :exc:`RuntimeError`
            If the :attr:`_controller` attribute has not been set.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """
        # This function is to mimic the `ADSModule.stop_instance()` which we use the self._controller attribute to access.
        return await self._controller.stop_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @Instance.online
    @has_controller
    async def restart_instance(self, format_data: Union[bool, None] = None) -> ActionResult | ActionResultError:
        """|coro|

        Restart the Instance.

        .. note::
            The Instance MUST be running (:attr:`~Instance.running = True`) or you will get a :class:`ConnectionError`

        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`AMPControllerInstance` generated and set to :attr:`_controller` first. See ``__init__()``


        Parameters
        -----------
        format_data: Union[bool, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Raises
        -------
        :exc:`ConnectionError`:
            The requested instance is not available at this time if the Instance is offline.
        :exc:`RuntimeError`:
            If the :attr:`_controller` attribute has not been set.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        # This function is to mimic the `ADSModule.restart_instance()` which we use the self._controller attribute to access.
        return await self._controller.restart_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.

    @has_controller
    async def update_instance(self, format_data: Union[bool, None] = None) -> ActionResult | ActionResultError:
        """|coro|
        Update the AMP Instance.

        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`AMPControllerInstance` generated and set to :attr:`_controller` first. See ``__init__()``


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """
        # This function is to mimic the `ADSModule.update_instance()` which we use the self._controller attribute to access.
        return await self._controller.upgrade_instance(instance_name=self.instance_name, format_data=format_data)  # type: ignore -- See the @has_controller decorator.


class AMPMinecraftInstance(MinecraftModule, AMPInstance):
    """
    Represents a Minecraft Instance from AMP containing all relevant API Endpoints specific to Minecraft Instances.

    Attributes
    -----------
    amp_version: Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    application_endpoints: list[dict[str, str]]
        The list of application endpoints for the Instance.
    app_state: :class:`AMPInstanceState`
        The state of the application.
    container_cpus: :class:`float`
        The amount of CPU cores allocated to the container, default is 0.0.
    container_memory_mb: :class:`int`
        The amount of memory allocated to the container in MB.
    container_memory_policy: :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance.
    daemon: :class:`bool`
        If the Instance is a daemon.
    daemon_autostart: :class:`bool`
        If the Instance should be autostart on boot.
    deployment_args: dict[:class:`str`, :class:`str`]
        The deployment arguments of the Instance.
    description: :class:`str`
        The description of the Instance, default is "".
    disk_usage_mb: :class:`int`
        The disk usage of the Instance in MB.
    display_image_source: :class:`str`
        The source of the display image, default is "".
    exclude_from_firewall: :class:`bool`
        If the Instance should be excluded from the firewall.
    friendly_name: :class:`str`
        The friendly name of the Instance.
    ip: :class:`str`
        The IP address of the Instance.
    instance_id: :class:`str`
        The Instance GUID.
    instance_name: :class:`str`
        The Instance name.
    is_container_instance: :class:`bool`
        If the Instance is a container instance.
    is_https: :class:`bool`
        If the Instance is using HTTPS.
    management_mode: :class:`int`
        The management mode of the Instance.
    metrics: Union[:class:`Metric`, None]
        The metrics of the Instance, default is None.
    module: :class:`str`
        The module of the Instance, default is "Minecraft".
    module_display_name: :class:`str`
        The display name of the module, default is "".
    port: :class:`str`
        The port of the Instance.
    release_stream: :class:`int`
        The release stream of the Instance.
    running: :class:`bool`
        If the Instance is running.
    suspended: :class:`bool`
        If the Instance is suspended.
    tags: Union[:class:`None`, :class:`list`]
        The list of tags of the Instance, default is None.
    target_id: :class:`str`
        The target ID of the Instance.
    url: :class:`str`
        The API url.
    """

    module: str = "Minecraft"


class AMPADSInstance(AMPInstance):
    """
    Typically referred to the "Target ADS" which is apart of the available Instances of the :class:`AMPControllerInstance` via :attr:`~AMPControllerInstance.instances`.

    .. note::
        No fundamental difference between this class and a :class:`AMPInstance`.


    Attributes
    -----------
    amp_version: Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    application_endpoints: list[dict[str, str]]
        The list of application endpoints for the Instance.
    app_state: :class:`AMPInstanceState`
        The state of the application.
    container_cpus: :class:`float`
        The amount of CPU cores allocated to the container, default is 0.0.
    container_memory_mb: :class:`int`
        The amount of memory allocated to the container in MB.
    container_memory_policy: :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance.
    daemon: :class:`bool`
        If the Instance is a daemon.
    daemon_autostart: :class:`bool`
        If the Instance should be autostart on boot.
    deployment_args: dict[:class:`str`, :class:`str`]
        The deployment arguments of the Instance.
    description: :class:`str`
        The description of the Instance, default is "".
    disk_usage_mb: :class:`int`
        The disk usage of the Instance in MB.
    display_image_source: :class:`str`
        The source of the display image, default is "".
    exclude_from_firewall: :class:`bool`
        If the Instance should be excluded from the firewall.
    friendly_name: :class:`str`
        The friendly name of the Instance.
    ip: :class:`str`
        The IP address of the Instance.
    instance_id: :class:`str`
        The Instance GUID.
    instance_name: :class:`str`
        The Instance name.
    is_container_instance: :class:`bool`
        If the Instance is a container instance.
    is_https: :class:`bool`
        If the Instance is using HTTPS.
    management_mode: :class:`int`
        The management mode of the Instance.
    metrics: Union[:class:`Metric`, None]
        The metrics of the Instance, default is None.
    module: :class:`str`
        The module of the Instance, default is "ADS".
    module_display_name: :class:`str`
        The display name of the module, default is "".
    port: :class:`str`
        The port of the Instance.
    release_stream: :class:`int`
        The release stream of the Instance.
    running: :class:`bool`
        If the Instance is running.
    suspended: :class:`bool`
        If the Instance is suspended.
    tags: Union[:class:`None`, :class:`list`]
        The list of tags of the Instance, default is None.
    target_id: :class:`str`
        The target ID of the Instance.
    url: :class:`str`
        The API url.
    """

    module: str = "ADS"
