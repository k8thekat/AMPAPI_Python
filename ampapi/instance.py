from dataclasses import field
from typing import TYPE_CHECKING, Union

from .analytics import AnalyticsPlugin
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin
from .minecraft import MinecraftModule
from .types import *

if TYPE_CHECKING:
    from .ads import ADSInstance

__all__ = ("AMPInstance", "AMPMinecraftInstance")


class AMPInstance(Core, EmailSenderPlugin, LocalFileBackupPlugin, FileManagerPlugin, AnalyticsPlugin, Instance, AppStatus, Updates):
    """
    AMPInstance represents an entire Instance from AMP that is not the main panel.\n
    This is similar to what you get when 'Managing' an instance from the Web GUI.


    """
    Module: str = "Instance"
    _AppState: State_enum = field(default=State_enum(value=-1))
    _State: State_enum = field(default=State_enum(value=-1))
    _Uptime: str = field(default="N/A")
    _Metrics: Metric | None = field(default=None)
    _ConsoleEntries: list[Console_Entries] = field(default_factory=list)
    _Status: AppStatus | None = field(default=None)
    _Ports: list[Port] = field(default_factory=list)
    _Tasks: list[Task] = field(default_factory=list)
    _Running: bool

    def __init__(self, data: Instance | None, ADS: "ADSInstance"):
        self._logger.debug(msg=f"DEBUG {type(self).__name__} __init__")
        super().__init__()

        if isinstance(data, Instance):
            self.parse_data(data=data)
        self._ADS: "ADSInstance" = ADS

        self.url = f"{self._bridge.url}/API/ADSModule/Servers/{self.InstanceID}"

    @property
    def State(self) -> str:
        """
        Returns the Application State from `Core.get_status()` of the Instance (eg. The Server/Application state inside the Instance).
        """
        if self._State is None:
            return State_enum(value=-1).name
        return self._State.name

    @State.setter
    def State(self, value: State_enum) -> None:
        self._State = State_enum(value=value)

    @property
    def AppState(self) -> str:
        """
        Represents the Application State from `ADS.get_instances()`. \n
        This attribute doesn't update unless `ADS.get_instances()` is called again and the class is remade.

        -----
        * To check if the Instance is running, check the `AMPInstance.Running` attribute.
        * To check if the Application is running, call `AMPInstance.get_status()` and check the `AMPInstance.State` property.
        """
        if self._AppState is None:
            return State_enum(value=-1).name
        return self._AppState.name

    @AppState.setter
    def AppState(self, value: int) -> None:
        self._AppState = State_enum(value=value)

    @property
    def Running(self) -> bool:
        """
        Represents the Instance State in bool format.
        * `True` = Running \n
        * `False` = Offline or Stopped

        """
        return self._Running

    @Running.setter
    def Running(self, value: int) -> None:
        self._Running = bool(value)

    @Core.online
    async def stop(self, format_data: Union[bool, None] = None) -> ActionResult | None:
        """
        Stops the Instance.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Raises:
        ---
            ConnectionError: The requested instance is not available at this time.

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        return await self._ADS.stop_instance(instance_name=self.InstanceName, format_data=format_data)

    async def start(self, format_data: Union[bool, None] = None) -> ActionResult | None:
        """
        Start the Instance.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        return await self._ADS.start_instance(instance_name=self.InstanceName, format_data=format_data)

    @Core.online
    async def restart(self, format_data: Union[bool, None] = None) -> ActionResult | None:
        """
        Restart the Instance.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Raises:
        ---
            ConnectionError: The requested instance is not available at this time.

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        return await self._ADS.restart_instance(instance_name=self.InstanceName, format_data=format_data)

    async def update(self, format_data: Union[bool, None] = None) -> ActionResult | None:
        """
        Update the AMP Instance.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """
        return await self._ADS.upgrade_instance(instance_name=self.InstanceName, format_data=format_data)

    @Core.online
    async def get_status(self, format_data: Union[bool, None] = None) -> AppStatus | None:
        """
        Gets the AMP Instance Application Status information and updates the class properties(State, Uptime and Metrics)


        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Raises:
        ---
            ConnectionError: The requested instance is not available at this time.

        Returns:
        ---
            Status: On success returns a AppStatus dataclass.
            * See `types.py -> AppStatus`
        """

        result: AppStatus = await super().get_status(format_data=format_data)
        self.parse_data(data=result)
        return result

    @Core.online
    async def get_updates(self, format_data: Union[bool, None] = None) -> Updates | None:
        """
        Requests the recent entries of the Instance Updates; will acquire all updates from previous API call of `getUpdate()` 
        and updates the class properties(ConsoleEntries, Status, Messages, Ports and Tasks).

        * If the Instance is `Offline/Undefined` the method will return None

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Raises:
        ---
            ConnectionError: The requested instance is not available at this time.

        Returns:
        ---
            Updates: On success returns a Updates dataclass.
            * See `types.py -> Updates`
        """

        result: Updates = await super().get_updates(format_data=format_data)
        self.parse_data(data=result)
        return result


class AMPMinecraftInstance(MinecraftModule, AMPInstance):
    """
    AMPMinecraftInstance represents a Minecraft Instance from AMP that is not the main panel.\n
    """

    Module: str = "Minecraft"
