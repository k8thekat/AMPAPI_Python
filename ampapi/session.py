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
from datetime import UTC, datetime
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

    from ._types import CapabilitiesResponse, HubTokenResponse, LoginResponse, PasswordPolicyResponse, QueryParameters, TokenResponse

__all__ = ("Session",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Session:
    """One login to an AMP 3 panel.

    It logs in on the first call that needs it, renews the token before it runs out, and logs in again if AMP ends the
    session (a logout elsewhere, or an admin's force logout). Calls made at the same time share one login.
    Hand it to a :class:`Panel` for the API calls.

    .. note::
        AMP 3 sessions are Bearer tokens. A login lasts 8 hours, or 28 days with `remember_me`. Each login is its own
        session; ending one leaves the others alone.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    url : :class:`str`
        The panel's URL, eg. ``"http://192.168.1.10:8443"``.
    username : :class:`str`
        The AMP username to log in as.
    password : :class:`str`
        The password for `username`.
    remember_me : :class:`bool`, optional
        If the login should ask for the long (28 day) token or not, by default False.
    session : Union[:class:`ClientSession`, None], optional
        An aiohttp session to send requests through, by default None.
        Without one we make our own, and :meth:`clean_up` closes it. :meth:`clean_up` logs out either way.

    """

    # How far through a token's lifetime we renew it, the same point AMP's web panel uses.
    _renew_point: ClassVar[float] = 0.75

    def __init__(  # noqa: D107
        self,
        url: str,
        username: str,
        password: str,
        *,
        remember_me: bool = False,
        session: Optional[ClientSession] = None,
    ) -> None:
        self.url: str = url.rstrip("/")
        self.username: str = username
        self.remember_me: bool = remember_me
        self._password: str = password
        self._session: Optional[ClientSession] = session
        self._own_session: bool = session is None
        self._token: Optional[str] = None
        self._expiration: Optional[datetime] = None
        self._renew_after: Optional[datetime] = None
        self._claims: dict[str, Any] = {}
        self._login_lock: asyncio.Lock = asyncio.Lock()

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
        data: Optional[Union[dict[str, Any], list[Any], bytes]] = None,
        *,
        files: Optional[Mapping[str, bytes]] = None,
        parameters: Optional[QueryParameters] = None,
        raw_bytes: bool = False,
        use_token: bool = True,
    ) -> tuple[int, str, Any]:
        """Send one request and decode the reply. Raises nothing for an error status, the caller decides.

        `data` is sent as JSON, or as it is with ``Content-Type: application/octet-stream`` when it's bytes. `files` is
        sent as the web panel's upload form instead, a `files` part and a `paths` part for each one.

        Returns
        -------
        tuple[:class:`int`, :class:`str`, Any]
            The HTTP status, the ``WWW-Authenticate`` header (empty when not sent) and the decoded JSON body,
            `None` for an empty one. With `raw_bytes` a successful reply is the bytes as they came.

        """
        if self._session is None:
            self._session = ClientSession()
        headers: dict[str, str] = {"Accept": "*/*" if raw_bytes is True else "application/json"}
        if use_token is True and self._token is not None:
            headers["Authorization"] = f"Bearer {self._token}"

        json_body: Optional[Union[dict[str, Any], list[Any]]] = None
        raw_body: Optional[Union[bytes, FormData]] = None
        if isinstance(data, bytes):
            raw_body = data
            headers["Content-Type"] = "application/octet-stream"
        elif files is not None:
            # A new form for each send, as aiohttp sends a form only once and a dead session sends it again.
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
        body: Any = json.loads(reply) if reply else None
        return status, authenticate_header, body

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

    def _login_result(self, data: LoginResponse) -> TokenResponse:
        """Keep the token from a login-like call, or raise for the follow-up step AMP asked for instead."""
        if "passwordChangeRequired" in data:
            raise AMPAPIPasswordChangeRequiredError(username=self.username, reason=data["reason"])
        if "passkeyRequired" in data:
            raise AMPAPIPasskeyRequiredError(username=self.username)
        return self._store_token(data=data)

    async def _ensure_login(self, used_token: Optional[str] = None) -> None:
        """Log in, or renew, when needed. Calls made at the same time wait for one login.

        Parameters
        ----------
        used_token : Union[:class:`str`, None], optional
            The token a request was refused with, by default None.
            If we already hold a different one, another call has logged in again since, so we don't.

        """
        async with self._login_lock:
            if used_token is not None and used_token == self._token:
                self._forget_token()

            if self._token is None:
                await self.login()
            elif self._renew_after is not None and datetime.now(tz=UTC) >= self._renew_after:
                try:
                    await self.renew()
                except AMPAPIRequestError as error:
                    # The session ended between calls, so a renew is refused and we start a new one.
                    if error.status != 401:
                        raise
                    await self.login()

    async def _send_with_login(
        self,
        method: str,
        path: str,
        data: Optional[Union[dict[str, Any], list[Any], bytes]] = None,
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
            The HTTP status and the decoded JSON body, `None` for an empty one, or the bytes with `raw_bytes`.

        Raises
        ------
        AMPAPIRequestError
            If a login this needed was refused.

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
        data: Optional[Union[dict[str, Any], list[Any]]] = None,
        *,
        parameters: Optional[QueryParameters] = None,
        use_token: bool = True,
    ) -> Any:
        """Send a request with `_send_with_login`, raising for an error status.

        Raises
        ------
        AMPAPIRequestError
            If AMP answers with an error status.

        """
        status, body = await self._send_with_login(
            method=method,
            path=path,
            data=data,
            parameters=parameters,
            use_token=use_token,
        )
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method=method, path=path, data=body)
        return body

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
        path: str = "/api/auth/change-expired-password"
        data: dict[str, Any] = {"username": self.username, "currentPassword": self._password, "newPassword": new_password}
        status, _authenticate_header, body = await self._send(method="POST", path=path, data=data, use_token=False)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path=path, data=body)

        self._password = new_password
        return self._login_result(data=body)

    async def clean_up(self) -> None:
        """Log out, then close the aiohttp session if we made it.

        |coro|

        Endpoint: ``POST /api/auth/logout``

        Logging out here keeps a finished script from leaving its session open on AMP for the rest of its 8 hours.
        A failed logout is logged and the aiohttp session still closes.

        """
        try:
            await self.logout()
        except (AMPAPIRequestError, ClientError) as error:
            LOGGER.warning("<%s.%s> | Logout failed, closing anyway | Error: %s", __class__.__name__, "clean_up", error)

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
        data: dict[str, Any] = {"username": self.username, "password": self._password, "rememberMe": self.remember_me}
        status, _authenticate_header, body = await self._send(method="POST", path="/api/auth/login", data=data, use_token=False)
        if status == 401:
            reason: str = body.get("message", "") if _is_json_object(value=body) else ""
            raise AMPAPILoginError(username=self.username, reason=reason)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/auth/login", data=body)

        LOGGER.debug("<%s.%s> | Username: %s | Remember Me: %s", __class__.__name__, "login", self.username, self.remember_me)
        return self._login_result(data=body)

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
            If the session has already ended (401).

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
        path: str = "/api/auth/login/second-factor"
        data: dict[str, Any] = {"username": self.username, "password": self._password, "code": code, "rememberMe": self.remember_me}
        status, _authenticate_header, body = await self._send(method="POST", path=path, data=data, use_token=False)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path=path, data=body)
        return self._login_result(data=body)
