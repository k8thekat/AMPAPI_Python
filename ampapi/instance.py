from .types import Instance
from .adsmodule import ADSModule
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin


class AMPInstance(ADSModule, Core, EmailSenderPlugin, LocalFileBackupPlugin, FileManagerPlugin, Instance):
    """
    AMPInstance represents an entire Instance from AMP that is not the main panel.\n
    This is similar to what you get when 'Managing' an instance from the Web GUI.


    """
    Module: str = "Instance"

    def __init__(self, data: Instance | None):
        print(f"DEBUG AMPInstance __init__")
        super().__init__()
        if isinstance(data, Instance):
            self.parse_data(data=data)

        self.url = f"{self._bridge.url}/API/ADSModule/Servers/{self.InstanceID}"
