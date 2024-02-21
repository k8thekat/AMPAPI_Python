from __future__ import annotations
from typing import Union

from ampapi.types import APIparams

from .types import *
from .base import Base
from .bridge import Bridge
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

        # if not isinstance(self, Controller):
        #     return self.ADS_ONLY

        await self._connect()
        parameters = {"InstanceId": instanceID}
        result = await self._call_api("ADSModule/GetInstance", parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return fromdict(Instance, result)  # type:ignore

    async def getInstances(self) -> list[Controller] | str | bool | int | None:
        """
        Returns a list of all Instances on the AMP Panel.\n
        **Requires ADS**

        Returns:
            list[Controller] | str | bool | int | None: On success returns a list of Controller dataclasses. 
                See `types.py -> Controller`\n
        """

        await self._connect()
        parameters = {}
        result = await self._call_api("ADSModule/GetInstances", parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return list(fromdict(Controller, controller) for controller in result)

    async def getInstanceStatuses(self) -> list[InstanceStatus] | dict | str | bool | int | None:
        """
        Returns a dictionary of the Server/Instance Status. \n
        **Requires ADS**

        Returns:
            list[InstanceStatus] | dict | str | bool | int | None: Returns a list of InstanceStatus dataclasses.
                See `types.py -> InstanceStatus`

        """
        # if not isinstance(self, Controller):
        #     return self.ADS_ONLY

        await self._connect()
        result = await self._call_api('ADSModule/GetInstanceStatuses')
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return list(InstanceStatus(**instance)for instance in result)
