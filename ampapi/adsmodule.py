from __future__ import annotations
from typing import Union

from .types import *
from .base import Base
from dataclass_wizard import fromdict

__all__ = ("ADSModule",)


class ADSModule(Base):
    async def getInstance(self, instanceID: str) -> Instance | str | bool | int | None:
        """
        Returns the Instance information for the provided Instance ID.\n
        **Requires ADS**

        Args:
            instanceID (str): The Instance ID to get information for.

        Returns:
            Instance | str | bool | int | None: On success returns a Instance dataclass. 
                See `types.py -> Instance`
        """

        if not isinstance(self, Controller):
            return self.ADS_ONLY

        await self._connect()
        parameters = {"InstanceId": instanceID}
        result = await self._call_api("ADSModule/GetInstance", parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return fromdict(Instance, result)  # type:ignore

    async def getInstanceStatuses(self) -> list[InstanceStatus] | dict | str | bool | int | None:
        """
        Returns a dictionary of the Server/Instance Status. \n
        **Requires ADS**

        Returns:
            list[InstanceStatus] | dict | str | bool | int | None: Returns a list of InstanceStatus dataclasses.
                See `types.py -> InstanceStatus`

        """
        if not isinstance(self, Controller):
            return self.ADS_ONLY

        await self._connect()
        result = await self._call_api('ADSModule/GetInstanceStatuses')
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return list(InstanceStatus(**instance)for instance in result)
