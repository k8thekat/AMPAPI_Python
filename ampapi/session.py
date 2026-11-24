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
import base64
import ipaddress
import json
import logging
import re
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Self, TypeGuard, Union

from aiohttp import ClientError, ClientSession, FormData

from .errors import AMPAPILoginError, AMPAPIPasskeyRequiredError, AMPAPIPasswordChangeRequiredError, AMPAPIRequestError
from .utils import is_dotted_key, is_json_object

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping, Sequence
    from types import TracebackType

    from ._types import (
        CapabilitiesResponse,
        ExpiredPasswordRequest,
        HubTokenResponse,
        InviteAcceptedResponse,
        InviteAcceptRequest,
        InvitePreviewResponse,
        LoginRequest,
        LoginResponse,
        PasskeyFlowResponse,
        PasskeyLoginRequest,
        PasswordPolicyResponse,
        QueryParameters,
        SecondFactorRequest,
        TokenClaims,
        TokenResponse,
    )

__all__ = ("Session", "redact")

LOGGER: logging.Logger = logging.getLogger(__name__)

# The project's own capture tool (`.scripts/amp3/capture.py`) imports `redact`, so both redact alike.
# Matched on the key's ending, so `code` / `errorCode` stay readable and `licenceKey` / `refreshToken` do not.
# `passkeyMessageKey` (a translation key) and a setting's `effectiveKey` (its config name) are not secrets, so kept.
# An analytics `userKey` / `analyticsKey` is kept too, as it means nothing outside this installation.
# `authorization` and `cookie` cover the request and reply headers that carry a session.
# `ticket` covers a download ticket, in the `download-ticket` / `zip-ticket` reply and in the download's query (#3-60b).
SECRET_KEYS = re.compile(
    r"(token|password|secret|jwt|(?<!message)(?<!effective)(?<!user)(?<!analytics)key|credentials|recoverycodes|codes|cacert|blob"
    r"|externalip|externaladdress|authorization|cookie|ticket)$",
    re.IGNORECASE,
)
# A game's device sign-in code, wherever it sits in a string: a hytale update put "Authorization code: <code>" in its
# running task's `message`, and the sign-in URL carries it as `user_code=`.
SIGN_IN_CODES = re.compile(r"(user_code=|Authorization code: )[A-Za-z0-9-]+", re.IGNORECASE)
# Any IPv4 address in a string value. Only the global ones are blanked, and only under keys that name an address,
# as four-part version strings (`minAMPVersion`, `agentVersion`) look just like global IPs.
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
# `uri` and `url` too, as an endpoint's `steam://connect/<address>:<port>` link carries the public address.
ADDRESS_KEYS = re.compile(r"(host|hosts|address|addresses|ip|ips|display|endpoint|endpoints|origin|uri|url)$", re.IGNORECASE)
# A GUID in a request path, which a capture's file name swaps for `{id}` so one route's captures sort together.
GUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE)
# Anything else a file name shouldn't hold, eg. the `%` of an escaped file path.
UNSAFE_NAME = re.compile(r"[^A-Za-z0-9._{}-]")
# The reply headers worth keeping in a capture; the rest is transport noise.
KEEP_HEADERS = ("content-type", "www-authenticate", "set-cookie", "location", "retry-after", "x-")


def _is_json_list(value: object) -> TypeGuard[list[Any]]:
    return isinstance(value, list)


def _blank_public_ip(match: re.Match[str]) -> str:
    try:
        return "<public ip>" if ipaddress.ip_address(match.group(0)).is_global else match.group(0)
    except ValueError:
        return match.group(0)


def redact(value: Any, key: str = "") -> Any:
    """Hide the secrets in a request or a reply, at any depth.

    A string under a secret-looking key (a token, password, key, secret, recovery code, download ticket, or the
    `Authorization` header) becomes ``"<redacted str len=N>"``. A game's sign-in code is blanked wherever it sits in a string, and a
    public IP address under an address-like key (`host`, `address`, `url`, ...) becomes ``"<public ip>"``.
    Private addresses are left as they are. Running `redact` again over a redacted copy changes nothing.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    value : Any
        The decoded JSON to redact. Dicts and lists are walked, and anything that isn't a string is kept as it is.
    key : :class:`str`, optional
        The key `value` sits under, by default "".

    Returns
    -------
    Any
        A copy of `value` with its secrets hidden.

    """
    if is_json_object(value=value):
        return {item_key: redact(item, item_key) for item_key, item in value.items()}
    if _is_json_list(value=value):
        return [redact(item, key) for item in value]

    if not isinstance(value, str) or value.startswith("<redacted str len="):
        return value

    if SECRET_KEYS.search(key) and value:
        return f"<redacted str len={len(value)}>"
    # A recovery code is sent as `code`, but AMP's error codes there are dotted keys and a crash's exit code is a number
    if key.lower() == "code" and value and is_dotted_key(value=value) is False and value.lstrip("-").isdigit() is False:
        return f"<redacted str len={len(value)}>"
    value = SIGN_IN_CODES.sub(r"\1<redacted>", value)
    if ADDRESS_KEYS.search(key):
        return IPV4.sub(_blank_public_ip, value)
    return value


class Session:
    """One login to an AMP 3 panel, which a :class:`Panel` sends its calls through.

    .. code-block:: python

        session = Session(url="http://192.168.1.10:8443", username="amp_username", password="amp_password")

        # Leaving the block logs the `Session` out and closes it
        async with Panel(session=session) as panel:
            shards: list[Shard] = await panel.get_shards()

    The `Session` looks after the login for every call made through it:

    - Logs in on the first call that needs a session. A call that needs a session can raise :exc:`AMPAPILoginError`,
      :exc:`AMPAPIPasskeyRequiredError` or :exc:`AMPAPIPasswordChangeRequiredError` from the login.
    - Renews the token before the token runs out.
    - Logs in again when AMP ends the session, eg. a logout elsewhere or an admin's force logout.
    - Sends a request again while AMP's database or message bus is down, after 1, 2 and 4 seconds, then 8 seconds twice,
      the way the web panel does. AMP reports the outage as a 503 with ``"session.storeUnavailable"`` or
      ``"common.error.busUnavailable"``.
    - Shares one login between calls made at the same time. When AMP refuses the shared login, every waiting call raises
      the login's error, and the login isn't sent again.

    .. warning::
        The library can't repeat a login finished with :meth:`second_factor` or :meth:`complete_passkey_login`. Once AMP
        ends that session, or the session runs out, the next call that needs a session logs in by password. When the
        account needs a recovery code or a passkey, that password login raises :exc:`AMPAPIPasskeyRequiredError`.
        Catch :exc:`AMPAPIPasskeyRequiredError`, then call :meth:`second_factor` with a new recovery code, or run the
        passkey login again.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    url : :class:`str`
        The panel's URL, eg. ``"http://192.168.1.10:8443"``.
    username : :class:`str`
        The AMP username to log in as.
        - Before :meth:`accept_invite` the username can be anything, eg. ``""``, as the invite's username replaces it.
        - For :meth:`SetupModule.create_admin`, the username the panel's first admin gets.
    password : :class:`str`
        The password for `username`.
        - For :meth:`SetupModule.create_admin`, the password the panel's first admin gets. The password has to pass
        :meth:`get_password_policy`.
    remember_me : :class:`bool`, optional
        If a login asks for a 28 day token instead of an 8 hour token or not, by default False.
    session : Union[:class:`ClientSession`, None], optional
        An aiohttp `ClientSession` to send requests through, by default None.
        - Without a `ClientSession` the `Session` makes its own `ClientSession`, which :meth:`clean_up` closes.
        :meth:`clean_up` logs out either way.
    capture_dir : Union[:class:`Path`, None], optional
        A folder to save every request and AMP's reply in, redacted, for the whole run, by default None.
        - See :meth:`capture` for what each file holds, and for capturing only part of a run.

    Attributes
    ----------
    url : :class:`str`
        The panel's URL, without a trailing ``/``.
    username : :class:`str`
        The AMP username the `Session` logs in as.
        - The function :meth:`accept_invite` sets it to the invite's username.
    remember_me : :class:`bool`
        If a login asks for a 28 day token instead of an 8 hour token or not.

    """

    url: str
    username: str
    remember_me: bool
    # The password for `username`, kept for the logins we make again; `change_expired_password` replaces it.
    _password: str
    # The aiohttp session requests go through, made on the first request when none was handed to us.
    _session: Optional[ClientSession]
    # If we made `_session` ourselves, so `clean_up` closes it.
    _own_session: bool
    # The current token, when it runs out, the point we renew it after, and its decoded claims, all cleared at logout.
    _token: Optional[str]
    _expiration: Optional[datetime]
    _renew_after: Optional[datetime]
    _claims: TokenClaims
    # Held while logging in, so calls made at the same time share one login.
    _login_lock: asyncio.Lock
    # How many logins `_ensure_login` has finished, and the error the last one raised, for the calls that waited on it.
    _login_attempts: int
    _login_error: Optional[Exception]
    # The whole run's capture folder (`None` when off), and each open `capture` block's folder and if it's redacted.
    _capture_dir: Optional[Path]
    _capture_blocks: list[tuple[Path, bool]]

    # How far through a token's lifetime we renew it, the same point AMP's web panel uses.
    _renew_point: ClassVar[float] = 0.75
    # How long we wait before trying a renew again after AMP refused it, eg. with a 503.
    _renew_retry: ClassVar[timedelta] = timedelta(minutes=1)
    # The web panel tries a 503 again after each of these delays (in seconds) when AMP names one of these outages.
    _outage_codes: ClassVar[tuple[str, ...]] = ("session.storeUnavailable", "common.error.busUnavailable")
    _outage_delays: ClassVar[tuple[int, ...]] = (1, 2, 4, 8, 8)

    def __init__(  # noqa: D107
        self,
        url: str,
        username: str,
        password: str,
        *,
        remember_me: bool = False,
        session: Optional[ClientSession] = None,
        capture_dir: Optional[Path] = None,
    ) -> None:
        self.url = url.rstrip("/")
        self.username = username
        self.remember_me = remember_me
        self._password = password
        self._session = session
        self._own_session = session is None
        self._token = None
        self._expiration = None
        self._renew_after = None
        self._claims = {}
        self._login_lock = asyncio.Lock()
        self._login_attempts = 0
        self._login_error = None
        self._capture_dir = capture_dir
        self._capture_blocks = []

    async def __aenter__(self) -> Self:  # noqa: D105
        return self

    async def __aexit__(  # noqa: D105
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.clean_up()

    @property
    def enrolment_only(self) -> bool:
        """If the current session may only add a passkey (the token's ``amp:scope`` claim is ``"enrol"``).

        AMP hands out an enrolment-only session when the passkey policy is ``"Required"`` and the account has no passkey
        yet.
        """
        return self._claims.get("amp:scope") == "enrol"

    @property
    def expiration(self) -> Optional[datetime]:
        """When the current token runs out, `None` when not logged in."""
        return self._expiration

    @property
    def logged_in(self) -> bool:
        """If the `Session` holds a token that hasn't run out yet."""
        return self._expiration is not None and datetime.now(tz=UTC) < self._expiration

    @property
    def session_id(self) -> Optional[str]:
        """AMP's ID for the current session (the token's `sid` claim), which stays the same across renewals."""
        return self._claims.get("sid")

    @property
    def user_id(self) -> Optional[str]:
        """The logged in user's ID, the same as `ProfileResponse.id`."""
        return self._claims.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier")

    def _write_capture(
        self,
        *,
        method: str,
        path: str,
        query: Optional[Mapping[str, Any]],
        headers: Mapping[str, str],
        data: Optional[Union[Mapping[str, Any], list[Any], bytes]],
        files: Optional[Mapping[str, bytes]],
        status: int,
        reply_headers: Mapping[str, str],
        reply: bytes,
        body: Any,
    ) -> None:
        """Save one request and AMP's reply in every capture folder that's on: `capture_dir` and each open :meth:`capture`.

        The file is named from the method, the path with each GUID as ``{id}``, and the UTC time to the microsecond.
        A failure to write the file is logged, never raised, so the call carries on.
        """
        # The `capture_dir` folder is always redacted. A folder named twice gets the reply once.
        folders: dict[Path, bool] = {} if self._capture_dir is None else {self._capture_dir: True}
        for block_dir, block_redact in self._capture_blocks:
            if block_dir not in folders:
                folders[block_dir] = block_redact
        if not folders:
            return

        request_body: Any = data
        if isinstance(data, bytes):
            request_body = {"<bytes>": {"contentType": "application/octet-stream", "length": len(data)}}
        elif files is not None:
            request_body = {"<files>": [{"path": relative_path, "length": len(content)} for relative_path, content in files.items()]}

        # A download, an image or any other binary reply is kept as its type and size, never its bytes
        content_type: str = reply_headers.get("Content-Type", "")
        reply_body: Any = body
        if isinstance(body, bytes) or (reply and not content_type.startswith(("application/json", "application/problem+json", "text/"))):
            reply_body = {"<bytes>": {"contentType": content_type, "length": len(reply)}}

        # One moment for both the file name and `time`, so the file name and `time` always agree
        now: datetime = datetime.now(tz=UTC)
        capture: dict[str, Any] = {
            "time": now.isoformat(),
            "request": {"method": method, "url": self.url, "path": path, "parameters": query, "headers": headers, "body": request_body},
            "status": status,
            "headers": {key: value for key, value in reply_headers.items() if key.lower().startswith(KEEP_HEADERS)},
            "body": reply_body,
        }
        route: str = "_".join("{id}" if GUID.fullmatch(part) else part for part in path.strip("/").split("/"))
        route = UNSAFE_NAME.sub("_", route)[:150]
        # Year first sorts a route's files in time order. Windows refuses `:` and `|` in a file name, so neither is used.
        file_name: str = f"{method}_{route}_{now.strftime('%Y-%m-%d_%H-%M-%S.%f')}.json"
        for folder, hide in folders.items():
            # Mode "x" refuses a name that exists, so a second reply on the route in the same microsecond logs a warning
            try:
                text: str = json.dumps(redact(capture) if hide is True else capture, indent=4) + "\n"
                folder.mkdir(parents=True, exist_ok=True)
                with folder.joinpath(file_name).open(mode="x", encoding="utf-8") as file:
                    file.write(text)
            except (OSError, TypeError, ValueError) as error:
                LOGGER.warning(
                    "<%s.%s> | Failed to write a capture, carrying on | Method: %s | Path: %s | Folder: %s | Error: %r",
                    __class__.__name__,
                    "_write_capture",
                    method,
                    path,
                    folder,
                    error,
                )

    async def _send(
        self,
        method: str,
        path: str,
        data: Optional[Union[Mapping[str, Any], list[Any], bytes]] = None,
        *,
        files: Optional[Mapping[str, bytes]] = None,
        parameters: Optional[QueryParameters] = None,
        raw_bytes: bool = False,
        use_token: bool = True,
        setup_code: Optional[str] = None,
    ) -> tuple[int, str, Any]:
        """Send a request and decode the reply. Raises nothing for an error status, the caller decides.

        `data` is sent as JSON, or as it is with ``Content-Type: application/octet-stream`` when it's bytes. `files` is
        sent as the web panel's upload form instead, a `files` part and a `paths` part for each file.
        `setup_code` is sent as the ``X-Setup-Token`` header the first-run setup calls need, with the whitespace around
        the code removed.

        Every request goes through here, logins and renewals too. A 503 whose `code` says AMP's database
        (``"session.storeUnavailable"``) or message bus (``"common.error.busUnavailable"``) is down is sent again after
        1, 2 and 4 seconds, then 8 seconds twice, the way the web panel does. A request with `setup_code` isn't sent
        again, so a setup code never counts twice toward AMP's lockout.
        While :meth:`capture` or `capture_dir` has capturing on, each reply is saved by `_write_capture`.

        Returns
        -------
        tuple[:class:`int`, :class:`str`, Any]
            The HTTP status, the ``WWW-Authenticate`` header (empty when not sent) and the decoded JSON body,
            `None` for an empty one, or the text of a body that isn't JSON, eg. a proxy's error page.
            With `raw_bytes` a successful reply is the bytes as they came.

        Raises
        ------
        ValueError
            If `setup_code` is empty or only whitespace. Nothing is sent.

        """
        if self._session is None:
            self._session = ClientSession()

        headers: dict[str, str] = {"Accept": "*/*" if raw_bytes is True else "application/json"}
        if use_token is True and self._token is not None:
            headers["Authorization"] = f"Bearer {self._token}"

        # The setup code file ends in a newline, which a header can't carry
        if setup_code is not None:
            if not setup_code.strip():
                err = "The setup code is empty."
                raise ValueError(err)
            headers["X-Setup-Token"] = setup_code.strip()

        # aiohttp refuses a `bool` in the query string, so we write it the way AMP reads one (#3-51.4j)
        query: Optional[dict[str, Union[str, int, Sequence[str]]]] = None
        if parameters is not None:
            query = {}
            for key, value in parameters.items():
                if isinstance(value, bool):
                    query[key] = "true" if value is True else "false"
                else:
                    query[key] = value

        # We try again once for each delay, then hand back AMP's last answer.
        retries: int = 0
        while True:
            json_body: Optional[Union[Mapping[str, Any], list[Any]]] = None
            raw_body: Optional[Union[bytes, FormData]] = None

            if isinstance(data, bytes):
                raw_body = data
                headers["Content-Type"] = "application/octet-stream"

            elif files is not None:
                # A new form for each send, as aiohttp sends a form only once and a dead session or an outage sends it again.
                raw_body = FormData()

                for relative_path, content in files.items():
                    raw_body.add_field(name="files", value=content, filename=PurePosixPath(relative_path).name)
                    raw_body.add_field(name="paths", value=relative_path)
            else:
                json_body = data

            LOGGER.debug("<%s.%s> | Method: %s | Path: %s | Parameters: %s", __class__.__name__, "_send", method, path, query)
            async with self._session.request(
                method=method,
                url=self.url + path,
                params=query,
                json=json_body,
                data=raw_body,
                headers=headers,
            ) as res:
                reply: bytes = await res.read()
                authenticate_header: str = res.headers.get("WWW-Authenticate", "")
                status: int = res.status

            # A download comes back as bytes, but AMP's errors are JSON either way.
            download: bool = raw_bytes is True and 200 <= status < 300
            # AMP answers some calls (logout, reauth) with an empty 204, and some GETs use a 204 for "nothing yet".
            body: Any = reply if download is True else None
            if download is False and reply:
                try:
                    body = json.loads(reply)
                except ValueError:
                    # A proxy in front of AMP answers with its own page, eg. an HTML 502, so we keep it as text
                    body = reply.decode(encoding="utf-8", errors="replace")

            # Every reply is captured once `capture` is on, a 503 we send again included
            self._write_capture(
                method=method,
                path=path,
                query=query,
                headers=headers,
                data=data,
                files=files,
                status=status,
                reply_headers=res.headers,
                reply=reply,
                body=body,
            )
            if download is True:
                return status, authenticate_header, body
            code: Optional[str] = body.get("code") if is_json_object(value=body) else None
            if status != 503 or code not in self._outage_codes or retries == len(self._outage_delays):
                return status, authenticate_header, body

            # A setup code is never sent twice: 10 wrong codes lock the caller's IP address out, and an outage reply
            # doesn't say if AMP checked the code first, so a setup call raises the 503 and the caller decides
            if setup_code is not None:
                return status, authenticate_header, body

            delay: int = self._outage_delays[retries]
            retries += 1
            LOGGER.warning(
                "<%s.%s> | AMP is unavailable, trying again in %s seconds | Code: %s | Path: %s",
                __class__.__name__,
                "_send",
                delay,
                code,
                path,
            )
            await asyncio.sleep(delay=delay)

    def _store_token(self, data: TokenResponse) -> TokenResponse:
        """Keep a new token, and work out when to renew it."""
        now: datetime = datetime.now(tz=UTC)
        self._token = data["token"]
        self._expiration = datetime.fromisoformat(data["expiration"])
        self._renew_after = now + (self._expiration - now) * self._renew_point

        # The middle part of a JWT is base64 JSON; we only read it, AMP checks the signature.
        payload: str = self._token.split(".")[1]
        self._claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        LOGGER.debug(
            "<%s.%s> | Session ID: %s | Expiration: %s | Renew After: %s",
            __class__.__name__,
            "_store_token",
            self.session_id,
            self._expiration,
            self._renew_after,
        )
        if self.enrolment_only is True:
            LOGGER.warning(
                "<%s.%s> | AMP requires a passkey, this session can only add one | Username: %s",
                __class__.__name__,
                "_store_token",
                self.username,
            )

        return data

    def _forget_token(self) -> None:
        self._token = None
        self._expiration = None
        self._renew_after = None
        self._claims = {}

    # A password change made through a module (`change_password`, `reset_user_password`) keeps the new one here for
    # the logins we make again (#3-51.4g)
    def _keep_password(self, password: str) -> None:
        self._password = password

    async def _login_result(self, data: LoginResponse) -> TokenResponse:
        """Keep the token from a login-like call, or raise for the follow-up step AMP asked for instead.

        A token we already hold is logged out before the new token replaces it, so the old token's session isn't left
        open on AMP.
        A failed logout is logged, not raised.
        """
        if "passwordChangeRequired" in data:
            raise AMPAPIPasswordChangeRequiredError(username=self.username, reason=data["reason"])
        if "passkeyRequired" in data:
            raise AMPAPIPasskeyRequiredError(username=self.username)

        if self._token is not None:
            try:
                await self.logout()
            except (AMPAPIRequestError, ClientError, TimeoutError) as error:
                LOGGER.warning(
                    "<%s.%s> | Logout of the old session failed, keeping the new one | Error: %r",
                    __class__.__name__,
                    "_login_result",
                    error,
                )
        return self._store_token(data=data)

    async def _ensure_login(self, used_token: Optional[str] = None) -> None:
        """Log in, or renew, when needed. Calls made at the same time wait for a single shared login.

        A call that waited through a login that failed raises that login's error, rather than sending the same login
        again. A renew AMP refuses for anything but an ended session (eg. a 503) is logged, and we keep the token
        until it runs out, trying the renew again after `_renew_retry`.

        Parameters
        ----------
        used_token : Union[:class:`str`, None], optional
            The token a request was refused with, by default None.
            - If we already hold a different token, another call has logged in again since, so we don't log in again.

        """
        login_attempt: int = self._login_attempts
        async with self._login_lock:
            # A login failed while we waited, so we raise its error instead of sending the same password again
            if login_attempt != self._login_attempts and self._token is None and self._login_error is not None:
                raise self._login_error
            # A token AMP refused, or a token that has run out, can't be renewed, so we log in again
            if self._token is not None and (used_token == self._token or self.logged_in is False):
                self._forget_token()
            if self._token is not None and self._renew_after is not None and datetime.now(tz=UTC) >= self._renew_after:
                # We read the status ourselves, so a renew we recover from doesn't build an error that logs one
                status, _authenticate_header, body = await self._send(method="POST", path="/api/auth/renew", data={})
                if 200 <= status < 300:
                    self._store_token(data=body)
                elif status == 401:
                    # The session ended between calls, so we start a new one
                    LOGGER.debug(
                        "<%s.%s> | Session ended by AMP, logging in again | Session ID: %s",
                        __class__.__name__,
                        "_ensure_login",
                        self.session_id,
                    )
                    self._forget_token()
                else:
                    # The token still works until it runs out, so we keep it and renew later
                    self._renew_after = datetime.now(tz=UTC) + self._renew_retry
                    LOGGER.warning(
                        "<%s.%s> | Renew refused, keeping the current token | Status: %s | Expiration: %s | Next Renew: %s",
                        __class__.__name__,
                        "_ensure_login",
                        status,
                        self._expiration,
                        self._renew_after,
                    )

            if self._token is None:
                self._login_error = None
                try:
                    await self.login()
                except Exception as error:
                    # Kept for the calls waiting on this login, so they don't each send it again
                    self._login_error = error
                    raise
                finally:
                    # Counted once it ends, so every call that came in while it ran sees the change
                    self._login_attempts += 1

    async def _send_with_login(
        self,
        method: str,
        path: str,
        data: Optional[Union[Mapping[str, Any], list[Any], bytes]] = None,
        *,
        files: Optional[Mapping[str, bytes]] = None,
        parameters: Optional[QueryParameters] = None,
        raw_bytes: bool = False,
        use_token: bool = True,
        setup_code: Optional[str] = None,
    ) -> tuple[int, Any]:
        """Send a request, logging in first when it needs a session and we have to. Raises nothing for an error status.

        A 401 for a token AMP no longer accepts gets one new login and a second try. With `use_token` set to `False`
        we send no token and never log in, for the calls that need no session. The rest go to `_send` as they are.
        The first-run setup calls send `setup_code` with `use_token` set to `False`, so they never reach the second try.

        Returns
        -------
        tuple[:class:`int`, Any]
            The HTTP status and the decoded JSON body, `None` for an empty one, the text of a body that isn't JSON, or
            the bytes with `raw_bytes`.

        Raises
        ------
        AMPAPILoginError
            If a login the request needed was refused, as :meth:`login` raises it.
        AMPAPIPasskeyRequiredError
            If a login the request needed asks for a second factor.
        AMPAPIPasswordChangeRequiredError
            If a login the request needed asks for a new password first.
        AMPAPIRequestError
            If a login the request needed got any other error status.

        """
        if use_token is True:
            await self._ensure_login()

        used_token: Optional[str] = self._token
        status, authenticate_header, body = await self._send(
            method=method,
            path=path,
            data=data,
            files=files,
            parameters=parameters,
            raw_bytes=raw_bytes,
            use_token=use_token,
            setup_code=setup_code,
        )

        # AMP only says `invalid_token` when we sent one, so a call without a session never gets here.
        if status == 401 and "invalid_token" in authenticate_header:
            LOGGER.debug("<%s.%s> | Session ended by AMP, logging in again | Path: %s", __class__.__name__, "_send_with_login", path)
            await self._ensure_login(used_token=used_token)
            status, authenticate_header, body = await self._send(
                method=method,
                path=path,
                data=data,
                files=files,
                parameters=parameters,
                raw_bytes=raw_bytes,
            )

        return status, body

    async def _request(
        self,
        method: str,
        path: str,
        data: Optional[Union[Mapping[str, Any], list[Any], bytes]] = None,
        *,
        files: Optional[Mapping[str, bytes]] = None,
        parameters: Optional[QueryParameters] = None,
        raw_bytes: bool = False,
        use_token: bool = True,
        setup_code: Optional[str] = None,
    ) -> Any:
        """Send a request with `_send_with_login`, raising for an error status.

        The `Session`'s own calls, and every module's calls through `Base._request`, go this way. The parameters are
        `Base._request`'s. Only :class:`SetupModule`'s calls send `setup_code` (see `_send`).

        Returns
        -------
        Any
            The decoded JSON body, `None` for an empty one (a 204), the text of a body that isn't JSON, or the bytes
            with `raw_bytes`.

        Raises
        ------
        AMPAPIRequestError
            If AMP answers with an error status, or is still down after the last outage delay.
        AMPAPILoginError
            If a login the request needed was refused.
        AMPAPIPasskeyRequiredError
            If a login the request needed asks for a second factor.
        AMPAPIPasswordChangeRequiredError
            If a login the request needed asks for a new password first.
        ValueError
            If `setup_code` is empty or only whitespace. Nothing is sent.

        """
        status, body = await self._send_with_login(
            method=method,
            path=path,
            data=data,
            files=files,
            parameters=parameters,
            raw_bytes=raw_bytes,
            use_token=use_token,
            setup_code=setup_code,
        )
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method=method, path=path, data=body)

        return body

    async def accept_invite(
        self,
        token: str,
        email: str,
        *,
        display_name: Optional[str] = None,
        locale: str = "en",
    ) -> InviteAcceptedResponse:
        """Make the account an invite was for, which logs the `Session` in as the new account.

        |coro|

        Endpoints: ``POST /api/invites/preview`` for the invite's username, then ``POST /api/invites/accept``

        This call needs no login, and no :class:`Panel`. Make a :class:`Session` with the password the new account should
        have and any `username`, eg. ``""``, then call :meth:`accept_invite`.

        - The `Session`'s `username` becomes the username the invite was made with, see :meth:`preview_invite`.
        - From then on the `Session` renews and logs in again as the new account, like any other login.
        - If the `Session` was already logged in, the earlier session is logged out once the new account exists.

        Parameters
        ----------
        token : :class:`str`
            The invite code from :meth:`AccountModule.create_invite` or :meth:`AccountModule.rearm_invite`.
        email : :class:`str`
            The new account's email address.
        display_name : Union[:class:`str`, None], optional
            The new account's display name, by default None.
        locale : :class:`str`, optional
            The new account's language, by default "en".

        Returns
        -------
        :class:`InviteAcceptedResponse`
            The new account's session token, which the `Session` keeps.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the `Session`'s password doesn't pass :meth:`get_password_policy`.\n
            **404** - If the invite code is wrong, used, revoked or out of date `invalid_or_expired`. The 404 comes from
            reading the invite first, so nothing is made.\n
            **410** - If another account took the invite's username since the invite was made, from AMP's docs and not
            seen live.

        """
        # AMP gives the account the invite's username, so we read it from the invite first and keep it as `username`
        preview: InvitePreviewResponse = await self.preview_invite(token=token)
        data: InviteAcceptRequest = {
            "token": token,
            "email": email,
            "password": self._password,
            "displayName": display_name,
            "locale": locale,
        }

        result: InviteAcceptedResponse = await self._request(method="POST", path="/api/invites/accept", data=data, use_token=False)
        # We only take the invite's username once the account exists, so a refused accept leaves the session as it was.
        self.username = preview["userName"]
        await self._login_result(data=result)
        return result

    async def begin_passkey_login(self) -> PasskeyFlowResponse:
        """Start a login with a passkey, or a passkey proof for :meth:`reauth_with_passkey`.

        |coro|

        Endpoint: ``POST /api/auth/passkey/begin``

        This call needs no login. AMP takes no username: the options allow any passkey the authenticator holds for the
        panel.

        - The library holds no passkeys, so hand `options` to a WebAuthn authenticator, eg. a browser's
          ``navigator.credentials.get``.
        - Send the authenticator's answer and `flowId` to :meth:`complete_passkey_login` to log in, or to
          :meth:`reauth_with_passkey` for a passkey proof.
        - Call :meth:`abandon_passkey_login` for a flow the authenticator gave up on.

        .. note::
            Passkeys only work through the panel's public HTTPS address, so the `Session`'s `url` has to be that address.
            :meth:`get_capabilities` reads ``"Eligible"`` in `passkeyStatus` there.

        Returns
        -------
        :class:`PasskeyFlowResponse`
            The flow's ID and the WebAuthn request options.

        Raises
        ------
        AMPAPIRequestError
            **409** - If passkeys don't work at the panel's public address. The error's `code` says why. From AMP's
            docs and not seen live.\n
            **429** - If AMP throttled the caller's IP address after failed logins `auth.login.errorThrottled`.\n
            **429** - If the caller's IP address has too many passkey flows open, from AMP's docs and not seen live.

        """
        return await self._request(method="POST", path="/api/auth/passkey/begin", data={}, use_token=False)

    async def complete_passkey_login(self, flow_id: str, response: Mapping[str, Any]) -> TokenResponse:
        """Finish a passkey login with the authenticator's answer to :meth:`begin_passkey_login`, which logs in.

        |coro|

        Endpoint: ``POST /api/auth/passkey/complete``

        The `Session` keeps the new token. If the `Session` was already logged in, the earlier session is logged out.
        AMP takes no username here, so the `Session`'s `username` stays as it was.

        .. warning::
            The library can't repeat a passkey login.

            - The new session renews like any other.
            - Once AMP ends the session, or the session runs out, the next call that needs a session logs in by password
              with the `Session`'s `username` and password.
            - Under the passkey policy ``"Required"`` that password login raises :exc:`AMPAPIPasskeyRequiredError`.

        Parameters
        ----------
        flow_id : :class:`str`
            The `flowId` from :meth:`begin_passkey_login`.
        response : Mapping[:class:`str`, Any]
            The authenticator's answer, the WebAuthn `PublicKeyCredential` as JSON with base64url values:
            `id`, `rawId`, `type`, `extensions` and `response` (`authenticatorData`, `clientDataJSON`, `signature`,
            `userHandle`). The `clientDataJSON` has to name the panel's public address as its origin.

        Returns
        -------
        :class:`TokenResponse`
            The new session's token.

        Raises
        ------
        AMPAPIRequestError
            **400** - If AMP can't read the answer, from AMP's docs and not seen live.\n
            **401** - If AMP refuses the answer, eg. the wrong origin, the wrong rpId, no user verification, a bad
            signature or another flow's answer `passkeys.error.assertionRejected`.\n
            **401** - If the flow is over, eg. already used or abandoned `passkeys.error.ceremonyExpired`.\n
            **401** - If AMP has no passkey with the answer's credential ID `passkeys.error.unknownCredential`.\n
            **401** - If the passkey's signature counter went backwards `passkeys.error.cloneDetected`. AMP deletes
            that passkey.\n
            **429** - If AMP throttled the caller's IP address after failed logins `auth.login.errorThrottled`.

        """
        data: PasskeyLoginRequest = {"flowId": flow_id, "response": response, "rememberMe": self.remember_me}
        body: TokenResponse = await self._request(method="POST", path="/api/auth/passkey/complete", data=data, use_token=False)
        return await self._login_result(data=body)

    async def abandon_passkey_login(self, flow_id: str) -> None:
        """End a passkey flow from :meth:`begin_passkey_login` that won't be finished.

        |coro|

        Endpoint: ``POST /api/auth/passkey/abandon``

        This call needs no login. AMP answers the same whether or not the flow exists.

        AMP limits how many passkey flows the caller's IP address can have open. An open flow counts toward that limit
        until the flow runs out, so abandoning the flow frees its place sooner.

        Parameters
        ----------
        flow_id : :class:`str`
            The `flowId` from :meth:`begin_passkey_login`.

        """
        await self._request(method="POST", path="/api/auth/passkey/abandon", data={"flowId": flow_id}, use_token=False)

    @contextmanager
    def capture(self, path: Path, *, redact: bool = True) -> Generator[None]:
        """Save every request the `Session` sends, and AMP's reply, as a JSON file in `path` while the block runs.

        Every call through the `Session` is captured, logins, renewals and error replies included, from any task that
        uses the `Session` while the block runs.

        - Each file holds the request: method, path, query parameters, headers and body.
        - Each file holds the reply: status, the headers worth keeping and body.
        - A binary reply, such as a download, is kept as its content type and length only.
        - Each file is named from the method, the path with each GUID as ``{id}``, then the UTC time to the
          microsecond, eg. ``GET_api_shards_{id}_state_2026-11-13_21-52-07.123456.json``. A route's files sort in
          time order, and a file already in `path` is never written over.

        A capture that fails to write is logged as a warning, and the call carries on. While the block runs, the
        `capture_dir` the `Session` was made with, and any outer :meth:`capture` block, still get every reply too.

        .. versionadded:: 6.0.0

        Parameters
        ----------
        path : :class:`Path`
            The folder to save the captures in.
            - The folder is made when missing.
        redact : :class:`bool`, optional
            If secrets and public IP addresses are hidden in the captures or not, by default True.
            - See :func:`redact` for what is hidden.
            - With `False` the files hold your password and tokens as sent.

        Yields
        ------
        None
            Nothing, the captures go to `path`.

        """
        block: tuple[Path, bool] = (path, redact)
        self._capture_blocks.append(block)
        try:
            yield
        finally:
            self._capture_blocks.remove(block)

    async def change_expired_password(self, new_password: str) -> TokenResponse:
        """Change the password when AMP asks for a new password at login, which logs the `Session` in.

        |coro|

        Endpoint: ``POST /api/auth/change-expired-password``

        Call :meth:`change_expired_password` after :meth:`login` raised :exc:`AMPAPIPasswordChangeRequiredError`. On
        success the `Session` keeps the new password for later logins.

        Parameters
        ----------
        new_password : :class:`str`
            The new password, which has to pass :meth:`get_password_policy`.

        Returns
        -------
        :class:`TokenResponse`
            The new session's token.

        Raises
        ------
        AMPAPIRequestError
            If AMP refuses the new password.\n
            If the account doesn't need a password change.
        AMPAPIPasskeyRequiredError
            If the account also needs a second factor.

        """
        data: ExpiredPasswordRequest = {"username": self.username, "currentPassword": self._password, "newPassword": new_password}
        body: LoginResponse = await self._request(method="POST", path="/api/auth/change-expired-password", data=data, use_token=False)
        self._password = new_password
        return await self._login_result(data=body)

    async def clean_up(self) -> None:
        """Log out, then close the aiohttp `ClientSession` if the `Session` made it.

        |coro|

        Endpoint: ``POST /api/auth/logout``

        Logging out keeps a finished script from leaving its session open on AMP until the session runs out.
        A failed logout, a timeout included, is logged, not raised. The `ClientSession` closes either way.

        """
        try:
            await self.logout()
        except (AMPAPIRequestError, ClientError, TimeoutError) as error:
            LOGGER.warning("<%s.%s> | Logout failed, closing anyway | Error: %r", __class__.__name__, "clean_up", error)
        finally:
            if self._own_session is True and self._session is not None:
                await self._session.close()
                self._session = None

    async def get_capabilities(self) -> CapabilitiesResponse:
        """Get which login methods the panel offers, such as passkeys.

        |coro|

        Endpoint: ``GET /api/auth/capabilities``

        This call needs no login.

        Returns
        -------
        :class:`CapabilitiesResponse`
            The panel's passkey status and policy.

        """
        return await self._request(method="GET", path="/api/auth/capabilities", use_token=False)

    async def get_hub_token(self) -> HubTokenResponse:
        """Get a short lived token for AMP's SignalR hub, which is where live events come from.

        |coro|

        Endpoint: ``POST /api/auth/hub-token``

        Returns
        -------
        :class:`HubTokenResponse`
            The hub token, which lasts about 60 seconds.

        """
        return await self._request(method="POST", path="/api/auth/hub-token", data={})

    async def get_password_policy(self) -> PasswordPolicyResponse:
        """Get the rules a new password has to pass.

        |coro|

        Endpoint: ``GET /api/auth/password-policy``

        This call needs no login.

        Returns
        -------
        :class:`PasswordPolicyResponse`
            The password policy.

        """
        return await self._request(method="GET", path="/api/auth/password-policy", use_token=False)

    async def login(self) -> TokenResponse:
        """Log in with the username and password the `Session` was made with.

        |coro|

        Endpoint: ``POST /api/auth/login``

        You don't usually need :meth:`login`, as any call that needs a session logs in first.
        If the `Session` was already logged in, the earlier session is logged out once AMP hands over the new token.

        Returns
        -------
        :class:`TokenResponse`
            The new session's token.

        Raises
        ------
        AMPAPILoginError
            If AMP refuses the username or password.\n
            If the account is suspended. The error's `reason` reads "This account has been suspended."
        AMPAPIPasswordChangeRequiredError
            If the account has to change its password first, see :meth:`change_expired_password`.
        AMPAPIPasskeyRequiredError
            If the account needs a second factor, see :meth:`second_factor`.
        AMPAPIRequestError
            **429** - If AMP throttled the caller's IP address after failed logins `auth.login.errorThrottled`.\n
            If AMP answers with any other error status.

        """
        data: LoginRequest = {"username": self.username, "password": self._password, "rememberMe": self.remember_me}
        status, _authenticate_header, body = await self._send(method="POST", path="/api/auth/login", data=data, use_token=False)
        if status == 401:
            reason: str = body.get("message", "") if is_json_object(value=body) else ""
            raise AMPAPILoginError(username=self.username, reason=reason)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/auth/login", data=body)

        LOGGER.debug("<%s.%s> | Username: %s | Remember Me: %s", __class__.__name__, "login", self.username, self.remember_me)
        return await self._login_result(data=body)

    async def renew(self) -> TokenResponse:
        """Swap the current token for a fresh token in the same session.

        |coro|

        Endpoint: ``POST /api/auth/renew``

        You don't usually need :meth:`renew`, as a call renews the token on its own once 75% of the token's lifetime
        has passed. The old token keeps working until the session ends.

        Returns
        -------
        :class:`TokenResponse`
            The new token.

        Raises
        ------
        AMPAPIRequestError
            **401** - If the session has already ended.\n
            If AMP answers with any other error status.

        """
        status, _authenticate_header, body = await self._send(method="POST", path="/api/auth/renew", data={})
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/auth/renew", data=body)

        return self._store_token(data=body)

    async def logout(self) -> None:
        """End the current session on AMP, so every token of that session stops working.

        |coro|

        Endpoint: ``POST /api/auth/logout``

        Other logins of the same user are left alone. A later call that needs a session logs in again.
        A session AMP had already ended counts as logged out.

        Raises
        ------
        AMPAPIRequestError
            If AMP answers with an error other than 401. The `Session` forgets the token either way.

        """
        if self._token is None:
            return

        status, _authenticate_header, body = await self._send(method="POST", path="/api/auth/logout", data={})
        self._forget_token()

        # A 401 means AMP had already ended this session, which is what we were after.
        if status == 401:
            return
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/auth/logout", data=body)

    async def preview_invite(self, token: str) -> InvitePreviewResponse:
        """Get who an invite code is for, without using it.

        |coro|

        Endpoint: ``POST /api/invites/preview``

        This call needs no login.

        Parameters
        ----------
        token : :class:`str`
            The invite code.

        Returns
        -------
        :class:`InvitePreviewResponse`
            The username and display name the account will get.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the invite code is wrong, used, revoked or out of date `invalid_or_expired`.

        """
        return await self._request(method="POST", path="/api/invites/preview", data={"token": token}, use_token=False)

    async def reauth(self, password: Optional[str] = None) -> None:
        """Confirm the password again, which AMP asks for before sensitive changes.

        |coro|

        Endpoint: ``POST /api/auth/reauth``

        Parameters
        ----------
        password : Union[:class:`str`, None], optional
            The password to confirm with, by default None.
            - Without a password, the password the `Session` logs in with is used.

        Raises
        ------
        AMPAPIRequestError
            **401** - If AMP refuses the password `auth.error.reproofRejected`.

        """
        confirm_password: str = password if password is not None else self._password
        await self._request(method="POST", path="/api/auth/reauth", data={"password": confirm_password})

    async def reauth_with_passkey(self, flow_id: str, response: Mapping[str, Any]) -> None:
        """Confirm the logged in user with a passkey instead of the password, as :meth:`reauth` does.

        |coro|

        Endpoint: ``POST /api/auth/passkey/reauth``

        Start the flow with :meth:`begin_passkey_login`, then send the authenticator's answer to
        :meth:`reauth_with_passkey` instead of to :meth:`complete_passkey_login`.

        Parameters
        ----------
        flow_id : :class:`str`
            The `flowId` from :meth:`begin_passkey_login`.
        response : Mapping[:class:`str`, Any]
            The authenticator's answer, as :meth:`complete_passkey_login` takes it. The passkey has to be one of the
            logged in user's passkeys.

        Raises
        ------
        AMPAPIRequestError
            **400** - If AMP can't read the answer, from AMP's docs and not seen live.\n
            **401** - If AMP refuses the answer, from AMP's docs and not seen live.\n
            **401** - If the passkey belongs to another account, from AMP's docs and not seen live.

        """
        await self._request(method="POST", path="/api/auth/passkey/reauth", data={"flowId": flow_id, "response": response})

    async def second_factor(self, code: str) -> TokenResponse:
        """Finish a login that needs a second factor, using one of the account's recovery codes.

        |coro|

        Endpoint: ``POST /api/auth/login/second-factor``

        Call :meth:`second_factor` after :meth:`login` raised :exc:`AMPAPIPasskeyRequiredError`. Each recovery code works
        once, see :meth:`AccountModule.generate_recovery_codes`.

        .. warning::
            The library can't repeat a login made with a recovery code.

            - The new session renews like any other.
            - Once AMP ends the session, eg. a logout or an admin's force logout, or the session runs out because no call
              renewed the session in time, the next call that needs a session logs in by password and raises
              :exc:`AMPAPIPasskeyRequiredError`. Catch :exc:`AMPAPIPasskeyRequiredError`, then call :meth:`second_factor`
              again with a new recovery code.
            - With `remember_me` the session lasts 28 days instead of 8 hours.

        Parameters
        ----------
        code : :class:`str`
            One of the account's recovery codes.

        Returns
        -------
        :class:`TokenResponse`
            The new session's token.

        Raises
        ------
        AMPAPIRequestError
            **401** - If the recovery code is wrong or already used `auth.login.recoveryCodeRejected`.
        AMPAPIPasswordChangeRequiredError
            If the account also has to change its password.

        """
        data: SecondFactorRequest = {"username": self.username, "password": self._password, "code": code, "rememberMe": self.remember_me}
        body: LoginResponse = await self._request(method="POST", path="/api/auth/login/second-factor", data=data, use_token=False)
        return await self._login_result(data=body)
