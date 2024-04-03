from __future__ import annotations

from typing import Union

from .base import Base
from .types import *

__all__ = ("LocalFileBackupPlugin",)


class LocalFileBackupPlugin(Base):
    """
    Contains the base functions for any `/API/LocalFileBackupPlugin/` AMP API endpoints.

    """
    # LocalFileBackupPlugin.TakeBackup:({'Parameters': [{'Name': 'Title', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Sticky', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def take_backup(self, title: str, description: str, sticky: bool = False, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Takes a backup of the AMP Server/Instance.

        Args:
            title (str): Title of the backup; aka `Name`
            description (str): Brief description of why or what the backup is for.
            sticky (bool, optional): Sticky backups won't be deleted to make room for automatic backups. Defaults to `False`.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: Results from the API call. 
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Title": title,
            "Description": description,
            "Sticky": sticky
        }
        result = await self._call_api(api='LocalFileBackupPlugin/TakeBackup', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # LocalFileBackupPlugin.UploadToS3:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    async def upload_to_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Upload a backup to S3.

        Args:
            backup_id (str): The backup ID to upload.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            RunningTask: Returns a RunningTask dataclass.
                See `types.py -> RunningTask` 
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id
        }
        result = await self._call_api(api='LocalFileBackupPlugin/UploadToS3', parameters=parameters, format_data=format_data, format=RunningTask)
        return result

    # LocalFileBackupPlugin.DownloadFromS3:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    async def download_from_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> RunningTask:
        """
        Download a backup from S3.


        Args:
            backup_id (str): The backup ID to download.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            RunningTask: Returns a RunningTask dataclass.
                See `types.py -> RunningTask`
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id
        }
        result = await self._call_api(api='LocalFileBackupPlugin/DownloadFromS3', parameters=parameters, format_data=format_data, format=RunningTask)
        return result

    # LocalFileBackupPlugin.DeleteFromS3:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def delete_from_s3(self, backup_id: str, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Delete a backup from S3.

        Args:
            backup_id (str): The backup ID to delete.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id
        }
        result = await self._call_api(api='LocalFileBackupPlugin/DeleteFromS3', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # LocalFileBackupPlugin.GetBackups:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    async def get_backups(self, format_data: Union[bool, None] = None) -> list[Backup]:
        """
        Get a list of Backups.

        Returns:
            list[Backup]: List of backups.
                See `types.py -> Backup`
        """
        await self._connect()
        result = await self._call_api(api='LocalFileBackupPlugin/GetBackups', format_data=format_data, format=Backup, _use_from_dict=False)
        return result

    # LocalFileBackupPlugin.RestoreBackup:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'DeleteExistingData', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def restore_backup(self, backup_id: str, delete_existing_data: bool = False, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Restore a backup.

        Args:
            backup_id (str): The backup ID to restore.
            delete_existing_data (bool, optional): Delete the backup after restoring. Defaults to False.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id,
            "DeleteExistingData": delete_existing_data
        }
        result = await self._call_api(api='LocalFileBackupPlugin/RestoreBackup', parameters=parameters, format_data=format_data, format=ActionResult)
        return result

    # LocalFileBackupPlugin.DeleteLocalBackup:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def delete_local_backup(self, backup_id: str) -> None:
        """
        Delete a local backup.

        Args:
            backup_id (str): The backup ID to delete.

        Returns:
            None
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id
        }
        await self._call_api(api='LocalFileBackupPlugin/DeleteLocalBackup', parameters=parameters)
        return

    # LocalFileBackupPlugin.SetBackupSticky:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'Sticky', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'Void', 'IsComplexType': False})
    async def set_backup_sticky(self, backup_id: str, sticky: bool = False) -> None:
        """
        Set a backup as sticky.

        Args:
            backup_id (str): The backup ID to set as sticky.
            sticky (bool, optional): Set the backup as sticky. Defaults to False.

        Returns:
            None
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id,
            "Sticky": sticky
        }
        await self._call_api(api='LocalFileBackupPlugin/SetBackupSticky', parameters=parameters)
        return
