# API class types
from __future__ import annotations
from typing import Any, Union, NamedTuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


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
    Maintainence = 250
    Indeterminate = 999  # The state is unknown, or doesn't apply (for modules that don't start an external process)


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


@dataclass()
class ActionResult():
    """
    Represents the results of some API calls.
    """
    Status: bool
    Reason: str | None = None


@dataclass()
class Login_UserInfo():
    """
    Represents an AMP users information, tied to `LoginResults()`

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

    def __init__(self, data: str | None = None, Major: int = 0, Minor: int = 0, Revision: int = 0, MinorRevision: int = 0, Build: int = 0) -> None:
        """
        __init__ _summary_

        Args:
            data (str | None, optional): AMP Version as a string; parsed into attributes (Called by `Core/GetUpdateInfo()`). Defaults to None.
            Major (int, optional): Major Version #. Defaults to 0.
            Minor (int, optional): Minor Version #. Defaults to 0.
            Revision (int, optional): Revision Version #. Defaults to 0.
            MinorRevision (int, optional): Minor Revision #. Defaults to 0.
            Build (int, optional): Build #. Defaults to 0.
        """
        params = ["Major", "Minor", "Revision", "MinorRevision", "Build"]
        vars = [Major, Minor, Revision, MinorRevision, Build]
        if data != None:
            vars = data.split(".")

        for i in range(0, len(vars)):
            setattr(self, params[i], vars[i])


@dataclass()
class UpdateInfo():
    """
    Represents AMP API call `Core/GetUpdateInfo`

    """
    UpdateAvailable: bool
    ReleaseNotesURL: str
    Build: str
    Version: AMP_Version  # type:ignore
    ToolsVersion: None | str = None
    PatchOnly: None | bool = None

    @property
    def Version(self) -> AMP_Version:
        """
        Converters our Build str into a data class we can use better.

        Returns:
            AMP_Version: Returns an `AMP_Version` data class
        """
        return AMP_Version(data=self._Version)

    @Version.setter
    def Version(self, value: str) -> None:
        self._Version = value


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
    Active_Users: Metrics_Data
    CPU_Usage: Metrics_Data
    Memory_Usage: Metrics_Data


@dataclass()
class Status():
    """
    Tied to `Updates()`, represents the Instance stats
    """
    State: State_enum
    Uptime: str
    Metrics: Metric


@dataclass()
class InstanceStatus():
    """
    Represents the data returned from `getInstanceStatus()`

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

    Current Port of the related AMP Instance. Tied to `Updates().Ports`
    """
    Listening: bool
    Name: str
    Port: int
    Protocol: int


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
    Represents the data from AMP API call `getUpdates` \n
    """
    ConsoleEntries: list[Console_Entries]
    Status: Status
    Messages: list[Messages]  # No ideal usage at this time.
    Ports: list[Port] | None = None  # No ideal usage at this time.
    Tasks: list[Task] | None = None  # No ideal usage at this time.


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
    Tags: None | list = None
    AMPVersion: AMP_Version | None = None
    SpecificDockerImage: str = ""
    ModuleDisplayName: str = ""  # 'Terraria'
    Metrics: Metric | None = None
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


@dataclass()
class ScheduleData():
    """
    Represents the Data returned from the AMP API call `getScheduleData()`
    """
    AvailableMethods: list[Methods] | None = None
    # AvailableTriggers: list[str] | None = None
    AvailableTriggers: list[Triggers] | None = None
    # PopulatedTriggers: list[str] | None = None
    PopulatedTriggers: list[Triggers] | None = None


@dataclass()
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
class Node():
    """
    Represents the data returns from the AMP API call `getConfig()` or `getConfigs()`

    """
    Actions: list[str]
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
    Repesents the data returns from AMP API call `getFileChunk()`
    """
    Base64Data: str
    BytesLength: int


@dataclass()
class Directory():
    """
    Repesents the data returns from AMP API call `getDirectoryListing()`
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
    Represents a Bukkit Plugin

    """

    author: dict[str, int]
    category: dict[str, int]
    contributors: str
    donationLink: str
    downloads: int
    existenceStatus: int
    external: bool
    file: dict[str, str | int]
    icon: dict[str, str]
    id: int
    likes: int
    links: dict[str, str]
    name: str
    premium: bool
    rating: dict[str, float | int]
    releaseDate: int  # 1417419240
    sourceCodeLink: str
    supportedLanguages: str
    tag: str
    testedVersions: list[str]
    updateDate: int  # 1708187123
    version: dict[str, int | str]
