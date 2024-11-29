from typing import Union

from .base import Base
from .dataclass import ActionResult

__all__ = ("EmailSenderPlugin",)


class EmailSenderPlugin(Base):
    """
    Contains the functions for any ``/API/EmailSenderPlugin/`` API endpoints.

    """

    async def test_SMTP_settings(self, format_data: Union[bool, None] = None) -> ActionResult:
        """|coro|

        Test SMTP Settings.

        .. note::
            This is a development endpoint.

        Parameters
        -----------
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.
        """
        await self._connect()
        result = await self._call_api(api="EmailSenderPlugin/TestSMTPSettings", format_data=format_data)
        return ActionResult(**result)
