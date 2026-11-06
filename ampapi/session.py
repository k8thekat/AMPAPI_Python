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
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Self

from aiohttp import ClientSession

from .errors import (
    AMPAPILoginError,
    AMPAPIPasskeyRequiredError,
    AMPAPIPasswordChangeRequiredError,
    AMPAPIRequestError,
    _is_json_object,  # pyright: ignore[reportPrivateUsage]
)

if TYPE_CHECKING:
    from types import TracebackType

    from ._types import (
        CapabilitiesResponse,
        HealthStatusResponse,
        HubTokenResponse,
        LoginResponse,
        PasswordPolicyResponse,
        PermissionsResponse,
        ProfileResponse,
        TokenResponse,
    )

__all__ = ("Session",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Session:
    """One login to an AMP 3 panel.

    It logs in on the first call that needs it, renews the token before it runs out, and logs in again if AMP ends the
    session (a logout elsewhere, or an admin's force logout). Calls made at the same time share one login.

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
        Without one we make our own, and :meth:`clean_up` closes it.

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

    async def _send(self, method: str, path: str, data: Optional[dict[str, Any]] = None, *, use_token: bool = True) -> tuple[int, str, Any]:
        """Send one request and decode the reply. Raises nothing for an error status, the caller decides.

        Returns
        -------
        tuple[:class:`int`, :class:`str`, Any]
            The HTTP status, the ``WWW-Authenticate`` header (empty when not sent) and the decoded JSON body,
            `None` for an empty one.

        """
        if self._session is None:
            self._session = ClientSession()

        headers: dict[str, str] = {"Accept": "application/json"}
        if use_token is True and self._token is not None:
            headers["Authorization"] = f"Bearer {self._token}"

        LOGGER.debug("<%s.%s> | Method: %s | Path: %s", __class__.__name__, "_send", method, path)
        async with self._session.request(method=method, url=self.url + path, json=data, headers=headers) as res:
            text: str = await res.text()
            challenge: str = res.headers.get("WWW-Authenticate", "")
            status: int = res.status

        # AMP answers some calls (logout, reauth) with an empty 204.
        body: Any = json.loads(text) if text else None
        return status, challenge, body

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

    async def _request(self, method: str, path: str, data: Optional[dict[str, Any]] = None) -> Any:
        """Send a request that needs a session, logging in first when we have to.

        A 401 for a token AMP no longer accepts gets one new login and a second try.

        Raises
        ------
        AMPAPIRequestError
            If AMP answers with an error status.

        """
        await self._ensure_login()
        used_token: Optional[str] = self._token
        status, challenge, body = await self._send(method=method, path=path, data=data)

        if status == 401 and "invalid_token" in challenge:
            LOGGER.debug("<%s.%s> | Session ended by AMP, logging in again | Path: %s", __class__.__name__, "_request", path)
            await self._ensure_login(used_token=used_token)
            status, challenge, body = await self._send(method=method, path=path, data=data)

        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method=method, path=path, data=body)
        return body

    async def _request_public(self, path: str) -> Any:
        """GET a call that needs no session."""
        status, _challenge, body = await self._send(method="GET", path=path, use_token=False)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="GET", path=path, data=body)
        return body

    async def change_expired_password(self, new_password: str) -> TokenResponse:
        """Change the password AMP asked for at login, which logs in.

        |coro|

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
        data: dict[str, Any] = {"username": self.username, "currentPassword": self._password, "newPassword": new_password}
        status, _challenge, body = await self._send(method="POST", path="/api/Auth/change-expired-password", data=data, use_token=False)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/Auth/change-expired-password", data=body)

        self._password = new_password
        return self._login_result(data=body)

    async def clean_up(self) -> None:
        """Close the aiohttp session if we made it.

        |coro|

        .. note::
            This does not log out; AMP keeps the session until it runs out. Call :meth:`logout` first to end it.

        """
        if self._own_session is True and self._session is not None:
            await self._session.close()
            self._session = None

    async def get_capabilities(self) -> CapabilitiesResponse:
        """Get which login methods the panel offers, such as passkeys.

        |coro|

        Returns
        -------
        :class:`CapabilitiesResponse`
            The panel's passkey status and policy.

        """
        return await self._request_public(path="/api/auth/capabilities")

    async def get_health_status(self) -> HealthStatusResponse:
        """Get the panel's state, eg. still in first-run setup or ``"ready"``.

        |coro|

        Returns
        -------
        :class:`HealthStatusResponse`
            The panel's phase, plus the preview countdown on a preview build.

        """
        return await self._request_public(path="/api/health/status")

    async def get_hub_token(self) -> HubTokenResponse:
        """Get a short lived token for AMP's SignalR hub, which is where live events come from.

        |coro|

        Returns
        -------
        :class:`HubTokenResponse`
            The hub token; it lasts about 60 seconds.

        """
        return await self._request(method="POST", path="/api/auth/hub-token", data={})

    async def get_password_policy(self) -> PasswordPolicyResponse:
        """Get the rules a new password has to pass.

        |coro|

        Returns
        -------
        :class:`PasswordPolicyResponse`
            The password policy.

        """
        return await self._request_public(path="/api/Auth/password-policy")

    async def get_permissions(self) -> PermissionsResponse:
        """Get the logged in user's grants, along with every permission AMP knows about.

        |coro|

        Returns
        -------
        :class:`PermissionsResponse`
            The grants, the catalog and the user's role IDs.

        """
        return await self._request(method="GET", path="/api/me/permissions")

    async def get_profile(self) -> ProfileResponse:
        """Get the logged in user's own account.

        |coro|

        Returns
        -------
        :class:`ProfileResponse`
            The user's ID, names and email.

        """
        return await self._request(method="GET", path="/api/profile")

    async def login(self) -> TokenResponse:
        """Log in with the username and password this session was made with.

        |coro|

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
        status, _challenge, body = await self._send(method="POST", path="/api/Auth/login", data=data, use_token=False)
        if status == 401:
            reason: str = body.get("message", "") if _is_json_object(value=body) else ""
            raise AMPAPILoginError(username=self.username, reason=reason)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/Auth/login", data=body)

        LOGGER.debug("<%s.%s> | Username: %s | Remember Me: %s", __class__.__name__, "login", self.username, self.remember_me)
        return self._login_result(data=body)

    async def renew(self) -> TokenResponse:
        """Swap the current token for a fresh one in the same session.

        |coro|

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
        status, _challenge, body = await self._send(method="POST", path="/api/Auth/renew", data={})
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/Auth/renew", data=body)
        return self._store_token(data=body)

    async def logout(self) -> None:
        """End this session; every token it was given stops working.

        |coro|

        Other logins of the same user are left alone. A later call that needs a session logs in again.
        """
        if self._token is None:
            return

        status, _challenge, body = await self._send(method="POST", path="/api/auth/logout", data={})
        self._forget_token()
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/auth/logout", data=body)

    async def reauth(self, password: Optional[str] = None) -> None:
        """Confirm the password again, which AMP asks for before sensitive changes.

        |coro|

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
        confirm: str = password if password is not None else self._password
        await self._request(method="POST", path="/api/auth/reauth", data={"password": confirm})

    async def second_factor(self, code: str) -> TokenResponse:
        """Finish a login that needs a second factor, using one of the account's recovery codes.

        |coro|

        Call this after :meth:`login` raised :exc:`AMPAPIPasskeyRequiredError`.

        .. warning::
            Not yet tested live. Passkeys need the panel on HTTPS.

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
            If AMP refuses the code.
        AMPAPIPasswordChangeRequiredError
            If the account also has to change its password.

        """
        data: dict[str, Any] = {"username": self.username, "password": self._password, "code": code, "rememberMe": self.remember_me}
        status, _challenge, body = await self._send(method="POST", path="/api/Auth/login/second-factor", data=data, use_token=False)
        if not 200 <= status < 300:
            raise AMPAPIRequestError(status=status, method="POST", path="/api/Auth/login/second-factor", data=body)
        return self._login_result(data=body)
