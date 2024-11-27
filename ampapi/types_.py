from __future__ import annotations

from typing import Any, TypedDict

from typing_extensions import NotRequired


class ActionSpec(TypedDict):
    """
    ads_module: dict[:class:`str`, Any]

    file_manager_plugin: dict[:class:`str`, Any]

    email_sender_plugin: dict[:class:`str`, Any]

    common_core_plugin: dict[:class:`str`, Any]

    core: dict[:class:`str`, Any]

    """

    ads_module: dict[str, Any]
    file_manager_plugin: dict[str, Any]
    email_sender_plugin: dict[str, Any]
    common_core_plugin: dict[str, Any]
    core: dict[str, Any]


class APISpec(TypedDict):
    """
    analytics_plugin: dict[:class:`str`, :class:`APISPecEndpointData`]

    common_core_plugin: dict[:class:`str`, :class:`APISPecEndpointData`]

    email_sender_plugin: dict[:class:`str`, :class:`APISPecEndpointData`]

    file_manager_plugin: dict[:class:`str`, :class:`APISPecEndpointData`]

    local_file_backup_plugin: dict[:class:`str`, :class:`APISPecEndpointData`]

    minecraft_module: dict[:class:`str`, :class:`APISPecEndpointData`]

    """

    analytics_plugin: dict[str, APISPecEndpointData]
    common_core_plugin: dict[str, APISPecEndpointData]
    email_sender_plugin: dict[str, APISPecEndpointData]
    file_manager_plugin: dict[str, APISPecEndpointData]
    local_file_backup_plugin: dict[str, APISPecEndpointData]
    minecraft_module: dict[str, APISPecEndpointData]


class APISPecEndpointData(TypedDict):
    """
    description: :class:`str`

    is_complex_type: :class:`bool`

    parameters: :class:`APISpecEndpointParameters`

    return_type_name: :class:`str`

    returns: :class:`str`

    """

    id: str
    description: str
    is_complex_type: bool
    parameters: APISpecEndpointParameters
    return_type_name: str
    returns: str


class APISpecEndpointParameters(TypedDict):
    """
    description: :class:`str`

    name: :class:`str`

    option: :class:`bool`

    param_enum_values: :class:`str`

    type_name: :class:`str`

    """

    id: str
    description: str
    name: str
    option: bool
    param_enum_values: str
    type_name: str


class BukkitCategories(TypedDict):
    """
    id: :class:`int`

    name: :class:`str`

    """

    id: int
    name: str


class Consumes(TypedDict, total=False):
    """
    description: :class:`str`

    input_type: :class:`str`

    name: :class:`str`

    value_type: :class:`str`

    enum_values: NotRequired[:class:`str`]

    """

    description: str
    input_type: str
    name: str
    value_type: str
    enum_values: NotRequired[str]


class MethodsData(TypedDict):
    """
    id: :class:`str`

    name: :class:`str`

    description: :class:`str`

    consumes: list[:class:`Consumes`]

    """

    id: str
    name: str
    description: str
    consumes: list[Consumes]


class ParameterMapping(TypedDict, total=False):
    """
    user: NotRequired[:class:`str`]

    reason: NotRequired[:class:`str`]

    """

    user: NotRequired[str]
    reason: NotRequired[str]


class PermissionNode(TypedDict):
    """
    name: :class:`str`

    node: :class:`str`

    display_name: :class:`str`

    description: :class:`str`

    children: list[:class:`PermissionNode`]

    """

    id: str
    name: str
    node: str
    display_name: str
    description: str | None
    children: list[PermissionNode]


class ScheduleDataData(TypedDict):
    """
    available_methods: list[:class:`MethodsData`]

    available_triggers: list[:class:`TriggersData`]

    populated_triggers: list[:class:`TriggersData`]

    """

    available_methods: list[MethodsData]
    available_triggers: list[TriggersData]
    populated_triggers: list[TriggersData]


class TriggersData(TypedDict):
    """
    id: :class:`str`

    description: :class:`str`

    emits: list[:class:`str`]

    enabled_state: :class:`int`

    tasks: list[:class:`TriggerTasksData`]

    type: :class:`str`

    trigger_type: :class:`str`

    last_execute_error: NotRequired[:class:`bool`]

    last_error_reason: NotRequired[:class:`str`]

    """

    id: str
    description: str
    emits: list[str]
    enabled_state: int
    tasks: list[TriggerTasksData]
    type: str
    trigger_type: str
    last_execute_error: NotRequired[bool]
    last_error_reason: NotRequired[str]


class TriggerTasksData(TypedDict):
    """
    id: :class:`str`

    task_method_name: :class:`str`

    parameter_mapping: :class:`ParameterMapping`

    enabled_state: :class:`int`

    locked: :class:`bool`

    created_by: :class:`str`

    order: :class:`int`
    """

    id: str
    task_method_name: str
    parameter_mapping: ParameterMapping
    enabled_state: int
    locked: bool
    created_by: str
    order: int


class MCUserData(TypedDict):
    """
    name: :class:`str`

    uuid: :class:`str`
    """

    name: str
    uuid: str
