from datetime import datetime
from pprint import pformat
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from .types_ import TriggersData

APIResponseDataTableAlias = Union["UserApplicationData", "DeploymentTemplate"]


class DeploymentTemplate:
    """
    Used for :meth:`ADSModule.update_deployment_template` function call.

    .. note::
        Your pre-created data structure to be parsed for the required API parameters.


    Attributes
    -----------
    clone_role_into_user: :class:`bool`
        Clone the :attr:`template_role` to the users of this template.
    description: :class:`str`
        The description of the deployment template.
    id: :class:`int`
        The ID of the deployment template.
    module: :class:`str`
        The AMP Instance module type. eg. "Generic", "Minecraft"
    name: :class:`str`
        The deployment template name.
    template_base_app: :class:`str`
        The application that is template is used for.
    template_instance: Any
        UNK
    template_role: :class:`str`
        The template role name, similar to the AMP User Roles.
    match_datastore_tags: :class:`bool`
        To force match the datastore tags; if any.
    settings_mappings: dict[:class:`str`, :class:`str`]
        A dictionary of setting mappings.
    start_on_boot: :class:`bool`
        If the Instance should start on ADS01/Controller boot or not, default is False.
    tags: list[:class:`str`]
        The list of tags to assign to the template or that belong to the template.
    zip_overlay_path: :class:`bool`
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
        dict[:class:`str`, Any]
            Returns the class attributes in a key, value paired dict.
        """
        temp: dict[str, Any] = {}
        for key in self.__slots__:
            temp[key] = getattr(self, key)
        return temp


class TriggerID:
    """
    Used for a multitude of functions all related to Triggers and their IDs.

    Simply access the respective attribute and the unique GUID for that :class:`AMPInstance` Trigger ID will be returned.
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

    def __init__(self, data: list["TriggersData"]) -> None:
        for entry in data:
            setattr(self, entry["description"], entry["id"])

    def __repr__(self) -> str:
        _temp: dict[str, str] = vars(self)
        _temp.pop("_init")
        return pformat(_temp)


# class SettingsLogin(Enum):
#     @property
#     def use_auth_server(self) -> str:
#         """
#         use_auth_server _summary_
#         """

#         return "Core.Login.UseAuthServer"

#     def auth_server_url(self) -> str:
#         return "Core.Login.AuthServerURL"


class UserApplicationData:
    id: str
    user_session_id: str
    session_id: str | None
    name: str
    join_time: datetime  # ISO format timestamp.
    tags: str | None
    uid: str
    ip_address: str
    port: int
    time_logged_in: str  # 00:00:00.00000

    __slots__ = (
        "id",
        "ip_address",
        "join_time",
        "name",
        "port",
        "session_id",
        "tags",
        "time_logged_in",
        "uid",
        "user_session_id",
    )

    def __init__(
        self,
        id: str,  # noqa: A002 # This is due to id overshadowing Python built-ins, the JSON response data comes in with an id key.
        user_session_id: str,
        name: str,
        join_time: str,
        uid: str,
        ip_address: str,
        port: int,
        time_logged_in: str,
        session_id: Union[str, None] = None,
        tags: Union[str, None] = None,
    ) -> None:
        self.id = id
        self.user_session_id = user_session_id
        self.name = name
        self.join_time = datetime.fromisoformat(join_time)
        self.uid = uid
        self.ip_address = ip_address
        self.port = port
        self.time_logged_in = time_logged_in
        self.session_id = session_id
        self.tags = tags

        return
