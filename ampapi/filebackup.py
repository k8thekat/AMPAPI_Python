from __future__ import annotations

from typing import Any, Union

from .base import Base
from .dataclass import ActionResult, Backup, RunningTask
from .enums import *

__all__ = ("LocalFileBackupPlugin",)


class LocalFileBackupPlugin(Base):
    """
    Contains all Endpoints for `/API/LocalFileBackupPlugin/`.

    """

    async def delete_from_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete a backup from S3.

        Args:
        ---
            backup_id (str): The backup ID to delete.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: On success returns a ActionResult dataclass.
            * See `types.py -> ActionResult`
        """
        await self._connect()
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/DeleteFromS3", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def delete_local_backup(self, backup_id: str) -> None:
        """
        Delete a local backup.

        Args:
        ---
            backup_id (str): The backup ID to delete.

        Returns:
        ---
            None
        """
        await self._connect()
        parameters: dict[str, str] = {"BackupId": backup_id}
        await self._call_api(api="LocalFileBackupPlugin/DeleteLocalBackup", parameters=parameters)
        return

    async def download_from_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Download a backup from S3.


        Args:
        ---
            backup_id (str): The backup ID to download.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            RunningTask: Returns a RunningTask dataclass.
            * See `types.py -> RunningTask`
        """
        await self._connect()
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/DownloadFromS3", parameters=parameters, format_data=format_data, format_=RunningTask
        )
        return result

    async def get_backups(self, format_data: Union[bool, None] = None) -> list[Backup]:
        """
        Get a list of Backups.

        Returns:
        ---
            list[Backup]: List of backups.
            * See `types.py -> Backup`
        """
        await self._connect()
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/GetBackups", format_data=format_data, format_=Backup, _use_from_dict=False
        )
        return result

    async def refresh_backup_list(self) -> None:
        """
        Refresh the list of backups.

        Returns:
        ---
            None
        """
        await self._connect()
        await self._call_api(api="LocalFileBackupPlugin/RefreshBackupList")
        return

    async def restore_backup(
        self, backup_id: str, delete_existing_data: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """
        Restore a backup.

        Args:
        ---
            backup_id (str): The backup ID to restore.
            delete_existing_data (bool, optional): Delete the backup after restoring. Defaults to False.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult | str | dict[str, Any] | list | bool | int | None: On success returns a ActionResult dataclass.
            * See `types.py -> ActionResult`
        """
        await self._connect()
        parameters: dict[str, Any] = {"BackupId": backup_id, "DeleteExistingData": delete_existing_data}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/RestoreBackup", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def set_backup_sticky(self, backup_id: str, sticky: bool = False) -> None:
        """
        Set a backup as sticky.

        Args:
        ---
            backup_id (str): The backup ID to set as sticky.
            sticky (bool, optional): Set the backup as sticky. Defaults to False.

        Returns:
        ---
            None
        """
        await self._connect()
        parameters: dict[str, Any] = {"BackupId": backup_id, "Sticky": sticky}
        await self._call_api(api="LocalFileBackupPlugin/SetBackupSticky", parameters=parameters)
        return

    async def take_backup(
        self, title: str, description: str, sticky: bool = False, format_data: Union[bool, None] = None
    ) -> ActionResult:
        """
        Takes a backup of the AMP Server/Instance.

        Args:
        ---
            title (str): Title of the backup; aka `Name`
            description (str): Brief description of why or what the backup is for.
            sticky (bool, optional): Sticky backups won't be deleted to make room for automatic backups. Defaults to `False`.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: Results from the API call.
            * See `types.py -> ActionResult`
        """

        await self._connect()
        parameters: dict[str, Any] = {"Title": title, "Description": description, "Sticky": sticky}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/TakeBackup", parameters=parameters, format_data=format_data, format_=ActionResult
        )
        return result

    async def upload_to_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Upload a backup to S3.

        Args:
            backup_id (str): The backup ID to upload.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            RunningTask: Returns a RunningTask dataclass.
            * See `types.py -> RunningTask`
        """
        await self._connect()
        parameters: dict[str, str] = {"BackupId": backup_id}
        result: Any = await self._call_api(
            api="LocalFileBackupPlugin/UploadToS3", parameters=parameters, format_data=format_data, format_=RunningTask
        )
        return result
