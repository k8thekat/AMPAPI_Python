VERSION: 2.5.0.12
BUILD: 20240530.3
INSTANCE TYPE: ADS

____________________________________________________
ADSModule:
	AddDatastore:
		Parameters:
			{'Name': 'newDatastore', 'TypeName': 'InstanceDatastore', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteDatastore:
		Parameters:
			{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateDatastore:
		Parameters:
			{'Name': 'updatedDatastore', 'TypeName': 'InstanceDatastore', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetDatastores:
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	RequestDatastoreSizeCalculation:
		Parameters:
			{'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetDatastore:
		Parameters:
			{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: JObject
		IsComplexType: True
	RepairDatastore:
		Parameters:
			{'Name': 'id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetDatastoreInstances:
		Parameters:
			{'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	MoveInstanceDatastore:
		Parameters:
			{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'datastoreId', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetDeploymentTemplates:
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	CreateDeploymentTemplate:
		Parameters:
			{'Name': 'Name', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateDeploymentTemplate:
		Parameters:
			{'Name': 'templateToUpdate', 'TypeName': 'DeploymentTemplate', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteDeploymentTemplate:
		Parameters:
			{'Name': 'Id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CloneTemplate:
		Parameters:
			{'Name': 'Id', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
			{'Name': 'NewName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ApplyTemplate:
		Description: Overlays an existing template on an existing instance. Used to perform package reconfigurations. Do not use this to 'transform' an existing application into another. The instance should be deleted and re-created in that situation.
		Returns: 
		Parameters:
			{'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'TemplateID', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
			{'Name': 'NewFriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': True}
			{'Name': 'Secret', 'TypeName': 'String', 'Description': '', 'Optional': True}
			{'Name': 'RestartIfPreviouslyRunning', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeployTemplate:
		Parameters:
			{'Name': 'TemplateID', 'TypeName': 'Int32', 'Description': 'The ID of the template to be deployed, as per the Template Management UI in AMP itself.', 'Optional': False}
			{'Name': 'NewUsername', 'TypeName': 'String', 'Description': 'If specified, AMP will create a new user with this name for this instance. Must be unique. If this user already exists, this will be ignored but the new instance will be assigned to this user.', 'Optional': True}
			{'Name': 'NewPassword', 'TypeName': 'String', 'Description': "If 'NewUsername' is specified and the user doesn't already exist, the password that will be assigned to this user.", 'Optional': True}
			{'Name': 'NewEmail', 'TypeName': 'String', 'Description': "If 'NewUsername' is specified and the user doesn't already exist, the email address that will be assigned to this user.", 'Optional': True}
			{'Name': 'RequiredTags', 'TypeName': 'List<String>', 'Description': "If specified, AMP will only deploy this template to targets that have every single 'tag' specified in their target configuration. You can adjust this via the controller by clicking 'Edit' on the target settings.", 'Optional': True}
			{'Name': 'Tag', 'TypeName': 'String', 'Description': "Unrelated to RequiredTags. This is to uniquely identify this instance to your own systems. It may be something like an order ID or service ID so you can find the associated instance again at a later time. If 'UseTagAsInstanceName' is enabled, then this will also be used as the instance name for the created instance - but it must be unique.", 'Optional': True}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': 'A friendly name for this instance. If left blank, AMP will generate one for you.', 'Optional': True}
			{'Name': 'Secret', 'TypeName': 'String', 'Description': 'Must be a non-empty strong in order to get a callback on deployment state change. This secret will be passed back to you in the callback so you can verify the request.', 'Optional': True}
			{'Name': 'PostCreate', 'TypeName': 'PostCreateAppActions', 'Description': '0: Do Nothing, 1: Update Once, 2: Update Always, 3: Update and Start Once, 4: Update and Start Always, 5. Start Always', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'UpdateOnce': 1, 'UpdateAlways': 2, 'UpdateAndStartOnce': 3, 'UpdateAndStartAlways': 4, 'StartAlways': 5}}
			{'Name': 'ExtraProvisionSettings', 'TypeName': 'Dictionary<String, String>', 'Description': 'A dictionary of setting nodes and values to create the new instance with. Identical in function to the provisioning arguments in the template itself.', 'Optional': True}
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetTargetInfo:
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	GetSupportedApplications:
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetSupportedAppSummaries:
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	RefreshAppCache:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	RefreshRemoteConfigStores:
		Parameters:
			{'Name': 'force', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: Void
		IsComplexType: False
	GetApplicationEndpoints:
		Parameters:
			{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	ReactivateLocalInstances:
		Parameters:
		ReturnTypeName: RunningTask
		IsComplexType: True
	GetInstances:
		Parameters:
			{'Name': 'ForceIncludeSelf', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetInstance:
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: JObject
		IsComplexType: True
	ModifyCustomFirewallRule:
		Parameters:
			{'Name': 'instanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'PortNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
			{'Name': 'Range', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
			{'Name': 'Protocol', 'TypeName': 'PortProtocol', 'Description': '', 'Optional': False, 'ParamEnumValues': {'TCP': 0, 'UDP': 1, 'Both': 2}}
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Open', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ManageInstance:
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult<String>
		IsComplexType: True
	GetGroup:
		Parameters:
			{'Name': 'GroupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: JObject
		IsComplexType: True
	RefreshGroup:
		Parameters:
			{'Name': 'GroupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetLocalInstances:
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetInstanceStatuses:
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetProvisionFitness:
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	AttachADS:
		Parameters:
			{'Name': 'Friendly', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'IsHTTPS', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'Host', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Port', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
			{'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DetachTarget:
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateTargetInfo:
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Url', 'TypeName': 'Uri', 'Description': '', 'Optional': False}
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Tags', 'TypeName': 'List<String>', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ConvertToManaged:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetInstanceNetworkInfo:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	SetInstanceNetworkInfo:
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'PortMappings', 'TypeName': 'Dictionary<String, Int32>', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ApplyInstanceConfiguration:
		Parameters:
			{'Name': 'InstanceID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'Args', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}
			{'Name': 'RebuildConfiguration', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateLocalInstance:
		Parameters:
			{'Name': 'Instance', 'TypeName': 'LocalAMPInstance', 'Description': '', 'Optional': False}
			{'Name': 'PostCreate', 'TypeName': 'PostCreateAppActions', 'Description': '', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'UpdateOnce': 1, 'UpdateAlways': 2, 'UpdateAndStartOnce': 3, 'UpdateAndStartAlways': 4, 'StartAlways': 5}}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateInstanceFromSpec:
		Parameters:
			{'Name': 'SpecId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'TargetADSInstance', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'PostCreate', 'TypeName': 'PostCreateAppActions', 'Description': '', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'UpdateOnce': 1, 'UpdateAlways': 2, 'UpdateAndStartOnce': 3, 'UpdateAndStartAlways': 4, 'StartAlways': 5}}
			{'Name': 'StartOnBoot', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
			{'Name': 'TargetDatastore', 'TypeName': 'Int32', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateInstance:
		Parameters:
			{'Name': 'TargetADSInstance', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'NewInstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'Module', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'IPBinding', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'PortNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
			{'Name': 'AdminUsername', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'AdminPassword', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'ProvisionSettings', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}
			{'Name': 'AutoConfigure', 'TypeName': 'Boolean', 'Description': 'When enabled, all settings other than the Module, Target and FriendlyName are ignored and replaced with automatically generated values.', 'Optional': True}
			{'Name': 'PostCreate', 'TypeName': 'PostCreateAppActions', 'Description': '', 'Optional': True, 'ParamEnumValues': {'DoNothing': 0, 'UpdateOnce': 1, 'UpdateAlways': 2, 'UpdateAndStartOnce': 3, 'UpdateAndStartAlways': 4, 'StartAlways': 5}}
			{'Name': 'StartOnBoot', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
			{'Name': 'DisplayImageSource', 'TypeName': 'String', 'Description': '', 'Optional': True}
			{'Name': 'TargetDatastore', 'TypeName': 'Int32', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	SetInstanceConfig:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Value', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RefreshInstanceConfig:
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'AndUpdateInstance', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	HandoutInstanceConfigs:
		Parameters:
			{'Name': 'ForModule', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Values', 'TypeName': 'List<String>', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetProvisionArguments:
		Parameters:
			{'Name': 'ModuleName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<ProvisionSettingInfo>
		IsComplexType: True
	TestADSLoginDetails:
		Parameters:
			{'Name': 'url', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'password', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RegisterTarget:
		Parameters:
			{'Name': 'controllerUrl', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'myUrl', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'password', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'twoFactorToken', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'friendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateTarget:
		Parameters:
			{'Name': 'TargetID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: Void
		IsComplexType: False
	UpdateInstanceInfo:
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'FriendlyName', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'StartOnBoot', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'Suspended', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'ExcludeFromFirewall', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'RunInContainer', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'ContainerMemory', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
			{'Name': 'ContainerSwap', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
			{'Name': 'MemoryPolicy', 'TypeName': 'ContainerMemoryPolicy', 'Description': '', 'Optional': False, 'ParamEnumValues': {'NotSpecified': 0, 'Reserve': 100, 'Restrict': 200}}
			{'Name': 'ContainerMaxCPU', 'TypeName': 'Single', 'Description': '', 'Optional': False}
			{'Name': 'ContainerImage', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	SetInstanceSuspended:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Suspended', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpgradeInstance:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	StartAllInstances:
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	StopAllInstances:
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpgradeAllInstances:
		Parameters:
			{'Name': 'RestartRunning', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	StartInstance:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RestartInstance:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	StopInstance:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteInstanceUsers:
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteInstance:
		Parameters:
			{'Name': 'InstanceName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: RunningTask
		IsComplexType: True
	ExtractEverywhere:
		Parameters:
			{'Name': 'SourceArchive', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	Servers:
		Parameters:
			{'Name': 'id', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Data', 'TypeName': 'JObject', 'Description': '', 'Optional': False}
			{'Name': 'RealIP', 'TypeName': 'IPAddress', 'Description': '', 'Optional': False}
		ReturnTypeName: JSONRawResponse
		IsComplexType: True
____________________________________________________
FileManagerPlugin:
	Dummy:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	CalculateFileMD5Sum:
		Parameters:
			{'Name': 'FilePath', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult<String>
		IsComplexType: True
	ChangeExclusion:
		Parameters:
			{'Name': 'ModifyPath', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'AsDirectory', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'Exclude', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateArchive:
		Parameters:
			{'Name': 'PathToArchive', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ExtractArchive:
		Parameters:
			{'Name': 'ArchivePath', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'DestinationPath', 'TypeName': 'String', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetDirectoryListing:
		Parameters:
			{'Name': 'Dir', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	GetFileChunk:
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Position', 'TypeName': 'Int64', 'Description': '', 'Optional': False}
			{'Name': 'Length', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: JObject
		IsComplexType: True
	AppendFileChunk:
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Data', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Delete', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: Void
		IsComplexType: False
	ReadFileChunk:
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Offset', 'TypeName': 'Int64', 'Description': '', 'Optional': False}
			{'Name': 'ChunkSize', 'TypeName': 'Int64', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult<String>
		IsComplexType: True
	WriteFileChunk:
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Data', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Offset', 'TypeName': 'Int64', 'Description': '', 'Optional': False}
			{'Name': 'FinalChunk', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DownloadFileFromURL:
		Parameters:
			{'Name': 'Source', 'TypeName': 'Uri', 'Description': '', 'Optional': False}
			{'Name': 'TargetDirectory', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RenameFile:
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'NewFilename', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CopyFile:
		Parameters:
			{'Name': 'Origin', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'TargetDirectory', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	TrashFile:
		Description: Moves a file to trash, files must be trashed before they can be deleted.
		Returns: 
		Parameters:
			{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	TrashDirectory:
		Description: Moves a directory to trash, files must be trashed before they can be deleted.
		Returns: 
		Parameters:
			{'Name': 'DirectoryName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	EmptyTrash:
		Description: Empties a trash bin
		Returns: 
		Parameters:
			{'Name': 'TrashDirectoryName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	CreateDirectory:
		Description: Creates a new directory. The parent directory must already exist.
		Returns: 
		Parameters:
			{'Name': 'NewPath', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RenameDirectory:
		Description: Renames a directory
		Returns: 
		Parameters:
			{'Name': 'oldDirectory', 'TypeName': 'String', 'Description': 'The full path to the old directory', 'Optional': False}
			{'Name': 'NewDirectoryName', 'TypeName': 'String', 'Description': 'The name component of the new directory (not the full path)', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
____________________________________________________
EmailSenderPlugin:
	TestSMTPSettings:
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
____________________________________________________
LocalFileBackupPlugin:
	RefreshBackupList:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	UploadToS3:
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: RunningTask
		IsComplexType: True
	DownloadFromS3:
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: RunningTask
		IsComplexType: True
	DeleteFromS3:
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetBackups:
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	RestoreBackup:
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'DeleteExistingData', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteLocalBackup:
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: Void
		IsComplexType: False
	SetBackupSticky:
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'Sticky', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	TakeBackup:
		Parameters:
			{'Name': 'Title', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Sticky', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'WasCreatedAutomatically', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
____________________________________________________
CommonCorePlugin:
____________________________________________________
Core:
	GetAuditLogEntries:
		Parameters:
			{'Name': 'Before', 'TypeName': 'Nullable<DateTime>', 'Description': '', 'Optional': False}
			{'Name': 'Count', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<IAuditLogEntry>
		IsComplexType: True
	GetSettingsSpec:
		Parameters:
		ReturnTypeName: Dictionary<String, IEnumerable<JObject>>
		IsComplexType: True
	RefreshSettingValueList:
		Parameters:
			{'Name': 'Node', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RefreshSettingsSourceCache:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	GetSettingValues:
		Parameters:
			{'Name': 'SettingNode', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'WithRefresh', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: IDictionary<String, String>
		IsComplexType: False
	GetProvisionSpec:
		Parameters:
		ReturnTypeName: List<JObject>
		IsComplexType: True
	GetConfig:
		Parameters:
			{'Name': 'node', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: JObject
		IsComplexType: True
	GetConfigs:
		Parameters:
			{'Name': 'nodes', 'TypeName': 'String[]', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	SetConfigs:
		Parameters:
			{'Name': 'data', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}
		ReturnTypeName: Boolean
		IsComplexType: False
	SetConfig:
		Parameters:
			{'Name': 'node', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'value', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ActivateAMPLicence:
		Parameters:
			{'Name': 'LicenceKey', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'QueryOnly', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult<JObject>
		IsComplexType: True
	GetRoleData:
		Parameters:
		ReturnTypeName: IEnumerable<AuthRoleSummary>
		IsComplexType: True
	GetRoleIds:
		Parameters:
		ReturnTypeName: IDictionary<Guid, String>
		IsComplexType: False
	GetRole:
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: AuthRoleSummary
		IsComplexType: True
	CreateRole:
		Parameters:
			{'Name': 'Name', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'AsCommonRole', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult<Guid>
		IsComplexType: True
	DeleteRole:
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RenameRole:
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'NewName', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	SetAMPRolePermission:
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'PermissionNode', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Enabled', 'TypeName': 'Nullable<Boolean>', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetAMPRolePermissions:
		Parameters:
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<String>
		IsComplexType: False
	GetScheduleData:
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	AddEventTrigger:
		Parameters:
			{'Name': 'triggerId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RunEventTriggerImmediately:
		Parameters:
			{'Name': 'triggerId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	AddIntervalTrigger:
		Parameters:
			{'Name': 'months', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'days', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'hours', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'minutes', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'daysOfMonth', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'description', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetTimeIntervalTrigger:
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: JObject
		IsComplexType: True
	EditIntervalTrigger:
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'months', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'days', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'hours', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'minutes', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'daysOfMonth', 'TypeName': 'Int32[]', 'Description': '', 'Optional': False}
			{'Name': 'description', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	SetTriggerEnabled:
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'Enabled', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	AddTask:
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'MethodID', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'ParameterMapping', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	EditTask:
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'ParameterMapping', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ChangeTaskOrder:
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'NewOrder', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteTask:
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'TaskID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteTrigger:
		Parameters:
			{'Name': 'TriggerID', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetActiveAMPSessions:
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	EndUserSession:
		Parameters:
			{'Name': 'Id', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: Void
		IsComplexType: False
	GetAMPUsersSummary:
		Parameters:
		ReturnTypeName: IEnumerable<UserInfoSummary>
		IsComplexType: True
	GetAMPUserInfo:
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: UserInfo
		IsComplexType: True
	GetAllAMPUserInfo:
		Parameters:
		ReturnTypeName: IEnumerable<UserInfo>
		IsComplexType: True
	SetAMPUserRoleMembership:
		Parameters:
			{'Name': 'UserId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'RoleId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
			{'Name': 'IsMember', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetPermissionsSpec:
		Parameters:
		ReturnTypeName: IList<IPermissionsTreeNode>
		IsComplexType: True
	CreateUser:
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult<Guid>
		IsComplexType: True
	DeleteUser:
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateUserInfo:
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Disabled', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'PasswordExpires', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'CannotChangePassword', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'MustChangePassword', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
			{'Name': 'EmailAddress', 'TypeName': 'String', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetWebauthnChallenge:
		Parameters:
		ReturnTypeName: ActionResult<String>
		IsComplexType: True
	GetWebauthnCredentialIDs:
		Parameters:
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: JObject
		IsComplexType: True
	WebauthnRegister:
		Parameters:
			{'Name': 'attestationObject', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'clientDataJSON', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'description', 'TypeName': 'String', 'Description': '', 'Optional': True}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetWebauthnCredentialSummaries:
		Parameters:
		ReturnTypeName: IEnumerable<WebauthnCredentialSummary>
		IsComplexType: True
	RevokeWebauthnCredential:
		Parameters:
			{'Name': 'ID', 'TypeName': 'Int32', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateAccountInfo:
		Parameters:
			{'Name': 'EmailAddress', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'TwoFactorPIN', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	EnableTwoFactor:
		Description: Sets up two-factor authentication for the given user. ConfirmTwoFactorSetup must be invoked to complete setup.
		Returns: Data container the URI for a QR code that should be scanned by a mobile authenticator.
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'Password', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult<TwoFactorSetupInfo>
		IsComplexType: True
	ConfirmTwoFactorSetup:
		Description: Completes two-factor setup by supplying a valid two factor code based on the secret provided by EnableTwoFactor
		Returns: 
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'TwoFactorCode', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DisableTwoFactor:
		Parameters:
			{'Name': 'Password', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'TwoFactorCode', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ResetUserPassword:
		Description: For administrative users to alter the password of another user
		Returns: 
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'NewPassword', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteInstanceUsers:
		Parameters:
			{'Name': 'InstanceId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	ChangeUserPassword:
		Description: For a user to change their own password, requires knowing the old password
		Returns: 
		Parameters:
			{'Name': 'Username', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'OldPassword', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'NewPassword', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'TwoFactorPIN', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetUpdates:
		Description: Gets changes to the server status, in addition to any notifications or console output that have occured since the last time GetUpdates() was called by the current session.
		Returns: 
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	GetNewGuid:
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
		Parameters:
			{'Name': 'PermissionNode', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: Boolean
		IsComplexType: False
	GetTasks:
		Parameters:
		ReturnTypeName: IEnumerable<RunningTask>
		IsComplexType: True
	GetPortSummaries:
		Parameters:
		ReturnTypeName: IEnumerable<ListeningPortSummary>
		IsComplexType: True
	GetStatus:
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	CancelTask:
		Parameters:
			{'Name': 'TaskId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DismissTask:
		Parameters:
			{'Name': 'TaskId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DismissAllTasks:
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetUserInfo:
		Description: Provides information about a given in-application user (as opposed to AMP system users)
		Returns: 
		Parameters:
			{'Name': 'UID', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: SimpleUser
		IsComplexType: True
	Start:
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
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	Restart:
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	Kill:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	Sleep:
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	UpdateApplication:
		Parameters:
		ReturnTypeName: ActionResult
		IsComplexType: True
	AcknowledgeAMPUpdate:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	GetModuleInfo:
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	GetAPISpec:
		Parameters:
		ReturnTypeName: Dictionary<String, Dictionary<String, JObject>>
		IsComplexType: True
	GetUserActionsSpec:
		Parameters:
		ReturnTypeName: Object
		IsComplexType: False
	GetAuthencationRequirements:
		Parameters:
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: IEnumerable<AuthencationRequirement>
		IsComplexType: True
	Login:
		Parameters:
			{'Name': 'username', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'password', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'token', 'TypeName': 'String', 'Description': '', 'Optional': False}
			{'Name': 'rememberMe', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}
		ReturnTypeName: JObject
		IsComplexType: True
	GetRemoteLoginToken:
		Parameters:
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': True}
			{'Name': 'IsTemporary', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}
		ReturnTypeName: String
		IsComplexType: False
	SendConsoleMessage:
		Parameters:
			{'Name': 'message', 'TypeName': 'String', 'Description': '', 'Optional': False}
		ReturnTypeName: Void
		IsComplexType: False
	UpdateAMPInstance:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	GetUpdateInfo:
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	Logout:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	RestartAMP:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	UpgradeAMP:
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	GetDiagnosticsInfo:
		Parameters:
		ReturnTypeName: Dictionary<String, String>
		IsComplexType: False
	GetWebserverMetrics:
		Parameters:
		ReturnTypeName: Object
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
