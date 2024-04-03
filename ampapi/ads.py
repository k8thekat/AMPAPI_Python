from typing import TYPE_CHECKING, Self, Union

from .adsmodule import ADSModule
from .core import Core
from .emailsender import EmailSenderPlugin
from .filebackup import LocalFileBackupPlugin
from .filemanager import FileManagerPlugin
from .instance import AMPInstance, AMPMinecraftInstance
from .types import Controller, Instance

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
        Returns a list of all Instances on the AMP Panel and updates our self object.
        `**ADSInstance Only**`

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Self] | str | bool | int | None: On success returns a list of Self dataclasses. 

        """

        ads_list = []
        result: list[Controller] = await super().get_instances(format_data=format_data)
        if isinstance(result, list):
            self.parse_data(data=result[0])  # Need to update our self object.
            for i in range(1, len(result)):
                ads_list.append(ADSInstance().parse_data(data=result[i]))
            return ads_list
        else:
            return result
