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

import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Union

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

    def __init__(self, session: Session) -> None:  # noqa: D107
        self.session = session

    @staticmethod
    def _to_enum[E: Enum, V: (int, str)](enum: type[E], value: V) -> Union[E, V]:
        """`value` as a member of `enum`, or the plain number or name when AMP sent one the library doesn't know yet."""
        try:
            return enum(value)
        except ValueError:
            return value

    @staticmethod
    def _without_none[V](mapping: Mapping[str, Optional[V]]) -> dict[str, V]:
        """`mapping` without its `None` values, for a body or query where AMP keeps whatever is left out."""
        return {key: value for key, value in mapping.items() if value is not None}

    @staticmethod
    def _key_name(name: str) -> str:
        """The camelCase key AMP reads for a snake_case name, eg. ``"memory_limit_mb"`` becomes ``"memoryLimitMb"``.

        It turns `AMPObject`'s attribute names back, where each word after the first starts with a capital, as in every
        infra setting and preference key.
        """
        words: list[str] = name.removesuffix("_").split("_")
        return words[0] + "".join(word.capitalize() for word in words[1:])

    async def _request(
        self,
        method: str,
        path: str,
        *,
        data: Optional[Union[Mapping[str, Any], list[Any], bytes]] = None,
        files: Optional[Mapping[str, bytes]] = None,
        parameters: Optional[QueryParameters] = None,
        raw_bytes: bool = False,
        use_token: bool = True,
        setup_code: Optional[str] = None,
    ) -> Any:
        """Send a call through our :class:`Session`, raising for an error status.

        The session logs in when the call needs it, and waits out a panel outage the way the web panel does: a 503
        whose `code` says AMP's database (``"session.storeUnavailable"``) or message bus
        (``"common.error.busUnavailable"``) is down is sent again after 1, 2 and 4 seconds, then 8 seconds twice.

        Parameters
        ----------
        method : :class:`str`
            The HTTP method, eg. ``"GET"``.
        path : :class:`str`
            The path, eg. ``"/api/licence"``.
        data : Union[Mapping[:class:`str`, Any], list[Any], :class:`bytes`, None], optional
            The JSON body, by default None.
            - A few calls take a list.
            - Bytes are sent as they are, with ``Content-Type: application/octet-stream``.
        files : Union[Mapping[:class:`str`, :class:`bytes`], None], optional
            Files to send as the web panel's upload form, each relative path to its content, by default None.
        parameters : Union[:class:`QueryParameters`, None], optional
            The query string, by default None.
            - A list value repeats its key, eg. ``{"shard": ["a", "b"]}`` is sent as ``shard=a&shard=b``.
        raw_bytes : :class:`bool`, optional
            If a successful reply should come back as bytes rather than JSON or not, by default False.
            - Downloads need `raw_bytes`.
            - An error is still read as JSON, or kept as text when the error isn't JSON.
        use_token : :class:`bool`, optional
            If the call needs a session or not, by default True.
            - Without a session we don't log in or send a token, eg. for ``GET /api/health/status``.
        setup_code : Union[:class:`str`, None], optional
            The first-run setup's code, sent as the ``X-Setup-Token`` header, by default None.
            - Only :class:`SetupModule`'s calls send a setup code.

        Returns
        -------
        Any
            The decoded JSON body, `None` for an empty one (a 204), the text of a body that isn't JSON, or the bytes
            with `raw_bytes`.

        Raises
        ------
        AMPAPIRequestError
            If AMP answers with an error status, or is still down after the last delay.
        AMPAPILoginError
            If a login this call needed was refused.
        AMPAPIPasskeyRequiredError
            If a login this call needed asks for a second factor.
        AMPAPIPasswordChangeRequiredError
            If a login this call needed asks for a new password first.
        ValueError
            If `setup_code` is empty or only whitespace. Nothing is sent.

        """
        return await self.session._request(  # pyright: ignore[reportPrivateUsage]
            method=method,
            path=path,
            data=data,
            files=files,
            parameters=parameters,
            raw_bytes=raw_bytes,
            use_token=use_token,
            setup_code=setup_code,
        )
