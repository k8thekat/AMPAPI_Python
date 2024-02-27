from __future__ import annotations
from typing import Union

from .types import *
from .base import Base

__all__ = ("LocalFileBackupPlugin",)


class LocalFileBackupPlugin(Base):
    """
    Contains the base functions for any `/API/LocalFileBackupPlugin/` AMP API endpoints.

    """
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
