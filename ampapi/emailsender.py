from typing import Union

from .base import Base
from .dataclass import ActionResult
from .enums import *

__all__ = ("EmailSenderPlugin",)


class EmailSenderPlugin(Base):
    """
    Contains the base functions for any `/API/EmailSenderPlugin/` AMP API endpoints.

    """

    # EmailSenderPlugin.TestSMTPSettings:({'Parameters': [], 'ReturnTypeName': 'ActionResult', 'IsComplexType': True})
    async def test_SMTP_settings(self, format_data: Union[bool, None] = None) -> ActionResult:
        """
        Test SMTP Settings.

        Parameters
        ----------
        format_data : (Union[bool, None], optional)
            Format the JSON response data.  (Uses `FORMAT_DATA` global constant if None), Defaults to None.

        Returns
        -------
        ActionResult :
            Results from the API call. See -> :py:class:ActionResult

        """
        await self._connect()
        result = await self._call_api(api="EmailSenderPlugin/TestSMTPSettings", format_data=format_data)
        return ActionResult(**result)
