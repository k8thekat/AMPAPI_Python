from ampapi.types import Controller, Instance
from ampapi.adsmodule import ADSModule
from ampapi.core import Core
from ampapi.emailsender import EmailSenderPlugin
from ampapi.filebackup import LocalFileBackupPlugin
from ampapi.filemanager import FileManagerPlugin

__all__ = ("ADSInstance",)


class ADSInstance(ADSModule, Core, EmailSenderPlugin, LocalFileBackupPlugin, FileManagerPlugin, Controller):
    """
    The ADS class is the top most level of Instances inside of AMP, may also be referred to as the "Controller".


    """
    # TODO -
    # - Overwrite any ADS only type commands
    # -- Possibly overwrite return types and return Self with populated data.
    # - Try out modified `self._url` on Base and see if it still works.
    # - Possible Properties
    # -- Make a property to return Instances (possibly populated classes of `instance.py`)

    def __init__(self):
        print("ADSInstance __init__")
        super().__init__()
    #     # self.data: Controller = data
    #     # self.parse_data(data)

    # async def getInstances(self) -> list[Controller] | str | bool | int | None:
    #     return await super().getInstances()
