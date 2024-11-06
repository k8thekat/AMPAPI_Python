INSTANCE TYPE: Minecraft
VERSION: 2.6.0.0
BUILD: 20241023.2

____________________________________________________
MinecraftModule:
	BukGetCategories:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JSONRawResponse
		IsComplexType: True
	BukGetPopularPlugins:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JSONRawResponse
		IsComplexType: True
	BukGetPluginsForCategory:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'CategoryId', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PageNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PageSize', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JSONRawResponse
		IsComplexType: True
	BukGetPluginInfo:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'PluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JSONRawResponse
		IsComplexType: True
	BukGetInstalledPlugins:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JSONRawResponse
		IsComplexType: True
	BukGetRemovePlugin:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'PluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	BukGetInstallUpdatePlugin:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'pluginId', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	BukGetSearch:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Query', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PageNumber', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'PageSize', 'TypeName': 'Int32', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: JSONRawResponse
		IsComplexType: True
	GetHeadByUUID:
		Description: Get a skin as a base64 string
		Returns: 
		Parameters:
			{'Name': 'id', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: String
		IsComplexType: False
	GetFailureReason:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: String
		IsComplexType: False
	AcceptEULA:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Boolean
		IsComplexType: False
	BanUserByID:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	KickUserByID:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	ClearInventoryByID:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	KillByID:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	SmiteByID:
		Description: Strike a player with lightning
		Returns: 
		Parameters:
			{'Name': 'ID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	GetOPWhitelist:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: JObject
		IsComplexType: True
	GetWhitelist:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	LoadOPList:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	AddOPEntry:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RemoveOPEntry:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	AddToWhitelist:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	RemoveWhitelistEntry:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'UserOrUUID', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
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
LocalFileBackupPlugin:
	RefreshBackupList:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: Void
		IsComplexType: False
	UploadToS3:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	DownloadFromS3:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: RunningTask
		IsComplexType: True
	DeleteFromS3:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	GetBackups:
		Description: None
		Returns: None
		Parameters:
		ReturnTypeName: IEnumerable<JObject>
		IsComplexType: True
	RestoreBackup:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'DeleteExistingData', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	DeleteLocalBackup:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: Void
		IsComplexType: False
	SetBackupSticky:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Sticky', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
	TakeBackup:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'Title', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'Sticky', 'TypeName': 'Boolean', 'Description': '', 'Optional': False, 'ParamEnumValues': None}
			{'Name': 'WasCreatedAutomatically', 'TypeName': 'Boolean', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: ActionResult
		IsComplexType: True
____________________________________________________
CommonCorePlugin:
____________________________________________________
AnalyticsPlugin:
	GetAnalyticsSummary:
		Description: None
		Returns: None
		Parameters:
			{'Name': 'PeriodDays', 'TypeName': 'Int32', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'StartDate', 'TypeName': 'Nullable<DateTime>', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
			{'Name': 'Filters', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': True, 'ParamEnumValues': None}
		ReturnTypeName: Object
		IsComplexType: False
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
		Description: Gets changes to the server status, in addition to any notifications or console output that have occured since the last time GetUpdates() was called by the current session.
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
