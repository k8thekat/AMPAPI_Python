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

from ._types import (
    ACTION_RESULT_EXCLUDED_KEYS,
    ACTION_RESULT_REQUIRED_KEYS,
    BACKUP_EXCLUDED_KEYS,
    BACKUP_REQUIRED_KEYS,
    RUNNING_TASK_EXCLUDED_KEYS,
    RUNNING_TASK_REQUIRED_KEYS,
    ActionResultResponse,
    BackupResponse,
    RunningTaskResponse,
    is_response_type,
)
from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPITypeError
from .modules import ActionResult, Backup, RunningTask

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

__all__ = ("LocalFileBackupPlugin",)


class LocalFileBackupPlugin(Base):
    """Contains all functions for any ``/API/LocalFileBackupPlugin/`` API endpoints."""

    async def backup_will_stop_server(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> bool:
        """|coro|

        Check if taking a backup will stop the Instance.

        Endpoint: `LocalFileBackupPlugin/BackupWillStopServer`

        .. note::
            Requires the ``LocalFileBackup.Backup.ViewBackupsList`` permission.


        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`bool`
            On success returns True if a backup will stop the Instance, otherwise False.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/BackupWillStopServer",
            request_params=request_params,
            **response_params,
        )
        if isinstance(result, bool):
            return result
        raise AMPAPITypeError(end_point="LocalFileBackupPlugin/BackupWillStopServer", cur_type=result, expec_type=bool)

    async def delete_from_s3(
        self,
        backup_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete a backup from S3.

        Endpoint: `LocalFileBackupPlugin/DeleteFromS3`

        Parameters
        ----------
        backup_id : :class:`str`
            The backup ID to delete.
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
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/DeleteFromS3",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/DeleteFromS3", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/DeleteFromS3", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def delete_local_backup(
        self,
        backup_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Delete a local backup.

        Endpoint: `LocalFileBackupPlugin/DeleteLocalBackup`

        .. versionchanged:: 5.0.0
            Returns an :class:`ActionResult` and takes `format_data`.

        Parameters
        ----------
        backup_id : :class:`str`
            The backup ID to delete.
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
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/DeleteLocalBackup",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/DeleteLocalBackup", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/DeleteLocalBackup", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def download_from_s3(
        self,
        backup_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Download a backup from S3.

        Endpoint: `LocalFileBackupPlugin/DownloadFromS3`


        Parameters
        ----------
        backup_id : :class:`str`
            The backup ID to download.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/DownloadFromS3",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/DownloadFromS3", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if "is_primary_task" not in result:
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/DownloadFromS3", cur_type=result, expec_type=dict)
        if format_data is True:
            return RunningTask.from_response(result)
        return result

    async def get_backups(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Backup] | list[BackupResponse]:
        """|coro|

        Get a list of Backups.

        Endpoint: `LocalFileBackupPlugin/GetBackups`

        Parameters
        ----------
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        list[:class:`Backup`] | list[:class:`BackupResponse`]
            On success returns a list of :class:`Backup` dataclasses, or the raw dictionaries when `format_data` is False.

        Raises
        ------
        :exc:`AMPAPITypeError`
            If AMP did not answer with a list of Backups.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/GetBackups",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, list):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/GetBackups", cur_type=result, expec_type=list)

        if format_data is None:
            format_data = self.format_data

        backups: list[BackupResponse] = []
        for item in result:
            if not is_response_type(item, BackupResponse, BACKUP_REQUIRED_KEYS, BACKUP_EXCLUDED_KEYS):
                raise AMPAPITypeError(end_point="LocalFileBackupPlugin/GetBackups", cur_type=item, expec_type=dict)
            backups.append(item)
        if format_data is True:
            return [Backup.from_response(backup) for backup in backups]
        return backups

    async def refresh_backup_list(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Refresh the list of backups.

        Endpoint: `LocalFileBackupPlugin/RefreshBackupList`

        Parameters
        ----------
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        return await self._post(
            url="LocalFileBackupPlugin/RefreshBackupList",
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    async def restore_backup(
        self,
        backup_id: str,
        delete_existing_data: bool = False,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Restore a backup.

        Endpoint: `LocalFileBackupPlugin/RestoreBackup`

        Parameters
        ----------
        backup_id : :class:`str`
            The backup ID to restore.
        delete_existing_data : :class:`bool`, optional
            Delete the backup after restoring, defaults to False.
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
        parameters: dict[str, Any] = {"BackupId": backup_id, "DeleteExistingData": delete_existing_data}
        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/RestoreBackup",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/RestoreBackup", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/RestoreBackup", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def set_backup_sticky(
        self,
        backup_id: str,
        sticky: bool = False,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Set a backup as sticky.

        Endpoint: `LocalFileBackupPlugin/SetBackupSticky`

        .. versionchanged:: 5.0.0
            Returns an :class:`ActionResult` and takes `format_data`.

        Parameters
        ----------
        backup_id : :class:`str`
            The backup ID to set as sticky.
        sticky : :class:`bool`, optional
            Set the backup as sticky, defaults to False.
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
        parameters: dict[str, Any] = {"BackupId": backup_id, "Sticky": sticky}
        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/SetBackupSticky",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )

        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/SetBackupSticky", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if not is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/SetBackupSticky", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult.from_response(result)
        return result

    async def take_backup(
        self,
        name: str,
        description: str,
        sticky: bool = False,
        local: bool | None = None,
        s3: bool | None = None,
        *,
        was_created_automatically: Union[bool, None] = None,
        dirty_only: Union[bool, None] = None,
        backup_while_running: Union[bool, None] = None,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse | ActionResult | ActionResultResponse:
        """|coro|

        Takes a backup of the AMP Server.

        Endpoint: `LocalFileBackupPlugin/TakeBackup`

        .. versionchanged:: 5.0.0
            Returns a :class:`RunningTask`, not an :class:`ActionResult`.

        Parameters
        ----------
        name : :class:`str`
            The name of the backup.
        description : :class:`str`
            Brief description of why or what the backup is for.
        sticky : :class:`bool`, optional
            Sticky backups won't be deleted to make room for automatic backups, defaults to `False`.
        local : :class:`bool`, optional
            If the backup should be local or not.
        s3 : :class:`bool`, optional
            If the backup should be on S3 or not.
        was_created_automatically : Union[:class:`bool`, None], optional
            Mark the backup as one AMP created automatically, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
        dirty_only : Union[:class:`bool`, None], optional
            Back up only if files changed since the last backup, by default None, which leaves AMP's default. When
            nothing changed, AMP takes no backup and answers an :class:`ActionResult`.

            .. versionadded:: 5.0.0
        backup_while_running : Union[:class:`bool`, None], optional
            Take the backup while the Instance is running, by default None, which leaves AMP's default.

            .. versionadded:: 5.0.0
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask` | :class:`RunningTaskResponse` | :class:`ActionResult` | :class:`ActionResultResponse`
            On success returns a :class:`RunningTask` dataclass, unless format_data is False which returns the raw dict.
            With `dirty_only` True and no file changed, AMP takes no backup and answers an :class:`ActionResult`.

        """
        await self._reauth()
        parameters: dict[str, Any] = {"Title": name, "Description": description, "Sticky": sticky}
        if local is not None:
            parameters["Local"] = local
        if s3 is not None:
            parameters["S3"] = s3
        if was_created_automatically is not None:
            parameters["WasCreatedAutomatically"] = was_created_automatically
        if dirty_only is not None:
            parameters["DirtyOnly"] = dirty_only
        if backup_while_running is not None:
            parameters["BackupWhileRunning"] = backup_while_running

        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/TakeBackup",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/TakeBackup", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        # if not is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
        #     raise AMPAPITypeError(end_point="LocalFileBackupPlugin/TakeBackup", cur_type=result, expec_type=dict)
        # if format_data is True:
        #     return RunningTask.from_response(result)
        # return result

        # A running task carries the ActionResult keys too, so it is checked first.
        if is_response_type(result, RunningTaskResponse, RUNNING_TASK_REQUIRED_KEYS, RUNNING_TASK_EXCLUDED_KEYS):
            if format_data is True:
                return RunningTask.from_response(result)
            return result

        # With `DirtyOnly` and nothing changed, AMP takes no backup and answers an ActionResult (vm1, 2026-10-24).
        if is_response_type(result, ActionResultResponse, ACTION_RESULT_REQUIRED_KEYS, ACTION_RESULT_EXCLUDED_KEYS):
            if format_data is True:
                return ActionResult.from_response(result)
            return result
        raise AMPAPITypeError(end_point="LocalFileBackupPlugin/TakeBackup", cur_type=result, expec_type=dict)

    async def upload_to_s3(
        self,
        backup_id: str,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> RunningTask | RunningTaskResponse:
        """|coro|

        Upload a backup to S3.

        Endpoint: `LocalFileBackupPlugin/UploadToS3`

        Parameters
        ----------
        backup_id : :class:`str`
            The backup ID to upload.
        format_data : Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.

        """
        await self._reauth()
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: ResponseAliasFull = await self._post(
            url="LocalFileBackupPlugin/UploadToS3",
            parameters=parameters,
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/UploadToS3", cur_type=result, expec_type=dict)

        if format_data is None:
            format_data = self.format_data

        if "is_primary_task" not in result:
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/UploadToS3", cur_type=result, expec_type=dict)
        if format_data is True:
            return RunningTask.from_response(result)
        return result
