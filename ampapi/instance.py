from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Union

from .analytics import AnalyticsPlugin
from .core import Core
from .dataclass import ActionResult, Instance, InstanceStatus, Updates
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin
from .minecraft import MinecraftModule

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
    url: :class:`str`
        The API url.
    """

    url: str
    _controller: Union[AMPControllerInstance, None]

    def __init__(self, data: Union[Instance, None], controller: Union[AMPControllerInstance, None] = None) -> None:
        self.logger.debug("DEBUG %s __init__ %s", type(self).__name__, id(self))
        super().__init__()

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
    async def get_application_status(self, format_data: Union[bool, None] = None) -> InstanceStatus:
        """|coro|

        Gets the AMP Instance Application Status information and updates the class properties(State, Uptime and Metrics)

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
        result: InstanceStatus = await super().get_status(format_data=format_data)
        self.parse_data(data=result)
        return result

    @has_controller
    async def get_instance_status(self) -> Union[AMPInstance, AMPMinecraftInstance]:
        """|coro|

        Requests the recent changes to the Instance, updates our ``self`` object and returns the updated object.

        .. note::
            Typical usage is to get current information pertaining to an Instance and keeping it updated.


        .. warning::
            This only applies if you are manually creating these classes.\n
            - You must have a :class:`AMPControllerInstance` generated and set to :attr:`_controller` first. See ``__init__()``



        Raises
        -------
        :exc:`RuntimeError`:
            If the :attr:`_controller` attribute has not been set.

        Returns
        --------
        Union[:class:`AMPInstance`, :class:`AMPMinecraftInstance`]
            Returns an updated ``self`` object.
        """
        result: Instance = await self._controller.get_instance(instance_id=self.instance_id)  # type: ignore -- See the @has_controller decorator.
        self.parse_data(data=result)
        return self

    @Instance.online
    async def get_updates(self, format_data: Union[bool, None] = None) -> Updates:
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

        result: Updates = await super().get_updates(format_data=format_data)
        self.parse_data(data=result)
        return result

    @has_controller
    async def start_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
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
    async def stop_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
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
    async def restart_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
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
    async def update_instance(self, format_data: Union[bool, None] = None) -> ActionResult:
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
    module: :class:`str`
        The API module type, default is "Minecraft".
    """

    module: str = "Minecraft"


class AMPADSInstance(AMPInstance):
    """
    Typically referred to the "Target ADS" which is apart of the available Instances of the :class:`AMPControllerInstance` via :attr:`~AMPControllerInstance.instances`.

    .. note::
        No fundamental difference between this class and a :class:`AMPInstance`.


    Attributes
    -----------
    module: :class:`str`
        The API module type, default is "ADS".
    """

    module: str = "ADS"
