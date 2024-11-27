from typing import Any, Union

from .base import Base
from .dataclass import (
    ActionResult,
    Application,
    Controller,
    CreateInstance,
    Endpoints,
    Instance,
    InstanceDatastore,
    InstanceInfo,
    InstanceStatus,
    PortInfo,
    PostCreateActionsState,
    Provision,
    ProvisionSettingInfo,
    RemoteTargetInfo,
    RunningTask,
    Template,
)
from .modules import DeploymentTemplate

__all__ = ("ADSModule",)


class ADSModule(Base):
    """
    Contains the functions for any ``/API/ADSModule/`` API endpoints.


    .. warning::
        Do not change the :attr:`~ADSModule.module` attribute for any reason.


    .. note::
        Every function in this class requires the Instance type be of either :class:`AMPADSInstance`, :class:`ADSModule` or the :attr:`~ADSModule.module` attribute to be "ADS".\n
        If the ``format_data`` parameter is None on any function; the global ``FORMAT_DATA`` will be used instead.


    """

    module = "ADS"

    @Base.ads_only
    async def add_datastore(
        self,
        new_datastore: InstanceDatastore,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Add a new datastore.

        Parameters
        -----------
        new_datastore: :class:`InstanceDatastore`
            Your pre-created data structure to be parsed for the required API parameters.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()

        if isinstance(new_datastore, InstanceDatastore):
            data: dict[Any, Any] = self.dataclass_to_dict(dataclass_=new_datastore)

        parameters: dict[str, Union[dict[Any, Any], Any]] = {
            "newDatastore": data,
        }
        result: Any = await self._call_api(
            api="ADSModule/AddDatastore", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def apply_instance_configuration(
        self,
        instance_id: str,
        args: dict[str, str],
        rebuild_configuration: bool = False,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Apply an Instance configuration.

        .. warning::
            This Endpoint has not been fully tested, multiple parameters are unknown, or functionality is unknown.


        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        args: dict[:class:`str`, :class:`str`]
            UNK.
        rebuild_configuration: :class:`bool`, optional
            UNK, defaults to False.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, Any] = {"instanceId": instance_id, "args": args, "rebuildConfiguration": rebuild_configuration}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/ApplyInstanceConfiguration", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def apply_template(
        self, instance_id: str, template_id: int, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Overlays an existing template on an existing instance, used to perform package reconfigurations.

        .. warning::
            Do not use this to "transform" an existing application into another. The instance should be deleted and re-created in that situation.

        .. note::
            If you need to get an AMP Templates ID, use :meth:`get_deployment_templates` and access the :attr:`DeploymentTemplate.id` attribute.


        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID to apply the template to.
        template_id: :class:`int`
            The Template ID to apply.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"InstanceID": instance_id, "TemplateID": template_id}
        result: Any = await self._call_api(
            api="ADSModule/ApplyTemplate", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def attach_ads(
        self,
        friendly_name: str,
        instance_id: str,
        host: str,
        port: int,
        is_https: bool,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Attach an AMP Instance to the specified Target ADS name.

        Parameters
        -----------
        friendly_name: :class:`str`
            Name of the ADS.
        instance_id: :class:`str`
            The Instance ID of the Instance you want to attach to the ADS.
        host: :class:`str`
            The URL/URi to access the Instance.
        port: :class:`int`
            The Port you want to attach the Instance to.
        is_https: :class:`bool`
            To use HTTPS or not.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, Any] = {
            "friendly": friendly_name,
            "isHttps": is_https,
            "host": host,
            "port": port,
            "instanceId": instance_id,
        }
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/AttachADS", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def clone_template(self, template_id: int, name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Clone an existing AMP Deployment Template.

        .. note::
            If you need to get an AMP Templates ID, use :meth:`get_deployment_templates` and access the :attr:`DeploymentTemplate.id` attribute.


        Parameters
        -----------
        template_id: :class:`int`
            The Template ID to copy.
        name: :class:`str`
            The name for the newly cloned Template.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Id": template_id, "NewName": name}
        result: Any = await self._call_api(
            api="ADSModule/CloneTemplate", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def create_deployment_template(self, template_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Create a new Deployment Template. Typically used in conjunction with :meth:`update_deployment_template`.

        Parameters
        -----------
        template_name: :class:`str`
            The name for the newly created Template.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Name": template_name}
        result: Any = await self._call_api(
            api="ADSModule/CreateDeploymentTemplate", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def create_instance(self, instance: CreateInstance, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Create an AMP Instance.

        .. note::
            See the :class:`CreateInstance` for more details on how to configure the Instance when creating.


        Parameters
        -----------
        instance: :class:`CreateInstance`
            Your pre-created data structure to be parsed for the required API parameters.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        if isinstance(instance, CreateInstance):
            parameters: dict[Any, Any] = self.dataclass_to_dict(dataclass_=instance)

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/CreateInstance", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def create_local_instance(
        self,
        instance: CreateInstance,
        post_create: PostCreateActionsState = PostCreateActionsState.do_nothing,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Create a local AMP Instance, similar to :meth:`create_instance`. Use case could be on a remote Target ADS Instance instead of letting AMP decide where to create the Instance.

        .. note::
            See the :class:`CreateInstance` for more details on how to configure the Instance when creating.



        Parameters
        -----------
        instance: :class:`CreateInstance`
            Your pre-created data structure to be parsed for the required API parameters.
        post_create: :class:`PostCreateActions`, optional
            The action to take after creating the local instance, defaults to :attr:`~PostCreateActions.do_nothing`.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        if isinstance(instance, CreateInstance):
            data: dict[Any, Any] = self.dataclass_to_dict(dataclass_=instance)

        parameters: dict[str, Any] = {"instance": data, "postCreate": post_create}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/CreateLocalInstance", parameters=parameters, format_data=format_data, format_=ActionResult
        )

        return result

    @Base.ads_only
    async def delete_datastore(self, datastore_id: int, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Delete the specified Datastore by ID.

        .. note::
            You will need to know the Datastore ID you want to move the Instance ID to. See :func:`get_datastores` as a means to get the IDs.


        Parameters
        -----------
        datastore_id: :class:`int`
            The datastore ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Union[int, Any]] = {"id": datastore_id}
        result: Any = await self._call_api(
            api="ADSModule/DeleteDatastore", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def delete_deployment_template(self, template_id: int, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Delete an existing Deployment Template.

        .. note::
            If you need to get an AMP Templates ID, use :meth:`get_deployment_templates` and access the :attr:`DeploymentTemplate.id` attribute.


        Parameters
        -----------
        template_id: :class:`int`
            The Template id.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, int] = {"Id": template_id}
        result: Any = await self._call_api(
            api="ADSModule/DeleteDeploymentTemplate", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def delete_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> RunningTask:
        """|coro|

        Delete an Instance.

        .. note::
            The ``instance_name`` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        -----------
        instance_name: :class:`str`
            The Instance name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.
        """

        parameters: dict[str, str] = {"InstanceName": instance_name}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/DeleteInstance", parameters=parameters, format_data=format_data, format_=RunningTask
        )
        return result

    @Base.ads_only
    async def delete_instance_users(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Delete all Users from an Instance.

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {"InstanceId": instance_id}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/DeleteInstanceUsers", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def deploy_template(self, template: Template, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Deploy a Instance template.

        Parameters
        -----------
        template:  Union[:class:`Template`, None], optional
            Your pre-created data structure to be parsed for the required API parameters.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[Any, Any] = self.dataclass_to_dict(dataclass_=template)
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/DeployTemplate", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def detach_target(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        De-tach an Instance from the ADS.

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """

        parameters: dict[str, str] = {"id": instance_id}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/DetachTarget", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def extract_everywhere(self, source_archive: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Extracts everything from an archive.

        .. note::
            The parameter ``source_archive`` will be sanitized. See :meth:`~Base.sanitized_path`


        Parameters
        -----------
        source_archive: :class:`str`
            The source archive, typically a path to the archive.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {"SourceArchive": self.sanitize_path(path=source_archive)}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/ExtractEverywhere", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def get_application_endpoints(self, instance_id: str, format_data: Union[bool, None] = None) -> list[Endpoints]:
        """|coro|

        Get the application endpoints for the specified instance.

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`Endpoints`]
            Returns a list of endpoints for the specified instance.
        """

        parameters: dict[str, str] = {"instanceId": instance_id}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/GetApplicationEndpoints", parameters=parameters, format_data=format_data, format_=Endpoints
        )
        return result

    @Base.ads_only
    async def get_datastore(self, datastore_id: int, format_data: Union[bool, None] = None) -> InstanceDatastore:
        """|coro|

        Get the information for the specified datastore.

        .. note::
            You will need to know the Datastore ID you want to move the Instance ID to. See :func:`get_datastores` as a means to get the IDs.


        Parameters
        -----------
        datastore_id: :class:`int`
            The datastore ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`InstanceDataStore`
            On success returns an :class:`InstanceDataStore` dataclass.
        """

        parameters: dict[str, Union[Any, int]] = {"id": datastore_id}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/GetDatastore", parameters=parameters, format_data=format_data, format_=InstanceDatastore
        )
        return result

    @Base.ads_only
    async def get_datastores(self, format_data: Union[bool, None] = None) -> list[InstanceDatastore]:
        """|coro|

        Get a list of Datastores.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`DatastoreInstance`]
            On success returns a list of :class:`DatastoreInstance` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(api="ADSModule/GetDatastores", format_data=format_data, format_=InstanceDatastore)
        return result

    @Base.ads_only
    async def get_datastore_instances(self, datastore_id: int, format_data: Union[bool, None] = None) -> list[Instance]:
        """|coro|

        Get a list of Instances tied to the specified datastore.

        .. note::
            You will need to know the Datastore ID you want to move the Instance ID to. See :func:`get_datastores` as a means to get the IDs.


        Parameters
        -----------
        datastore_id: :class:`int`
            The datastore ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`Instance`]
            On success returns a list of :class:`Instance` dataclasses.
        """

        parameters: dict[str, Union[Any, int]] = {"datastoreId": datastore_id}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/GetDatastoreInstances", parameters=parameters, format_data=format_data, format_=Instance
        )
        return result

    @Base.ads_only
    async def get_deployment_templates(self, format_data: Union[bool, None] = None) -> list[DeploymentTemplate]:
        """|coro|

        Gets a list of Deployment Templates.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`DeploymentTemplate`]
            On success returns a list of :class:`DeploymentTemplate` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/GetDeploymentTemplates", format_data=format_data, format_=DeploymentTemplate
        )
        return result

    @Base.ads_only
    async def get_group(self, group_id: str, format_data: Union[bool, None] = None) -> dict:
        """|coro|

        Get the specified group.

        .. note::
            Unsure what this is used for or does. May return ADS information/Instances related to it.


        Parameters
        -----------
        group_id: :class:`str`
            The Group ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        dict
            On success returns an dictionary.
        """

        parameters: dict[str, str] = {"groupId": group_id}
        await self._connect()
        result: Any = await self._call_api("ADSModule/GetGroup", parameters, format_data=format_data)
        return result

    # @Base.ADSonly
    async def get_instance(self, instance_id: str, format_data: Union[bool, None] = None) -> Instance:
        """|coro|

        Returns the Instance information for the provided Instance ID.\n

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`Instance`
            On success returns a :class:`Instance` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"InstanceId": instance_id}
        result: Any = await self._call_api(
            api="ADSModule/GetInstance", parameters=parameters, format_data=format_data, format_=Instance
        )
        return result

    @Base.ads_only
    async def get_instances(
        self, include_self: bool = True, format_data: Union[bool, None] = None
    ) -> list[Union[Controller, Instance]]:
        """|coro|

        Returns a list of all Instances the Target ADS or Controller and AMP User has permission to access.\n

        .. note::
            If ``include_self`` is False; we force ``format_data = False``


        Parameters
        -----------
        include_self: :class:`bool`, optional
            Force include the Controller or Target ADS Instance in the results, by default True.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[Union[:class:`Controller`, :class:`Instance`]]
            If ``format_data`` or global ``FORMAT_DATA`` is True we return a :class:`Controller` dataclasses containing their :class:`Instance` dataclasses
            or if used on Target ADS Instance will return a list containing any combination of :class:`AMPADSInstance`, :class:`AMPMinecraftInstance` and :class:`AMPInstance` respectively.
        """
        await self._connect()
        parameters: dict[str, bool] = {"ForceIncludeSelf": include_self}

        if include_self is False:
            format_data = False

        result: Any = await self._call_api(
            api="ADSModule/GetInstances", parameters=parameters, format_data=format_data, format_=Controller
        )
        return result

    @Base.ads_only
    async def get_instance_network_info(self, instance_name: str, format_data: Union[bool, None] = None) -> list[PortInfo]:
        """|coro|

        Get the Port and or Network information of an Instance.

        .. note::
            The ``instance_name`` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        -----------
        instance_name: :class:`str`
            The name of the Instance we are targeting.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`PortInfo`]
            On success returns a list of :class:`PortInfo` dataclasses.
        """

        parameters: dict[str, str] = {"instanceName": instance_name}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/GetInstanceNetworkInfo", parameters=parameters, format_data=format_data, format_=PortInfo
        )
        return result

    @Base.ads_only
    async def get_instance_statuses(self, format_data: Union[bool, None] = None) -> list[InstanceStatus]:
        """|coro|

        Returns a dictionary of the Instance Status. \n

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`InstanceStatus`]
            On success returns a list of :class:`InstanceStatus` dataclasses.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/GetInstanceStatuses", format_data=format_data, format_=InstanceStatus
        )
        return result

    @Base.ads_only
    async def get_local_instances(self, format_data: Union[bool, None] = None) -> list[Instance]:
        """
        Gets the local instances related to the ADS or Controller.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`Instance`]
            On success returns a list of :class:`Instance` dataclasses.
        """
        await self._connect()
        result = await self._call_api(api="ADSModule/GetLocalInstances", format_data=format_data, format_=Instance)
        return result

    @Base.ads_only
    async def get_provision_arguments(
        self, module_name: str, format_data: Union[bool, None] = None
    ) -> list[ProvisionSettingInfo]:
        """|coro|

        Get Provision Arguments.

        Parameters
        -----------
        module_name: :class:`str`
            The Module Name (eg. "Minecraft")
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`ProvisionSettingInfo`]
            On success returns a list of :class:`ProvisionSettingInfo` dataclasses.
        """

        parameters: dict[str, str] = {"ModuleName": module_name}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/GetProvisionArguments",
            parameters=parameters,
            format_data=format_data,
            format_=ProvisionSettingInfo,
        )
        return result

    @Base.ads_only
    async def get_provision_fitness(self, format_data: Union[bool, None] = None) -> Provision:
        """|coro|

        Get the provision fitness of the ADS or Controller.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`Provision`
            On success returns a :class:`Provision` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="ADSModule/GetProvisionFitness", format_data=format_data, format_=Provision)
        return result

    @Base.ads_only
    async def get_supported_applications(self, format_data: Union[bool, None] = None) -> list[Application]:
        """|coro|

        Get supported applications, such as :class:`Template` information and the list of :class:`Applications` when creating an Instance.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`Application`]
            Returns a list of all applications that can be deployed.
        """
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/GetSupportedApplications", format_data=format_data, format_=Application
        )
        return result

    @Base.ads_only
    async def get_target_info(self, format_data: Union[bool, None] = None) -> RemoteTargetInfo:
        """|coro|

        Get target info.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RemoteTargetInfo`
            On success returns a :class:`RemoteTargetInfo` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(api="ADSModule/GetTargetInfo", format_data=format_data, format_=RemoteTargetInfo)
        return result

    @Base.ads_only
    async def handout_instance_configs(
        self, module: str, setting_node: str, values: list[str], format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Handout Instance Configuration.

        Parameters
        -----------
        module: :class:`str`
            The Module Name. eg. "Minecraft"
        setting_node: :class:`str`
            A setting node. See "./docs/setting_nodes.md"
        values: list[:class:`str`]
            The values for the setting node.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, Any] = {"ForModule": module, "SettingNode": setting_node, "Values": values}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/HandoutInstanceConfigs", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def manage_instance(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Manage the specified instance.

        .. note::
            Actual usage unknown, may be used for AMP instance management via the web interface.


        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {"instanceId": instance_id}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/ManageInstance", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def modify_custom_firewall_rule(
        self,
        instance_id: str,
        port_number: int,
        range_: int,
        protocol: int,
        description: str,
        open_: bool = True,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Modify the Firewall Rule of the specified instance.

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        port_number: :class:`int`
            Port number.
        range_: :class:`int`
            Port range.
        protocol: :class:`int`
            UDP/TCP/Both.
        description: :class:`str`
            Description for which the rule is applied.
        open_: :class:`bool`, optional
            Open or close the port mapping, by default True
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """
        parameters: dict[str, Any] = {
            "instanceId": instance_id,
            "portNumber": port_number,
            "range": range_,
            "protocol": protocol,
            "description": description,
            "open": open_,
        }

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/ModifyCustomFirewallRule", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def move_instance_datastore(
        self,
        instance_id: str,
        datastore_id: int,
        format_data: Union[bool, None] = None,
    ) -> RunningTask:
        """|coro|

        Move an Instance to a different Datastore.

        .. note::
            You will need to know the Datastore ID you want to move the Instance ID to. See :func:`get_datastores` as a means to get the IDs.


        Parameters
        -----------
        instance_id (str):
            The Instance ID to move.
        datastore_id: :class:`int`
            The ID of the datastore to move the Instance to.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"instanceId": instance_id, "datastoreId": datastore_id}
        result: Any = await self._call_api(
            api="ADSModule/MoveInstanceDatastore", parameters=parameters, format_data=format_data, format_=RunningTask
        )
        return result

    async def reactivate_instance(self, instance_id: str, format_data: Union[bool, None] = None) -> RunningTask:
        parameters: dict[str, str] = {"instanceId": instance_id}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/ReactivateInstance", parameters=parameters, format_data=format_data, format_=RunningTask
        )
        return result

    @Base.ads_only
    async def reactivate_local_instances(self, format_data: Union[bool, None] = None) -> RunningTask:
        """|coro|

        Reactivate local instances.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.
        """

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/ReactivateLocalInstances", format_data=format_data, format_=RunningTask
        )
        return result

    @Base.ads_only
    async def refresh_app_cache(self) -> None:
        """|coro|

        Refresh the application cache.

        Returns
        --------
        None
        """

        await self._connect()
        await self._call_api(api="ADSModule/RefreshAppCache", _no_data=True)
        return

    @Base.ads_only
    async def refresh_group(self, group_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Refresh the specified group.

        Parameters
        -----------
        group_id: :class:`str`
            The Group ID to refresh.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {"groupId": group_id}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/RefreshGroup", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def refresh_instance_config(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Refresh an Instance Configuration.

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {"InstanceId": instance_id}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/RefreshInstanceConfig", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def refresh_remote_config_stores(self, force: bool = False) -> None:
        """|coro|

        Refresh remote config stores.

        Parameters
        -----------
        force: :class:`bool`, optional
            Force refresh, defaults to False.

        Returns
        --------
        None
        """

        parameters: dict[str, bool] = {"force": force}

        await self._connect()
        await self._call_api(api="ADSModule/RefreshRemoteConfigStores", parameters=parameters, _no_data=True)
        return

    @Base.ads_only
    async def register_target(
        self,
        controller_url: str,
        my_url: str,
        username: str,
        password: str,
        friendly_name: str,
        two_factor_token: str = "",
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Registers a Target to a Controller.

        Parameters
        -----------
        controller_url: :class:`str`
            The Controller panel url.
        my_url: :class:`str`
            The Target AMP panel url.
        username: :class:`str`
            The username for logging into the Target AMP panel.
        password: :class:`str`
            The password for logging into the Target AMP panel.
        friendly_name: :class:`str`
            Instance Friendly Name.
        two_factor_token: :class:`str`
            The two-factor authentication token for the username. Defaults to ""
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {
            "controllerUrl": controller_url,
            "myUrl": my_url,
            "username": username,
            "password": password,
            "twoFactorToken": two_factor_token,
            "friendlyName": friendly_name,
        }
        await self._connect()
        result = await self._call_api(
            api="ADSModule/RegisterTarget", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def repair_datastore(self, datastore_id: int, format_data: Union[bool, None] = None) -> RunningTask:
        """|coro|

        Repair the specified datastore.

        .. note::
            You will need to know the Datastore ID you want to move the Instance ID to. See :func:`get_datastores` as a means to get the IDs.


        Parameters
        -----------
        datastore_id (int):
            The datastore ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.
        """

        parameters: dict[str, Union[Any, int]] = {"id": datastore_id}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/RepairDatastore", parameters=parameters, format_data=format_data, format_=RunningTask
        )
        return result

    @Base.ads_only
    async def request_datastore_size_calculation(
        self, datastore_id: int, format_data: Union[bool, None] = None
    ) -> RunningTask:
        """|coro|

        Request a calculation of the size of the specified Datastore.

        .. note::
            You will need to know the Datastore ID you want to move the Instance ID to. See :func:`get_datastores` as a means to get the IDs.


        Parameters
        -----------
        datastore_id (int):
            The datastore ID.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.
        """

        parameters: dict[str, Union[Any, int]] = {"datastoreId": datastore_id}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/RequestDatastoreSizeCalculation",
            parameters=parameters,
            format_data=format_data,
            format_=RunningTask,
        )
        return result

    @Base.ads_only
    async def restart_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Restart an Instance.

        .. note::
            The ``instance_name`` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        -----------
        instance_name: :class:`str`
            The Instance Name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        -------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {"InstanceName": instance_name}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/RestartInstance", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def servers(self, id_: str, req_rawjson: str = "application/json", format_data: Union[bool, None] = None) -> Any:
        """|coro|

        Used for proxy authentication.

        .. warning::
            This Endpoint has not been fully tested, multiple parameters are unknown, or functionality is unknown.


        Parameters
        -----------
        id_ : str
            The Instance ID.
        req_rawjson : str, optional
            The data type, by default "application/json"
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        Any
            UNK.
        """
        parameters: dict[str, str] = {"id": id_, "REQ_RAWJSON": req_rawjson}

        await self._connect()
        result: Any = await self._call_api(api="ADSModule/Servers", parameters=parameters, format_data=format_data)
        return result

    @Base.ads_only
    async def set_instance_network_info(
        self, instance_id: str, port_mappings: dict[str, int], format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Set the Port mappings for an Instance.

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID.
        port_mappings: dict[:class:`str`, :class:`int`]
            Port ranges and protocols to map.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, Any] = {"instanceId": instance_id, "portMappings": port_mappings}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/SetInstanceNetworkInfo", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def set_instance_config(
        self, instance_name: str, setting_node: str, value: str, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Set an :class:`AMPInstance` Setting Node setting.

        .. note::
            See `../nodes/setting_nodes.md` for possible ``setting_node`` values.


        .. note::
            The ``instance_name`` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        -----------
        instance_name: :class:`str`
            The Instance name.
        setting_node: :class:`str`
            The setting node name.
        value: :class:`str`
            The value for the setting node.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """

        parameters: dict[str, str] = {"InstanceName": instance_name, "SettingNode": setting_node, "Value": value}
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/SetInstanceConfig", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def set_instance_suspended(
        self, instance_name: str, suspended: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Set an Instances suspended State.

        .. note::
            The ``instance_name`` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        -----------
        instance_name: :class:`str`
            The Instance name.
        suspended: :class:`bool`
            Set the instance to be suspended, default False.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        parameters: dict[str, Any] = {"InstanceName": instance_name, "Suspended": suspended}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/SetInstanceSuspended", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def start_all_instances(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Start all Instances.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """
        parameters: dict[str, str] = {"TargetADSInstance": instance_id}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/StartAllInstances", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def start_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Start an Instance.

        .. note::
            The ``instance_name`` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        -----------
        instance_name: :class:`str`
            The Instance name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {"InstanceName": instance_name}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/StartInstance", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def stop_all_instances(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Stop all Instances.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """
        parameters: dict[str, str] = {"TargetADSInstance": instance_id}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/StopAllInstances", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def stop_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Stop an Instance.

        .. note::
            The ``instance_name`` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        ----------
        instance_name :
            The Instance name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """

        parameters: dict[str, str] = {"InstanceName": instance_name}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/StopInstance", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def update_datastore(
        self,
        updated_datastore: InstanceDatastore,
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Update an existing datastore.

        Parameters
        -----------
        updated_datastore: :class:`InstanceDatastore`
            Your pre-created data structure to be parsed for the required API parameters.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """
        await self._connect()

        if isinstance(updated_datastore, InstanceDatastore):
            data: dict[Any, Any] = self.dataclass_to_dict(dataclass_=updated_datastore)

        parameters: dict[str, Union[Any, dict[Any, Any]]] = {
            "updatedDatastore": data,
        }
        result: Any = await self._call_api(
            api="ADSModule/UpdateDatastore", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def update_deployment_template(
        self, template_to_update: DeploymentTemplate, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Update an existing Deployment Template.

        Parameters
        -----------
        template_to_update : :class:`DeploymentTemplate`
            Your pre-created data structure to be parsed for the required API parameters.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        await self._connect()
        if isinstance(template_to_update, DeploymentTemplate):
            data: dict[Any, Any] = template_to_update.to_dict()

        parameters: dict[str, dict[Any, Any]] = {"templateToUpdate": data}
        result: Any = await self._call_api(
            api="ADSModule/UpdateDeploymentTemplate", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def update_instance_info(self, instance_info: InstanceInfo, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update an Instances info.

        Parameters
        -----------
        instance_info: :class:`InstanceInfo`
            Your pre-created data structure to be parsed for the required API parameters.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """

        if isinstance(instance_info, InstanceInfo):
            parameters: dict[Any, Any] = self.dataclass_to_dict(dataclass_=instance_info)

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/UpdateInstanceInfo", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def update_target(self, target_id: str) -> None:
        """|coro|

        Update Target ADS Instance.

        .. note::
            Typically this will be used on Instances with a the :attr:`~Instance.module` == "ADS"


        Parameters
        -----------
        target_id: :class:`str`
            The Target Instance ID.

        Returns
        --------
        None
        """

        parameters: dict[str, str] = {"TargetID": target_id}

        await self._connect()
        await self._call_api(api="ADSModule/UpdateTarget", parameters=parameters, _no_data=True)
        return

    @Base.ads_only
    async def update_target_info(
        self,
        instance_id: str,
        friendly_name: str,
        url: str,
        description: str,
        tags: list[str],
        format_data: Union[bool, None] = None,
    ) -> ActionResult:
        """|coro|

        Update a target Instance information.

        Parameters
        -----------
        instance_id: :class:`str`
            The Instance ID for the Instance you want to update.
        friendly_name: :class:`str`
            The Instance friendly name you want to set.
        url: :class:`str`
            The Instance URL you want to set.
        description (str): The description for the Instance.
        tags: list[:class:`str`]
            The tags you want to add to the Instance.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, Any] = {
            "id": instance_id,
            "friendlyName": friendly_name,
            "url": url,
            "description": description,
            "tags": tags,
        }
        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/UpdateTargetInfo", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def upgrade_all_instances(
        self, instance_id: str, restart_running: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Upgrade all Instances.

        Parameters
        -----------
        restart_running: :class:`bool`
            Restart any running Instances, default is False.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, Union[str, bool]] = {"RestartRunning": restart_running, "TargetADSInstance": instance_id}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/UpgradeAllInstances", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    @Base.ads_only
    async def upgrade_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Update or Upgrade the Instance

        .. note::
            The ``instance_name`` parameter is referring to :attr:`~Instance.instance_name` attribute of an Instance.


        Parameters
        -----------
        instance_name: :class:`str`
            The Instance name.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        parameters: dict[str, str] = {"InstanceName": instance_name}

        await self._connect()
        result: Any = await self._call_api(
            api="ADSModule/UpgradeInstance", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result
