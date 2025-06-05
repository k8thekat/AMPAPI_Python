import asyncio
from collections.abc import Iterable
from dataclasses import fields
from typing import Any, Optional, Union, overload

import aiohttp

from .adsmodule import ADSModule
from .core import Core
from .emailsender import EmailSenderPlugin
from .filemanager import FileManagerPlugin
from .instance import AMPADSInstance, AMPInstance, AMPMinecraftInstance
from .modules import ActionResultError, Controller, Instance

__all__ = ("AMPControllerInstance", "InstanceTypeAliases")

InstanceTypeAliases = Union[AMPInstance, AMPMinecraftInstance, AMPADSInstance]


class AMPControllerInstance(ADSModule, Core, EmailSenderPlugin, FileManagerPlugin, Controller):
    """
    The AMPControllerInstance class is the top most level of Instances inside of AMP. This has access the Target ADS and all Instances it can see.\n

    .. note::
        All API Endpoints an AMP Controller Instance would have access to this class object does too.


    .. note::
        See :meth:`ADSModule.get_instances(include_self = True)` making the first instance "typically" the Controller Instance. aka ``ADS01``.


    .. note::
        Similar to what you see when you log into AMP web GUI and see the Instances list.
        This attribute is cached and will require calling :meth:`~ADSModule.get_instances` to access the API converted class objects.
        * See the :attr:`AMPControllerInstance.instances` attribute.


    Attributes
    -----------
    id: :class:`int`
        UNK
    disabled: :class:`bool`
        If the Controller is Disabled or not.
    is_remote: :class:`bool`
        If the Controller is remote or not.
    platform: :class:`PlatformInfo`
        Platform information related to the Instance.
    datastores: list[dict[:class:`str`, Union[:class:`str`, :class:`int`]]]
        The Datastores that the Controller has access to.
    creates_in_containers: :class:`bool`
        The Controller will create the Instances in containers.
    can_create: :class:`bool`
        If the Controller can create Instances or not.
    available_instances: list[:class:`Instance`]
        A list of AMP Instances the Controller/ADS has permissions to see.
    available_ips : list[:class:`str`]
        The list of available IPs the Controller/Instance has.
    tags: list[:class:`str`]
        The tags related to the Controller/Instance.
    url: :class:`str`
        The URL for the Controller/Instance.
    last_updated: Union[:class:`str`, :class:`datetime`]
        The last_updated comes in as  ISO format and :meth:`Controller`__post_init__` converts it into a datetime object.
    instance_id: :class:`str`
        The Controller/Instance ID tied to the Instance, default is "0".
    state: :py:class:`AMPInstanceState`
        The state the Controller/Instance is in. See enum :py:class:`AMPInstanceState`, default is ``AMPInstanceState.UNDEFINED``.
    fitness: Union[Fitness, None]
        UNK.
    friendly_name: :class:`str`
        The Controller/Instance friendly name, default is "None".
    state_reason: :class:`str`
        UNK, default is "".
    description: :class:`str`
        Controller/Instance description, default is "".
    tags_list : Union[list[:class:`str`]]
        The list of tags related to the Controller/Instance if any, default is None.
    triggers: :class:`TriggerID`
        You can access all the trigger IDs an instance has via this attribute. See :class:`TriggerID` for more information.
    """

    _controller_exists: bool = False

    def __init__(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        super().__init__(session=session)
        self.module: str = "ADS"

    def __getattr__(self, name: str) -> Union[AttributeError, Any]:
        if name in [field.name for field in fields(class_or_instance=Controller)] and self._controller_exists is False:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}' | You must call <AMPControllerInstance>.get_instances() with 'format_data=True' to update this object."
            )
        return self.__getattribute__(name)

    def __del__(self) -> None:
        try:
            asyncio.run(self.__adel__())
            self.logger.debug("Closed `aiohttp.ClientSession`| Session: %s", self.session)
        except RuntimeError:
            self.logger.error("Failed to close our `aiohttp.ClientSession`")

    async def __adel__(self) -> None:
        if self.session is not None:
            await self.session.close()

    @property
    def instances(self) -> set[Union[AMPADSInstance, AMPInstance, AMPMinecraftInstance]]:
        """
        Represents all Instances the :class:`AMPControllerInstance` can see,
        these are transferred from :attr:`~Controller.available_instance`.\n

        .. note::
            Similar to :attr:`~Controller.available_instance` but converted into a type of :class:`AMPInstance` classes that have API functions.\n
            The set of :class:`AMPInstance` types will be ordered by :attr:`~Instance.instance_id`.


        Returns
        --------
        set[Union[:class:`AMPADSInstance`, :class:`AMPInstance`, :class:`AMPMinecraftInstance`]]
            A set of converted :class:`Instance` classes sorted by :class:`~Instance.instance_id`.
        """
        return self._instances

    @instances.setter
    def instances(self, data: Any) -> None:
        """
        self.instances setter will take :attr:`~Controller.available_instances` and convert them into a type of :class:`AMPInstance`.

        Parameters
        -----------
        data: Any
            A list of :class:`Instance`.
        """
        self._instances: set[InstanceTypeAliases] = self.instance_conversion(instances=self.available_instances)

    @overload
    def instance_conversion(self, instances: Instance) -> InstanceTypeAliases: ...

    @overload
    def instance_conversion(self, instances: Iterable[Instance]) -> set[InstanceTypeAliases]: ...

    def instance_conversion(
        self, instances: Iterable[Instance] | Instance
    ) -> set[InstanceTypeAliases] | InstanceTypeAliases:
        """
        Takes a set of :class:`Instance` dataclasses and turns them into :class:`AMPInstance`, :class:`AMPMinecraftInstance` and or :class:`AMPADSInstance` respectively to facilitate API function accessibility.

        .. note::
            By default the list of instances will be sorted.


        Parameters
        -----------
        instances: Iterable[:class:`Instance`] | :class:`Instance`
            An Iterable of :class:`Instance` dataclasses or a single object.

        Returns
        --------
        set[Union[:class:`AMPInstance`, :class:`AMPMinecraftInstance`, :class:`AMPADSInstance`]] | Union[:class:`AMPInstance`, :class:`AMPMinecraftInstance`, :class:`AMPADSInstance`]
            The set of converted :class:`Instance` objects or a single converted object.
        """
        conv_instances: set[Union[AMPInstance, AMPMinecraftInstance, AMPADSInstance]] = set()
        if isinstance(instances, list) and len(instances) > 0:
            instances = sorted(instances)
            for entry in instances:
                if entry.module == "ADS":
                    conv_instances.add(AMPADSInstance(data=entry, controller=self, session=self.session))

                elif entry.module == "Minecraft":
                    conv_instances.add(AMPMinecraftInstance(data=entry, controller=self, session=self.session))

                else:
                    conv_instances.add(AMPInstance(data=entry, controller=self, session=self.session))

        elif isinstance(instances, Instance):
            if instances.module == "ADS":
                return AMPADSInstance(data=instances, controller=self, session=self.session)

            elif instances.module == "Minecraft":
                return AMPMinecraftInstance(data=instances, controller=self, session=self.session)

            else:
                return AMPInstance(data=instances, controller=self, session=self.session)
        return conv_instances

    @overload
    async def get_instance(
        self, instance_id: str, format_data: Union[bool, None] = True
    ) -> InstanceTypeAliases | ActionResultError: ...

    @overload
    async def get_instance(
        self, instance_id: str, format_data: Union[bool, None] = False
    ) -> InstanceTypeAliases | ActionResultError: ...

    @overload
    async def get_instance(self, instance_id: str, format_data: Union[bool, None] = False) -> ActionResultError | dict: ...

    async def get_instance(
        self, instance_id: str, format_data: Union[bool, None] = None
    ) -> InstanceTypeAliases | ActionResultError | dict:
        """
        Retrieve a single Instance by ID and convert the Instance

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID to retrieve.

        Returns
        --------
        :class:`InstanceTypeAliases`
            On success returns a :class:`InstanceTypeAliases` dataclass.
        """
        result: Instance | ActionResultError = await super().get_instance(instance_id=instance_id, format_data=format_data)
        if isinstance(result, (dict, ActionResultError)):
            return result
        else:
            return self.instance_conversion(instances=result)

    @overload
    async def get_instances(
        self, include_self: bool = True, format_data: Union[bool, None] = None
    ) -> set[InstanceTypeAliases]: ...

    @overload
    async def get_instances(
        self, include_self: bool = True, format_data: Union[bool, None] = False
    ) -> Iterable[Union[Controller, Instance]]: ...

    async def get_instances(
        self, include_self: bool = True, format_data: Union[bool, None] = True
    ) -> Union[set[InstanceTypeAliases], Iterable[Union[Controller, Instance]], ActionResultError]:
        """|coro|

        Returns a set of converted :class:`Instances` to :class:`AMPInstance`, :class:`AMPMinecraftInstance` and :class:`AMPADSInstance`.\n

        .. note::
            If ``format_data`` == ``False`` this will return the list of :class:`Controller` and or :class:`Instance` dataclasses instead.


        .. warning::
            This will be only Instances the AMP Controller and AMP User has permission to access.\n


        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.

        Returns
        --------
        Union[set[Union[:class:`AMPInstance`, :class:`AMPMinecraftInstance`, :class:`AMPADSInstance`]], list[Union[:class:`Controller`, :class:`Instance`]]]
            On success returns a set of :class:`AMPInstance`, :class:`AMPMinecraftInstance` and or :class:`AMPADSInstance` dataclasses. \n

        """
        result: list[Union[Controller, Instance]] | ActionResultError = await super().get_instances(
            include_self=include_self, format_data=format_data
        )
        if isinstance(result, ActionResultError):
            return result

        if isinstance(result[0], Controller):
            self.logger.debug(
                "Updating %s, with Controller dataclass: %s |\nObject:\n%s", __class__.__name__, id(result[0]), result[0]
            )
            # We make the first Controller dataclass our AMPControllerInstance and transfer all the information from the Controller to Self.
            _url = self.url
            self.parse_data(data=result[0])
            self._controller_exists = True
            self.url = _url
            # Since we populated all the attributes from result[0] onto ourselves;
            # we can convert Controller.available_instances dynamically by
            # setting it to our self.instances attribute using the @setter for instances attribute.
            self.instances = self.available_instances
            # Then we remove the Controller from the list as we converted that object and don't want to re-add those instances again.
            result.pop(0)
            # Now we are going to go through and find any other Controllers and place all those Instances under our self object.
            for i in result:
                # If we have another Controller, we want to get it's available_instances and convert them into proper objects to be used.
                if isinstance(i, Controller):
                    self.logger.debug("Found an additional Controller dataclass: %s | %s", id(i), i)
                    # after the conversion we are updating our instance attribute; we cannot overwrite the attribute as we just updated the attribute above.
                    res: set[InstanceTypeAliases] = self.instance_conversion(instances=i.available_instances)
                    if isinstance(res, InstanceTypeAliases):
                        self.instances.add(res)
                    elif isinstance(res, set):
                        self.instances.update(res)

            return self.instances

        return result
