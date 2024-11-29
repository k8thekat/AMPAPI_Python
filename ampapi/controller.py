from collections.abc import Iterable
from dataclasses import fields
from typing import Any, Union

from .adsmodule import ADSModule
from .core import Core
from .dataclass import Controller, Instance
from .emailsender import EmailSenderPlugin
from .filemanager import FileManagerPlugin
from .instance import AMPADSInstance, AMPInstance, AMPMinecraftInstance

__all__ = ("AMPControllerInstance",)


class AMPControllerInstance(ADSModule, Core, EmailSenderPlugin, FileManagerPlugin, Controller):
    """
    The AMPControllerInstance class is the top most level of Instances inside of AMP. This has access the Target ADS and all Instances it can see.\n

    .. note::
        All API Endpoints an AMP Controller Instance would have access to this class object does too.


    """

    _controller_exists: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.module: str = "ADS"

    def __getattr__(self, name: str) -> Union[AttributeError, Any]:
        if name in [field.name for field in fields(class_or_instance=Controller)] and self._controller_exists is False:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}' | You must call <AMPControllerInstance>.get_instances() with 'format_data=True' to update this object."
            )
        return self.__getattribute__(name)

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
        self._instances: set[Union[AMPInstance, AMPMinecraftInstance, AMPADSInstance]] = self.instance_conversion(
            instances=self.available_instances
        )

    def instance_conversion(
        self, instances: Iterable[Instance]
    ) -> set[Union[AMPInstance, AMPMinecraftInstance, AMPADSInstance]]:
        """
        Takes a set of :class:`Instance` dataclasses and turns them into :class:`AMPInstance`, :class:`AMPMinecraftInstance` and or :class:`AMPADSInstance` respectively to facilitate API function accessibility.

        .. note::
            By default the list of instances will be sorted.


        Parameters
        -----------
        instances: Iterable[:class:`Instance`]
            An Iterable of :class:`Instance` dataclasses.

        Returns
        --------
        set[Union[:class:`AMPInstance`, :class:`AMPMinecraftInstance`, :class:`AMPADSInstance`]]
            The set of converted :class:`Instance` objects.
        """
        instances = sorted(instances)
        conv_instances: set[Union[AMPInstance, AMPMinecraftInstance, AMPADSInstance]] = set()
        if isinstance(instances, list) and len(instances) > 0:
            for entry in instances:
                if entry.module == "ADS":
                    conv_instances.add(AMPADSInstance(data=entry, controller=self))

                elif entry.module == "Minecraft":
                    conv_instances.add(AMPMinecraftInstance(data=entry, controller=self))

                else:
                    conv_instances.add(AMPInstance(data=entry, controller=self))
        return conv_instances

    async def get_instances(
        self, include_self: bool = True, format_data: Union[bool, None] = None
    ) -> Union[set[Union[AMPInstance, AMPMinecraftInstance, AMPADSInstance]], Iterable[Union[Controller, Instance]]]:
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
        result: list[Union[Controller, Instance]] = await super().get_instances(
            include_self=include_self, format_data=format_data
        )

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
                    self.instances.update(self.instance_conversion(instances=i.available_instances))

            return self.instances

        return result
