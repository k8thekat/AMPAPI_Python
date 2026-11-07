"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMPAPI_Python.

AMPAPI_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMPAPI_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMPAPI_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

from __future__ import annotations

import asyncio
import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

from .errors import (
    AMPAPIRequestError,
    _is_json_object,  # pyright: ignore[reportPrivateUsage]
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ._types import QueryParameters
    from .session import Session

__all__ = ("Base",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Base:
    """The root of every `...Module` mixin, holding the :class:`Session` their calls go through.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session to send calls through. It logs in on the first call that needs it.

    """

    session: Session
    # The web panel tries a 503 again after each of these delays (in seconds) when AMP names one of these outages.
    _outage_codes: ClassVar[tuple[str, ...]] = ("session.storeUnavailable", "common.error.busUnavailable")
    _outage_delays: ClassVar[tuple[int, ...]] = (1, 2, 4, 8, 8)

    def __init__(self, session: Session) -> None:  # noqa: D107
        self.session = session

    @staticmethod
    def _to_enum[E: Enum, V: (int, str)](enum: type[E], value: V) -> Union[E, V]:
        """`value` as a member of `enum`, or the plain number or name when AMP sent one the library doesn't know yet."""
        try:
            return enum(value)
        except ValueError:
            return value

    async def _request(
        self,
        method: str,
        path: str,
        *,
        data: Optional[Union[dict[str, Any], list[Any], bytes]] = None,
        files: Optional[Mapping[str, bytes]] = None,
        parameters: Optional[QueryParameters] = None,
        raw_bytes: bool = False,
        use_token: bool = True,
    ) -> Any:
        """Send a call through our :class:`Session`, waiting out a panel outage the way the web panel does.

        A 503 whose `code` says AMP's database (``"session.storeUnavailable"``) or message bus
        (``"common.error.busUnavailable"``) is down is sent again after 1, 2, 4, 8 and 8 seconds.

        Parameters
        ----------
        method : :class:`str`
            The HTTP method, eg. ``"GET"``.
        path : :class:`str`
            The path, eg. ``"/api/licence"``.
        data : Union[dict[:class:`str`, Any], list[Any], :class:`bytes`, None], optional
            The JSON body, by default None. A few calls take a list.
            Bytes are sent as they are, with ``Content-Type: application/octet-stream``.
        files : Union[Mapping[:class:`str`, :class:`bytes`], None], optional
            Files to send as the web panel's upload form, each relative path to its content, by default None.
        parameters : Union[:class:`QueryParameters`, None], optional
            The query string, by default None.
            A list value repeats its key, eg. ``{"shard": ["a", "b"]}`` is sent as ``shard=a&shard=b``.
        raw_bytes : :class:`bool`, optional
            If a successful reply should come back as bytes rather than JSON or not, by default False.
            Downloads need it. An error is still read as JSON.
        use_token : :class:`bool`, optional
            If the call needs a session or not, by default True.
            Without one we don't log in or send a token, eg. for ``GET /api/health/status``.

        Returns
        -------
        Any
            The decoded JSON body, `None` for an empty one (a 204), or the bytes with `raw_bytes`.

        Raises
        ------
        AMPAPIRequestError
            If AMP answers with an error status, or is still down after the last delay.
            A login this call needs is not retried; a 503 there raises at once.

        """
        status, body = await self.session._send_with_login(  # pyright: ignore[reportPrivateUsage]
            method=method,
            path=path,
            data=data,
            files=files,
            parameters=parameters,
            raw_bytes=raw_bytes,
            use_token=use_token,
        )
        # We check the reply before building an error, so a retried outage only logs our warning.
        for delay in self._outage_delays:
            code: Optional[str] = body.get("code") if _is_json_object(value=body) else None
            if status != 503 or code not in self._outage_codes:
                break

            LOGGER.warning(
                "<%s.%s> | AMP is unavailable, trying again in %s seconds | Code: %s | Path: %s",
                __class__.__name__,
                "_request",
                delay,
                code,
                path,
            )
            await asyncio.sleep(delay=delay)
            status, body = await self.session._send_with_login(  # pyright: ignore[reportPrivateUsage]
                method=method,
                path=path,
                data=data,
                files=files,
                parameters=parameters,
                raw_bytes=raw_bytes,
                use_token=use_token,
            )

        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method=method, path=path, data=body)
        return body
