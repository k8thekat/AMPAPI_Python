# API class types
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Union


class State_enum(Enum):
    """
    Represents the state of an instance

    Author: p0t4t0sandwich -> https://github.com/p0t4t0sandwich/ampapi-py/blob/main/ampapi/types.py

    """

    Undefined = -1
    Stopped = 0
    PreStart = 5
    Configuring = 7  # The server is performing some first-time-start configuration.
    Starting = 10
    Ready = 20
    Restarting = 30  # Server is in the middle of stopping, but once shutdown has finished it will automatically restart.
    Stopping = 40
    PreparingForSleep = 45
    Sleeping = 50  # The application should be able to be resumed quickly if using this state. Otherwise use Stopped.
    Waiting = 60  # The application is waiting for some external service/application to respond/become available.
    Installing = 70
    Updating = 75
    AwaitingUserInput = 80  # Used during installation, means that some user input is required to complete setup (authentication etc).
    Failed = 100
    Suspended = 200
    Maintenance = 250
    Indeterminate = 999  # The state is unknown, or doesn't apply (for modules that don't start an external process)


class PostCreateActions(Enum):
    """
    The action the Instance will take after creation. Used in dataclass parameters.

    """

    DoNothing = 0
    StartInstance = 1
    StartAndUpdate = 2
    FullStartup = 3
    EveryTime = 16


class PostCreate(Enum):
    """
    Represents the state of the API call `ADSModule/DeployTemplate`

    """

    Do_Nothing = 0
    Update_Once = 1
    Update_Always = 2
    Update_and_Start_Once = 3
    Update_and_Start_Always = 4
    Start_Always = 5


class ContainerMemoryPolicy(Enum):
    NotSpecified = 0
    Reserve = 100
    Restrict = 200


@dataclass()
class APIParams():
    """
    A class to hold Login information for AMP API.\n
    **`DO NOT SET OR UPDATE _sessions`** The API handle's this.

    """

    url: str
    user: str
    password: str
    use_2fa: bool = False
    token: str = ""
    _sessions: dict[str, APISession] = field(init=False, default_factory=dict)


@dataclass()
class APISession():
    """
    Stores the Session ID and the TTL or time to live/last usage of the session ID.

    """

    id: str
    ttl: datetime


@dataclass()
class ActionResult():
    """
    Represents the results of some API calls.

    """

    Status: bool
    Reason: str | None = field(default=None)
    Result: str | None = field(default=None)


@dataclass()
class Login_UserInfo():
    """
    Represents an AMP users information, tied to `LoginResults()` along with the endpoint `get_amp_users_summary()`

    """

    ID: str
    Username: str
    IsTwoFactorEnabled: bool
    Disabled: bool
    GravatarHash: str
    IsLDAPUser: bool
    LastLogin: str  # type:ignore
    EmailAddress: str = ""

    @property
    def LastLogin(self) -> datetime:
        """
        Converts our LastLogin attribute into a Datetime Object.

        Returns:
            datetime: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
        """
        if isinstance(self._LastLogin, datetime):
            return self._LastLogin

        return datetime.fromtimestamp(int(self._LastLogin[6:-2]) / 1000)

    @LastLogin.setter
    def LastLogin(self, value: str) -> None:
        self._LastLogin = value


@dataclass()
class LoginResults():
    """
    Represents an AMP Login response.

    """

    success: bool
    result: int
    permissions: list[str] = field(default_factory=list)
    resultReason: str = ""
    sessionID: str = ""
    rememberMeToken: str = ""
    userInfo: Login_UserInfo | None = None  # second data class


@dataclass()
class AMP_Version():
    """
    Conversion class for `UpdateInfo.Build`

    """

    Major: int
    Minor: int
    Revision: int
    MinorRevision: int
    Build: Union[int, None] = None


@dataclass()
class UpdateInfo():
    """
    Represents AMP API call `Core/GetUpdateInfo`.

    """

    UpdateAvailable: bool
    ReleaseNotesURL: str
    Build: str
    Version: str  # type:ignore
    ToolsVersion: None | str = None
    PatchOnly: None | bool = None


@dataclass()
class Metrics_Data():
    """
    Represents the data from `Metrics()`

    """

    RawValue: int
    MaxValue: int
    Percent: int
    Units: str
    Color: None | str = None
    Color2: None | str = None
    Color3: None | str = None


@dataclass()
class Metric():
    """
    The Metrics dataclass for Updates_Status().Metrics, houses all the Metrics information.

    """

    Active_Users: None | Metrics_Data = field(default=None)
    CPU_Usage: None | Metrics_Data = field(default=None)
    Memory_Usage: None | Metrics_Data = field(default=None)


@dataclass()
class AppStatus():
    """
    Tied to `get_status()`, represents the Instance stats.

    """

    State: State_enum
    Uptime: str
    Metrics: Metric


@dataclass()
class InstanceStatus():
    """
    Represents the data returned from `get_instance_status()`

    """

    InstanceID: str
    Running: bool


@dataclass()
class Console_Entries():
    """
    Represents an individual entry in the related AMP Instances Console. Tied to `Updates().Console_Entries`

    """

    Contents: str
    Source: str
    Type: str
    Timestamp: str  # type:ignore #dataclass wizard needs these.

    @property
    def Timestamp(self) -> datetime:
        """
        Converts our Timestamp attribute into a Datetime Object.

        Returns:
            datetime: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
        """

        if isinstance(self._Timestamp, datetime):
            return self._Timestamp

        return datetime.fromtimestamp(int(self._Timestamp[6:-2]) / 1000)

    @Timestamp.setter
    def Timestamp(self, value: str) -> None:
        self._Timestamp = value


@dataclass()
class Port():
    """

    Current Port of the related AMP Instance. Tied to `Updates().Ports` and the API call `get_port_summaries()`

    """

    Listening: bool
    Name: str
    Port: int
    Protocol: int
    Required: bool | None = field(default=None)
    IsDelayedOpen: bool | None = field(default=None)


@dataclass()
class Messages():
    """
    Represents a Message from the dataclass `Updates().Messages`\n
    *Not sure what generates these inside AMP or where to find them.*

    """

    AgeMinutes: int
    Expired: bool
    Id: str
    Message: str
    Source: str


@dataclass()
class Task():
    """
    Represents a Task that is being run on an Instance. Tied to dataclass `Updates().Tasks`

    """

    IsPrimaryTask: bool
    StartTime: str
    Id: str
    Name: str
    Description: str
    HideFromUI: bool
    FastDismiss: bool
    LastUpdatePushed: str
    ProgressPercent: float
    IsCancellable: bool
    Origin: str
    IsIndeterminate: bool
    State: int
    Status: str


@dataclass()
class Updates():
    """
    Represents the data from AMP API call `get_updates()` \n

    """

    ConsoleEntries: list[Console_Entries]
    Status: AppStatus
    Messages: list[Messages]  # No ideal usage at this time.
    Ports: list[Port] = field(default_factory=list)  # No ideal usage at this time.
    Tasks: list[Task] = field(default_factory=list)  # No ideal usage at this time.


@dataclass()
class Instance():
    """
    Represents the data from the AMP API call `getInstance()` or a list of these from `getInstances()`

    """

    AppState: State_enum
    ApplicationEndpoints: list[dict[str, str]]  # [{'DisplayName': 'Application ' \n 'Address', 'Endpoint': '0.0.0.0:7785', 'Uri': 'steam://connect/0.0.0.0:7785'}, {'DisplayName': 'SFTP '\n'Server','Endpoint': '0.0.0.0:2240','Uri': 'steam://connect/0.0.0.0:2240'}
    ContainerCPUs: float  # 0.0
    ContainerMemoryMB: int  # 0
    ContainerMemoryPolicy: int  # 0
    Daemon: bool  # False
    DaemonAutostart: bool  # True
    DeploymentArgs: dict[str, str]  # {'FileManagerPlugin.SFTP.SFTPIPBinding': '0.0.0.0','FileManagerPlugin.SFTP.SFTPPortNumber': '2240','GenericModule.App.ApplicationIPBinding': '0.0.0.0','GenericModule.App.ApplicationPort1': '7785','GenericModule.App.ApplicationPort2': '0','GenericModule.App.ApplicationPort3': '0','GenericModule.App.RemoteAdminPort': '0','GenericModule.Meta.Author': 'JasperFirecai2, EnderWolf, '                             'IceOfWraith','GenericModule.Meta.ConfigManifest': 'terrariaconfig.json','GenericModule.Meta.ConfigRoot': 'terraria.kvp','GenericModule.Meta.Description': 'Terraria generic module '\n'with support for '\n'various options.','GenericModule.Meta.DisplayImageSource': 'steam:105600','GenericModule.Meta.DisplayName': 'Terraria','GenericModule.Meta.EndpointURIFormat': 'steam://connect/{0}','GenericModule.Meta.MetaConfigManifest': 'terrariametaconfig.json','GenericModule.Meta.MinAMPVersion': '','GenericModule.Meta.OS': '3','GenericModule.Meta.OriginalSource': 'CubeCoders-AMPTemplates','GenericModule.Meta.URL': 'https://store.steampowered.com/app/105600/Terraria/'},
    DiskUsageMB: int  # 0
    ExcludeFromFirewall: bool  # False,
    FriendlyName: str  # 'VM Terraria',
    IP: str  # '127.0.0.1',
    # InstalledVersion: dict[str, int]  # {'Build': 2,'Major': 2,'MajorRevision': 0,'Minor': 4,'MinorRevision': 0,'Revision': 0}
    InstanceID: str  # '89518e00-3c00-4d6d-93d3-f1faa1541788'
    InstanceName: str  # 'VMTerraria01'
    IsContainerInstance: bool  # False
    IsHTTPS: bool  # False,
    ManagementMode: int  # 10
    Module: str  # 'GenericModule'
    Port: str  # 8097
    ReleaseStream: int  # 10
    Running: bool  # True
    Suspended: bool  # False
    TargetID: str  # '47d31130-25ed-47d3-af50-c0ebd947830d'
    Tags: None | list = field(default=None)
    AMPVersion: AMP_Version | None = field(default=None)
    SpecificDockerImage: str = ""
    ModuleDisplayName: str = ""  # 'Terraria'
    Metrics: Metric | None = field(default=None)
    DisplayImageSource: str = ""  # steam:105600
    Description: str = ""


@dataclass()
class Controller():
    """
    Represents an AMP Controller (aka Target manager) that manages the Instances it has access to.

    """

    AvailableInstances: list[Instance]
    State: State_enum
    AvailableIPs: list[str]
    CanCreate: bool
    CreatesInContainers: bool
    Datastores: list[dict[str, str | int]]
    Description: str
    Disabled: bool
    FriendlyName: str
    Id: int
    InstanceId: str
    IsRemote: bool
    Tags: list[str]
    Platform: dict[str, int | str | bool | AMP_Version | dict[str, int | str]]
    Fitness: dict[str, bool | float | int] | None = None
    LastUpdated: str  # type:ignore

    @property
    def LastUpdated(self) -> datetime:
        """
        Converts our LastUpdated attribute into a Datetime Object.

        Returns:
            datetime: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
        """

        if isinstance(self._LastUpdated, datetime):
            return self._LastUpdated

        return datetime.fromtimestamp(int(self._LastUpdated[6:-2]) / 1000)

    @LastUpdated.setter
    def LastUpdated(self, value: str) -> None:
        self._LastUpdated = value


@dataclass()
class TriggerTasks():
    """
    Tied to `Triggers()`.

    Hold's information regarding AMP Tasks and their status.

    """

    Id: str
    TaskMethodName: str
    ParameterMapping: dict[str, str]
    EnabledState: int
    Locked: bool
    CreatedBy: str
    Order: int


@dataclass()
class Methods():
    """
    Tied to `ScheduleData().AvailableMethods`.

    Hold's information regarding Methods/Events that are available to the Instance. Varies depending on instance type.

    """

    Id: str = ""
    Name: str = ""
    Description: str = ""
    Consumes: list[dict[str, str]] = field(default_factory=list[dict[str, str]])


@dataclass()
class Triggers():
    """
    Tied to `ScheduleData().AvailableTriggers` and `ScheduleData().PopulatedTriggers`

    """

    EnabledState: int
    Tasks: list[TriggerTasks] = field(default_factory=list[dict[str, str]])  # type:ignore TODO - See if this works or breaks.
    Id: str = ""
    Type: str = ""
    Description: str = ""
    TriggerType: str = ""
    Emits: list[str] = field(default_factory=list[str])
    LastExecuteError: bool = field(default=False)
    LastErrorReason: str = field(default="")


@dataclass()
class ScheduleData():
    """
    Represents the Data returned from the AMP API call `get_schedule_data()`

    """

    AvailableMethods: list[Methods] | None = None
    # AvailableTriggers: list[str] | None = None
    AvailableTriggers: list[Triggers] | None = None
    # PopulatedTriggers: list[str] | None = None
    PopulatedTriggers: list[Triggers] | None = None


@dataclass(init=False)
class Players():
    """
    Represents the Data returned from the AMP API call `getUserlist()`
    The attributes are not 100% accurate. Used Minecraft Module as a test.
    `{'6eb7be5e-3d33-4b40-8aab-7889c243cc1a': 'Anth0kage'}`

    """

    id: str = ""
    name: str = ""

    def __init__(self, data: dict[str, str]):
        for id, name in data.items():
            setattr(self, "id", id)
            setattr(self, "name", name)


@dataclass()
class User():
    """
    Represents the Data returned from the AMP API call `getAllAMPUserInfo()`

    """

    CannotChangePassword: bool
    Disabled: bool
    GravatarHash: str
    ID: str
    IsLDAPUser: bool
    IsSuperUser: bool
    IsTwoFactorEnabled: bool
    MustChangePassword: bool
    Name: str
    PasswordExpires: bool
    Permissions: list[str]
    Roles: list[str]
    LastLogin: str  # type:ignore

    @property
    def LastLogin(self) -> datetime:
        """
        Converts our LastLogin attribute into a Datetime Object.

        Returns:
            datetime: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
        """

        if isinstance(self._LastLogin, datetime):
            return self._LastLogin

        return datetime.fromtimestamp(int(self._LastLogin[6:-2]) / 1000)

    @LastLogin.setter
    def LastLogin(self, value: str) -> None:
        self._LastLogin = value


@dataclass()
class SettingSpec():
    """
    Represents the data returns from the AMP API call `getConfig()` or `getConfigs()`

    """

    AlwaysAllowRead: bool
    Category: str
    CurrentValue: str
    Description: str
    EnumValuesAreDeferred: bool
    InputType: str
    IsProvisionSpec: bool
    Keywords: str
    MaxLength: int
    Name: str
    Node: str
    Placeholder: str
    ReadOnly: bool
    ReadOnlyProvision: bool
    RequiresRestart: bool
    Suffix: str
    Tag: str
    ValType: str
    Actions: list[Any] = field(default_factory=list)


@dataclass()
class Role():
    """
    Represents the data returns from the AMP API call `getRole()`

    """

    ID: str
    IsDefault: bool
    Name: str
    Description: str
    Hidden: bool
    Permissions: list[str]
    Members: list[str]
    IsInstanceSpecific: bool
    IsCommonRole: bool
    DisableEdits: bool


@dataclass()
class FileChunk():
    """
    Represents the data returns from AMP API call `getFileChunk()`

    """

    Base64Data: str
    BytesLength: int


@dataclass()
class Directory():
    """
    Represents the data returns from AMP API call `getDirectoryListing()`

    """

    IsDirectory: bool
    IsVirtualDirectory: bool
    Filename: str
    SizeBytes: int
    IsDownloadable: bool
    IsEditable: bool
    IsArchive: bool
    IsExcludedFromBackups: bool
    Created: str  # type:ignore
    Modified: str  # type:ignore

    @property
    def Created(self) -> datetime | str:
        """
        Converts our Created attribute into a Datetime Object.

        Returns:
            datetime | str: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
                `Will return str on windowsOS if out of range(1970-2038)`
        """

        if isinstance(self._Created, datetime):
            return self._Created

        try:
            return datetime.fromtimestamp(int(self._Created[6:-2]) / 1000)
        except OSError:
            # This is to deal with WindowsOS when returning values outside datetime restricted years (1970-2038) as of 2/18/2024
            return self._Created[6:-2]

    @Created.setter
    def Created(self, value: str) -> None:
        self._Created = value

    @property
    def Modified(self) -> datetime | str:
        """
        Converts our Modified attribute into a Datetime Object.

        Returns:
            datetime | str: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
                `Will return str on windowsOS if out of range(1970-2038)`
        """

        if isinstance(self._Modified, datetime):
            return self._Modified

        try:
            return datetime.fromtimestamp(int(self._Modified[6:-2]) / 1000)
        except OSError:
            # This is to deal with WindowsOS when returning values outside datetime restricted years (1970-2038) as of 2/18/2024
            return self._Modified[6:-2]

    @Modified.setter
    def Modified(self, value: str) -> None:
        self._Modified = value


@dataclass()
class Session():
    """
    Represents the data returns from the AMP API call `getActiveAMPSessions()`

    """
    Source: str
    SessionID: str
    Username: str
    SessionType: str
    StartTime: str  # type:ignore
    LastActivity: str  # type:ignore

    @property
    def StartTime(self) -> datetime:
        """
        Converts our StartTime attribute into a Datetime Object.

        Returns:
            datetime: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
        """

        if isinstance(self._StartTime, datetime):
            return self._StartTime

        return datetime.fromtimestamp(int(self._StartTime[6:-2]) / 1000)

    @StartTime.setter
    def StartTime(self, value: str) -> None:
        self._StartTime = value

    @property
    def LastActivity(self) -> datetime:
        """
        Converts our LastActivity attribute into a Datetime Object.

        Returns:
            datetime: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
        """

        if isinstance(self._LastActivity, datetime):
            return self._LastActivity

        return datetime.fromtimestamp(int(self._LastActivity[6:-2]) / 1000)

    @LastActivity.setter
    def LastActivity(self, value: str) -> None:
        self._LastActivity = value


@dataclass
class BukkitPlugin():
    """
    Represents the data returned from any Bukkit API call for a Bukkit Plugin.

    """

    author: dict[str, int]
    category: dict[str, int]
    downloads: int
    file: dict[str, str | int]
    id: int
    likes: int
    links: dict[str, str]
    name: str
    tag: str
    version: dict[str, int | str]
    icon: dict[str, str]
    updateDate: int | None = field(default=None)  # 1708187123
    testedVersions: list[str] = field(default_factory=list[str])
    releaseDate: int | None = field(default=None)  # 1417419240
    rating: dict[str, float | int] = field(default_factory=dict)
    external: bool | None = field(default=None)
    existenceStatus: int | None = field(default=None)
    installedVersion: int | None = field(default=None)
    versions: list[int] | None = field(default=None)
    premium: bool | None = field(default=None)
    sourceCodeLink: str = field(default="")
    supportedLanguages: str = field(default="")
    contributors: str = field(default="")
    donationLink: str = field(default="")


@dataclass
class InstanceDatastore():
    """
    Represents a InstanceDatastore to be used in `add_datastore()`

    AMP must have read/write/execute access to the directory specified in the `Directory` parameter.

    Args:
        Directory: The on-disk location where instances will be stored. Changing this will not affect existing instances, only newly created ones.
        InstanceLimit: The maximum number of instances that can be provisioned on this datastore. Defaults to 0 for unlimited.
        SoftLimitMB: Datastores that reach or exceed this limit in total size will not be considered as deployment targets. This is only a soft limit and does not prevent instances on this datastore from using more space.
        Priority: Instances with a lower priority number are preferred over those with a higher number, all other factors being equal.
        Active: Deactivating a datastore prevents new instances from being provisioned to it. Defaults to True.

    """

    Id: int
    FriendlyName: str
    Description: str
    Directory: str
    SoftLimitMB: int
    Priority: int
    Tags: list[str]
    IsInternal: bool
    InstanceLimit: str = field(default="0")
    Active: bool = field(default=True)
    CurrentUsageMB: int = field(default=-1)
    SanitisedName: str = field(default="None")


@dataclass
class RunningTask():
    """
    Represents the data returned from some API calls that return RunningTask.\n

    https://github.com/p0t4t0sandwich/ampapi-py/blob/main/ampapi/types.py#L887

    """

    IsPrimaryTask: bool
    StartTime: str
    Id: str
    Name: str
    Description: str
    HideFromUI: bool
    FastDismiss: bool
    LastUpdatePushed: str
    ProgressPercent: float
    IsCancellable: bool
    Origin: str
    IsIndeterminate: bool
    State: int
    Status: str


@dataclass
class DeploymentTemplate():
    """
    Used for `update_deployment_template()` API call.

    """

    Id: int
    Name: str
    Description: str
    Module: str
    TemplateInstance: Any  # Unsure what this field is at this time. #TODO - Need to figure this out.
    TemplateRole: str
    TemplateBaseApp: str
    CloneRoleIntoUser: bool
    ZipOverlayPath: str
    MatchDatastoreTags: bool
    SettingMappings: dict[str, str]
    Tags: list[str]
    StartOnBoot: bool = field(default=False)


@dataclass
class Template():
    """
    Represents the data for a deployment template to deploy an instance.

    """

    TemplateID: int  # The ID of the template to be deployed, as per the Template Management UI in AMP itself.
    NewUsername: str | None = field(default=None)  # If specified, AMP will create a new user with this name for this instance. Must be unique. If this user already exists, this will be ignored but the new instance will be assigned to this user.
    NewPassword: str | None = field(default=None)  # If 'NewUsername' is specified and the user doesn't already exist, the password that will be assigned to this user.
    NewEmail: str | None = field(default=None)  # If 'NewUsername' is specified and the user doesn't already exist, the email address that will be assigned to this user.
    RequiredTags: list[str] | None = field(default=None)   # If specified, AMP will only deploy this template to targets that have every single 'tag' specified in their target configuration. You can adjust this via the controller by clicking 'Edit' on the target settings.
    Tag: str | None = field(default=None)  # Unrelated to RequiredTags. This is to uniquely identify this instance to your own systems. It may be something like an order ID or service ID so you can find the associated instance again at a later time. If 'UseTagAsInstanceName' is enabled, then this will also be used as the instance name for the created instance - but it must be unique.
    FriendlyName: str | None = field(default=None)  # A friendly name for this instance. If left blank, AMP will generate one for you.
    Secret: str | None = field(default=None)   # Must be a non-empty strong in order to get a callback on deployment state change. This secret will be passed back to you in the callback so you can verify the request.
    PostCreate: PostCreateActions = field(default=PostCreateActions.DoNothing)
    ExtraProvisionSettings: dict[str, str] | None = field(default=None)   # A dictionary of setting nodes and values to create the new instance with. Identical in function to the provisioning arguments in the template itself.


@dataclass
class RemoteTargetInfo():
    """
    Represents the information from the API call RemoteTargetInfo.\n
    Author: p0t4t0sandwich -> RemoteTargetInfo https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L859

    """

    IPAddressList: list[str]
    PlatformInfo: PlatformInfo
    Datastores: list[InstanceDatastore]
    DeploysInContainers: bool


@dataclass
class PlatformInfo():
    """
    Represents thePlatformInfo tied to RemoteTargetInfo dataclass.\n
    Author: p0t4t0sandwich -> PlatformInfo https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L451

    """

    IsSharedSetup: bool
    AdminRights: int
    CPUInfo: CPUInfo
    InstalledRAMMB: int
    OS: int
    PlatformName: str
    HardwarePlatformName: str
    SystemType: int
    Virtualization: int
    InstalledGlibcVersion: GlibcInfo


@dataclass
class CPUInfo():
    """

    Represents a CPUInfo dataclass.\n
    Author: p0t4t0sandwich -> CPUInfo https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L151

    """

    Sockets: int
    Cores: int
    Threads: int
    Vendor: str
    ModelName: str
    TotalCores: int
    TotalThreads: int


@dataclass
class GlibcInfo():
    """
    Represents a GlibcInfo dataclass.\n
    Author: p0t4t0sandwich -> GlibcInfo https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L423

    """

    Major: int
    Minor: int
    Build: int
    Revision: int
    MajorRevision: int
    MinorRevision: int


@dataclass
class CreateInstance():
    """
    Used for `create_instance()` API call.

    """

    TargetADSInstance: str = field(default="")  # Tied to Auto Configure
    NewInstanceId: str = field(default="")
    Module: str = field(default="")  # Tied to Auto Configure
    InstanceName: str = field(default="")
    FriendlyName: str = field(default="")  # Tied to Auto Configure
    IPBinding: str = field(default="192.168.0.1")
    PortNumber: int = field(default=8001)
    AdminUsername: str = field(default="")
    AdminPassword: str = field(default="")
    ProvisionSettings: dict[str, str] = field(default_factory=dict)
    AutoConfigure: bool = field(default=False)  # When enabled, all settings other than the Module, Target and FriendlyName are ignored and replaced with automatically generated values
    PostCreate: PostCreateActions = field(default=PostCreateActions.DoNothing)
    StartOnBoot: bool = field(default=False)
    DisplayImageSource: str = field(default="")
    TargetDatastore: int = field(default=0)


@dataclass
class InstanceInfo():
    """
    Used for `update_instance_info()` API call.

    """

    InstanceId: str
    FriendlyName: str
    Description: str
    Suspended: bool
    ExcludeFromFirewall: bool
    RunInContainer: bool
    ContainerMemory: int
    ContainerMaxCPU: str  # Unsure exactly what this field is or does.
    ContainerImage: str
    MemoryPolicy: ContainerMemoryPolicy = field(default=ContainerMemoryPolicy.Reserve)
    StartOnBoot: bool = field(default=False)


@dataclass
class AuditLogEntry():
    """
    Represents an entry in the AuditLog.

    """
    Category: str
    Id: int
    Message: str
    Source: str
    User: str
    Timestamp: datetime  # type: ignore

    @property
    def Timestamp(self) -> datetime:
        """
        Converts our Timestamp attribute into a Datetime Object.

        Returns:
            datetime: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
        """
        if isinstance(self._Timestamp, datetime):
            return self._Timestamp

        return datetime.fromtimestamp(int(self._Timestamp[6:-2]) / 1000)

    @Timestamp.setter
    def Timestamp(self, value: str) -> None:
        self._Timestamp = value


@dataclass
class Endpoints():
    """
    Application Endpoints -> See `get_application_endpoints()`

    """
    DisplayName: str
    Endpoint: str
    Uri: str


@dataclass
class PortInfo():
    """
    Represents the data from the AMP API call `get_instance_network_info()`

    """

    Description: str
    IsUserDefined: bool
    PortNumber: int
    Protocol: int
    ProvisionNodeName: str
    Range: int
    Verified: bool


@dataclass
class Provision():
    """
    Represents the data from `get_provision_fitness()`

    """

    Available: bool
    CPUServiceRatio: float
    FreeDiskMB: int
    FreeRAMMB: int
    LoadAvg: float
    RemainingInstanceSlots: int
    Score: float
    ThreadQueueLength: int
    TotalServices: int


@dataclass
class Module():
    """
    Represents the data from the AMP API call `get_module_info()`

    """

    AMPBuild: str
    AMPVersion: str
    APIVersion: str
    AllowRememberMe: bool
    Analytics: bool
    AppName: str
    Author: str
    BasePort: int
    Branding: dict  # ': {'BackgroundURL': '','BrandingMessage': '','CompanyName': '','DisplayBranding': False,'ForgotPasswordURL': '','LogoURL': '','PageTitle': 'Provider Page Title Not Set','ShortBrandingMessage': 'PoweredByAMP','SplashFrameURL': '','SubmitTicketURL': '','SupportText': '','SupportURL': '','URL': '','WelcomeMessage': ''},
    BuildSpec: str
    DisplayBaseURI: str
    EndpointURI: str
    FeatureSet: list
    FriendlyName: str  # ': 'ADS',
    InstanceId: str  # ': '5777d7ac-a2ae-4a72-87f6-64893737a30f',
    InstanceName: str  # ': 'ADS01',
    IsRemoteInstance: bool  # ': False,
    LoadedPlugins: list[str]  # ': ['ADSModule', 'FileManagerPlugin', 'LocalFileBackupPlugin'],
    ModuleName: str  # ': 'ADSModule',
    Name: str  # ': 'Application Deployment Server',
    PrimaryEndpoint: str  # ': '0.0.0.0:2223',
    RequiresFullLoad: bool  # ': True,
    SupportsSleep: bool  # ': False,
    Timestamp: str  # ': '22/03/2024 17:32',
    ToolsVersion: str  # ': '2.4.6.10',
    VersionCodename: str  # ': 'Callisto'}


@dataclass
class TimedTrigger():
    """
    Represents the data of `get_time_interval_trigger()`.

    """

    Description: str  # ': 'Every 5 minutes',
    EnabledState: int  # ': 1,
    Id: str  # ': 'd6a6cbf9-f36d-466e-94ce-d85af3586b4e',
    MatchDays: list[int]  # ': [0, 1, 2, 3, 4, 5, 6],
    MatchDaysOfMonth: list[int]  # ': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    MatchHours: list[int]  # ': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
    MatchMinutes: list[int]  # ': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
    MatchMonths: list[int]  # ': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    Name: str  # ': 'Interval Trigger',
    Order: int  # ': 0,
    Tasks: TriggerTasks  # ': {'f3f334bc-d341-4b6b-beda-a33121439bcd': {'CreatedBy': '4569b62e-5df0-4e58-b063-b1a229e3b4eb','EnabledState': 1,'Id': 'f3f334bc-d341-4b6b-beda-a33121439bcd','Locked': False,'Order': 0,'ParameterMapping': {'Input': ''},'TaskMethodName': 'Event.MinecraftModule.SendConsole'}}}


@dataclass(init=False)
class Diagnostics():
    """
    Represents the data of `get_diagnostics_info()`.

    """
    Application_Name: str  # ': 'AMP',
    Application_Version: str  # ': '2.5.0.0',
    Build_Date: str  # ': '22/03/2024 17:32',
    Build_Spec: str  # ': 'Release',
    CPU_Layout: str  # ': '1S/2C/2T',
    CPU_Model: str  # ': 'AMD Ryzen 7 5700G',
    Codename: str  # ': 'Callisto',
    Installed_RAM: int  # ': '3877',
    InstanceID: str  # ': '5777d7ac-a2ae-4a72-87f6-64893737a30f',
    Last_Arguments: str  # ': '',
    Last_Executable: str  # ': '',
    Last_Process_ID: int  # ': '1333',
    Loaded_Plugins: str  # ': 'FileManagerPlugin, EmailSenderPlugin, WebRequestPlugin,' 'LocalFileBackupPlugin, CommonCorePlugin',
    Module: str  # ': 'ADSModule',
    Module_Application: str  # ': 'Application Deployment',
    Platform: str  # ': 'Linux Mint 21.2',
    Release_Stream: str  # ': 'Mainline',
    System_Type: str  # ': 'x86_64',
    Tools_Version: str  # ': '2.4.6.10',
    Virtualization: str  # ': 'VMware'
    OS: str  # 'Linux',

    def __init__(self, data: dict[str, Any]):
        for key, value in data.items():
            key = key.replace(" ", "_")
            setattr(self, key, value)


@dataclass
class OPWhitelist():
    """
    Represents the results from `get_op_whitelist()`.

    """

    OPList: list = field(default_factory=list)
    Whitelist: list = field(default_factory=list)


@dataclass
class OPList():
    """
    Represents the results from `get_op_whitelist()`.

    """

    level: int
    name: str
    uuid: str


@dataclass
class MCUser():
    """
    Represents the results from `mc_get_whitelist()`.

    """

    name: str
    uuid: str


@dataclass
class Application():
    """
    Represents the results from `get_supported_applications()`.

    """

    Author: str  # ': 'Greelan',
    ContainerReason: str  # ': 'This application has extra requirements or dependencies ''that may not be satisfied by the host system.',
    ContainerSupport: int  # ': 8,
    Description: str  # ': 'Xonotic Dedicated Server',
    DisplayImageSource: str  # ': 'url:https://gitlab.com/xonotic/xonotic/-/raw/master/misc/logos/xonotic_logo.png',
    ExtraSetupStepsURI: str  # ': '',
    FriendlyName: str  # ': 'Xonotic',
    Id: str  # ': '02440481-2c3d-4098-8c5f-8690bd62c442',
    IsServiceSpec: bool  # ': False,
    ModuleName: str  # ': 'GenericModule',
    NoCommercialUsage: bool  # ': False,
    SupportedPlatforms: int  # ': 3}
    Settings: dict = field(default_factory=dict)


@dataclass
class ProvisionSettingInfo():
    """
    Represents the data from `get_provision_arguments()`.

    """

    DefaultValue: str
    Description: str
    EndpointName: str
    Node: str
    Type: str
    ValueRange: int | str


@dataclass
class Backup():
    """
    Represents the results from `get_backups()`.

    """
    CreatedAutomatically: bool  # ': False,
    Description: str  # ': '',
    Id: str  # ': '69bfae19-28dc-4699-8998-d8875970cbad',
    ModuleName: str  # ': 'ADSModule',
    Name: str  # ': 'TestBU',
    SourceOS: int  # ': 2,
    Sticky: bool  # ': True,
    StoredLocally: bool  # ': True,
    StoredRemotely: bool  # ': False,
    TakenBy: str  # ': 'gatekeeper',
    TotalSizeBytes: int  # ': 0}
    Timestamp: datetime  # ': '/Date(1711435525392)/', #type:ignore

    @property
    def Timestamp(self) -> datetime:
        """
        Converts our Timestamp attribute into a Datetime Object.

        Returns:
            datetime: Returns a `Non-Timezone` aware object. Will use OS/machines timezone information.
        """
        if isinstance(self._Timestamp, datetime):
            return self._Timestamp

        return datetime.fromtimestamp(int(self._Timestamp[6:-2]) / 1000)

    @Timestamp.setter
    def Timestamp(self, value: str) -> None:
        self._Timestamp = value
