from __future__ import annotations

import functools
import logging
from dataclasses import dataclass, field, fields
from datetime import datetime
from logging import Logger
from pprint import pformat
from typing import TYPE_CHECKING, Any, ClassVar, Union

from dataclass_wizard.errors import MissingFields
from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Concatenate

    from typing_extensions import ParamSpec, Self, TypeVar

    D = TypeVar("D", bound="Instance")
    T = ParamSpec("T")
    F = TypeVar("F")
    # X = TypeVar("X", bound=DataclassInstance)

from .enums import (
    AccessModeState,
    ADSModeState,
    AMPDownloadMirrorState,
    AMPInstanceState,
    AMPTheme,
    ApplicationUpdatesState,
    AppStartupModeState,
    ContainerMemoryPolicyState,
    DefaultIPBindingState,
    LoggingLevelState,
    PortAssignmentState,
    PostCreateActionsState,
    PostCreateState,
    ReleaseStreamState,
    TwoFactoryModeState,
)

SettingSpecTableAliases = Union[
    AccessModeState,
    PostCreateState,
    ApplicationUpdatesState,
    LoggingLevelState,
    AMPTheme,
    AppStartupModeState,
    TwoFactoryModeState,
    PortAssignmentState,
    DefaultIPBindingState,
    AMPDownloadMirrorState,
    ADSModeState,
    ReleaseStreamState,
]


def attribute_converter(data: dict[str, Any]) -> dict[str, Any]:
    """
    Removes private attributes (aka ``_attribute``) designation from the dict key values.
    - Typically after calling :py:func:`vars`.

    Parameters
    ----------
    data : dict[str, Any]
        The data or object to remove private attributes from as keys.

    Returns
    -------
    dict[str, Any]
        The private attributes removed.
    """

    new_vars: dict[str, Any] = {}
    for key, value in vars(data).items():
        # We do this to avoid any private attributes such as the _controller attribute or _logger.
        # Which can cause infinite recursion as the __repr__ functions would call themselves due to inheritance.
        if key.startswith("_"):
            continue
        else:
            new_vars[key] = value
    return new_vars


@dataclass()
class ActionResult:
    """
    Represents the JSON response data from most API Endpoints.

    Attributes
    ----------
    status : bool
        If the API call was successful.
    reason : Union[str, None]
        If :attr:`status` is ``False`` this will typically have a ``str`` response.
    result : Union[str, None]
        If :attr:`status` is ``True`` this will contain data related to the API call.
    """

    status: bool
    reason: Union[str, None] = field(default=None)
    result: Union[str, None] = field(default=None)

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass()
class AMPVersionInfo:
    """
    Tied to the class attribute for :py:class:`UpdateInfo.build`
    - Currently has a converter function ``v2.6.0.0``
    - ``__repr__`` has been overridden to display in a joined string with build at the end.

    Attributes
    ----------
    major : int
        The major version number of the AMP build.
    minor : int
        The minor version number of the AMP build.
    revision : int
        The revision number of the AMP build.
    minor_revision : int
        The minor revision number of the AMP build.
    build : Union[int, None]
        The build number, defaults to None.

    """

    major: int
    minor: int
    revision: int
    minor_revision: int = 0
    major_revision: Union[int, None] = None
    build: Union[int, None] = None

    @classmethod
    def to_dataclass(cls, data: str, sep: str = ".") -> Union[str, AMPVersionInfo]:
        """
        Parse a string type of the Version into a dataclass.
        - Assumes structure is ``"2.6.0.0"``

        Parameters
        ----------
        data : str
            The string type of the Version to parse.
        sep : str
            The separator to split the string by.

        Returns
        -------
        str | :py:class:`AMPVersionInfo`
            Returns the built dataclass if it succeeds. Otherwise you will get the data passed in back.
        """

        new_data: list[str] = data.split(sep=sep)
        # Unpack the data converted into ints.
        try:
            temp: Self = cls(*[int(entry) for entry in new_data])

        except (UnboundLocalError, MissingFields) as e:
            _logger = logging.getLogger()
            _logger.error("Unable to convert the data %s | Error: %s", data, e)
            return data
        return temp

    def __repr__(self) -> str:
        return f"{self.major}.{self.minor}.{self.revision}.{self.minor_revision} | {self.build}"


@dataclass
class AnalyticsCountryData:
    """
    Represents the JSON response data from :py:class:`AnalyticsSummary.country_data`.

    Attributes
    ----------
    country : str
        The country code; similar to the ISO 3166-1 Alpha-2 format.
    display_session_time : str
        The current display's session time per country.
    session_count: int
        The current number of sessions per country.
    session_time_percent : float
        UNK
    total_session_time : float
        The total session time per country.
    unique_player_count : int
        The unique player count per country.
    unique_player_percent : int
        The unique player percent out of all countries.
    session_percent: int
        The percent of total sessions related to this country.

    """

    country: str
    display_session_time: str
    session_count: int
    session_time_percent: float
    total_session_time: float
    unique_player_count: int
    unique_player_percent: float
    session_percent: float = field(default_factory=float)


@dataclass
class AnalyticsFilter:
    """
    A dataclass to handle filtering for :py:class:`AnalyticsPlugin.get_analytics_summary()`, pass this dataclass in as the :parameter:`filter_`
    - Simply create this class and fill out either :attribute:`username`, :attribute:`user_id` and or :attribute:`country`.


    Attributes
    ----------
    country : str
        The country to filter by. `Must be in ISO 3166-1 Alpha-2 format.`
    first_session : Union[bool, None]
        Whether or not to filter by first session only. Defaults to None.
    meta : Union[Any, None]
        UNK
    username : Union[str , None]
        The username to filter by. Defaults to None.
    user_id : Union[str, None]
        The user_id to filter by, currently using the :attribute:`username` attribute. Defaults to None.
    """

    country: str
    first_session: Union[bool, None] = None
    meta: Union[Any, None] = None
    username: Union[str, None] = None
    user_id: Union[str, None] = None
    # fmt: off
    _country_list: ClassVar[list[str]] = ["AF","AX","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM",
                                          "AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ",
                                          "BM","BT","BO","BQ","BA","BW","BV","BR","IO","BN","BG","BF",
                                          "BI","CV","KH","CM","CA","KY","CF","TD","CL","CN","CX","CC",
                                          "CO","KM","CG","CD","CK","CR","CI","HR","CU","CW","CY","CZ",
                                          "DK","DJ","DM","DO","EC","EG","SV","GQ","ER","EE","ET","FK",
                                          "FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH",
                                          "GI","GR","GL","GD","GP","GU","GT","GG","GN","GW","GY","HT",
                                          "HM","VA","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM",
                                          "IL","IT","JM","JP","JE","JO","KZ","KE","KI","KP","KR","KW",
                                          "KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK",
                                          "MG","MW","MY","MV","ML","MT","MH","MQ","MR","MU","YT","MX",
                                          "FM","MD","MC","MN","ME","MS","MA","MZ","MM","NA","NR","NP",
                                          "NL","NC","NZ","NI","NE","NG","NU","NF","MP","NO","OM","PK",
                                          "PW","PS","PA","PG","PY","PE","PH","PN","PL","PT","PR","QA",
                                          "RE","RO","RU","RW","BL","SH","KN","LC","MF","PM","VC","WS",
                                          "SM","ST","SA","SN","RS","SC","SL","SG","SX","SK","SI","SB",
                                          "SO","ZA","GS","SS","ES","LK","SD","SR","SJ","SZ","SE","CH",
                                          "SY","TW","TJ","TZ","TH","TL","TG","TK","TO","TT","TN","TR",
                                          "TM","TC","TV","UG","UA","AE","GB","US","UM","UY","UZ","VU",
                                          "VE","VN","VG","VI","WF","EH","YE","ZM","ZW",]
    # fmt: on
    def __post_init__(self) -> None:
        if self.username is None and self.user_id is None and self.first_session is None and self.country is None:
            raise ValueError("At least one of these attributes must be set | (username, user_id, country, first_session).")

        if self.country is not None and self.country not in self._country_list:
            raise ValueError(f"The Country attribute must be in ISO 3166-1 Alpha-2 format. | Received: {self.country}")


@dataclass
class AnalyticsStats:
    """
    Represents the JSON response data from :py:class:`AnalyticsSummary.stats`.

    Attributes
    ----------
    name : str
        The Name of the current :py:class:`AnalyticsStats`
        - ["Total Sessions", "Unique Users", "New Users", "Total Session Time", "Bounce Rate", "Session Duration", "Sessions Per User", "Longest Session"]
        - *note* Bounce Rate = "Sessions where the user joined and then quickly left again."
    description : str
        The description of :py:class:`AnalyticsStats.name` that is being tracked!
    current : Union[int, float]
        Represents the actual value; similar to :attribute:`display_value` but in a raw representation.
        - Could be seconds, minutes or a count value depending on the :attribute:`description`.
    display_value : Union[int, str, float]
        The value being displayed on the Analytics Summary Page after formatting.
    difference : Union[int, str, float]
        Has values such as "Infinity", 0, and 0.0.
    previous : Union[int, str, float]
        UNK
    """

    name: str
    description: str
    current: Union[int, str, float]
    display_value: Union[int, str, float]
    difference: Union[int, str, float]
    previous: Union[int, str, float]


@dataclass
class AnalyticsSummary:
    """
    Represents the JSON response data from :py:func:`AnalyticsPlugin.get_analytics_summary()`.

    Attributes
    ----------
    busiest_time : dict[str, Union[int, str]]
        UNK. Default is a list.
    country_data : list[:py:class:`AnalyticsCountryData`]
        The Country information for the summary. Default is a list.
    graph_data : list[dict[str, Union[int, str]]]
        The Data displayed on the Web UI panel Analytics Menu. Default is a list.
    is_demo : bool
        UNK. Default is False.
    quietest_time : dict[str, Union[int, str]]
        UNK. Default is a dict.
    stats : list[:class:`AnalyticsStats`]
        The Analytics Stats of the summary. Default is a list.
    top_players : list[:class:`AnalyticsTopPlayers`]
        The TOP players from the summary. Default is a list.
    """

    busiest_time: dict[str, Union[int, str]] = field(default_factory=dict)
    country_data: list[AnalyticsCountryData] = field(default_factory=list)
    graph_data: list[dict[str, Union[int, str]]] = field(default_factory=list)
    is_demo: bool = field(default=False)
    quietest_time: dict[str, Union[int, str]] = field(default_factory=dict)
    stats: list[AnalyticsStats] = field(default_factory=list)
    top_players: list[AnalyticsTopPlayers] = field(default_factory=list)

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class AnalyticsTopPlayers:
    """
    Represents the JSON Response data from :class:`Analytics_Summary.topPlayers`.

    Attributes
    ----------
    display_session_time : str
        Display the session time.
    percent : float
        The percent of how much this value in comparison to :attribute:`total_session_time`.
    total_session_time : float
        The total amount of session time the user has for the day.
    username : str
        The name of the session user. Like an IGN.
    """

    display_session_time: str
    percent: float
    total_session_time: float
    username: str


@dataclass()
class APIParams:
    """
    A class to hold Login information for the AMP API.\n
    - ``**DO NOT SET OR UPDATE**``-> :attribute:`_sessions` The API handle's this.

    Attributes
    ----------
    url : str
        The URL to access the Web GUI panel home page/login page.
        - Must be relative to the machine running the API.
    user : str
        The AMP User name to login to the Web Panel.
    password: str
        The AMP User password to login to the Web Panel.
    use_2fa : bool
        To use :py:class:`TOTP` 2 Factor Authentication. Default is False.
    token : str
        The 2 Factor Authentication Token Code to generate a :py:class:`TOTP` code. Default is ""

    """

    url: str
    user: str
    password: str
    use_2fa: bool = False
    token: str = ""
    _sessions: dict[str, APISession] = field(init=False, default_factory=dict)


@dataclass()
class APISession:
    """
    Stores the Session ID and the TTL usage for :py:class:`APIParams._session`.

    Attributes
    ----------
    id : str
        The ``SESSIONID`` dict key from the JSON response of :func:`Login()`.
    ttl : datetime
        The time to live of the :attribute:`id`. This can be adjusted by :py:class:`Base.session_ttl` value.
    """

    id: str
    ttl: datetime


@dataclass
class Application:
    """
    Represents the JSON response data from `MinecraftModule.get_supported_applications()`.
    - Shows Template/App information. Similar to the all the applications in a repo lists.


    Attributes
    ----------
    author : str
        The author of the application/template.
    container_reason : str
        The reason the application is using a container, if any.
    container_support : int
        UNK - Unsure what this value is for.
    description : str
        A brief description of what the application is.
    display_image_source : str
        The url for the application image. Typically what you see as the Instance Banner.
    extra_setup_steps_uri : str
        UNK
    friendly_name : str
        A formatted version of the name.
    id : str
        A unique ID for the application.
    is_service_spec : bool
        UNK.
    module_name : str
        The type of Module this application uses. (eg. "Minecraft", "Generic")
    no_commercial_usage : bool
        As the attribute implies; if it's for commercial usage or not.
    supported_platforms : int
        UNK
    settings : dict[str, Any]
        A dict of Instance specific settings to apply for this application.
    """

    author: str
    container_reason: str
    container_support: int
    description: str
    display_image_source: str
    extra_setup_steps_uri: str
    friendly_name: str
    id: str
    is_service_spec: bool
    module_name: str
    no_commercial_usage: bool
    supported_platforms: int
    settings: dict = field(default_factory=dict)

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class AuditLogEntry:
    """
    Represents the JSON response data from :py:func:`Core.get_audit_log_entries()`

    Attributes
    ----------
    acknowledged : bool
        UNK
    category : str
        The type of log entry.
    event_type : int
        The type of event that occurred.
    id : int
        UNK
    message : str
        The message tied to the log entry.
    source : str
        UNK
    user : str
        The AMP Username tied to the log entry.
    timestamp : str | datetime
        The timestamp comes in as  ISO format and __post_init__() converts it into a datetime object.
    """

    acknowledged: bool
    category: str
    event_type: int
    id: int
    message: str
    source: str
    user: str
    timestamp: str  # type:ignore

    def __post_init__(self) -> None:
        self.timestamp: datetime = datetime.fromisoformat(self.timestamp)  # type:ignore

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class Backup:
    """
    Represents the JSON response data from :py:func:`ADSModule.get_backups()`.

    Attributes
    ----------
    created_automatically : bool
        If the backup was created by a Scheduled Task.
    description : str
        The description for the backup; if any.
    id : str
        The backup GUID.
    module_name : str
        What type of Instance that created the backup. *eg. Minecraft, ADS, Generic
    name : str
        The name of the backup.
    source_os : int
        Unsure. I believe there is an ENUM correlation for which int value is which type of OS
    sticky : bool
        If the Backup is Sticky.
    stored_locally : bool
        If the backup is local or not.
    stored_remotely : bool
        If the backup is stored in S3/Cloud or similar.
    taken_by :
        Who created the backup.
    total_size_bytes : int
        The total size of the backup is bytes.
    timestamp : str | datetime
        The timestamp comes in as  ISO format and __post_init__() converts it into a datetime object.
    """

    created_automatically: bool  # ': False,
    description: str  # ': '',
    id: str  # ': '69bfae19-28dc-4699-8998-d8875970cbad',
    module_name: str  # ': 'ADSModule',
    name: str  # ': 'TestBU',
    source_os: int  # ': 2,
    sticky: bool  # ': True,
    stored_locally: bool  # ': True,
    stored_remotely: bool  # ': False,
    taken_by: str  # ': 'gatekeeper',
    total_size_bytes: int  # ': 0}
    timestamp: str  # ': '/Date(1711435525392)/' #type:ignore

    def __post_init__(self) -> None:
        self.timestamp: datetime = datetime.fromtimestamp(int(self.timestamp[6:-2]) / 1000)  # type:ignore

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class BukkitPlugin:
    """
    Represents the JSON response data from any Bukkit API call. *Most notable related to :py:class:`MinecraftModule`.

    Attributes:
    -----------
    author : dict[str, int]
        The author's name and ID tied to the author as a dict key, value pair.
    category : dict[str, int]
        The category name and ID tied to the category as a dict key, value pair.
    downloads : int
        The number of downloads the plugin has had.
    file : dict[str, Union[str, int]]
        UNK
    id : int
        The ID of the plugin.
    likes : int
        The number of likes the plugin has had.
    links : dict[str, str]
        The links related to the plugin. Unsure of data structure.
    name : str
        The name of the plugin.
    tag : str
        The tag related to the plugin.
    version : dict[str , Union[int, str]]
        The version information of the plugin.
    icon : dict[str, str]
        The icon name and url in a dict key, value pair.
    tested_version : list[str]
        The tested versions of the plugin. Default is a list
    update_date : Union[int, None]
        The timestamp of when it was updated. Default is None
    release_date : Union[int, None]
        The timestamp of when it was released. Default is None
    rating : dict[str, Union[float, int]]
        The rating. Default is a dict.
    external : Union[bool, None]
        If the plugin is external or not. Default is None
    existence_status : Union[int, None]
        UNK. Default is None
    installed_version : Union[int, None]
        The plugin version currently installed. Default is None.
    versions : Union[list[int], None]
        The plugins alternate versions, if any. Default is None.
    premium : Union[bool, None]
        If the plugin is premium or not. Default is None.
    source_code_link : str
        The URL to the source code. Default is "".
    supported_languages : str
        The languages this plugin supports. Default is "".
    contributors : str
        The contributors to the source code/plugin. Default is "".
    donation_link : str
        The URL to donate/support the plugin. Default is "".
    """

    author: dict[str, int]
    category: dict[str, int]
    downloads: int
    file: dict[str, Union[str, int]]
    id: int
    likes: int
    links: dict[str, str]
    name: str
    tag: str
    version: dict[str, Union[int, str]]
    icon: dict[str, str]
    tested_versions: list[str] = field(default_factory=list[str])
    update_date: Union[int, None] = field(default=None)  # 1708187123
    release_date: Union[int, None] = field(default=None)  # 1417419240
    rating: dict[str, Union[float, int]] = field(default_factory=dict)
    external: Union[bool, None] = field(default=None)
    existence_status: Union[int, None] = field(default=None)
    installed_version: Union[int, None] = field(default=None)
    versions: Union[list[int], None] = field(default=None)
    premium: Union[bool, None] = field(default=None)
    source_code_link: str = field(default="")
    supported_languages: str = field(default="")
    contributors: str = field(default="")
    donation_link: str = field(default="")

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass()
class ConsoleEntries:
    """
    Represents the JSON response data from :py:class:`Updates().console_entries`.


    Attributes
    ----------
    contents : str
        The contents of the console entry.
    source : str
        The source of the console entry. eg "Server thread/INFO, ..."
    type : str
        The type of message. eg "Console, Chat, Error, ...
    timestamp : str | datetime
        The timestamp comes in as  ISO format and __post_init__() converts it into a datetime object.
    """

    contents: str
    source: str
    type: str
    timestamp: str  # type: ignore

    def __post_init__(self) -> None:
        self.timestamp: datetime = datetime.fromisoformat(self.timestamp)  # type:ignore

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass()
class Controller:
    """
    Represents the JSON response data for an AMP Controller Instance.
    - See :py:func:`ADSModule.get_instances(include_self = True)` making the first instance "typically" the Controller Instance. AKA ``ADS01``.

    Attributes
    -----------
    id : int
        UNK
    disabled : bool
        If the Controller is Disabled or not.
    is_remote : bool
        If the Controller is remote or not.
    platform : :py:class:`PlatformInfo`
        Platform information related to the Instance.
    datastores : list[dict[str, Union[str, int]]]
        The Datastores that the Controller has access to.
    creates_in_containers : bool
        The Controller will create the Instances in containers.
    can_create : bool
        If the Controller can create Instances or not.
    available_instances : list[:class:`Instance`]
        A list of AMP Instances the Controller/ADS has permissions to see.
        - Similar to what you see when you log into AMP web GUI and see the Instances list.
        - This attribute is cached and will require calling `:py:class:`ADSModule.get_instances()` to access the API converted class objects.
            - See the :py:class:`AMPControllerInstance.instances` attribute.
    available_ips : list[str]
        The list of available IPs the Controller/Instance has.
    tags : list[str]
        The tags related to the Controller/Instance.
    url : str
        The URL for the Controller/Instance.
    last_updated : Union[str, datetime]
        The last_updated comes in as  ISO format and __post_init__() converts it into a datetime object.
    instance_id : str
        The Controller/Instance ID tied to the Instance. Default is "0".
    state : :py:class:`AMPInstanceState`
        The state the Controller/Instance is in. See enum :py:class:`AMPInstanceState`. Default is ``AMPInstanceState.UNDEFINED``.
    fitness : Union[Fitness, None]
        UNK.
    friendly_name : str
        The Controller/Instance friendly name. Default is "None".
    state_reason : str
        UNK. Default is "".
    description : str
        Controller/Instance description. Default is "".
    tags_list : Union[list[str]]
        The list of tags related to the Controller/Instance if any. Default is None.

    """

    id: int
    disabled: bool
    is_remote: bool
    platform: PlatformInfo
    datastores: list[dict[str, Union[str, int]]]
    creates_in_containers: bool
    can_create: bool
    available_instances: list[Instance]
    available_ips: list[str]
    tags: list[str]
    url: str
    last_updated: str  # type: ignore
    instance_id: str = "0"
    state: AMPInstanceState = AMPInstanceState.undefined
    fitness: Union[Fitness, None] = field(default=None)
    friendly_name: str = "None"
    state_reason: str = ""
    description: str = ""
    tags_list: Union[list[str], None] = field(default=None)

    def __post_init__(self) -> None:
        self.last_updated: datetime = datetime.fromisoformat(self.last_updated)  # type: ignore

    def __hash__(self) -> int:
        return hash(self.instance_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.instance_id == other.instance_id

    def __repr__(self) -> str:
        new_vars: dict[str, Any] = {}
        for key, value in vars(self).items():
            # We do this to avoid any private attributes such as the _controller attribute or _logger.
            if key.startswith("_"):
                continue
            else:
                new_vars[key] = value
        return pformat(new_vars)

        # res = f"Type: {type(self)} | ID : {id(self)}\n"
        # res += f"Name: {self.friendly_name}\nInstance ID: {self.instance_id}\n"
        # res += f"Url: {self.url}\n"
        # res += f"Instance State: {self.state.name}\n"
        # res += f"Instances:\n{self.available_instances}"
        # res += "\n"
        # return res


@dataclass
class CPUInfo:
    """

    Represents the JSON response data from :py:class:`PlatformInfo.cpu_info` attribute.\n
        - Original Author: p0t4t0sandwich
            - :py:class:`CPUInfo` : https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L151

    Attributes
    ----------
    sockets : int
        The number of CPU sockets the AMP Instance has access to.
    cores : int
        The number of cores the AMP Instance has access to.
    threads : int
        The number of threads the AMP Instance has access to.
    vendor : str
        The vendor of the CPU.
    model_name : str
        The model name of the CPU.
    total_cores : int
        The number of total cores the AMP Instance has access to.
    total_threads : int
        The number of total threads the AMP Instance has access to.
    """

    sockets: int
    cores: int
    threads: int
    vendor: str
    model_name: str
    total_cores: int
    total_threads: int

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class CreateInstance:
    """
    Used for :py:func:`ADSModule.create_instance()` API call.

    Attributes
    ----------
    target_ads_instance : str
        The Target instance ID to tie this Instance to.
    friendly_name : str
        The Instance friendly name, this is what you see in the web GUI.
    module : str
        The Instance module it will use.
    new_instance_id : str
        UNK
    instance_name : str
        The name for the Instance, similar to :py:attribute:`friendly_name`.
    ip_binding : str
        The IP to assign to the Instance. See :py:class:`Controller.available_ips`.
    port_number : int
        The Port to assign to the Instance.
        - Unsure if this respects port ranges of the ADS or not.
    admin_username : str
        UNK
    admin_password : str
        The password for the :attribute:`admin_username`.
    provision_settings : dict[str, str]
        UNK
    auto_configure : bool
        When enabled, all settings other than the module, target and friendly_name are ignored and replaced with automatically generated values
    post_create : :class:`PostCreateActionsState`
        The action to take after creating the instance. Defaults to :class:`PostCreateActionsState.do_nothing`
    start_on_boot : bool
        If the instance starts on boot or not. Default is False.
    display_image_source : str
        If the instance has a banner to display, you can define it here. Default is "".
    target_datastore : int
        The Datastore ID to create this Instance on.
        - See :py:class:`Controller.datastores` ID values.
    """

    target_ads_instance: str  # Tied to Auto Configure
    friendly_name: str  # Tied to Auto Configure
    module: str  # Tied to Auto Configure
    new_instance_id: str = field(default="")
    instance_name: str = field(default="")
    ip_binding: str = field(default="192.168.0.1")
    port_number: int = field(default=8001)
    admin_username: str = field(default="")
    admin_password: str = field(default="")
    provision_settings: dict[str, str] = field(default_factory=dict)
    auto_configure: bool = field(default=False)
    post_create: PostCreateActionsState = field(default=PostCreateActionsState.do_nothing)
    start_on_boot: bool = field(default=False)
    display_image_source: str = field(default="")
    target_datastore: int = field(default=0)

    # TODO - Implement attribute checking.
    # def __post_init__(self):
    # if self.auto_configure is False:
    # if any other attributes are NOT set we should error out or ...
    # possibly default all values to None and check for NONE; raise an error so someone doesn't miss a setting?
    # Having default values could be an issue if they forget to set something with auto_configure is False.


class DeploymentTemplate:
    """
    Used for :py:func:`ADSModule.update_deployment_template()` API call.
    - Your pre-created data structure to be parsed for the required API parameters.

    Attributes
    ----------
    clone_role_into_user : bool
        Clone the :attribute:`template_role` to the users of this template.
    description : str
        The description of the deployment template.
    id : int
        The ID of the deployment template.
    module : str
        The AMP Instance module type. eg. "Generic", "Minecraft"
    name : str
        The deployment template name.
    template_base_app : str
        The application that is template is used for.
    template_instance : Any
        UNK
    template_role : str
        The template role name, similar to the AMP User Roles.
    match_datastore_tags : bool
        To force match the datastore tags; if any.
    settings_mappings : dict[str, str]
        A dictionary of setting mappings.
    start_on_boot : bool
        If the Instance should start on ADS01/Controller boot or not. Default is False.
    tags: list[str]
        The list of tags to assign to the template or that belong to the template.
    zip_overlay_path : bool
        To zip the overlay path.

    """

    __slots__ = (
        "clone_role_into_user",
        "description",
        "id",
        "match_datastore_tags",
        "module",
        "name",
        "settings_mappings",
        "start_on_boot",
        "tags",
        "template_base_app",
        "template_instance",
        "template_role",
        "zip_overlay_path",
    )

    def __init__(
        self,
        id: int,  # noqa: A002 # This is due to id overshadowing Python built-ins.
        name: str,
        description: str,
        module: str,
        template_instance: Any,
        template_role: str,
        template_base_app: str,
        clone_role_into_user: bool,
        zip_overlay_path: str,
        match_datastore_tags: bool,
        settings_mappings: dict[str, str],
        tags: list[str],
        start_on_boot: bool = False,
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.module: str = module
        self.template_instance = template_instance
        self.template_role: str = template_role
        self.template_base_app: str = template_base_app
        self.clone_role_into_user: bool = clone_role_into_user
        self.zip_overlay_path: str = zip_overlay_path
        self.match_datastore_tags: bool = match_datastore_tags
        self.settings_mappings: dict[str, str] = settings_mappings
        self.tags: list[str] = tags
        self.start_on_boot: bool = start_on_boot

    def to_dict(self) -> dict[str, Any]:
        """
        As the function name implies; converts the class to a dict.

        Returns
        -------
        dict[str, Any]
            Returns the class attributes in a key, value paired dict.
        """
        temp: dict[str, Any] = {}
        for key in self.__slots__:
            temp[key] = getattr(self, key)
        return temp


@dataclass()
class Diagnostics:
    """
    Represents the JSON response data from :class:`Core.get_diagnostics_info()`.

    Attributes
    ----------
    application_name : str
        The Instance application name.
    application_version : str
        The Instance application version.
    build_date : str
        The date of the AMP Instance build.
    build_spec : str
        Similar to :attribute:`release_stream`.
    cpu_layout : str
        Number of Sockets, Cores and Threads *eg 1S/2C/10T
    cpu_model : str
        The name of the CPU.
    codename : str
        The release/build code name.
    installed_ram : int
        The amount of installed ram on the system.
    instance_id : str
        The Instance GUID
    last_arguments : str
        The last used arguments when running the Instance.
    last_executable : str
        The last used file executable for the Instance.
    last_process_id : int
        The last used process ID.
    loaded_plugins : str
        The AMP loaded plugin's for the Instance.
    module : str
        The Instance module. *eg ADSModule, Minecraft, Generic*
    module_application : str
        The Instance application.
    network_mode : Any
        UNK
    platform : str
        The machine full name of the Operating System.
    release_stream : str
        Mainline, Developer, etc
    system_type : str
        The bit type of the Instance Operating System.
    tools_version : str
        The version of the build tools for the Instance.
    virtualization : str
        If the system is using a VM or not. *eg VMware*
    os : str
        The machine Operating System.
    """

    application_name: str  # ': 'AMP',
    application_version: str  # ': '2.5.0.0',
    build_date: str  # ': '22/03/2024 17:32',
    build_spec: str  # ': 'Release',
    cpu_layout: str  # ': '1S/2C/2T',
    cpu_model: str  # ': 'AMD Ryzen 7 5700G',
    codename: str  # ': 'Callisto',
    installed_ram: int  # ': '3877',
    instance_id: str  # ': '5777d7ac-a2ae-4a72-87f6-64893737a30f',
    last_arguments: str  # ': '',
    last_executable: str  # ': '',
    last_process_id: int  # ': '1333',
    loaded_plugins: (
        str  # ': 'FileManagerPlugin, EmailSenderPlugin, WebRequestPlugin,' 'LocalFileBackupPlugin, CommonCorePlugin',
    )
    module: str  # ': 'ADSModule',
    module_application: str  # ': 'Application Deployment',
    network_mode: Any
    platform: str  # ': 'Linux Mint 21.2',
    release_stream: str  # ': 'Mainline',
    system_type: str  # ': 'x86_64',
    tools_version: str  # ': '2.4.6.10',
    virtualization: str  # ': 'VMware'
    os: str  # 'Linux',

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass()
class Directory:
    """
    Represents the data returns from AMP API call `FileManagerPlugin.get_directory_listing()`

    """

    is_directory: bool
    is_virtual_directory: bool
    filename: str
    size_bytes: int
    is_downloadable: bool
    is_editable: bool
    is_archive: bool
    is_excluded_from_backups: bool
    created: str  # type: ignore
    modified: str  # type: ignore

    def __post_init__(self) -> None:
        self.created: datetime = datetime.fromtimestamp(self.created)  # type: ignore
        self.modified: datetime = datetime.fromtimestamp(self.modified)  # type: ignore


@dataclass
class Endpoints:
    """
    Application Endpoints -> See `ADSModule.get_application_endpoints()`

    """

    display_name: str
    endpoint: str
    uri: str


@dataclass()
class FileChunk:
    """
    Represents the data returns from AMP API call `FileManagerPlugin.get_file_chunk()`

    """

    base_64_data: str
    bytes_length: int


@dataclass()
class Fitness:
    """
    Represents the :py:class:`Instance.fitness` attribute.

    Attributes
    ----------
    score_description : str
        A summary of the "remaining slots" aka the number of Instances you have left to create.
        - Includes the amount of "Free Ram" and "CPU Ratio".
    """

    available: bool
    total_services: int
    free_ram_mb: int
    free_disk_mb: int
    cpu_service_ratio: float
    thread_queue_length: int
    load_avg: float
    remaining_instance_slots: int
    score: float
    score_description: str
    score_zero_factors: list


@dataclass
class InstanceDatastore:
    """
    Represents a InstanceDatastore to be used in `ADSModule.add_datastore()`

    This class is also used in update_datastore, get_datastores, get_datastore

    AMP must have read/write/execute access to the directory specified in the `Directory` parameter.

    Parameters
    -----------
    directory:
        The on-disk location where instances will be stored. Changing this will not affect existing instances, only newly created ones.
    instance_limit:
        The maximum number of instances that can be provisioned on this datastore. Defaults to 0 for unlimited.
    soft_limit_mb:
        Datastores that reach or exceed this limit in total size will not be considered as deployment targets. This is only a soft limit and does not prevent instances on this datastore from using more space.
    priority:
        Instances with a lower priority number are preferred over those with a higher number, all other factors being equal.
    active:
        Deactivating a datastore prevents new instances from being provisioned to it. Defaults to True.

    """

    id: int
    friendly_name: str
    description: str
    directory: str
    soft_limit_mb: int
    priority: int
    tags: list[str]
    is_internal: bool
    instance_limit: str = field(default="0")
    active: bool = field(default=True)
    current_usage_mb: int = field(default=-1)
    sanitized_name: str = field(default="None")


@dataclass
class InstanceInfo:
    """
    Used for `ADSModule.update_instance_info()` API call.

    """

    instance_id: str
    friendly_name: str
    description: str
    suspended: bool
    exclude_from_firewall: bool
    run_in_container: bool
    container_memory: int
    container_max_cpu: str  # Unsure exactly what this field is or does.
    container_image: str
    memory_policy: ContainerMemoryPolicyState = field(default=ContainerMemoryPolicyState.reserve)
    start_on_boot: bool = field(default=False)
    welcome_message: Union[str, None] = field(default=None)


@dataclass(slots=True)
class Instance:
    """
    Represents the data from the AMP API call `ADSModule.get_instance()` or a list of these from `ADSModule.get_instances()`

    """

    application_endpoints: list[dict[str, str]]
    app_state: AMPInstanceState
    container_memory_mb: int
    container_memory_policy: int
    daemon: bool
    daemon_autostart: bool
    deployment_args: dict[str, str]
    disk_usage_mb: int
    exclude_from_firewall: bool
    friendly_name: str
    ip: str
    instance_id: str
    instance_name: str
    is_container_instance: bool
    is_https: bool
    management_mode: int
    module: str
    port: str
    release_stream: int
    running: bool
    suspended: bool
    target_id: str
    amp_version: Union[str, dict, AMPVersionInfo, None] = field(default=None)
    container_cpus: float = field(default=0.0)
    tags: Union[None, list] = field(default=None)
    module_display_name: str = ""
    metrics: Union[Metric, None] = field(default=None)
    display_image_source: str = ""
    description: str = ""

    _instance_offline: str = "The requested instance is not available at this time."

    def __post_init__(self) -> None:
        if self.amp_version is not None:
            # This is only used for older versions of AMP v ``>2.6.0.0``  and earlier.
            if isinstance(self.amp_version, dict):
                try:
                    setattr(self, "amp_version", AMPVersionInfo(**self.amp_version))
                except Exception as e:
                    _logger: Logger = logging.getLogger()
                    _logger.warning("We attempted to unpack <self.amp_version> and failed %s", e)
                    return
            # Per Mike and Developers of AMP state they will be using string versions from `2.6.0.0` and this handles that.
            if isinstance(self.amp_version, str):
                setattr(self, "amp_version", AMPVersionInfo.to_dataclass(self.amp_version))

    def __hash__(self) -> int:
        return hash(self.instance_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.instance_id == other.instance_id

    def __repr__(self) -> str:
        res: str = f"Type: {type(self)} | ID: {id(self)}\n"
        res += f"Name: {self.instance_name}\nInstance ID: {self.instance_id}\n"
        res += f"Application State: {self.app_state.name}\nInstance Running: {self.running}\nModule: {self.module}\nPort: {self.port}"
        res += "\n"
        return res

    def __lt__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.instance_id < other.instance_id

    @staticmethod
    def online(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """
        Checks the :attr:`running` property and raises :exc:`ConnectionError` if the attribute is equal to "False".

        Raises
        --------
        :exc:`ConnectionError`
            The requested instance is not currently running at this time.
        """

        @functools.wraps(wrapped=func)
        def wrapper_online(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            if self.running is True:
                return func(self, *args, **kwargs)
            else:
                raise ConnectionError(self._instance_offline)

        return wrapper_online


@dataclass()
class InstanceStatus:
    """
    Represents the data returned from `ADSModule.get_instance_statuses()`

    """

    instance_id: str
    running: bool


@dataclass()
class LoginResults:
    """
    Represents an AMP Login response.

    """

    success: bool
    result: int
    permissions: list[str] = field(default_factory=list)
    result_reason: str = ""
    session_id: str = ""
    remember_me_token: str = ""
    user_info: Union[LoginUserInfo, None] = None  # second data class


@dataclass()
class LoginUserInfo:
    """
    Represents an AMP users information, tied to `LoginResults()` along with the endpoint `Core.get_amp_users_summary()`

    """

    id: str
    username: str
    is_two_factor_enabled: bool
    disabled: bool
    gravatar_hash: str
    is_ldap_user: bool
    last_login: str  # type: ignore
    email_address: str = ""

    def __post_init__(self) -> None:
        self.last_login: datetime = datetime.fromtimestamp(int(self.last_login[6:-2]) / 1000)  # type:ignore


@dataclass
class MCUser:
    """
    Represents the results from `MinecraftModule.mc_get_whitelist()`.

    """

    name: str
    uuid: str


@dataclass()
class Messages:
    """
    Represents a Message from the dataclass `Updates().Messages`\n
    * Not sure what generates these inside AMP or where to find them.*

    """

    age_minutes: int
    expired: bool
    id: str
    message: str
    source: str


@dataclass()
class Methods:
    """
    Tied to `ScheduleData().AvailableMethods`.

    Hold's information regarding Methods/Events that are available to the Instance. Varies depending on instance type.

    """

    id: str = ""
    name: str = ""
    description: str = ""
    consumes: list[dict[str, str]] = field(default_factory=list[dict[str, str]])


@dataclass()
class Metric:
    """
    The Metrics dataclass for AppStatus().Metrics and Instance().Metrics, houses all the Metrics information.

    """

    active_users: Union[None, MetricsData] = field(default=None)
    cpu_usage: Union[None, MetricsData] = field(default=None)
    memory_usage: Union[None, MetricsData] = field(default=None)


@dataclass()
class MetricsData:
    """
    Represents the data from `Metrics()`

    """

    raw_value: int
    max_value: int
    percent: int
    units: str
    color: Union[None, str] = None
    color2: Union[None, str] = None
    color3: Union[None, str] = None


@dataclass
class Module:
    """
    Represents the data from the AMP API call `Core.get_module_info()`

    """

    amp_build: str
    amp_version: str
    api_version: str
    allow_remember_me: bool
    analytics: bool
    app_name: str
    author: str
    base_port: int
    branding: dict  # ': {'BackgroundURL': '','BrandingMessage': '','CompanyName': '','DisplayBranding': False,'ForgotPasswordURL': '','LogoURL': '','PageTitle': 'Provider Page Title Not Set','ShortBrandingMessage': 'PoweredByAMP','SplashFrameURL': '','SubmitTicketURL': '','SupportText': '','SupportURL': '','URL': '','WelcomeMessage': ''},
    build_spec: str
    display_base_uri: str
    end_point_ur: str
    feature_set: list
    friendly_name: str  # ': 'ADS',
    instance_id: str  # ': '5777d7ac-a2ae-4a72-87f6-64893737a30f',
    instance_name: str  # ': 'ADS01',
    is_remote_instance: bool  # ': False,
    loaded_plugins: list[str]  # ': ['ADSModule', 'FileManagerPlugin', 'LocalFileBackupPlugin'],
    module_name: str  # ': 'ADSModule',
    name: str  # ': 'Application Deployment Server',
    primary_endpoint: str  # ': '0.0.0.0:2223',
    requires_full_load: bool  # ': True,
    supports_sleep: bool  # ': False,
    timestamp: str  # ': '22/03/2024 17:32',
    tools_version: str  # ': '2.4.6.10',
    version_codename: str  # ': 'Callisto'}


@dataclass
class OPList:
    """
    Represents the results from `MinecraftModule.get_op_whitelist()`.

    """

    level: int
    name: str
    uuid: str


@dataclass
class OPWhitelist:
    """
    Represents the results from `MinecraftModule.get_op_whitelist()`.

    """

    op_list: list = field(default_factory=list)
    whitelist: list = field(default_factory=list)


@dataclass
class PlatformInfo:
    """
    Represents thePlatformInfo tied to RemoteTargetInfo dataclass.\n
    Author: p0t4t0sandwich -> PlatformInfo https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L451

    """

    is_shared_setup: bool
    admin_rights: int
    cpu_info: CPUInfo
    installed_ram_mb: int
    os: int
    platform_name: str
    hardware_platform_name: str
    system_type: int
    virtualization: int
    installed_glibc_version: str  # "AMPVersionInfo"


@dataclass(init=False)
class Players:
    """
    Represents the Data returned from the AMP API call `Core.get_user_list()`
    The attributes are not 100% accurate. Used Minecraft Module as a test.
    `{'6eb7be5e-3d33-4b40-8aab-7889c243cc1a': 'Anth0kage'}`

    """

    id: str = ""
    name: str = ""

    def __init__(self, data: dict[str, str]) -> None:
        for id_, name in data.items():
            setattr(self, "id", id_)
            setattr(self, "name", name)


@dataclass()
class Port:
    """

    Current Port of the related AMP Instance. Tied to `Updates().Ports` and the API call `Core.get_port_summaries()`

    """

    listening: bool
    name: str
    port: int
    protocol: int
    required: Union[bool, None] = field(default=None)
    is_delayed_open: Union[bool, None] = field(default=None)


@dataclass
class Provision:
    """
    Represents the data from `ADSModule.get_provision_fitness()`

    """

    available: bool
    cpu_service_ratio: float
    free_disk_mb: int
    free_ram_mb: int
    load_avg: float
    remaining_instance_slots: int
    score: float
    thread_queue_length: int
    total_services: int


@dataclass
class ProvisionSettingInfo:
    """
    Represents the data from `ADSModule.get_provision_arguments()`.

    """

    default_value: str
    description: str
    endpoint_name: str
    node: str
    type: str
    value_range: Union[int, str]


@dataclass
class PortInfo:
    """
    Represents the data from the AMP API call `ADSModule.get_instance_network_info()`

    """

    description: str
    us_user_defined: bool
    port_number: int
    protocol: int
    provision_node_name: str
    range: int
    verified: bool


@dataclass
class RemoteTargetInfo:
    """
    Represents the information from the API call RemoteTargetInfo.\n
    Author: p0t4t0sandwich -> RemoteTargetInfo https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L859

    """

    ip_address_list: list[str]
    platform_info: PlatformInfo
    datastores: list[InstanceDatastore]
    deploys_in_containers: bool


@dataclass()
class Role:
    """
    Represents the data returns from the AMP API call `Core.get_role()`

    """

    id: str
    is_default: bool
    name: str
    description: str
    hidden: bool
    permissions: list[str]
    members: list[str]
    is_instance_specific: bool
    is_common_role: bool
    disable_edits: bool


@dataclass
class RunningTask:
    """
    Represents the data returned from some API calls that return RunningTask.\n

    https://github.com/p0t4t0sandwich/ampapi-py/blob/main/ampapi/types.py#L887

    """

    is_primary_task: bool
    start_time: str  # type: ignore
    id: str
    name: str
    description: str
    hide_from_ui: bool
    fast_dismiss: bool
    last_update_pushed: str  # type: ignore
    progress_percent: float
    is_cancellable: bool
    origin: str
    is_indeterminate: bool
    state: int
    status: str

    def __repr__(self) -> str:
        return pformat(vars(self), indent=1)

    def __post_init__(self) -> None:
        self.last_update_pushed: datetime = datetime.fromtimestamp(int(self.last_update_pushed[6:-2]) / 1000)  # type: ignore
        self.start_time: datetime = datetime.fromtimestamp(int(self.start_time[6:-2]) / 1000)  # type: ignore


@dataclass()
class ScheduleData:
    """
    Represents the Data returned from the AMP API call `Core.get_schedule_data()`

    """

    available_methods: Union[list[Methods], None] = None
    available_triggers: Union[list[Triggers], None] = None
    populated_triggers: Union[list[Triggers], None] = None


@dataclass()
class Session:
    """
    Represents the data returns from the AMP API call `Core.get_active_amp_sessions()`

    """

    source: str
    session_id: str
    username: str
    session_type: str
    start_time: str  # type: ignore
    last_activity: str  # type: ignore

    def __post_init__(self) -> None:
        self.start_time: datetime = datetime.fromtimestamp(int(self.start_time[6:-2]) / 1000)  # type: ignore
        self.last_activity: datetime = datetime.fromtimestamp(int(self.last_activity[6:-2]) / 1000)  # type: ignore


@dataclass()
class SettingSpec:
    """
    Represents the data returns from the AMP API call `Core.get_config()` or `Core.get_configs()`

    """

    actions: list[SettingSpecAction] = field(default_factory=list)
    always_allow_read: bool = field(default=False)
    attributes: Union[SettingsSpecAttribute, None] = field(default=None)
    category: Union[str, None] = field(default=None)
    current_value: Union[list, str, bool, int, dict, SettingSpecTableAliases, None] = field(default=None)
    description: Union[str, None] = field(default=None)
    enum_values: Union[None, dict[str, Any]] = field(default=None)
    enum_values_are_deferred: bool = field(default=False)
    input_type: Union[str, None] = field(default=None)
    is_provision_spec: bool = field(default=False)
    keywords: Union[str, None] = field(default=None)
    max_length: int = 0
    max_value: Any = field(default=None)
    min_value: Any = field(default=None)
    meta: Union[str, None] = field(default=None)
    name: Union[str, None] = field(default=None)
    node: Union[str, None] = field(default=None)
    order: int = field(default=10)
    placeholder: Union[str, None] = field(default=None)
    read_only: bool = field(default=False)
    read_only_provision: bool = field(default=False)
    required: bool = field(default=False)
    requires_restart: bool = field(default=False)
    selection_source: Union[SettingSpecSelectionSource, None] = field(default=None)
    subcategory: Union[str, None] = field(default=None)
    suffix: Union[str, None] = field(default=None)
    tag: Union[str, None] = field(default=None)
    val_type: Union[str, None] = field(default=None)

    def __post_init__(self) -> None:
        _table = SettingSpecTable().table
        if self.node in _table and isinstance(self.current_value, int) and self.node is not None:
            self.current_value = _table[self.node](self.current_value)


@dataclass()
class SettingSpecAction:
    argument: str
    caption: str
    is_client_side: bool
    method: str
    module: str
    type_id: str


@dataclass()
class SettingsSpecAttribute:
    key_name: str
    key_placeholder: str
    type_id: str
    value_name: str
    value_placeholder: str


@dataclass()
class SettingsSpecParent:
    branding: list[SettingSpec] = field(default_factory=list)
    external_services: list[SettingSpec] = field(default_factory=list)
    file_manager: list[SettingSpec] = field(default_factory=list)
    instance_deployment: list[SettingSpec] = field(default_factory=list)
    login: list[SettingSpec] = field(default_factory=list)
    security_and_privacy: list[SettingSpec] = field(default_factory=list)
    system_settings: list[SettingSpec] = field(default_factory=list)
    updates: list[SettingSpec] = field(default_factory=list)


@dataclass()
class SettingSpecSelectionSource:
    deferred: bool
    must_validate: bool
    type_id: str


class SettingSpecTable:
    table: ClassVar[dict[str, type[SettingSpecTableAliases]]] = {
        "ADSModule.Network.AccessMode": AccessModeState,
        "ADSModule.Defaults.DefaultPostCreate": PostCreateState,
        "steamcmdplugin.SteamUpdateSettings.UpdateCheckMethod": ApplicationUpdatesState,
        "Core.Monitoring.LogLevel": LoggingLevelState,
        "Core.AMP.Theme": AMPTheme,
        "Core.AMP.AppStartupMode": AppStartupModeState,
        "Core.Security.TwoFactorMode": TwoFactoryModeState,
        "ADSModule.Network.PortAssignment": PortAssignmentState,
        "ADSModule.Network.DefaultIPBinding": DefaultIPBindingState,
        "ADSModule.Network.DefaultAppIPBinding": DefaultIPBindingState,
        "ADSModule.Network.DockerExternalIPBinding": DefaultIPBindingState,
        "ADSModule.ADS.DownloadMirror": AMPDownloadMirrorState,
        "ADSModule.ADS.Mode": ADSModeState,
        "ADSModule.Defaults.DefaultReleaseStream": ReleaseStreamState,
    }


@dataclass()
class Status:
    """
    Represents the JSON response data from :meth:`Core.get_status()`

    Attributes
    ----------
    state: :class:`AMPInstanceState`
        The state of the AMP Instance.
    uptime : str
        The up time of the Instance.
    metrics : Union[:py:class:`Metric`, None]
        The Metrics data related to the Instance if any. Default is None.
    """

    state: AMPInstanceState
    uptime: str
    metrics: Union[Metric, None] = field(default=None)

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass()
class Template:
    """
    Allows a user to fill out a Template to deploy an instance.

    Specific API functions will ask for this.
    - :func:`deploy_template()`


    Attributes
    ----------
    template_id : int
        The ID of the template to be deployed, as per the Template Management UI in AMP itself.
    new_username : Union[str, None]
        If specified, AMP will create a new user with this name for this instance. Default is None.
        - Must be unique, If this user already exists, this will be ignored but the new instance will be assigned to this user.
    new_password: Union[str, None]
        If :attribute:`new_username` is specified and the user doesn't already exist, the password will be assigned to this user. Default is None.
    new_email : Union[str, None]
        If :attribute:`new_username` is specified and the user doesn't already exist, the email address will be assigned to this user. Default is None.
    required_tags : Union[list[str], None]
        If specified, AMP will only deploy this template to targets that have every single 'tag' specified in their target configuration. You can adjust this via the controller by clicking 'Edit' on the target settings. Default is None.
    tag : Union[str, None]
        Unrelated to RequiredTags. This is to uniquely identify this instance to your own systems. It may be something like an order ID or service ID so you can find the associated instance again at a later time. Default is None.
        - If 'UseTagAsInstanceName' is enabled, then this will also be used as the instance name for the created instance - but it must be unique.
    friendly_name : Union[str, None]
        A friendly name for this instance. If left blank, AMP will generate one for you. Defaults is None.
    secret : Union[str, None]
        Must be a non-empty strong in order to get a callback on deployment state change. This secret will be passed back to you in the callback so you can verify the request. Default is None.
    post_create : :py:class:`PostCreateActionState`
        Default is :py:class:`PostCreateActionState.do_nothing`.
    extra_provision_settings: Union[dict[str, str], None]
        A dictionary of setting nodes and values to create the new instance with. Identical in function to the provisioning arguments in the template itself. Default is None.
    """

    template_id: int
    new_username: Union[str, None] = field(default=None)
    new_password: Union[str, None] = field(default=None)
    new_email: Union[str, None] = field(default=None)
    required_tags: Union[list[str], None] = field(default=None)
    tag: Union[str, None] = field(default=None)  #
    friendly_name: Union[str, None] = field(default=None)
    secret: Union[str, None] = field(default=None)
    post_create: PostCreateActionsState = field(default=PostCreateActionsState.do_nothing)
    extra_provision_settings: Union[dict[str, str], None] = field(default=None)

    def __repr__(self) -> str:
        return self.__class__.__qualname__ + " ".join([
            f"{f.name}={{self.{f.name}!r}}" for f in fields(class_or_instance=self) if f is not None
        ])


@dataclass
class TimedTrigger:
    """
    Represents the data of `Core.get_time_interval_trigger()`.

    """

    description: str  # ': 'Every 5 minutes',
    enabled_state: int  # ': 1,
    id: str  # ': 'd6a6cbf9-f36d-466e-94ce-d85af3586b4e',
    match_days: list[int]  # ': [0, 1, 2, 3, 4, 5, 6],
    match_days_of_month: list[
        int
    ]  # ': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
    match_hours: list[int]  # ': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
    match_minutes: list[int]  # ': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
    match_months: list[int]  # ': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    name: str  # ': 'Interval Trigger',
    order: int  # ': 0,
    tasks: TriggerTasks  # ': {'f3f334bc-d341-4b6b-beda-a33121439bcd': {'CreatedBy': '4569b62e-5df0-4e58-b063-b1a229e3b4eb','EnabledState': 1,'Id': 'f3f334bc-d341-4b6b-beda-a33121439bcd','Locked': False,'Order': 0,'ParameterMapping': {'Input': ''},'TaskMethodName': 'Event.MinecraftModule.SendConsole'}}}


@dataclass()
class Triggers:
    """
    Tied to `ScheduleData().AvailableTriggers` and `ScheduleData().PopulatedTriggers`

    """

    enabled_state: int
    tasks: list[TriggerTasks] = field(default_factory=list["TriggerTasks"])
    id: str = ""
    type: str = ""
    description: str = ""
    trigger_type: str = ""
    emits: list[str] = field(default_factory=list[str])
    last_execute_error: bool = field(default=False)
    last_error_reason: str = field(default="")


@dataclass()
class TriggerTasks:
    """
    Tied to `Triggers()`.

    Hold's information regarding AMP Tasks and their status.

    """

    id: str
    task_method_name: str
    parameter_mapping: dict[str, str]
    enabled_state: int
    locked: bool
    created_by: str
    order: int


@dataclass()
class UpdateInfo:
    """
    Represents AMP API call `Core/GetUpdateInfo`.

    """

    update_available: bool
    release_notes_url: str
    build: str
    version: str
    tools_version: Union[None, str] = None
    patch_only: Union[None, bool] = None


@dataclass()
class Updates:
    """
    Represents the data from AMP API call `Core.get_updates()` \n

    """

    console_entries: list[ConsoleEntries]
    status: Status
    messages: list[Messages]  # No ideal usage at this time.
    ports: list[Port] = field(default_factory=list)  # No ideal usage at this time.
    tasks: list[RunningTask] = field(default_factory=list)  # No ideal usage at this time.

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass()
class User:
    """
    Represents the Data returned from the AMP API call `Core.get_all_amp_user_info()`

    """

    cannot_change_password: bool
    disable: bool
    gravatar_hash: str
    id: str
    is_ldap_user: bool
    is_super_user: bool
    is_two_factor_enabled: bool
    must_change_password: bool
    name: str
    password_expires: bool
    permissions: list[str]
    roles: list[str]
    last_login: str  # type:ignore

    def __post_init__(self) -> None:
        self.last_login: datetime = datetime.fromisoformat(self.last_login)  # type:ignore
