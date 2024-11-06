from __future__ import annotations

import json
import logging
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from io import TextIOWrapper

    from .controller import AMPControllerInstance
    from .core import Core
    from .dataclass import SettingSpec, SettingsSpecParent, UpdateInfo
    from .instance import AMPADSInstance, AMPInstance, AMPMinecraftInstance


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

    @staticmethod
    async def AMP_to_API_update(
        instance: AMPControllerInstance | AMPInstance | AMPMinecraftInstance, sanitize_json: bool
    ) -> None:
        """
        Gets the AMP Instance API Endpoints and writes them out to a file. Used for version changes.

        Parameters
        ----------
        instance : AMPControllerInstance | AMPInstance | AMPMinecraftInstance
            Any type of AMP Instance to get the API endpoints for.
        sanitize_json : bool
            Sanitize the JSON responses to meet PEP8 compliance.
        """
        await APIUtil.parse_get_api_spec_to_file(instance=instance, sanitize_json=sanitize_json)

    @staticmethod
    def dump_to_file(data: Union[dict, list], path: Union[Path, None] = None, no_format: bool = True) -> None:
        """
        Dump's a list or dict to a file.

        Parameters
        ----------
        data : Union[dict, list]
            The data to dump to a file.
        path : Union[Path, None], optional
            The Path to store the dump file, by default None
            - If ``None`` will use the ``__file__.parent`` path.
        """
        if path is None:
            _cwd: Path = Path(__file__).parent.joinpath(f"{datetime.today().date()}.dump")
        else:
            _cwd = path.joinpath(f"{datetime.today().date()}.dump")
        with Path.open(_cwd, "w+") as file:
            res: str = json.dumps(data, indent=4, skipkeys=True, separators=(",", ": "), sort_keys=True)
            file.write(res)

    @staticmethod
    def permission_node_parse(
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
                APIUtil.permission_node_parse(data=entry["children"], index=index + 1, file=file)

        if index == 0:
            file.close()

    @staticmethod
    def settings_node_parse(
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
            # file.write(f"\n{example_note}\n")

        for key in vars(data):
            # Our second headers.
            header: str = "Settings " + key.title() + " Nodes"
            # file.write("\n:raw-html:`<hr>`\n")
            file.write(f"\n{header}\n")
            file.write(f"{APIUtil.repeat_to_length(string=header, repeat_char='#')}\n")
            file.write(":raw-html:`<hr>`\n\n")

            data_key: list[SettingSpec] = getattr(data, key)
            if isinstance(data_key, list):
                for entry in data_key:
                    file.write(f"\n**Name**: {entry.name}\n")
                    if entry.description != None and len(entry.description) > 0:
                        file.write(f"\t| Description: {entry.description}\n")
                    file.write(f"\t| Node: `{entry.node}`\n")
        file.close()

    @staticmethod
    def repeat_to_length(string: str, repeat_char: str, length: int | None = None) -> str:
        if length == None:
            length = len(string) + 1
        return repeat_char * length

    @staticmethod
    async def parse_get_api_spec_to_file(
        instance: Union[Core, AMPADSInstance, AMPInstance, AMPMinecraftInstance], sanitize_json: bool
    ) -> None:
        """
        Creates a Markdown file related to the type of :param:`instance` that is passed in to the function.
        - See directory ``/docs/{Module_type}_api_spec.md``. where {Module_type} is the class ``.Module`` attribute.

        Parameters
        ----------
        instance : Union[Core, AMPControllerInstance, AMPInstance, AMPMinecraftInstance]
            The class of either :py:class:`Core:, :py:class:'AMPInstance`, :py:class:`AMPControllerInstance` and or :py:class:`AMPMinecraftInstance`.
        sanitize_json : bool
            Sanitize the JSON responses to meet PEP8 compliance. Default is False.

        See -> `../docs/api_spec.md`
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
            for parent, parent_value in data.items():
                if parent not in parents:
                    parents.append(parent)
                    file.write("____________________________________________________\n")
                    file.write(f"{parent}:\n")
                if isinstance(parent_value, dict):
                    for child, child_value in parent_value.items():
                        file.write(f"\t{child}:\n")
                        if isinstance(child_value, dict):
                            for key, value in child_value.items():
                                if key == "Parameters":
                                    file.write(f"\t\t{key}:\n")
                                    for entry in value:
                                        file.write(f"\t\t\t{entry}\n")
                                else:
                                    file.write(f"\t\t{key}: {value}\n")

                        else:
                            file.write(f"\t\t({child_value})\n")

            file.close()


from typing import TypedDict


class PermissionNode(TypedDict):
    name: str
    node: str
    display_name: str
    description: str | None
    children: list[PermissionNode]
