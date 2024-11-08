from __future__ import annotations

import json
import logging
import traceback
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

from .instance import AMPMinecraftInstance

if TYPE_CHECKING:
    from io import TextIOWrapper

    from .controller import AMPADSInstance, AMPControllerInstance, AMPInstance
    from .core import Core
    from .dataclass import Methods, SettingSpec, SettingsSpecParent, Triggers, TriggerTasks, UpdateInfo
    from .types_ import Consumes, ParameterMapping, PermissionNode


class APIUtil:
    """
    AMP API util functions to:
    - Parse JSON responses.
    - Dump Data to Files.
    - Generate API Spec Markdown files.
    """

    # static strings for documentation
    _instance_id_note = (
        """.. note::\n\tReplace ``instance-id`` with the something like the :py:class:`~Instance.instance_id` value.\n\n"""
    )
    _parent_node_note: str = (
        '.. note::\n\tAll nodes in this section will be prefixed with "%s.", see examples :ref:`Permission Nodes`\n\n'
    )
    _wildcard_nodes: str = """.. note::\n\tAny node with a '*' at the end of it is a wild card and using that will make all permissions nodes in that section equal to the value set, treat it like parent inheritance.\n\n"""

    _trigger_note: str = """.. note::\n\tAll of these triggers will have a unique ID field that is generated from :meth:`~Core.get_triggers` due to uniqueness.\n\n"""

    _method_note: str = """.. note::\n\t Place holder text....\n\n"""

    @staticmethod
    async def amp_api_update(instance: AMPControllerInstance, sanitize_json: bool) -> None:
        """|coro|

        Gets the AMP Instance API Endpoints and writes them out to a file. Used for version changes.

        .. note::
            Having a ``Minecraft`` type Instance is beneficial for this call. Otherwise you will only get the ADS/Controller API spec sheet.


        Parameters
        ----------
        instance : AMPControllerInstance
            Must be the Controller instance; as we are looking for the ADS and a Minecraft Instance.
        sanitize_json : bool
            Sanitize the JSON responses to meet PEP8 compliance.
        """
        # We call get_instances() to force a current listing of instances to be populated.
        await instance.get_instances()
        for entry in instance.instances:
            # Minecraft instances have their own unique API endpoints; so we need to get those.
            if entry.module == "Minecraft" and isinstance(entry, AMPMinecraftInstance) and entry.running is True:
                await APIUtil._parse_get_api_spec_to_file(instance=entry, sanitize_json=sanitize_json)
                break
        # We found our Minecraft Instance, now lets parse our Controller/ADS
        await APIUtil._parse_get_api_spec_to_file(instance=instance, sanitize_json=sanitize_json)

    @staticmethod
    async def generate_settings_permission_rst(instance: AMPControllerInstance | AMPADSInstance) -> None:
        """|coro|

        This will generate the Sphinx ``.rst`` files we use for documentation. The files will be written to ``../docs/nodes/``

        .. warning::
            There may be a few errors due to the formatting of AMPs return information; so it is wrapped in ``try/excepts``

        Parameters
        -----------
        instance: AMPControllerInstance | AMPADSInstance
            Must be of these types as the API endpoint :meth:`get_settingspec` is not available to all.
        """
        logger: Logger = logging.getLogger()
        spec: SettingsSpecParent = await instance.get_setting_spec()
        try:
            APIUtil._settings_node_parse(data=spec, title="Setting Nodes", title_body="", path="../docs/nodes")
        except Exception:
            logger.error(
                "Ran into a <Exception> when attempting to generate the Setting Nodes.rst.\n %s", traceback.print_exc()
            )
        perms: list[PermissionNode] = await instance.get_permissions_spec()
        try:
            APIUtil._permission_node_parse(data=perms, title="Permission Nodes", title_body="", path="../docs/nodes")
        except Exception:
            logger.error(
                "Ran into a <Exception> when attempting to generate the Permission Nodes.rst.\n %s", traceback.print_exc()
            )

    @staticmethod
    async def _parse_get_api_spec_to_file(
        instance: Union[Core, AMPADSInstance, AMPInstance, AMPMinecraftInstance], sanitize_json: bool
    ) -> None:
        """|coro|

        Creates a Markdown file related to the type of :param:`instance` that is passed in to the function.
        .. note::
            See directory ``/docs/{Module_type}_api_spec.md``. where {Module_type} is the class ``.Module`` attribute.

        Parameters
        ----------
        instance : Union[Core, AMPControllerInstance, AMPInstance, AMPMinecraftInstance]
            The class of either :py:class:`Core:, :py:class:'AMPInstance`, :py:class:`AMPControllerInstance` and or :py:class:`AMPMinecraftInstance`.
        sanitize_json : bool
            Sanitize the JSON responses to meet PEP8 compliance. Default is False.
        """
        _logger: Logger = logging.getLogger()

        data: dict[Any, Any] = await instance.get_api_spec(sanitize_json=sanitize_json)
        platform_info: UpdateInfo = await instance.get_update_info()
        instance_type = instance.module

        _dir: Path = Path(__file__).parent.joinpath(f"../docs/{instance_type}_api_spec.md")
        _logger.info(
            "Instance Type: %s\nVersion: %s\nBuild: %s\nPath: %s",
            instance_type,
            platform_info.version,
            platform_info.build,
            _dir,
        )
        parents: list = []
        mode = "x"
        if _dir.exists():
            mode = "w"
        with Path.open(_dir, mode) as file:
            file.write(f"INSTANCE TYPE: {instance_type}\n")
            file.write(f"VERSION: {platform_info.version}\n")
            file.write(f"BUILD: {platform_info.build}\n\n")
            for parent, parent_value in sorted(data.items()):
                if parent not in parents:
                    parents.append(parent)
                    file.write("____________________________________________________\n")
                    file.write(f"{parent}:\n")
                if isinstance(parent_value, dict):
                    for child, child_value in sorted(parent_value.items()):
                        file.write(f"\t{child}:\n")
                        if isinstance(child_value, dict):
                            for key, value in sorted(child_value.items()):
                                if key == "Parameters":
                                    file.write(f"\t\t{key}:\n")
                                    for entry in value:
                                        file.write(f"\t\t\t{entry}\n")
                                else:
                                    file.write(f"\t\t{key}: {value}\n")

                        else:
                            file.write(f"\t\t({child_value})\n")

            file.close()

    @staticmethod
    def _permission_node_parse(
        data: list[PermissionNode],
        title: str = "",
        title_body: str = "",
        index: int = 0,
        path: str | None = None,
        file: Union[TextIOWrapper, None] = None,
    ) -> None:
        from docs.samples.permission_node_usage import example_note

        index = index
        used_keys: list[Any] = []

        file_name: str = title.lower().replace(" ", "_")
        _dir: Path = (
            Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
        )
        mode = "x"
        if _dir.exists():
            mode = "w"

        if file == None:
            file = Path.open(_dir, mode)

        if index == 0:
            # First through iteration, we write our header and title.
            file.write(".. role:: raw-html(raw)\n\t:format: html\n")
            file.write(f"\n{title}\n")
            file.write(f"{APIUtil.repeat_to_length(string=title, repeat_char='=')}\n")
            file.write(":raw-html:`<hr>`\n\n")
            file.write(title_body + "\n")
            file.write("\n" + APIUtil._wildcard_nodes)
            file.write(f"\n{example_note}\n")

        for entry in data:
            # print(f"Currently on {index} -- checking {entry['name']} | not used?: {entry['name'] not in used_keys}")
            if isinstance(entry, dict) and entry["name"] not in used_keys and index == 0:
                used_keys.append(entry["name"])

                # Our first headers.
                header = entry["name"] + " Permission Nodes"
                file.write(f"\n{header}\n")
                file.write(f"{APIUtil.repeat_to_length(string=header, repeat_char='#')}\n")
                file.write(":raw-html:`<hr>`\n\n")

                # Our node description handler.
                if entry["description"] is not None and len(entry["description"]) > 0:
                    file.write(f"Description: {entry['description']}\n\n")

                temp: list[str] = entry["node"].split(".")
                # This is to handle Instances having their Instance ID as the value.
                if entry["node"].startswith("Instances") and isinstance(entry["children"], list):
                    file.write(APIUtil._instance_id_note)

                    # Handles formatting our nodes
                    file.write(f"- {temp[-1]}.*\n")

                    for children in entry["children"]:
                        # We cheaply ignore them since they always have a "-" in them.
                        if "-" in children["name"]:
                            new_child: PermissionNode = children["children"][0]
                            for node in new_child["children"]:
                                # Handles formatting our nodes
                                file.write(f"- Instances.`instance-id`.{node['name']}\n")
                    continue
                else:
                    # Our notes about the prefix characters.
                    file.write(APIUtil._parent_node_note % entry["name"] + "\n")
                    # Handles formatting our nodes
                    file.write(f"- {temp[-1]}.*\n")
            if isinstance(entry, dict) and entry["name"] not in used_keys and index == 1:
                used_keys.append(entry["name"])

                # Our second headers.
                header = entry["name"] + " Nodes"
                # file.write("\n:raw-html:`<hr>`\n")
                file.write(f"\n{header}\n")
                file.write(f"{APIUtil.repeat_to_length(string=header, repeat_char='~')}\n")
                file.write(":raw-html:`<hr>`\n\n")

                # Our node description handler.
                if entry["description"] is not None and len(entry["description"]) > 0:
                    file.write(f"Description: {entry['description']}\n\n")

                # Handles formatting our nodes
                temp = entry["node"].split(".")

                # These 4 modules DO NOT have 2 layers of parents to get through. So we need to cut them shorter.
                if entry["node"].startswith(("ADS", "FileManager", "LocalFileBackup", "Core")) and isinstance(
                    entry["children"], list
                ):
                    file.write(f"- {temp[-1]}.*\n")
                    for node in entry["children"]:
                        file.write(f"- {temp[-1]}.{node['name']}\n")
                    continue
                else:
                    # Our notes about the prefix characters.
                    file.write(APIUtil._parent_node_note % entry["name"] + "\n")

                    # Handles formatting our nodes
                    file.write(f"- {temp[-1]}.*\n")
            if isinstance(entry, dict) and entry["name"] not in used_keys and index == 2:
                used_keys.append(entry["name"])
                header: str | Any = entry["name"] + " Nodes"
                if entry["node"].startswith("Settings.FileManagerPlugin."):
                    header = "FMP " + header

                # Handles the Header for the rst to break up sections. This is our second subsection.
                file.write(f"\n{header}\n")
                file.write(f"{APIUtil.repeat_to_length(string=header, repeat_char='^')}\n")
                file.write(":raw-html:`<hr>`\n\n")

                # Handles formatting our nodes
                temp = entry["node"].split(".")
                file.write(f"- {temp[-1]}.*\n")

                # handles the remaining entries of our nodes.
                if isinstance(entry["children"], list):
                    for node in entry["children"]:
                        # Handles formatting our nodes
                        file.write(f"- {temp[-1]}.{node['name']}\n")

            if isinstance(entry["children"], list):
                APIUtil._permission_node_parse(data=entry["children"], index=index + 1, file=file)

        if index == 0:
            file.close()

    @staticmethod
    def _settings_node_parse(
        data: SettingsSpecParent,
        title: str = "",
        title_body: str = "",
        index: int = 0,
        path: None | str = None,
        file: Union[TextIOWrapper, None] = None,
    ) -> None:
        from docs.samples.settings_node_usage import example_note

        index = index

        file_name: str = title.lower().replace(" ", "_")
        _dir: Path = (
            Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
        )
        mode = "x"
        if _dir.exists():
            mode = "w"

        if file == None:
            file = Path.open(_dir, mode)

        if index == 0:
            # First through iteration, we write our header and title.
            file.write(".. role:: raw-html(raw)\n\t:format: html\n")
            file.write(f"\n{title}\n")
            file.write(f"{APIUtil.repeat_to_length(string=title, repeat_char='=')}\n")
            file.write(":raw-html:`<hr>`\n\n")
            file.write(title_body + "\n")
            file.write("\n" + APIUtil._wildcard_nodes)
            file.write(f"\n{example_note}\n")

        for key in sorted(vars(data)):
            # Our second headers.
            header: str = "Settings " + key.title() + " Nodes"
            # file.write("\n:raw-html:`<hr>`\n")
            file.write(f"\n{header}\n")
            file.write(f"{APIUtil.repeat_to_length(string=header, repeat_char='#')}\n")
            file.write(":raw-html:`<hr>`\n\n")

            data_key: list[SettingSpec] = getattr(data, key)
            if isinstance(data_key, list):
                for entry in sorted(data_key):
                    file.write(f"\n**Name**: {entry.name}\n")
                    if entry.description != None and len(entry.description) > 0:
                        file.write(f"\t| Description: {entry.description}\n")
                    file.write(f"\t| Node: `{entry.node}`\n")
        file.close()

    @staticmethod
    def _trigger_event_parse(
        data: list[Triggers],
        title: str = "",
        title_body: str = "",
        path: None | str = None,
    ) -> None:
        """
        This assumes you have acquired the ScheduleData already and are passing in :attr:`~scheduleData.available_triggers`

        .. note::
            All of these triggers will have a unique ID field that is generated from :meth:`~Core.get_triggers` due to uniqueness.


        Parameters
        -----------
        data: list[:class:`Triggers`]
            The list of dataclass Triggers.
        title: :class:`str`, optional
            The Title of the document header; this is also used to set the filename, by default "".
        title_body: :class:`str`, optional
            The body just under the document header, by default "".
        path: :class:`None | str`, optional
            The path to save the .rst file., by default None.
        """
        from docs.samples.trigger_event_usage import example_note

        file_name: str = title.lower().replace(" ", "_")
        _dir: Path = (
            Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
        )
        mode = "x"
        if _dir.exists():
            mode = "w"

        file = Path.open(_dir, mode)

        # First through iteration, we write our header and title.
        file.write(".. role:: raw-html(raw)\n\t:format: html\n")
        file.write(f"\n{title}\n")
        file.write(f"{APIUtil.repeat_to_length(string=title, repeat_char='=')}\n")
        file.write(":raw-html:`<hr>`\n\n")
        file.write(title_body + "\n")

        sub_header: str = "\nEvents Information\n"
        file.write(sub_header)
        file.write(f"{APIUtil.repeat_to_length(string=sub_header, repeat_char='#')}\n")
        file.write(":raw-html:`<hr>`\n")
        file.write("\n" + APIUtil._trigger_note)
        file.write(f"\n{example_note}\n")
        for trigger in sorted(data):
            _temp: str = " | "
            file.write("\n:raw-html:`<hr>`\n")
            file.write(f"**Trigger Description**: {trigger.description}\n\n")
            if len(trigger.emits) > 0:
                file.write(f"- Emits: {_temp.join(trigger.emits)}\n")
        file.close()

    @staticmethod
    def _method_event_parse(data: list[Methods], title: str = "", title_body: str = "", path: None | str = None) -> None:
        from docs.samples.method_event_usage import example_note

        file_name: str = title.lower().replace(" ", "_")
        _dir: Path = (
            Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
        )
        mode = "x"
        if _dir.exists():
            mode = "w"

        file = Path.open(_dir, mode)

        # First through iteration, we write our header and title.
        file.write(".. role:: raw-html(raw)\n\t:format: html\n")
        file.write(f"\n{title}\n")
        file.write(f"{APIUtil.repeat_to_length(string=title, repeat_char='=')}\n")
        file.write(":raw-html:`<hr>`\n")
        file.write(title_body + "\n")

        # make a sub heading with "Event Method Names:"
        sub_header: str = "\nMethod Information\n"
        file.write(sub_header)
        file.write(f"{APIUtil.repeat_to_length(string=sub_header, repeat_char='#')}\n")
        file.write(":raw-html:`<hr>`\n")
        file.write("\n" + APIUtil._method_note)
        file.write(f"\n{example_note}\n")

        for method in sorted(data):
            file.write(f"\n{method.name}\n")
            file.write(f"{APIUtil.repeat_to_length(string=method.name, repeat_char='~')}\n")
            file.write(":raw-html:`<hr>`\n")
            file.write(f"- ``{method.id}``\n\n")
            file.write(f"{method.description}\n\n")
            file.write("Consumes these values:\n")
            for entry in sorted(method.consumes):
                # print(entry, type(entry.enum_values), entry.enum_values)
                file.write(f"\t* {entry.name}: type({entry.value_type})\n")
                if isinstance(entry.enum_values, dict):
                    for key, value in sorted(entry.enum_values.items()):
                        file.write(f"\t\t* {key} - {value}\n")
        file.close()

    @staticmethod
    def dump_to_file(
        data: Union[dict, list], file_name: str = "", path: Union[Path, None] = None, no_format: bool = True
    ) -> None:
        """
        Dump's a list or dict to a file.

        Parameters
        ----------
        data : Union[dict, list]
            The data to dump to a file.
        path : Union[Path, None], optional
            The Path to store the dump file, by default None
            - If ``None`` will use the ``../docs/dumps/`` path.
        """
        if file_name == "":
            file_name = str(object=datetime.today().date())
        if path is None:
            _cwd: Path = Path("../docs/dumps/").joinpath(f"{file_name}.dump")
        else:
            _cwd = path.joinpath(f"{file_name}.dump")

        with _cwd.open(mode="w+") as file:
            res: str = json.dumps(data, indent=4, skipkeys=True, separators=(",", ": "), sort_keys=True)
            file.write(res)

    @staticmethod
    def repeat_to_length(string: str, repeat_char: str, length: int = 0) -> str:
        """
        Will repeat the passed in ``repeat_char`` by the ``len(string)`` provided or by the ``length`` parameter.

        .. note::
            By default the ``repeat_char`` will be one longer than the provided string unless you specify the ``length`` parameter.


        Parameters
        -----------
        string: str
            The string to match the :meth:`len` of.
        repeat_char: str
            The char to repeat to the length of the string or the ``length`` parameter.
        length: int, optional
            The length to repeat the char by, by default 0.

        Returns
        --------
        :class:`str`
            The modified ``repeat_char`` str by the ``length`` provided.
        """
        if length == 0:
            length = len(string) + 1
        return repeat_char * length
