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
from typing import TYPE_CHECKING, Any, ClassVar, Optional

from .errors import AMPAPIRequestError

if TYPE_CHECKING:
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

    async def _request(
        self,
        method: str,
        path: str,
        *,
        data: Optional[dict[str, Any]] = None,
        parameters: Optional[QueryParameters] = None,
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
        data : Union[dict[:class:`str`, Any], None], optional
            The JSON body, by default None.
        parameters : Union[:class:`QueryParameters`, None], optional
            The query string, by default None.
            A list value repeats its key, eg. ``{"shard": ["a", "b"]}`` is sent as ``shard=a&shard=b``.
        use_token : :class:`bool`, optional
            If the call needs a session or not, by default True.
            Without one we don't log in or send a token, eg. for ``GET /api/health/status``.

        Returns
        -------
        Any
            The decoded JSON body, `None` for an empty one (a 204).

        Raises
        ------
        AMPAPIRequestError
            If AMP answers with an error status, or is still down after the last delay.

        """
        # TODO: Raw byte and text replies, for the file and snapshot downloads (#47.7).
        # `Session._send` only decodes JSON for now.
        for delay in self._outage_delays:
            try:
                return await self.session._request(  # pyright: ignore[reportPrivateUsage]
                    method=method,
                    path=path,
                    data=data,
                    parameters=parameters,
                    use_token=use_token,
                )
            except AMPAPIRequestError as error:
                if error.status != 503 or error.code not in self._outage_codes:
                    raise
                LOGGER.warning(
                    "<%s.%s> | AMP is unavailable, trying again in %s seconds | Code: %s | Path: %s",
                    __class__.__name__,
                    "_request",
                    delay,
                    error.code,
                    path,
                )
                await asyncio.sleep(delay=delay)

        # AMP is still down after the last delay, so this try's error goes to the caller.
        return await self.session._request(  # pyright: ignore[reportPrivateUsage]
            method=method,
            path=path,
            data=data,
            parameters=parameters,
            use_token=use_token,
        )
