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

import asyncio
import logging
from dataclasses import fields
from types import TracebackType
from typing import Any, Optional, Self, Union

import aiohttp

from .modules import APIParams

__all__ = ("Bridge",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Bridge(APIParams):
    """Handles the API login credentials for connecting to AMP.

    Simply create the class similar to the example below and then access any other API class you wish.\n
    Then when creating any API class,  this will pull login details from the :py:class:`Bridge`.

    .. code-block:: python
        :linenos:

        # This is to handle login details.
        _params = APIParams(url="http://192.168.13.130:8080", user="bot_username", password="bot_password")
        _bridge: Bridge = Bridge(api_params=_params)
        del _params

    A user that signs in through an OIDC provider has no password, so set `auth_mode` to
    :attr:`AuthMode.oidc <ampapi._enums.AuthMode.oidc>` on the :class:`APIParams` instead.
    Your app sends the user to the URL from :meth:`~Core.get_oidc_login_url`, catches the redirect to `redirect_uri` and
    passes the `code` and `state` it carries to :meth:`~Core.oidc_login`. After that every call uses the stored session.

    .. code-block:: python
        :linenos:

        _params = APIParams(url="http://192.168.13.130:8080", auth_mode=AuthMode.oidc)
        _bridge: Bridge = Bridge(api_params=_params)
        controller = Controller()

        # Send the user's browser to this URL
        login_url = await controller.get_oidc_login_url(redirect_uri="https://example.com/callback")

        # Your app receives the redirect with `code` and `state` in its query
        await controller.oidc_login(code=code, state=state, redirect_uri="https://example.com/callback")

    .. note::
        Each :class:`Bridge`, the singleton or one made with ``singleton=False``, holds its own
        :class:`aiohttp.ClientSession`, and every object made with it sends its calls through that session.
        It is made on the first call, and a session from an event loop that has finished is replaced.
        Close it with ``await bridge.clean_up()``, ``async with bridge:`` or :meth:`~Base.clean_up` on your :class:`Controller`.
        To use your own, pass it as `session` or set :attr:`session`. It is yours, so it is never closed for you.


    .. versionchanged:: 5.0.0
        :class:`Bridge` added optional parameter to allow for non-singleton usage.
        Takes the `auth_mode` setting from :class:`APIParams`.
        Holds the :class:`aiohttp.ClientSession` its objects share, which :meth:`clean_up` closes.
        Takes `session`, which moved here from :class:`Base` and :class:`Controller`.

    Parameters
    ----------
    api_params : :class:`APIParams`
        The prebuilt class to pass login credentials to <Bridge>.
    singleton : :class:`bool`, optional
        If `True`, the :class:`Bridge` will be created as a singleton, by default True.
    session : Union[:class:`aiohttp.ClientSession`, None], optional
        A session for every object made with this :class:`Bridge` to send its calls through, by default None.
        It is never closed for you, and without one the :class:`Bridge` makes its own on the first call.
        Only the first ``Bridge()`` of a singleton takes it, so set :attr:`session` after that.

    """

    # This is the session we made, and only `clean_up` closes it
    _client_session: Union[aiohttp.ClientSession, None]
    # The event loop our session was made in
    _client_session_loop: Union[asyncio.AbstractEventLoop, None]
    # A session passed in is the caller's, we use it while it is open and never close it
    _external_session: Union[aiohttp.ClientSession, None]
    # The logins running now, keyed by Instance ID like `_sessions`
    _logins_pending: dict[str, asyncio.Future[None]]

    @property
    def session(self) -> Union[aiohttp.ClientSession, None]:
        """The :class:`aiohttp.ClientSession` every object made with this :class:`Bridge` sends its calls through.

        Reading it gives a session passed in while it is open, otherwise the one we made, which is None until the first
        call. Setting it uses your session from the next call on, and it is never closed for you. Setting None goes back
        to the session we make.

        .. versionadded:: 5.0.0

        """
        if self._external_session is not None and self._external_session.closed is False:
            return self._external_session
        return self._client_session

    @session.setter
    def session(self, value: Union[aiohttp.ClientSession, None]) -> None:
        self._external_session = value

    def __new__(  # noqa: D417
        cls,
        api_params: APIParams,  # noqa: ARG004
        singleton: bool = True,
        session: Optional[aiohttp.ClientSession] = None,  # noqa: ARG004
        *args: Any,
        **kwargs: Any,
    ) -> Union["Bridge", Self]:
        """Controls instance creation, returning a shared instance when ``singleton=True``.

        Parameters
        ----------
        api_params : :class:`APIParams`
            The prebuilt class to handle login credentials.
        singleton : :class:`bool`, optional
            If `True`, returns the existing shared instance if one exists, by default True.
        session : Union[:class:`aiohttp.ClientSession`, None], optional
            Taken by :meth:`__init__`, by default None.

        Returns
        -------
        :class:`Bridge`
            A new or existing :class:`Bridge` instance.

        """
        if singleton is True:
            if hasattr(cls, "_instance") is False:
                cls._instance: Bridge = super().__new__(cls, *args, **kwargs)
                return cls._instance
            return cls._instance

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, api_params: APIParams, singleton: bool = True, session: Optional[aiohttp.ClientSession] = None) -> None:
        """Initializes the :class:`Bridge` with the provided API credentials.

        Skips re-initialization if this instance is already a singleton.

        Parameters
        ----------
        api_params : :class:`APIParams`
            The prebuilt class to handle login credentials.
        singleton : :class:`bool`, optional
            If `True`, prevents re-initialization of an existing singleton instance, by default True.
        session : Union[:class:`aiohttp.ClientSession`, None], optional
            A session for every object made with this :class:`Bridge` to send its calls through, by default None.

        """
        if singleton and getattr(self, "_initialized", False):
            return
        LOGGER.debug("<%s.%s> | ID: %s | API_PARAMS: %s | SINGLETON: %s", __class__.__name__, "__init__", id(self), api_params, singleton)

        for field in fields(class_or_instance=api_params):
            setattr(self, field.name, getattr(api_params, field.name))

        self._client_session = None
        self._client_session_loop = None
        self._external_session = session
        self._logins_pending = {}

        if singleton:
            self._initialized = True

    async def clean_up(self) -> None:
        """|coro|

        Close the :class:`aiohttp.ClientSession` this :class:`Bridge` made. The next call makes a new one.

        .. note::
            A session passed in as `session` is yours, so it is never closed here.
            Safe to call more than once.

        .. versionadded:: 5.0.0

        """
        LOGGER.debug("<%s.%s> | Closing our `aiohttp.ClientSession` | SESSION: %s", __class__.__name__, "clean_up", self._client_session)
        client_session: Union[aiohttp.ClientSession, None] = self._client_session
        self._client_session = None
        self._client_session_loop = None
        if client_session is not None:
            await client_session.close()

    async def __aenter__(self) -> Self:
        """|coro|

        Enter the async context manager.

        .. note::
            Nothing is opened here. The :class:`aiohttp.ClientSession` is made on the first call,
            and it is closed on the way out.

        .. versionadded:: 5.0.0


        Returns
        -------
        :class:`Self`
            The :class:`Bridge` that entered the context manager.

        """
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """|coro|

        Exit the async context manager, closing our :class:`aiohttp.ClientSession` with :meth:`clean_up`.

        .. note::
            Exceptions are not suppressed, so any error propagates.

        .. versionadded:: 5.0.0


        Parameters
        ----------
        exc_type : type[:class:`BaseException`] | None
            The exception class, if one was raised inside the context.
        exc_value : :class:`BaseException` | None
            The exception instance, if one was raised inside the context.
        traceback : :class:`TracebackType` | None
            The traceback, if an exception was raised inside the context.

        """
        await self.clean_up()

    @classmethod
    def _get_bridge(cls) -> "Bridge":
        """Retrieves the :class:`Bridge` class instance variable.\n

        .. note::
            Current usage is inside :class:`Base` only.


        Raises
        ------
        :exc:`ValueError`
            If the :class:`Bridge` has not been created yet.

        Returns
        -------
        :class:`Bridge`:
                The :class:`Bridge`._instance attribute.

        """
        if not hasattr(cls, "_instance"):
            err = "Failed to setup connection. You need to initiate <Bridge> first."
            raise ValueError(err)
        return cls._instance

    async def _get_client_session(self) -> aiohttp.ClientSession:
        """|coro|

        Get the :class:`aiohttp.ClientSession` a call is sent through.

        A session passed in is used while it is open. Otherwise we use our own, and make a new one in the running event
        loop when we have none, ours is closed, or ours belongs to another event loop.

        Returns
        -------
        :class:`aiohttp.ClientSession`
            The session to send the call through.

        """
        if self._external_session is not None and self._external_session.closed is False:
            return self._external_session
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        if self._client_session is not None and self._client_session.closed is False and self._client_session_loop is loop:
            return self._client_session

        # We swap before closing, so a call made while we wait on the close gets the new session
        stale_session: Union[aiohttp.ClientSession, None] = self._client_session
        client_session: aiohttp.ClientSession = aiohttp.ClientSession()
        self._client_session = client_session
        self._client_session_loop = loop
        LOGGER.debug("<%s.%s> | New `aiohttp.ClientSession` | SESSION: %s", __class__.__name__, "_get_client_session", client_session)
        # A session from a finished event loop still closes, there is just nothing left for it to do
        if stale_session is not None:
            await stale_session.close()
        return client_session

    def _get_pending_login(self, instance_id: str) -> Union[asyncio.Future[None], None]:
        """Get the login running for this Instance ID in the running event loop, if there is one."""
        pending: Union[asyncio.Future[None], None] = self._logins_pending.get(instance_id)
        # A login cut off when its event loop ended can't be awaited here, so we drop it
        if pending is not None and pending.get_loop() is not asyncio.get_running_loop():
            del self._logins_pending[instance_id]
            return None
        return pending
