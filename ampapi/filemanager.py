"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMPAPI_Python.

AMPAPI_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMPAPI_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMPAPI_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union, Unpack

from ._types import ACTION_RESULT_EXCLUDED_KEYS, ACTION_RESULT_REQUIRED_KEYS, ActionResultResponse, is_response_type
from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPITypeError
from .modules import ActionResult, Directory, FileChunk, FolderUploadFile

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

    from ._types import DirectoryResponse, FileChunkResponse

__all__ = ("FileManagerPlugin",)


class FileManagerPlugin(Base):
    """Contains all functions for any ``/API/FileManagerPlugin/`` API endpoints.

    .. note::
        All file_path fields must include the path to the file and the file name.
        All paths are relative to the Server/Instance root that is making the API call.


    .. note::
        You do not need to include the "/" at the start of the path.
        All file_path fields are sanitized prior to making the API call. See :meth:`~Base.sanitize_path`


    .. note::
        "await Instance.copyFile("eula.txt", "test")" would move "./InstanceName/eula.txt"
        to "./InstanceName/test/eula.txt"



    """

    async def calculate_file_md5_sum(
        self,
        file_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Calculate the MD5 sum of a file.

        Endpoint: `FileManagerPlugin/CalculateFileMD5Sum`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"FilePath": self.sanitize_path(path=file_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/CalculateFileMD5Sum",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/CalculateFileMD5Sum", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/CalculateFileMD5Sum", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def change_exclusion(
        self,
        file_path: str,
        as_directory: bool,
        exclude: bool,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Change a file or directory to be excluded from backups.

        Endpoint: `FileManagerPlugin/ChangeExclusion`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        as_directory : :class:`bool`
            If file_path is a directory.
        exclude : :class:`bool`
            If file_path should be excluded from backups or not.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {
            "ModifyPath": self.sanitize_path(path=file_path),
            "AsDirectory": as_directory,
            "Exclude": exclude,
        }
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/ChangeExclusion",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/ChangeExclusion", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/ChangeExclusion", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def copy_file(
        self,
        file_path: str,
        destination_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Moves a file from the origin directory to the target_directory.

        Endpoint: `FileManagerPlugin/CopyFile`

        .. warning::
            Make sure to NOT INCLUDE the file name in the destionation_path parameter.


        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        destination_path : :class:`str`
            Similar to file_path; do not include the file name. (eg. "test")
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Origin": self.sanitize_path(file_path), "TargetDirectory": destination_path}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/CopyFile",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/CopyFile", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/CopyFile", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def create_archive(
        self,
        file_path: str,
        *,
        overwrite_existing: Union[bool, None] = None,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Create an archive file.

        Endpoint: `FileManagerPlugin/CreateArchive`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        overwrite_existing : Union[:class:`bool`, None], optional
            Overwrite an archive that already exists, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        # parameters: dict[str, str] = {"PathToArchive": self.sanitize_path(file_path)}
        # `OverwriteExisting` is a Boolean, so the values are no longer all strings.
        parameters: dict[str, Any] = {"PathToArchive": self.sanitize_path(file_path)}
        if overwrite_existing is not None:
            parameters["OverwriteExisting"] = overwrite_existing
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/CreateArchive",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/CreateArchive", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/CreateArchive", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def create_directory(
        self,
        file_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Creates a new directory. The parent directory must already exist.

        Endpoint: `FileManagerPlugin/CreateDirectory`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"NewPath": self.sanitize_path(file_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/CreateDirectory",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/CreateDirectory", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/CreateDirectory", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def download_file_from_url(
        self,
        source: str,
        file_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Download a file from a URL.

        Endpoint: `FileManagerPlugin/DownloadFileFromURL`

        Parameters
        ----------
        source : :class:`str`
            The URL to file.
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Source": source, "TargetDirectory": self.sanitize_path(file_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/DownloadFileFromURL",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/DownloadFileFromURL", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/DownloadFileFromURL", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def download_folder_as_zip(
        self,
        directory_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Download an entire folder as a zip archive.

        Endpoint: `FileManagerPlugin/DownloadFolderAsZip`

        .. note::
            Requires the ``FileManager.FileManager.DownloadFiles`` permission.


        Parameters
        ----------
        directory_path : :class:`str`
            Path to the folder; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"DirectoryPath": self.sanitize_path(directory_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/DownloadFolderAsZip",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/DownloadFolderAsZip", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/DownloadFolderAsZip", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def empty_trash(
        self,
        file_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Empties a trash bin for the AMP Server/Instance.

        Endpoint: `FileManagerPlugin/EmptyTrash`

        .. note::
            Typically the directory is called ``Trashed Files``, it is case sensitive and located in the Server/Instance root directory.


        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"TrashDirectoryName": self.sanitize_path(file_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/EmptyTrash",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/EmptyTrash", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/EmptyTrash", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def extract_archive(
        self,
        file_path: str,
        destination_path: Union[str, None] = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Extract an archive file.

        Endpoint: `FileManagerPlugin/ExtractArchive`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        destination_path : Union[:class:`str`, None], optional
            The path to extract the archive to; relative to the Server/Instance root. eg ``home/config``, defaults to None.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"ArchivePath": self.sanitize_path(file_path)}

        if destination_path is not None:
            parameters["DestinationPath"] = destination_path

        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/ExtractArchive",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/ExtractArchive", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/ExtractArchive", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def get_directory_listing(
        self,
        file_path: str = "",
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Directory] | list[DirectoryResponse]:
        """|coro|

        Returns a dictionary of the path's properties and the files contained in the directory and their properties.

        Endpoint: `FileManagerPlugin/GetDirectoryListing`

        .. note::
            If a file has a similar name it may return the file instead of the directory.


        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`Directory`]
            On success returns a list of :class:`Directory` dataclasses.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Dir": self.sanitize_path(file_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/GetDirectoryListing",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="FileManagerPlugin/GetDirectoryListing", cur_type=result, expec_type=list)
        if format_data is None:
            format_data = self.format_data
        if format_data is True:
            return [Directory.from_response(item) for item in result]
        return result

    async def get_file_chunk(
        self,
        file_path: str,
        index: int,
        length: int,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> FileChunk | FileChunkResponse:
        """|coro|

        Returns a specific section of Base64 data from the file.

        Endpoint: `FileManagerPlugin/GetFileChunk`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        index : :class:`int`
            The start position to read the file from, in bytes.
        length : :class:`int`
            How far to read from the index position, in bytes.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`FileChunk`
            On success returns a :class:`FileChunk` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"Filename": self.sanitize_path(file_path), "Position": index, "Length": length}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/GetFileChunk",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/GetFileChunk", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if "base64_data" not in result:
            raise AMPAPITypeError(end_point="FileManagerPlugin/GetFileChunk", cur_type=result, expec_type=dict)
        if format_data is True:
            return FileChunk.from_response(result)
        return result

    async def read_file_chunk(
        self,
        file_path: str,
        offset: int,
        chunk_size: Union[int, None] = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Read a chunk of data from a file.

        Endpoint: `FileManagerPlugin/ReadFileChunk`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        offset : :class:`int`
            The start position to read the file from, in bytes.
        chunk_size : Union[:class:`int`, None], optional
            How far to read from the offset position, in bytes.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"Filename": self.sanitize_path(file_path), "Offset": offset}
        if chunk_size is not None:
            parameters["ChunkSize"] = chunk_size

        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/ReadFileChunk",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/ReadFileChunk", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/ReadFileChunk", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def release_file_upload_lock(
        self,
        file_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Releases a File Upload Lock.

        Endpoint: `FileManagerPlugin/ReleaseFileUploadLock`

        .. note::
            AMP answers success whether or not a lock was held, or the file exists (measured on AMP-2.8.0.8).

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Filename": self.sanitize_path(file_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/ReleaseFileUploadLock",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/ReleaseFileUploadLock", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/ReleaseFileUploadLock", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def rename_directory(
        self,
        file_path: str,
        name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Rename a directory.

        Endpoint: `FileManagerPlugin/RenameDirectory`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the directory; relative to the Instance root. eg ``./InstanceName/``.
        name : :class:`str`
            The new name for the directory, do not include the path.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {
            "oldDirectory": self.sanitize_path(path=file_path),
            "newDirectoryName": name,
        }
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/RenameDirectory",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/RenameDirectory", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/RenameDirectory", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def rename_file(
        self,
        file_path: str,
        file_name: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Changes the name of a file.

        Endpoint: `FileManagerPlugin/RenameFile`

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        file_name : :class:`str`
            The new name for the file; no path needed. (eg. "renamed_myfile.txt")
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Filename": self.sanitize_path(path=file_path), "NewFilename": file_name}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/RenameFile",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/RenameFile", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/RenameFile", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def trash_directory(
        self,
        file_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Moves a directory to the trash, directories must be trashed before they can be `emptied`.

        Endpoint: `FileManagerPlugin/TrashDirectory`

        .. note::
            See :meth:`FileManagerPlugin.empty_trash` to remove the files from the trash directory.


        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"DirectoryName": self.sanitize_path(path=file_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/TrashDirectory",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/TrashDirectory", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/TrashDirectory", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def trash_file(
        self,
        file_path: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Moves a file to the trash, files must be trashed before they can be `emptied`.

        Endpoint: `FileManagerPlugin/TrashFile`

        .. note::
            See :meth:`FileManagerPlugin.empty_trash` to remove the files from the trash directory.


        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"Filename": self.sanitize_path(path=file_path)}
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/TrashFile",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/TrashFile", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/TrashFile", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def write_file_chunk(
        self,
        file_path: str,
        data: str,
        offset: int,
        final_chunk: bool = False,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Write data to a file with an offset.

        Endpoint: `FileManagerPlugin/WriteFileChunk`

        .. versionchanged:: 5.0.0
            `append` is renamed `final_chunk`. It was always sent as AMP's `FinalChunk`, which marks the last chunk.

        Parameters
        ----------
        file_path : :class:`str`
            Path to the file; relative to the Instance root. eg ``./InstanceName/``.
        data : :class:`str`
            The base64 encoding of the bytes to be written.
        offset : :class:`int`
            The position offset from start of file.
        final_chunk : :class:`bool`, optional
            If this is the last chunk of the file or not, by default False.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {
            "Filename": self.sanitize_path(path=file_path),
            "Data": data,
            "Offset": offset,
            "FinalChunk": final_chunk,
        }
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/WriteFileChunk",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/WriteFileChunk", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/WriteFileChunk", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def upload_folder(
        self,
        target_directory: str,
        files: list[FolderUploadFile],
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Upload an entire folder as a set of files with relative paths.

        Endpoint: `FileManagerPlugin/UploadFolder`

        .. note::
            The `target_directory` must already exist, AMP answers "The specified directory does not exist" otherwise.
            Subfolders in a file's `relative_path` are created.


        .. note::
            Requires the ``FileManager.FileManager.UploadFiles`` permission.


        Parameters
        ----------
        target_directory : :class:`str`
            Path to the folder the files are uploaded into; relative to the Instance root. eg ``./InstanceName/``.
        files : list[:class:`FolderUploadFile`]
            The files to upload, each one's content is sent as base64.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.

        """
        await self._reauth()
        parameters: dict[str, Any] = {
            "TargetDirectory": self.sanitize_path(target_directory),
            "Files": [file.to_dict() for file in files],
        }
        result: ResponseAliasFull = await self._post(
            url="FileManagerPlugin/UploadFolder",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="FileManagerPlugin/UploadFolder", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="FileManagerPlugin/UploadFolder", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result
