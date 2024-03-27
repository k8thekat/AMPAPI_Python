from .types import Instance
from .adsmodule import ADSModule
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin
from .minecraft import MinecraftModule


__all__ = ("AMPInstance", "AMPMinecraftInstance")


class AMPInstance(Core, EmailSenderPlugin, LocalFileBackupPlugin, FileManagerPlugin, Instance):
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


class AMPMinecraftInstance(MinecraftModule, AMPInstance):
    """
    AMPMinecraftInstance represents a Minecraft Instance from AMP that is not the main panel.\n
    """

    Module: str = "Minecraft"
