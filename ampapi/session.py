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
import json
import logging
from datetime import UTC, datetime, timedelta
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Self, Union

from aiohttp import ClientError, ClientSession, FormData

from .errors import (
    AMPAPILoginError,
    AMPAPIPasskeyRequiredError,
    AMPAPIPasswordChangeRequiredError,
    AMPAPIRequestError,
    _is_json_object,  # pyright: ignore[reportPrivateUsage]
)

if TYPE_CHECKING:
    from collections.abc import Mapping
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
        PasswordPolicyResponse,
        QueryParameters,
        SecondFactorRequest,
        TokenClaims,
        TokenResponse,
    )

__all__ = ("Session",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Session:
    """One login to an AMP 3 panel.

    It logs in on the first call that needs it, renews the token before it runs out, and logs in again if AMP ends the
    session (a logout elsewhere, or an admin's force logout). Calls made at the same time share one login, and when AMP
    refuses it they all raise its error instead of each sending it again. Hand it to a :class:`Panel` for the API calls.

    While AMP's database or message bus is down (a 503 with ``"session.storeUnavailable"`` or
    ``"common.error.busUnavailable"``), a request is sent again after 1, 2 and 4 seconds, then 8 seconds twice, the way
    the web panel does. A renew AMP refuses for any other reason than an ended session is logged, and we keep using the
    token until it runs out.

    .. note::
        AMP 3 sessions are Bearer tokens. A login lasts 8 hours, or 28 days with `remember_me`. Each login is its own
        session; ending one leaves the others alone.

    .. note::
        Any call that needs a session logs in first when it has to, so it can raise :exc:`AMPAPILoginError`,
        :exc:`AMPAPIPasskeyRequiredError` or :exc:`AMPAPIPasswordChangeRequiredError` from that login.

    .. warning::
        A login finished with :meth:`second_factor` can't be made again on its own, as each recovery code works once.
        Once AMP ends that session, or it runs out, the next call raises :exc:`AMPAPIPasskeyRequiredError`. Catch it and
        call :meth:`second_factor` with a new code. With `remember_me` a login lasts 28 days.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    url : :class:`str`
        The panel's URL, eg. ``"http://192.168.1.10:8443"``.
    username : :class:`str`
        The AMP username to log in as.
        Before :meth:`accept_invite` it can be anything, eg. ``""``, as the invite's username replaces it.
    password : :class:`str`
        The password for `username`.
    remember_me : :class:`bool`, optional
        If the login should ask for the long (28 day) token or not, by default False.
    session : Union[:class:`ClientSession`, None], optional
        An aiohttp session to send requests through, by default None.
        Without one we make our own, and :meth:`clean_up` closes it. :meth:`clean_up` logs out either way.

    Attributes
    ----------
    url : :class:`str`
        The panel's URL, without a trailing ``/``.
    username : :class:`str`
        The AMP username we log in as. :meth:`accept_invite` sets it to the invite's.
    remember_me : :class:`bool`
        If a login asks for the long (28 day) token or not.

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
        """If this session may only add a passkey (the token's ``amp:scope`` claim is ``"enrol"``).

        AMP hands these out when the passkey policy is ``"Required"`` and the account has no passkey yet.
        """
        return self._claims.get("amp:scope") == "enrol"

    @property
    def expiration(self) -> Optional[datetime]:
        """When the current token runs out, `None` when not logged in."""
        return self._expiration

    @property
    def logged_in(self) -> bool:
        """If we hold a token that has not run out yet."""
        return self._expiration is not None and datetime.now(tz=UTC) < self._expiration

    @property
    def session_id(self) -> Optional[str]:
        """AMP's ID for this login (the token's `sid` claim); it stays the same across renewals."""
        return self._claims.get("sid")

    @property
    def user_id(self) -> Optional[str]:
        """The logged in user's ID, the same as `ProfileResponse.id`."""
        return self._claims.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier")

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
    ) -> tuple[int, str, Any]:
        """Send a request and decode the reply. Raises nothing for an error status, the caller decides.

        `data` is sent as JSON, or as it is with ``Content-Type: application/octet-stream`` when it's bytes. `files` is
        sent as the web panel's upload form instead, a `files` part and a `paths` part for each one.

        Every request goes through here, logins and renewals too. A 503 whose `code` says AMP's database
        (``"session.storeUnavailable"``) or message bus (``"common.error.busUnavailable"``) is down is sent again after
        1, 2 and 4 seconds, then 8 seconds twice, the way the web panel does.

        Returns
        -------
        tuple[:class:`int`, :class:`str`, Any]
            The HTTP status, the ``WWW-Authenticate`` header (empty when not sent) and the decoded JSON body,
            `None` for an empty one, or the text of a body that isn't JSON, eg. a proxy's error page.
            With `raw_bytes` a successful reply is the bytes as they came.

        """
        if self._session is None:
            self._session = ClientSession()

        headers: dict[str, str] = {"Accept": "*/*" if raw_bytes is True else "application/json"}
        if use_token is True and self._token is not None:
            headers["Authorization"] = f"Bearer {self._token}"

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

            LOGGER.debug("<%s.%s> | Method: %s | Path: %s | Parameters: %s", __class__.__name__, "_send", method, path, parameters)
            async with self._session.request(
                method=method,
                url=self.url + path,
                params=parameters,
                json=json_body,
                data=raw_body,
                headers=headers,
            ) as res:
                reply: bytes = await res.read()
                authenticate_header: str = res.headers.get("WWW-Authenticate", "")
                status: int = res.status

            # A download comes back as bytes, but AMP's errors are JSON either way.
            if raw_bytes is True and 200 <= status < 300:
                return status, authenticate_header, reply
            # AMP answers some calls (logout, reauth) with an empty 204, and some GETs use a 204 for "nothing yet".
            body: Any = None
            if reply:
                try:
                    body = json.loads(reply)
                except ValueError:
                    # A proxy in front of AMP answers with its own page, eg. an HTML 502, so we keep it as text
                    body = reply.decode(encoding="utf-8", errors="replace")
            code: Optional[str] = body.get("code") if _is_json_object(value=body) else None
            if status != 503 or code not in self._outage_codes or retries == len(self._outage_delays):
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

    async def _login_result(self, data: LoginResponse) -> TokenResponse:
        """Keep the token from a login-like call, or raise for the follow-up step AMP asked for instead.

        A token we already hold is logged out before the new one replaces it, so its session isn't left open on AMP.
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
        """Log in, or renew, when needed. Calls made at the same time wait for one login.

        A call that waited through a login that failed raises that login's error, rather than sending the same login
        again. A renew AMP refuses for anything but an ended session (eg. a 503) is logged, and we keep the token
        until it runs out, trying the renew again after `_renew_retry`.

        Parameters
        ----------
        used_token : Union[:class:`str`, None], optional
            The token a request was refused with, by default None.
            If we already hold a different one, another call has logged in again since, so we don't.

        """
        login_attempt: int = self._login_attempts
        async with self._login_lock:
            # A login failed while we waited, so we raise its error instead of sending the same password again
            if login_attempt != self._login_attempts and self._token is None and self._login_error is not None:
                raise self._login_error
            # A token AMP refused, or one that has run out, can't be renewed, so we log in again
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
    ) -> tuple[int, Any]:
        """Send a request, logging in first when it needs a session and we have to. Raises nothing for an error status.

        A 401 for a token AMP no longer accepts gets one new login and a second try. With `use_token` set to `False`
        we send no token and never log in, for the calls that need no session. The rest go to `_send` as they are.

        Returns
        -------
        tuple[:class:`int`, Any]
            The HTTP status and the decoded JSON body, `None` for an empty one, the text of a body that isn't JSON, or
            the bytes with `raw_bytes`.

        Raises
        ------
        AMPAPILoginError
            If a login this needed was refused, as :meth:`login` raises it.
        AMPAPIPasskeyRequiredError
            If a login this needed asks for a second factor.
        AMPAPIPasswordChangeRequiredError
            If a login this needed asks for a new password first.
        AMPAPIRequestError
            If a login this needed got any other error status.

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
    ) -> Any:
        """Send a request with `_send_with_login`, raising for an error status.

        Our own calls and every module's, through `Base._request`, go this way. The parameters are `Base._request`'s.

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
            If a login this needed was refused.
        AMPAPIPasskeyRequiredError
            If a login this needed asks for a second factor.
        AMPAPIPasswordChangeRequiredError
            If a login this needed asks for a new password first.

        """
        status, body = await self._send_with_login(
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

    async def accept_invite(
        self,
        token: str,
        email: str,
        *,
        display_name: Optional[str] = None,
        locale: str = "en",
    ) -> InviteAcceptedResponse:
        """Make the account an invite was for, which logs this session in as it.

        |coro|

        Endpoints: ``POST /api/invites/preview`` for the invite's username, then ``POST /api/invites/accept``

        This one needs no session, and no :class:`Panel`. Make a :class:`Session` with the password the new account
        should have, and any `username`, eg. ``""``, then call this. The account's username is the one the invite was
        made with (see :meth:`preview_invite`), so we read it from the invite first and keep it as `username`.
        From then on the session renews and logs in again as the new account, like any other login.
        A session this one already held is logged out once the account exists. A failed logout is logged, not raised.

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
            The new account's session token, which this session keeps.

        Raises
        ------
        AMPAPIRequestError
            If the code is wrong, used, revoked or out of date (404 from the preview, ``"invalid_or_expired"``), or the
            session's password is too weak for :meth:`get_password_policy` (400).

        """
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

    async def change_expired_password(self, new_password: str) -> TokenResponse:
        """Change the password AMP asked for at login, which logs in.

        |coro|

        Endpoint: ``POST /api/auth/change-expired-password``

        Call this after :meth:`login` raised :exc:`AMPAPIPasswordChangeRequiredError`. On success the new password is
        kept for later logins.

        Parameters
        ----------
        new_password : :class:`str`
            The new password; it has to pass :meth:`get_password_policy`.

        Returns
        -------
        :class:`TokenResponse`
            The new session's token.

        Raises
        ------
        AMPAPIRequestError
            If AMP refuses the new password, or the account doesn't need a change.
        AMPAPIPasskeyRequiredError
            If the account also needs a second factor.

        """
        data: ExpiredPasswordRequest = {"username": self.username, "currentPassword": self._password, "newPassword": new_password}
        body: LoginResponse = await self._request(method="POST", path="/api/auth/change-expired-password", data=data, use_token=False)
        self._password = new_password
        return await self._login_result(data=body)

    async def clean_up(self) -> None:
        """Log out, then close the aiohttp session if we made it.

        |coro|

        Endpoint: ``POST /api/auth/logout``

        Logging out here keeps a finished script from leaving its session open on AMP for the rest of its 8 hours.
        A failed logout, a timeout included, is logged and the aiohttp session still closes, whatever the logout raised.

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
            The hub token; it lasts about 60 seconds.

        """
        return await self._request(method="POST", path="/api/auth/hub-token", data={})

    async def get_password_policy(self) -> PasswordPolicyResponse:
        """Get the rules a new password has to pass.

        |coro|

        Endpoint: ``GET /api/auth/password-policy``

        Returns
        -------
        :class:`PasswordPolicyResponse`
            The password policy.

        """
        return await self._request(method="GET", path="/api/auth/password-policy", use_token=False)

    async def login(self) -> TokenResponse:
        """Log in with the username and password this session was made with.

        |coro|

        Endpoint: ``POST /api/auth/login``

        You don't usually need this, any call that needs a session logs in first.
        When this session is already logged in, its old session is logged out once AMP hands over the new token.
        A failed logout is logged, not raised.

        Returns
        -------
        :class:`TokenResponse`
            The new session's token.

        Raises
        ------
        AMPAPILoginError
            If AMP refuses the username or password.
        AMPAPIPasswordChangeRequiredError
            If the account has to change its password first, see :meth:`change_expired_password`.
        AMPAPIPasskeyRequiredError
            If the account needs a second factor, see :meth:`second_factor`.
        AMPAPIRequestError
            If AMP answers with any other error status.

        """
        data: LoginRequest = {"username": self.username, "password": self._password, "rememberMe": self.remember_me}
        status, _authenticate_header, body = await self._send(method="POST", path="/api/auth/login", data=data, use_token=False)
        if status == 401:
            reason: str = body.get("message", "") if _is_json_object(value=body) else ""
            raise AMPAPILoginError(username=self.username, reason=reason)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/auth/login", data=body)

        LOGGER.debug("<%s.%s> | Username: %s | Remember Me: %s", __class__.__name__, "login", self.username, self.remember_me)
        return await self._login_result(data=body)

    async def renew(self) -> TokenResponse:
        """Swap the current token for a fresh one in the same session.

        |coro|

        Endpoint: ``POST /api/auth/renew``

        Calls renew on their own once 75% of a token's lifetime has passed. The old token keeps working until the
        session ends.

        Returns
        -------
        :class:`TokenResponse`
            The new token.

        Raises
        ------
        AMPAPIRequestError
            If the session has already ended (401), or AMP answers with any other error status.

        """
        status, _authenticate_header, body = await self._send(method="POST", path="/api/auth/renew", data={})
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/auth/renew", data=body)

        return self._store_token(data=body)

    async def logout(self) -> None:
        """End this session; every token it was given stops working.

        |coro|

        Endpoint: ``POST /api/auth/logout``

        Other logins of the same user are left alone. A later call that needs a session logs in again.
        A session AMP had already ended counts as logged out.

        Raises
        ------
        AMPAPIRequestError
            If AMP answers with an error other than 401. The token is forgotten either way.

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

        This one needs no session.

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
            If the code is wrong, used, revoked or out of date (404, ``"invalid_or_expired"``).

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
            Without one we use the password this session logged in with.

        Raises
        ------
        AMPAPIRequestError
            If AMP refuses the password (401, ``"auth.error.reproofRejected"``).

        """
        confirm_password: str = password if password is not None else self._password
        await self._request(method="POST", path="/api/auth/reauth", data={"password": confirm_password})

    async def second_factor(self, code: str) -> TokenResponse:
        """Finish a login that needs a second factor, using one of the account's recovery codes.

        |coro|

        Endpoint: ``POST /api/auth/login/second-factor``

        Call this after :meth:`login` raised :exc:`AMPAPIPasskeyRequiredError`. Each code works once; see
        :meth:`AccountModule.generate_recovery_codes`.

        .. warning::
            The session renews like any other, but it can't log in again on its own. Once AMP ends it (a logout, an
            admin's force logout), or it runs out because no call renewed it in time, the next call that needs a
            session logs in by password and raises :exc:`AMPAPIPasskeyRequiredError`. Catch it and call this again with
            a new code. With `remember_me` a login lasts 28 days instead of 8 hours.

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
            If AMP refuses the code (401, ``"auth.login.recoveryCodeRejected"``), a wrong or already used one alike.
        AMPAPIPasswordChangeRequiredError
            If the account also has to change its password.

        """
        data: SecondFactorRequest = {"username": self.username, "password": self._password, "code": code, "rememberMe": self.remember_me}
        body: LoginResponse = await self._request(method="POST", path="/api/auth/login/second-factor", data=data, use_token=False)
        return await self._login_result(data=body)
