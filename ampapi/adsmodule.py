from __future__ import annotations

from typing import Union

from .base import Base
from .types import *

__all__ = ("ADSModule",)


class ADSModule(Base):
    """
    Contains the base functions for any `/API/ADSModule/` AMP API endpoints.

    """

    # ADSModule.AddDatastore:({'Parameters': [{'Name': 'newDatastore', 'TypeName': 'InstanceDatastore', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def add_datastore(self, new_datastore: InstanceDatastore, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Add a new datastore.
        **Requires ADS**

        Args:
        ---
            new_datastore (InstanceDatastore): InstanceDatastore dataclass. See `types.py -> InstanceDatastore`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None) 
        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()

        if isinstance(new_datastore, InstanceDatastore):
            data: dict[Any, Any] = self.dataclass_to_dict(dataclass=new_datastore)

        parameters: dict[str, dict[Any, Any]] = {
            "newDatastore": data
        }
        result: Any = await self._call_api(api="ADSModule/AddDatastore", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.DeleteDatastore:({'Parameters': [{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def delete_datastore(self, datastore_id: int, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete a datastore.
        **Requires ADS**

        Args:
        ---
            datastore_id (int): The datastore ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass. 
            * See `types.py -> ActionResult`

        """

        await self._connect()
        parameters: dict[str, int] = {
            "id": datastore_id
        }
        result: Any = await self._call_api(api="ADSModule/DeleteDatastore", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.UpdateDatastore:({'Parameters': [{'Name': 'updatedDatastore', 'TypeName': 'InstanceDatastore', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def update_datastore(self, updated_datastore: InstanceDatastore, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update an existing datastore.
        **Requires ADS**

        Args:
        ---
            updated_datastore (InstanceDatastore): The updated datastore. See `types.py -> InstanceDatastore`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()

        if isinstance(updated_datastore, InstanceDatastore):
            data: dict[Any, Any] = self.dataclass_to_dict(dataclass=updated_datastore)

        parameters: dict[str, dict[Any, Any]] = {
            "updatedDatastore": data
        }
        result: Any = await self._call_api(api="ADSModule/UpdateDatastore", parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.GetDatastores:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_datastores(self, format_data: Union[bool, None] = None) -> list[InstanceDatastore]:
        """
        Get a list of Datastores.
        **Requires ADS**

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
           list[DatastoreInstance]: On success returns a list of DatastoreInstance dataclasses.
            * See `types.py -> DatastoreInstance`
        """

        await self._connect()
        result: Any = await self._call_api(api="ADSModule/GetDatastores", format_data=format_data, format=InstanceDatastore)
        return result

    # ADSModule.RequestDatastoreSizeCalculation:({'Parameters': [{'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    @Base.ADSonly
    async def request_datastore_size_calculation(self, datastore_id: int, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Request a calculation of the size of the specified datastore.
        **Requires ADS**

        Args:
        ---
            datastore_id (int): The datastore ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            RunningTask: On success returns a RunningTask dataclass.
            * See `types.py -> RunningTask`
        """

        parameters: dict[str, int] = {
            "datastoreId": datastore_id
        }

        await self._connect()
        result: Any = await self._call_api(api="ADSModule/RequestDatastoreSizeCalculation", parameters=parameters, format_data=format_data, format=RunningTask)
        return result

    # ADSModule.GetDatastore:({'Parameters': [{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    @Base.ADSonly
    async def get_datastore(self, datastore_id: int, format_data: Union[bool, None] = None) -> InstanceDatastore:
        """
        Get the information for the specified datastore.
        **Requires ADS**

        Args:
        ---
            datastore_id (int): The datastore ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            InstanceDataStore: On success returns an InstanceDataStore dataclass.
            * See `types.py -> InstanceDataStore`
        """

        parameters: dict[str, int] = {
            "id": datastore_id
        }

        await self._connect()
        result: Any = await self._call_api(api="ADSModule/GetDatastore", parameters=parameters, format_data=format_data, format=InstanceDatastore)
        return result

    # ADSModule.RepairDatastore:({'Parameters': [{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    @Base.ADSonly
    async def repair_datastore(self, datastore_id: int, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Repair the specified datastore.
        **Requires ADS**

        Args:
        ---
            datastore_id (int): The datastore ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            RunningTask: On success returns a RunningTask dataclass.
            * See `types.py -> RunningTask`
        """

        parameters: dict[str, int] = {
            "id": datastore_id
        }
        await self._connect()
        result: Any = await self._call_api(api="ADSModule/RepairDatastore", parameters=parameters, format_data=format_data, format=RunningTask)
        return result

    # ADSModule.GetDatastoreInstances:({'Parameters': [{'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_datastore_instances(self, datastore_id: int, format_data: Union[bool, None] = None) -> list[Instance]:
        """
        Get a list of Instances tied to the specified datastore.
        **Requires ADS**

        Args:
        ---
            datastore_id (int): The datastore ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)


        Returns:
        ---
            list[Instance]: On success returns a list of Instance dataclasses.
            * See `types.py -> Instance`
        """

        parameters: dict[str, int] = {
            "datastoreId": datastore_id
        }
        await self._connect()
        result: Any = await self._call_api(api="ADSModule/GetDatastoreInstances", parameters=parameters, format_data=format_data, format=Instance)
        return result

    # ADSModule.MoveInstanceDatastore:({'Parameters': [{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    @Base.ADSonly
    async def move_instance_datastore(self, instance_id: str, datastore_id: int, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Move an Instance to a different datastore.
        **Requires ADS**

        Args:
        ---
            instance_id (str): The Instance ID to move.
            datastore_id (int): The datastore ID to move the Instance to.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            RunningTask: On success returns a RunningTask dataclass.
            * See `types.py -> RunningTask`
        """

        await self._connect()
        parameters: dict[str, Any] = {
            "instanceId": instance_id,
            "datastoreId": datastore_id
        }
        result: Any = await self._call_api(api="ADSModule/MoveInstanceDatastore", parameters=parameters, format_data=format_data, format=RunningTask)
        return result

    # ADSModule.GetInstance:({'Parameters': [{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    @Base.ADSonly
    async def get_instance(self, instance_id: str, format_data: Union[bool, None] = None) -> Instance:
        """
        Returns the Instance information for the provided Instance ID.\n
        **Requires ADS**

        Args:
        ---
            instance_id (str): The Instance ID to get information for.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            Instance | str | bool | int | None: On success returns a Instance dataclass. 
            * See `types.py -> Instance`
        """

        await self._connect()
        parameters: dict[str, str] = {
            "InstanceId": instance_id
        }
        result: Any = await self._call_api(api="ADSModule/GetInstance", parameters=parameters, format_data=format_data, format=Instance)
        return result

    # ADSModule.GetInstances:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_instances(self, format_data: Union[bool, None] = None) -> list[Controller]:
        """
        Returns a list of all Instances on the AMP Panel.\n
        **Requires ADS**

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[Controller] | str | bool | int | None: On success returns a list of Controller dataclasses. 
            * See `types.py -> Controller`
        """

        await self._connect()
        result: Any = await self._call_api(api="ADSModule/GetInstances", format_data=format_data, format=Controller)
        return result

    # ADSModule.GetInstanceStatuses:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_instance_statuses(self, format_data: Union[bool, None] = None) -> list[InstanceStatus]:
        """
        Returns a dictionary of the Server/Instance Status. \n
        **Requires ADS**

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)


        Returns:
        ---
            list[InstanceStatus]: On success returns a list of InstanceStatus dataclasses.
            * See `types.py -> InstanceStatus`

        """

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/GetInstanceStatuses', format_data=format_data, format=InstanceStatus)
        return result

    # ADSModule.GetDeploymentTemplates:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_deployment_templates(self, format_data: Union[bool, None] = None) -> list[DeploymentTemplate]:
        """
        Gets a list of Deployment Templates.
        **Requires ADS**

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[DeploymentTemplate]: On success returns a list of DeploymentTemplate dataclasses.
            * See `types.py -> DeploymentTemplate`
        """

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/GetDeploymentTemplates', format_data=format_data, format=DeploymentTemplate)
        return result

    # ADSModule.CreateDeploymentTemplate:({'Parameters': [{'Name': 'Name', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def create_deployment_template(self, template_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Create a new Deployment Template. Typically used in conjunction with `update_deployment_template()`.
        **Requires ADS**

        Args:
        ---
            template_name (str): Template name.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        parameters: dict[str, str] = {
            "Name": template_name
        }
        result: Any = await self._call_api(api='ADSModule/CreateDeploymentTemplate', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.UpdateDeploymentTemplate:({'Parameters': [{'Name': 'templateToUpdate', 'TypeName': 'DeploymentTemplate', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def update_deployment_template(self, template_to_update: DeploymentTemplate, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update an existing Deployment Template.
        **Requires ADS**

        Args:
        ---
            template_name (str): Template name.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        if isinstance(template_to_update, DeploymentTemplate):
            data: dict[Any, Any] = self.dataclass_to_dict(dataclass=template_to_update)

        parameters: dict[str, dict[Any, Any]] = {
            "templateToUpdate": data
        }
        result: Any = await self._call_api(api='ADSModule/UpdateDeploymentTemplate', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.DeleteDeploymentTemplate:({'Parameters': [{'Name': 'Id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def delete_deployment_template(self, template_id: int, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete an existing Deployment Template.
        **Requires ADS**

        Args:
        ---
            template_id (int): Template ID
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        parameters: dict[str, int] = {
            "Id": template_id
        }
        result: Any = await self._call_api(api='ADSModule/DeleteDeploymentTemplate', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.CloneTemplate:({'Parameters': [{'Name': 'Id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'NewName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def clone_template(self, template_id: int, new_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Clone an existing Template.
        **Requires ADS**

        Args:
        ---
            template_id (int): Template ID.
            new_name (str): New Template name.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        parameters: dict[str, Any] = {
            "Id": template_id,
            "NewName": new_name
        }
        result: Any = await self._call_api(api='ADSModule/CloneTemplate', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.ApplyTemplate:({'Description': "Overlays an existing template on an existing instance. Used to perform package reconfigurations. Do not use this to 'transform' an existing application into another. The instance should be deleted and re-created in that situation.", 'Returns': '', 'Parameters': [{'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'TemplateID', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'NewFriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': True}, {'Name': 'Secret', 'TypeName': 'String', 'Description': '', 'Optional': True}, {'Name': 'RestartIfPreviouslyRunning', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def apply_template(self, instance_id: str, template_id: int, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Overlays an existing template on an existing instance. 
        Used to perform package reconfigurations. 
        **Requires ADS**

        `**Do not use this to 'transform' an existing application into another. The instance should be deleted and re-created in that situation.**`

        Args:
        ---
            instance_id (str): The Instance ID to apply the template to.
            template_id (int): The Template ID to apply.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        parameters: dict[str, Any] = {
            "InstanceID": instance_id,
            "TemplateID": template_id
        }
        result: Any = await self._call_api(api='ADSModule/ApplyTemplate', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.DeployTemplate:({'Parameters': [{'Name': 'TemplateID', 'TypeName': 'Int32', 'Description': 'The ID of the template to be deployed, as per the Template Management UI in AMP itself.', 'Optional': False}, {'Name': 'NewUsername', 'TypeName': 'String', 'Description': 'If specified, AMP will create a new user with this name for this instance. Must be unique. If this user already exists, this will be ignored but the new instance will be assigned to this user.', 'Optional': True}, {'Name': 'NewPassword', 'TypeName': 'String', 'Description': "If 'NewUsername' is specified and the user doesn't already exist, the password that will be assigned to this user.", 'Optional': True}, {'Name': 'NewEmail', 'TypeName': 'String', 'Description': "If 'NewUsername' is specified and the user doesn't already exist, the email address that will be assigned to this user.", 'Optional': True}, {'Name': 'RequiredTags', 'TypeName': 'List<String>', 'Description': "If specified, AMP will only deploy this template to targets that have every single 'tag' specified in their target configuration. You can adjust this via the controller by clicking 'Edit' on the target settings.", 'Optional': True}, {'Name': 'Tag', 'TypeName': 'String', 'Description': "Unrelated to RequiredTags. This is to uniquely identify this instance to your own systems. It may be something like an order ID or service ID so you can find the associated instance again at a later time. If 'UseTagAsInstanceName' is enabled, then this will also be used as the instance name for the created instance - but it must be unique.", 'Optional': True}, {'Name': 'FriendlyName', 'TypeName': 'String', 'Description': 'A friendly name for this instance. If left blank, AMP will generate one for you.', 'Optional': True}, {'Name': 'Secret', 'TypeName': 'String', 'Description': 'Must be a non-empty strong in order to get a callback on deployment state change. This secret will be passed back to you in the callback so you can verify the request.', 'Optional': True}, {'Name': 'PostCreate', 'TypeName': 'PostCreateActions', 'Description': '0: Do nothing, 1: Start instance only, 2: Start instance and update application, 3: Full application startup.', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'StartInstance': 1, 'StartAndUpdate': 2, 'FullStartup': 3, 'EveryTime': 16}}, {'Name': 'ExtraProvisionSettings', 'TypeName': 'Dictionary<String, String>', 'Description': 'A dictionary of setting nodes and values to create the new instance with. Identical in function to the provisioning arguments in the template itself.', 'Optional': True}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    @Base.ADSonly
    async def deploy_template(self, template: Template, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Deploy a Instance template.
        **Requires ADS**

        Args:
        ---
            template (Template | None, optional): The Template to deploy. See `types.py -> Template`.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`.
        """

        parameters: dict[Any, Any] = self.dataclass_to_dict(dataclass=template)
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/DeployTemplate', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.GetTargetInfo:({'Parameters': [], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    @Base.ADSonly
    async def get_target_info(self, format_data: Union[bool, None] = None) -> RemoteTargetInfo:
        """
        Get target info.
        **Requires ADS**

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            RemoteTargetInfo: On success returns a RemoteTargetInfo dataclass.
            * See `types.py -> RemoteTargetInfo`.
        """

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/GetTargetInfo', format_data=format_data, format=RemoteTargetInfo)
        return result

    # ADSModule.GetSupportedApplications:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_supported_applications(self, format_data: Union[bool, None] = None) -> list[Application]:
        """
        Get supported applications.
        **Requires ADS**

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[dict[str, Any]] | str | dict[str, Any] | bool | int | None: Returns a list of all applications that can be deployed.

        """

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/GetSupportedApplications', format_data=format_data, format=Application)
        return result

    # ADSModule.RefreshAppCache:({'Parameters': [], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    @Base.ADSonly
    async def refresh_app_cache(self) -> None:
        """
        Refresh the application cache.

        Returns:
        ---
            None
        """

        await self._connect()
        await self._call_api(api='ADSModule/RefreshAppCache')
        return

    # ADSModule.RefreshRemoteConfigStores:({'Parameters': [{'Name': 'force', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    @Base.ADSonly
    async def refresh_remote_config_stores(self, force: bool = False) -> None:
        """
        Refresh remote config stores.

        Args:
        ---
            force (bool, optional): Force refresh. Defaults to False.
        """

        parameters: dict[str, bool] = {
            "force": force
        }

        await self._connect()
        await self._call_api(api='ADSModule/RefreshRemoteConfigStores', parameters=parameters)
        return

    # ADSModule.GetApplicationEndpoints:({'Parameters': [{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_application_endpoints(self, instance_id: str, format_data: Union[bool, None] = None) -> list[Endpoints]:
        """
        Get the application endpoints for the specified instance.

        Args:
        ---
            instance_id (str): Instance ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)


        Returns:
        ---
            list[Endpoints]: Returns a list of endpoints for the specified instance.
        """

        parameters: dict[str, str] = {
            "instanceId": instance_id
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/GetApplicationEndpoints', parameters=parameters, format_data=format_data, format=Endpoints)
        return result

    # ADSModule.ReactivateLocalInstances:({'Parameters': [], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    @Base.ADSonly
    async def reactivate_local_instances(self, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Reactivate local instances.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            RunningTask: On success returns a RunningTask dataclass.
            * See `types.py -> RunningTask`.
        """

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/ReactivateLocalInstances', format_data=format_data, format=RunningTask)
        return result

    # ADSModule.ModifyCustomFirewallRule:({'Parameters': [{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'PortNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'Range', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'Protocol', 'TypeName': 'PortProtocol', 'Description': '', 'Optional': False, 'ParamEnumValues': {'TCP': 0, 'UDP': 1, 'Both': 2}}, {'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Open', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def modify_custom_firewall_rule(self, instance_id: str, port_number: int, range: int, protocol: int, description: str, open: bool = True, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Modify the Firewall Rule of the specified instance.

        Args:
        ---
            instance_id (str): The Instance ID.
            port_number (int): Port number.
            range (int): Port range.
            protocol (int): UDP/TCP/Both.
            description (str): Description for which the rule is applied.
            open (bool): Open or close the port mapping. Defaults to True.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, Any] = {
            "instanceId": instance_id,
            "portNumber": port_number,
            "range": range,
            "protocol": protocol,
            "description": description,
            "open": open
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/ModifyCustomFirewallRule', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.ManageInstance:({'Parameters': [{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult<String>', 'IsComplexType': True})
    @Base.ADSonly
    async def manage_instance(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Manage the specified instance.\n
        *Note* May be used for AMP instance management via the web interface.

        Args:
        ---
            instance_id (str): The Instance ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass. 
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "instanceId": instance_id
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/ManageInstance', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.GetGroup:({'Parameters': [{'Name': 'GroupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    @Base.ADSonly
    async def get_group(self, group_id: str, format_data: Union[bool, None] = None) -> dict:
        """
        Get the specified group.
        *Note* Unsure what this is used for or does. May return ADS information/Instances related to it.

        Args:
        ---
            group_id (str): Group ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            dict: On success returns an dictionary.
        """

        parameters: dict[str, str] = {
            "groupId": group_id
        }
        await self._connect()
        result: Any = await self._call_api('ADSModule/GetGroup', parameters, format_data=format_data)
        return result

    # ADSModule.RefreshGroup:({'Parameters': [{'Name': 'GroupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def refresh_group(self, group_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Refresh the specified group.

        Args:
        ---
            group_id (str): Group ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "groupId": group_id
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/RefreshGroup', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.GetLocalInstances:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_local_instances(self, format_data: Union[bool, None] = None) -> list[Instance]:
        """
        Gets the local instances related to the ADS/Controller. 

        Returns:
        ---
            list[Instance]: Returns a list of Instance dataclass objects.
            * See `types.py -> Instance`
        """

        await self._connect()
        result = await self._call_api(api='ADSModule/GetLocalInstances', format_data=format_data, format=Instance)
        return result

    # ADSModule.GetProvisionFitness:({'Parameters': [], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    @Base.ADSonly
    async def get_provision_fitness(self, format_data: Union[bool, None] = None) -> Provision:
        """
        Get the provision fitness of the ADS/Controller.

        Returns:
        ---
            Provision: On success returns a Provision dataclass object.
            * See `types.py -> Provision`
        """

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/GetProvisionFitness', format_data=format_data, format=Provision)
        return result

    # ADSModule.AttachADS:({'Parameters': [{'Name': 'Friendly', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'IsHTTPS', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}, {'Name': 'Host', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Port', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def attach_ads(self, friendly: str, is_https: bool, host: str, port: int, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Attach an Instance to the ADS.


        Args:
        ---
            friendly (str): Name of the ADS.
            is_https (bool): To use HTTPS.
            host (str): URL/URi.
            port (int): Port.
            instance_id (str): Instance ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, Any] = {
            "friendly": friendly,
            "isHttps": is_https,
            "host": host,
            "port": port,
            "instanceId": instance_id
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/AttachADS', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.DetatchTarget:({'Parameters': [{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def detach_target(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        De-tach an Instance from the ADS.

        Args:
        ---
            instance_id (str): Instance ID.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "id": instance_id
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/DetachTarget', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.UpdateTargetInfo:({'Parameters': [{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Url', 'TypeName': 'Uri', 'Description': '', 'Optional': False}, {'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Tags', 'TypeName': 'List<String>', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def update_target_info(self, instance_id: str, friendly_name: str, url: str, description: str, tags: list[str], format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update a target Instance information.

        Args:
        ---
            instance_id (str): Instance ID.
            friendly_name (str): Instance Friendly Name.
            url (str): Instance URL.
            description (str): The description for the Instance.
            tags (list[str]): Tags.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, Any] = {
            "id": instance_id,
            "friendlyName": friendly_name,
            "url": url,
            "description": description,
            "tags": tags
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/UpdateTargetInfo', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.ConvertToManaged:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def convert_to_managed(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Convert an instance to managed.

        Args:
        ---
            instance_name (str): Instance name.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "instanceName": instance_name
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/ConvertToManaged', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.GetInstanceNetworkInfo:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_instance_network_info(self, instance_name: str, format_data: Union[bool, None] = None) -> list[PortInfo]:
        """
        Get the Port/Network information of an Instance.

        Args:
        ---
            instance_name (str): The Instance Name (NOT Friendly Name).
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[PortInfo]: On success returns a list of PortInfo dataclasses.
            * See `types.py -> PortInfo`
        """

        parameters: dict[str, str] = {
            "instanceName": instance_name
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/GetInstanceNetworkInfo', parameters=parameters, format_data=format_data, format=PortInfo)
        return result

    # ADSModule.SetInstanceNetworkInfo:({'Parameters': [{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'PortMappings', 'TypeName': 'Dictionary<String, Int32>', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def set_instance_network_info(self, instance_id: str, port_mappings: dict[str, int], format_data: Union[bool, None] = None) -> ActionResult:
        """
        Set the Port mappings for an Instance.

        Args:
        ---
            instance_id (str): The Instance ID.
            port_mappings (dict[str, int]): Port ranges and protocols to map.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, Any] = {
            "instanceId": instance_id,
            "portMappings": port_mappings
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/SetInstanceNetworkInfo', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.ApplyInstanceConfiguration:({'Parameters': [{'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'Args', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}, {'Name': 'RebuildConfiguration', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def apply_instance_configuration(self, instance_id: str, args: dict[str, str], rebuild_configuration: bool = False, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Apply an Instance configuration. 

        Args:
        ---
            instance_id (str): The Instance ID.
            args (dict[str, str]): UNK.
            rebuild_configuration (bool, optional): UNK. Defaults to False.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, Any] = {
            "instanceId": instance_id,
            "args": args,
            "rebuildConfiguration": rebuild_configuration
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/ApplyInstanceConfiguration', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.CreateLocalInstance:({'Parameters': [{'Name': 'Instance', 'TypeName': 'LocalAMPInstance', 'Description': '', 'Optional': False}, {'Name': 'PostCreate', 'TypeName': 'PostCreateActions', 'Description': '', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'StartInstance': 1, 'StartAndUpdate': 2, 'FullStartup': 3, 'EveryTime': 16}}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def create_local_instance(self, instance: CreateInstance, post_create: PostCreateActions = PostCreateActions.DoNothing, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Create a local AMP Instance.

        Args:
        ---
            instance (LocalAMPInstance): CreateInstance dataclass. See `types.py -> CreateInstance`
            post_create (PostCreateActions, optional): The action to take after creating the local instance. Defaults to PostCreateActions.DoNothing.
                See `types.py -> PostCreateActions`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        if isinstance(instance, CreateInstance):
            data: dict[Any, Any] = self.dataclass_to_dict(dataclass=instance)

        parameters: dict[str, Any] = {
            "instance": data,
            "postCreate": post_create
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/CreateLocalInstance', parameters=parameters, format_data=format_data, format=ActionResult)

        return result

    # ADSModule.CreateInstance:({'Parameters': [{'Name': 'TargetADSInstance', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'NewInstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'Module', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'IPBinding', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'PortNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'AdminUsername', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'AdminPassword', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'ProvisionSettings', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}, {'Name': 'AutoConfigure', 'TypeName': 'Boolean', 'Description': 'When enabled, all settings other than the Module, Target and FriendlyName are ignored and replaced with automatically generated values.', 'Optional': True}, {'Name': 'PostCreate', 'TypeName': 'PostCreateActions', 'Description': '', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'StartInstance': 1, 'StartAndUpdate': 2, 'FullStartup': 3, 'EveryTime': 16}}, {'Name': 'StartOnBoot', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}, {'Name': 'DisplayImageSource', 'TypeName': 'String', 'Description': '', 'Optional': True}, {'Name': 'TargetDatastore', 'TypeName': 'Int32', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def create_instance(self, instance: CreateInstance, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Create an AMP Instance.

        Args:
        ---
            instance (CreateInstance): A CreateInstance dataclass. See `types.py -> CreateInstance`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        if isinstance(instance, CreateInstance):
            parameters: dict[Any, Any] = self.dataclass_to_dict(dataclass=instance)

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/CreateInstance', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.SetInstanceConfig:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Value', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def set_instance_config(self, instance_name: str, setting_node: str, value: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Set an Instance Configuration.

        Args:
        ---
            instance_name (str): The Instance Name
            setting_node (str): A setting node. See "./docs/setting_nodes.md"
            value (str): The value for the setting node.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "InstanceName": instance_name,
            "SettingNode": setting_node,
            "Value": value
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/SetInstanceConfig', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.RefreshInstanceConfig:({'Parameters': [{'Name': 'InstanceId', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def refresh_instance_config(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Refresh an Instance Configuration.

        Args:
            instance_id (str): The Instance ID
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "InstanceId": instance_id
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/RefreshInstanceConfig', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.HandoutInstanceConfigs:({'Parameters': [{'Name': 'ForModule', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Values', 'TypeName': 'List<String>', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def handout_instance_configs(self, for_module: str, setting_node: str, values: list[str], format_data: Union[bool, None] = None) -> ActionResult:
        """
        Handout Instance Configuration.

        Args:
        ---
            for_module (str): The Module Name. eg. "Minecraft"
            setting_node (str): A setting node. See "./docs/setting_nodes.md"
            values (list[str]): The values for the setting node.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, Any] = {
            "ForModule": for_module,
            "SettingNode": setting_node,
            "Values": values
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/HandoutInstanceConfigs', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.GetProvisionArguments:({'Parameters': [{'Name': 'ModuleName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'IEnumerable<ProvisionSettingInfo>', 'IsComplexType': True})
    @Base.ADSonly
    async def get_provision_arguments(self, module_name: str, format_data: Union[bool, None] = None) -> list[ProvisionSettingInfo]:
        """
        Get Provision Arguments.

        Args:
        ---
            module_name (str): The Module Name (eg. "Minecraft")
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            list[ProvisionSettingInfo]: On success returns a list of ProvisionSettingInfo dataclasses.
            * See `types.py -> ProvisionSettingInfo`

        """

        parameters: dict[str, str] = {
            "ModuleName": module_name
        }
        await self._connect()
        result: Any = await self._call_api(api='ADSModule/GetProvisionArguments', parameters=parameters, format_data=format_data, format=ProvisionSettingInfo)
        return result

    # ADSModule.RegisterTarget:({'Parameters': [{'Name': 'controllerUrl', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'myUrl', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'password', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'twoFactorToken', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'friendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def register_target(self, controller_url: str, my_url: str, username: str, password: str,
                              friendly_name: str, two_factor_token: str = "", format_data: Union[bool, None] = None) -> ActionResult:
        """
        Registers a Target to a Controller.

        Args:
        ---
            controller_url (str): The Controller(Main) AMP panel url.
            my_url (str): The Target AMP panel url.
            username (str): The username for logging into the Target AMP panel.
            password (str): The password for logging into the Target AMP panel.
            friendly_name (str): Instance Friendly Name.
            two_factor_token (str): The two-factor authentication token for the username. Defaults to ""
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "controllerUrl": controller_url,
            "myUrl": my_url,
            "username": username,
            "password": password,
            "twoFactorToken": two_factor_token,
            "friendlyName": friendly_name
        }
        await self._connect()
        result = await self._call_api(api='ADSModule/RegisterTarget', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.UpdateTarget:({'Parameters': [{'Name': 'TargetID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    @Base.ADSonly
    async def update_target(self, target_id: str) -> None:
        """
        Update Target Instance.

        Args:
        ---
            target_id (str): The Target Instance ID.

        Returns:
        ---
            None
        """

        parameters: dict[str, str] = {
            "TargetID": target_id
        }

        await self._connect()
        await self._call_api(api='ADSModule/UpdateTarget', parameters=parameters)
        return

    # ADSModule.UpdateInstanceInfo:({'Parameters': [{'Name': 'InstanceId', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'StartOnBoot', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}, {'Name': 'Suspended', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}, {'Name': 'ExcludeFromFirewall', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}, {'Name': 'RunInContainer', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}, {'Name': 'ContainerMemory', 'TypeName': 'Int32', 'Description': '', 'Optional': False}, {'Name': 'MemoryPolicy', 'TypeName': 'ContainerMemoryPolicy', 'Description': '', 'Optional': False, 'ParamEnumValues': {'NotSpecified': 0, 'Reserve': 100, 'Restrict': 200}}, {'Name': 'ContainerMaxCPU', 'TypeName': 'Single', 'Description': '', 'Optional': False}, {'Name': 'ContainerImage', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def update_instance_info(self, instance_info: InstanceInfo, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update an Instances info.

        Args:
        ---
            instance_info (InstanceInfo): The InstanceInfo dataclass.
                See `types.py -> InstanceInfo`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        if isinstance(instance_info, InstanceInfo):
            parameters: dict[Any, Any] = self.dataclass_to_dict(dataclass=instance_info)

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/UpdateInstanceInfo', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.SetInstanceSuspended:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Suspended', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def set_instance_suspended(self, instance_name: str, suspended: bool = False, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Set an Instances suspended State.

        Args:
        ---
            instance_name (str): The Instance Name
            suspended (bool): The Suspended value. Default False
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, Any] = {
            "InstanceName": instance_name,
            "Suspended": suspended
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/SetInstanceSuspended', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.UpgradeInstance:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def upgrade_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Update or Upgrade the Instance

        Args:
        ---
            instance_name (str): The Instance Name
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "InstanceName": instance_name
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/UpgradeInstance', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.StartAllInstances:({'Parameters': [], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def start_all_instances(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Start all Instances.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/StartAllInstances', format_data=format_data, format=ActionResult)
        return result

    # ADSModule.StopAllInstances:({'Parameters': [], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def stop_all_instances(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Stop all Instances.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/StopAllInstances', format_data=format_data, format=ActionResult)
        return result

    # ADSModule.UpgradeAllInstances:({'Parameters': [{'Name': 'RestartRunning', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def upgrade_all_instances(self, restart_running: bool = False, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Upgrade all Instances.

        Args:
        ---
            restart_running (bool): Restart running Instances. Default False
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, bool] = {
            "RestartRunning": restart_running
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/UpgradeAllInstances', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.StartInstance:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def start_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Start an Instance.

        Args:
        ---
            instance_name (str): The Instance Name
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "InstanceName": instance_name
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/StartInstance', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.RestartInstance:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def restart_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Restart an Instance.

        Args:
        ---
            instance_name (str): The Instance Name
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "InstanceName": instance_name
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/RestartInstance', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.StopInstance:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def stop_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Stop an Instance.

        Args:
        ---
            instance_name (str): The Instance Name
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "InstanceName": instance_name
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/StopInstance', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.DeleteInstanceUsers:({'Parameters': [{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def delete_instance_users(self, instance_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete all Users from an Instance.

        Args:
        ---
            instance_id (str): The Instance ID
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "InstanceId": instance_id
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/DeleteInstanceUsers', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.DeleteInstance:({'Parameters': [{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    @Base.ADSonly
    async def delete_instance(self, instance_name: str, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Delete an Instance.

        Args:
        ---
            instance_name (str): The Instance name.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            RunningTask: On success returns a RunningTask dataclass.
            * See `types.py -> RunningTask`
        """

        parameters: dict[str, str] = {
            "InstanceName": instance_name
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/DeleteInstance', parameters=parameters, format_data=format_data, format=RunningTask)
        return result

    # ADSModule.ExtractEverywhere:({'Parameters': [{'Name': 'SourceArchive', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    @Base.ADSonly
    async def extract_everywhere(self, source_archive: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Extracts everything from an archive.

        Args:
        ---
            source_archive (str): The source archive.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns an ActionResult dataclass.
            * See `types.py -> ActionResult`
        """

        parameters: dict[str, str] = {
            "SourceArchive": source_archive
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/ExtractEverywhere', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # ADSModule.Servers:({'Parameters': [{'Name': 'id', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'REQ_RAWJSON', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JSONRawResponse', 'IsComplexType': True})
    @Base.ADSonly
    async def servers(self, id: str, req_rawjson: str = "application/json", format_data: Union[bool, None] = None) -> Any:
        """
        Used for proxy authentication.

        Args:
        ---
            id (str): _description_
            req_rawjson (str): _description_
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            Any: UNK.
        """

        parameters: dict[str, str] = {
            "id": id,
            "REQ_RAWJSON": req_rawjson
        }

        await self._connect()
        result: Any = await self._call_api(api='ADSModule/Servers', parameters=parameters, format_data=format_data)
        return result
