INSTANCE TYPE: ADS
VERSION: 2.6.0.0
BUILD: 20241023.2

____________________________________________________
ADSModule:
	AddDatastore:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'newDatastore', 'TypeName': 'InstanceDatastore', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteDatastore:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateDatastore:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'updatedDatastore', 'TypeName': 'InstanceDatastore', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetDatastores:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	RequestDatastoreSizeCalculation:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetDatastore:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JObject
		IsComplexType: True
	RepairDatastore:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetDatastoreInstances:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	MoveInstanceDatastore:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetDeploymentTemplates:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	CreateDeploymentTemplate:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Name', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateDeploymentTemplate:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'templateToUpdate', 'TypeName': 'DeploymentTemplate', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteDeploymentTemplate:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Id', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CloneTemplate:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Id', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ApplyTemplate:
		Description: Overlays an existing template on an existing instance. Used to perform package reconfigurations. Do not use this to 'transform' an existing application into another. The instance should be deleted and re-created in that situation.
		Returns: 
		Parameters:
			{'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TemplateID', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewFriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'Secret', 'TypeName': 'String', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'RestartIfPreviouslyRunning', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeployTemplate:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TemplateID', 'TypeName': 'Int32', 'Description': 'The ID of the template to be deployed, as per the Template Management UI in AMP itself.', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewUsername', 'TypeName': 'String', 'Description': 'If specified, AMP will create a new user with this name for this instance. Must be unique. If this user already exists, this will be ignored but the new instance will be assigned to this user.', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'NewPassword', 'TypeName': 'String', 'Description': "If 'NewUsername' is specified and the user doesn't already exist, the password that will be assigned to this user.", 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'NewEmail', 'TypeName': 'String', 'Description': "If 'NewUsername' is specified and the user doesn't already exist, the email address that will be assigned to this user.", 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'RequiredTags', 'TypeName': 'List<String>', 'Description': "If specified, AMP will only deploy this template to targets that have every single 'tag' specified in their target configuration. You can adjust this via the controller by clicking 'Edit' on the target settings.", 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'Tag', 'TypeName': 'String', 'Description': "Unrelated to RequiredTags. This is to uniquely identify this instance to your own systems. It may be something like an order ID or service ID so you can find the associated instance again at a later time. If 'UseTagAsInstanceName' is enabled, then this will also be used as the instance name for the created instance - but it must be unique.", 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': 'A friendly name for this instance. If left blank, AMP will generate one for you.', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'Secret', 'TypeName': 'String', 'Description': 'Must be a non-empty strong in order to get a callback on deployment state change. This secret will be passed back to you in the callback so you can verify the request.', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'PostCreate', 'TypeName': 'PostCreateAppActions', 'Description': '0: Do Nothing, 1: Update Once, 2: Update Always, 3: Update and Start Once, 4: Update and Start Always, 5. Start Always', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'UpdateOnce': 1, 'UpdateAlways': 2, 'UpdateAndStartOnce': 3, 'UpdateAndStartAlways': 4, 'StartAlways': 5}}
			{'Name': 'ExtraProvisionSettings', 'TypeName': 'Dictionary<String, String>', 'Description': 'A dictionary of setting nodes and values to create the new instance with. Identical in function to the provisioning arguments in the template itself.', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetTargetInfo:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	GetSupportedApplications:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetSupportedAppSummaries:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	RefreshAppCache:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	RefreshRemoteConfigStores:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'force', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	GetApplicationEndpoints:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	ReactivateInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	ReactivateLocalInstances:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetInstances:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ForceIncludeSelf', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JObject
		IsComplexType: True
	ModifyCustomFirewallRule:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PortNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Range', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Protocol', 'TypeName': 'PortProtocol', 'Description': '', 'Optional': False, 'ParamEnumValues': {'TCP': 0, 'UDP': 1, 'Both': 2}}
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Open', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ManageInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult<String>
		IsComplexType: True
	GetGroup:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'GroupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JObject
		IsComplexType: True
	RefreshGroup:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'GroupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetLocalInstances:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetInstanceStatuses:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetProvisionFitness:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	AttachADS:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Friendly', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'IsHTTPS', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Host', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Port', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DetachTarget:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateTargetInfo:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Url', 'TypeName': 'Uri', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Tags', 'TypeName': 'List<String>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetInstanceNetworkInfo:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	SetInstanceNetworkInfo:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PortMappings', 'TypeName': 'Dictionary<String, Int32>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ApplyInstanceConfiguration:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Args', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'RebuildConfiguration', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateLocalInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Instance', 'TypeName': 'LocalAMPInstance', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PostCreate', 'TypeName': 'PostCreateAppActions', 'Description': '', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'UpdateOnce': 1, 'UpdateAlways': 2, 'UpdateAndStartOnce': 3, 'UpdateAndStartAlways': 4, 'StartAlways': 5}}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateInstanceFromSpec:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'SpecId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TargetADSInstance', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PostCreate', 'TypeName': 'PostCreateAppActions', 'Description': '', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'UpdateOnce': 1, 'UpdateAlways': 2, 'UpdateAndStartOnce': 3, 'UpdateAndStartAlways': 4, 'StartAlways': 5}}
			{'Name': 'StartOnBoot', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'TargetDatastore', 'TypeName': 'Int32', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TargetADSInstance', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewInstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Module', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'IPBinding', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PortNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'AdminUsername', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'AdminPassword', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'ProvisionSettings', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'AutoConfigure', 'TypeName': 'Boolean', 'Description': 'When enabled, all settings other than the Module, Target and FriendlyName are ignored and replaced with automatically generated values.', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'PostCreate', 'TypeName': 'PostCreateAppActions', 'Description': '', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'UpdateOnce': 1, 'UpdateAlways': 2, 'UpdateAndStartOnce': 3, 'UpdateAndStartAlways': 4, 'StartAlways': 5}}
			{'Name': 'StartOnBoot', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'DisplayImageSource', 'TypeName': 'String', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'TargetDatastore', 'TypeName': 'Int32', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	SetInstanceConfig:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Value', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RefreshInstanceConfig:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	HandoutInstanceConfigs:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ForModule', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Values', 'TypeName': 'List<String>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetProvisionArguments:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ModuleName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<ProvisionSettingInfo>
		IsComplexType: True
	TestADSLoginDetails:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'url', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'password', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'twoFactorToken', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RegisterTarget:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'controllerUrl', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'myUrl', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'password', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'twoFactorToken', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'friendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateTarget:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TargetID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	UpdateInstanceInfo:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'StartOnBoot', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Suspended', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'ExcludeFromFirewall', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'RunInContainer', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'ContainerMemory', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'ContainerSwap', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'MemoryPolicy', 'TypeName': 'ContainerMemoryPolicy', 'Description': '', 'Optional': False, 'ParamEnumValues': {'NotSpecified': 0, 'Reserve': 100, 'Restrict': 200}}
			{'Name': 'ContainerMaxCPU', 'TypeName': 'Single', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'ContainerImage', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'WelcomeMessage', 'TypeName': 'String', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	SetInstanceSuspended:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Suspended', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpgradeInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	StartAllInstances:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TargetADSInstance', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	StopAllInstances:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TargetADSInstance', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpgradeAllInstances:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TargetADSInstance', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'RestartRunning', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	StartInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RestartInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	StopInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteInstanceUsers:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteInstance:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	ExtractEverywhere:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'SourceArchive', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	Servers:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Data', 'TypeName': 'JObject', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'RealIP', 'TypeName': 'IPAddress', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JSONRawResponse
		IsComplexType: True
____________________________________________________
FileManagerPlugin:
	Dummy:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	CalculateFileMD5Sum:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'FilePath', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult<String>
		IsComplexType: True
	ChangeExclusion:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ModifyPath', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'AsDirectory', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Exclude', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateArchive:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'PathToArchive', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ExtractArchive:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ArchivePath', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'DestinationPath', 'TypeName': 'String', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetDirectoryListing:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Dir', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetFileChunk:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Position', 'TypeName': 'Int64', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Length', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JObject
		IsComplexType: True
	AppendFileChunk:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Data', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Delete', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	ReadFileChunk:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Offset', 'TypeName': 'Int64', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'ChunkSize', 'TypeName': 'Int64', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult<String>
		IsComplexType: True
	ReleaseFileUploadLock:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	WriteFileChunk:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Data', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Offset', 'TypeName': 'Int64', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'FinalChunk', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DownloadFileFromURL:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Source', 'TypeName': 'Uri', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TargetDirectory', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RenameFile:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewFilename', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CopyFile:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Origin', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TargetDirectory', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	TrashFile:
		Description: Moves a file to trash, files must be trashed before they can be deleted.
		Returns: 
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	TrashDirectory:
		Description: Moves a directory to trash, files must be trashed before they can be deleted.
		Returns: 
		Parameters:
			{'Name': 'DirectoryName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	EmptyTrash:
		Description: Empties a trash bin
		Returns: 
		Parameters:
			{'Name': 'TrashDirectoryName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateDirectory:
		Description: Creates a new directory. The parent directory must already exist.
		Returns: 
		Parameters:
			{'Name': 'NewPath', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RenameDirectory:
		Description: Renames a directory
		Returns: 
		Parameters:
			{'Name': 'oldDirectory', 'TypeName': 'String', 'Description': 'The full path to the old directory', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewDirectoryName', 'TypeName': 'String', 'Description': 'The name component of the new directory (not the full path)', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
____________________________________________________
EmailSenderPlugin:
	TestSMTPSettings:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
____________________________________________________
CommonCorePlugin:
____________________________________________________
Core:
	GetAuditLogEntries:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Before', 'TypeName': 'Nullable<DateTime>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Count', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<IAuditLogEntry>
		IsComplexType: True
	RunSecurityCheck:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetSettingsSpec:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Dictionary<String, IEnumerable<JObject>>
		IsComplexType: True
	RefreshSettingValueList:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Node', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RefreshSettingsSourceCache:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	GetSettingValues:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'WithRefresh', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: IDictionary<String, String>
		IsComplexType: False
	GetProvisionSpec:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: List<JObject>
		IsComplexType: True
	GetConfig:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'node', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JObject
		IsComplexType: True
	GetConfigs:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'nodes', 'TypeName': 'String[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	SetConfigs:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'data', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Boolean
		IsComplexType: False
	SetConfig:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'node', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'value', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ActivateAMPLicence:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'LicenceKey', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'QueryOnly', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult<JObject>
		IsComplexType: True
	GetRoleData:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<AuthRoleSummary>
		IsComplexType: True
	GetRoleIds:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IDictionary<Guid, String>
		IsComplexType: False
	GetRole:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: AuthRoleSummary
		IsComplexType: True
	CreateRole:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Name', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'AsCommonRole', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult<Guid>
		IsComplexType: True
	DeleteRole:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RenameRole:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewName', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	SetAMPRolePermission:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PermissionNode', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Enabled', 'TypeName': 'Nullable<Boolean>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetAMPRolePermissions:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<String>
		IsComplexType: False
	GetScheduleData:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	AddEventTrigger:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'triggerId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RunEventTriggerImmediately:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'triggerId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	AddIntervalTrigger:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'months', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'days', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'hours', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'minutes', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'daysOfMonth', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'description', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetTimeIntervalTrigger:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JObject
		IsComplexType: True
	EditIntervalTrigger:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'months', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'days', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'hours', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'minutes', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'daysOfMonth', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'description', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	SetTriggerEnabled:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Enabled', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	AddTask:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'MethodID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'ParameterMapping', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	EditTask:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'ParameterMapping', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ChangeTaskOrder:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewOrder', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteTask:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteTrigger:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetActiveAMPSessions:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	EndUserSession:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	GetAMPUsersSummary:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<UserInfoSummary>
		IsComplexType: True
	GetAMPUserInfo:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: UserInfo
		IsComplexType: True
	GetAllAMPUserInfo:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<UserInfo>
		IsComplexType: True
	SetAMPUserRoleMembership:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'UserId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'IsMember', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetPermissionsSpec:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IList<IPermissionsTreeNode>
		IsComplexType: True
	CreateUser:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult<Guid>
		IsComplexType: True
	DeleteUser:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateUserInfo:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Disabled', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PasswordExpires', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'CannotChangePassword', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'MustChangePassword', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'EmailAddress', 'TypeName': 'String', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetWebauthnChallenge:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: ActionResult<String>
		IsComplexType: True
	GetWebauthnCredentialIDs:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JObject
		IsComplexType: True
	WebauthnRegister:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'attestationObject', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'clientDataJSON', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'description', 'TypeName': 'String', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetWebauthnCredentialSummaries:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<WebauthnCredentialSummary>
		IsComplexType: True
	RevokeWebauthnCredential:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ID', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateAccountInfo:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'EmailAddress', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TwoFactorPIN', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	EnableTwoFactor:
		Description: Sets up two-factor authentication for the given user. ConfirmTwoFactorSetup must be invoked to complete setup.
		Returns: Data container the URI for a QR code that should be scanned by a mobile authenticator.
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Password', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult<TwoFactorSetupInfo>
		IsComplexType: True
	ConfirmTwoFactorSetup:
		Description: Completes two-factor setup by supplying a valid two factor code based on the secret provided by EnableTwoFactor
		Returns: 
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TwoFactorCode', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DisableTwoFactor:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Password', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TwoFactorCode', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ResetUserPassword:
		Description: For administrative users to alter the password of another user
		Returns: 
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewPassword', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteInstanceUsers:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ChangeUserPassword:
		Description: For a user to change their own password, requires knowing the old password
		Returns: 
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'OldPassword', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'NewPassword', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'TwoFactorPIN', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetUpdates:
		Description: Gets changes to the server status, in addition to any notifications or console output that have occurred since the last time GetUpdates() was called by the current session.
		Returns: 
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	GetNewGuid:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Guid
		IsComplexType: False
	GetUserList:
		Description: Returns a list of in-application users
		Returns: 
		Parameters:
		ReturnTypeName: Dictionary<String, String>
		IsComplexType: False
	CurrentSessionHasPermission:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'PermissionNode', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Boolean
		IsComplexType: False
	GetTasks:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<RunningTask>
		IsComplexType: True
	GetPortSummaries:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<ListeningPortSummary>
		IsComplexType: True
	GetStatus:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	CancelTask:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TaskId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DismissTask:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'TaskId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DismissAllTasks:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetUserInfo:
		Description: Provides information about a given in-application user (as opposed to AMP system users)
		Returns: 
		Parameters:
			{'Name': 'UID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: SimpleUser
		IsComplexType: True
	Start:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	Suspend:
		Description: Prevents the current instance from being started, and stops it if it's currently running.
		Returns: 
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	Resume:
		Description: Allows the service to be re-started after previously being suspended.
		Returns: 
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	Stop:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	Restart:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	Kill:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	Sleep:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateApplication:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	AcknowledgeAMPUpdate:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	GetModuleInfo:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	GetAPISpec:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Dictionary<String, Dictionary<String, JObject>>
		IsComplexType: True
	GetUserActionsSpec:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Object
		IsComplexType: False
	GetAuthenticationRequirements:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: IEnumerable<AuthenticationRequirement>
		IsComplexType: True
	Login:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'password', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'token', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'rememberMe', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JObject
		IsComplexType: True
	GetRemoteLoginToken:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'IsTemporary', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: String
		IsComplexType: False
	SendConsoleMessage:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'message', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	UpdateAMPInstance:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	GetUpdateInfo:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	Logout:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	RestartAMP:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	UpgradeAMP:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	GetDiagnosticsInfo:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Dictionary<String, String>
		IsComplexType: False
	CreateTestTask:
		Description: DEV: Creates a non-ending task with 50% progress for testing purposes
		Returns: 
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	AsyncTest:
		Description: DEV: Async test method
		Returns: 
		Parameters:
		ReturnTypeName: String
		IsComplexType: False
