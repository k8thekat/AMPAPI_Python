from typing import Union

from .adsmodule import ADSModule
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin
from .minecraft import MinecraftModule
from .types import AppStatus, Instance, State_enum, Updates

__all__ = ("AMPInstance", "AMPMinecraftInstance")


class AMPInstance(Core, EmailSenderPlugin, LocalFileBackupPlugin, FileManagerPlugin, Instance, AppStatus, Updates):
    """
    AMPInstance represents an entire Instance from AMP that is not the main panel.\n
    This is similar to what you get when 'Managing' an instance from the Web GUI.


    """
    Module: str = "Instance"

    def __init__(self, data: Instance | None):
        # print(f"DEBUG {type(self).__name__} __init__")
        super().__init__()

        if isinstance(data, Instance):
            self.parse_data(data=data)

        self.url = f"{self._bridge.url}/API/ADSModule/Servers/{self.InstanceID}"

    @property
    def State(self) -> State_enum:
        """
        Returns the AppState of the Instance.
        """
        return self.AppState

    @State.setter
    def State(self, value: State_enum) -> None:
        self.AppState = value

    async def get_status(self, format_data: Union[bool, None] = None) -> AppStatus:
        """
        Gets the AMP Server/Instance Status information and updates the class properties(State, Uptime and Metrics)

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Status: On success returns a Status dataclass.
                See `types.py -> AppStatus`
        """

        result: AppStatus = await super().get_status(format_data=format_data)
        self.parse_data(data=result)
        return result

    async def get_updates(self, format_data: Union[bool, None] = None) -> Updates:
        """
        Requests the recent entries of the Instance Updates; will acquire all updates from previous API call of `getUpdate()` 
        and updates the class properties(ConsoleEntries, Status, Messages, Ports and Tasks).

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Updates: On success returns a Updates dataclass.
                See `types.py -> Updates`
        """

        result: Updates = await super().get_updates(format_data=format_data)
        self.parse_data(data=result)
        return result


class AMPMinecraftInstance(MinecraftModule, AMPInstance):
    """
    AMPMinecraftInstance represents a Minecraft Instance from AMP that is not the main panel.\n
    """

    Module: str = "Minecraft"
