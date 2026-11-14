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
    "AMPAPIHubError",
    "AMPAPILoginError",
    "AMPAPIPasskeyRequiredError",
    "AMPAPIPasswordChangeRequiredError",
    "AMPAPIRequestError",
    "AMPAPIUploadError",
)

LOGGER: logging.Logger = logging.getLogger("AMPAPI_Python.errors")


def _is_dotted_key(value: object) -> bool:
    """If `value` is one of AMP's dotted keys, eg. ``"shards.migration.notRunning"``, rather than an English sentence."""
    # A sentence has spaces in it.
    if not isinstance(value, str) or value.split() != [value]:
        return False
    # A key has its dots between words; a one word sentence would only end with a dot.
    return "." in value.rstrip(".")


def _is_json_object(value: object) -> TypeGuard[dict[str, Any]]:
    """If `value` is a decoded JSON object; its keys are always strings."""
    return isinstance(value, dict)


class AMPAPIError(Exception):
    """The base of every error this library raises."""


# TODO: Nothing raises this until the hubs come back (#3-50.1).
class AMPAPIHubError(AMPAPIError):
    """Raised when one of AMP's hubs refuses a call, eg. joining a shard that no longer exists.

    Attributes
    ----------
    hub : :class:`str`
        The hub, eg. ``"shard"``.
    target : :class:`str`
        The call it refused, eg. ``"JoinShard"``.
    error : Any
        What AMP said: a `{code, params, message}` object for a refused join, or a string for a call it couldn't run.

    """

    hub: str
    target: str
    error: Any

    def __init__(self, hub: str, target: str, error: Any) -> None:  # noqa: D107
        self.hub = hub
        self.target = target
        self.error = error
        message = "An AMP hub refused a call. | Hub: %s | Target: %s | Error: %s"
        super().__init__(message % (hub, target, error))
        LOGGER.error(message, hub, target, error)


class AMPAPILoginError(AMPAPIError):
    """Raised when AMP refuses a login, a wrong password and an unknown user alike.

    Attributes
    ----------
    username : :class:`str`
        The username that was refused.
    reason : :class:`str`
        AMP's message, eg. "Invalid username or password.".

    """

    username: str
    reason: str

    def __init__(self, username: str, reason: str) -> None:  # noqa: D107
        self.username = username
        self.reason = reason
        message = "AMP refused the login. Reason: %s | Username: %s"
        super().__init__(message % (reason, username))
        LOGGER.error(message, reason, username)


class AMPAPIPasskeyRequiredError(AMPAPIError):
    """Raised when the account needs a second factor; nothing was logged in.

    Send one of the account's recovery codes to :meth:`~ampapi.Session.second_factor`. A passkey itself needs a browser.

    .. warning::
        Passkeys need the panel on HTTPS.

    Attributes
    ----------
    username : :class:`str`
        The username that needs the second factor.

    """

    username: str

    def __init__(self, username: str) -> None:  # noqa: D107
        self.username = username
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

    username: str
    reason: str

    def __init__(self, username: str, reason: str) -> None:  # noqa: D107
        self.username = username
        self.reason = reason
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
        AMP's dotted error key, eg. ``"auth.error.reproofRejected"``, when it sent one: as `code`, as `reason`, or
        alone in `error`, eg. ``{"error": "shards.migration.notRunning"}``.
    message : Union[:class:`str`, None]
        AMP's message, when it sent one. A body of only ``{"error": ...}`` lands here, a dotted key and a sentence alike;
        only a dotted key is the `code` too.
    params : Union[dict[:class:`str`, Any], None]
        Values for the `code` translation, when AMP sent any.
    errors : Union[list[:class:`str`], dict[:class:`str`, list[:class:`str`]], None]
        The validation errors: a list of messages, or field names to messages, when AMP sent any.
    data : Any
        The decoded response body, `None` for an empty one, or the text of a body that isn't JSON, eg. a proxy's error
        page.

    """

    status: int
    method: str
    path: str
    code: Optional[str]
    message: Optional[str]
    params: Optional[dict[str, Any]]
    errors: Optional[list[str] | dict[str, list[str]]]
    data: Any

    def __init__(self, status: int, method: str, path: str, data: Any) -> None:  # noqa: D107
        self.status = status
        self.method = method
        self.path = path
        self.data = data
        self.code = None
        self.message = None
        self.params = None
        self.errors = None

        # Each error shape AMP sends has a different set of these keys, so we take whichever are there.
        if _is_json_object(value=data):
            # A refused recovery code carries its dotted key as `reason`, everything else as `code`.
            self.code = data.get("code", data.get("reason"))
            # Invites, running tasks, spire enrolment and shard moves send `{error}`, with a dotted key or an English sentence in it.
            self.message = data.get("message", data.get("title", data.get("error")))
            # A dotted key there is the code as well, so `code` reads the same whichever shape AMP chose.
            if self.code is None and _is_dotted_key(value=data.get("error")) is True:
                self.code = data["error"]

            self.params = data.get("params")
            self.errors = data.get("errors")

        message = "We encountered an error response from the AMP API. Status: %s | Request: %s %s | Code: %s | Message: %s | Errors: %s"
        super().__init__(message % (status, method, path, self.code, self.message, self.errors))
        LOGGER.error(message, status, method, path, self.code, self.message, self.errors)


class AMPAPIUploadError(AMPAPIError):
    """Raised when a chunked upload can't go on, see :meth:`~ampapi.ShardModule.upload_shard_file`.

    Either AMP already holds part of an earlier upload to the path, or it stopped taking the chunks.

    .. versionadded:: 6.0.0

    Attributes
    ----------
    path : :class:`str`
        The file's path in the shard.
    session_id : :class:`str`
        The upload's `sessionId`.
    received : :class:`int`
        How many bytes AMP holds for the upload.
    size : :class:`int`
        The file's size in bytes.

    """

    path: str
    session_id: str
    received: int
    size: int

    def __init__(self, path: str, session_id: str, received: int, size: int, reason: str) -> None:  # noqa: D107
        self.path = path
        self.session_id = session_id
        self.received = received
        self.size = size
        message = "%s | Path: %s | Session ID: %s | Received: %s of %s bytes"
        super().__init__(message % (reason, path, session_id, received, size))
        LOGGER.error(message, reason, path, session_id, received, size)
