from __future__ import annotations

from pprint import pformat
from typing import TypedDict

from typing_extensions import NotRequired


class PermissionNode(TypedDict):
    name: str
    node: str
    display_name: str
    description: str | None
    children: list[PermissionNode]


class Consumes(TypedDict, total=False):
    """
    available_methods: consumes key
    """

    description: str
    input_type: str
    name: str
    value_type: str
    enum_values: NotRequired[str]


class ParameterMapping(TypedDict, total=False):
    user: NotRequired[str]
    reason: NotRequired[str]


class ScheduleDataData(TypedDict):
    available_methods: list[MethodsData]
    available_triggers: list[TriggersData]
    populated_triggers: list


class TriggersData(TypedDict):
    id: str
    description: str
    emits: list[str]
    enabled_state: int
    tasks: list[TriggerTasksData]
    type: str
    trigger_type: str
    last_execute_error: NotRequired[bool]
    last_error_reason: NotRequired[str]


class MethodsData(TypedDict):
    """
    available_methods
    """

    id: str
    name: str
    description: str
    consumes: list[Consumes]


class TriggerTasksData(TypedDict):
    id: str
    task_method_name: str
    parameter_mapping: ParameterMapping
    enabled_state: int
    locked: bool
    created_by: str
    order: int


class TriggerID:
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

    def __init__(self, data: list[TriggersData]) -> None:
        for entry in data:
            setattr(self, entry["description"], entry["id"])

    def __repr__(self) -> str:
        _temp: dict[str, str] = vars(self)
        _temp.pop("_init")
        return pformat(_temp)
