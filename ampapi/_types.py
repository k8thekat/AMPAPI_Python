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

from typing import Any, NotRequired, Optional, Required, TypedDict, TypeGuard, Union

ResponseTypeAlias = Union[
    "ActionResultResponse",
    "AnalyticsSummaryResponse",
    "AppSummaryResponse",
    "ApplicationResponse",
    "AuditLogEntryResponse",
    "DiagnosticsInfoResponse",
    "ControllerResponse",
    "FileChunkResponse",
    "DeploymentTemplateResponse",
    "InstanceDatastoreResponse",
    "InstanceStatusResponse",
    # "EndpointResponseError",
    "LoginResponse",
    "LoginUserInfoResponse",
    "ModuleInfoResponse",
    "PortInfoResponse",
    "PortResponse",
    "ProvisionResponse",
    "ProvisionSettingInfoResponse",
    "RemoteTargetInfoResponse",
    "RoleResponse",
    "RunningTaskResponse",
    "ScheduleDataResponse",
    "SessionResponse",
    "StatusResponse",
    "UpdateInfoResponse",
    "UpdatesResponse",
    "UserInfoResponse",
    "ConfigResponse",
    # One list[Any] covers the list responses (AuditLogEntry, LoginUserInfo, Port, Role, Session and UserInfo).
    # pyright cannot narrow list[A] | list[B] by inspecting the elements, so each endpoint's own return
    # annotation carries the precise list type instead (eg. -> list[Session] | list[SessionResponse]).
    list[Any],
]

# Key sets used to discriminate a raw response dict into a specific TypedDict.
# A response matches when it has every key in *_REQUIRED_KEYS and none in *_EXCLUDED_KEYS.
# The excluded tuples exist because multiple response types share a "status" key; they will need to
# grow whenever a new TypedDict joining `ResponseTypeAlias` collides with an existing key set.
# Only "status" is Required[] on ActionResultResponse; "reason" is optional, so requiring it would
# reject valid responses. This matches the existing core.py narrowing.
ACTION_RESULT_REQUIRED_KEYS: tuple[str, ...] = ("status",)
# "console_entries" excludes UpdatesResponse, "is_primary_task" excludes RunningTaskResponse; both carry a "status".
ACTION_RESULT_EXCLUDED_KEYS: tuple[str, ...] = ("console_entries", "is_primary_task")

ANALYTICS_SUMMARY_REQUIRED_KEYS: tuple[str, ...] = ("stats", "graph_data")
ANALYTICS_SUMMARY_EXCLUDED_KEYS: tuple[str, ...] = ()

RUNNING_TASK_REQUIRED_KEYS: tuple[str, ...] = ("status", "is_primary_task")
RUNNING_TASK_EXCLUDED_KEYS: tuple[str, ...] = ()

# "state" alone no longer identifies StatusResponse; RunningTaskResponse carries one too, so "uptime"
# is required to separate them.
STATUS_REQUIRED_KEYS: tuple[str, ...] = ("state", "uptime")
STATUS_EXCLUDED_KEYS: tuple[str, ...] = ("is_primary_task",)

APPLICATION_REQUIRED_KEYS: tuple[str, ...] = ("module_name", "container_reason")
APPLICATION_EXCLUDED_KEYS: tuple[str, ...] = ()

INSTANCE_DATASTORE_REQUIRED_KEYS: tuple[str, ...] = ("id", "sanitised_name")
INSTANCE_DATASTORE_EXCLUDED_KEYS: tuple[str, ...] = ()

# InstanceResponse also carries "instance_id" + "running", so "instance_name" separates the two.
INSTANCE_STATUS_REQUIRED_KEYS: tuple[str, ...] = ("instance_id", "running")
INSTANCE_STATUS_EXCLUDED_KEYS: tuple[str, ...] = ("instance_name",)

PROVISION_SETTING_INFO_REQUIRED_KEYS: tuple[str, ...] = ("node", "custom_field_type")
PROVISION_SETTING_INFO_EXCLUDED_KEYS: tuple[str, ...] = ()

REMOTE_TARGET_INFO_REQUIRED_KEYS: tuple[str, ...] = ("ip_address_list", "datastores")
REMOTE_TARGET_INFO_EXCLUDED_KEYS: tuple[str, ...] = ()

ENDPOINTS_REQUIRED_KEYS: tuple[str, ...] = ("display_name", "endpoint", "uri")
ENDPOINTS_EXCLUDED_KEYS: tuple[str, ...] = ()

# "module_name" separates a full ApplicationResponse from the condensed summary.
APP_SUMMARY_REQUIRED_KEYS: tuple[str, ...] = ("id", "container_reason")
APP_SUMMARY_EXCLUDED_KEYS: tuple[str, ...] = ("module_name",)

CONTROLLER_REQUIRED_KEYS: tuple[str, ...] = ("available_instances", "is_remote")
CONTROLLER_EXCLUDED_KEYS: tuple[str, ...] = ()

DEPLOYMENT_TEMPLATE_REQUIRED_KEYS: tuple[str, ...] = ("template_base_app", "zip_overlay_path")
DEPLOYMENT_TEMPLATE_EXCLUDED_KEYS: tuple[str, ...] = ()

PROVISION_REQUIRED_KEYS: tuple[str, ...] = ("cpu_service_ratio", "remaining_instance_slots")
PROVISION_EXCLUDED_KEYS: tuple[str, ...] = ()

DIAGNOSTICS_REQUIRED_KEYS: tuple[str, ...] = ("application_name", "application_version")
DIAGNOSTICS_EXCLUDED_KEYS: tuple[str, ...] = ()

PORT_INFO_REQUIRED_KEYS: tuple[str, ...] = ("port_number", "provision_node_name")
PORT_INFO_EXCLUDED_KEYS: tuple[str, ...] = ()

# InstanceResponse shares "instance_id" with several types; "instance_name" + "module" pins it down.
INSTANCE_REQUIRED_KEYS: tuple[str, ...] = ("instance_id", "instance_name", "module")
INSTANCE_EXCLUDED_KEYS: tuple[str, ...] = ()

SCHEDULE_DATA_REQUIRED_KEYS: tuple[str, ...] = ("available_methods", "available_triggers")
SCHEDULE_DATA_EXCLUDED_KEYS: tuple[str, ...] = ()

# The eight UI categories are the whole response; branding + system_settings is enough to pin it down.
SETTINGS_SPEC_PARENT_REQUIRED_KEYS: tuple[str, ...] = ("branding", "system_settings")
SETTINGS_SPEC_PARENT_EXCLUDED_KEYS: tuple[str, ...] = ()

# The match_* keys are what separates a time interval trigger from the event triggers in TriggersResponse.
TIMED_TRIGGER_REQUIRED_KEYS: tuple[str, ...] = ("match_days", "match_minutes")
TIMED_TRIGGER_EXCLUDED_KEYS: tuple[str, ...] = ()

# user_session_id is the in-application user key; AMP Users (UserInfoResponse) never carry one.
USER_APPLICATION_DATA_REQUIRED_KEYS: tuple[str, ...] = ("user_session_id", "join_time")
USER_APPLICATION_DATA_EXCLUDED_KEYS: tuple[str, ...] = ()

# Confirmed against a live GetBackups response (AMP 2.8.0.8, a Minecraft Instance backup).
BACKUP_REQUIRED_KEYS: tuple[str, ...] = ("id", "stored_locally", "stored_remotely")
BACKUP_EXCLUDED_KEYS: tuple[str, ...] = ()

# Confirmed against a live ImportConfig reply (AMP 2.8.0.8, a missing file). Every list was empty.
IMPORT_CONFIG_REQUIRED_KEYS: tuple[str, ...] = ("imported", "not_imported", "unrecognised", "rejected")
IMPORT_CONFIG_EXCLUDED_KEYS: tuple[str, ...] = ()

# TODO: Confirm these keys against a live GetOPWhitelist response.
# The captured response is a "Missing Method" error, so they come from the `OPWhitelist` dataclass.
OP_WHITELIST_REQUIRED_KEYS: tuple[str, ...] = ("op_list", "whitelist")
OP_WHITELIST_EXCLUDED_KEYS: tuple[str, ...] = ()


def is_response_type[ResponseT](
    data: ResponseTypeAlias,
    response_type: type[ResponseT],  # noqa: ARG001
    required_keys: tuple[str, ...] = (),
    excluded_keys: tuple[str, ...] = (),
) -> TypeGuard[ResponseT]:
    """Check a response against a key set to narrow it to a specific TypedDict.

    .. note::
        The ``response_type`` parameter is only used to tell the type checker what the response
        narrows to; the keys are what actually get validated at runtime.


    Parameters
    ----------
    data : :class:`ResponseTypeAlias`
        The response data to validate.
    response_type : type[:class:`ResponseT`]
        The TypedDict the response narrows to when the key check passes. (eg. :class:`ActionResultResponse`)
    required_keys : tuple[:class:`str`, ...], optional
        Every key the response must contain, by default ().
    excluded_keys : tuple[:class:`str`, ...], optional
        Any key that disqualifies the response, by default ().

    Returns
    -------
    :class:`TypeGuard`
        True when `data` is a dict holding all of `required_keys` and none of `excluded_keys`.

    """
    if not isinstance(data, dict):
        return False
    return all(key in data for key in required_keys) and not any(key in data for key in excluded_keys)


def is_response_list[ResponseT](
    data: ResponseTypeAlias,
    response_type: type[ResponseT],
    required_keys: tuple[str, ...] = (),
    excluded_keys: tuple[str, ...] = (),
) -> TypeGuard[list[ResponseT]]:
    """Check every entry of a list response against a key set to narrow it to a list of a specific TypedDict.

    .. note::
        An empty list narrows successfully; there is nothing to contradict the key set.


    Parameters
    ----------
    data : :class:`ResponseTypeAlias`
        The response data to validate.
    response_type : type[:class:`ResponseT`]
        The TypedDict each entry narrows to when the key check passes. (eg. :class:`ApplicationResponse`)
    required_keys : tuple[:class:`str`, ...], optional
        Every key each entry must contain, by default ().
    excluded_keys : tuple[:class:`str`, ...], optional
        Any key that disqualifies an entry, by default ().

    Returns
    -------
    :class:`TypeGuard`
        True when ``data`` is a list and every entry satisfies the key set.

    """
    if not isinstance(data, list):
        return False
    return all(is_response_type(entry, response_type, required_keys, excluded_keys) for entry in data)


class ActionResultResponse(TypedDict, total=False):
    status: Required[bool]
    reason: str
    result: str
    # Added in AMP 2.8.
    support_url: Union[str, None]
    support_title: Union[str, None]


class ActionSpec(TypedDict):
    """ads_module : dict[:class:`str`, Any]

    file_manager_plugin : dict[:class:`str`, Any]

    email_sender_plugin : dict[:class:`str`, Any]

    common_core_plugin : dict[:class:`str`, Any]

    core : dict[:class:`str`, Any]

    """

    ads_module: dict[str, Any]
    file_manager_plugin: dict[str, Any]
    email_sender_plugin: dict[str, Any]
    common_core_plugin: dict[str, Any]
    core: dict[str, Any]


class APISpec(TypedDict):
    """analytics_plugin : dict[:class:`str`, :class:`APISpecEndpointData`]

    common_core_plugin : dict[:class:`str`, :class:`APISpecEndpointData`]

    email_sender_plugin : dict[:class:`str`, :class:`APISpecEndpointData`]

    file_manager_plugin : dict[:class:`str`, :class:`APISpecEndpointData`]

    local_file_backup_plugin : dict[:class:`str`, :class:`APISpecEndpointData`]

    minecraft_module : dict[:class:`str`, :class:`APISpecEndpointData`]

    """

    analytics_plugin: dict[str, APISpecEndpointData]
    common_core_plugin: dict[str, APISpecEndpointData]
    email_sender_plugin: dict[str, APISpecEndpointData]
    file_manager_plugin: dict[str, APISpecEndpointData]
    local_file_backup_plugin: dict[str, APISpecEndpointData]
    minecraft_module: dict[str, APISpecEndpointData]


class APISpecEndpointData(TypedDict):
    """description : :class:`str`

    is_complex_type : :class:`bool`

    parameters : :class:`APISpecEndpointParameters`

    return_type_name : :class:`str`

    returns : :class:`str`

    """

    id: str
    description: str
    is_complex_type: bool
    parameters: APISpecEndpointParameters
    return_type_name: str
    returns: str


class APISpecEndpointParameters(TypedDict):
    """description : :class:`str`

    name : :class:`str`

    option : :class:`bool`

    param_enum_values : :class:`str`

    type_name : :class:`str`

    """

    id: str
    description: str
    name: str
    option: bool
    param_enum_values: str
    type_name: str


class ApplicationResponse(TypedDict):
    """Represents the JSON response data for a single entry from :meth:`ADSModule.get_supported_applications`."""

    id: str
    friendly_name: str
    description: Union[str, None]
    module_name: str
    settings: dict[str, Any]
    supported_platforms: int
    container_support: int
    container_reason: Union[str, None]
    extra_setup_steps_uri: Union[str, None]
    display_image_source: str
    author: Union[str, None]
    no_commercial_usage: bool
    deprecated_reason: Union[str, None]
    is_service_spec: bool
    is_multi_ip_aware: bool
    # Added in 2.8.0.4; absent on 2.6.5.0.
    resource_usage_info: NotRequired[Union[str, None]]


class AnalyticsGraphDataResponse(TypedDict):
    date: str
    end_date: str
    count: int


class AnalyticsStatResponse(TypedDict):
    raw_name: str
    name: str
    display_value: Union[int, float, str]
    current: Union[int, float]
    previous: Union[int, float]
    difference: float
    description: str


class AnalyticsSummaryResponse(TypedDict):
    stats: list[AnalyticsStatResponse]
    graph_data: list[AnalyticsGraphDataResponse]
    country_data: list[Any]
    top_players: list[Any]
    quietest_time: AnalyticsGraphDataResponse
    busiest_time: AnalyticsGraphDataResponse
    is_demo: bool


class AppSummaryResponse(TypedDict):
    """Represents a single entry from :meth:`ADSModule.get_supported_app_summaries`.

    .. note::
        A condensed :class:`ApplicationResponse`; it drops ``module_name``, ``settings`` and
        ``is_multi_ip_aware``.

    """

    id: str
    friendly_name: str
    description: Union[str, None]
    supported_platforms: int
    container_support: int
    container_reason: Union[str, None]
    extra_setup_steps_uri: Union[str, None]
    resource_usage_info: Union[str, None]
    display_image_source: str
    author: Union[str, None]
    no_commercial_usage: bool
    deprecated_reason: Union[str, None]
    is_service_spec: bool


class AuditLogEntryResponse(TypedDict):
    id: int
    event_type: int
    source: str
    user: str
    category: str
    message: str
    timestamp: str
    acknowledged: bool


class AvailableMethodsResponse(TypedDict):
    id: str
    name: str
    description: str
    category: str
    display_format: str | None
    consumes: list[ConsumeResponse]


class AvailableTriggersResponse(TypedDict):
    id: str
    type: str
    description: str
    emits: list[str]
    tasks: list[Any]
    trigger_type: str
    enabled_state: int
    last_run: None


class BackupResponse(TypedDict):
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
    timestamp: str
    compressed_size_bytes: NotRequired[Union[int, None]]
    hash_sha1: NotRequired[Union[str, None]]
    meta: NotRequired[Any]
    parent_manifest: NotRequired[Union[str, None]]
    remote_store_id: NotRequired[Union[str, None]]


class BukkitCategories(TypedDict):
    """id : :class:`int`

    name : :class:`str`

    """

    id: int
    name: str


class ControllerResponse(TypedDict):
    """Represents a single target from :meth:`ADSModule.get_instances`.

    .. note::
        This is a *target*, not an Instance; the Instances live in :attr:`available_instances`.
        A Controller returns one of these per attached target, local and remote.

    """

    available_instances: list[InstanceResponse]
    available_ips: list[str]
    can_create: bool
    creates_in_containers: bool
    datastores: list[TargetDatastoreResponse]
    description: str
    disabled: bool
    # Null on every target observed so far, so its shape is unconfirmed; see the Fitness dataclass.
    fitness: Union[dict[str, Any], None]
    friendly_name: str
    id: int
    instance_id: str
    is_remote: bool
    last_updated: str
    platform: PlatformInfoResponse
    state: int
    state_reason: Union[str, None]
    tags: list[str]
    tags_list: Union[str, None]
    url: str

    # Ver: 2.8.0.4; absent on 2.6.5.0.
    last_poll_update: NotRequired[str]
    last_push_update: NotRequired[str]
    push_update_throttle_interval: NotRequired[str]
    poll_update_throttle_interval: NotRequired[str]
    can_push_update: NotRequired[bool]
    can_poll_update: NotRequired[bool]


class CPUInfoResponse(TypedDict):
    """Represents the ``cpu_info`` block nested inside :class:`PlatformInfoResponse`."""

    sockets: int
    cores: int
    threads: int
    vendor: str
    model_name: str
    total_cores: int
    total_threads: int


class ConfigResponse(TypedDict):
    """Current response structure from :meth:`get_config()`."""

    read_only: bool
    name: str
    description: str
    category: str
    subcategory: str
    current_value: int
    val_type: str
    enum_values: None
    enum_values_are_deferred: bool
    selection_source: None
    node: str
    input_type: str
    is_provision_spec: bool
    read_only_provision: bool
    actions: list[Any]
    keywords: str
    always_allow_read: bool
    tag: str
    min_value: None
    max_value: None
    max_length: int
    placeholder: str
    suffix: str
    meta: str
    requires_restart: bool
    required: bool
    attributes: None
    order: int


class ConsoleEntriesResponse(TypedDict):
    """Represents the JSON response data for each entry of :attr:`UpdatesResponse.console_entries`."""

    timestamp: str
    source: str
    # Confirmed against getupdates.json; only ever seen as None.
    source_id: Union[str, None]
    type: str
    contents: str


class ConsumeResponse(TypedDict):
    name: str
    display_name: None
    description: str
    placeholder: str
    suffix: str
    value_type: str
    enum_values: dict[str, str] | None
    selection_source: None
    input_type: str


# Confirmed live on AMP 2.8.0.8: AMP spells the mapping key `setting_mappings`, and sends null for
# `description`, `module`, `template_instance`, `template_role` and `template_base_app` on a bare template.
class DeploymentTemplateResponse(TypedDict):
    """Represents a single entry from :meth:`ADSModule.get_deployment_templates`."""

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
    start_on_boot: bool


class DirectoryResponse(TypedDict):
    is_directory: bool
    is_virtual_directory: bool
    filename: str
    size_bytes: int
    created: str
    modified: str
    is_downloadable: bool
    is_editable: bool
    is_archive: bool
    is_excluded_from_backups: bool
    is_smart_excluded_from_backups: NotRequired[bool]


class DiagnosticsInfoResponse(TypedDict):
    os: str
    platform: str
    system_type: str
    hardware_platform: Any
    cpu_model: str
    cpu_layout: str
    installed_ram: str
    virtualization: str
    network_mode: Any
    module: str
    module_application: str
    loaded_plugins: str
    application_name: str
    application_version: str
    codename: str
    tools_version: str
    release_stream: str
    build_spec: str
    build_date: str
    instance_id: str
    last_executable: str
    last_arguments: str
    last_process_id: str
    server_type: NotRequired[str]
    server_jar: NotRequired[str]
    java_version: NotRequired[str]
    config_version: NotRequired[str]


class EndpointsResponse(TypedDict):
    """Represents a single entry from :meth:`ADSModule.get_application_endpoints`."""

    display_name: str
    endpoint: str
    uri: str


class FileChunkResponse(TypedDict):
    base64_data: str
    bytes_length: int


class EndpointResponseError(TypedDict, total=False):
    title: Required[str]
    status: bool
    message: str
    stackTrace: Required[Any]


class ImportConfigResponse(TypedDict):
    """The raw response from :meth:`GenericModule.import_config`."""

    # TODO: Confirm the element types against a real import.
    # Only empty lists were seen, so they are typed as Any for now.
    settings: dict[str, Any]
    imported: list[Any]
    not_imported: list[Any]
    unrecognised: list[Any]
    rejected: list[Any]


class InstanceResponse(TypedDict):
    """Represents a single AMP Instance.

    .. note::
        These arrive nested under ``available_instances`` on each target returned by
        :meth:`ADSModule.get_instances`, and directly from :meth:`ADSModule.get_instance`.

    """

    application_endpoints: list[EndpointsResponse]
    app_state: int
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
    amp_version: Union[str, dict[str, int], None]
    container_cpus: float
    tags: Union[list[str], None]
    module_display_name: Union[str, None]
    # Keyed by metric name: cpu_usage, memory_usage, active_users (+ tps) on AMP 2.8.0.8; empty while stopped.
    metrics: Union[dict[str, MetricsKeyResponse], None]
    display_image_source: Union[str, None]
    description: Union[str, None]
    # Confirmed against getinstances.json on 2.6.5.0; these were absent from the original definition.
    application_ip: Union[str, None]
    container_swap_mb: int
    custom_mount_binds: dict[str, str]
    extra_container_packages: list[str]
    group: Union[str, None]
    is_multi_ip_aware: bool
    order: int
    specific_docker_image: Union[str, None]
    use_host_mode_network: bool
    welcome_message: Union[str, None]


class InstanceDatastoreResponse(TypedDict):
    """Represents the JSON response data from :meth:`ADSModule.get_datastore`, or a single entry from :meth:`ADSModule.get_datastores`."""

    id: int
    friendly_name: str
    description: str
    directory: str
    soft_limit_mb: int
    current_usage_mb: int
    instance_limit: int
    priority: int
    active: bool
    tags: list[str]
    is_internal: bool
    # Note the British spelling; this is what AMP sends on the wire.
    sanitised_name: str


class InstanceStatusResponse(TypedDict):
    """Represents a single entry from :meth:`ADSModule.get_instance_statuses`."""

    instance_id: str
    running: bool


class KeyDrift(TypedDict):
    """How captured payloads differ from the TypedDict that declares them, from :func:`key_drift.key_drift`."""

    missing: dict[str, int]
    "Each required key some payloads lacked, with how many lacked it. A nested key is dotted (`metrics.tps`)."
    unexpected: dict[str, int]
    "Each key the shape does not declare, with how many payloads carried it."


class LoginResponse(TypedDict):
    # A failed login sends None for these four (confirmed against AMP 2.8.0.8).
    permissions: Union[list[str], None]
    remember_me_token: Union[str, None]
    result: int
    result_reason: str
    session_id: Union[str, None]
    success: bool
    # Confirmed against login.json; this carries a username, so it is the LoginUserInfo shape and not
    # the AMP User shape UserInfoResponse.
    user_info: Union[LoginUserInfoResponse, None]


# Not total=False, so pyright can narrow the response union to this shape by its keys.
class LoginUserInfoResponse(TypedDict):
    id: str
    username: str
    email_address: str | None
    is_two_factor_enabled: bool
    disabled: bool
    last_login: str
    gravatar_hash: str
    is_ldap_user: bool
    is_oidc_user: bool
    avatar_base64: str | None


class MCUserData(TypedDict):
    """name : :class:`str`

    uuid : :class:`str`
    """

    name: str
    uuid: str


class MessagesResponse(TypedDict):
    """Represents the JSON response data for each entry of :attr:`UpdatesResponse.messages`."""

    # Depends on the message; a "metrics" message carries instance_id, metrics, state and uptime.
    parameters: Union[dict[str, Any], None]
    id: str
    expired: bool
    source: str
    message: str
    age_minutes: int


class MethodsData(TypedDict):
    """id : :class:`str`

    name : :class:`str`

    description : :class:`str`

    consumes : list[:class:`Consumes`]

    """

    id: str
    name: str
    description: str
    consumes: list[ConsumeResponse]


class MetricsResponse(TypedDict):
    """Represents the data inside the JSON key `metrics` for :meth:`get_status()`."""

    cpu_usage: MetricsKeyResponse
    memory_usage: MetricsKeyResponse
    active_users: MetricsKeyResponse
    # Confirmed against AMP 2.8.0.8: the ADS sends the two usage keys, some Minecraft Instances send tps.
    physical_ram_usage: NotRequired[MetricsKeyResponse]
    swap_usage: NotRequired[MetricsKeyResponse]
    tps: NotRequired[MetricsKeyResponse]


class MetricsKeyResponse(TypedDict):
    """Represents the JSON response data for each of the attributes of :class:`Metrics`."""

    raw_value: int
    max_value: int
    percent: int
    units: str
    color: Optional[str]
    color2: Optional[str]
    color3: Optional[str]
    # Confirmed against getstatus.json; AMP sends a short label for the metric tile (eg "CPU", "RAM").
    short_name: NotRequired[str]


class ModuleInfoResponse(TypedDict):
    name: str
    author: str
    app_name: str
    supports_sleep: bool
    loaded_plugins: list[str]
    amp_version: str
    amp_build: str
    tools_version: str
    api_version: str
    version_codename: str
    timestamp: str
    build_spec: str
    branding: dict[str, Any]
    analytics: bool
    analytics_tag: str
    feature_set: list[Any]
    instance_id: str
    instance_name: str
    friendly_name: str
    endpoint_uri: str
    primary_endpoint: str
    module_name: str
    is_remote_instance: bool
    display_base_uri: str
    requires_full_load: bool
    allow_remember_me: bool
    base_port: int
    is_oidc_enabled: bool
    oidc_provider_friendly_name: str


class OPWhitelistResponse(TypedDict):
    """The raw response from :meth:`MinecraftModule.mc_get_op_whitelist`."""

    op_list: list[MCUserData]
    whitelist: list[MCUserData]


class ParameterMapping(TypedDict, total=False):
    """user : NotRequired[:class:`str`]

    reason : NotRequired[:class:`str`]

    """

    user: NotRequired[str]
    reason: NotRequired[str]


class PermissionNode(TypedDict):
    """Permission node response structure.

    Keys
    ----
    name : :class:`str`

    node : :class:`str`

    display_name : :class:`str`

    description : :class:`str`

    children : Union[list[:class:`PermissionNode`], None]

    """

    name: Required[str]
    node: Required[str]
    display_name: Required[str]
    description: Optional[str]
    children: Required[Union[list[PermissionNode], None]]


class PlatformInfoResponse(TypedDict):
    """Represents the platform block nested inside a target.

    .. note::
        Two endpoints send different subsets of this. :meth:`ADSModule.get_target_info` sends only the
        required keys below, while the ``platform`` block on each :meth:`ADSModule.get_instances` target
        also carries the ``NotRequired`` ones.

    """

    cpu_info: CPUInfoResponse
    installed_ram_mb: int
    os: int
    platform_name: str
    system_type: int
    virtualization: int
    docker_network_is_host_mode: bool
    has_memory_limit: bool
    admin_rights: NotRequired[int]
    hardware_platform_name: NotRequired[str]
    installed_glibc_version: NotRequired[str]
    is_shared_setup: NotRequired[bool]
    max_swap_mb: NotRequired[int]


class PortInfoResponse(TypedDict):
    """Represents a single entry from :meth:`ADSModule.get_instance_network_info`.

    .. note::
        ``protocol`` arrives as an int; see :class:`Protocols` for the mapping.

    """

    port_number: int
    protocol: int
    provision_node_name: str
    verified: bool
    description: str
    range: int
    is_user_defined: bool
    is_firewall_target: bool
    # Added in 2.8.0.4; absent on 2.6.5.0.
    is_child: NotRequired[bool]
    min_listening: NotRequired[int]
    offset: NotRequired[int]
    parent_node: NotRequired[Union[str, None]]
    parent_ref: NotRequired[Union[str, None]]


class PortResponse(TypedDict):
    listening: bool
    protocol: int
    port: int
    name: str
    is_delayed_open: bool
    required: bool
    # Added in AMP 2.8.
    listening_count: NotRequired[int]
    range: NotRequired[int]
    min_listening: NotRequired[int]


class ProvisionSettingInfoResponse(TypedDict):
    """Represents a single entry from :meth:`ADSModule.get_provision_arguments`."""

    node: str
    type: str
    description: str
    default_value: Union[str, int, None]
    value_range: Union[int, str]
    custom_field_type: Union[str, None]
    related_setting: Union[str, None]
    endpoint_name: str
    endpoint_format: Union[str, None]
    # Added in 2.8.0.4; absent on 2.6.5.0.
    hidden: NotRequired[bool]
    min_listening: NotRequired[int]


# TODO: Verify these keys against a live response.
# Derived from the `Provision` dataclass and docs; the endpoint returns a null body on the ADS and Controller.
class ProvisionResponse(TypedDict):
    """Represents the JSON response data from :meth:`ADSModule.get_provision_fitness`.

    .. note::
        The related :class:`Fitness` dataclass carries two extra fields, ``score_description`` and
        ``score_zero_factors``; those belong to a target's ``fitness`` block, not to this endpoint.

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


class RemoteTargetInfoResponse(TypedDict):
    """Represents the JSON response data from :meth:`ADSModule.get_target_info`."""

    ip_address_list: list[str]
    platform_info: PlatformInfoResponse
    # The target payload carries a reduced datastore shape, not a full InstanceDatastoreResponse.
    datastores: list[TargetDatastoreResponse]
    deploys_in_containers: bool


class RoleResponse(TypedDict):
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


class RunningTaskResponse(TypedDict):
    """Represents the JSON response data for any endpoint that returns a RunningTask, eg. :meth:`Core.get_tasks`."""

    is_primary_task: bool
    start_time: str
    id: str
    remote_instance_id: Union[str, None]
    parent_task_id: Union[str, None]
    name: str
    description: str
    hide_from_ui: bool
    fast_dismiss: bool
    last_update_pushed: str
    progress_percent: float
    speed: Union[str, None]
    is_cancellable: bool
    origin: str
    dont_propagate: bool
    is_indeterminate: bool
    state: int
    state_message: Union[str, None]
    end_time: Union[str, None]
    status: bool
    reason: Union[str, None]
    support_url: Union[str, None]
    support_title: Union[str, None]


class ScheduleDataResponse(TypedDict):
    available_methods: list[AvailableMethodsResponse]
    available_triggers: list[AvailableTriggersResponse]
    populated_triggers: list[AvailableTriggersResponse]


class SessionResponse(TypedDict):
    source: str
    session_id: str
    last_activity: str
    start_time: str
    username: str
    session_type: str


class SettingsSpecParentResponse(TypedDict):
    """The raw response from :meth:`Core.get_setting_spec`; one key per settings category in the UI.

    Every value is a list of the same shape :meth:`Core.get_config` returns for a single node.
    """

    branding: list[ConfigResponse]
    external_services: list[ConfigResponse]
    file_manager: list[ConfigResponse]
    instance_deployment: list[ConfigResponse]
    login: list[ConfigResponse]
    security_and_privacy: list[ConfigResponse]
    system_settings: list[ConfigResponse]
    updates: list[ConfigResponse]


# Not total=False, so pyright can narrow the response union to this shape by its keys.
class StatusResponse(TypedDict):
    state: int
    uptime: str
    metrics: MetricsResponse
    # Added in AMP 2.8.
    ports: NotRequired[list[PortResponse]]


class TargetDatastoreResponse(TypedDict):
    """The reduced datastore shape carried in :class:`RemoteTargetInfoResponse`; only an ID and a name."""

    id: int
    friendly_name: str


class TimedTriggerResponse(TypedDict):
    """The raw response from :meth:`Core.get_time_interval_trigger`.

    .. note::
        This is *not* :class:`TriggersResponse`; a time interval trigger fires off the ``match_*``
        schedule fields instead of an event, and carries no ``emits`` / ``type`` keys.

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
    tasks: list[TriggersTasksResponse]
    # Confirmed live on AMP 2.8.0.8; an ISO timestamp once the trigger has fired, null before.
    last_executed: NotRequired[Union[str, None]]


class TriggersResponse(TypedDict):
    """id : :class:`str`

    description : :class:`str`

    emits : list[:class:`str`]

    enabled_state : :class:`int`

    tasks : list[:class:`TriggerTasksData`]

    type : :class:`str`

    trigger_type : :class:`str`

    last_execute_error : NotRequired[:class:`bool`]

    last_error_reason : NotRequired[:class:`str`]

    last_run : NotRequired[Union[:class:`str`, None]]

    """

    id: str
    description: str
    emits: list[str]
    enabled_state: int
    tasks: list[TriggersTasksResponse]
    type: str
    trigger_type: str
    last_execute_error: NotRequired[bool]
    last_error_reason: NotRequired[str]
    last_run: NotRequired[Union[str, None]]


class TriggersTasksResponse(TypedDict):
    """id : :class:`str`

    task_method_name : :class:`str`

    parameter_mapping : :class:`ParameterMapping`

    enabled_state : :class:`int`

    locked : :class:`bool`

    created_by : :class:`str`

    order : :class:`int`
    """

    id: str
    task_method_name: str
    parameter_mapping: ParameterMapping
    enabled_state: int
    locked: bool
    created_by: str
    order: int


# Not total=False, so pyright can narrow the response union to this shape by its keys.
class UpdateInfoResponse(TypedDict):
    update_available: bool
    version: str
    build: str
    release_notes_url: str
    tools_version: str
    patch_only: bool


# Not total=False, so pyright can narrow the response union to this shape by its keys.
class UpdatesResponse(TypedDict):
    status: StatusResponse
    console_entries: list[ConsoleEntriesResponse]
    messages: list[MessagesResponse]
    tasks: list[RunningTaskResponse]
    ports: list[PortResponse]


class UserApplicationDataResponse(TypedDict):
    """The raw response from :meth:`Core.get_user_info`.

    .. note::
        This is an in-application user (eg a connected Minecraft player), *not* an AMP User.
        See :class:`UserInfoResponse` for the latter.

    """

    id: str
    user_session_id: str
    name: str
    join_time: str
    uid: str
    ip_address: str
    port: int
    time_logged_in: str
    session_id: NotRequired[Union[str, None]]
    tags: NotRequired[Union[str, None]]


class UserInfoResponse(TypedDict):
    id: str
    name: str
    email_address: None
    disabled: bool
    permissions: None
    is_super_user: bool
    last_login: str
    password_expires: bool
    cannot_change_password: bool
    must_change_password: bool
    is_two_factor_enabled: bool
    roles: list[str]
    is_ldap_user: bool
    is_oidc_user: bool
    gravatar_hash: str
    avatar_base64: None
