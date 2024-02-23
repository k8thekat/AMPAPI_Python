from ampapi.types import Any, InstanceStatus, Session
from .types import Controller, Instance
from .adsmodule import ADSModule
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin

from typing import Self

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

    async def get_instances(self) -> list[Controller | Self] | str | bool | dict[str, Any] | int | None:
        """
        Returns a list of all Instances on the AMP Panel.\n
        `**ADSInstance Only**`

        Returns:
            list[Self] | str | bool | int | None: On success returns a list of Self dataclasses. 

        """
        ads_list = []
        result = await super().get_instances()
        if isinstance(result, list):
            for i in range(len(result)):
                if i == 0:
                    self.parse_data(data=result[i])  # Need to update our self object.
                ads_list.append(ADSInstance().parse_data(data=result[i]))
            return ads_list
        else:
            return result

    async def get_instance_statuses(self) -> list[InstanceStatus] | dict | str | bool | int | None:
        """
        Returns a dictionary of the Server/Instance Status. \n
        `**ADSInstance Only**`

        Returns:
            list[InstanceStatus] | dict | str | bool | int | None: Returns a list of InstanceStatus dataclasses.
                See `types.py -> InstanceStatus`

        """
        return await super().get_instance_statuses()

    async def get_instance(self, instanceID: str) -> Instance | str | dict[str, Any] | list | bool | int | None:
        """
        Returns the Instance information for the provided Instance ID.\n
        `**ADSInstance Only**`

        Args:
            instanceID (str): The Instance ID to get information for.

        Returns:
            Instance | str | bool | int | None: On success returns a Instance dataclass. 
        """
        return await super().get_instance(instanceID)

    async def end_user_session(self, session_id: str) -> str | None:
        """
        Closes the specified User's session ID to AMP.\n
        `**ADSInstance Only**`

        Args:
            session_id (str): session ID to end.

        Returns:
            None: ""
        """
        return await super().end_user_session(session_id)

    async def get_active_amp_sessions(self) -> list[Session] | str | dict[str, Any] | list | bool | int | None:
        """
        Returns currently active AMP Sessions.\n
        `**ADSInstance Only**`

        Returns:
            Session | str | dict[str, Any] | list | bool | int | None: Returns a dataclass Session.
                See `types.py -> Session`
        """
        return await super().get_active_amp_sessions()
