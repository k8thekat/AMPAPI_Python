from __future__ import annotations
from typing import Union

from .types import *
from .base import Base

__all__ = ("LocalFileBackupPlugin",)


class LocalFileBackupPlugin(Base):
    """
    Contains the base functions for any `/API/LocalFileBackupPlugin/` AMP API endpoints.

    """
    # LocalFileBackupPlugin.TakeBackup:({'Parameters': [{'Name': 'Title', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Description', 'TypeName': 'String', 'Description': '', 'Optional': False}, {'Name': 'Sticky', 'TypeName': 'Boolean', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def take_backup(self, title: str, description: str, sticky: bool = False) -> ActionResult | str | dict[str, Any] | list | bool | int | None:
        """
        Takes a backup of the AMP Server/Instance.

        Args:
            title (str): Title of the backup; aka `Name`
            description (str): Brief description of why or what the backup is for.
            sticky (bool, optional): Sticky backups won't be deleted to make room for automatic backups. Defaults to `False`.

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: Results from the API call. 
                See `types.py -> ActionResult`
        """

        await self._connect()
        parameters = {
            "Title": title,
            "Description": description,
            "Sticky": sticky
        }
        result = await self._call_api('LocalFileBackupPlugin/TakeBackup', parameters)
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    # LocalFileBackupPlugin.UploadToS3:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    async def upload_to_s3(self, backup_id: str) -> str | dict[str, Any] | list | bool | int | None:
        """
        Upload a backup to S3.

        Args:
            backup_id (str): The backup ID to upload.

        Returns:
            str | dict[str, Any] | list | bool | int | None: #TODO See what this returns.
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id
        }
        result = await self._call_api('LocalFileBackupPlugin/UploadToS3', parameters)
        if isinstance(result, dict):
            return result
        return result

    # LocalFileBackupPlugin.DownloadFromS3:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'RunningTask', 'IsComplexType': True})
    async def download_from_s3(self, backup_id: str) -> str | dict[str, Any] | list | bool | int | None:
        """
        Download a backup from S3.

        Args:
            backup_id (str): The backup ID to download.

        Returns:
            str | dict[str, Any] | list | bool | int | None: #TODO See what this returns.
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id
        }
        result = await self._call_api('LocalFileBackupPlugin/DownloadFromS3', parameters)
        if isinstance(result, dict):
            return result
        return result

    # LocalFileBackupPlugin.DeleteFromS3:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def delete_from_s3(self, backup_id: str) -> ActionResult | str | dict[str, Any] | list | bool | int | None:
        """
        Delete a backup from S3.

        Args:
            backup_id (str): The backup ID to delete.

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id
        }
        result = await self._call_api('LocalFileBackupPlugin/DeleteFromS3', parameters)
        if isinstance(result, dict):
            return ActionResult(**result)
        return result

    # LocalFileBackupPlugin.GetBackups:({'Parameters': [], 'ReturnTypeName': 'IEnumerable<JObject>', 'IsComplexType': True})
    async def get_backups(self) -> list | str | dict[str, Any] | bool | int | None:
        """
        Get a list of Backups.

        Returns:
            list | dict[str, Any] | bool | int | None: List of backups.
        """
        await self._connect()
        result = await self._call_api('LocalFileBackupPlugin/GetBackups')
        if isinstance(result, list):
            return result
        return result

    # LocalFileBackupPlugin.RestoreBackup:({'Parameters': [{'Name': 'BackupId', 'TypeName': 'Guid', 'Description': '', 'Optional': False}, {'Name': 'DeleteExistingData', 'TypeName': 'Boolean', 'Description': '', 'Optional': True}], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def restore_backup(self, backup_id: str, delete_existing_data: bool = False) -> ActionResult | str | dict[str, Any] | list | bool | int | None:
        """
        Restore a backup.

        Args:
            backup_id (str): The backup ID to restore.
            delete_existing_data (bool, optional): Delete the backup after restoring. Defaults to False.

        Returns:
            ActionResult | str | dict[str, Any] | list | bool | int | None: On success returns a ActionResult dataclass.
                See `types.py -> ActionResult`
        """
        await self._connect()
        parameters = {
            "BackupId": backup_id,
            "DeleteExistingData": delete_existing_data
        }
        result = await self._call_api('LocalFileBackupPlugin/RestoreBackup', parameters)
        if isinstance(result, dict):
            return ActionResult(**result)
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
        await self._call_api('LocalFileBackupPlugin/DeleteLocalBackup', parameters)
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
        await self._call_api('LocalFileBackupPlugin/SetBackupSticky', parameters)
        return
