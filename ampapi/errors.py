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
from typing import Any, Optional, TypeGuard

__all__ = (
    "AMPAPIError",
    "AMPAPILoginError",
    "AMPAPIPasskeyRequiredError",
    "AMPAPIPasswordChangeRequiredError",
    "AMPAPIRequestError",
)

LOGGER: logging.Logger = logging.getLogger("AMPAPI_Python.errors")


def _is_json_object(value: object) -> TypeGuard[dict[str, Any]]:
    """If `value` is a decoded JSON object; its keys are always strings."""
    return isinstance(value, dict)


class AMPAPIError(Exception):
    """The base of every error this library raises."""


class AMPAPILoginError(AMPAPIError):
    """Raised when AMP refuses a login, a wrong password and an unknown user alike.

    Attributes
    ----------
    username : :class:`str`
        The username that was refused.
    reason : :class:`str`
        AMP's message, eg. "Invalid username or password.".

    """

    def __init__(self, username: str, reason: str) -> None:  # noqa: D107
        self.username: str = username
        self.reason: str = reason
        message = "AMP refused the login. Reason: %s | Username: %s"
        super().__init__(message % (reason, username))
        LOGGER.error(message, reason, username)


class AMPAPIPasskeyRequiredError(AMPAPIError):
    """Raised when the account needs a second factor; nothing was logged in.

    Send one of the account's recovery codes to :meth:`~ampapi.Session.second_factor`. A passkey itself needs a browser.

    .. warning::
        Not yet seen live. Passkeys need the panel on HTTPS.

    Attributes
    ----------
    username : :class:`str`
        The username that needs the second factor.

    """

    def __init__(self, username: str) -> None:  # noqa: D107
        self.username: str = username
        message = "AMP needs a second factor for this login. | Username: %s"
        super().__init__(message % username)
        LOGGER.warning(message, username)


class AMPAPIPasswordChangeRequiredError(AMPAPIError):
    """Raised when the account has to change its password before it can log in; nothing was logged in.

    Call :meth:`~ampapi.Session.change_expired_password` with the new password.

    Attributes
    ----------
    username : :class:`str`
        The username that has to change its password.
    reason : :class:`str`
        AMP's reason, eg. ``"forced"`` for an account created with `requirePasswordChange`.

    """

    def __init__(self, username: str, reason: str) -> None:  # noqa: D107
        self.username: str = username
        self.reason: str = reason
        message = "AMP needs a password change before this login. Reason: %s | Username: %s"
        super().__init__(message % (reason, username))
        LOGGER.warning(message, reason, username)


class AMPAPIRequestError(AMPAPIError):
    """Raised for an error response from the AMP API.

    AMP answers errors in a few shapes; whichever arrived, its parts are on the attributes below.

    Attributes
    ----------
    status : :class:`int`
        The HTTP status code.
    method : :class:`str`
        The HTTP method of the request.
    path : :class:`str`
        The path of the request, eg. ``/api/me/permissions``.
    code : Union[:class:`str`, None]
        AMP's dotted error key, eg. ``auth.error.reproofRejected``, when it sent one.
    message : Union[:class:`str`, None]
        AMP's message, when it sent one.
    params : Union[dict[:class:`str`, Any], None]
        Values for the `code` translation, when AMP sent any.
    errors : Union[list[:class:`str`], dict[:class:`str`, list[:class:`str`]], None]
        The validation errors: a list of messages, or field names to messages, when AMP sent any.
    data : Any
        The decoded response body, `None` for an empty one.

    """

    def __init__(self, status: int, method: str, path: str, data: Any) -> None:  # noqa: D107
        self.status: int = status
        self.method: str = method
        self.path: str = path
        self.data: Any = data
        self.code: Optional[str] = None
        self.message: Optional[str] = None
        self.params: Optional[dict[str, Any]] = None
        self.errors: Optional[list[str] | dict[str, list[str]]] = None

        # Each error shape AMP sends has a different set of these keys, so we take whichever are there.
        if _is_json_object(value=data):
            self.code = data.get("code")
            self.message = data.get("message", data.get("title"))
            self.params = data.get("params")
            self.errors = data.get("errors")

        message = "We encountered an error response from the AMP API. Status: %s | Request: %s %s | Code: %s | Message: %s | Errors: %s"
        super().__init__(message % (status, method, path, self.code, self.message, self.errors))
        LOGGER.error(message, status, method, path, self.code, self.message, self.errors)
