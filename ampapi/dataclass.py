from __future__ import annotations

import functools
import logging
from dataclasses import dataclass, field, fields
from datetime import datetime
from logging import Logger
from operator import attrgetter
from pprint import pformat
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, Union

from dataclass_wizard.errors import MissingFields
from typing_extensions import Self

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Concatenate

    from typing_extensions import ParamSpec, Self, TypeVar

    from .types_ import MCUserData

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


def attribute_converter(data: dict[str, Any]) -> dict[str, Any]:
    """
    Removes private attributes (aka ``_attribute``) designation from the dict key values.

    .. note::
        Typically after calling :meth:`vars`.


    Parameters
    ----------
    data: dict[:class:`str`, Any]
        The data or object to remove private attributes from as keys.

    Returns
    -------
    dict[:class:`str`, Any]
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


def timestamp_converter(data: str) -> datetime:
    """
    Convert either the ``C#`` date str into a Python :class:`datetime` object or the ISO format.

    .. note::
        This is for older than 2.6.0.0 AMP Installs.


    Parameters
    -----------
    data: :class:`str`
        The date string to convert.

    Returns
    --------
    :class:`datetime`
        The converted string as a :class:`datetime` object..
    """

    if data.startswith("/Date"):
        return datetime.fromtimestamp(int(data[6:-2]) / 1000)
    else:
        return datetime.fromisoformat(data)


@dataclass
class ActionResult:
    """
    Represents the JSON response data from most API Endpoints.

    Attributes
    -----------
    status: :class:`bool`
        If the API call was successful.
    reason: Union[str, None]
        If :attr:`~ActionResult.status` is ``False`` this will typically have a :class:`str` response.
    result: Union[str, None]
        If :attr:`~ActionResult.status` is ``True`` this will contain data related to the API call.
    """

    status: bool
    reason: Union[str, None] = field(default=None)
    result: Union[str, None] = field(default=None)

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class AnalyticsCountryData:
    """
    Represents the JSON response data from :attr:`~AnalyticsSummary.country_data`.

    Attributes
    -----------
    country: :class:`str`
        The country code; similar to the ISO 3166-1 Alpha-2 format.
    display_session_time: :class:`str`
        The current display's session time per country.
    session_count: :class:`int`
        The current number of sessions per country.
    session_time_percent: :class:`float`
        UNK
    total_session_time: :class:`float`
        The total session time per country.
    unique_player_count: :class:`int`
        The unique player count per country.
    unique_player_percent: :class:`int`
        The unique player percent out of all countries.
    session_percent: :class:`int`
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
    A dataclass to handle filtering for :meth:`~AnalyticsPlugin.get_analytics_summary`, pass this dataclass in as the ``filter_``

    .. note::
        Simply create this class and fill out either :attr:`username`, :attr:`user_id` and or :attr:`country`.


    .. note::
        The :attr:`country` must be in **ISO 3166-1 Alpha-2 format**


    Attributes
    -----------
    country: :class:`str`
        The country to filter by.
    first_session: Union[:class:`bool`, None]
        Whether or not to filter by first session only, defaults to None.
    meta: Union[Any, None]
        UNK
    username: Union[:class:`str` , None]
        The username to filter by, defaults to None.
    user_id: Union[str, None]
        The user_id to filter by, currently using the :attr:`username` attribute, defaults to None.
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
    Represents the JSON response data from :attr:`AnalyticsSummary.stats`.

    .. note::
        * ["Total Sessions", "Unique Users", "New Users", "Total Session Time", "Bounce Rate", "Session Duration", "Sessions Per User", "Longest Session"]
        * Bounce Rate = "Sessions where the user joined and then quickly left again."


    Attributes
    -----------
    name: :class:`str`
        The Name of the current :class:`AnalyticsStats`
    description: :class:`str`
        The description of :attr:`AnalyticsStats.name` that is being tracked!
    current: Union[:class:`int`, float]
        Represents the actual value; similar to :attr:`display_value` but in a raw representation.
        - Could be seconds, minutes or a count value depending on the :attr:`description`.
    display_value: Union[:class:`int`, :class:`str`, float]
        The value being displayed on the Analytics Summary Page after formatting.
    difference: Union[:class:`int`, :class:`str`, float]
        Has values such as "Infinity", 0, and 0.0.
    previous: Union[:class:`int`, :class:`str`, float]
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
    Represents the JSON response data from :meth:`~AnalyticsPlugin.get_analytics_summary`.

    Attributes
    -----------
    busiest_time: dict[:class:`str`, Union[:class:`int`, :class:`str`]]
        UNK, default is a list.
    country_data: list[:class:`AnalyticsCountryData`]
        The Country information for the summary, default is a list.
    graph_data: list[dict[:class:`str`, Union[:class:`int`, :class:`str`]]]
        The Data displayed on the Web UI panel Analytics Menu, default is a list.
    is_demo: :class:`bool`
        UNK, default is False.
    quietest_time: dict[str, Union[:class:`int`, :class:`str`]]
        UNK, default is a dict.
    stats: list[:class:`AnalyticsStats`]
        The Analytics Stats of the summary, default is a list.
    top_players: list[:class:`AnalyticsTopPlayers`]
        The TOP players from the summary, default is a list.
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
    Represents the JSON Response data from :attr:`~Analytics_Summary.top_players`.

    Attributes
    -----------
    display_session_time: :class:`str`
        Display the session time.
    percent: :class:`float`
        The percent of how much this value in comparison to :attr:`~AnalyticsTopPlayers.total_session_time`.
    total_session_time: :class:`float`
        The total amount of session time the user has for the day.
    username: :class:`str`
        The name of the session user. Like an IGN.
    """

    display_session_time: str
    percent: float
    total_session_time: float
    username: str


@dataclass
class APIParams:
    """
    A class to hold Login information for the AMP API.

    .. note::
        The :attr:`url` must be relative to the machine running the API and the machine must be able to connect to AMP.


    .. warning::
        ``**DO NOT SET OR UPDATE**``-> :attr:`APIParams._sessions`.


    Attributes
    -----------
    url: :class:`str`
        The URL to access the Web GUI panel home page/login page.
    user: :class:`str`
        The AMP User name to login to the Web Panel.
    password: :class:`str`
        The AMP User password to login to the Web Panel.
    use_2fa: bool
        To use :py:class:`TOTP` 2 Factor Authentication, default is False.
    token: :class:`str`
        The 2 Factor Authentication Token Code to generate a :class:`TOTP` code, default is ""
    """

    url: str
    user: str
    password: str
    use_2fa: bool = False
    token: str = ""
    _sessions: dict[str, APISession] = field(init=False, default_factory=dict)


@dataclass
class APISession:
    """
    Stores the Session ID and the TTL usage for :class:`APIParams._session`.

    Attributes
    -----------
    id: :class:`str`
        The ``SESSIONID`` dict key from the JSON response of :meth:`Login`.
    ttl: :class:`datetime`
        The time to live of the :attr:`id`. This can be adjusted by ::class:`Base.session_ttl` value.
    """

    id: str
    ttl: datetime


@dataclass
class Application:
    """
    Represents the JSON response data from :meth:`MinecraftModule.get_supported_applications`.

    .. note::
        Shows Template/App information. Similar to the all the applications in a repo lists.


    Attributes
    -----------
    author: :class:`str`
        The author of the application/template.
    container_reason: :class:`str`
        The reason the application is using a container, if any.
    container_support: :class:`int`
        UNK - Unsure what this value is for.
    description: :class:`str`
        A brief description of what the application is.
    display_image_source: :class:`str`
        The url for the application image. Typically what you see as the Instance Banner.
    extra_setup_steps_uri: :class:`str`
        UNK
    friendly_name: :class:`str`
        A formatted version of the name.
    id: :class:`str`
        A unique ID for the application.
    is_service_spec: :class:`bool`
        UNK.
    module_name: :class:`str`
        The type of Module this application uses. (eg. "Minecraft", "Generic")
    no_commercial_usage: :class:`bool`
        As the attribute implies; if it's for commercial usage or not.
    supported_platforms: :class:`int`
        UNK
    settings: dict[:class:`str`, Any]
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
    Represents the JSON response data from :meth:`Core.get_audit_log_entries`

    Attributes
    -----------
    acknowledged: :class:`bool`
        UNK
    category: :class:`str`
        The type of log entry.
    event_type: :class:`int`
        The type of event that occurred.
    id: :class:`int`
        UNK
    message: :class:`str`
        The message tied to the log entry.
    source: :class:`str`
        UNK
    user: :class:`str`
        The AMP Username tied to the log entry.
    timestamp: :class:`str` | :class:`datetime`
        The timestamp comes in as  ISO format and :meth:`AuditLogEntry.__post_init__` converts it into a datetime object.
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
        self.timestamp: datetime = timestamp_converter(data=self.timestamp)  # type:ignore

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class Backup:
    """
    Represents the JSON response data from :meth:`ADSModule.get_backups`.

    Attributes
    -----------
    created_automatically: :class:`bool`
        If the backup was created by a Scheduled Task.
    description: :class:`str`
        The description for the backup, if any.
    id: :class:`str`
        The backup GUID.
    module_name: :class:`str`
        What type of Instance that created the backup. *eg. Minecraft, ADS, Generic*
    name: :class:`str`
        The name of the backup.
    source_os: :class:`int`
        Unsure. I believe there is an ENUM correlation for which int value is which type of OS
    sticky: :class:`bool`
        If the Backup is Sticky.
    stored_locally: :class:`bool`
        If the backup is local or not.
    stored_remotely: :class:`bool`
        If the backup is stored in S3/Cloud or similar.
    taken_by: :class:`str`
        Who created the backup.
    total_size_bytes: :class:`int`
        The total size of the backup is bytes.
    timestamp: :class:`datetime`
        The timestamp comes in as  ISO format and converts it into a datetime object.
    """

    created_automatically: bool
    description: str
    id: str
    module_name: str
    name: str
    source_os: int
    sticky: bool
    stored_locally: bool
    stored_remotely: bool
    taken_by: str
    total_size_bytes: int
    timestamp: str  # type: ignore

    def __post_init__(self) -> None:
        self.timestamp: datetime = timestamp_converter(data=self.timestamp)  # type:ignore

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class BukkitPlugin:
    """
    Represents the JSON response data from any Bukkit function call. Related to :class:`MinecraftModule`.

    Attributes
    -----------
    author: dict:class:`[`str, :class:`int`]
        The author's name and ID tied to the author as a dict key, value pair.
    category: dict[:class:`str`, :class:`int`]
        The category name and ID tied to the category as a dict key, value pair.
    downloads: :class:`int`
        The number of downloads the plugin has had.
    file: dict[:class:`str`, Union[:class:`str`, :class:`int`]]
        UNK
    id: :class:`int`
        The ID of the plugin.
    likes: :class:`int`
        The number of likes the plugin has had.
    links: dict[:class:`str`, :class:`str`]
        The links related to the plugin. Unsure of data structure.
    name: :class:`str`
        The name of the plugin.
    tag: :class:`str`
        The tag related to the plugin.
    version: dict[:class:`str` , Union[:class:`int`, :class:`str`]]
        The version information of the plugin.
    icon: dict[:class:`str`, :class:`str`]
        The icon name and url in a dict key, value pair.
    tested_version: list[:class:`str`]
        The tested versions of the plugin, default is a list
    update_date: Union[:class:`int`, None]
        The timestamp of when it was updated, default is None
    release_date: Union[:class:`int`, None]
        The timestamp of when it was released, default is None
    rating: dict[:class:`str`, Union[float, :class:`int`]]
        The rating, default is a dict.
    external: Union[:class:`bool`, None]
        If the plugin is external or not, default is None
    existence_status: Union[:class:`int`, None]
        UNK, default is None
    installed_version: Union[:class:`int`, None]
        The plugin version currently installed, default is None.
    versions: Union[list[:class:`int`], None]
        The plugins alternate versions, if any, default is None.
    premium: Union[:class:`bool`, None]
        If the plugin is premium or not, default is None.
    source_code_link: :class:`str`
        The URL to the source code, default is "".
    supported_languages: :class:`str`
        The languages this plugin supports, default is "".
    contributors: :class:`str`
        The contributors to the source code/plugin, default is "".
    donation_link: :class:`str`
        The URL to donate/support the plugin, default is "".
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


@dataclass
class ConsoleEntries:
    """
    Represents the JSON response data from :attr:`Updates.console_entries`.


    Attributes
    -----------
    contents: :class:`str`
        The contents of the console entry.
    source: :class:`str`
        The source of the console entry. eg "Server thread/INFO, ..."
    type: :class:`str`
        The type of message. eg "Console, Chat, Error, ...
    timestamp: :class:`str` | :class:`datetime`
        The timestamp comes in as ISO format and :meth:`~ConsoleEntries.__post_init__` converts it into a datetime object.
    """

    contents: str
    source: str
    type: str
    timestamp: str  # type: ignore

    def __post_init__(self) -> None:
        self.timestamp: datetime = timestamp_converter(data=self.timestamp)  # type:ignore

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class Controller:
    """
    Represents the JSON response data for an AMP Controller Instance.

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
        self.last_updated: datetime = timestamp_converter(data=self.last_updated)  # type:ignore

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

    Represents the JSON response data from :class:`~PlatformInfo.cpu_info` attribute.\n
    Original Author: p0t4t0sandwich
    :class:`CPUInfo` : https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L151

    Attributes
    -----------
    sockets: :class:`int`
        The number of CPU sockets the AMP Instance has access to.
    cores: :class:`int`
        The number of cores the AMP Instance has access to.
    threads: :class:`int`
        The number of threads the AMP Instance has access to.
    vendor: :class:`str`
        The vendor of the CPU.
    model_name: :class:`str`
        The model name of the CPU.
    total_cores: :class:`int`
        The number of total cores the AMP Instance has access to.
    total_threads: :class:`int`
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
    Represents the JSON response data from :meth:`ADSModule.create_instance` function call.

    .. note::
        Unsure if this :attr:`~CreateInstance.port_number` respects port ranges of the ADS or not.


    Attributes
    -----------
    target_ads_instance: :class:`str`
        The Target instance ID to tie this Instance to.
    friendly_name: :class:`str`
        The Instance friendly name, this is what you see in the web GUI.
    module: :class:`str`
        The Instance module it will use.
    new_instance_id: :class:`str`
        UNK
    instance_name: :class:`str`
        The name for the Instance, similar to :attr:`friendly_name`.
    ip_binding: :class:`str`
        The IP to assign to the Instance. See :attr:`Controller.available_ips`.
    port_number: :class:`int`
        The Port to assign to the Instance.
    admin_username: :class:`str`
        UNK
    admin_password: :class:`str`
        The password for the :attr:`admin_username`.
    provision_settings: dict[:class:`str`, :class:`str`]
        UNK
    auto_configure: :class:`bool`
        When enabled, all settings other than the module, target and friendly_name are ignored and replaced with automatically generated values
    post_create: :class:`PostCreateActionsState`
        The action to take after creating the instance, defaults to :attr:`~PostCreateActionsState.do_nothing`
    start_on_boot: :class:`bool`
        If the instance starts on boot or not, default is False.
    display_image_source: :class:`str`
        If the instance has a banner to display, you can define it here, default is "".
    target_datastore: :class:`int`
        The Datastore ID to create this Instance on.
            * See :attr:`Controller.datastores` ID values.
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


@dataclass
class DCConsumes:
    """
    Represents the JSON response data from :attr:`~Methods.consumes`.

    Attributes
    -----------
    description: :class:`str`
        The description of the consumes method.
    input_type: :class:`str`
        The type of var that is provided by the User.
    name: :class:`str`
        The name of the method.
    value_type: :class:`str`
        The type of the value when provided.
    enum_values: :class:`str` | dict, optional
        The values to be used for "input_type" if Any, default is "".
    """

    description: str
    input_type: str
    name: str
    value_type: str
    enum_values: str | dict = field(default="")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name == other.name

    def __lt__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name < other.name


# TODO - update docstring
@dataclass
class DCParameterMapping:
    """
    Represents the JSON response data for :attr:`~TriggerTasks.parameter_mapping`

    Attributes
    -----------
    user: :class:`str`
        UNK, default is "".
    reason: :class:`str`
        UNK, default is "".
    title: :class:`str`
        UNK, default is "".
    subtitle: :class:`str`
        UNK, default is "".
    """

    user: str = field(default="")
    reason: str = field(default="")
    title: str = field(default="")
    subtitle: str = field(default="")


@dataclass
class Diagnostics:
    """
    Represents the JSON response data from :meth:`Core.get_diagnostics_info`.

    Attributes
    -----------
    application_name: :class:`str`
        The Instance application name.
    application_version: :class:`str`
        The Instance application version.
    build_date: :class:`str`
        The date of the AMP Instance build.
    build_spec: :class:`str`
        Similar to :attr:`Diagnostics.release_stream`.
    cpu_layout: :class:`str`
        Number of Sockets, Cores and Threads *eg 1S/2C/10T*
    cpu_model: :class:`str`
        The name of the CPU.
    codename: :class:`str`
        The release/build code name.
    installed_ram: :class:`int`
        The amount of installed ram on the system.
    instance_id: :class:`str`
        The Instance GUID
    last_arguments: :class:`str`
        The last used arguments when running the Instance.
    last_executable: :class:`str`
        The last used file executable for the Instance.
    last_process_id: :class:`int`
        The last used process ID.
    loaded_plugins: :class:`str`
        The AMP loaded plugin's for the Instance.
    module: :class:`str`
        The Instance module. *eg ADSModule, Minecraft, Generic*
    module_application: :class:`str`
        The Instance application.
    network_mode: Any
        UNK
    platform: :class:`str`
        The machine full name of the Operating System.
    release_stream: :class:`str`
        Mainline, Developer, etc
    system_type: :class:`str`
        The bit type of the Instance Operating System.
    tools_version: :class:`str`
        The version of the build tools for the Instance.
    virtualization: :class:`str`
        If the system is using a VM or not. *eg VMware*
    os: :class:`str`
        The machine Operating System.
    """

    application_name: str
    application_version: str | VersionInfo
    build_date: str
    build_spec: str
    cpu_layout: str
    cpu_model: str
    codename: str
    installed_ram: int
    instance_id: str
    last_arguments: str
    last_executable: str
    last_process_id: int
    loaded_plugins: str
    module: str
    module_application: str
    network_mode: Any
    platform: str
    release_stream: str
    system_type: str
    tools_version: str
    virtualization: str
    os: str

    def __repr__(self) -> str:
        return pformat(vars(self))

    def __post_init__(self) -> None:
        if isinstance(self.application_version, str):
            self.application_version = VersionInfo.to_dataclass(data=self.application_version)


@dataclass
class Directory:
    """
    Represents the JSON response data from :meth:`FileManagerPlugin.get_directory_listing`

    Attributes
    -----------
    is_directory: :class:`bool`
        If the path is a directory.
    is_virtual_directory: :class:`bool`
        If the path is a virtual directory.
    filename: :class:`str`
        The name of the file or directory.
    size_bytes: :class:`int`
        The size of the file/directory in bytes.
    is_downloadable: :class:`bool`
        If the file can be downloaded.
    is_editable: :class:`bool`
        If the file can be edited.
    is_archive: :class:`bool`
        If the file is an archive.
    is_excluded_from_backups: :class:`bool`
        If the file is excluded from backups.
    created: :class:`str` | :class:`datetime`
        The time the file/directory was created.
    modified: :class:`str` | :class:`datetime`
        The time the file/directory was last modified.
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
        self.created: datetime = timestamp_converter(self.created)  # type: ignore
        self.modified: datetime = timestamp_converter(self.modified)  # type: ignore


@dataclass
class Endpoints:
    """
    Represents the JSON response data from :meth:`ADSModule.get_application_endpoints`

    Attributes
    -----------
    display_name: :class:`str`
        The name of the endpoint.
    endpoint: :class:`str`
        The name of the endpoint.
    uri: :class:`str`
        The URI of the endpoint.

    """

    display_name: str
    endpoint: str
    uri: str


@dataclass
class FileChunk:
    """
    Represents the JSON response data from :meth:`FileManagerPlugin.get_file_chunk`

    Attributes
    -----------
    base_64_data: :class:`str`
        The base64 encoded string of the file chunk.
    bytes_length: :class:`int`
        The length of the file chunk in bytes.

    """

    base_64_data: str
    bytes_length: int


@dataclass
class Fitness:
    """
    Represents the JSON response data for :attr:`Instance.fitness` attribute.

    Attributes
    -----------
    available: :class:`bool`
        If the Instance is available to create more services or not.
    total_services: :class:`int`
        The total number of services running on the Instance.
    free_ram_mb: :class:`int`
        The amount of free RAM on the Instance.
    free_disk_mb: :class:`int`
        The amount of free disk space on the Instance.
    cpu_service_ratio: :class:`float`
        The ratio of CPU usage to the number of services running on the Instance.
    thread_queue_length: :class:`int`
        The length of the thread queue on the Instance.
    load_avg: :class:`float`
        The load average on the Instance.
    remaining_instance_slots: :class:`int`
        The number of remaining Instance slots on the License.
    score: :class:`float`
        The score of the Instance.
    score_description: :class:`str`
        A summary of the "remaining slots" aka the number of Instances you have left to create.
        * Includes the amount of "Free Ram" and "CPU Ratio".
    score_zero_factors: list[Any]
        A list of factors that determine the score of the Instance.

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
    score_zero_factors: list[Any]


@dataclass
class InstanceDatastore:
    """
    Represents a the class object to be used in :meth:`ADSModule.add_datastore`

    .. warning::
        AMP must have read/write/execute access to the directory specified in the `Directory` parameter.


    .. note::
        This class is also used in :meth:`ADSModule.update_datastore`, :meth:`ADSModule.get_datastores`, :meth:`ADSModule.get_datastore`



    Parameters
    -----------
    id: :class:`int`
        The ID of the datastore.
    friendly_name: :class:`str`
        The friendly name of the datastore.
    description: :class:`str`
        The description of the datastore.
    directory: :class:`str`
        The on-disk location where instances will be stored. Changing this will not affect existing instances, only newly created ones.
    soft_limit_mb: :class:`int`
        Datastores that reach or exceed this limit in total size will not be considered as deployment targets. This is only a soft limit and does not prevent instances on this datastore from using more space.
    priority: :class:`int`
        Instances with a lower priority number are preferred over those with a higher number, all other factors being equal.
    tags: list[:class:`str`]
        A list of tags to apply to the datastore.
    is_internal: :class:`bool`
        If the datastore is internal.
    instance_limit:
        The maximum number of instances that can be provisioned on this datastore, defaults to 0 for unlimited.
    active:
        Deactivating a datastore prevents new instances from being provisioned to it, defaults to True.
    current_usage_mb: :class:`int`
        The current usage of the datastore in megabytes, defaults to -1.
    sanitized_name: :class:`str`
        The sanitized name of the datastore, defaults to "None".
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
    Represents the JSON response data for :meth:`ADSModule.update_instance_info`.

    Attributes
    -----------
    instance_id: :class:`str`
        The Instance GUID.
    friendly_name: :class:`str`
        The friendly name of the Instance.
    description: :class:`str`
        The description of the Instance.
    suspended: :class:`bool`
        If the Instance is suspended.
    exclude_from_firewall: :class:`bool`
        If the Instance should be excluded from the firewall.
    run_in_container: :class:`bool`
        If the Instance should be run in a container.
    container_memory: :class:`int`
        The amount of memory allocated to the container in MB.
    container_max_cpu: :class:`str`
        The maximum amount of CPU cores allocated to the container.
    container_image: :class:`str`
        The container/docker image to use.
    memory_policy: :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance, default is :attr:`ContainerMemoryPolicyState.reserve`.
    start_on_boot: :class:`bool`
        If the Instance should start on boot, default is False.
    welcome_message: :class:`str`
        The welcome message of the Instance, default is None.
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
    Represents the JSON response data for :meth:`ADSModule.get_instance` or a list of these from :meth:`ADSModule.get_instances`.


    Attributes
    -----------
    application_endpoints: list[dict[str, str]]
        The list of application endpoints for the Instance.
    app_state: :class:`AMPInstanceState`
        The state of the application.
    container_memory_mb: :class:`int`
        The amount of memory allocated to the container in MB.
    container_memory_policy: :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance.
    daemon: :class:`bool`
        If the Instance is a daemon.
    daemon_autostart: :class:`bool`
        If the Instance should be autostart on boot.
    deployment_args: dict[:class:`str`, :class:`str`]
        The deployment arguments of the Instance.
    disk_usage_mb: :class:`int`
        The disk usage of the Instance in MB.
    exclude_from_firewall: :class:`bool`
        If the Instance should be excluded from the firewall.
    friendly_name: :class:`str`
        The friendly name of the Instance.
    ip: :class:`str`
        The IP address of the Instance.
    instance_id: :class:`str`
        The Instance GUID.
    instance_name: :class:`str`
        The Instance name.
    is_container_instance: :class:`bool`
        If the Instance is a container instance.
    is_https: :class:`bool`
        If the Instance is using HTTPS.
    management_mode: :class:`int`
        The management mode of the Instance.
    module: :class:`str`
        The module of the Instance.
    port: :class:`str`
        The port of the Instance.
    release_stream: :class:`int`
        The release stream of the Instance.
    running: :class:`bool`
        If the Instance is running.
    suspended: :class:`bool`
        If the Instance is suspended.
    target_id: :class:`str`
        The target ID of the Instance.
    amp_version: Union[:class:`str`, :class:`dict`, :class:`AMPVersionInfo`, None]
        The version of the AMP, default is None.
    container_cpus: :class:`float`
        The amount of CPU cores allocated to the container, default is 0.0.
    tags: Union[:class:`None`, :class:`list`]
        The list of tags of the Instance, default is None.
    module_display_name: :class:`str`
        The display name of the module, default is "".
    metrics: Union[:class:`Metric`, None]
        The metrics of the Instance, default is None.
    display_image_source: :class:`str`
        The source of the display image, default is "".
    description: :class:`str`
        The description of the Instance, default is "".
    """

    application_endpoints: list[dict[str, str]]
    app_state: AMPInstanceState
    container_memory_mb: int
    container_memory_policy: ContainerMemoryPolicyState
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
    amp_version: Union[str, dict, VersionInfo, None] = field(default=None)
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
            # Per Mike and Developers of AMP state they will be using string versions from `2.6.0.0` and this handles that.
            if isinstance(self.amp_version, dict):
                try:
                    setattr(self, "amp_version", VersionInfo(**self.amp_version))
                except Exception as e:
                    _logger: Logger = logging.getLogger()
                    _logger.warning("We attempted to unpack <self.amp_version> and failed %s", e)
                    return
            if isinstance(self.amp_version, str):
                setattr(self, "amp_version", VersionInfo.to_dataclass(self.amp_version))

    def __hash__(self) -> int:
        return hash(self.instance_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.instance_id == other.instance_id

    def __lt__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.instance_id < other.instance_id

    def __repr__(self) -> str:
        res: str = f"Type: {type(self)} | ID: {id(self)}\n"
        res += f"Name: {self.instance_name}\nInstance ID: {self.instance_id}\n"
        res += f"Application State: {self.app_state.name}\nInstance Running: {self.running}\nModule: {self.module}\nPort: {self.port}"
        res += "\n"
        return res

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


@dataclass
class InstanceStatus:
    """
    Represents the JSON response data from :meth:`ADSModule.get_instance_statuses`.

    Attributes
    -----------
    instance_id: :class:`str`
        The Instance ID.
    running: :class:`bool`
        Whether the Instance is running.

    """

    instance_id: str
    running: bool


@dataclass
class LoginResults:
    """
    Represents the JSON response data from the AMP Login response.

    Attributes
    -----------
    success: :class:`bool`
        Whether the login was successful.
    result: :class:`int`
        The result code.
    permissions: list[:class:`str`], optional
        A list of permissions, defaults to [].
    result_reason: :class:`str`, optional
        The result reason, defaults to "".
    session_id: :class:`str`, optional
        The session ID, defaults to "".
    remember_me_token: :class:`str`, optional
        The remember me token, defaults to "".
    user_info: :class:`LoginUserInfo`, optional
        The user information, defaults to None.

    """

    success: bool
    result: int
    permissions: list[str] = field(default_factory=list)
    result_reason: str = ""
    session_id: str = ""
    remember_me_token: str = ""
    user_info: Union[LoginUserInfo, None] = field(default=None)  # second data class


@dataclass
class LoginUserInfo:
    """
    Represents an AMP users information, tied to :class:`LoginResults` along with representing the JSON response from the function :meth`~Core.get_amp_users_summary`

    Attributes
    -----------
    id: :class:`str`
        The user ID.
    username: :class:`str`
        The username.
    is_two_factor_enabled: :class:`bool`
        If the user has 2FA enabled.
    disabled: :class:`bool`
        If the user is disabled.
    gravatar_hash: :class:`str`
        The gravatar hash.
    is_ldap_user: :class:`bool`
        If the user is a LDAP user.
    last_login: :class:`datetime`
        The last login date.
    email_address: :class:`str`, optional
        The email address, defaults to "" if not set.

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
        self.last_login: datetime = timestamp_converter(self.last_login)  # type:ignore


@dataclass
class MCUser:
    """
    Represents the JSON response data from :meth:`MinecraftModule.mc_get_whitelist`.

    Attributes
    -----------
    name: :class:`str`
        The username.
    uuid: :class:`str`
        The Minecraft UUID.

    """

    name: str
    uuid: str


@dataclass
class Messages:
    """
    Represents a Message from the dataclass attribute :attr:`Updates.messages`

    Attributes
    -----------
    age_minutes: :class:`int`
        The age of the message in minutes.
    expired: :class:`bool`
        Whether the message has expired.
    id: :class:`str`
        The message ID.
    message: :class:`str`
        The message.
    source: :class:`str`
        The source of the message.

    """

    age_minutes: int
    expired: bool
    id: str
    message: str
    source: str


@dataclass
class Methods:
    """
    Tied to :attr:`ScheduleData.available_methods`.

    Hold's information regarding Methods/Events that are available to the Instance. Varies depending on instance type.

    Attributes
    -----------
    id: :class:`str`
        The method ID.
    name: :class:`str`
        The method name.
    description: :class:`str`
        The method description.
    consumes: list[:class:`DCConsumes`]
        A list of parameters the method consumes.

    """

    id: str = ""
    name: str = ""
    description: str = ""
    consumes: list[DCConsumes] = field(default_factory=list)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name == other.name

    def __lt__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name < other.name


@dataclass
class Metric:
    """
    Represents the JSON response data for :attr:`AppStatus.metrics` and :attr:`Instance.metrics`.

    Attributes
    -----------
    active_users: Union[None, :class:`MetricsData`]
        The active users data.
    cpu_usage: Union[None, :class:`MetricsData`]
        The cpu usage data.
    memory_usage: Union[None, :class:`MetricsData`]
        The memory usage data.

    """

    active_users: Union[None, MetricsData] = field(default=None)
    cpu_usage: Union[None, MetricsData] = field(default=None)
    memory_usage: Union[None, MetricsData] = field(default=None)


@dataclass
class MetricsData:
    """
    Represents the JSON response data for each of the attributes of :class:`Metrics`.

    Attributes
    -----------
    raw_value: :class:`int`
        The raw value.
    max_value: :class:`int`
        The max value.
    percent: :class:`int`
        The percent.
    units: :class:`str`
        The unit of measurement.
    color: Union[None, :class:`str`]
        Color number 1 if applicable..
    color2: Union[None, :class:`str`]
        Color number 2 if applicable.
    color3: Union[None, :class:`str`]
        Color number 3 if applicable.

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
    Represents the JSON response data from :meth:`Core.get_module_info`

    Attributes
    -----------
    amp_build: :class:`str`
        The AMP build.
    amp_version: :class:`str`
        The AMP version.
    api_version: :class:`str`
        The API version.
    allow_remember_me: :class:`bool`
        Whether remember me is allowed.
    analytics: :class:`bool`
        Whether analytics is enabled.
    app_name: :class:`str`
        The app name.
    author: :class:`str`
        The author.
    base_port: :class:`int`
        The base port.
    branding: :class:`dict`
        The branding data.
    build_spec: :class:`str`
        The build spec.
    display_base_uri: :class:`str`
        The display base uri.
    end_point_ur: :class:`str`
        The end point uri.
    feature_set: :class:`list`
        The feature set.
    friendly_name: :class:`str`
        The friendly name.
    instance_id: :class:`str`
        The instance id.
    instance_name: :class:`str`
        The instance name.
    is_remote_instance: :class:`bool`
        Whether the instance is remote.
    loaded_plugins: list[:class:`str`]
        A list of loaded plugins.
    module_name: :class:`str`
        The module name.
    name: :class:`str`
        The full name.
    primary_endpoint: :class:`str`
        The primary endpoint.
    requires_full_load: :class:`bool`
        Whether the instance requires full load.
    supports_sleep: :class:`bool`
        Whether the instance supports sleep.
    timestamp: :class:`str`
        The current timestamp.
    tools_version: :class:`str`
        The tools version.
    version_codename: :class:`str`
        The version codename.
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
    Represents the JSON response data from :meth:`MinecraftModule.get_op_whitelist`.

    Attributes
    -----------
    level: :class:`int`
        The level of the operator user.
    name: :class:`str`
        The name of the user.
    uuid: :class:`str`
        The UUID of the user.

    """

    level: int
    name: str
    uuid: str


@dataclass
class OPWhitelist:
    """
    Represents the JSON response data from :meth:`MinecraftModule.get_op_whitelist`.

    Attributes
    -----------
    op_list: list[:class:`MCUserData`]
        The list of operator users.
    whitelist: list[:class:`MCUserData`]
        The list of whitelisted users.

    """

    op_list: list[MCUserData] = field(default_factory=list)
    whitelist: list[MCUserData] = field(default_factory=list)


@dataclass
class PlatformInfo:
    """
    Represents the data from the attribute :attr:`RemoteTargetInfo.platform_info`.

    Attributes
    -----------
    cpu_info: :class:`CPUInfo`
        The CPU information.
    installed_ram_mb: :class:`int`
        The installed RAM in MB of the system.
    os: :class:`int`
        The system operating system.
    platform_name: :class:`str`
        The platform name.
    system_type: :class:`int`
        The system type.
    virtualization: :class:`int`
        The virtualization.
    is_shared_setup: :class:`bool`
        Whether the instance is shared setup.
    admin_rights: :class:`int`
        The admin rights level.
    hardware_platform_name: :class:`str`
        The hardware platform name.
    installed_glibc_version: :class:`str`
        The installed glibc version.

    """

    cpu_info: CPUInfo
    installed_ram_mb: int
    os: int
    platform_name: str
    system_type: int
    virtualization: int
    is_shared_setup: bool = field(default=False)
    admin_rights: int = field(default=0)
    hardware_platform_name: str = field(default="")
    installed_glibc_version: str = field(default="")  # "AMPVersionInfo"


class Player(NamedTuple):
    """
    Represents a single player connected to a server.

    Attributes
    -----------
    uuid: :class:`str`
        The UUID of the player.
    name: :class:`str`
        The name of the player.
    """

    uuid: str = ""
    name: str = ""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name == other.name

    def __lt__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name < other.name


@dataclass(init=False)
class Players:
    """
    Represents the JSON response data from :meth:`~Core.get_user_list`.


    .. note::
        The print out of this dataclass can be long depending on the number of players connected due to separation by newline.


    Attributes
    -----------
    sorted: list[:class:`Player`]
        A sorted list of :class:`Player` objects by name.

    """

    # {'781a2971-c14b-42c2-8742-d1e2b029d00a': 'k8_thekat', '50686fad-4027-4bdb-a4a5-2533f8a1e51f': 'WolfDevilAngel'}
    sorted: list[Player]

    def __init__(self, data: dict[str, str]) -> None:
        for uuid, name in data.items():
            self.sorted.append(Player(uuid=uuid, name=name))
        self.sorted.sort(key=attrgetter("name"))

    def __repr__(self) -> str:
        return "\n".join([p.name for p in self.sorted])

    def get_player(self, name_or_uuid: str) -> list[Player]:
        """
        Search for a player by their name or UUID.

        Parameters
        -----------
        name_or_uuid: :class:`str`
            The players name or UUID.

        Returns
        --------
        :class:`list[Player]`
            A list of :class:`Player` objects matching the search string.
        """
        return [p for p in self.sorted if name_or_uuid in (p.name, p.uuid)]


@dataclass
class Port:
    """

    Current Port of the related AMP Instance. Tied to :attr:`Updates.ports` and the JSON response data from :meth:`Core.get_port_summaries`.

    Attributes
    -----------
    listening: :class:`bool`
        Whether the port is listening.
    name: :class:`str`
        The name of the port.
    port: :class:`int`
        The port number.
    protocol: :class:`int`
        The protocol number.
    required: :class:`bool`
        Whether the port is required.
    is_delayed_open: :class:`bool`
        Whether the port is delayed open.

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
    Represents the JSON response data from :meth:`ADSModule.get_provision_fitness`.

    Attributes
    -----------
    available: :class:`bool`
        Whether the instance is available.
    cpu_service_ratio: :class:`float`
        The CPU service ratio.
    free_disk_mb: :class:`int`
        The free disk in MB.
    free_ram_mb: :class:`int`
        The free RAM in MB.
    load_avg: :class:`float`
        The load average.
    remaining_instance_slots: :class:`int`
        The remaining instance slots.
    score: :class:`float`
        The score.
    thread_queue_length: :class:`int`
        The thread queue length.
    total_services: :class:`int`
        The total services.

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
    Represents the JSON response data from :meth:`ADSModule.get_provision_arguments`.

    Attributes
    -----------
    default_value: :class:`str`
        The default value.
    description: :class:`str`
        The description.
    endpoint_name: :class:`str`
        The endpoint name.
    node: :class:`str`
        The node.
    type: :class:`str`
        The type.
    value_range: Union[:class:`int`, :class:`str`]
        The value range.

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
    Represents the JSON response data from :meth:`ADSModule.get_instance_network_info`.

    Attributes
    -----------
    description: :class:`str`
        The description.
    us_user_defined: :class:`bool`
        Whether the port is user defined.
    port_number: :class:`int`
        The port number.
    protocol: :class:`int`
        The protocol number.
    provision_node_name: :class:`str`
        The provision node name.
    range: :class:`int`
        The range.
    verified: :class:`bool`
        Whether the port is verified.

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
    Represents the JSON response data from :meth:`ADSModule.get_target_info`.

    Attributes
    -----------
    ip_address_list: :class:`list[str]`
        The IP address list.
    platform_info: :class:`PlatformInfo`
        The platform info.
    datastores: list[:class:`InstanceDatastore`]
        The datastores.
    deploys_in_containers: :class:`bool`

    """

    ip_address_list: list[str]
    platform_info: PlatformInfo
    datastores: list[InstanceDatastore]
    deploys_in_containers: bool


@dataclass
class Role:
    """
    Represents the JSON response data from :meth:`Core.get_role`.

    Attributes
    -----------
    id: :class:`str`
        The ID of the AMP role.
    is_default: :class:`bool`
        If the AMP role is the default role or not.
    name: :class:`str`
        The name of the AMP role.
    description: :class:`str`
        The description of the AMP role.
    hidden: :class:`bool`
        If the AMP role is hidden or not.
    permissions: :class:`list[str]`
        The list of permissions the AMP role has.
    members: :class:`list[str]`
        The list of AMP users who have the role.
    is_instance_specific: :class:`bool`
        If the AMP role is only for a specific instance or not.
    is_common_role: :class:`bool`
        If the AMP role is common or not.
    disable_edits: :class:`bool`
        If the AMP role can be edited by users with the role or not.

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
    Represents the JSON response data from functions that return RunningTask.

    Attributes
    -----------
    is_primary_task: :class:`bool`
        If the task is the primary task or not.
    start_time: :class:`str`
        The start time of the task.
    id: :class:`str`
        The ID of the task.
    name: :class:`str`
        The name of the task.
    description: :class:`str`
        The description of the task.
    hide_from_ui: :class:`bool`
        If the task is hidden from the UI or not.
    fast_dismiss: :class:`bool`
        If the task is fast dismiss or not.
    last_update_pushed: :class:`str`
        The last update pushed of the task.
    progress_percent: :class:`float`
        The progress percent of the task.
    is_cancellable: :class:`bool`
        If the task is cancellable or not.
    origin: :class:`str`
        The origin of the task.
    is_indeterminate: :class:`bool`
        If the task is indeterminate or not.
    state: :class:`int`
        The state of the task.
    status: :class:`str`
        The status of the task.

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
        self.last_update_pushed: datetime = timestamp_converter(data=self.last_update_pushed)  # type: ignore
        self.start_time: datetime = timestamp_converter(data=self.start_time)  # type: ignore


@dataclass
class ScheduleData:
    """
    Represents the JSON response data from :meth:`Core.get_schedule_data`.

    Attributes
    -----------
    available_methods: list[:class:`Methods`]
        The available methods.
    available_triggers: list[:class:`Triggers`]
        The available triggers.
    populated_triggers: list[:class:`Triggers`]
        The populated triggers.

    """

    available_methods: list[Methods] = field(default_factory=list)
    available_triggers: list[Triggers] = field(default_factory=list)
    populated_triggers: list[Triggers] = field(default_factory=list)


@dataclass
class Session:
    """
    Represents the JSON response data from :meth:`Core.get_active_amp_sessions`.

    Attributes
    -----------
    source: :class:`str`
        The source of the session.
    session_id: :class:`str`
        The ID of the session.
    username: :class:`str`
        The username the session belongs to.
    session_type: :class:`str`
        The type of the session.
    start_time: :class:`datetime`
        The start time of the session.
    last_activity: :class:`datetime`
        The last time the session was active.

    """

    source: str
    session_id: str
    username: str
    session_type: str
    start_time: str  # type: ignore
    last_activity: str  # type: ignore

    def __post_init__(self) -> None:
        self.start_time: datetime = timestamp_converter(self.start_time)  # type: ignore
        self.last_activity: datetime = timestamp_converter(self.last_activity)  # type: ignore


@dataclass
class SettingSpec:
    """
    Represents the JSON response data from :meth:`Core.get_config` or :meth:`Core.get_configs`.

    These represent a single setting field in the Instance configuration UI.

    Attributes
    -----------
    category: :class:`str`
        Which category the setting will appear under in the Instance configuration UI.
    actions: list[:class:`SettingSpecAction`]
        The list of actions related to the setting, defaults to an empty list.
    always_allow_read: :class:`bool`
        If the setting should always allow read or not.
    attributes: :class:`SettingsSpecAttribute`, optional
        The attributes that are set/prompted for when changing this setting.
    current_value: Union[:class:`list`, :class:`str`, :class:`bool`, :class:`int`, :class:`dict`, :class:`SettingSpecTableAliases`]
        The current value of the setting, default is "".
    description: :class:`str`, optional
        The text description below the setting name in the UI, default is "".
    enum_values: :class:`dict`, optional
        A dictionary representing the possible enum values for the setting, default is None.
    enum_values_are_deferred: :class:`bool`
        UNK, default is False.
    input_type: :class:`str`, optional
        The type of input to expect for the setting field, default is None.
    is_provision_spec: :class:`bool`
        if the setting is also a provision spec, default is False.
    keywords: :class:`str`
        UNK, default is "".
    max_length: :class:`int`
        UNK, all fields are 0 in data, default is 0.
    min_value: None
        UNK, all fields are null in data, default is None.
    meta: :class:`str`
        UNK, all fields are "", default is "".
    name: :class:`str`
        The name of the setting.
    node: :class:`str`
        The node required to have to edit this setting, default is "".
    order: :class:`int`
        The order in which this setting will appear in the UI, default is 1.
    placeholder: :class:`str`
        The placeholder text for the setting field, default is "".
    read_only: :class:`bool`
        If the setting is read only or not, default is False.
    read_only_provision: :class:`bool`
        UNK, all fields are False in data, default is False.
    required: :class:`bool`
        If the setting is required or not, default is False.
    requires_restart: :class:`bool`
        If the setting requires the Instance or Server to be restarted, default is False.
    selection_source: Union[:class:`SettingSpecSelectionSource`, None]
        UNK, most fields are null in data, default is None.
    subcategory: :class:`str`
        The subcategory the setting will appear under in the Instance configuration UI, default is "".
    suffix: :class:`str`
        The suffix applied to the string current_value, default is "".
    tag: :class:`str`
        What the setting is related to, similar to a Server Config property or file, default is "".
    val_type: :class:`str`
        What the type is of the current_value, default is "".

    """

    category: str
    actions: list[SettingSpecAction] = field(default_factory=list)
    always_allow_read: bool = field(default=False)
    attributes: Union[SettingsSpecAttribute, None] = field(default=None)
    current_value: Union[list, str, bool, int, dict, SettingSpecTableAliases] = ""
    description: str = ""
    enum_values: Union[None, dict[str, Any]] = field(default=None)
    enum_values_are_deferred: bool = field(default=False)
    input_type: Union[str, None] = field(default=None)
    is_provision_spec: bool = field(default=False)
    keywords: str = ""
    max_length: int = 0
    max_value: None = field(default=None)
    min_value: None = field(default=None)
    meta: str = ""
    name: str = field(default="")
    node: str = ""
    order: int = field(default=1)
    placeholder: str = ""
    read_only: bool = field(default=False)
    read_only_provision: bool = field(default=False)
    required: bool = field(default=False)
    requires_restart: bool = field(default=False)
    selection_source: Union[SettingSpecSelectionSource, None] = field(default=None)
    subcategory: str = ""
    suffix: str = ""
    tag: str = ""
    val_type: str = ""  # ['Boolean', 'Int32', 'String', 'Enum', "List<String>"]

    def __post_init__(self) -> None:
        # determines the current value type and converts the data into the respective dataclass if needed.
        _table = SettingSpecTable().table
        if self.node in _table and isinstance(self.current_value, int) and self.node is not None:
            self.current_value = _table[self.node](self.current_value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name == other.name

    def __lt__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.name < other.name


@dataclass
class SettingSpecAction:
    """
    Represents the JSON response data from :attr:`SettingSpec.actions`.

    Attributes
    -----------
    argument: :class:`str`
        The argument of the action.
    caption: :class:`str`
        The caption of the action.
    is_client_side: :class:`bool`
        If the action is client side or not.
    method: :class:`str`
        The method of the action, these relate to API Endpoints when combined with the module.
    module: :class:`str`
        The module the action belongs to.
    type_id: :class:`str`
        The type id of the action.
    """

    argument: str
    caption: str
    is_client_side: bool
    method: str
    module: str
    type_id: str


@dataclass
class SettingsSpecAttribute:
    """
    Represents the JSON response data from :attr:`SettingSpec.attributes`.

    Attributes
    -----------
    key_name: :class:`str`
        The name of the key.
    key_placeholder: :class:`str`
        The placeholder text for the key.
    type_id: :class:`str`
        The type id of the key.
    value_name: :class:`str`
        The name of the value.
    value_placeholder: :class:`str`
        The placeholder text for the value.
    read_only_keys: :class:`bool`
        If the key is read only or not.
    """

    key_name: str
    key_placeholder: str
    type_id: str
    value_name: str
    value_placeholder: str
    read_only_keys: bool = False


@dataclass
class SettingsSpecParent:
    """
    Represents the JSON response data from :meth:`Core.get_setting_spec`.

    Attributes
    -----------
    branding: list[:class:`SettingSpec`]
        The list of branding settings in the UI, default is an empty list.
    external_services: list[:class:`SettingSpec`]
        The list of external services settings in the UI, default is an empty list.
    file_manager: list[:class:`SettingSpec`]
        The list of file manager settings in the UI, default is an empty list.
    instance_deployment: list[:class:`SettingSpec`]
        The list of instance deployment settings in the UI, default is an empty list.
    login: list[:class:`SettingSpec`]
        The list of login settings in the UI, default is an empty list.
    security_and_privacy: list[:class:`SettingSpec`]
        The list of security and privacy settings in the UI, default is an empty list.
    system_settings: list[:class:`SettingSpec`]
        The list of system settings in the UI, default is an empty list.
    updates: list[:class:`SettingSpec`]
        The list of update settings in the UI, default is an empty list.
    """

    branding: list[SettingSpec] = field(default_factory=list)
    external_services: list[SettingSpec] = field(default_factory=list)
    file_manager: list[SettingSpec] = field(default_factory=list)
    instance_deployment: list[SettingSpec] = field(default_factory=list)
    login: list[SettingSpec] = field(default_factory=list)
    security_and_privacy: list[SettingSpec] = field(default_factory=list)
    system_settings: list[SettingSpec] = field(default_factory=list)
    updates: list[SettingSpec] = field(default_factory=list)


@dataclass
class SettingSpecSelectionSource:
    """
    Represents the JSON response data from :attr:`SettingSpec.selection_source`.

    Attributes
    -----------
    deferred: :class:`bool`
        If the selection source is deferred or not.
    must_validate: :class:`bool`
        If the selection source must validate or not.
    type_id: :class:`str`
        The type id of the selection source.
    """

    deferred: bool
    must_validate: bool
    type_id: str


@dataclass
class Status:
    """
    Represents the JSON response data from :meth:`Core.get_updates`

    Attributes
    -----------
    state: :class:`AMPInstanceState`
        The state of the AMP Instance.
    uptime: :class:`str`
        The up time of the Instance, in Days, Hours, Minutes, Seconds format. 00:00:00:00
    metrics: Union[:class:`Metric`, None]
        The Metrics data related to the Instance if any, default is None.
    """

    state: AMPInstanceState
    uptime: str
    metrics: Union[Metric, None] = field(default=None)

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class Template:
    """
    A placeholder class for all the parameters to deploy or create a template.


    * :meth:`ADSModule.deploy_template`


    Attributes
    -----------
    template_id : int
        The ID of the template to be deployed, as per the Template Management UI in AMP itself.
    new_username : Union[:class:`str`, None] , optional
        If specified, AMP will create a new user with this name for this instance. Default is None.
        * Must be unique, If this user already exists, this will be ignored but the new instance will be assigned to this user.
    new_password: Union[:class:`str`, None] , optional
        If :attr:`new_username` is specified and the user doesn't already exist, the password will be assigned to this user. Default is None.
    new_email : Union[:class:`str`, None] , optional
        If :attr:`new_username` is specified and the user doesn't already exist, the email address will be assigned to this user. Default is None.
    required_tags: Union[list[:class:`str`], None] , optional
        If specified, AMP will only deploy this template to targets that have every single 'tag' specified in their target configuration. You can adjust this via the controller by clicking 'Edit' on the target settings. Default is None.
    tag : Union[:class:`str`, None] , optional
        Unrelated to required_tags. This is to uniquely identify this instance to your own systems. It may be something like an order ID or service ID so you can find the associated instance again at a later time. Default is None.
    friendly_name: Union[:class:`str`, None] , optional
        A friendly name for this instance. If left blank, AMP will generate one for you. Defaults is None.
    secret : Union[:class:`str`, None] , optional
        Must be a non-empty strong in order to get a callback on deployment state change. This secret will be passed back to you in the callback so you can verify the request. Default is None.
    post_create: :class:`PostCreateActionState`, optional
        The action to take after the Instance is created, default is :attr:`PostCreateActionState.do_nothing`.
    extra_provision_settings: Union[dict[:class:`str`, :class:`str`], None]
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
    Represents the data of :meth:`Core.get_time_interval_trigger`.

    Attributes
    -----------
    description: :class:`str`
        The description of the trigger, this is shown in the UI.
    enabled_state: :class:`bool`
        If the Timed Trigger is enabled or not.
    id: :class:`str`
        The ID of the Timed Trigger, these are unique per Instance.
    match_days: list[:class:`int`]
        The days of the week to match, starting at 0 for Monday.
    match_days_of_month: list[:class:`int`]
        The days of the month to match.
    match_hours: list[:class:`int`]
        The hours of the day to match.
    match_minutes: list[:class:`int`]
        The minutes of the hour to match.
    match_months: list[:class:`int`]
        The months to match.
    name: :class:`str`
        The name of the Timed Trigger, this is shown in the UI.
    order: :class:`int`
        The order in which this trigger will appear in the Event list.
    tasks: :class:`list[TriggerTasks]`
        The list of tasks associated with this Timed Trigger.
    """

    description: str
    enabled_state: bool
    id: str
    match_days: list[int]
    match_days_of_month: list[int]
    match_hours: list[int]
    match_minutes: list[int]
    match_months: list[int]
    name: str
    order: int
    tasks: TriggerTasks


@dataclass
class Triggers:
    """
    Represents the JSON reponse data for attributes :attr:`ScheduleData.available_triggers` and :attr:`ScheduleData.populated_triggers`.


    .. note::
        The :attr:`Triggers.id` is unique per Instance.


    Attributes
    -----------
    enabled_state: :class:`int`
        If the trigger is enabled or not.
    tasks: :class:`list[TriggerTasks]`, optional
        The list of tasks associated with this trigger, default is an empty list.
    id: :class:`str`
        The ID of the trigger, these are unique per Instance.
    type: :class:`str`
        The type of trigger, typically a TimeIntervalTrigger or EventTrigger.
    description: :class:`str`
        The description of the trigger.
    trigger_type: :class:`str`
        The same as :attr:`Triggers.type`.
    emits: :class:`list[str]`, optional
        The parameters the trigger emits to the Event allowing usage in the trigger, default is an empty list.
    last_execute_error: :class:`bool`, optional
        If the last execution of the trigger resulted in an error or not, default is False.
    last_error_reason: :class:`str`, optional
        The reason the last execution of the trigger resulted in an error, default is "".
    """

    enabled_state: int
    tasks: list[TriggerTasks] = field(default_factory=list)
    id: str = ""
    type: str = ""
    description: str = ""
    trigger_type: str = ""
    emits: list[str] = field(default_factory=list)
    last_execute_error: bool = field(default=False)
    last_error_reason: str = field(default="")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.description == other.description

    def __lt__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.description < other.description


@dataclass
class TriggerTasks:
    """
    Represents the JSON response for the attribute :attr:`Triggers.tasks`.

    Hold's information regarding AMP Tasks and their status.

    Attributes
    ----------
    id: :class:`str`
        The ID of the task, these are unique per Instance.
    task_method_name: :class:`str`
        The name of the task method.
    parameter_mapping: :class:`DCParameterMapping`
        The parameter mapping for the task.
    enabled_state: :class:`int`
        If the task is enabled or not.
    locked: :class:`bool`
        If the task is locked or not.
    created_by: :class:`str`
        The user that created the task.
    order: :class:`int`
        The order in which this task will appear in the list of tasks.

    """

    id: str
    task_method_name: str
    parameter_mapping: DCParameterMapping
    enabled_state: int
    locked: bool
    created_by: str
    order: int


@dataclass
class UpdateInfo:
    """
    Represents the JSON response data from :meth:`Core.get_update_info`.

    Attributes
    -----------
    update_available: :class:`bool`
        If an update is available or not.
    release_notes_url: :class:`str`
        The URL to the release notes for the update.
    build: :class:`str`
        The build of the update.
    version: :class:`str`
        The version of the update.
    tools_version: :class:`str`
        The tools version of the update, default is None.
    patch_only: :class:`bool`
        If the update is a patch only update or not, default is None
    """

    update_available: bool
    release_notes_url: str
    build: str
    version: str
    tools_version: Union[None, str] = None
    patch_only: Union[None, bool] = None


@dataclass
class Updates:
    """
    Represents the JSON response data from :meth:`Core.get_updates`.

    Attributes
    -----------
    console_entries: :class:`list[ConsoleEntries]`
        The list of entries in the console.
    status: :class:`Status`
        The status of the Server.
    messages: :class:`list[Messages]`
        The list of messages the Instance or Server has.
    ports: :class:`list[Port]`, optional
        The list of ports the Server is listening/using, default is an empty list.
    tasks: :class:`list[RunningTask]` , optional
        The list of tasks the Server is running, default is an empty list.
    """

    console_entries: list[ConsoleEntries]
    status: Status
    messages: list[Messages]
    ports: list[Port] = field(default_factory=list)
    tasks: list[RunningTask] = field(default_factory=list)

    def __repr__(self) -> str:
        return pformat(vars(self))


@dataclass
class User:
    """
    Represents the JSON response data from the function :meth:`Core.get_all_amp_user_info` or :meth:`Core.get_amp_user_info`

    Attributes
    -----------
    cannot_change_password: :class:`bool`
        If the user cannot change their password or not.
    disable: :class:`bool`
        If the user is disabled or not.
    gravatar_hash: :class:`str`
        The gravatar hash of the user.
    id: :class:`str`
        The ID of the user.
    is_ldap_user: :class:`bool`
        If the user is an LDAP user or not.
    is_super_user: :class:`bool`
        If the user has the Super User role or not.
    is_two_factor_enabled: :class:`bool`
        If the user has 2FA enabled or not.
    must_change_password: :class:`bool`
        If the user must change their password or not when they log in next.
    name: :class:`str`
        The name of the user.
    password_expires: :class:`bool`
        If the user password expires or not when they log in next.
    permissions: :class:`list[str]`
        The list of permissions the user has.
    roles: :class:`list[str]`
        The list of AMP roles the user has.
    email_address: :class:`str`
        The email address of the user.
    last_login: :class:`datetime`
        The last login date of the user.

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
    email_address: str
    last_login: str  # type:ignore

    def __post_init__(self) -> None:
        self.last_login: datetime = timestamp_converter(self.last_login)  # type:ignore


@dataclass
class VersionInfo:
    """
    Tied to the class attribute for :class:`UpdateInfo.build`

    .. note::
        * Currently has a converter function ``v2.6.0.0``
        * ``__repr__`` has been overridden to display in a joined string with build at the end.


    Attributes
    -----------
    major: :class:`int`
        The major version number of the AMP build.
    minor: :class:`int`
        The minor version number of the AMP build.
    revision: :class:`int`
        The revision number of the AMP build.
    minor_revision: :class:`int`
        The minor revision number of the AMP build.
    build: Union[:class:`int`, None]
        The build number, defaults to None.
    """

    major: int
    minor: int
    revision: int
    minor_revision: int = 0
    major_revision: Union[int, None] = None
    build: Union[int, None] = None

    @classmethod
    def to_dataclass(cls, data: str, sep: str = ".") -> Union[str, VersionInfo]:
        """
        Parse a string type of the Version into a dataclass.

        .. note::
            Assumes structure is ``"2.6.0.0"``


        Parameters
        ----------
        data: :class:`str`
            The string type of the Version to parse.
        sep: :class:`str`
            The separator to split the string by.

        Returns
        -------
        :class:`str` | :class:`AMPVersionInfo`
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

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.major == other.major
            and self.minor == other.minor
            and self.revision == other.revision
            and self.minor_revision == other.minor_revision
        )

    def __lt__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.major < other.major
            and self.minor < other.minor
            and self.revision < other.revision
            and self.minor_revision < other.minor_revision
        )

    def __repr__(self) -> str:
        return f"{self.major}.{self.minor}.{self.revision}.{self.minor_revision} | {self.build}"
