from __future__ import annotations

from .base import Base
from .types import *

__all__ = ("EmailSenderPlugin",)


class EmailSenderPlugin(Base):
    """
    Contains the base functions for any `/API/EmailSenderPlugin/` AMP API endpoints.

    """

    # EmailSenderPlugin.TestSMTPSettings:({'Parameters': [], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def test_SMTP_settings(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Test SMTP Settings.

        Args:
        ---
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
        ---
            ActionResult: Results from the API call.
            * See `types.py -> ActionResult`

        """
        await self._connect()
        result = await self._call_api(api="EmailSenderPlugin/TestSMTPSettings", format_data=format_data)
        return ActionResult(**result)
