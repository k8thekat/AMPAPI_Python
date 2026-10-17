from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union, Unpack

from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPITypeError
from .modules import ActionResult, Backup, RunningTask

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

    from ._types import ActionResultResponse, RunningTaskResponse

__all__ = ("LocalFileBackupPlugin",)


class LocalFileBackupPlugin(Base):
    """Contains all functions for any ``/API/LocalFileBackupPlugin/`` API endpoints.

    """

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
        if "status" not in result:
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/DeleteFromS3", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult(**result)
        return result

    async def delete_local_backup(
        self,
        backup_id: str,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Delete a local backup.

        Parameters
        ----------
        backup_id : :class:`str`
            The backup ID to delete.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, str] = {"BackupId": backup_id}
        return await self._post(
            url="LocalFileBackupPlugin/DeleteLocalBackup",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

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
            return RunningTask(**result)
        return result

    async def get_backups(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> list[Backup] | list[dict[str, Any]]:
        """|coro|

        Get a list of Backups.

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
        list[:class:`Backup`]
            On success returns a list of :class:`Backup` dataclasses.

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
        if format_data is True:
            return [Backup(**item) for item in result]
        return result

    async def refresh_backup_list(
        self,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Refresh the list of backups.

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
        if "status" not in result:
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/RestoreBackup", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult(**result)
        return result

    async def set_backup_sticky(
        self,
        backup_id: str,
        sticky: bool = False,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None:
        """|coro|

        Set a backup as sticky.

        Parameters
        ----------
        backup_id : :class:`str`
            The backup ID to set as sticky.
        sticky : :class:`bool`, optional
            Set the backup as sticky, defaults to False.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        None

        """
        await self._reauth()
        parameters: dict[str, Any] = {"BackupId": backup_id, "Sticky": sticky}
        return await self._post(
            url="LocalFileBackupPlugin/SetBackupSticky",
            parameters=parameters,
            no_data=True,
            request_params=request_params,
            **response_params,
        )

    async def take_backup(
        self,
        name: str,
        description: str,
        sticky: bool = False,
        local: bool | None = None,
        s3: bool | None = None,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Takes a backup of the AMP Server.

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
        parameters: dict[str, Any] = {"Title": name, "Description": description, "Sticky": sticky}
        if local is not None:
            parameters["Local"] = local
        if s3 is not None:
            parameters["S3"] = s3

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
        if "status" not in result:
            raise AMPAPITypeError(end_point="LocalFileBackupPlugin/TakeBackup", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult(**result)
        return result

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
            return RunningTask(**result)
        return result
