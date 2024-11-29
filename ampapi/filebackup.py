from __future__ import annotations

from typing import Any, Union

from .base import Base
from .dataclass import ActionResult, Backup, RunningTask

__all__ = ("LocalFileBackupPlugin",)


class LocalFileBackupPlugin(Base):
    """
    Contains all functions for any ``/API/LocalFileBackupPlugin/`` API endpoints.

    """

    async def delete_from_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Delete a backup from S3.

        Parameters
        -----------
        backup_id: :class:`str`
            The backup ID to delete.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/DeleteFromS3", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def delete_local_backup(self, backup_id: str) -> None:
        """|coro|

        Delete a local backup.

        Parameters
        -----------
        backup_id: :class:`str`
            The backup ID to delete.

        Returns
        --------
        None
        """
        await self._connect()
        parameters: dict[str, str] = {"BackupId": backup_id}
        await self._call_api(api="LocalFileBackupPlugin/DeleteLocalBackup", parameters=parameters, _no_data=True)
        return

    async def download_from_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> RunningTask:
        """|coro|

        Download a backup from S3.


        Parameters
        -----------
        backup_id: :class:`str`
            The backup ID to download.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/DownloadFromS3", parameters=parameters, format_data=format_data, format_=RunningTask
        )
        return result

    async def get_backups(self, format_data: Union[bool, None] = None) -> list[Backup]:
        """|coro|

        Get a list of Backups.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        list[:class:`Backup`]
            On success returns a list of :class:`Backup` dataclasses.
        """
        await self._connect()
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/GetBackups", format_data=format_data, format_=Backup, _use_from_dict=False
        )
        return result

    async def refresh_backup_list(self) -> None:
        """|coro|

        Refresh the list of backups.

        Returns
        --------
        None
        """
        await self._connect()
        await self._call_api(api="LocalFileBackupPlugin/RefreshBackupList", _no_data=True)
        return

    async def restore_backup(
        self, backup_id: str, delete_existing_data: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Restore a backup.

        Parameters
        -----------
        backup_id: :class:`str`
            The backup ID to restore.
        delete_existing_data: :class:`bool`, optional
            Delete the backup after restoring, defaults to False.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """
        await self._connect()
        parameters: dict[str, Any] = {"BackupId": backup_id, "DeleteExistingData": delete_existing_data}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/RestoreBackup", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def set_backup_sticky(self, backup_id: str, sticky: bool = False) -> None:
        """|coro|

        Set a backup as sticky.

        Parameters
        -----------
        backup_id: :class:`str`
            The backup ID to set as sticky.
        sticky: :class:`bool`, optional
            Set the backup as sticky, defaults to False.

        Returns
        --------
        None
        """
        await self._connect()
        parameters: dict[str, Any] = {"BackupId": backup_id, "Sticky": sticky}
        await self._call_api(api="LocalFileBackupPlugin/SetBackupSticky", parameters=parameters, _no_data=True)
        return

    async def take_backup(
        self, name: str, description: str, sticky: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """|coro|

        Takes a backup of the AMP Server.

        Parameters
        -----------
        name: :class:`str`
            The name of the backup.
        description: :class:`str`
            Brief description of why or what the backup is for.
        sticky: :class:`bool`, optional
            Sticky backups won't be deleted to make room for automatic backups, defaults to ``False``.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns a :class:`ActionResult` dataclass.
        """

        await self._connect()
        parameters: dict[str, Any] = {"Title": name, "Description": description, "Sticky": sticky}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/TakeBackup", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def upload_to_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> RunningTask:
        """|coro|

        Upload a backup to S3.

        Parameters
        -----------
        backup_id: :class:`str`
            The backup ID to upload.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`RunningTask`
            On success returns a :class:`RunningTask` dataclass.
        """
        await self._connect()
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/UploadToS3", parameters=parameters, format_data=format_data, format_=RunningTask
        )
        return result
