from ampapi.types import Instance
from ampapi.adsmodule import ADSModule
from ampapi.core import Core
from ampapi.emailsender import EmailSenderPlugin
from ampapi.filebackup import LocalFileBackupPlugin
from ampapi.filemanager import FileManagerPlugin


class AMPInstance(ADSModule, Core, EmailSenderPlugin, LocalFileBackupPlugin, FileManagerPlugin, Instance):
    """
    AMPInstance represents an entire Instance from AMP that is not the main panel.\n
    This is similar to what you get when 'Managing' an instance from the Web GUI.


    """

    def __init__(self):
        print("AMPInstance __init__")
        super().__init__()
        self._url = f"/ADSModule/Servers/{self.InstanceID}"  # may need to add `/API` to these.

    def test(self):
        print()
