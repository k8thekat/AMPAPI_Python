from typing import Any, Union

from .base import Base
from .dataclass import ActionResult, Directory, FileChunk

__all__ = ("FileManagerPlugin",)


class FileManagerPlugin(Base):
    """
    Contains all functions for any ``/API/FileManagerPlugin/`` API endpoints.

    .. note::
        All file_path fields must include the path to the file and the file name. All paths are relative to the Server/Instance root that is making the API call.


    .. note::
        You do not need to include the "/" at the start of the path. All file_path fields are sanitized prior to making the API call. See :meth:`~Base.sanitize_path`


    .. note::
        "await Instance.copyFile("eula.txt", "test")" would move "./InstanceName/eula.txt" to "./InstanceName/test/eula.txt"



    """

    # TODO - What does the delete parameter on this function do?
    async def append_file_chunk(self, file_path: str, data: str, delete: bool) -> None:
        """|coro|

        Append data to a file.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        data: :class:`str`
            Binary data to be written.
        delete: :class:`bool`
            UNK
        """

        await self._connect()
        parameters: dict[str, Any] = {"Filename": self.sanitize_path(path=file_path), "Data": data, "Delete": delete}
        await self._call_api(api="FileManagerPlugin/AppendFileChunk", parameters=parameters)
        return

    async def calculate_file_md5_sum(self, file_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Calculate the MD5 sum of a file.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"FilePath": self.sanitize_path(path=file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/CalculateFileMD5Sum", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def change_exclusion(
        self, file_path: str, as_directory: bool, exclude: bool, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Change a file or directory to be excluded from backups.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        as_directory: :class:`bool`
            If file_path is a directory.
        exclude: :class:`bool`
            If file_path should be excluded from backups or not.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, Any] = {
            "ModifyPath": self.sanitize_path(path=file_path),
            "AsDirectory": as_directory,
            "Exclude": exclude,
        }
        result: Any = await self._call_api(
            api="FileManagerPlugin/ChangeExclusion", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def copy_file(self, file_path: str, destination_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Moves a file from the origin directory to the target_directory.

        .. warning::
            Make sure to NOT INCLUDE the file name in the destionation_path parameter.


        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        destionation_path: :class:`str`
            Similar to file_path; do not include the file name. (eg. "test")
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Origin": self.sanitize_path(file_path), "TargetDirectory": destination_path}
        result: Any = await self._call_api(
            api="FileManagerPlugin/CopyFile", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def create_archive(self, file_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Create an archive file.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"PathToArchive": self.sanitize_path(file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/CreateArchive", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def create_directory(self, file_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Creates a new directory. The parent directory must already exist.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"NewPath": self.sanitize_path(file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/CreateDirectory", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def download_file_from_url(
        self, source: str, file_path: str, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Download a file from a URL.

        Parameters
        -----------
        source: :class:`str`
            The URL to file.
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Source": source, "TargetDirectory": self.sanitize_path(file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/DownloadFileFromURL", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def empty_trash(self, file_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Empties a trash bin for the AMP Server/Instance.

        .. note::
            Typically the directory is called ``Trashed Files``, it is case sensitive and located in the Server/Instance root directory.


        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"TrashDirectoryName": self.sanitize_path(file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/EmptyTrash", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def extract_archive(
        self, file_path: str, destination_path: Union[str, None] = None, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Extract an archive file.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        destination_path: Union[:class:`str`, None], optional
            The path to extract the archive to; relative to the Server/Instance root. eg ``home/config``, defaults to None.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"ArchivePath": self.sanitize_path(file_path)}

        if destination_path is not None:
            parameters["DestinationPath"] = destination_path

        result: Any = await self._call_api(
            api="FileManagerPlugin/ExtractArchive", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def get_directory_listing(self, file_path: str = "", format_data: Union[bool, None] = None) -> list[Directory]:
        """|coro|

        Returns a dictionary of the path's properties and the files contained in the directory and their properties.

        .. note::
            If a file has a similar name it may return the file instead of the directory.


        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`Directory`]
            On success returns a list of :class:`Directory` dataclasses.
        """

        await self._connect()
        parameters: dict[str, str] = {"Dir": self.sanitize_path(file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/GetDirectoryListing",
            parameters=parameters,
            format_data=format_data,
            format_=Directory,
            _use_from_dict=False,
        )
        return result

    async def get_file_chunk(
        self, file_path: str, index: int, length: int, format_data: Union[bool, None] = None
    ) -> FileChunk:
        """|coro|

        Returns a specific section of Base64 data from the file.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        index: :class:`int`
            The start position to read the file from, in bytes.
        length: :class:`int`
            How far to read from the index position, in bytes.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`FileChunk`
            On success returns a :class:`FileChunk` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Filename": self.sanitize_path(file_path), "Position": index, "Length": length}
        result: Any = await self._call_api(
            api="FileManagerPlugin/GetFileChunk", parameters=parameters, format_data=format_data, format_=FileChunk
        )
        return result

    async def read_file_chunk(
        self, file_path: str, offset: int, chunk_size: Union[int, None] = None, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Read a chunk of data from a file.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        index: :class:`int`
            The start position to read the file from, in bytes.
        length: :class:`int`
            How far to read from the index position, in bytes.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Filename": self.sanitize_path(file_path), "Offset": offset}
        if chunk_size is not None:
            parameters["ChunkSize"] = chunk_size

        result: Any = await self._call_api(
            api="FileManagerPlugin/ReadFileChunk", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    # TODO - Test functionality or get clarification on use/action.
    async def release_file_upload_lock(self, file_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Releases a File Upload Lock.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"Filename": self.sanitize_path(file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/ReleaseFileUploadLock",
            parameters=parameters,
            format_data=format_data,
            format_=ActionResult,
        )
        return result

    async def rename_directory(self, file_path: str, name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Rename a directory.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the directory; relative to the Instance root. eg ``./InstanceName/``.
        name: :class:`str`
            The new name for the directory, do not include the path.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {
            "oldDirectory": self.sanitize_path(path=file_path),
            "newDirectoryName": name,
        }
        result: Any = await self._call_api(
            api="FileManagerPlugin/RenameDirectory", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def rename_file(self, file_path: str, file_name: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Changes the name of a file.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        file_name: :class:`str`
            The new name for the file; no path needed. (eg. "renamed_myfile.txt")
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Filename": self.sanitize_path(path=file_path), "NewFilename": file_name}
        result: Any = await self._call_api(
            api="FileManagerPlugin/RenameFile", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def trash_directory(self, file_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Moves a directory to the trash, directories must be trashed before they can be ``emptied``.

        .. note::
            See :meth:`FileManagerPlugin.empty_trash` to remove the files from the trash directory.


        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"DirectoryName": self.sanitize_path(path=file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/TrashDirectory", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def trash_file(self, file_path: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Moves a file to the trash, files must be trashed before they can be ``emptied``.

        .. note::
            See :meth:`FileManagerPlugin.empty_trash` to remove the files from the trash directory.


        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, str] = {"Filename": self.sanitize_path(path=file_path)}
        result: Any = await self._call_api(
            api="FileManagerPlugin/TrashFile", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def write_file_chunk(
        self, file_path: str, data: str, offset: int, append: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Write data to a file with an offset.

        Parameters
        -----------
        file_path: :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        data: :class:`str`
            The binary data to be written.
        index: :class:`int`
            The position offset from start of file.
        append: :class:`bool`
            Appends the data to the end of the file, default is False.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {
            "Filename": self.sanitize_path(path=file_path),
            "Data": data,
            "Offset": offset,
            "FinalChunk": append,
        }
        result: Any = await self._call_api(
            api="FileManagerPlugin/WriteFileChunk", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result
