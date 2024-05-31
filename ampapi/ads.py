from dataclasses import fields
from typing import Any, Self, Union

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
    _AvailableInstances: list[AMPInstance | AMPMinecraftInstance] = []
    _Controller_exists: bool = False

    @property
    def AvailableInstances(self) -> list[AMPInstance | AMPMinecraftInstance]:
        return self._AvailableInstances

    @AvailableInstances.setter
    def AvailableInstances(self, instances: list[Instance]) -> None:
        self._AvailableInstances = []
        if isinstance(instances, list) and len(instances) > 0:
            for i in range(0, len(instances)):
                if instances[i].Module == "ADS":
                    continue

                elif instances[i].Module == "Minecraft":
                    self._AvailableInstances.append(AMPMinecraftInstance(data=instances[i]))

                else:
                    self._AvailableInstances.append(AMPInstance(data=instances[i]))

    def __init__(self) -> None:
        self._logger.debug(msg=f"DEBUG {type(self).__name__} __init__")
        super().__init__()

    def __getattr__(self, name: str) -> AttributeError | Any:
        if name in [field.name for field in fields(class_or_instance=Controller)] and self._Controller_exists == False:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}' | You must call get_instances() with 'format_data=True' to update this object.")
        return self.__getattribute__(name)

    async def get_instances(self, format_data: Union[bool, None] = None) -> list[Controller | Self]:
        """
        Returns a list of all Controller Instances on the AMP Panel.\n
        `format_data == True` -- Will update our current object calling this method with the Instances belonging to it, else any Controller attributes will raise an AttributeError.

        `**ADSInstance Only**`

        Args:
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Self] | str | bool | int | None: On success returns a list of Self dataclasses. 

        """
        ads_list: list[ADSInstance | Controller] = []
        result: list[Controller] = await super().get_instances(format_data=format_data)
        if isinstance(result, list) and isinstance(result[0], Controller):
            self._Controller_exists = True
            self.parse_data(data=result[0])  # Need to update our self object.
            for i in range(1, len(result)):
                ads_list.append(ADSInstance().parse_data(data=result[i]))
            return ads_list
        else:
            return result
