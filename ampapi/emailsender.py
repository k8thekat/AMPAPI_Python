from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, Unpack

from .base import Base, ResponseAliasFull, ResponseHandlerOptions
from .errors import AMPAPITypeError
from .modules import ActionResult

if TYPE_CHECKING:
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]

    from ._types import ActionResultResponse

__all__ = ("EmailSenderPlugin",)


class EmailSenderPlugin(Base):
    """Contains the functions for any ``/API/EmailSenderPlugin/`` API endpoints."""

    async def test_SMTP_settings(
        self,
        *,
        format_data: Union[bool, None] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResult | ActionResultResponse:
        """|coro|

        Test SMTP Settings.

        .. note::
            This is a development endpoint.

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
        :class:`ActionResult`
            On success returns an :class:`ActionResult` dataclass.

        """
        await self._reauth()
        result: ResponseAliasFull = await self._post(
            url="EmailSenderPlugin/TestSMTPSettings",
            request_params=request_params,
            **response_params,
        )
        if not isinstance(result, dict):
            raise AMPAPITypeError(end_point="EmailSenderPlugin/TestSMTPSettings", cur_type=result, expec_type=dict)
        if format_data is None:
            format_data = self.format_data
        if "status" not in result:
            raise AMPAPITypeError(end_point="EmailSenderPlugin/TestSMTPSettings", cur_type=result, expec_type=dict)
        if format_data is True:
            return ActionResult(**result)
        return result
