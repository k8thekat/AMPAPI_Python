from __future__ import annotations
from .base import Base
from .core import Core
from pathlib import Path
from typing import Any


class Util(Base):
    """
    AMP API util functions to parse specific API calls for specific Data.
    """
    async def getNodespec(self, amp: Core) -> str | dict[str, Any] | list | bool | int | None:
        """
        Creates a `setting_nodes.txt` in the script directory with nodes from api `Core/GetSettingSpec`

        Args:
            amp (Core): API_Core class object signed in.

        See -> `amp/util/setting_nodes.txt` 

        """
        res = await amp.get_settings_spec()
        dir = Path(__file__).parent.joinpath("setting_nodes.md")
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

    async def getPermissionNodes(self, amp: Core) -> str | dict[str, Any] | list | bool | int | None:
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
        dir = Path(__file__).parent.joinpath("permission_nodes.md")
        mode = "x"
        if dir.exists():
            mode = "w"

        if file == None:
            file = open(dir, mode)

        if not isinstance(text, list):
            return

        for index in text:
            if "Node" in index:
                file.write(f'{index["Node"]} \n')
            if "Children" in index:
                self.node_scrape(text=index["Children"], file=file)
