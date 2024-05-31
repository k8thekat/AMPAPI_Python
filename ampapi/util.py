from __future__ import annotations

from io import TextIOWrapper
from pathlib import Path
from typing import Any, Union

from ampapi.types import UpdateInfo

from .ads import ADSInstance
from .core import Core
from .instance import AMPInstance, AMPMinecraftInstance


class APIUtil():
    """
    AMP API util functions to parse specific API calls for specific Data.
    """

    async def get_node_spec(self, amp: Core) -> str | dict[str, Any] | list | bool | int | None:
        """
        Creates a `setting_nodes.txt` in the script directory with nodes from api `Core/GetSettingSpec`

        Args:
            amp (Core): API_Core class object signed in.

        See -> `amp/util/setting_nodes.txt`

        """
        res = await amp.get_settings_spec()
        dir = Path(__file__).parent.joinpath("../docs/setting_nodes.md")
        mode = "x"
        if dir.exists():
            mode = "w"
        file = open(dir, mode)

        if not isinstance(res, dict):
            return res

        for key in res:
            for value in res[key]:
                for entry in value:
                    if entry.lower() == "node":
                        file.write(f"{value[entry]} \n")
        file.close()

    async def get_permission_nodes(self, amp: Core) -> str | dict[str, Any] | list | bool | int | None:
        """
        Creates a `permission_nodes.txt` in the script directory with nodes from api `Core/GetPermissionsSpec`

        Args:
            amp (Core): API_Core class object signed in.

        See -> `amp/util/permission_nodes.txt`
        """
        res = await amp.get_permissions_spec()
        if isinstance(res, list):
            self.node_scrape(text=res)
        else:
            raise ValueError(f"Error - invalid data type returned. {type(res)}")

    def node_scrape(self, text: list[dict], file=None) -> None:
        """
        Pulls the key "Nodes" from the list of dictionary results and dumps them to a txt file.

        Args:
            text (list): The list of dictionary's
            file (_type_, optional): The file object to dump text to. Defaults to None. `**LEAVE NONE**`
        """
        dir = Path(__file__).parent.joinpath("../docs/permission_nodes.md")
        mode = "x"
        if dir.exists():
            mode = "w"

        if file == None:
            file = open(dir, mode)

        if not isinstance(text, list):
            return None

        for index in text:
            if "Node" in index:
                file.write(f'{index["Node"]} \n')
            if "Children" in index:
                self.node_scrape(text=index["Children"], file=file)
        file.close()

    @classmethod
    async def parse_get_api_spec(cls, instance: Union[Core, ADSInstance, AMPInstance, AMPMinecraftInstance]) -> None:
        """
        Creates a `api_spec.txt` in the script directory with nodes from api `Core/GetAPISpec`
        #TODO - Improve formatting of the Markdown file.
        Args:
            instance(str): The API Class 

        See -> `../docs/api_spec.md`
        """
        data: dict[Any, Any] = await instance.get_api_spec()
        platform_info: UpdateInfo = await instance.get_update_info()
        if not isinstance(data, dict):
            return None

        if isinstance(instance, Core):
            instance_type: str = "Core"

        if isinstance(instance, (ADSInstance, AMPInstance, AMPMinecraftInstance)):
            instance_type = instance.Module

        dir: Path = Path(__file__).parent.joinpath(f"../docs/{instance_type}_api_spec.md")
        parents: list = []
        mode = "x"
        if dir.exists():
            mode = "w"
        file: TextIOWrapper = open(file=dir, mode=mode)

        file.write(f"INSTANCE TYPE: {instance_type}\n")
        file.write(f"VERSION: {platform_info.Version}\n")
        file.write(f"BUILD: {platform_info.Build}\n\n")
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
