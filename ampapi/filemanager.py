from __future__ import annotations
from typing import Union

from .types import *
from .base import Base

__all__ = ("FileManagerPlugin",)


class FileManagerPlugin(Base):
    async def copyFile(self, source: str, destination: str) -> ActionResult | str | bool | int | None:
        """
        Moves a file from the source directory to the destination. The path is relative to the Server/Instance home directory.\n
            Example `await Instance.copyFile("eula.txt", "test")` would move `/eula.txt` to `/test/eula.txt`

        Args:
            source (str): Directory starts from the Instance home path (`/`) along with the file name and the extension. (eg. "eula.txt")
                -> (File Manager `/` directory) eg `.ampdata/instance/VM_Minecraft/Minecraft/` *this is the home directory*
            destination (str): Similar to source; do not include the file name. (eg. "test")

        Returns:
            ActionResult | str | bool | int | None: Results from the API call.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'Origin': source,
            'TargetDirectory': destination
        }
        result = await self._call_api('FileManagerPlugin/CopyFile', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def renameFile(self, original: str, new: str) -> ActionResult | str | bool | int | None:
        """
        Changes the name of a file. \n
            Path's are absolute and relative to the Instances home directory. Do not include the (`/`)

        Args:
            original (str): The path to the file and the file name included. (eg. "test/myfile.txt")
            new (str): The file name to be changed; no path needed. (eg. "renamed_myfile.txt")

        Returns:
            ActionResult | str | bool | int | None: Results from the API call.
            See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'Filename': original,
            'NewFilename': new
        }
        result = await self._call_api('FileManagerPlugin/RenameFile', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def renameDirectory(self, oldDirectory: str, newDirectoryName: str) -> ActionResult | str | bool | int | None:
        """
        Changes the name of a file.\n
            Path's are absolute and relative to the Instances home directory. Do not include the (`/`)

        Args:
            oldDirectory (str): The full path to the old directory.
            newDirectoryName (str): The name component of the new directory (not the full path).

        Returns:
            ActionResult | str | bool | int | None: Results from the API call.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'oldDirectory': oldDirectory,
            'newDirectoryName': newDirectoryName
        }
        result = await self._call_api('FileManagerPlugin/RenameDirectory', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def getDirectoryListing(self, directory: str = "") -> list[Directory] | str | bool | int | None:
        """
        Returns a dictionary of the directory's properties and the files contained in the directory and their properties.

        Args:
            directory (str): Relative to the Server root directory . eg `Minecraft/` - If a file has a similar name it may return the file instead of the directory.

        Returns:
            list[Directory] | str | bool | int | None: Returns a list of Directory dataclasses.
                See `types.py -> Directory`
        """

        await self._connect()
        parameters = {
            'Dir': directory
        }
        result = await self._call_api('FileManagerPlugin/GetDirectoryListing', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return list(Directory(**directory) for directory in result)

    async def getFileChunk(self, name: str, position: int, length: int) -> FileChunk | str | bool | int | None:
        """
        Returns a specific section of Base64Data from a file.

        Args:
            name (str): File to open and read from.
            position (int): Start position to read from.
            length (int): How far to read from the start position.

        Returns:
            FileChunk | str | bool | int | None: Returns a FileChunk dataclass.
                See `types.py -> FileChunk`
        """
        await self._connect()
        parameters = {
            'Filename': name,
            'Position': position,
            'Length': length
        }
        result = await self._call_api('FileManagerPlugin/GetFileChunk', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return FileChunk(**result)  # type:ignore

    async def writeFileChunk(self, filename: str, data: str, offset: int, finalChunk: bool) -> ActionResult | str | bool | int | None:
        """
        Write data to a file with an offset.

        Args:
            filename (str): File to write data to.
            data (str): binary data to be written.
            offset (int): data offset from 0.
            finalChunk (bool): UNK

        Returns:
            ActionResult | str | bool | int | None: Results from the API call.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'Filename': filename,
            'Data': data,
            'Offset': offset,
            "FinalChunk": finalChunk
        }
        result = await self._call_api('FileManagerPlugin/WriteFileChunk', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def trashDirectory(self, dir_name: str) -> ActionResult | str | bool | int | None:
        """
        Moves a directory to the trash, files must be trashed before they can be `emptied`.\n
        See emptyTrash().

        Args:
            dir_name (str): Directory name; relative to the Server/Instance root. Supports pathing. eg `/home/config`

        Returns:
            ActionResult | str | bool | int | None: Results from the API call. 
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'DirectoryName': dir_name
        }
        result = await self._call_api('FileManagerPlugin/TrashDirectory', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def trashFile(self, filename: str) -> ActionResult | str | bool | int | None:
        """
        Moves a file to the trash, files must be trashed before they can be `emptied`. \n
        See emptyTrash().

        Args:
            filename (str): File name; relative to the Server/Instance root. Supports pathing. eg `/home/config`

        Returns:
            ActionResult | str | bool | int | None: Results from the API call. 
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'Filename': filename
        }
        result = await self._call_api('FileManagerPlugin/TrashFile', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore

    async def emptyTrash(self, trash_dir: str) -> ActionResult | str | bool | int | None:
        """
        Empties a trash bin for the AMP Server/Instance.

        Args:
            trash_dir (str): Directory name; relative to the Server/Instance root. Supports pathing. eg `/home/config` \n
            Typically the directory is called `Trashed Files`, it is case sensitive and located in the Server/Instance root directory.

        Returns:
            ActionResult | str | bool | int | None: Results from the API call. 
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            'TrashDirectoryName': trash_dir
        }
        result = await self._call_api('FileManagerPlugin/EmptyTrash', parameters)
        if isinstance(result, Union[None, bool, int, str]):
            return result
        return ActionResult(**result)  # type:ignore
