"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMPAPI_Python.

AMPAPI_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMPAPI_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMPAPI_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

from __future__ import annotations

import base64
import datetime
import logging
import secrets
import sys
import types
import typing
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from operator import attrgetter
from pprint import pformat
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, Self, TypeGuard, Union

from . import _types
from ._enums import (
    AccessModeState,
    ADSModeState,
    AMPDownloadMirrorState,
    AMPTheme,
    ApplicationUpdatesState,
    AppStartupModeState,
    ContainerMemoryPolicyState,
    DefaultIPBindingState,
    IfOperators,
    InstanceState,
    LoggingLevelState,
    MailPriority,
    PortAssignmentState,
    PostCreateState,
    Protocols,
    ReleaseStreamState,
    TwoFactoryModeState,
)
from .errors import AMPAPITypeError

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from typing import Self

    from typing_extensions import ParamSpec, TypeVar

    from ._types import (
        AnalyticsGraphDataResponse,
        AnalyticsStatsResponse,
        BrandingResponse,
        ConsoleEntriesResponse,
        ConsumesResponse,
        DiagnosticsResponse,
        LoginUserInfoResponse,
        MCUserResponse,
        MessageParametersResponse,
        MessagesResponse,
        MetricsResponse,
        ParameterMappingResponse,
        PortResponse,
        RunningTaskResponse,
        ScheduleDataResponse,
        SettingSpecResponse,
        StatusResponse,
        TriggersResponse,
        TriggerTasksResponse,
        UptimeResponse,
    )

    T = ParamSpec("T")
    F = TypeVar("F")

__all__ = (
    "APIParams",
    "APISession",
    "ActionResult",
    "AnalyticsCountryData",
    "AnalyticsFilter",
    "AnalyticsGraphData",
    "AnalyticsStats",
    "AnalyticsSummary",
    "AnalyticsTopPlayers",
    "AnalyticsUserDetails",
    "Application",
    "AuditLogEntry",
    "Backup",
    "Branding",
    "BuildInfo",
    "BukkitPlugin",
    "CPUInfo",
    "ConsoleEntries",
    "Consumes",
    "CreateInstance",
    "DeploymentTemplate",
    "Diagnostics",
    "Directory",
    "Endpoints",
    "FileChunk",
    "Fitness",
    "FolderUploadFile",
    "ImportConfig",
    "InstanceDatastore",
    "InstanceInfo",
    "InstanceStatus",
    "LicenceInfo",
    "LoginResults",
    "LoginUserInfo",
    "MCUser",
    "MessageParameters",
    "Messages",
    "Methods",
    "Metrics",
    "MetricsData",
    "OPList",
    "OPWhitelist",
    "ParameterMapping",
    "PermissionNode",
    "PlatformInfo",
    "Player",
    "Players",
    "Port",
    "PortInfo",
    "Provision",
    "ProvisionSettingInfo",
    "RemoteTargetInfo",
    "ResponseData",
    "Role",
    "RoleMember",
    "RunningTask",
    "ScheduleData",
    "SecurityCheck",
    "Session",
    "SettingSpec",
    "SettingSpecAction",
    "SettingSpecSelectionSource",
    "SettingSpecTable",
    "SettingSpecTableAliases",
    "SettingsSpecAttribute",
    "SettingsSpecParent",
    "Status",
    "StructuredDiagnostics",
    "TargetDatastore",
    "Template",
    "TimedTrigger",
    "TriggerID",
    "TriggerTasks",
    "Triggers",
    "TwoFactorSetupInfo",
    "UpdateInfo",
    "Updates",
    "Uptime",
    "UserApplicationData",
    "UserInfo",
)

LOGGER: logging.Logger = logging.getLogger(__name__)

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
    """Removes private attributes (aka ``_attribute``) designation from the dict key values.

    .. note::
        Typically after calling :meth:`vars`.


    Parameters
    ----------
    data : dict[:class:`str`, Any]
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
        new_vars[key] = value
    return new_vars


def _field_values(instance: Any) -> dict[str, Any]:
    """Collect a dataclass instance's field values into a dict.

    A `slots=True` dataclass has no `__dict__`, and `vars(self)` raises on it. The `__repr__` methods use this instead.

    Parameters
    ----------
    instance : Any
        The dataclass instance.

    Returns
    -------
    dict[:class:`str`, Any]
        Field name to value, in field order.

    """
    return {field_.name: getattr(instance, field_.name) for field_ in fields(instance)}


def _dataclass_to_dict(dataclass_: Any) -> dict[str, Any]:
    """Deconstruct a dataclass into an API parameter dict.

    .. note::
        Keys are the dataclass field names verbatim; AMP takes these nested payload objects in
        ``snake_case``, so no key conversion happens here. Attributes set to None are omitted
        entirely rather than sent as ``null``.


    .. note::
        :class:`Enum` attributes are unwrapped to their ``.value``; :func:`json.dumps` cannot
        serialize an Enum, so leaving them intact raises when the request is built.


    Parameters
    ----------
    dataclass_ : Any
        The dataclass instance to deconstruct.

    Returns
    -------
    dict[:class:`str`, Any]
        The dataclass attributes as a key, value paired dict.

    Raises
    ------
    :exc:`AMPAPITypeError`
        When the object passed in is not a dataclass instance.

    """
    if not is_dataclass(dataclass_):
        raise AMPAPITypeError(end_point="<dataclass_to_dict>", cur_type=dataclass_, expec_type=dict)
    values: dict[str, Any] = {}
    for entry in fields(class_or_instance=dataclass_):
        value: Any = getattr(dataclass_, entry.name)
        if value is None:
            continue
        values[entry.name] = value.value if isinstance(value, Enum) else value
    return values


def timestamp_converter(timestamp: str) -> datetime.datetime:
    """Convert either the ``C#`` date str into a Python :class:`datetime` object or the ISO format.

    .. note::
        This is for older than 2.6.0.0 AMP Installs.


    Parameters
    ----------
    timestamp : :class:`str`
        The date string to convert.

    Returns
    -------
    :class:`datetime`
        The converted string as a :class:`datetime` object.

    """
    if timestamp.startswith("/Date"):
        return datetime.datetime.fromtimestamp(int(timestamp[6:-2]) / 1000, tz=datetime.UTC)
    return datetime.datetime.fromisoformat(timestamp)


def _is_json_object(value: object) -> TypeGuard[dict[str, Any]]:
    """If `value` is a decoded JSON object, whose keys are always strings."""
    return isinstance(value, dict)


def _is_json_array(value: object) -> TypeGuard[list[Any]]:
    """If `value` is a decoded JSON array."""
    return isinstance(value, list)


# TODO: Remove once every caller uses `from_response` (#24 phase C).
def build[ResponseT: ResponseData](cls: type[ResponseT], data: Mapping[str, Any]) -> ResponseT:
    """Forward to :meth:`ResponseData.from_response`, kept until the callers are converted."""
    return cls.from_response(data)


class ResponseData:
    """The base of every dataclass that holds an AMP response.

    .. note::
        A subclass is a dataclass that declares one field per key AMP sends. Nested dataclasses are built from the
        type hints of those fields.

    .. versionadded:: 5.0.0

    """

    # Empty, so a `slots=True` subclass doesn't get a `__dict__` back from this base.
    __slots__ = ()

    # Class/key pairs already reported. Each unknown key AMP sends is logged once, not on every response.
    _reported_unknown_keys: ClassVar[set[tuple[str, str]]] = set()
    # The converter of every field of each class, worked out once per class.
    _build_plans: ClassVar[dict[type, dict[str, Any]]] = {}

    @staticmethod
    def _converter(hint: Any) -> Callable[[Any], Any] | None:
        """The function that turns a response value into what the type hint names, worked out once from the hint.

        Returns None when the hint holds no dataclass or list. The value is then used as sent.
        """
        origin = typing.get_origin(hint)
        # A union tries each member in order and takes the first that converts.
        # `list[Consumes] | list[ConsumesResponse]` builds Consumes.
        if origin is Union or origin is types.UnionType:
            options: list[Callable[[Any], Any]] = []
            for option in typing.get_args(hint):
                if option is type(None):
                    continue
                option_converter = ResponseData._converter(option)
                if option_converter is not None:
                    options.append(option_converter)
            if not options:
                return None

            def convert_union(value: Any) -> Any:
                for option_converter in options:
                    converted = option_converter(value)
                    if converted is not value:
                        return converted
                return value

            return convert_union
        if isinstance(hint, type) and issubclass(hint, ResponseData):
            # Bound once here, so each nested value doesn't look the classmethod up again.
            from_response = hint.from_response
            return lambda value: from_response(value) if _is_json_object(value) else value
        if origin is list:
            element_converter = ResponseData._converter((typing.get_args(hint) or (Any,))[0])
            if element_converter is None:
                return lambda value: list(value) if _is_json_array(value) else value
            return lambda value: [element_converter(item) for item in value] if _is_json_array(value) else value
        return None

    @classmethod
    def _build_plan(cls) -> dict[str, Callable[[Any], Any] | None]:
        """Each field name of this dataclass and the converter for its value, worked out once per class."""
        plan = cls._build_plans.get(cls)
        if plan is None:
            # `modules.py` imports its TypedDicts only for type checking. The `_types` names are added for the hints
            # that mention them.
            namespace: dict[str, Any] = {**vars(_types), **vars(sys.modules[cls.__module__])}
            field_types = typing.get_type_hints(cls, globalns=namespace)
            # Only `from_response` calls this, after it has checked the class is a dataclass.
            plan = {
                entry.name: ResponseData._converter(field_types[entry.name])
                for entry in fields(cls)  # pyright: ignore[reportArgumentType]
            }
            cls._build_plans[cls] = plan
        return plan

    @classmethod
    def from_response(cls, data: Mapping[str, Any]) -> Self:
        """Build this dataclass from an AMP response, converting nested dataclasses from the field type hints.

        Keys the dataclass doesn't declare are dropped and logged once, instead of raising a :exc:`TypeError`.

        .. versionadded:: 5.0.0

        Parameters
        ----------
        data : Mapping[:class:`str`, Any]
            The sanitised AMP response for it.

        Returns
        -------
        :class:`Self`
            The built dataclass, with its nested dataclasses built too.

        Raises
        ------
        :exc:`TypeError`
            When the class isn't a dataclass.

        """
        if not is_dataclass(cls):
            msg = f"from_response() needs a dataclass, got {cls!r}."
            raise TypeError(msg)
        # The cache is read here first, which skips a classmethod call on every response after the first.
        plan = ResponseData._build_plans.get(cls)
        if plan is None:
            plan = cls._build_plan()
        values: dict[str, Any] = {}
        for key, value in data.items():
            if key not in plan:
                if (cls.__name__, key) not in cls._reported_unknown_keys:
                    cls._reported_unknown_keys.add((cls.__name__, key))
                    LOGGER.warning(
                        "<%s> | %s has no field %r, AMP sent a key the library doesn't know yet and it was left out.",
                        "from_response",
                        cls.__name__,
                        key,
                    )
                continue
            convert = plan[key]
            values[key] = value if convert is None else convert(value)
        return cls(**values)


@dataclass(slots=True)
class ActionResult(ResponseData):
    """Represents the JSON response data from most API Endpoints.

    Attributes
    ----------
    status : :class:`bool`
        If the API call was successful.
    reason : Union[str, None]
        If :attr:`~ActionResult.status` is ``False`` this will typically have a :class:`str` response.
    result : Union[:class:`str`, dict[:class:`str`, Any], None]
        If :attr:`~ActionResult.status` is ``True`` this will contain data related to the API call.

        .. versionchanged:: 5.0.0
            Can be a dict, for the endpoints that answer an object (eg. :meth:`Core.enable_two_factor`).
    support_url : Union[str, None], optional
        A link AMP offers for help with a failure, default is None.
    support_title : Union[str, None], optional
        The title to show for :attr:`~ActionResult.support_url`, default is None.

    """

    status: bool
    reason: Union[str, None] = field(default=None)
    result: Union[str, dict[str, Any], None] = field(default=None)
    # Added in AMP 2.8 (confirmed against 2.8.0.8); defaulted so older responses still construct.
    support_url: Union[str, None] = field(default=None)
    support_title: Union[str, None] = field(default=None)

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class AnalyticsCountryData(ResponseData):
    """Represents the JSON response data from :attr:`~AnalyticsSummary.country_data`.

    Attributes
    ----------
    country : :class:`str`
        The country code; similar to the ISO 3166-1 Alpha-2 format.
    display_session_time : :class:`str`
        The current display's session time per country.
    session_count : :class:`int`
        The current number of sessions per country.
    session_time_percent : :class:`float`
        UNK
    total_session_time : :class:`float`
        The total session time per country.
    unique_player_count : :class:`int`
        The unique player count per country.
    unique_player_percent : :class:`int`
        The unique player percent out of all countries.
    sessions_percent : :class:`float`
        The percent of total sessions related to this country.

        .. versionchanged:: 5.0.0
            `session_percent` is renamed `sessions_percent`, the key AMP sends.

    """

    country: str
    display_session_time: str
    session_count: int
    session_time_percent: float
    total_session_time: float
    unique_player_count: int
    unique_player_percent: float
    # session_percent: float = field(default_factory=float)
    sessions_percent: float


@dataclass(slots=True)
class AnalyticsFilter:
    """A dataclass to handle filtering for :meth:`~AnalyticsPlugin.get_analytics_summary`, pass this dataclass in as the ``filter_``

    .. note::
        Simply create this class and fill out either :attr:`username`, :attr:`user_id` and or :attr:`country`.


    .. note::
        The :attr:`country` must be in **ISO 3166-1 Alpha-2 format**


    Attributes
    ----------
    country : Union[:class:`str`, None]
        The country to filter by, defaults to None.
    first_session : Union[:class:`bool`, None]
        Whether or not to filter by first session only, defaults to None.
    meta : Union[Any, None]
        UNK
    username : Union[:class:`str` , None]
        The username to filter by, defaults to None.
    user_id : Union[str, None]
        The user_id to filter by, currently using the :attr:`username` attribute, defaults to None.

    """

    country: Union[str, None] = None
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
                                          "VE","VN","VG","VI","WF","EH","YE","ZM","ZW"]
    # fmt: on
    def __post_init__(self) -> None:  # noqa: D105
        if self.username is None and self.user_id is None and self.first_session is None and self.country is None:
            msg = "At least one of these attributes must be set | (username, user_id, country, first_session)."
            raise ValueError(msg)

        if self.country is not None and self.country not in self._country_list:
            msg = f"The Country attribute must be in ISO 3166-1 Alpha-2 format. | Received: {self.country}"
            raise ValueError(msg)


@dataclass(slots=True)
class AnalyticsGraphData(ResponseData):
    """Represents the JSON response data for the entries of :attr:`AnalyticsSummary.graph_data` and for
    :attr:`AnalyticsSummary.busiest_time` and :attr:`AnalyticsSummary.quietest_time`.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    date : :class:`str`
        When the period starts, as an ISO 8601 string (eg. "2026-09-21T00:00:00Z").
    end_date : :class:`str`
        When the period ends, as an ISO 8601 string.
    count : :class:`int`
        The number of sessions in the period.

    """

    date: str
    end_date: str
    count: int


@dataclass(slots=True)
class AnalyticsStats(ResponseData):
    """Represents the JSON response data from :attr:`AnalyticsSummary.stats`.

    .. note::
        * ["Total Sessions", "Unique Users", "New Users", "Total Session Time", "Bounce Rate",
          "Session Duration", "Sessions Per User", "Longest Session"]
        * Bounce Rate = "Sessions where the user joined and then quickly left again."


    Attributes
    ----------
    name : :class:`str`
        The Name of the current :class:`AnalyticsStats`
    description : :class:`str`
        The description of :attr:`AnalyticsStats.name` that is being tracked!
    current : Union[:class:`int`, float]
        Represents the actual value; similar to :attr:`display_value` but in a raw representation.
        - Could be seconds, minutes or a count value depending on the :attr:`description`.
    display_value : Union[:class:`int`, :class:`str`, float]
        The value being displayed on the Analytics Summary Page after formatting.
    difference : Union[:class:`int`, :class:`str`, float]
        Has values such as "Infinity", 0, and 0.0.
    previous : Union[:class:`int`, :class:`str`, float]
        UNK
    raw_name : :class:`str`, optional
        The name AMP uses for the stat internally (eg. "TotalSessions"), default is "".

        .. versionadded:: 5.0.0

    """

    name: str
    description: str
    current: Union[int, str, float]
    display_value: Union[int, str, float]
    difference: Union[int, str, float]
    previous: Union[int, str, float]
    raw_name: str = ""


@dataclass(slots=True)
class AnalyticsSummary(ResponseData):
    """Represents the JSON response data from :meth:`~AnalyticsPlugin.get_analytics_summary`.

    Attributes
    ----------
    busiest_time : :class:`AnalyticsGraphData` | :class:`AnalyticsGraphDataResponse`
        The period with the most sessions, default is an empty :class:`AnalyticsGraphData`.

        .. versionchanged:: 5.0.0
            Is an :class:`AnalyticsGraphData`, was a dict.
    country_data : list[:class:`AnalyticsCountryData`]
        The Country information for the summary, default is a list.
    graph_data : list[:class:`AnalyticsGraphData`] | list[:class:`AnalyticsGraphDataResponse`]
        The Data displayed on the Web UI panel Analytics Menu, default is a list.

        .. versionchanged:: 5.0.0
            Holds :class:`AnalyticsGraphData`, was a list of dicts.
    is_demo : :class:`bool`
        UNK, default is False.
    quietest_time : :class:`AnalyticsGraphData` | :class:`AnalyticsGraphDataResponse`
        The period with the fewest sessions, default is an empty :class:`AnalyticsGraphData`.

        .. versionchanged:: 5.0.0
            Is an :class:`AnalyticsGraphData`, was a dict.
    stats : list[:class:`AnalyticsStats`] | list[:class:`AnalyticsStatsResponse`]
        The Analytics Stats of the summary, default is a list.
    top_players : list[:class:`AnalyticsTopPlayers`]
        The TOP players from the summary, default is a list.

    """

    busiest_time: AnalyticsGraphData | AnalyticsGraphDataResponse = field(
        default_factory=lambda: AnalyticsGraphData(date="", end_date="", count=0),
    )
    country_data: list[AnalyticsCountryData] = field(default_factory=list[AnalyticsCountryData])
    graph_data: list[AnalyticsGraphData] | list[AnalyticsGraphDataResponse] = field(default_factory=list[AnalyticsGraphData])
    is_demo: bool = field(default=False)
    quietest_time: AnalyticsGraphData | AnalyticsGraphDataResponse = field(
        default_factory=lambda: AnalyticsGraphData(date="", end_date="", count=0),
    )
    stats: list[AnalyticsStats] | list[AnalyticsStatsResponse] = field(default_factory=list[AnalyticsStats])
    top_players: list[AnalyticsTopPlayers] = field(default_factory=list["AnalyticsTopPlayers"])

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class AnalyticsTopPlayers(ResponseData):
    """Represents the JSON Response data from :attr:`~Analytics_Summary.top_players`.

    Attributes
    ----------
    display_session_time : :class:`str`
        Display the session time.
    percent : :class:`float`
        The percent of how much this value in comparison to :attr:`~AnalyticsTopPlayers.total_session_time`.
    total_session_time : :class:`float`
        The total amount of session time the user has for the day.
    username : :class:`str`
        The name of the session user. Like an IGN.

    """

    display_session_time: str
    percent: float
    total_session_time: float
    username: str


@dataclass(slots=True)
class AnalyticsUserDetails(ResponseData):
    """Represents the JSON response data from :meth:`AnalyticsPlugin.get_user_details`.

    .. note::
        AMP only has data for a player when the Instance has `AnalyticsPlugin.Privacy.EnableAnalytics` and
        `AnalyticsPlugin.Privacy.UserSpecificData` turned on.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    username : :class:`str`
        The player's name, as passed to :meth:`AnalyticsPlugin.get_user_details`.
    first_session : :class:`datetime.datetime`
        When the player's first recorded session started, in UTC.
    last_session : :class:`datetime.datetime`
        When the player's last recorded session started, in UTC.
    session_count : :class:`int`
        The number of recorded sessions.
    total_session_time : :class:`float`
        The total time across every session, in minutes.
    display_total_session_time : :class:`str`
        :attr:`total_session_time` as AMP displays it. (eg. `"34 mins"`)
    average_session_time : :class:`float`
        The average session length, in minutes.
    display_average_session_time : :class:`str`
        :attr:`average_session_time` as AMP displays it.
    longest_session : :class:`float`
        The longest session, in minutes.
    display_longest_session : :class:`str`
        :attr:`longest_session` as AMP displays it.
    days_active : :class:`int`
        The number of days the player has a session on.
    average_time_per_day : :class:`float`
        The average time played per day, in minutes.
    average_time_per_week : :class:`float`
        The average time played per week, in minutes.
    average_time_per_month : :class:`float`
        The average time played per month, in minutes.
    recent_sessions : dict[:class:`str`, :class:`str`]
        Each recent session's start time (AMP's ISO string) and its length as AMP displays it. (eg. `"34m 10s"`)

    """

    username: str
    first_session: str | datetime.datetime
    last_session: str | datetime.datetime
    session_count: int
    total_session_time: float
    display_total_session_time: str
    average_session_time: float
    display_average_session_time: str
    longest_session: float
    display_longest_session: str
    days_active: int
    average_time_per_day: float
    average_time_per_week: float
    average_time_per_month: float
    recent_sessions: dict[str, str]

    def __post_init__(self) -> None:  # noqa: D105
        # AMP sends these without a timezone. They match `UserApplicationData.join_time`, which AMP marks as UTC.
        if isinstance(self.first_session, str):
            self.first_session = timestamp_converter(timestamp=self.first_session).replace(tzinfo=datetime.UTC)
        if isinstance(self.last_session, str):
            self.last_session = timestamp_converter(timestamp=self.last_session).replace(tzinfo=datetime.UTC)


@dataclass(slots=True)
class APIParams:
    """A class to hold Login information for the AMP API.

    .. note::
        The :attr:`url` must be relative to the machine running the API and the machine must be able to connect to AMP.


    .. warning::
        ``**DO NOT SET OR UPDATE**``-> :attr:`APIParams._sessions`.


    Attributes
    ----------
    url : :class:`str`
        The URL to access the Web GUI panel home page/login page. A trailing `/` is removed.
    user : :class:`str`
        The AMP User name to login to the Web Panel.
    password : :class:`str`
        The AMP User password to login to the Web Panel.
    use_2fa : bool
        To use :py:class:`TOTP` 2 Factor Authentication, default is False.
    token : :class:`str`
        The 2 Factor Authentication Token Code to generate a :class:`TOTP` code, default is ""

    """

    url: str
    user: str
    password: str
    use_2fa: bool = False
    token: str = ""
    _sessions: dict[str, APISession] = field(init=False, default_factory=dict[str, "APISession"])

    def __post_init__(self) -> None:
        """Strips a trailing `/` from :attr:`url`."""
        # We drop any trailing slash once here so every URL built from `url` is right.
        self.url = self.url.rstrip("/")


@dataclass(slots=True)
class APISession:
    """Stores the Session ID and the TTL usage for :attr:`APIParams._sessions`.

    Attributes
    ----------
    id : :class:`str`
        The `session_id` key from the JSON response of :meth:`Core.login`.
    ttl : :class:`datetime`
        The time to live of the :attr:`id`. This can be adjusted by ::class:`Base.session_ttl` value.

    """

    id: str
    ttl: datetime.datetime

    def __repr__(self) -> str:  # noqa: D105
        return f"ID: {self.id} | TTL: {self.ttl}"


@dataclass(slots=True)
class Application(ResponseData):
    """Represents the JSON response data from :meth:`MinecraftModule.get_supported_applications`
    and :meth:`ADSModule.get_supported_app_summaries`.

    .. note::
        Shows Template/App information. Similar to the all the applications in a repo lists.

    .. note::
        An entry from :meth:`ADSModule.get_supported_app_summaries` leaves out `module_name`, `settings` and
        `is_multi_ip_aware`, which keep their defaults.

    .. versionchanged:: 5.0.0
        `module_name` defaults to "".


    Attributes
    ----------
    author : :class:`str`
        The author of the application/template.
    container_reason : :class:`str`
        The reason the application is using a container, if any.
    container_support : :class:`int`
        UNK - Unsure what this value is for.
    description : :class:`str`
        A brief description of what the application is.
    display_image_source : :class:`str`
        The URL for the application image. Typically what you see as the Instance Banner.
    extra_setup_steps_uri : :class:`str`
        UNK
    friendly_name : :class:`str`
        A formatted version of the name.
    id : :class:`str`
        A unique ID for the application.
    is_service_spec : :class:`bool`
        UNK.
    no_commercial_usage : :class:`bool`
        As the attribute implies; if it's for commercial usage or not.
    supported_platforms : :class:`int`
        UNK
    module_name : :class:`str`, optional
        The type of Module this application uses. (eg. "Minecraft", "Generic"), default is "".
    settings : dict[:class:`str`, :class:`str`], optional
        A dict of Instance specific settings to apply for this application, default is an empty dict.

    """

    author: str | None
    container_reason: str | None
    container_support: int
    description: str | None
    display_image_source: str
    extra_setup_steps_uri: str | None
    friendly_name: str
    id: str
    is_service_spec: bool
    no_commercial_usage: bool
    supported_platforms: int
    # The summary from `get_supported_app_summaries` leaves these three out.
    module_name: str = field(default="")
    deprecated_reason: str | None = field(default=None)
    is_multi_ip_aware: bool = field(default=False)
    # Added in AMP 2.8.0.4; defaulted so 2.6.5.0 responses still construct.
    resource_usage_info: str | None = field(default=None)
    settings: dict[str, str] = field(default_factory=dict[str, str])

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class AuditLogEntry(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_audit_log_entries`

    Attributes
    ----------
    acknowledged : :class:`bool`
        UNK
    category : :class:`str`
        The type of log entry.
    event_type : :class:`int`
        The type of event that occurred.
    id : :class:`int`
        UNK
    message : :class:`str`
        The message tied to the log entry.
    source : :class:`str`
        UNK
    user : :class:`str`
        The AMP Username tied to the log entry.
    timestamp : :class:`str` | :class:`datetime`
        The timestamp comes in as  ISO format and :meth:`AuditLogEntry.__post_init__` converts it into a datetime object.

    """

    acknowledged: bool
    category: str
    event_type: int
    id: int
    message: str
    source: str
    user: str
    timestamp: str | datetime.datetime

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.timestamp, str):
            self.timestamp = timestamp_converter(timestamp=self.timestamp)

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class Backup(ResponseData):
    """Represents the JSON response data from :meth:`LocalFileBackupPlugin.get_backups`.

    Attributes
    ----------
    created_automatically : :class:`bool`
        If the backup was created by a Scheduled Task.
    description : :class:`str`
        The description for the backup, if any.
    id : :class:`str`
        The backup GUID.
    module_name : :class:`str`
        What type of Instance that created the backup. *eg. Minecraft, ADS, Generic*
    name : :class:`str`
        The name of the backup.
    source_os : :class:`int`
        Unsure. I believe there is an ENUM correlation for which int value is which type of OS
    sticky : :class:`bool`
        If the Backup is Sticky.
    stored_locally : :class:`bool`
        If the backup is local or not.
    stored_remotely : :class:`bool`
        If the backup is stored in S3/Cloud or similar.
    taken_by : :class:`str`
        Who created the backup.
    total_size_bytes : :class:`int`
        The total size of the backup is bytes.
    timestamp : :class:`datetime`
        The timestamp comes in as  ISO format and converts it into a datetime object.
    compressed_size_bytes : Union[:class:`int`, None], optional
        The size of the backup once compressed, in bytes, default is None.
    hash_sha1 : Union[:class:`str`, None], optional
        The SHA1 hash of the backup, default is None.
    meta : Any, optional
        UNK - only ever seen as None, default is None.
    parent_manifest : Union[:class:`str`, None], optional
        UNK - only ever seen as None, default is None.
    remote_store_id : Union[:class:`str`, None], optional
        The ID of the remote store holding the backup, if any, default is None.

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
    timestamp: str | datetime.datetime
    # Confirmed against AMP 2.8.0.8 (FretsServer01); defaulted so older responses still construct.
    compressed_size_bytes: Union[int, None] = field(default=None)
    hash_sha1: Union[str, None] = field(default=None)
    meta: Any = field(default=None)
    parent_manifest: Union[str, None] = field(default=None)
    remote_store_id: Union[str, None] = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.timestamp, str):
            self.timestamp = timestamp_converter(timestamp=self.timestamp)

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class Branding(ResponseData):
    """Represents the JSON response data from :attr:`Module.branding`.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    display_branding : :class:`bool`
        If the branding is shown.
    page_title : :class:`str`
        The title of the web panel page.
    company_name : :class:`str`
        The company name.
    welcome_message : :class:`str`
        The welcome message on the login page.
    branding_message : :class:`str`
        The branding message.
    short_branding_message : :class:`str`
        The short branding message (eg. "PoweredByAMP").
    url : :class:`str`
        The URL of the company.
    support_url : :class:`str`
        The URL of the support page.
    support_text : :class:`str`
        The text shown for the support link.
    submit_ticket_url : :class:`str`
        The URL to submit a support ticket.
    logo_url : :class:`str`
        The URL of the logo.
    background_url : :class:`str`
        The URL of the login background.
    splash_frame_url : :class:`str`
        The URL of the splash frame.
    forgot_password_url : :class:`str`
        The URL of the forgot password page.
    hosted_analytics_tag : :class:`str`
        The hosted analytics tag.

    """

    display_branding: bool
    page_title: str
    company_name: str
    welcome_message: str
    branding_message: str
    short_branding_message: str
    url: str
    support_url: str
    support_text: str
    submit_ticket_url: str
    logo_url: str
    background_url: str
    splash_frame_url: str
    forgot_password_url: str
    hosted_analytics_tag: str


@dataclass(slots=True)
class BuildInfo(ResponseData):
    """Tied to the class attribute for :class:`UpdateInfo.build`

    .. note::
        * Currently has a converter function ``v2.6.0.0``
        * `__repr__` has been overridden to display in a joined string with build at the end.


    Attributes
    ----------
    major : :class:`int`
        The major version number of the AMP build.
    minor : :class:`int`
        The minor version number of the AMP build.
    revision : :class:`int`
        The revision number of the AMP build.
    minor_revision : :class:`int`
        The minor revision number of the AMP build.
    build : Union[:class:`int`, None]
        The build number, defaults to None.

    """

    major: int
    minor: int
    revision: int
    minor_revision: int = 0
    major_revision: Union[int, None] = None
    build: Union[int, None] = None

    @classmethod
    def to_dataclass(cls, data: str, sep: str = ".") -> Union[str, BuildInfo]:
        """Parse a string type of the Version into a dataclass.

        .. note::
            Assumes structure is ``"2.6.0.0"``


        Parameters
        ----------
        data : :class:`str`
            The string type of the Version to parse.
        sep : :class:`str`
            The separator to split the string by.

        Returns
        -------
        :class:`str` | :class:`BuildInfo`
            Returns the built dataclass if it succeeds. Otherwise you will get the data passed in back.

        """
        new_data: list[str] = data.split(sep=sep)
        # Unpack the data converted into ints.
        try:
            temp: Self = cls(*[int(entry) for entry in new_data])

        # ValueError for a part that isn't a number, TypeError for too many or too few parts.
        except (UnboundLocalError, ValueError, TypeError) as e:
            _logger = logging.getLogger(__name__)
            _logger.error("Unable to convert the data %s | Error: %s", data, e)
            return data
        return temp

    __hash__ = None  # type: ignore[assignment]
    """Mutable dataclass; intentionally unhashable."""

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return (
            isinstance(other, self.__class__)
            and self.major == other.major
            and self.minor == other.minor
            and self.revision == other.revision
            and self.minor_revision == other.minor_revision
        )

    def __lt__(self, other: object) -> bool:  # noqa: D105
        # Compared part by part like any version number, so 2.5.0.0 is older than 2.6.0.0.
        return isinstance(other, self.__class__) and (self.major, self.minor, self.revision, self.minor_revision) < (
            other.major,
            other.minor,
            other.revision,
            other.minor_revision,
        )

    def __repr__(self) -> str:  # noqa: D105
        base = f"{self.major}.{self.minor}.{self.revision}.{self.minor_revision}"
        return base if self.build is None else f"{base}.{self.build}"


@dataclass(slots=True)
class BukkitPlugin(ResponseData):
    """Represents the JSON response data from any Bukkit function call. Related to :class:`MinecraftModule`.

    Attributes
    ----------
    author : dict:class:`[`str, :class:`int`]
        The author's name and ID tied to the author as a dict key, value pair.
    category : dict[:class:`str`, :class:`int`]
        The category name and ID tied to the category as a dict key, value pair.
    downloads : :class:`int`
        The number of downloads the plugin has had.
    file : dict[:class:`str`, Union[:class:`str`, :class:`int`]]
        UNK
    id : :class:`int`
        The ID of the plugin.
    likes : :class:`int`
        The number of likes the plugin has had.
    links : dict[:class:`str`, :class:`str`]
        The links related to the plugin. Unsure of data structure.
    name : :class:`str`
        The name of the plugin.
    tag : :class:`str`
        The tag related to the plugin.
    version : dict[:class:`str` , Union[:class:`int`, :class:`str`]]
        The version information of the plugin.
    icon : dict[:class:`str`, :class:`str`]
        The icon name and URL in a dict key, value pair.
    tested_version : list[:class:`str`]
        The tested versions of the plugin, default is a list
    update_date : Union[:class:`int`, None]
        The timestamp of when it was updated, default is None
    release_date : Union[:class:`int`, None]
        The timestamp of when it was released, default is None
    rating : dict[:class:`str`, Union[float, :class:`int`]]
        The rating, default is a dict.
    external : Union[:class:`bool`, None]
        If the plugin is external or not, default is None
    existence_status : Union[:class:`int`, None]
        UNK, default is None
    installed_version : Union[:class:`int`, None]
        The plugin version currently installed, default is None.
    versions : Union[list[:class:`int`], None]
        The plugins alternate versions, if any, default is None.
    premium : Union[:class:`bool`, None]
        If the plugin is premium or not, default is None.
    source_code_link : :class:`str`
        The URL to the source code, default is "".
    supported_languages : :class:`str`
        The languages this plugin supports, default is "".
    contributors : :class:`str`
        The contributors to the source code/plugin, default is "".
    donation_link : :class:`str`
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
    rating: dict[str, Union[float, int]] = field(default_factory=dict[str, Union[float, int]])
    external: Union[bool, None] = field(default=None)
    existence_status: Union[int, None] = field(default=None)
    installed_version: Union[int, None] = field(default=None)
    versions: Union[list[int], None] = field(default=None)
    premium: Union[bool, None] = field(default=None)
    source_code_link: str = field(default="")
    supported_languages: str = field(default="")
    contributors: str = field(default="")
    donation_link: str = field(default="")

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class ConsoleEntries(ResponseData):
    """Represents the JSON response data from :attr:`Updates.console_entries`.

    Attributes
    ----------
    contents : :class:`str`
        The contents of the console entry.
    source : :class:`str`
        The source of the console entry. eg "Server thread/INFO, ..."
    type : :class:`str`
        The type of message. eg "Console, Chat, Error, ...
    timestamp : :class:`str` | :class:`datetime`
        The timestamp comes in as ISO format and :meth:`~ConsoleEntries.__post_init__` converts it into a datetime object.
    source_id : Union[:class:`str`, None], optional
        The ID of the console entry's source, default is None.

    """

    contents: str
    source: str
    type: str
    timestamp: str | datetime.datetime
    # Confirmed against getupdates.json; only ever seen as None, defaulted so older responses still construct.
    source_id: Union[str, None] = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.timestamp, str):
            self.timestamp = timestamp_converter(timestamp=self.timestamp)

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class Consumes(ResponseData):
    """Represents the JSON response data from :attr:`~Methods.consumes`.

    .. versionchanged:: 5.0.0
        Renamed from `DCConsumes`.

    Attributes
    ----------
    description : :class:`str`
        The description of the consumes method.
    input_type : :class:`str`
        The type of var that is provided by the User.
    name : :class:`str`
        The name of the method.
    value_type : :class:`str`
        The type of the value when provided.
    enum_values : Union[dict[:class:`str`, :class:`str`], None], optional
        The values to be used for "input_type" if Any, default is None.

        .. versionchanged:: 5.0.0
            Is None when the argument has no values, was "".
    placeholder : :class:`str`, optional
        The placeholder text the web panel shows in the input, default is "".

        .. versionadded:: 5.0.0
    suffix : :class:`str`, optional
        The text shown after the input (eg. a unit), default is "".

        .. versionadded:: 5.0.0
    display_name : Union[:class:`str`, None], optional
        The name the web panel shows, default is None.

        .. versionadded:: 5.0.0
    selection_source : Union[:class:`str`, None], optional
        Where the choices come from, default is None. Only seen as null so far.

        .. versionadded:: 5.0.0
    locked : :class:`bool`, optional
        If the argument is locked, default is False.

        .. versionadded:: 5.0.0
    locked_value : Union[:class:`str`, None], optional
        The value the argument is locked to, default is None. Only seen as null so far.

        .. versionadded:: 5.0.0
    locked_reason : Union[:class:`str`, None], optional
        Why the argument is locked, default is None. Only seen as null so far.

        .. versionadded:: 5.0.0

    """

    description: str
    input_type: str
    name: str
    value_type: str
    # AMP sends null for this as well as a dict (captured in getscheduledata.json).
    enum_values: Union[dict[str, str], None] = field(default=None)
    placeholder: str = field(default="")
    suffix: str = field(default="")
    display_name: Union[str, None] = field(default=None)
    selection_source: Union[str, None] = field(default=None)
    locked: bool = field(default=False)
    locked_value: Union[str, None] = field(default=None)
    locked_reason: Union[str, None] = field(default=None)

    __hash__ = None  # type: ignore[assignment]
    """Mutable dataclass; intentionally unhashable."""

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.name == other.name

    def __lt__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.name < other.name


@dataclass(slots=True)
class CPUInfo(ResponseData):
    """Represents the JSON response data from :class:`~PlatformInfo.cpu_info` attribute.\n
    Original Author: p0t4t0sandwich
    :class:`CPUInfo` : https://github.com/p0t4t0sandwich/ampapi-py/blob/7a28af9b640efab329cf9ca2bf39c4112a13b287/ampapi/types.py#L151

    Attributes
    ----------
    sockets : :class:`int`
        The number of CPU sockets the AMP Instance has access to.
    cores : :class:`int`
        The number of cores the AMP Instance has access to.
    threads : :class:`int`
        The number of threads the AMP Instance has access to.
    vendor : :class:`str`
        The vendor of the CPU.
    model_name : :class:`str`
        The model name of the CPU.
    total_cores : :class:`int`
        The number of total cores the AMP Instance has access to.
    total_threads : :class:`int`
        The number of total threads the AMP Instance has access to.

    """

    sockets: int
    cores: int
    threads: int
    vendor: str
    model_name: str
    total_cores: int
    total_threads: int

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class CreateInstance:
    """Represents the JSON response data from :meth:`ADSModule.create_instance` function call.

    .. note::
        Unsure if this :attr:`~CreateInstance.port_number` respects port ranges of the ADS or not.


    Attributes
    ----------
    target_ads_instance : :class:`str`
        The Target Instance ID to tie this Instance to.
    friendly_name : :class:`str`
        The Instance friendly name, this is what you see in the web GUI.
    module : :class:`str`
        The Instance module it will use.
    new_instance_id : :class:`str`
        The ID for the new Instance, default is the zero GUID ("00000000-0000-0000-0000-000000000000"), which lets AMP pick the ID.
    instance_name : :class:`str`
        The name for the Instance, similar to :attr:`friendly_name`.
    ip_binding : :class:`str`
        The IP to assign to the Instance. See :attr:`Controller.available_ips`.
    port_number : :class:`int`
        The Port to assign to the Instance.
    admin_username : :class:`str`
        The username of the Instance's admin user, default is "admin". AMP rejects an empty username.
    admin_password : :class:`str`
        The password for the :attr:`admin_username`, default is a generated `secrets.token_urlsafe(18)` value.
        AMP rejects an empty password, and the generated one is ignored when :attr:`auto_configure` is True.
    provision_settings : dict[:class:`str`, :class:`str`]
        UNK
    auto_configure : :class:`bool`
        When enabled, all settings other than the module, target and friendly_name are ignored and
        replaced with automatically generated values
    post_create : :class:`PostCreateState`
        The action to take after creating the Instance, defaults to :attr:`~PostCreateState.do_nothing`
    start_on_boot : :class:`bool`
        If the Instance starts on boot or not, default is False.
    display_image_source : :class:`str`
        If the Instance has a banner to display, you can define it here, default is "".
    target_datastore : :class:`int`
        The Datastore ID to create this Instance on.
            * See :attr:`Controller.datastores` ID values.

    """

    target_ads_instance: str  # Tied to Auto Configure
    friendly_name: str  # Tied to Auto Configure
    module: str  # Tied to Auto Configure
    new_instance_id: str = field(default="00000000-0000-0000-0000-000000000000")
    instance_name: str = field(default="")
    ip_binding: str = field(default="192.168.0.1")
    port_number: int = field(default=8001)
    admin_username: str = field(default="admin")
    admin_password: str = field(default_factory=lambda: secrets.token_urlsafe(18))
    provision_settings: dict[str, str] = field(default_factory=dict[str, str])
    auto_configure: bool = field(default=False)
    post_create: PostCreateState = field(default=PostCreateState.do_nothing)
    start_on_boot: bool = field(default=False)
    display_image_source: str = field(default="")
    target_datastore: int = field(default=0)
    group: str | None = field(default=None)

    # TODO: Implement attribute checking.
    # When auto_configure is False, raise if a setting was left unset so it isn't missed;
    # the current defaults would hide a forgotten setting.
    def to_dict(self) -> dict[str, str | int | dict[str, str] | bool]:
        """As the function name implies; converts the class to a dict for use as an API parameter.

        Returns
        -------
        dict[:class:`str`, :class:`str` | :class:`int` | dict[:class:`str`, :class:`str`] | :class:`bool`]
            The class attributes keyed by their AMP API parameter names.

        """
        data: dict[str, str | int | dict[str, str] | bool] = {
            "TargetADSInstance": self.target_ads_instance,
            "NewInstanceId": self.new_instance_id,
            "Module": self.module,
            "InstanceName": self.instance_name,
            "FriendlyName": self.friendly_name,
            "IPBinding": self.ip_binding,
            "PortNumber": self.port_number,
            "AdminUsername": self.admin_username,
            "AdminPassword": self.admin_password,
            "ProvisionSettings": self.provision_settings,
            "AutoConfigure": self.auto_configure,
            "PostCreate": self.post_create.value,
            "StartOnBoot": self.start_on_boot,
            "DisplayImageSource": self.display_image_source,
            "TargetDatastore": self.target_datastore,
        }
        if self.group is not None:
            data["Group"] = self.group
        return data


# The hand-written class before 5.0.0, when it became a dataclass built with `from_response`.
# class DeploymentTemplate:
#     """Used for :meth:`ADSModule.update_deployment_template` function call.
#
#     .. note::
#         Your pre-created data structure to be parsed for the required API parameters.
#
#
#     Attributes
#     ----------
#     clone_role_into_user : :class:`bool`
#         Clone the :attr:`template_role` to the users of this template.
#     description : Union[:class:`str`, None]
#         The description of the deployment template.
#     id : :class:`int`
#         The ID of the deployment template.
#     module : Union[:class:`str`, None]
#         The AMP Instance module type. eg. "Generic", "Minecraft"
#     name : :class:`str`
#         The deployment template name.
#     template_base_app : Union[:class:`str`, None]
#         The application that is template is used for.
#     template_instance : Any
#         UNK
#     template_role : Union[:class:`str`, None]
#         The template role name, similar to the AMP User Roles.
#     match_datastore_tags : :class:`bool`
#         To force match the datastore tags; if any.
#     setting_mappings : dict[:class:`str`, :class:`str`]
#         A dictionary of setting mappings.
#     start_on_boot : :class:`bool`
#         If the Instance should start on ADS01/Controller boot or not, default is False.
#     tags : list[:class:`str`]
#         The list of tags to assign to the template or that belong to the template.
#     zip_overlay_path : :class:`bool`
#         To zip the overlay path.
#
#     """
#
#     __slots__ = (
#         "clone_role_into_user",
#         "description",
#         "id",
#         "match_datastore_tags",
#         "module",
#         "name",
#         "setting_mappings",
#         "start_on_boot",
#         "tags",
#         "template_base_app",
#         "template_instance",
#         "template_role",
#         "zip_overlay_path",
#     )
#
#     def __init__(
#         self,
#         id: int,  # This is due to id overshadowing Python built-ins.
#         name: str,
#         description: Union[str, None],
#         module: Union[str, None],
#         template_instance: Any,
#         template_role: Union[str, None],
#         template_base_app: Union[str, None],
#         clone_role_into_user: bool,
#         zip_overlay_path: str,
#         match_datastore_tags: bool,
#         setting_mappings: dict[str, str],
#         tags: list[str],
#         start_on_boot: bool = False,
#     ) -> None:
#         self.id: int = id
#         self.name: str = name
#         self.description: Union[str, None] = description
#         self.module: Union[str, None] = module
#         self.template_instance = template_instance
#         self.template_role: Union[str, None] = template_role
#         self.template_base_app: Union[str, None] = template_base_app
#         self.clone_role_into_user: bool = clone_role_into_user
#         self.zip_overlay_path: str = zip_overlay_path
#         self.match_datastore_tags: bool = match_datastore_tags
#         self.setting_mappings: dict[str, str] = setting_mappings
#         self.tags: list[str] = tags
#         self.start_on_boot: bool = start_on_boot
#
#     def to_dict(self) -> dict[str, Any]:
#         """As the function name implies; converts the class to a dict.
#
#         Returns
#         -------
#         dict[:class:`str`, Any]
#             Returns the class attributes in a key, value paired dict.
#
#         """
#         temp: dict[str, Any] = {}
#         for key in self.__slots__:
#             temp[key] = getattr(self, key)
#         return temp


@dataclass(slots=True)
class DeploymentTemplate(ResponseData):
    """Used for :meth:`ADSModule.update_deployment_template` function call.

    .. note::
        Your pre-created data structure to be parsed for the required API parameters.

    .. versionchanged:: 5.0.0
        A dataclass built with :meth:`DeploymentTemplate.from_response`. An unknown key is logged instead of raising.

    Attributes
    ----------
    clone_role_into_user : :class:`bool`
        Clone the :attr:`template_role` to the users of this template.
    description : Union[:class:`str`, None]
        The description of the deployment template.
    id : :class:`int`
        The ID of the deployment template.
    module : Union[:class:`str`, None]
        The AMP Instance module type. eg. "Generic", "Minecraft"
    name : :class:`str`
        The deployment template name.
    template_base_app : Union[:class:`str`, None]
        The application that is template is used for.
    template_instance : Any
        UNK
    template_role : Union[:class:`str`, None]
        The template role name, similar to the AMP User Roles.
    match_datastore_tags : :class:`bool`
        To force match the datastore tags; if any.
    setting_mappings : dict[:class:`str`, :class:`str`]
        A dictionary of setting mappings.
    start_on_boot : :class:`bool`
        If the Instance should start on ADS01/Controller boot or not, default is False.
    tags : list[:class:`str`]
        The list of tags to assign to the template or that belong to the template.
    zip_overlay_path : :class:`str`
        The path of the overlay to zip.

    """

    id: int
    name: str
    description: Union[str, None]
    module: Union[str, None]
    template_instance: Any
    template_role: Union[str, None]
    template_base_app: Union[str, None]
    clone_role_into_user: bool
    zip_overlay_path: str
    match_datastore_tags: bool
    setting_mappings: dict[str, str]
    tags: list[str]
    start_on_boot: bool = False

    def to_dict(self) -> dict[str, Any]:
        """As the function name implies; converts the class to a dict.

        Returns
        -------
        dict[:class:`str`, Any]
            Returns the class attributes in a key, value paired dict.

        """
        temp: dict[str, Any] = {}
        for key in self.__slots__:
            temp[key] = getattr(self, key)
        return temp


# This may be only controller diag info.
@dataclass(slots=True)
class Diagnostics(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_diagnostics_info`.

    Attributes
    ----------
    application_name : :class:`str`
        The Instance application name.
    application_version : :class:`str`
        The Instance application version.
    build_date : :class:`str`
        The date of the AMP Instance build.
    build_spec : :class:`str`
        Similar to :attr:`Diagnostics.release_stream`.
    cpu_layout : :class:`str`
        Number of Sockets, Cores and Threads *eg 1S/2C/10T*
    cpu_model : :class:`str`
        The name of the CPU.
    codename : :class:`str`
        The release/build code name.
    hardware_platform : :class:`str`
        The hardware the system runs on (eg. a motherboard or hypervisor name).
    installed_ram : :class:`str`
        The amount of installed ram on the system.
    instance_id : :class:`str`
        The Instance GUID
    last_arguments : :class:`str`
        The last used arguments when running the Instance.
    last_executable : :class:`str`
        The last used file executable for the Instance.
    last_process_id : :class:`int`
        The last used process ID.
    loaded_plugins : :class:`str`
        The AMP loaded plugin's for the Instance.
    module : :class:`str`
        The Instance module. *eg ADSModule, Minecraft, Generic*
    module_application : :class:`str`
        The Instance application.
    network_mode : :class:`str`
        The network mode of the Instance (eg. "Standard").
    platform : :class:`str`
        The machine full name of the Operating System.
    release_stream : :class:`str`
        Mainline, Developer, etc
    system_type : :class:`str`
        The bit type of the Instance Operating System.
    server_jar : :class:`str`
        The .jar file to rune a Minecraft application Instance.
    server_type : :class:`str`
        The 'type' of server. eg. Forge, Fabric, etc...
    java_version : :class:`str`
        The path to the java lib.
    config_version : :class:`str`
        The version of the application template a Generic Instance runs, "" for every other module.
    tools_version : :class:`str`
        The version of the build tools for the Instance.
    virtualization : :class:`str`
        If the system is using a VM or not. *eg VMware*
    os : :class:`str`
        The machine Operating System.

    """

    os: str
    platform: str
    system_type: str
    hardware_platform: str
    cpu_model: str
    cpu_layout: str
    installed_ram: str
    virtualization: str
    network_mode: str
    module: str
    module_application: str
    loaded_plugins: str
    application_name: str
    application_version: str | BuildInfo
    codename: str
    tools_version: str
    release_stream: str
    build_spec: str
    build_date: str
    instance_id: str
    last_executable: str
    last_arguments: str
    last_process_id: str
    # These appear to be Minecraft Instances only.
    server_jar: str = ""
    server_type: str = ""
    java_version: str = ""
    # Generic Instances (GenericModule) only, eg. a Counter-Strike: Source server sends "3".
    config_version: str = ""

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.application_version, str):
            self.application_version = BuildInfo.to_dataclass(data=self.application_version)


@dataclass(slots=True)
class Directory(ResponseData):
    """Represents the JSON response data from :meth:`FileManagerPlugin.get_directory_listing`

    Attributes
    ----------
    is_directory : :class:`bool`
        If the path is a directory.
    is_virtual_directory : :class:`bool`
        If the path is a virtual directory.
    filename : :class:`str`
        The name of the file or directory.
    size_bytes : :class:`int`
        The size of the file/directory in bytes.
    is_downloadable : :class:`bool`
        If the file can be downloaded.
    is_editable : :class:`bool`
        If the file can be edited.
    is_archive : :class:`bool`
        If the file is an archive.
    is_excluded_from_backups : :class:`bool`
        If the file is excluded from backups.
    created : :class:`str` | :class:`datetime`
        The time the file/directory was created.
    modified : :class:`str` | :class:`datetime`
        The time the file/directory was last modified.
    is_smart_excluded_from_backups : :class:`bool`
        If the file is smart excluded from backups.

    """

    is_directory: bool
    is_virtual_directory: bool
    filename: str
    size_bytes: int
    is_downloadable: bool
    is_editable: bool
    is_archive: bool
    is_excluded_from_backups: bool
    created: str | datetime.datetime
    modified: str | datetime.datetime
    is_smart_excluded_from_backups: bool = False

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.created, str):
            self.created = timestamp_converter(timestamp=self.created)
        if isinstance(self.modified, str):
            self.modified = timestamp_converter(timestamp=self.modified)


@dataclass(slots=True)
class Endpoints(ResponseData):
    """Represents the JSON response data from :meth:`ADSModule.get_application_endpoints`

    Attributes
    ----------
    display_name : :class:`str`
        The name of the endpoint.
    endpoint : :class:`str`
        The name of the endpoint.
    uri : :class:`str`
        The URI of the endpoint.

    """

    display_name: str
    endpoint: str
    uri: str


@dataclass(slots=True)
class FileChunk(ResponseData):
    """Represents the JSON response data from :meth:`FileManagerPlugin.get_file_chunk`

    Attributes
    ----------
    base64_data : :class:`str`
        The base64 encoded string of the file chunk.
    bytes_length : :class:`int`
        The length of the file chunk in bytes.

    """

    base64_data: str
    bytes_length: int


@dataclass(slots=True)
class Fitness(ResponseData):
    """Represents the JSON response data for :attr:`Instance.fitness` attribute.

    Attributes
    ----------
    available : :class:`bool`
        If the Instance is available to create more services or not.
    total_services : :class:`int`
        The total number of services running on the Instance.
    free_ram_mb : :class:`int`
        The amount of free RAM on the Instance.
    free_disk_mb : :class:`int`
        The amount of free disk space on the Instance.
    cpu_service_ratio : :class:`float`
        The ratio of CPU usage to the number of services running on the Instance.
    thread_queue_length : :class:`int`
        The length of the thread queue on the Instance.
    load_avg : :class:`float`
        The load average on the Instance.
    remaining_instance_slots : :class:`int`
        The number of remaining Instance slots on the License.
    score : :class:`float`
        The score of the Instance.
    score_description : :class:`str`
        A summary of the "remaining slots" aka the number of Instances you have left to create.
        * Includes the amount of "Free Ram" and "CPU Ratio".
    score_zero_factors : list[Any]
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


@dataclass(slots=True)
class FolderUploadFile:
    """Represents one file for :meth:`FileManagerPlugin.upload_folder`.

    Attributes
    ----------
    relative_path : :class:`str`
        The path of the file relative to the target directory. Subfolders in the path are created by AMP.
    data : :class:`bytes`
        The raw content of the file.

    """

    relative_path: str
    data: bytes

    def to_dict(self) -> dict[str, str]:
        """Converts the class to a dict for use as an API parameter.

        Returns
        -------
        dict[:class:`str`, :class:`str`]
            The class attributes keyed by their AMP API parameter names, with `data` as base64.

        """
        return {
            "RelativePath": self.relative_path,
            "Base64Data": base64.b64encode(self.data).decode(),
        }


@dataclass(slots=True)
class ImportConfig(ResponseData):
    """Represents the JSON response data from :meth:`GenericModule.import_config`.

    .. note::
        Only empty lists have been observed, so the element types are unconfirmed.

    Attributes
    ----------
    settings : dict[:class:`str`, Any]
        The settings read from the file.
    imported : list[Any]
        The settings that were imported.
    not_imported : list[Any]
        The settings that were not imported.
    unrecognised : list[Any]
        The settings AMP did not recognise.
    rejected : list[Any]
        The settings AMP rejected.

    """

    # TODO: Confirm the element types against a real import.
    # Only empty lists were seen, so they are typed as Any for now.
    settings: dict[str, Any] = field(default_factory=dict[str, Any])
    imported: list[Any] = field(default_factory=list[Any])
    not_imported: list[Any] = field(default_factory=list[Any])
    unrecognised: list[Any] = field(default_factory=list[Any])
    rejected: list[Any] = field(default_factory=list[Any])


@dataclass(slots=True)
class InstanceDatastore(ResponseData):
    """Represents a the class object to be used in :meth:`ADSModule.add_datastore`

    .. warning::
        AMP must have read/write/execute access to the directory specified in the `Directory` parameter.


    .. note::
        This class is also used in :meth:`ADSModule.update_datastore`, :meth:`ADSModule.get_datastores`, :meth:`ADSModule.get_datastore`



    Parameters
    ----------
    id : :class:`int`
        The ID of the datastore.
    friendly_name : :class:`str`
        The friendly name of the datastore.
    description : :class:`str`
        The description of the datastore.
    directory : :class:`str`
        The on-disk location where Instances will be stored. Changing this will not affect existing Instances, only newly created ones.
    soft_limit_mb : :class:`int`
        Datastores that reach or exceed this limit in total size will not be considered as deployment
        targets. This is only a soft limit and does not prevent Instances on this datastore from using
        more space.
    priority : :class:`int`
        Instances with a lower priority number are preferred over those with a higher number, all other factors being equal.
    tags : list[:class:`str`]
        A list of tags to apply to the datastore.
    is_internal : :class:`bool`
        If the datastore is internal.
    instance_limit:
        The maximum number of Instances that can be provisioned on this datastore, defaults to 0 for unlimited.
    active:
        Deactivating a datastore prevents new Instances from being provisioned to it, defaults to True.
    current_usage_mb : :class:`int`
        The current usage of the datastore in megabytes, defaults to -1.
    sanitised_name : :class:`str`
        The sanitised name of the datastore, defaults to "None".

    """

    id: int
    friendly_name: str
    description: str
    directory: str
    soft_limit_mb: int
    priority: int
    tags: list[str]
    is_internal: bool
    instance_limit: Union[int, str] = field(default=0)
    active: bool = field(default=True)
    current_usage_mb: int = field(default=-1)
    # AMP sends the British spelling.
    sanitised_name: str = field(default="None")

    def to_dict(self) -> dict[str, Any]:
        """As the function name implies; converts the class to a dict for use as an API parameter.

        Returns
        -------
        dict[:class:`str`, Any]
            The class attributes as a key, value paired dict; attributes set to None are omitted.

        """
        return _dataclass_to_dict(self)


@dataclass(slots=True)
class InstanceInfo:
    """Represents the JSON response data for :meth:`ADSModule.update_instance_info`.

    Attributes
    ----------
    instance_id : :class:`str`
        The Instance GUID.
    friendly_name : :class:`str`
        The friendly name of the Instance.
    description : :class:`str`
        The description of the Instance.
    suspended : :class:`bool`
        If the Instance is suspended.
    exclude_from_firewall : :class:`bool`
        If the Instance should be excluded from the firewall.
    run_in_container : :class:`bool`
        If the Instance should be run in a container.
    container_memory : :class:`int`
        The amount of memory allocated to the container in MB.
    container_max_cpu : :class:`str`
        The maximum amount of CPU cores allocated to the container.
    container_image : :class:`str`
        The container/docker image to use.
    memory_policy : :class:`ContainerMemoryPolicyState`
        The memory policy of the Instance, default is :attr:`ContainerMemoryPolicyState.reserve`.
    start_on_boot : :class:`bool`
        If the Instance should start on boot, default is False.
    welcome_message : :class:`str`
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

    def to_dict(self) -> dict[str, Any]:
        """As the function name implies; converts the class to a dict for use as an API parameter.

        Returns
        -------
        dict[:class:`str`, Any]
            The class attributes as a key, value paired dict; attributes set to None are omitted.

        """
        return _dataclass_to_dict(self)


@dataclass(slots=True)
class InstanceStatus(ResponseData):
    """Represents the JSON response data from :meth:`ADSModule.get_instance_statuses`.

    Attributes
    ----------
    instance_id : :class:`str`
        The Instance ID.
    running : :class:`bool`
        Whether the Instance is running.

    """

    instance_id: str
    running: bool


@dataclass(slots=True)
class LicenceInfo(ResponseData):
    """Represents the licence AMP reports from :meth:`Core.activate_amp_license`.

    .. warning::
        AMP sends the licence key back in :attr:`licence_key`. Keep it out of logs and files.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    licence_key : :class:`str`
        The licence key, as AMP sends it back.
    grade : :class:`str`
        The ID of the licence grade.
    grade_name : :class:`str`
        The name of the licence grade. (eg. `"Professional"`)
    product : :class:`str`
        The ID of the product the licence is for.
    product_name : :class:`str`
        The name of the product the licence is for. (eg. `"AMP"`)
    expires : Union[:class:`str`, :class:`datetime.datetime`]
        When the licence expires, converted to a naive :class:`datetime.datetime`. AMP sends no timezone, and none is added.
    usage : :class:`int`
        How many times the licence has been used. Its meaning is unconfirmed. Only one value has been seen.

    """

    licence_key: str
    grade: str
    grade_name: str
    product: str
    product_name: str
    expires: str | datetime.datetime
    usage: int

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.expires, str):
            self.expires = timestamp_converter(timestamp=self.expires)

    def __repr__(self) -> str:  # noqa: D105
        # The licence key stays out of the repr, which is what ends up in logs.
        return pformat({key: value for key, value in _field_values(self).items() if key != "licence_key"})


@dataclass(slots=True)
class LoginResults(ResponseData):
    """Represents the JSON response data from the AMP Login response.

    Attributes
    ----------
    success : :class:`bool`
        Whether the login was successful.
    result : :class:`int`
        The result code.
    permissions : Union[list[:class:`str`], None], optional
        A list of permissions, None when the login failed, defaults to [].
    result_reason : :class:`str`, optional
        The result reason, defaults to "".
    session_id : Union[:class:`str`, None], optional
        The session ID, None when the login failed, defaults to "".
    remember_me_token : Union[:class:`str`, None], optional
        The remember me token, None when the login failed, defaults to "".
    user_info : :class:`LoginUserInfo`, optional
        The user information, defaults to None.

    """

    success: bool
    result: int
    # A failed login sends None for these three (confirmed against AMP 2.8.0.8).
    permissions: Union[list[str], None] = field(default_factory=list[str])
    result_reason: str = ""
    session_id: Union[str, None] = ""
    remember_me_token: Union[str, None] = ""
    # LoginUserInfoResponse, not UserInfoResponse; only the login shape carries the username.
    user_info: Union[LoginUserInfo | LoginUserInfoResponse, None] = field(default=None)


@dataclass(slots=True)
class LoginUserInfo(ResponseData):
    """Represents an AMP users information, tied to :class:`LoginResults` along with representing the
    JSON response from the function :meth`~Core.get_amp_users_summary`

    Attributes
    ----------
    id : :class:`str`
        The user ID.
    username : :class:`str`
        The username.
    is_two_factor_enabled : :class:`bool`
        If the user has 2FA enabled.
    disabled : :class:`bool`
        If the user is disabled.
    gravatar_hash : :class:`str`
        The gravatar hash.
    is_ldap_user : :class:`bool`
        If the user is a LDAP user.
    last_login : :class:`datetime`
        The last login date.
    email_address : :class:`str`, optional
        The email address, defaults to "" if not set.

    """

    avatar_base64: str | None
    disabled: bool
    email_address: str | None
    gravatar_hash: str
    id: str
    is_ldap_user: bool
    is_oidc_user: bool
    is_two_factor_enabled: bool
    last_login: str | datetime.datetime
    username: str

    def __post_init__(self) -> None:  # noqa: D105
        # TODO: This may be best handled with a try/except and setting a default value afterwards. - 6/14/26
        if isinstance(self.last_login, str):
            self.last_login = timestamp_converter(self.last_login)


@dataclass(slots=True)
class MCUser(ResponseData):
    """Represents the JSON response data from :meth:`MinecraftModule.mc_get_whitelist`.

    Attributes
    ----------
    name : :class:`str`
        The username.
    uuid : :class:`str`
        The Minecraft UUID.

    """

    name: str
    uuid: str


@dataclass(slots=True)
class MessageParameters(ResponseData):
    """Represents the JSON response data from :attr:`Messages.parameters`.

    .. note::
        Which keys AMP sends depends on the message. A message from the ADSModule carries `instance_id`, `metrics`,
        `state` and `uptime`, a message from the LocalFileBackupPlugin carries `name` and `reason`.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    instance_id : Union[:class:`str`, None], optional
        The ID of the Instance the message is about, default is None.
    metrics : Union[:class:`Metrics`, :class:`MetricsResponse`, None], optional
        The metrics of that Instance, default is None.
    uptime : Union[:class:`Uptime`, :class:`UptimeResponse`, None], optional
        The uptime of that Instance, default is None.
    state : Union[:class:`InstanceState`, :class:`int`, None], optional
        The state of that Instance, default is None.
    name : Union[:class:`str`, None], optional
        The name of the backup, default is None.
    reason : Union[:class:`str`, None], optional
        The reason for the backup message, default is None.

    """

    instance_id: Union[str, None] = field(default=None)
    # AMP sends `state` as an int and __post_init__ converts it.
    metrics: Union[Metrics, MetricsResponse, None] = field(default=None)
    uptime: Union[Uptime, UptimeResponse, None] = field(default=None)
    state: Union[InstanceState, int, None] = field(default=None)
    name: Union[str, None] = field(default=None)
    reason: Union[str, None] = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.state, int):
            self.state = InstanceState(self.state)


@dataclass(slots=True)
class Messages(ResponseData):
    """Represents a Message from the dataclass attribute :attr:`Updates.messages`

    Attributes
    ----------
    age_minutes : :class:`int`
        The age of the message in minutes.
    expired : :class:`bool`
        Whether the message has expired.
    id : :class:`str`
        The message ID.
    message : :class:`str`
        The message.
    source : :class:`str`
        The source of the message.
    parameters : Union[:class:`MessageParameters`, :class:`MessageParametersResponse`, None], optional
        Extra data for the message, default is None.

        .. versionadded:: 5.0.0

    """

    age_minutes: int
    expired: bool
    id: str
    message: str
    source: str
    # Confirmed against getupdates.json; defaulted so older responses still construct.
    parameters: Union[MessageParameters, MessageParametersResponse, None] = field(default=None)


@dataclass(slots=True)
class Methods(ResponseData):
    """Tied to :attr:`ScheduleData.available_methods`.

    Hold's information regarding Methods/Events that are available to the Instance. Varies depending on Instance type.

    Attributes
    ----------
    id : :class:`str`
        The method ID.
    name : :class:`str`
        The method name.
    description : :class:`str`
        The method description.
    category : :class:`str`
        The category the method appears under in the Schedule UI, default is "".
    display_format : Union[:class:`str`, None]
        How the Schedule UI renders the method, default is None.
    consumes : list[:class:`Consumes` | :class:`ConsumesResponse`]
        A list of parameters the method consumes.
    notice : Union[:class:`str`, None], optional
        A note the Schedule UI shows for the method, default is None.

        .. versionadded:: 5.0.0

    """

    id: str = ""
    name: str = ""
    description: str = ""
    # Confirmed against getscheduledata.json.
    category: str = ""
    display_format: Union[str, None] = field(default=None)
    # `Methods.from_response(entry)` turns these into Consumes.
    consumes: list[Consumes] | list[ConsumesResponse] = field(default_factory=list[Consumes])
    notice: Union[str, None] = field(default=None)

    __hash__ = None  # type: ignore[assignment]
    """Mutable dataclass; intentionally unhashable."""

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.name == other.name

    def __lt__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.name < other.name


@dataclass(slots=True)
class Metrics(ResponseData):
    """Represents the JSON response data for :attr:`Status.metrics`.

    Attributes
    ----------
    active_users : :class:`MetricsData`
        The active users data.
    cpu_usage : :class:`MetricsData`
        The cpu usage data.
    memory_usage : :class:`MetricsData`
        The memory usage data.
    physical_ram_usage : Union[:class:`MetricsData`, None], optional
        The physical ram usage data, only sent by the ADS, default is None.
    swap_usage : Union[:class:`MetricsData`, None], optional
        The swap usage data, only sent by the ADS, default is None.
    tps : Union[:class:`MetricsData`, None], optional
        The ticks per second, only sent by some Minecraft Instances (eg. modded), default is None.

    """

    active_users: MetricsData
    cpu_usage: MetricsData
    memory_usage: MetricsData
    # Confirmed against AMP 2.8.0.8; which of these are sent depends on the Instance type.
    physical_ram_usage: Union[MetricsData, None] = field(default=None)
    swap_usage: Union[MetricsData, None] = field(default=None)
    tps: Union[MetricsData, None] = field(default=None)


@dataclass(slots=True)
class MetricsData(ResponseData):
    """Represents the JSON response data for each of the attributes of :class:`Metrics`.

    Attributes
    ----------
    raw_value : :class:`int`
        The raw value, or the current value of the field.
    max_value : :class:`int`
        The max value the field can have.
    percent : :class:`int`
        The percent of usage in relation to the ``max_value``.
    units : :class:`str`
        The unit of measurement for the field.
    color : Union[None, :class:`str`]
        Color number 1 if applicable..
    color2 : Union[None, :class:`str`]
        Color number 2 if applicable.
    color3 : Union[None, :class:`str`]
        Color number 3 if applicable.
    short_name : Union[None, :class:`str`], optional
        The short label AMP displays on the metric tile (eg "CPU", "RAM"), default is None.

    """

    raw_value: int
    max_value: int
    percent: int
    units: str
    color: Union[str, None] = field(default=None)
    color2: Union[str, None] = field(default=None)
    color3: Union[str, None] = field(default=None)
    # Present on every metric in getstatus.json; defaulted so older responses still construct.
    short_name: Union[str, None] = field(default=None)


@dataclass(slots=True)
class Module(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_module_info`.

    Attributes
    ----------
    amp_build : :class:`str`
        The AMP build.
    amp_version : :class:`str`
        The AMP version.
    api_version : :class:`str`
        The API version.
    allow_remember_me : :class:`bool`
        Whether remember me is allowed.
    analytics : :class:`bool`
        Whether analytics is enabled.
    analytics_tag : :class:`str`
        The analytics tag.
    app_name : :class:`str`
        The app name.
    author : :class:`str`
        The author.
    base_port : :class:`int`
        The base port.
    branding : :class:`Branding` | :class:`BrandingResponse`
        The branding data.

        .. versionchanged:: 5.0.0
            Is a :class:`Branding`, was a dict.
    build_spec : :class:`str`
        The build spec.
    display_base_uri : :class:`str`
        The display base URI.
    endpoint_uri : :class:`str`
        The endpoint URI.
    feature_set : list[:class:`str`]
        The feature set.
    friendly_name : :class:`str`
        The friendly name.
    instance_id : :class:`str`
        The Instance ID.
    instance_name : :class:`str`
        The Instance name.
    is_oidc_enabled : :class:`bool`
        Whether OIDC login is enabled.
    is_remote_instance : :class:`bool`
        Whether the Instance is remote.
    local_login_enabled : :class:`bool`, optional
        Whether logging in with a local AMP user is enabled, default is True.

        .. versionadded:: 5.0.0
    loaded_plugins : :class:`list[str]`
        A list of loaded plugins.
    module_name : :class:`str`
        The module name.
    name : :class:`str`
        The full name.
    oidc_provider_friendly_name : :class:`str`
        The OIDC provider friendly name.
    primary_endpoint : :class:`str`
        The primary endpoint.
    requires_full_load : :class:`bool`
        Whether the Instance requires full load.
    supports_sleep : :class:`bool`
        Whether the Instance supports sleep.
    timestamp : :class:`str`
        The current timestamp.
    tools_version : :class:`str`
        The tools version.
    version_codename : :class:`str`
        The version codename.

    """

    amp_build: str
    amp_version: str
    api_version: str
    allow_remember_me: bool
    analytics: bool
    analytics_tag: str
    app_name: str
    author: str
    base_port: int
    branding: Branding | BrandingResponse
    build_spec: str
    display_base_uri: str
    endpoint_uri: str
    feature_set: list[str]
    friendly_name: str
    instance_id: str
    instance_name: str
    is_oidc_enabled: bool
    is_remote_instance: bool
    loaded_plugins: list[str]
    module_name: str
    name: str
    oidc_provider_friendly_name: str
    primary_endpoint: str
    requires_full_load: bool
    supports_sleep: bool
    timestamp: str
    tools_version: str
    version_codename: str
    local_login_enabled: bool = True


@dataclass(slots=True)
class OPList(ResponseData):
    """Represents the JSON response data from :meth:`MinecraftModule.mc_load_op_list`.

    Attributes
    ----------
    level : :class:`int`
        The level of the operator user.
    name : :class:`str`
        The name of the user.
    uuid : :class:`str`
        The UUID of the user.

    """

    level: int
    name: str
    uuid: str


@dataclass(slots=True)
class OPWhitelist(ResponseData):
    """Represents the JSON response data from :meth:`MinecraftModule.mc_get_op_whitelist`.

    Attributes
    ----------
    op_list : list[:class:`MCUserResponse`]
        The list of operator users.
    whitelist : list[:class:`MCUserResponse`]
        The list of whitelisted users.

    """

    op_list: list[MCUserResponse] = field(default_factory=list["MCUserResponse"])
    whitelist: list[MCUserResponse] = field(default_factory=list["MCUserResponse"])


@dataclass(slots=True)
class ParameterMapping(ResponseData):
    """Represents the JSON response data for :attr:`TriggerTasks.parameter_mapping`.

    The arguments a task passes to its method. An argument the task's method doesn't take is None.
    AMP sends every value as a string (eg. `"true"`, `"55"`), which can hold a trigger variable (eg. `{@User}`).
    An empty string in a converted field becomes None.

    .. versionchanged:: 5.0.0
        Renamed from `DCParameterMapping`.
        Holds the arguments of every task method in AMP-2.8.0.8, not only `user`, `reason`, `title` and `subtitle`.
        An argument the task doesn't hold is None, not "".
        Booleans, numbers, `state`, `operation`, `priority` and `when` are converted from AMP's strings.
        A value that doesn't parse stays a string.

    Attributes
    ----------
    authorization_header : Union[:class:`str`, None], optional
        The `Authorization` header of the request (`WebRequestPlugin.MakePOSTRequest`), default is None.
    avatar_url : Union[:class:`str`, None], optional
        The URL of the avatar the message is posted with (`WebRequestPlugin.DiscordEmbedMessage`,
        `WebRequestPlugin.DiscordMessage`), default is None.
    backup_id : Union[:class:`str`, None], optional
        The ID of the backup to restore (`LocalFileBackupPlugin.RestoreBackup`), default is None.
    backup_while_running : Union[:class:`bool`, :class:`str`, None], optional
        If the backup is taken while the application is running (`LocalFileBackupPlugin.TakeBackup`), default is None.
    body : Union[:class:`str`, None], optional
        The body of the push message (`WebRequestPlugin.PushMessage`, `WebRequestPlugin.PushMessageChannel`), default is
        None.
    button_label : Union[:class:`str`, None], optional
        The label of the embed's button (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    button_url : Union[:class:`str`, None], optional
        The URL the embed's button opens (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    channel : Union[:class:`str`, None], optional
        The channel the push message is sent to (`WebRequestPlugin.PushMessageChannel`), default is None.
    color_hex : Union[:class:`str`, None], optional
        The colour of the embed, as a hex code (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    command : Union[:class:`str`, None], optional
        The command to run once the warnings have been sent (`CommonCorePlugin.CommandWithWarnings`), default is None.
    content_type : Union[:class:`str`, None], optional
        The `Content-Type` header of the request (`WebRequestPlugin.MakePOSTRequest`), default is None.
    contents : Union[:class:`str`, None], optional
        The text of the message (`WebRequestPlugin.DiscordMessage`, `WebRequestPlugin.SlackMessage`), default is None.
    description : Union[:class:`str`, None], optional
        The description of the embed (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    dirty_only : Union[:class:`bool`, :class:`str`, None], optional
        If the backup is taken only when files have changed since the last one (`LocalFileBackupPlugin.TakeBackup`),
        default is None.
    display_username : Union[:class:`str`, None], optional
        The name the message is posted under (`WebRequestPlugin.DiscordEmbedMessage`,
        `WebRequestPlugin.DiscordMessage`), default is None.
    existing_message_id : Union[:class:`str`, None], optional
        The ID of an existing message to edit in place of posting a new one (`WebRequestPlugin.DiscordEmbedMessage`),
        default is None.
    fields : Union[:class:`str`, None], optional
        The fields of the embed (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    five_mins : Union[:class:`str`, None], optional
        The warning sent five minutes before the command (`CommonCorePlugin.CommandWithWarnings`), default is None.
    five_secs : Union[:class:`str`, None], optional
        The warning sent five seconds before the command (`CommonCorePlugin.CommandWithWarnings`), default is None.
    footer_icon_url : Union[:class:`str`, None], optional
        The URL of the embed's footer icon (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    footer_text : Union[:class:`str`, None], optional
        The text of the embed's footer (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    headers : Union[:class:`str`, None], optional
        The headers of the request (`WebRequestPlugin.MakePOSTRequest`), default is None.
    image_url : Union[:class:`str`, None], optional
        The URL of the embed's image (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    input : Union[:class:`str`, None], optional
        The console input to send (`MinecraftModule.SendConsole`, `MinecraftModule.SendConsoleAdv`,
        `MinecraftModule.SendMultipleConsole`), default is None.
    instance_name_or_id : Union[:class:`str`, None], optional
        The name or ID of the Instance (`ADSModule.RestartInstance`, `ADSModule.StartInstance`,
        `ADSModule.StopInstance`), default is None.
    local : Union[:class:`bool`, :class:`str`, None], optional
        If the backup is kept locally (`LocalFileBackupPlugin.TakeBackup`), default is None.
    mac_address : Union[:class:`str`, None], optional
        The MAC address to send the Wake-on-LAN packet to (`CommonCorePlugin.SendWakeOnLan`), default is None.
    message : Union[:class:`str`, None], optional
        The message to send (`EmailSenderPlugin.SendMail`, `GenericModule.WriteLine`,
        `MinecraftModule.SendServerMessage`, `MinecraftModule.SendUserMessage`), default is None.
    one_hour : Union[:class:`str`, None], optional
        The warning sent one hour before the command (`CommonCorePlugin.CommandWithWarnings`), default is None.
    one_min : Union[:class:`str`, None], optional
        The warning sent one minute before the command (`CommonCorePlugin.CommandWithWarnings`), default is None.
    operation : Union[:class:`IfOperators`, :class:`str`, None], optional
        How `value_to_check` is compared with `value_to_compare`, as an :class:`IfOperators`
        (`CommonCorePlugin.ElseIfCondition`, `CommonCorePlugin.IfCondition`), default is None.
    payload : Union[:class:`str`, None], optional
        The body of the request (`WebRequestPlugin.MakePOSTRequest`), default is None.
    player : Union[:class:`str`, None], optional
        The player the message is sent to (`MinecraftModule.SendUserMessage`), default is None.
    priority : Union[:class:`MailPriority`, :class:`str`, None], optional
        The priority of the email, as a :class:`MailPriority` (`EmailSenderPlugin.SendMail`), default is None.
    quantity : Union[:class:`int`, :class:`str`, None], optional
        The amount of XP to give (`MinecraftModule.GiveXP`), default is None.
    reason : Union[:class:`str`, None], optional
        The reason given to the user (`MinecraftModule.BanUser`, `MinecraftModule.BanUserIP`,
        `MinecraftModule.KickUser`), default is None.
    restart_even_if_not_running : Union[:class:`bool`, :class:`str`, None], optional
        If the application is started after the backup even when it was not running before
        (`LocalFileBackupPlugin.TakeBackup`), default is None.
    s3 : Union[:class:`bool`, :class:`str`, None], optional
        If the backup is uploaded to S3 (`LocalFileBackupPlugin.TakeBackup`), default is None.
    seconds : Union[:class:`float`, :class:`str`, None], optional
        The number of seconds to wait (`CommonCorePlugin.Wait`), default is None.
    state : Union[:class:`InstanceState`, :class:`str`, None], optional
        The application state to check for, as an :class:`InstanceState` (`CommonCorePlugin.ElseIfAppState`,
        `CommonCorePlugin.IfAppState`, `CommonCorePlugin.IfNotAppState`, `CommonCorePlugin.WaitForAppState`), default is
        None.
    sticky : Union[:class:`bool`, :class:`str`, None], optional
        If the backup is kept when old backups are removed (`LocalFileBackupPlugin.TakeBackup`), default is None.
    subject : Union[:class:`str`, None], optional
        The subject of the email (`EmailSenderPlugin.SendMail`), default is None.
    subtitle : Union[:class:`str`, None], optional
        The subtitle to show (`MinecraftModule.SendGlobalTitle`, `MinecraftModule.SendTitle`), default is None.
    target : Union[:class:`str`, None], optional
        The player to teleport to (`MinecraftModule.TeleportToPlayer`), default is None.
    thirty_mins : Union[:class:`str`, None], optional
        The warning sent thirty minutes before the command (`CommonCorePlugin.CommandWithWarnings`), default is None.
    thirty_secs : Union[:class:`str`, None], optional
        The warning sent thirty seconds before the command (`CommonCorePlugin.CommandWithWarnings`), default is None.
    thumbnail_url : Union[:class:`str`, None], optional
        The URL of the embed's thumbnail (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    timeout_seconds : Union[:class:`int`, :class:`str`, None], optional
        The number of seconds to wait for the state before giving up (`CommonCorePlugin.WaitForAppState`), default is
        None.
    title : Union[:class:`str`, None], optional
        The title to show or send (`MinecraftModule.SendGlobalTitle`, `MinecraftModule.SendTitle`,
        `WebRequestPlugin.DiscordEmbedMessage`, `WebRequestPlugin.PushMessage`, `WebRequestPlugin.PushMessageChannel`),
        default is None.
    to : Union[:class:`str`, None], optional
        The address the email is sent to (`EmailSenderPlugin.SendMail`), default is None.
    uri : Union[:class:`str`, None], optional
        The URI the request is sent to (`WebRequestPlugin.MakeGETRequest`, `WebRequestPlugin.MakePOSTRequest`), default
        is None.
    url : Union[:class:`str`, None], optional
        The URL the embed's title links to (`WebRequestPlugin.DiscordEmbedMessage`), default is None.
    user : Union[:class:`str`, None], optional
        The user the task acts on (`MinecraftModule.BanUser`, `MinecraftModule.BanUserIP`, `MinecraftModule.Fabulous`,
        `MinecraftModule.GiveXP`, `MinecraftModule.KickUser`, `MinecraftModule.KillPlayer`, `MinecraftModule.SendTitle`,
        `MinecraftModule.SmitePlayer`, `MinecraftModule.TeleportToCoords`, `MinecraftModule.TeleportToPlayer`,
        `MinecraftModule.Weaken`), default is None.
    value_to_check : Union[:class:`str`, None], optional
        The value to check (`CommonCorePlugin.ElseIfCondition`, `CommonCorePlugin.IfCondition`), default is None.
    value_to_compare : Union[:class:`str`, None], optional
        The value `value_to_check` is compared with (`CommonCorePlugin.ElseIfCondition`,
        `CommonCorePlugin.IfCondition`), default is None.
    webhook_url : Union[:class:`str`, None], optional
        The webhook URL the message is posted to (`WebRequestPlugin.DiscordEmbedMessage`,
        `WebRequestPlugin.DiscordMessage`, `WebRequestPlugin.SlackMessage`), default is None.
    when : Union[:class:`datetime`, :class:`str`, None], optional
        The time to set, as a naive :class:`datetime` (`MinecraftModule.SetGameTime`), default is None.
    x : Union[:class:`float`, :class:`str`, None], optional
        The X coordinate to teleport to (`MinecraftModule.TeleportToCoords`), default is None.
    y : Union[:class:`float`, :class:`str`, None], optional
        The Y coordinate to teleport to (`MinecraftModule.TeleportToCoords`), default is None.
    y_angle : Union[:class:`float`, :class:`str`, None], optional
        The Y angle to face after the teleport (`MinecraftModule.TeleportToCoords`), default is None.
    z : Union[:class:`float`, :class:`str`, None], optional
        The Z coordinate to teleport to (`MinecraftModule.TeleportToCoords`), default is None.
    z_angle : Union[:class:`float`, :class:`str`, None], optional
        The Z angle to face after the teleport (`MinecraftModule.TeleportToCoords`), default is None.

    """

    _bool_fields: ClassVar[tuple[str, ...]] = (
        "backup_while_running",
        "dirty_only",
        "local",
        "restart_even_if_not_running",
        "s3",
        "sticky",
    )
    _int_fields: ClassVar[tuple[str, ...]] = ("quantity", "timeout_seconds")
    _float_fields: ClassVar[tuple[str, ...]] = ("seconds", "x", "y", "z", "y_angle", "z_angle")

    authorization_header: Union[str, None] = field(default=None)
    avatar_url: Union[str, None] = field(default=None)
    backup_id: Union[str, None] = field(default=None)
    backup_while_running: Union[bool, str, None] = field(default=None)
    body: Union[str, None] = field(default=None)
    button_label: Union[str, None] = field(default=None)
    button_url: Union[str, None] = field(default=None)
    channel: Union[str, None] = field(default=None)
    color_hex: Union[str, None] = field(default=None)
    command: Union[str, None] = field(default=None)
    content_type: Union[str, None] = field(default=None)
    contents: Union[str, None] = field(default=None)
    description: Union[str, None] = field(default=None)
    dirty_only: Union[bool, str, None] = field(default=None)
    display_username: Union[str, None] = field(default=None)
    existing_message_id: Union[str, None] = field(default=None)
    fields: Union[str, None] = field(default=None)
    five_mins: Union[str, None] = field(default=None)
    five_secs: Union[str, None] = field(default=None)
    footer_icon_url: Union[str, None] = field(default=None)
    footer_text: Union[str, None] = field(default=None)
    headers: Union[str, None] = field(default=None)
    image_url: Union[str, None] = field(default=None)
    input: Union[str, None] = field(default=None)
    instance_name_or_id: Union[str, None] = field(default=None)
    local: Union[bool, str, None] = field(default=None)
    mac_address: Union[str, None] = field(default=None)
    message: Union[str, None] = field(default=None)
    one_hour: Union[str, None] = field(default=None)
    one_min: Union[str, None] = field(default=None)
    operation: Union[IfOperators, str, None] = field(default=None)
    payload: Union[str, None] = field(default=None)
    player: Union[str, None] = field(default=None)
    priority: Union[MailPriority, str, None] = field(default=None)
    quantity: Union[int, str, None] = field(default=None)
    reason: Union[str, None] = field(default=None)
    restart_even_if_not_running: Union[bool, str, None] = field(default=None)
    s3: Union[bool, str, None] = field(default=None)
    seconds: Union[float, str, None] = field(default=None)
    state: Union[InstanceState, str, None] = field(default=None)
    sticky: Union[bool, str, None] = field(default=None)
    subject: Union[str, None] = field(default=None)
    subtitle: Union[str, None] = field(default=None)
    target: Union[str, None] = field(default=None)
    thirty_mins: Union[str, None] = field(default=None)
    thirty_secs: Union[str, None] = field(default=None)
    thumbnail_url: Union[str, None] = field(default=None)
    timeout_seconds: Union[int, str, None] = field(default=None)
    title: Union[str, None] = field(default=None)
    to: Union[str, None] = field(default=None)
    uri: Union[str, None] = field(default=None)
    url: Union[str, None] = field(default=None)
    user: Union[str, None] = field(default=None)
    value_to_check: Union[str, None] = field(default=None)
    value_to_compare: Union[str, None] = field(default=None)
    webhook_url: Union[str, None] = field(default=None)
    when: Union[datetime.datetime, str, None] = field(default=None)
    x: Union[float, str, None] = field(default=None)
    y: Union[float, str, None] = field(default=None)
    y_angle: Union[float, str, None] = field(default=None)
    z: Union[float, str, None] = field(default=None)
    z_angle: Union[float, str, None] = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105
        # AMP sends every value as a string. An empty one becomes None, a value that doesn't parse stays as sent.
        for name in self._bool_fields:
            raw_value = getattr(self, name)
            if raw_value == "":
                setattr(self, name, None)
            elif isinstance(raw_value, str) and raw_value.lower() in ("true", "false"):
                setattr(self, name, raw_value.lower() == "true")

        for name in self._int_fields:
            raw_value = getattr(self, name)
            if raw_value == "":
                setattr(self, name, None)
            elif isinstance(raw_value, str):
                try:
                    setattr(self, name, int(raw_value))
                except ValueError:
                    pass

        for name in self._float_fields:
            raw_value = getattr(self, name)
            if raw_value == "":
                setattr(self, name, None)
            elif isinstance(raw_value, str):
                try:
                    setattr(self, name, float(raw_value))
                except ValueError:
                    pass

        if self.state == "":
            self.state = None
        elif isinstance(self.state, str):
            try:
                self.state = InstanceState(int(self.state))
            except ValueError:
                pass

        if self.operation == "":
            self.operation = None
        elif isinstance(self.operation, str):
            try:
                self.operation = IfOperators(int(self.operation))
            except ValueError:
                pass

        if self.priority == "":
            self.priority = None
        elif isinstance(self.priority, str):
            try:
                self.priority = MailPriority(int(self.priority))
            except ValueError:
                pass

        if self.when == "":
            self.when = None
        elif isinstance(self.when, str):
            raw_when = self.when
            # AMP keeps an ISO value as sent, and rewrites one with seconds as month/day/year.
            try:
                self.when = datetime.datetime.fromisoformat(raw_when)
            except ValueError:
                try:
                    self.when = datetime.datetime.strptime(raw_when, "%m/%d/%Y %H:%M:%S")  # noqa: DTZ007
                except ValueError:
                    pass


@dataclass(slots=True)
class PermissionNode(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_permissions_spec`.

    .. versionchanged:: 5.0.0
        Is a dataclass, was a `TypedDict` in 4.6.0 (now :class:`PermissionNodeResponse`).

    Attributes
    ----------
    name : :class:`str`
        The name of the node.
    node : :class:`str`
        The full permission node (eg. "Settings.Core.Security").
    display_name : :class:`str`
        The name the web panel shows.
    description : Union[:class:`str`, None]
        The description of the node.
    children : Union[list[:class:`PermissionNode`], None]
        The nodes below this one, None on a node AMP sends no list for.

    """

    name: str
    node: str
    display_name: str
    description: Union[str, None]
    children: Union[list[PermissionNode], None]


@dataclass(slots=True)
class PlatformInfo(ResponseData):
    """Represents the data from the attribute :attr:`RemoteTargetInfo.platform_info`.

    Attributes
    ----------
    cpu_info : :class:`CPUInfo`
        The CPU information.
    installed_ram_mb : :class:`int`
        The installed RAM in MB of the system.
    os : :class:`int`
        The system operating system.
    platform_name : :class:`str`
        The platform name.
    system_type : :class:`int`
        The system type.
    virtualization : :class:`int`
        The virtualization.
    is_shared_setup : :class:`bool`
        Whether the Instance is shared setup.
    admin_rights : :class:`int`
        The admin rights level.
    hardware_platform_name : :class:`str`
        The hardware platform name.
    installed_glibc_version : :class:`str`
        The installed glibc version.
    docker_network_is_host_mode : :class:`bool`
        If the target's Docker network runs in host mode, defaults to False.
    has_memory_limit : :class:`bool`
        If the target has a memory limit applied, defaults to False.
    max_swap_mb : :class:`int`
        The maximum swap in MB available to the target, defaults to 0.

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
    # GetTargetInfo omits the four fields above; the `platform` block on a GetInstances target sends them
    # plus `max_swap_mb`. Everything here is defaulted so both shapes construct.
    docker_network_is_host_mode: bool = field(default=False)
    has_memory_limit: bool = field(default=False)
    max_swap_mb: int = field(default=0)


class Player(NamedTuple):
    """Represents a single player connected to a server.

    Attributes
    ----------
    uuid : :class:`str`
        The UUID of the player.
    name : :class:`str`
        The name of the player.

    """

    uuid: str = ""
    name: str = ""

    def __hash__(self) -> int:  # noqa: D105
        return hash(self.name)

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.name == other.name

    def __lt__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.name < other.name


@dataclass(init=False, slots=True)
class Players:
    """Represents the JSON response data from :meth:`~Core.get_user_list`.

    .. note::
        The print out of this dataclass can be long depending on the number of players connected due to separation by newline.


    Attributes
    ----------
    sorted : list[:class:`Player`]
        A sorted list of :class:`Player` objects by name.

    """

    # {'781a2971-c14b-42c2-8742-d1e2b029d00a': 'k8_thekat', '50686fad-4027-4bdb-a4a5-2533f8a1e51f': 'WolfDevilAngel'}
    sorted: list[Player]

    def __init__(self, data: dict[str, Any]) -> None:  # noqa: D107
        self.sorted = []
        for uuid, name in data.items():
            self.sorted.append(Player(uuid=uuid, name=str(name)))
        self.sorted.sort(key=attrgetter("name"))

    def __repr__(self) -> str:  # noqa: D105
        return "\n".join([p.name for p in self.sorted])

    def get_player(self, name_or_uuid: str) -> list[Player]:
        """Search for a player by their name or UUID.

        Parameters
        ----------
        name_or_uuid : :class:`str`
            The players name or UUID.

        Returns
        -------
        :class:`list[Player]`
            A list of :class:`Player` objects matching the search string.

        """
        return [p for p in self.sorted if name_or_uuid in (p.name, p.uuid)]


@dataclass(slots=True)
class Port(ResponseData):
    """Current Port of the related AMP Instance. Tied to :attr:`Updates.ports` and the JSON response
    data from :meth:`Core.get_port_summaries`.

    Attributes
    ----------
    listening : :class:`bool`
        Whether the port is listening.
    name : :class:`str`
        The name of the port.
    port : :class:`int`
        The port number.
    protocol : :class:`int`
        The protocol number.
    required : :class:`bool`
        Whether the port is required.
    is_delayed_open : :class:`bool`
        Whether the port is delayed open.

    """

    listening: bool
    name: str
    port: int
    protocol: int
    required: Union[bool, None] = field(default=None)
    is_delayed_open: Union[bool, None] = field(default=None)
    # Added in AMP 2.8; defaulted so older responses still construct.
    listening_count: Union[int, None] = field(default=None)
    range: Union[int, None] = field(default=None)
    min_listening: Union[int, None] = field(default=None)


@dataclass(slots=True)
class PortInfo(ResponseData):
    """Represents the JSON response data from :meth:`ADSModule.get_instance_network_info`.

    Attributes
    ----------
    description : :class:`str`
        The description.
    is_user_defined : :class:`bool`
        Whether the port is user defined.
    port_number : :class:`int`
        The port number.
    protocol : :class:`int`
        The protocol number.
        ```
        0 = TCP
        1 = UDP
        2 = TCP & UDP
        ```
    provision_node_name : :class:`str`
        The provision node name.
    range : :class:`int`
        The range.
    verified : :class:`bool`
        Whether the port is verified.
    is_firewall_target : :class:`bool`
        Whether the port is targeted by a firewall rule, defaults to False.

    """

    description: str
    is_user_defined: bool
    port_number: int
    protocol: Protocols | int
    provision_node_name: str
    range: int
    verified: bool
    is_firewall_target: bool = field(default=False)
    # Added in AMP 2.8.0.4; defaulted so 2.6.5.0 responses still construct.
    is_child: bool = field(default=False)
    min_listening: int = field(default=0)
    offset: int = field(default=0)
    parent_node: Union[str, None] = field(default=None)
    parent_ref: Union[str, None] = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105
        # AMP sends the protocol as an int; convert it so the annotation holds true.
        if isinstance(self.protocol, int):
            self.protocol = Protocols(self.protocol)


@dataclass(slots=True)
class Provision(ResponseData):
    """Represents the JSON response data from :meth:`ADSModule.get_provision_fitness`.

    Attributes
    ----------
    available : :class:`bool`
        Whether the Instance is available.
    cpu_service_ratio : :class:`float`
        The CPU service ratio.
    free_disk_mb : :class:`int`
        The free disk in MB.
    free_ram_mb : :class:`int`
        The free RAM in MB.
    load_avg : :class:`float`
        The load average.
    remaining_instance_slots : :class:`int`
        The remaining Instance slots.
    score : :class:`float`
        The score.
    thread_queue_length : :class:`int`
        The thread queue length.
    total_services : :class:`int`
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


@dataclass(slots=True)
class ProvisionSettingInfo(ResponseData):
    """Represents the JSON response data from :meth:`ADSModule.get_provision_arguments`.

    Attributes
    ----------
    default_value : Union[:class:`str`, :class:`int`, None]
        The default value.
    description : :class:`str`
        The description.
    endpoint_name : :class:`str`
        The endpoint name.
    node : :class:`str`
        The node.
    type : :class:`str`
        The type.
    value_range : Union[:class:`int`, :class:`str`]
        The value range.
    custom_field_type : Union[:class:`str`, None]
        The custom field type, if the setting uses one. (eg. "TCPUDPPort") Defaults to None.
    related_setting : Union[:class:`str`, None]
        The node of a setting this one is tied to, otherwise None.
    endpoint_format : Union[:class:`str`, None]
        The format string used to render the endpoint, otherwise None.

    """

    default_value: Union[str, int, None]
    description: str
    endpoint_name: str
    node: str
    type: str
    value_range: Union[int, str]
    custom_field_type: Union[str, None] = field(default=None)
    related_setting: Union[str, None] = field(default=None)
    endpoint_format: Union[str, None] = field(default=None)
    # Added in AMP 2.8.0.4; defaulted so 2.6.5.0 responses still construct.
    hidden: bool = field(default=False)
    min_listening: int = field(default=0)


@dataclass(slots=True)
class RemoteTargetInfo(ResponseData):
    """Represents the JSON response data from :meth:`ADSModule.get_target_info`.

    Attributes
    ----------
    ip_address_list : :class:`list[str]`
        The IP address list.
    platform_info : :class:`PlatformInfo`
        The Target's platform, with its :class:`CPUInfo`.
    datastores : list[:class:`TargetDatastore`]
        The datastores, carrying only an ID and a friendly name.

        .. versionchanged:: 5.0.0
            Holds :class:`TargetDatastore`, not :class:`InstanceDatastore`.
    deploys_in_containers : :class:`bool`
        If the target deploys Instances inside containers.

    """

    ip_address_list: list[str]
    # `RemoteTargetInfo.from_response(result)` turns these into dataclasses.
    platform_info: PlatformInfo
    datastores: list[TargetDatastore]
    deploys_in_containers: bool


@dataclass(slots=True)
class Role(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_role`.

    Attributes
    ----------
    id : :class:`str`
        The ID of the AMP role.
    is_default : :class:`bool`
        If the AMP role is the default role or not.
    name : :class:`str`
        The name of the AMP role.
    description : :class:`str`
        The description of the AMP role.
    hidden : :class:`bool`
        If the AMP role is hidden or not.
    permissions : :class:`list[str]`
        The list of permissions the AMP role has.
    members : list[:class:`RoleMember`]
        The list of AMP users who have the role.

        .. versionchanged:: 5.0.0
            `members` holds :class:`RoleMember` objects.
    is_instance_specific : :class:`bool`
        If the AMP role is only for a specific Instance or not.
    is_common_role : :class:`bool`
        If the AMP role is common or not.
    disable_edits : :class:`bool`
        If the AMP role can be edited by users with the role or not.

    """

    id: str
    is_default: bool
    name: str
    description: str
    hidden: bool
    permissions: list[str]
    # `Role.from_response(result)` turns these into dataclasses.
    members: list[RoleMember]
    is_instance_specific: bool
    is_common_role: bool
    disable_edits: bool


@dataclass(slots=True)
class RoleMember(ResponseData):
    """Represents an AMP user in :attr:`Role.members`.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    id : :class:`str`
        The ID of the AMP user.
    name : :class:`str`
        The name of the AMP user.

    """

    id: str
    name: str


@dataclass(slots=True)
class RunningTask(ResponseData):
    """Represents the JSON response data from functions that return RunningTask.

    Attributes
    ----------
    is_primary_task : :class:`bool`
        If the task is the primary task or not.
    start_time : :class:`str` | :class:`datetime.datetime`
        The start time of the task; converted to a :class:`datetime` object.
    id : :class:`str`
        The ID of the task.
    remote_instance_id : :class:`str` | None
        The GUID of the Instance the task belongs to, otherwise None when the task is local.
    parent_task_id : :class:`str` | None
        The ID of the task that spawned this one, otherwise None when it has no parent.
    name : :class:`str`
        The name of the task.
    description : :class:`str`
        The description of the task.
    hide_from_ui : :class:`bool`
        If the task is hidden from the UI or not.
    fast_dismiss : :class:`bool`
        If the task is fast dismiss or not.
    last_update_pushed : :class:`str` | :class:`datetime.datetime`
        The last update pushed of the task; converted to a :class:`datetime` object.
    progress_percent : :class:`float`
        The progress percent of the task.
    speed : :class:`str` | None
        UNK - The task's throughput, if it reports one. Has only ever been observed as None.
    is_cancellable : :class:`bool`
        If the task is cancellable or not.
    origin : :class:`str`
        The origin of the task. (eg. "Core.CreateTestTask")
    dont_propagate : :class:`bool`
        If the task is withheld from being pushed up to the ADS or not.
    is_indeterminate : :class:`bool`
        If the task is indeterminate or not.
    state : :class:`int`
        The state of the task.
    state_message : :class:`str` | None
        The message tied to the current state, otherwise None.
    end_time : :class:`str` | :class:`datetime.datetime` | None
        The end time of the task; converted to a :class:`datetime` object. None while the task is still running.
    status : :class:`bool`
        The status of the task.
    reason : :class:`str` | None
        The reason for the task's status, otherwise None.
    support_url : :class:`str` | None
        A URL pointing to related support information, otherwise None.
    support_title : :class:`str` | None
        The title to display for the :attr:`support_url`, otherwise None.

    """

    is_primary_task: bool
    start_time: str | datetime.datetime
    id: str
    remote_instance_id: str | None
    parent_task_id: str | None
    name: str
    description: str
    hide_from_ui: bool
    fast_dismiss: bool
    last_update_pushed: str | datetime.datetime
    progress_percent: float
    speed: str | None
    is_cancellable: bool
    origin: str
    dont_propagate: bool
    is_indeterminate: bool
    state: int
    state_message: str | None
    end_time: str | datetime.datetime | None
    status: bool
    reason: str | None
    support_url: str | None
    support_title: str | None

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self), indent=1)
        return pformat(_field_values(self), indent=1)

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.last_update_pushed, str):
            self.last_update_pushed = timestamp_converter(timestamp=self.last_update_pushed)
        if isinstance(self.start_time, str):
            self.start_time = timestamp_converter(timestamp=self.start_time)
        # end_time stays None until the task finishes, so it can't be converted unconditionally.
        if isinstance(self.end_time, str):
            self.end_time = timestamp_converter(timestamp=self.end_time)


class ScheduleData:
    """Represents the JSON response data from :meth:`Core.get_schedule_data`.

    Attributes
    ----------
    available_methods : list[:class:`Methods`]
        The available methods.
    available_triggers : list[:class:`Triggers`]
        The available triggers.
    populated_triggers : list[:class:`Triggers`]
        The populated triggers.

    """

    available_methods: list[Methods]
    available_triggers: list[Triggers]
    populated_triggers: list[Triggers]

    __slots__ = ("available_methods", "available_triggers", "populated_triggers")

    def __init__(self, data: ScheduleDataResponse) -> None:
        """..."""
        for key in self.__slots__:
            value = data.get(key, None)
            if value is None:
                setattr(self, key, [])
                continue
            if key == "available_methods":
                self.available_methods = [Methods.from_response(entry) for entry in value]
                continue
            if key == "available_triggers" or key == "populated_triggers":
                setattr(self, key, [Triggers.from_response(entry) for entry in value])
                continue


@dataclass(slots=True)
class SecurityCheck(ResponseData):
    """Represents one check from the JSON response data of :meth:`Core.run_security_check`.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    title : :class:`str`
        The name of the check.
    description : :class:`str`
        What the check looks for.
    resolution : :class:`str`
        How to fix the check when it fails.
    severity : :class:`int`
        How serious a failed check is. Only ``1`` and ``2`` have been seen, and the meaning of each is unconfirmed.
    passed : :class:`bool`
        If the check passed or not. AMP sends this as `Pass`.
    hidden : :class:`bool`
        If the check is hidden in the AMP UI or not.

    """

    title: str
    description: str
    resolution: str
    severity: int
    passed: bool
    hidden: bool


@dataclass(slots=True)
class Session(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_active_amp_sessions`.

    Attributes
    ----------
    source : :class:`str`
        The source of the session.
    session_id : :class:`str`
        The ID of the session.
    username : :class:`str`
        The username the session belongs to.
    session_type : :class:`str`
        The type of the session.
    start_time : :class:`datetime`
        The start time of the session.
    last_activity : :class:`datetime`
        The last time the session was active.

    """

    source: str
    session_id: str
    username: str
    session_type: str
    start_time: str | datetime.datetime
    last_activity: str | datetime.datetime

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.start_time, str):
            self.start_time = timestamp_converter(timestamp=self.start_time)
        if isinstance(self.last_activity, str):
            self.last_activity = timestamp_converter(timestamp=self.last_activity)


@dataclass(slots=True)
class SettingSpec(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_config` or :meth:`Core.get_configs`.

    These represent a single setting field in the Instance configuration UI.

    Attributes
    ----------
    category : :class:`str`
        Which category the setting will appear under in the Instance configuration UI.
    actions : list[:class:`SettingSpecAction`]
        The list of actions related to the setting, defaults to an empty list.
    always_allow_read : :class:`bool`
        If the setting should always allow read or not.
    attributes : :class:`SettingsSpecAttribute`, optional
        The attributes that are set/prompted for when changing this setting.
    current_value : Union[:class:`list`, :class:`str`, :class:`bool`, :class:`int`, :class:`dict`, :class:`SettingSpecTableAliases`]
        The current value of the setting, default is "".
    description : :class:`str`, optional
        The text description below the setting name in the UI, default is "".
    enum_values : Union[dict[:class:`str`, :class:`str`], None], optional
        A dictionary representing the possible enum values for the setting, default is None.
    enum_values_are_deferred : :class:`bool`
        UNK, default is False.
    input_type : :class:`str`, optional
        The type of input to expect for the setting field, default is None.
    is_provision_spec : :class:`bool`
        if the setting is also a provision spec, default is False.
    keywords : :class:`str`
        UNK, default is "".
    max_length : :class:`int`
        UNK, all fields are 0 in data, default is 0.
    min_value : None
        UNK, all fields are null in data, default is None.
    meta : :class:`str`
        UNK, all fields are "", default is "".
    name : :class:`str`
        The name of the setting.
    node : :class:`str`
        The node required to have to edit this setting, default is "".
    order : :class:`int`
        The order in which this setting will appear in the UI, default is 1.
    placeholder : :class:`str`
        The placeholder text for the setting field, default is "".
    read_only : :class:`bool`
        If the setting is read only or not, default is False.
    read_only_provision : :class:`bool`
        UNK, all fields are False in data, default is False.
    required : :class:`bool`
        If the setting is required or not, default is False.
    requires_restart : :class:`bool`
        If the setting requires the Instance or Server to be restarted, default is False.
    selection_source : Union[:class:`SettingSpecSelectionSource`, None]
        UNK, most fields are null in data, default is None.
    subcategory : :class:`str`
        The subcategory the setting will appear under in the Instance configuration UI, default is "".
    suffix : :class:`str`
        The suffix applied to the string current_value, default is "".
    tag : :class:`str`
        What the setting is related to, similar to a Server Config property or file, default is "".
    val_type : :class:`str`
        What the type is of the current_value, default is "".
    warn_text : Union[:class:`str`, None], optional
        The warning the UI shows when the setting is changed, default is None.

        .. versionadded:: 5.0.0
    warn_when_value : Any, optional
        The value that triggers `warn_text`, default is None. Only seen as null so far.

        .. versionadded:: 5.0.0

    """

    category: str
    actions: list[str] | list[SettingSpecAction] = field(default_factory=list[str])
    always_allow_read: bool = field(default=False)
    attributes: Union[SettingsSpecAttribute, None] = field(default=None)
    # TODO: This will need a tighter type definition.
    current_value: Union[list[SettingSpecTableAliases], str, bool, int, dict[Any, Any], SettingSpecTableAliases] = ""
    description: str = ""
    enum_values: Union[dict[str, str], None] = field(default=None)
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
    warn_text: Union[str, None] = field(default=None)
    warn_when_value: Any = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105
        # determines the current value type and converts the data into the respective dataclass if needed.
        _table = SettingSpecTable().table
        if self.node in _table and isinstance(self.current_value, int):
            self.current_value = _table[self.node](self.current_value)

    __hash__ = None  # type: ignore[assignment]
    """Mutable dataclass; intentionally unhashable."""

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.name == other.name

    def __lt__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.name < other.name


@dataclass(slots=True)
class SettingSpecAction(ResponseData):
    """Represents the JSON response data from :attr:`SettingSpec.actions`.

    Attributes
    ----------
    argument : :class:`str`
        The argument of the action.
    caption : :class:`str`
        The caption of the action.
    is_client_side : :class:`bool`
        If the action is client side or not.
    method : :class:`str`
        The method of the action, these relate to API Endpoints when combined with the module.
    module : :class:`str`
        The module the action belongs to.
    type_id : :class:`str`
        The type ID of the action.

    """

    argument: str
    caption: str
    is_client_side: bool
    method: str
    module: str
    type_id: str


@dataclass(slots=True)
class SettingSpecSelectionSource(ResponseData):
    """Represents the JSON response data from :attr:`SettingSpec.selection_source`.

    Attributes
    ----------
    deferred : :class:`bool`
        If the selection source is deferred or not.
    must_validate : :class:`bool`
        If the selection source must validate or not.
    type_id : :class:`str`
        The type ID of the selection source.

    """

    deferred: bool
    must_validate: bool
    type_id: str


class SettingSpecTable:
    """Maps a setting node to the Enum :class:`SettingSpec.current_value` is converted into."""

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


@dataclass(slots=True)
class SettingsSpecAttribute(ResponseData):
    """Represents the JSON response data from :attr:`SettingSpec.attributes`.

    Attributes
    ----------
    key_name : :class:`str`
        The name of the key.
    key_placeholder : :class:`str`
        The placeholder text for the key.
    type_id : :class:`str`
        The type ID of the key.
    value_name : :class:`str`
        The name of the value.
    value_placeholder : :class:`str`
        The placeholder text for the value.
    read_only_keys : :class:`bool`
        If the key is read only or not.
    key_enum_values : Union[dict[:class:`str`, :class:`str`], None], optional
        The values the key can take, default is None.

        .. versionadded:: 5.0.0
    key_enum_source : :class:`str`, optional
        Where the key values come from (eg. "SettingNodes"), default is "".

        .. versionadded:: 5.0.0

    """

    key_name: str
    key_placeholder: str
    type_id: str
    value_name: str
    value_placeholder: str
    read_only_keys: bool = False
    key_enum_values: Union[dict[str, str], None] = field(default=None)
    key_enum_source: str = ""


@dataclass(slots=True)
class SettingsSpecParent(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_setting_spec`.

    Attributes
    ----------
    backups : list[:class:`SettingSpec`]
        The list of backup settings in the UI, default is an empty list.

        .. versionadded:: 5.0.0
    branding : list[:class:`SettingSpec`]
        The list of branding settings in the UI, default is an empty list.
    external_services : list[:class:`SettingSpec`]
        The list of external services settings in the UI, default is an empty list.
    file_manager : list[:class:`SettingSpec`]
        The list of file manager settings in the UI, default is an empty list.
    instance_deployment : list[:class:`SettingSpec`]
        The list of Instance deployment settings in the UI, default is an empty list.
    login : list[:class:`SettingSpec`]
        The list of login settings in the UI, default is an empty list.
    meta_config : list[:class:`SettingSpec`]
        The list of meta config settings in the UI, default is an empty list.

        .. versionadded:: 5.0.0
    minecraft : list[:class:`SettingSpec`]
        The list of Minecraft settings in the UI, default is an empty list.

        .. versionadded:: 5.0.0
    modules : dict[:class:`str`, list[:class:`SettingSpec`]]
        The settings of each module category, keyed by its name, which has a colon (eg. `valheim:stadiacontroller`),
        default is an empty dict.

        .. versionadded:: 5.0.0
    security_and_privacy : list[:class:`SettingSpec`]
        The list of security and privacy settings in the UI, default is an empty list.
    system_settings : list[:class:`SettingSpec`]
        The list of system settings in the UI, default is an empty list.
    updates : list[:class:`SettingSpec`]
        The list of update settings in the UI, default is an empty list.

    """

    # Every category arrives as a list of raw setting dicts, the same shape Core.get_config returns for a
    # single node. from_response() turns them into SettingSpec.
    # Spelled as a union of lists rather than list[SettingSpec | SettingSpecResponse], because list is invariant in its
    # element type and the raw response would not be assignable to the combined form.
    backups: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    branding: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    external_services: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    file_manager: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    instance_deployment: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    login: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    meta_config: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    minecraft: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    security_and_privacy: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    system_settings: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    updates: list[SettingSpec] | list[SettingSpecResponse] = field(default_factory=list[SettingSpec])
    modules: dict[str, list[SettingSpec]] | dict[str, list[SettingSpecResponse]] = field(default_factory=dict[str, list[SettingSpec]])

    @classmethod
    def from_response(cls, data: Mapping[str, Any]) -> Self:
        """Build this dataclass from the `Core.get_setting_spec` response, including the `modules` dict.

        The base builds every category, but doesn't look inside a dict, so the setting lists under `modules` are built here.

        Parameters
        ----------
        data : Mapping[:class:`str`, Any]
            The sanitised AMP response for it.

        Returns
        -------
        :class:`Self`
            The built dataclass, with `modules` built too.

        """
        # An explicit `super(SettingsSpecParent, cls)`, because `slots=True` builds a new class and a bare `super()`
        # in this classmethod raises a TypeError.
        parent = super(SettingsSpecParent, cls).from_response(data)
        parent.modules = {
            name: [SettingSpec.from_response(entry) if isinstance(entry, dict) else entry for entry in entries]
            for name, entries in parent.modules.items()
        }
        return parent


@dataclass(slots=True)
class Status(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_status` and :attr:`Updates.status`.

    Attributes
    ----------
    state : :class:`InstanceState`
        The state of the AMP Instance.
    uptime : :class:`str`
        The up time of the Instance, in Days, Hours, Minutes, Seconds format. 00:00:00:00
    metrics : :class:`Metrics` | :class:`MetricsResponse`
        The Metrics data related to the Instance.
    ports : list[:class:`Port`], optional
        The ports of the Instance, default is an empty list.

    """

    # AMP sends these raw; from_response() converts the nested ones and __post_init__ converts the state, so the first
    # annotation of each holds true.
    state: InstanceState | int
    uptime: str
    metrics: Metrics | MetricsResponse
    # Added in AMP 2.8; defaulted so older responses still construct.
    ports: list[Port] | list[PortResponse] = field(default_factory=list[Port])

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.state, int):
            self.state = InstanceState(self.state)


@dataclass(slots=True)
class StructuredDiagnostics(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_structured_diagnostics`.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    core : :class:`Diagnostics` | :class:`DiagnosticsResponse`
        The diagnostics every Instance has.
    application : dict[:class:`str`, Any]
        The diagnostics of the Instance's module. Empty for modules that send none, a Minecraft Instance sends
        `server_jar`, `server_type` and `java_version`, a Generic Instance sends `config_version`.

    """

    core: Diagnostics | DiagnosticsResponse
    application: dict[str, Any]


@dataclass(slots=True)
class TargetDatastore(ResponseData):
    """Represents a datastore in :attr:`RemoteTargetInfo.datastores`, which carries only an ID and a name.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    id : :class:`int`
        The datastore ID.
    friendly_name : :class:`str`
        The datastore name.

    """

    id: int
    friendly_name: str


@dataclass(slots=True)
class Template:
    """A placeholder class for all the parameters to deploy or create a template.

    * :meth:`ADSModule.deploy_template`


    Attributes
    ----------
    template_id : int
        The ID of the template to be deployed, as per the Template Management UI in AMP itself.
    new_username : Union[:class:`str`, None] , optional
        If specified, AMP will create a new user with this name for this Instance. Default is None.
        * Must be unique, If this user already exists, this will be ignored but the new Instance will be assigned to this user.
    new_password : Union[:class:`str`, None] , optional
        If :attr:`new_username` is specified and the user doesn't already exist, the password will be
        assigned to this user. Default is None.
    new_email : Union[:class:`str`, None] , optional
        If :attr:`new_username` is specified and the user doesn't already exist, the email address will
        be assigned to this user. Default is None.
    required_tags : Union[list[:class:`str`], None] , optional
        If specified, AMP will only deploy this template to targets that have every single 'tag'
        specified in their target configuration. You can adjust this via the controller by clicking
        'Edit' on the target settings. Default is None.
    tag : Union[:class:`str`, None] , optional
        Unrelated to required_tags. This is to uniquely identify this Instance to your own systems. It
        may be something like an order ID or service ID so you can find the associated Instance again
        at a later time. Default is None.
    friendly_name : Union[:class:`str`, None] , optional
        A friendly name for this Instance. If left blank, AMP will generate one for you. Defaults is None.
    secret : Union[:class:`str`, None] , optional
        Must be a non-empty strong in order to get a callback on deployment state change. This secret
        will be passed back to you in the callback so you can verify the request. Default is None.
    post_create : :class:`PostCreateState`, optional
        The action to take after the Instance is created, default is :attr:`PostCreateState.do_nothing`.
    extra_provision_settings : Union[dict[:class:`str`, :class:`str`], None]
        A dictionary of setting nodes and values to create the new Instance with. Identical in function
        to the provisioning arguments in the template itself. Default is None.

    """

    template_id: int
    new_username: Union[str, None] = field(default=None)
    new_password: Union[str, None] = field(default=None)
    new_email: Union[str, None] = field(default=None)
    required_tags: Union[list[str], None] = field(default=None)
    tag: Union[str, None] = field(default=None)
    friendly_name: Union[str, None] = field(default=None)
    secret: Union[str, None] = field(default=None)
    post_create: PostCreateState = field(default=PostCreateState.do_nothing)
    extra_provision_settings: Union[dict[str, str], None] = field(default=None)

    def __repr__(self) -> str:  # noqa: D105
        return self.__class__.__qualname__ + " " + " ".join([f"{f.name}={getattr(self, f.name)!r}" for f in fields(class_or_instance=self)])

    def to_dict(self) -> dict[str, Any]:
        """As the function name implies; converts the class to a dict for use as an API parameter.

        Returns
        -------
        dict[:class:`str`, Any]
            The class attributes as a key, value paired dict; attributes set to None are omitted.

        """
        return _dataclass_to_dict(self)


@dataclass(slots=True)
class TimedTrigger(ResponseData):
    """Represents the data of :meth:`Core.get_time_interval_trigger`.

    Attributes
    ----------
    description : :class:`str`
        The description of the trigger, this is shown in the UI.
    enabled_state : :class:`bool`
        If the Timed Trigger is enabled or not.
    id : :class:`str`
        The ID of the Timed Trigger, these are unique per Instance.
    match_days : list[:class:`int`]
        The days of the week to match, starting at 0 for Monday.
    match_days_of_month : list[:class:`int`]
        The days of the month to match.
    match_hours : list[:class:`int`]
        The hours of the day to match.
    match_minutes : list[:class:`int`]
        The minutes of the hour to match.
    match_months : list[:class:`int`]
        The months to match.
    name : :class:`str`
        The name of the Timed Trigger, this is shown in the UI.
    order : :class:`int`
        The order in which this trigger will appear in the Event list.
    tasks : :class:`list[TriggerTasks]`
        The list of tasks associated with this Timed Trigger.
    last_executed : Union[:class:`str`, None], optional
        When the Timed Trigger last fired, None if it never has, by default None.

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
    # AMP sends a dict of raw task dicts keyed by task ID; from_response() turns it into a list of TriggerTasks.
    # Spelled as a union of lists rather than list[TriggerTasks | TriggerTasksResponse]; list is invariant
    # in its element type, so the raw response would not be assignable to the combined form.
    tasks: list[TriggerTasks] | list[TriggerTasksResponse] = field(default_factory=list["TriggerTasks"])
    # Confirmed live on AMP 2.8.0.8.
    last_executed: Union[str, None] = field(default=None)

    @classmethod
    def from_response(cls, data: Mapping[str, Any]) -> Self:
        """Build this dataclass from the `Core.get_time_interval_trigger` response, with `tasks` as a list.

        AMP keys `tasks` by task ID. Each task carries its own `id`, so the keys are dropped and the tasks are built
        as a list of :class:`TriggerTasks`.

        Parameters
        ----------
        data : Mapping[:class:`str`, Any]
            The sanitised AMP response for it.

        Returns
        -------
        :class:`Self`
            The built dataclass, with `tasks` built too.

        """
        tasks: Any = data.get("tasks")
        if _is_json_object(tasks):
            data = {**data, "tasks": list(tasks.values())}
        # An explicit `super(TimedTrigger, cls)`, because `slots=True` builds a new class and a bare `super()`
        # in this classmethod raises a TypeError.
        return super(TimedTrigger, cls).from_response(data)


class TriggerID:
    """Used for a multitude of functions all related to Triggers and their IDs.

    Simply access the respective attribute and the unique GUID for that :class:`Instance` Trigger ID will be returned.
    """

    a_backup_finishes_archiving: str
    a_backup_finishes_restoring: str
    a_backup_has_failed: str
    a_backup_has_started: str
    a_player_achieves_an_advancement: str
    a_player_commits_suicide: str
    a_player_gets_an_achievement: str
    a_player_is_killed_by_an_npc: str
    a_player_is_killed_by_another_player: str
    a_player_joins_the_server: str
    a_player_joins_the_server_for_the_first_time: str
    a_player_joins_the_server_while_it_was_empty: str
    a_player_leaves_the_server: str
    a_player_performs_an_action: str
    a_player_sends_a_chat_message: str
    a_player_tries_to_join_the_server_while_its_sleeping: str
    a_player_who_has_previously_visited_rejoins_the_server: str
    a_scheduled_backup_finishes_archiving: str
    the_application_state_changes: str
    the_last_player_leaves_the_server: str
    the_minecraft_server_is_unable_to_keep_up: str
    the_minecraft_server_repeatedly_fails_to_start: str
    the_minecraft_server_stops_unexpectedly: str
    the_minecraft_server_watchdog_forced_a_shutdown_server_unresponsive: str
    the_server_enters_sleep_mode: str
    the_server_wakes_up_from_sleep_mode_due_to_player_connect: str

    # Core.get_triggers feeds this from ScheduleData.available_triggers. Only `description` and `id` are read.
    def __init__(self, data: list[TriggersResponse]) -> None:  # noqa: D107
        for entry in data:
            setattr(self, entry["description"], entry["id"])

    def __repr__(self) -> str:  # noqa: D105
        _temp: dict[str, str] = vars(self)
        _temp.pop("_init")
        return pformat(_temp)


@dataclass(slots=True)
class Triggers(ResponseData):
    """Represents the JSON reponse data for attributes :attr:`ScheduleData.available_triggers` and :attr:`ScheduleData.populated_triggers`.

    .. note::
        The :attr:`Triggers.id` is unique per Instance.


    Attributes
    ----------
    enabled_state : :class:`int`
        If the trigger is enabled or not.
    tasks : :class:`list[TriggerTasks]`, optional
        The list of tasks associated with this trigger, default is an empty list.
    id : :class:`str`
        The ID of the trigger, these are unique per Instance.
    type : :class:`str`
        The type of trigger, typically a TimeIntervalTrigger or EventTrigger.
    description : :class:`str`
        The description of the trigger.
    trigger_type : :class:`str`
        The same as :attr:`Triggers.type`.
    emits : :class:`list[str]`, optional
        The parameters the trigger emits to the Event allowing usage in the trigger, default is an empty list.
    last_execute_error : :class:`bool`, optional
        If the last execution of the trigger resulted in an error or not, default is False.
    last_error_reason : :class:`str`, optional
        The reason the last execution of the trigger resulted in an error, default is "".
    last_run : Union[:class:`str`, None], optional
        When the trigger last fired, default is None.

    """

    enabled_state: int
    tasks: list[TriggerTasks] | list[TriggerTasksResponse] = field(default_factory=list["TriggerTasks"])
    id: str = ""
    type: str = ""
    description: str = ""
    trigger_type: str = ""
    emits: list[str] = field(default_factory=list[str])
    last_execute_error: bool = field(default=False)
    last_error_reason: str = field(default="")
    # Confirmed against getscheduledata.json.
    last_run: Union[str, None] = field(default=None)

    __hash__ = None  # type: ignore[assignment]
    """Mutable dataclass; intentionally unhashable."""

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.description == other.description

    def __lt__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, self.__class__) and self.description < other.description


@dataclass(slots=True)
class TriggerTasks(ResponseData):
    """Represents the JSON response for the attribute :attr:`Triggers.tasks`.

    Hold's information regarding AMP Tasks and their status.

    Attributes
    ----------
    id : :class:`str`
        The ID of the task, these are unique per Instance.
    task_method_name : :class:`str`
        The name of the task method.
    parameter_mapping : :class:`ParameterMapping`
        The arguments the task passes to its method (eg. `seconds` for `Event.CommonCorePlugin.Wait`).
    enabled_state : :class:`int`
        If the task is enabled or not.
    locked : :class:`bool`
        If the task is locked or not.
    created_by : :class:`str`
        The user that created the task.
    order : :class:`int`
        The order in which this task will appear in the list of tasks.
    error_behaviour : :class:`int`, optional
        What the task does when it fails, default is 0.

        .. versionadded:: 5.0.0
    wait_for_complete : :class:`bool`, optional
        If the trigger waits for the task to complete before running the next, default is False.

        .. versionadded:: 5.0.0
    last_execute_error : :class:`bool`, optional
        If the last run of the task failed, default is False.

        .. versionadded:: 5.0.0
    last_error_reason : Union[:class:`str`, None], optional
        Why the last run of the task failed, default is None.

        .. versionadded:: 5.0.0

    """

    id: str
    task_method_name: str
    parameter_mapping: ParameterMapping | ParameterMappingResponse
    enabled_state: int
    locked: bool
    created_by: str
    order: int
    error_behaviour: int = 0
    wait_for_complete: bool = False
    last_execute_error: bool = False
    last_error_reason: Union[str, None] = field(default=None)


@dataclass(slots=True)
class TwoFactorSetupInfo(ResponseData):
    """Represents the setup data from :meth:`Core.enable_two_factor`, to finish with :meth:`Core.confirm_two_factor_setup`.

    .. warning::
        :attr:`manual_key` is the user's two-factor secret. Keep it out of logs and files.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    url : :class:`str`
        The authenticator link, usually shown as a QR code.
    manual_key : :class:`str`
        The two-factor secret, for typing into an authenticator by hand.

    """

    url: str
    manual_key: str

    def __repr__(self) -> str:  # noqa: D105
        # The secret is in both fields, and the repr is what ends up in logs.
        return "TwoFactorSetupInfo(url=<hidden>, manual_key=<hidden>)"


@dataclass(slots=True)
class UpdateInfo(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_update_info`.

    Attributes
    ----------
    update_available : :class:`bool`
        If an update is available or not.
    release_notes_url : :class:`str`
        The URL to the release notes for the update.
    build : :class:`str`
        The build of the update.
    version : :class:`str`
        The version of the update.
    tools_version : :class:`str`
        The tools version of the update, default is None.
    patch_only : :class:`bool`
        If the update is a patch only update or not, default is None

    """

    update_available: bool
    release_notes_url: str
    build: str
    version: str
    tools_version: Union[str, None] = None
    patch_only: Union[bool, None] = None


@dataclass(slots=True)
class Updates(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_updates`.

    Attributes
    ----------
    console_entries : :class:`list[ConsoleEntries]`
        The list of entries in the console.
    status : :class:`Status`
        The status of the Server.
    messages : :class:`list[Messages]`
        The list of messages the Instance or Server has.
    ports : :class:`list[Port]`, optional
        The list of ports the Server is listening/using, default is an empty list.
    tasks : :class:`list[RunningTask]` , optional
        The list of tasks the Server is running, default is an empty list.

    """

    # AMP sends all of these raw; from_response() converts them so the first annotation of each holds true.
    # Spelled as a union of lists rather than list[ConsoleEntries | ConsoleEntriesResponse]; list is invariant
    # in its element type, so the raw response would not be assignable to the combined form.
    console_entries: list[ConsoleEntries] | list[ConsoleEntriesResponse]
    status: Status | StatusResponse
    messages: list[Messages] | list[MessagesResponse]
    ports: list[Port] | list[PortResponse] = field(default_factory=list[Port])
    tasks: list[RunningTask] | list[RunningTaskResponse] = field(default_factory=list[RunningTask])

    def __repr__(self) -> str:  # noqa: D105
        # return pformat(vars(self))
        return pformat(_field_values(self))


@dataclass(slots=True)
class Uptime(ResponseData):
    """Represents the JSON response data from :attr:`MessageParameters.uptime`.

    .. versionadded:: 5.0.0

    Attributes
    ----------
    days : :class:`int`
        The days the Instance has been running.
    hours : :class:`int`
        The hours part of the uptime.
    minutes : :class:`int`
        The minutes part of the uptime.
    seconds : :class:`int`
        The seconds part of the uptime.

    """

    days: int
    hours: int
    minutes: int
    seconds: int


# The hand-written class before 5.0.0, when it became a dataclass built with `build`.
# class UserApplicationData:
#     """Represents the JSON response data from :meth:`Core.get_user_info`."""
#
#     id: str
#     user_session_id: str
#     session_id: str | None
#     name: str
#     join_time: datetime.datetime  # ISO format timestamp.
#     tags: str | None
#     uid: str
#     ip_address: str
#     port: int
#     time_logged_in: str  # 00:00:00.00000
#
#     __slots__ = (
#         "id",
#         "ip_address",
#         "join_time",
#         "name",
#         "port",
#         "session_id",
#         "tags",
#         "time_logged_in",
#         "uid",
#         "user_session_id",
#     )
#
#     def __init__(
#         self,
#         id: str,  # This is due to id overshadowing Python built-ins, the JSON response data comes in with an id key.
#         user_session_id: str,
#         name: str,
#         join_time: str,
#         uid: str,
#         ip_address: str,
#         port: int,
#         time_logged_in: str,
#         session_id: Union[str, None] = None,
#         tags: Union[str, None] = None,
#     ) -> None:
#         self.id = id
#         self.user_session_id = user_session_id
#         self.name = name
#         self.join_time = timestamp_converter(timestamp=join_time)
#         self.uid = uid
#         self.ip_address = ip_address
#         self.port = port
#         self.time_logged_in = time_logged_in
#         self.session_id = session_id
#         self.tags = tags
#
#         return


@dataclass(slots=True)
class UserApplicationData(ResponseData):
    """Represents the JSON response data from :meth:`Core.get_user_info`.

    .. note::
        This is an in-application user (eg. a connected Minecraft player), not an AMP User.

    .. versionchanged:: 5.0.0
        Built like the other response dataclasses, with `display_name` added (sent by AMP-2.8.0.8).

    Attributes
    ----------
    id : :class:`str`
        The ID of the player in the application.
    user_session_id : :class:`str`
        The ID of the player's current session.
    name : :class:`str`
        The player's name.
    join_time : :class:`datetime.datetime`
        When the player joined.
    uid : :class:`str`
        The player's UID, the same as the keys of :meth:`Core.get_user_list`.
    ip_address : :class:`str`
        The IP address the player connected from.
    port : :class:`int`
        The port the player connected from.
    time_logged_in : :class:`str`
        How long the player has been logged in, as AMP's `hh:mm:ss.fffffff` time span.
    session_id : Union[:class:`str`, None]
        UNK, None in every capture, by default None.
    tags : Union[:class:`str`, None]
        UNK, None in every capture, by default None.
    display_name : Union[:class:`str`, None]
        The player's display name, by default None.

    """

    id: str
    user_session_id: str
    name: str
    join_time: str | datetime.datetime
    uid: str
    ip_address: str
    port: int
    time_logged_in: str
    session_id: Union[str, None] = None
    tags: Union[str, None] = None
    display_name: Union[str, None] = None

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.join_time, str):
            self.join_time = timestamp_converter(timestamp=self.join_time)


@dataclass(slots=True)
class UserInfo(ResponseData):
    """Represents the JSON response data from the function :meth:`Core.get_all_amp_user_info` or :meth:`Core.get_amp_user_info`

    Attributes
    ----------
    cannot_change_password : :class:`bool`
        If the user cannot change their password or not.
    disable : :class:`bool`
        If the user is disabled or not.
    gravatar_hash : :class:`str`
        The gravatar hash of the user.
    id : :class:`str`
        The ID of the user.
    is_ldap_user : :class:`bool`
        If the user is an LDAP user or not.
    is_super_user : :class:`bool`
        If the user has the Super User role or not.
    is_two_factor_enabled : :class:`bool`
        If the user has 2FA enabled or not.
    must_change_password : :class:`bool`
        If the user must change their password or not when they log in next.
    name : :class:`str`
        The name of the user.
    password_expires : :class:`bool`
        If the user password expires or not when they log in next.
    permissions : :class:`list[str]`
        The list of permissions the user has.
    roles : :class:`list[str]`
        The list of AMP roles the user has.
    email_address : :class:`str`
        The email address of the user.
    last_login : :class:`datetime`
        The last login date of the user.
    oidc_sub : Union[:class:`str`, None], optional
        The OIDC subject of the user, default is None.

    """

    id: str
    name: str
    email_address: None
    disabled: bool
    permissions: None
    is_super_user: bool
    last_login: str | datetime.datetime
    password_expires: bool
    cannot_change_password: bool
    must_change_password: bool
    is_two_factor_enabled: bool
    roles: list[str]
    is_ldap_user: bool
    is_oidc_user: bool
    gravatar_hash: str
    avatar_base64: None
    oidc_sub: Union[str, None] = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105
        if isinstance(self.last_login, str):
            self.last_login = timestamp_converter(timestamp=self.last_login)
