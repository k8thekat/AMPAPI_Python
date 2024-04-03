from __future__ import annotations

from typing import Union

from .base import FORMAT_DATA, Base
from .types import *

__all__ = ("FileManagerPlugin",)


class FileManagerPlugin(Base):
    """
    Contains the base functions for any `/API/FileManagerPlugin/` AMP API endpoints.

    """

    # FileManagerPlugin.CopyFile:({'Parameters': [{'Name': 'Origin', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'TargetDirectory', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def copy_file(self, origin: str, target_directory: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Moves a file from the origin directory to the target_directory. The path is relative to the Server/Instance home directory.\n
            Example `await Instance.copyFile("eula.txt", "test")` would move `/eula.txt` to `/test/eula.txt`

        Args:
            origin (str): Directory starts from the Instance home path (`/`) along with the file name and the extension. (eg. "eula.txt")
                -> (File Manager `/` directory) eg `.ampdata/instance/VM_Minecraft/Minecraft/` *this is the home directory*
            target_directory (str): Similar to source; do not include the file name. (eg. "test")
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'Origin': origin,
            'TargetDirectory': target_directory
        }
        result = await self._call_api(api='FileManagerPlugin/CopyFile', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.RenameFile:({'Parameters': [{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'NewFilename', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def rename_file(self, file_name: str, new_file_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Changes the name of a file. \n
            Path's are absolute and relative to the Instances home directory. Do not include the (`/`)

        Args:
            file_name (str): The path to the file and the file name included. (eg. "test/myfile.txt")
            new_file_name (str): The file name to be changed; no path needed. (eg. "renamed_myfile.txt")
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
            See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'Filename': file_name,
            'NewFilename': new_file_name
        }
        result = await self._call_api(api='FileManagerPlugin/RenameFile', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.RenameDirectory:({'Description': 'Renames a directory', 'Returns': '', 'Parameters': [{'Name': 'oldDirectory', 'TypeName': 'String', 'Description': 'The full path to the old directory', 'Optional': False}, {'Name': 'NewDirectoryName', 'TypeName': 'String', 'Description': 'The name component of the new directory (not the full path)', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def rename_directory(self, old_directory: str, new_directory_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Rename a directory.\n
            Path's are absolute and relative to the Instances home directory. Do not include the (`/`)

        Args:
            old_directory (str): The full path to the old directory.
            new_directory_name (str): The name component of the new directory (not the full path).
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: Results from the API call.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'oldDirectory': old_directory,
            'newDirectoryName': new_directory_name
        }
        result = await self._call_api(api='FileManagerPlugin/RenameDirectory', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.GetDirectoryListing:({'Parameters': [{'Name': 'Dir', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    async def get_directory_listing(self, directory: str = "", format_data: Union[bool, None] = None) -> list[Directory]:
        """
        Returns a dictionary of the directory's properties and the files contained in the directory and their properties.

        Args:
            directory (str): Relative to the Server root directory . eg `Minecraft/` - If a file has a similar name it may return the file instead of the directory.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            list[Directory]: Returns a list of Directory dataclasses.
                See `types.py -> Directory`
        """

        await self._connect()
        parameters = {
            'Dir': directory
        }
        result = await self._call_api(api='FileManagerPlugin/GetDirectoryListing', parameters=parameters, format_data=format_data, format=Directory, _use_from_dict=False)
        return result

    # FileManagerPlugin.GetFileChunk:({'Parameters': [{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Position', 'TypeName': 'Int64', 'Description': '', 'Optional': False}, {'Name': 'Length', 'TypeName': 'Int32', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'JObject', 'IsComplexType': True})
    async def get_file_chunk(self, file_name: str, position: int, length: int, format_data: Union[bool, None] = None) -> FileChunk:
        """
        Returns a specific section of Base64Data from a file.

        Args:
            name (str): File to open and read from.
            position (int): Start position to read from.
            length (int): How far to read from the start position.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            FileChunk: Returns a FileChunk dataclass.
                See `types.py -> FileChunk`
        """

        await self._connect()
        parameters = {
            'Filename': file_name,
            'Position': position,
            'Length': length
        }
        result = await self._call_api(api='FileManagerPlugin/GetFileChunk', parameters=parameters, format_data=format_data, format=FileChunk)
        return result

    # FileManagerPlugin.WriteFileChunk:({'Parameters': [{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Data', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Offset', 'TypeName': 'Int64', 'Description': '', 'Optional': False}, {'Name': 'FinalChunk', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def write_file_chunk(self, file_name: str, data: str, offset: int, final_chunk: bool, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Write data to a file with an offset.

        Args:
            file_name (str): File name to write the data to; relative to the Server/Instance root. Supports pathing. eg `home/config`
            data (str): Binary data to be written.
            offset (int): Data offset from start of file.
            final_chunk (bool): Appends the data to the end of the file.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: Results from the API call.
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'Filename': file_name,
            'Data': data,
            'Offset': offset,
            "FinalChunk": final_chunk
        }
        result = await self._call_api(api='FileManagerPlugin/WriteFileChunk', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.TrashDirectory:({'Description': 'Moves a directory to trash, files must be trashed before they can be deleted.', 'Returns': '', 'Parameters': [{'Name': 'DirectoryName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def trash_directory(self, directory_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Moves a directory to the trash, files must be trashed before they can be `emptied`.\n
            See `emptyTrash()`.

        Args:
            directory_name (str): Directory name; relative to the Server/Instance root. Supports pathing. eg `home/config`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: Results from the API call. 
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'DirectoryName': directory_name
        }
        result = await self._call_api(api='FileManagerPlugin/TrashDirectory', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.TrashFile:({'Description': 'Moves a file to trash, files must be trashed before they can be deleted.', 'Returns': '', 'Parameters': [{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def trash_file(self, file_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Moves a file to the trash, files must be trashed before they can be `emptied`. \n
            See `emptyTrash()`.

        Args:
            file_name (str): File name; relative to the Server/Instance root. Supports pathing. eg `home/config`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: Results from the API call. 
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'Filename': file_name
        }
        result = await self._call_api(api='FileManagerPlugin/TrashFile', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.EmptyTrash:({'Description': 'Empties a trash bin', 'Returns': '', 'Parameters': [{'Name': 'TrashDirectoryName', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def empty_trash(self, trash_directory_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Empties a trash bin for the AMP Server/Instance.

        Args:
            trash_directory_name (str): Path to the directory; relative to the Server/Instance root. eg `home/config`. \n
                - Typically the directory is called `Trashed Files`, it is case sensitive and located in the Server/Instance root directory.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: Results from the API call. 
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            'TrashDirectoryName': trash_directory_name
        }
        result = await self._call_api(api='FileManagerPlugin/EmptyTrash', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.CalculateFileMD5Sum:({'Parameters': [{'Name': 'FilePath', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult<String>', 'IsComplexType': True})
    async def calculate_file_md5_sum(self, file_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Calculate the MD5 sum of a file.

        Args:
            file_path (str): Path to the file; relative to the Server/Instance root. eg `home/config`.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "FilePath": file_path
        }
        result = await self._call_api(api='FileManagerPlugin/CalculateFileMD5Sum', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.ChangeExclusion:({'Parameters': [{'Name': 'ModifyPath', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'AsDirectory', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}, {'Name': 'Exclude', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def change_exclusion(self, modify_path: str, as_directory: bool, exclude: bool, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Change a file or directory to be excluded from backups.

        Args:
            modify_path (str): Path to the file; relative to the Server/Instance root. eg `home/config`
            as_directory (bool): If modify_path is a directory
            exclude (bool): If modify_path should be excluded
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "ModifyPath": modify_path,
            "AsDirectory": as_directory,
            "Exclude": exclude
        }
        result = await self._call_api(api='FileManagerPlugin/ChangeExclusion', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.CreateArchive:({'Parameters': [{'Name': 'PathToArchive', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def create_archive(self, path_to_archive: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Create an archive file.

        Args:
            path_to_archive (str): Path to the file; relative to the Server/Instance root. eg `home/config`
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "PathToArchive": path_to_archive
        }
        result = await self._call_api(api='FileManagerPlugin/CreateArchive', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.ExtractArchive:({'Parameters': [{'Name': 'ArchivePath', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'DestinationPath', 'TypeName': 'String', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def extract_archive(self, archive_path: str, destination_path: str | None = None, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Extract an archive file.

        Args:
            archive_path (str): Path to the archive to extract; relative to the Server/Instance root. eg `home/config`.
            destination_path (str | None, optional): Path to extract the archive to; relative to the Server/Instance root. eg `home/config`. Defaults to None.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "ArchivePath": archive_path
        }

        if destination_path != None:
            parameters["DestinationPath"] = destination_path

        result = await self._call_api(api='FileManagerPlugin/ExtractArchive', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.AppendFileChunk:({'Parameters': [{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Data', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Delete', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def append_file_chunk(self, file_name: str, data: str, delete: bool) -> None:
        """
        Append data to a file.

        Args:
            file_name (str): Path to the file; relative to the Server/Instance root. eg `home/config`.
            data (str): Binary data to be written.
            delete (bool): UNK #TODO - What does this do?
        """
        await self._connect()
        parameters = {
            "Filename": file_name,
            "Data": data,
            "Delete": delete
        }
        await self._call_api(api='FileManagerPlugin/AppendFileChunk', parameters=parameters)
        return

    # FileManagerPlugin.ReadFileChunk:({'Parameters': [{'Name': 'Filename', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Offset', 'TypeName': 'Int64', 'Description': '', 'Optional': False}, {'Name': 'ChunkSize', 'TypeName': 'Int64', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult<String>', 'IsComplexType': True})
    async def read_file_chunk(self, file_name: str, offset: int, chunk_size: int | None = None, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Read a chunk of data from a file.

        Args:
            file_name (str): Path to the file; relative to the Server/Instance root. eg `home/config`.
            offset (int): Data offset from start of file.
            chunk_size (int | None, optional): Data chunk size. Defaults to None.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "Filename": file_name,
            "Offset": offset
        }
        if chunk_size != None:
            parameters["ChunkSize"] = chunk_size

        result = await self._call_api(api='FileManagerPlugin/ReadFileChunk', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.DownloadFileFromURL:({'Parameters': [{'Name': 'Source', 'TypeName': 'Uri', 'Description': '', 'Optional': False}, {'Name': 'TargetDirectory', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def download_file_from_url(self, source: str, target_directory: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Download a file from a URL.

        Args:
            source (str): URL to file.
            target_directory (str): Path to the file; relative to the Server/Instance root. eg `home/config`.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "Source": source,
            "TargetDirectory": target_directory
        }
        result = await self._call_api(api='FileManagerPlugin/DownloadFileFromURL', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # FileManagerPlugin.CreateDirectory:({'Description': 'Creates a new directory. The parent directory must already exist.', 'Returns': '', 'Parameters': [{'Name': 'NewPath', 'TypeName': 'String', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def create_directory(self, new_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Creates a new directory. The parent directory must already exist.

        Args:
            new_path (str): Path to the directory; relative to the Server/Instance root. eg `home/config`.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns an ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "NewPath": new_path
        }
        result = await self._call_api(api='FileManagerPlugin/CreateDirectory', parameters=parameters, format_data=format_data, format=ActionResult)
        return result
