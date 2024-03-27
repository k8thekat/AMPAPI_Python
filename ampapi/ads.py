from typing import TYPE_CHECKING, Self, Union
from ampapi.types import Any, InstanceStatus, Session
from .types import Controller, Instance
from .adsmodule import ADSModule
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin
from .instance import AMPInstance, AMPMinecraftInstance


__all__ = ("ADSInstance",)


class ADSInstance(ADSModule, Core, EmailSenderPlugin, LocalFileBackupPlugin, FileManagerPlugin, Controller):
    """
    The ADS class is the top most level of Instances inside of AMP, may also be referred to as the "Controller".

    """

    Module: str = "ADS"

    @property
    def AvailableInstances(self) -> list[AMPInstance | AMPMinecraftInstance]:
        return self._AvailableInstances

    @AvailableInstances.setter
    def AvailableInstances(self, instances: list[Instance]) -> None:
        self._AvailableInstances: list[AMPInstance] = []
        if isinstance(instances, list) and len(instances) > 0:
            for i in range(0, len(instances)):
                if instances[i].Module == "ADS":
                    continue

                elif instances[i].Module == "Minecraft":
                    self._AvailableInstances.append(AMPMinecraftInstance(data=instances[i]))

                else:
                    self._AvailableInstances.append(AMPInstance(data=instances[i]))

    def __init__(self):
        # print(f"DEBUG {type(self).__name__} __init__")
        super().__init__()

    async def get_instances(self, format_data: Union[bool, None] = None) -> list[Controller | Self]:
        """
        Returns a list of all Instances on the AMP Panel.\n
        `**ADSInstance Only**`

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Self] | str | bool | int | None: On success returns a list of Self dataclasses. 

        """

        ads_list = []
        result = await super().get_instances(format_data=format_data)
        if isinstance(result, list):
            self.parse_data(data=result[0])  # Need to update our self object.
            for i in range(1, len(result)):
                ads_list.append(ADSInstance().parse_data(data=result[i]))
            return ads_list
        else:
            return result

    async def get_instance_statuses(self, format_data: Union[bool, None] = None) -> list[InstanceStatus]:
        """
        Returns a dictionary of the Server/Instance Status. \n
        `**ADSInstance Only**`

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[InstanceStatus] | dict | str | bool | int | None: Returns a list of InstanceStatus dataclasses.
                See `types.py -> InstanceStatus`

        """

        return await super().get_instance_statuses(format_data=format_data)

    async def get_instance(self, instance_id: str, format_data: Union[bool, None] = None) -> Instance:
        """
        Returns the Instance information for the provided Instance ID.\n
        `**ADSInstance Only**`

        Args:
            instance_id (str): The Instance ID to get information for.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Instance | str | bool | int | None: On success returns a Instance dataclass. 

        """

        return await super().get_instance(instance_id=instance_id, format_data=format_data)

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

    async def get_active_amp_sessions(self, format_data: Union[bool, None] = None) -> list[Session]:
        """
        Returns currently active AMP Sessions.\n
        `**ADSInstance Only**`

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Session | str | dict[str, Any] | list | bool | int | None: Returns a dataclass Session.
                See `types.py -> Session`

        """

        return await super().get_active_amp_sessions(format_data=format_data)
