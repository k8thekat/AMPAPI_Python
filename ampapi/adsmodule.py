from __future__ import annotations
from typing import Union

from .types import *
from .base import Base
from dataclass_wizard import fromdict

__all__ = ("ADSModule",)


class ADSModule(Base):
    """
    Contains the base functions for any `/API/ADSModule/` AMP API endpoints.

    """
    async def get_instance(self, instanceID: str) -> Instance | str | dict[str, Any] | list | bool | int | None:
        """
        Returns the Instance information for the provided Instance ID.\n
        **Requires ADS**

        Args:
            instanceID (str): The Instance ID to get information for.

        Returns:
            Instance | str | bool | int | None: On success returns a Instance dataclass. 
                See `types.py -> Instance`
        """

        await self._connect()
        parameters = {"InstanceId": instanceID}
        result = await self._call_api("ADSModule/GetInstance", parameters)
        if isinstance(result, dict):
            return fromdict(Instance, result)
        else:
            return result

    async def get_instances(self) -> list[Controller] | str | dict[str, Any] | list | bool | int | None:
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
        if isinstance(result, dict):
            # TODO - Check result data type.
            return list(fromdict(Controller, controller) for controller in result)
        else:
            return result

    async def get_instance_statuses(self) -> list[InstanceStatus] | dict | str | bool | int | None:
        """
        Returns a dictionary of the Server/Instance Status. \n
        **Requires ADS**

        Returns:
            list[InstanceStatus] | dict | str | bool | int | None: Returns a list of InstanceStatus dataclasses.
                See `types.py -> InstanceStatus`

        """

        await self._connect()
        result = await self._call_api('ADSModule/GetInstanceStatuses')
        if isinstance(result, dict):
            # TODO - Check result data type.
            return list(InstanceStatus(**instance)for instance in result)
        else:
            return result
