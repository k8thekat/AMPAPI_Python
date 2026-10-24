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
import copy
import datetime
import functools
import json
import logging
import re
import time
from collections.abc import Callable
from dataclasses import fields
from json import JSONEncoder
from pathlib import Path

# from pprint import pformat
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Optional, ParamSpec, TypedDict, Union, Unpack, overload

import aiohttp
from aiohttp import ClientResponse

# from dataclass_wizard import fromdict
from pyotp import TOTP

from ._enums import Module
from ._types import (
    DIAGNOSTICS_EXCLUDED_KEYS,
    DIAGNOSTICS_REQUIRED_KEYS,
    DiagnosticsResponse,
    EndpointResponseError,
    ResponseTypeAlias,
    is_response_type,
)
from .backoff import ExponentialBackoff
from .bridge import Bridge
from .errors import AMPAPIError, AMPAPINetworkError, AMPAPIResponseError
from .key_drift import KeyDriftCheck
from .modules import APISession, BuildInfo, Status, timestamp_converter

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Callable, Coroutine
    from datetime import timedelta
    from types import TracebackType
    from typing import Concatenate, Self

    from _typeshed import DataclassInstance
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]
    from typing_extensions import ParamSpec, TypeVar

    from .modules import Updates

    D = TypeVar("D", bound="Base")
    T = ParamSpec("T")
    F = TypeVar("F")
    X = TypeVar("X", bound=DataclassInstance)

__all__ = ("Base", "ResponseHandlerOptions")

ResponseAliasFull = Union[ResponseTypeAlias, str, bool, None]

LOGGER: logging.Logger = logging.getLogger(__name__)


# The three passes of `Base.camel_to_snake_re`, compiled once.
_PLURAL_ACRONYM_PATTERN: re.Pattern[str] = re.compile(r"([A-Z]{2,})(s)(?=[^a-z]|$)")
_WORD_BOUNDARY_PATTERN: re.Pattern[str] = re.compile("(.)([A-Z][a-z]+)")
_LOWER_UPPER_PATTERN: re.Pattern[str] = re.compile("([a-z0-9])([A-Z])")


def _plural_acronym_repl(match: re.Match[str]) -> str:
    """Lowers an acronym's trailing letters: `IDs` -> `Ids`, `CPUs` -> `Cpus`."""
    return match.group(1)[0] + match.group(1)[1:].lower() + match.group(2)


# Bounded: some answers are keyed by player ID, and an unbounded cache would grow without limit.
@functools.lru_cache(maxsize=4096)
def _snake_key(key: str) -> str:
    """The `snake_case` form of one AMP response key, remembered per key string.

    Spaces and underscores are stripped, :attr:`Base.json_key_mapping` is applied and
    :meth:`Base.camel_to_snake_re` does the rest.
    """
    # To handle keys with spaces and to remove underscores that exist already.
    new_key: str = key.replace(" ", "").replace("_", "")
    if new_key in Base.json_key_mapping:
        new_key = Base.json_key_mapping[new_key]
    return Base.camel_to_snake_re(data=new_key)


class DumpParameters(TypedDict, total=False):
    skipkeys: bool
    ensure_ascii: bool
    check_circular: bool
    allow_nan: bool
    cls: type[JSONEncoder] | None
    indent: int | str | None
    separators: tuple[str, str] | None
    default: Callable[[Any], Any] | None
    sort_keys: bool


class ResponseHandlerOptions(TypedDict, total=False):
    """Response handling parameters.

    Options:
    --------
    sanitize_json : :class:`bool`
        ...
    to_file : :class:`bool`
        ...
    path : :class:`pathlib.Path`
        ...
    check_key_drift : :class:`bool`
        Dev check, only with `to_file`: compare the capture with the TypedDict its endpoint narrows to.
    allow_null : :class:`bool`
        Return None when AMP answers JSON null, instead of raising.

    """

    sanitize_json: bool
    to_file: bool
    path: pathlib.Path
    check_key_drift: bool
    allow_null: bool


class _SessionDeadError(AMPAPIResponseError):
    """Raised by :meth:`Base._response_handler` when AMP says the stored session no longer exists.

    :meth:`Base._post` catches it once to log in again and resend. It is private. Anything that gets past
    :meth:`Base._post` is a plain :exc:`AMPAPIResponseError`.
    """

    def __init__(self, title: str, url: str, reason: str) -> None:
        self.title: str = title
        self.url: str = url
        self.reason: str = reason
        # Skips `AMPAPIResponseError`'s error log. A dead session is expected, and `_post` logs in again.
        AMPAPIError.__init__(self, f"{title} | URL: {url} | Reason: {reason}")


class Base:
    """Contains the base functions for all AMP API endpoints and handles the parsing of Bridge data.

    .. warning::
        Do not overwrite or alter the :attr:`instance_id`.


    .. note::
        A session expires after 240sec of inactivity per Cube Coders AMP.
        If for any reason you want to change that value; set the attribute :attr:`session_ttl`.\n


    Attributes
    ----------
    api_url : :class:`str`
        The URL to access the Web Panel. This comes from your :class:`APIParams`.
    session : :class:`aiohttp.ClientSession`
        A static Session to use, otherwise the class will generate it's own as needed.

    """

    # Private Attributes
    _bridge: Bridge
    _backoff: ExponentialBackoff[bool]
    _module: str
    _format_data: ClassVar[bool] = True
    _endpoint_url: str
    _instance_id: str
    _session_ttl: ClassVar[int] = 240
    # A login in progress on this object is waited for by the other calls, and the session it stores is used.
    # It only exists while a login runs. It is set in `__init__`.
    _login_pending: Union[asyncio.Future[None], None]

    # Cache state for classes whose attributes are populated from an API response rather than __init__.
    # `_is_cached` flips once data has been applied; `_cached_at` stamps when, so staleness can be told
    # apart from "never fetched".
    _is_cached: bool = False
    _cached_at: Optional[datetime.datetime] = None
    # Monotonic mirror of `_cached_at`; the staleness check runs on every guarded attribute access, and
    # `time.monotonic()` is far cheaper than building a tz-aware datetime each time.
    _cached_monotonic: Optional[float] = None
    _cache_timeout: ClassVar[int] = 300
    # Named in the cache messages so they can point at whatever actually refreshes the attribute.
    # `_cache_source` is the class-wide fallback; `_cache_sources` overrides it per attribute for the
    # ones populated by a different endpoint.
    _cache_source: ClassVar[str] = "the API call that populates it"
    _cache_sources: ClassVar[dict[str, str]] = {}
    # Shared by every instance and built on the first `check_key_drift` call; it reads the wrapper source once.
    _key_drift_check: ClassVar[Union[KeyDriftCheck, None]] = None

    # Error response strings.
    _ads_only: ClassVar[str] = "This API call is only available to <class:`ADSModule`> type classes."
    _failed_api: ClassVar[str] = "The API call returned a malformed response."
    _generic_only: ClassVar[str] = "This API call is only available on Generic (GenericModule) type instances."
    _minecraft_only: ClassVar[str] = "This API call is only available on Minecraft type instances."
    _no_bridge: ClassVar[str] = "Failed to setup connection. You need to initiate `<class Bridge>` first."
    _no_controller: ClassVar[str] = "The function failed as the <class:`Controller`> was not properly initialized and set."
    _no_data: ClassVar[str] = "Failed to receive any data from post request."
    _unauthorized_access: ClassVar[str] = "The user does not have the required permissions to interact with this instance."
    _instance_offline: ClassVar[str] = "The requested Instance is not available at this time. | URL: %s"
    _login_failed: ClassVar[str] = "Failed to login to AMP as '%s' (AMP result %s); check the user, password and 2FA token."
    # Login result codes confirmed in AMP's own logs. Any other code is reported as its number only.
    _login_result_names: ClassVar[dict[int, str]] = {0: "Failure", 5: "NoInstanceAccess", 100: "PassthruDisabled"}
    _no_cache: ClassVar[str] = "'%s.%s' has not been populated yet. You must call <%s>.%s first."
    _stale_cache: ClassVar[str] = (
        "'%s.%s' was cached %s seconds ago and the timeout is %s seconds; the value may be stale. Call <%s>.%s to refresh it."
    )
    _version_unavailable: ClassVar[str] = "The API call %s is no longer available at this version of AMP %s"

    # These are used to handle JSON keys that cannot be parsed properly via regex.
    # See :func:`camel_to_snake_re`
    json_key_mapping: ClassVar[dict[str, str]] = {
        "ContainerCPUs": "container_cpus",
        "InstalledRAMMB": "installed_ram_mb",
        "FreeRAMMB": "free_ram_mb",
        "AvailableIPs": "available_ips",
        "SecurityandPrivacy": "security_and_privacy",
        "Pass": "passed",
    }

    @property
    def module(self) -> Module | str:
        """The AMP Instance `!type`.

        Current Values: `ADS` | `Minecraft` | `Generic` | `SRCDS`

        Returns
        -------
        :class:`Module` | :class:`str`
            The AMP Instance `!type` as a :class:`Module`, or the raw string when it is not a known one.

        """
        try:
            return Module(self._module)
        except ValueError:
            return self._module

    @property
    def format_data(self) -> bool:
        """Controls whether the data returned from an API endpoint is formatted or not.\n
        Default is `True` which comes from the global parameter `FORMAT_DATA`.

        .. note::
            `True` = formatted \n
            `False` = unformatted


        Returns
        -------
        :class:`bool`
            Returns `True` or `False`.

        """
        return Base._format_data

    @format_data.setter
    def format_data(self, value: bool) -> None:
        Base._format_data = value

    @property
    def session_ttl(self) -> int:
        """How long before the session ID expires in seconds, default is 240 seconds."""
        return Base._session_ttl

    @session_ttl.setter
    def session_ttl(self, value: int) -> None:
        Base._session_ttl = value

    @property
    def instance_id(self) -> str:
        """The Instance ID AMP gave this Instance, default is "0" (zero).

        This is not set by a login. A Controller keeps "0", since it is the key its session is stored under.
        """
        return self._instance_id

    @property
    def endpoint_url(self) -> str:
        """The URL to access the AMP Instance API endpoints."""
        return self._endpoint_url

    def __init__(self, *, bridge: Optional[Bridge] = None, session: Optional[aiohttp.ClientSession] = None) -> None:  # noqa: D107
        self._endpoint_url = ""
        self._instance_id = "0"
        self._login_pending = None

        if bridge is None:
            try:
                self._bridge = Bridge._get_bridge()  # pyright: ignore[reportPrivateUsage]
            except ValueError:
                LOGGER.error(
                    "<%s.%s> | Failed to initialize, you must either must use a Singleton <Bridge> object or pass into the __init__.",
                    __class__.__name__,
                    "__init__",
                )
                raise
        else:
            self.parse_bridge(bridge=bridge)

        self._backoff = ExponentialBackoff(integral=True)

        LOGGER.debug("<%s.%s> | BRIDGE: %s | SESSION: %s |", __class__.__name__, "__init__", bridge, session)
        self.session: aiohttp.ClientSession | None = session

    @staticmethod
    def ads_only(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """Checks the class attribute `.module` and is equal to str(`ADS`) or if the type of Instance using the function is TargetADS.

        Parameters
        ----------
        func : Callable[Concatenate[D, T], Coroutine[None, None, F]]
            The function the decorator is wrapping.

        Returns
        -------
        Callable[Concatenate[D, T], Coroutine[None, None, F]]
            The function the decorator is wrapping.

        Raises
        ------
        RuntimeError
            The API call is only allowed to be run on a type(:py:class:`TargetADS`).

        """

        @functools.wraps(wrapped=func)
        def wrapper_ads_only(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            from .adsmodule import ADSModule  # noqa: PLC0415
            # from .instance import Controller

            # if self.module == "ADS" or type(self) is Controller or isinstance(self, ADSModule):
            if self.module == "ADS" or isinstance(self, ADSModule):
                return func(self, *args, **kwargs)
            raise RuntimeError(self._ads_only)

        return wrapper_ads_only

    @staticmethod
    def generic_only(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """Checks the class attribute `.module` is a Generic one, `GenericModule` for a game template or `Generic` for a
        Custom Application.

        .. note::
            :class:`Instance` carries the :class:`GenericModule` and :class:`SteamCMDPlugin` endpoints, so its
            subclasses (eg. :class:`MinecraftInstance`, :class:`TargetADS`) have them too. Any other module raises
            before the call is sent.

        Parameters
        ----------
        func : Callable[Concatenate[D, T], Coroutine[None, None, F]]
            The function the decorator is wrapping.

        Returns
        -------
        Callable[Concatenate[D, T], Coroutine[None, None, F]]
            The function the decorator is wrapping.

        Raises
        ------
        RuntimeError
            The API call is only allowed on a Generic type Instance.

        """

        @functools.wraps(wrapped=func)
        def wrapper_generic_only(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            if self.module in ("GenericModule", "Generic"):
                return func(self, *args, **kwargs)
            raise RuntimeError(self._generic_only)

        return wrapper_generic_only

    @overload
    async def _post(
        self,
        url: str,
        parameters: Union[dict[str, Any], None] = None,
        *,
        no_data: Literal[True],
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> None: ...

    @overload
    async def _post(
        self,
        url: str,
        parameters: Union[dict[str, Any], None] = None,
        *,
        no_data: bool = ...,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ResponseTypeAlias | str | bool | None: ...

    async def _post(
        self,
        url: str,
        parameters: Union[dict[str, Any], None] = None,
        *,
        no_data: bool = False,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ResponseTypeAlias | str | bool | None:
        """|coro|

        Makes a POST request via :class:`aiohttp.ClientSession` and passes the response to :meth:`_response_handler`.

        .. warning::
            Will raise :exc:`AMPAPINetworkError` or :exc:`AMPAPIResponseError` if any errors occur when attempting to call the API.

        .. note::
            When AMP answers that the stored session no longer exists, this calls :meth:`login` again and sends the request once more.
            A second dead answer raises, and `Core/Login` itself is never sent again.


        Parameters
        ----------
        url : :class:`str`
            The API endpoint to POST to, excluding the base panel URL and ``/API/`` prefix, eg ``Core/GetModuleInfo``.
        parameters : Union[None, dict[:class:`str`, Any]], optional
            The parameters to supply to the endpoint, by default None.
        no_data : :class:`bool`, optional
            If the endpoint answers JSON null or not. The body is still checked for errors, by default False.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded directly to :meth:`aiohttp.ClientSession.post`. The `headers`
            and `data` keys are populated automatically when `None`, by default None.

            .. code-block:: python

                headers = {"Accept": "text/javascript", "Authorization": f"Bearer {api_session.id}"}
                data = json.dumps(parameters)

        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ResponseTypeAlias` | :class:`str` | :class:`bool` | None
            The processed response on a successful (2xx) status, `None` if `no_data` is `True`.

        """
        _url: str = self._endpoint_url + "/API/" + url

        if parameters is None:
            parameters = {}

        # Ver. 2.6.2.8 Authorization header key change.
        if request_params is None:
            request_params = {}
        # A copy, since the headers and data are filled in below. A dict the caller passes again would carry the old ones.
        request_params = request_params.copy()

        # Headers the caller passed are theirs to keep. Only the ones we build here follow a new login.
        library_headers: bool = "headers" not in request_params

        # A dead session gets one login and one resend, once per call.
        # The RuntimeError retry below has no limit of its own, as before #18.
        session_retried: bool = False
        # Counts the RuntimeError retries, for the log line.
        runtime_retries: int = 0

        while True:
            api_session: APISession = self._bridge._sessions.get(  # pyright: ignore[reportPrivateUsage]
                self._instance_id,
                APISession(id="0", ttl=datetime.datetime.now(tz=datetime.UTC)),
            )
            if self.session is None:
                self.session = aiohttp.ClientSession()

            # request_params.setdefault("headers", {"Accept": "text/javascript", "Authorization": f"Bearer {api_session.id}"})
            # Rebuilt on every pass. A resend after a new login carries the new session ID.
            if library_headers is True:
                request_params["headers"] = {"Accept": "text/javascript", "Authorization": f"Bearer {api_session.id}"}
            request_params.setdefault("data", json.dumps(parameters))

            try:
                response: ClientResponse = await self.session.post(url=_url, **request_params)
                LOGGER.debug(
                    "<%s.%s> | POST URL: %s | API_SESSION: %s | INSTANCE_ID: %s",
                    __class__.__name__,
                    "_post",
                    _url,
                    api_session,
                    self._instance_id,
                )
                LOGGER.debug("<%s.%s> | REQ_PARAMS: %s", __class__.__name__, "_post", request_params)
                LOGGER.debug("<%s.%s> | RESP_PARAMS: %s", __class__.__name__, "_post", response_params)

            except RuntimeError as e:
                # Attempting to re-open the session if it is somehow closed during usage.
                if isinstance(e.args[0], str) and "session is closed" in e.args[0].lower():
                    self.session = aiohttp.ClientSession()

                # retry: int | float = self._backoff.delay()
                # The backoff can hand back 0 seconds (half of all first retries do). One second is the least we wait.
                retry: int | float = max(1, self._backoff.delay())
                runtime_retries += 1
                # LOGGER.error(
                #     "<%s.%s> encountered an <RuntimeError> and will retry in %s. | Exception: %s",
                #     __class__.__name__,
                #     "_post",
                #     retry,
                #     e,
                # )
                LOGGER.error(
                    "<%s.%s> encountered an <RuntimeError>, retry %s in %ss. | Exception: %s",
                    __class__.__name__,
                    "_post",
                    runtime_retries,
                    retry,
                    e,
                )
                await asyncio.sleep(delay=retry)
                # return await self._post(
                #     url=url,
                #     parameters=parameters,
                #     no_data=no_data,
                #     request_params=request_params,
                #     **response_params,
                # )
                # Same retry as the recursive call above. It stays in this loop, and `session_retried` carries over.
                continue

            # ? Suggestion
            # Further see what exceptions may be raised to narrow this comparison as the noqa can be avoided.
            except Exception as e:
                LOGGER.error(
                    "<%s.%s> encountered an <Exception> | Exception: %s",
                    __class__.__name__,
                    "_post",
                    e,
                )
                raise AMPAPINetworkError(status=0, url=_url, reason=str(e)) from e

            if response.content_length == 0:
                raise AMPAPINetworkError(status=response.status, url=_url, reason="The HTTP Header content length was 0.")

            match response.status:
                case status if 200 <= status < 300:
                    try:
                        if no_data is True:
                            # response.release()
                            # return None
                            # A Void endpoint answers JSON null, but AMP still reports a failure in the body with a 200.
                            response_params["allow_null"] = True
                            await self._response_handler(response=response, **response_params)
                            return None
                        return await self._response_handler(response=response, **response_params)

                    except _SessionDeadError as dead_session:
                        # A second dead answer, or a dead answer to the login itself, is a real failure.
                        if session_retried is True or url == "Core/Login":
                            raise AMPAPIResponseError(
                                title=dead_session.title,
                                url=dead_session.url,
                                reason=dead_session.reason,
                            ) from dead_session
                        # The handler no longer resets the session. It could wipe one another call just stored.
                        # Reset only if the stored session is still the one this pass sent.
                        # The login below is a fresh one and the loop resends with the new ID.
                        stored_session: Union[APISession, None] = self._bridge._sessions.get(self._instance_id)  # pyright: ignore[reportPrivateUsage]
                        if stored_session is not None and stored_session.id == api_session.id:
                            self._reset_session()
                        session_retried = True
                        await self._reauth()
                        continue

                case 400:
                    raise AMPAPINetworkError(status=400, url=_url, reason="Bad Request")
                case 401:
                    raise AMPAPINetworkError(status=401, url=_url, reason="Unauthorized")
                case 403:
                    raise AMPAPINetworkError(status=403, url=_url, reason="Forbidden")
                case 404:
                    raise AMPAPINetworkError(status=404, url=_url, reason="Not Found")
                case 408:
                    raise AMPAPINetworkError(status=408, url=_url, reason="Request Timeout")
                case 429:
                    raise AMPAPINetworkError(status=429, url=_url, reason="Too Many Requests")
                case 500:
                    raise AMPAPINetworkError(status=500, url=_url, reason="Internal Server Error")
                case 502:
                    raise AMPAPINetworkError(status=502, url=_url, reason="Bad Gateway")
                case 503:
                    raise AMPAPINetworkError(status=503, url=_url, reason="Service Unavailable")
                case 504:
                    raise AMPAPINetworkError(status=504, url=_url, reason="Gateway Timeout")
                case _:
                    raise AMPAPINetworkError(status=response.status, url=_url, reason=f"Unexpected status [{response.status}]")

    async def _response_handler(
        self,
        response: ClientResponse,
        *,
        sanitize_json: bool = True,
        to_file: bool = False,
        path: Optional[pathlib.Path] = None,
        check_key_drift: bool = False,
        allow_null: bool = False,
    ) -> ResponseTypeAlias | str | bool | None:
        """|coro|

        Processes a :class:`aiohttp.ClientResponse` into a parsed response object.

        .. warning::
            Will raise :exc:`AMPAPIResponseError` if the response JSON is `None` (unless `allow_null` is True),
            indicates ``"Unauthorized Access"``, ``"Instance Unavailable"``, or has `status` of `False`.


        Parameters
        ----------
        response : :class:`aiohttp.ClientResponse`
            The raw HTTP response to process.
        sanitize_json : :class:`bool`, optional
            Run the parsed JSON through :meth:`sanitize_json` before returning, by default True.
        to_file : :class:`bool`, optional
            Write the response JSON to a file at `path`, by default False.
        path : :class:`pathlib.Path` | None, optional
            Directory to write the response file to when `to_file` is `True`, by default None.
        check_key_drift : :class:`bool`, optional
            A dev check that runs with `to_file`: compare the response with the TypedDict its endpoint narrows to,
            log a warning and write ``<endpoint>.key_drift.json`` beside the capture when the keys differ, by default False.
        allow_null : :class:`bool`, optional
            Return None when AMP answers JSON null, for endpoints where null means "nothing to report", by default False.

        Returns
        -------
        :class:`ResponseTypeAlias` | :class:`str` | :class:`bool` | None
            The parsed and optionally sanitized JSON response.

        Raises
        ------
        :exc:`AMPAPIResponseError`
            If the response indicates an error condition.
        :exc:`ValueError`
            If `to_file` is `True` but `path` is `None`.
        :exc:`FileNotFoundError`
            If the provided `path` does not exist.

        """
        if to_file is True and path is None:
            msg = "Please provide a valid <Path> object when using `to_file` parameter."
            raise ValueError(msg)

        try:
            response_json: EndpointResponseError | ResponseTypeAlias | str | bool | None = await response.json()
        except Exception as e:
            LOGGER.error(
                "<%s.%s> | Encountered an Exception processing the <ClientResponse> as json().",
                __class__.__name__,
                "_response_handler",
                exc_info=e,
            )
            return None

        LOGGER.debug(
            "<%s.%s> | RESPONSE: %s | SANITIZE_JSON: %s | TO_FILE: %s | PATH: %s",
            __class__.__name__,
            "_response_handler",
            response,
            sanitize_json,
            to_file,
            path,
        )
        LOGGER.debug("<%s.%s> | RESP_JSON: %s", __class__.__name__, "_response_handler", response_json)

        if response_json is None:
            if allow_null is True:
                return None
            raise AMPAPIResponseError(title="None", url=str(response.url), reason="<ClientResponse> JSON returned <None>.")

        if sanitize_json is True:
            response_json = self.sanitize_json(response_json)

        if to_file is True and path is not None and response_json is not None:
            # ? SUGGESTION: May have to make this async in the future if it becomes blocking.
            if path.exists() is False:
                msg = "The path provided does not exist. %s"
                raise FileNotFoundError(msg, path)
            self.write_data_to_file(file_name=response.url.name.lower() + ".json", data=response_json, path=path)

        # A bool has no title or status to check.
        if isinstance(response_json, bool):
            return response_json

        # This is the logic gate for when we have an "EndpointResponseError" typically.
        if isinstance(response_json, dict) and "title" in response_json:
            title: str = response_json.get("title")

            # `Session.Exists` is the permission for having a session at all. That marks a dead session apart from a missing permission.
            # The call never ran. `_post` can log in again and send it once more.
            # It is a warning, not an error. Only a second dead answer is a failure, and `_post` raises that one.
            if title == "Unauthorized Access" and "Session.Exists" in str(response_json.get("message", "")):
                LOGGER.warning(
                    "<%s.%s> | AMP no longer knows the stored session. | URL: %s",
                    __class__.__name__,
                    "_response_handler",
                    response.url,
                )
                # self._reset_session()
                # `_post` resets it, and only when the stored session is still the one it sent.
                raise _SessionDeadError(title=title, url=str(response.url), reason=response_json.get("message", ""))

            if title == "Unauthorized Access" or title == "Instance Unavailable":
                LOGGER.error(
                    "<%s.%s> failed because of %s. | URL: %s",
                    __class__.__name__,
                    "_response_handler",
                    response_json,
                    response.url,
                )
                # api_session = APISession(id="0", ttl=datetime.datetime.now(tz=datetime.UTC))
                # self._bridge._sessions.update({self._instance_id: api_session})

            # This will be our default catch all for any "invalid" Responses.
            raise AMPAPIResponseError(title=response_json["title"], url=str(response.url), reason=response_json.get("message", ""))

        # A failed ActionResult, eg. RegisterTargetWithCode against a Controller whose ADS mode is not set yet.
        # AMP explains why in `reason`, so that is what gets raised.
        if isinstance(response_json, dict) and "status" in response_json and response_json["status"] is False:
            reason: str = str(response_json.get("reason") or "Status is False")
            LOGGER.error("%s failed because of Status: %s | Reason: %s", response.url, response_json["status"], reason)
            raise AMPAPIResponseError(title="Status False", url=str(response.url), reason=reason)

        # Error responses raised above, so only a real capture gets compared.
        if check_key_drift is True and to_file is True and path is not None:
            self._check_key_drift(response=response, data=response_json, path=path, sanitized=sanitize_json)

        return response_json

    def _check_key_drift(self, response: ClientResponse, data: object, path: pathlib.Path, *, sanitized: bool) -> None:
        """Dev check: compare a captured response with the TypedDict its endpoint narrows to.

        On drift, logs a warning and writes ``<endpoint>.key_drift.json`` beside the capture.
        See :class:`~ampapi.key_drift.KeyDriftCheck` for how an endpoint's TypedDict is found.

        Parameters
        ----------
        response : :class:`aiohttp.ClientResponse`
            The response the capture came from; its URL names the endpoint.
        data : :class:`object`
            The captured JSON response.
        path : :class:`pathlib.Path`
            The directory the capture was written to.
        sanitized : :class:`bool`
            If the JSON was sanitized; the TypedDicts use the sanitized `snake_case` keys.

        """
        # The URL ends in the endpoint, after any ADSModule/Servers/<id>/ proxy prefix.
        match = re.search(r"API/([A-Za-z]+/[A-Za-z0-9]+)$", response.url.path)
        if match is None:
            return
        endpoint: str = match.group(1)
        if sanitized is False:
            LOGGER.warning("<%s.%s> | Skipped %s; the TypedDicts use the sanitized keys.", __class__.__name__, "_check_key_drift", endpoint)
            return
        if Base._key_drift_check is None:
            Base._key_drift_check = KeyDriftCheck()
        found = Base._key_drift_check.check(endpoint=endpoint, data=data)
        if found is None:
            LOGGER.debug("<%s.%s> | No TypedDict is known for %s.", __class__.__name__, "_check_key_drift", endpoint)
            return
        shape, drift = found
        if not drift["missing"] and not drift["unexpected"]:
            return
        LOGGER.warning(
            "<%s.%s> | %s differs from %s | Missing: %s | Unexpected: %s",
            __class__.__name__,
            "_check_key_drift",
            endpoint,
            shape.__name__,
            drift["missing"],
            drift["unexpected"],
        )
        report: dict[str, object] = {"endpoint": endpoint, "shape": shape.__name__, **drift}
        path.joinpath(response.url.name.lower() + ".key_drift.json").write_text(json.dumps(report, indent=4))

    def _reset_session(self) -> None:
        """Forget this object's stored session. The next call logs in again.

        .. note::
            Only this object's own entry is reset. Other Instances on the same :class:`Bridge` keep theirs.

        """
        api_session = APISession(id="0", ttl=datetime.datetime.now(tz=datetime.UTC))
        self._bridge._sessions.update({self._instance_id: api_session})  # pyright: ignore[reportPrivateUsage]

    async def _reauth(self) -> Any:
        """|coro|
        Logs into AMP via "API/Core/Login" endpoint using your :class:`Bridge` object.

        .. note::
            If Applicable handles your 2FA using :class:`TOTP` \n
            Stores the session ID via :class:`APISession` dataclass for future usage inside the :class:`Bridge` object.


        Returns
        -------
        Union[:class:`LoginResultsResponse`, None]
            The raw response from ``API/Core/Login``, or None when the stored session is still valid.

        Raises
        ------
        :exc:`ValueError`
            If the 2 Factor Authentication code is not a formatted properly.
            - *aka* the :attr:`~Bridge.token` when making the :class:`Bridge` object.
        :exc:`AMPAPIResponseError`
            If AMP refused the login, or answered it with an error.
        :exc:`AMPAPINetworkError`
            If the login request itself failed.

        """
        # A login is in progress on this object. Wait, then check the stored session again.
        # If the login failed there is still none. This call then tries its own, one at a time.
        while self._login_pending is not None:
            await asyncio.shield(self._login_pending)

        code: Union[str, TOTP] = ""

        # get our InstanceID and use it to key for session_id
        session: APISession = self._bridge._sessions.get(self._instance_id, APISession(id="0", ttl=datetime.datetime.now(tz=datetime.UTC)))  # pyright: ignore[reportPrivateUsage]
        # if isinstance(session, APISession):
        ttl: timedelta = datetime.datetime.now(tz=datetime.UTC) - session.ttl
        if ttl.total_seconds() > self.session_ttl:
            session_id = "0"
        else:
            session_id: str = session.id

        if session_id == "0":
            # Set with no `await` since the check above. Other calls wait on it until the login is done.
            pending: asyncio.Future[None] = asyncio.get_running_loop().create_future()
            self._login_pending = pending
            try:
                if self._bridge.use_2fa is True:
                    try:
                        # Handles time based 2Factory Auth Key/Code
                        code = TOTP(self._bridge.token).now()

                    # pyotp raises binascii.Error, a ValueError, for a token that is not valid base32.
                    except ValueError as error:
                        msg = (
                            "Please check your 2 Factor Code, should not contain spaces, escape characters "
                            "and it must be enclosed in quotes!"
                        )
                        raise ValueError(msg) from error

                parameters: dict[str, Any] = {
                    "username": self._bridge.user,
                    "password": self._bridge.password,
                    "token": code,
                    "rememberMe": True,
                }
                # Network and response errors raise straight through; their URL already names Core/Login.
                # We post directly, since `_call_end_point` logs in first and would call us again.
                result = await self._post(url="Core/Login", parameters=parameters)
                if not isinstance(result, dict) or "remember_me_token" not in result or result["success"] is not True:
                    # AMP sends no reason; a wrong password and a wrong 2FA code both answer `result: 40`.
                    amp_result = result["result"] if isinstance(result, dict) and "remember_me_token" in result else result
                    if isinstance(amp_result, int) and not isinstance(amp_result, bool) and amp_result in self._login_result_names:
                        amp_result = f"{amp_result}, {self._login_result_names[amp_result]}"
                    reason: str = self._login_failed % (self._bridge.user, amp_result)
                    LOGGER.error("<%s.%s> | %s", __class__.__name__, "_reauth", reason)
                    raise AMPAPIResponseError(title="Login Failed", url=f"{self._endpoint_url}/API/Core/Login", reason=reason)

                # This is our new sessions table to correlate InstanceID to a sessionID.
                api_session = APISession(id=result["session_id"] or "0", ttl=datetime.datetime.now(tz=datetime.UTC))
                self._bridge._sessions.update({self._instance_id: api_session})  # pyright: ignore[reportPrivateUsage]
                return result
            # Resolved with None even when the login raised. Only the call that logged in sees the error.
            finally:
                self._login_pending = None
                if not pending.done():
                    pending.set_result(None)
        return None

    @property
    def cache_age(self) -> Optional[float]:
        """How many seconds ago this class had its API data applied, or None if it never has.

        Returns
        -------
        :class:`float` | None
            The age of the cached data in seconds, otherwise None.

        """
        if self._cached_monotonic is None:
            return None
        return time.monotonic() - self._cached_monotonic

    @property
    def cache_expired(self) -> bool:
        """If the cached API data is older than :attr:`_cache_timeout`.

        .. note::
            Returns False when nothing has been cached yet; use :attr:`_is_cached` to tell the two apart.


        Returns
        -------
        :class:`bool`
            True when the data is stale.

        """
        age: Optional[float] = self.cache_age
        return age is not None and age > self._cache_timeout

    @classmethod
    def _cache_hint(cls, name: str) -> str:
        """The call a user should make to populate or refresh a cached attribute.

        .. note::
            Falls back to :attr:`_cache_source` when the attribute has no entry in :attr:`_cache_sources`.


        Parameters
        ----------
        name : :class:`str`
            The attribute being reported on.

        Returns
        -------
        :class:`str`
            The call to name in the message. (eg. `"get_instances(format_data=True)"`)

        """
        return cls._cache_sources.get(name, cls._cache_source)

    def _mark_cached(self) -> None:
        """Stamp this class as holding freshly applied API data."""
        self._is_cached = True
        self._cached_at = datetime.datetime.now(tz=datetime.UTC)
        self._cached_monotonic = time.monotonic()

    async def clean_up(self, *, logout: bool = False) -> None:
        """|coro|

        Close any open :class:`aiohttp.ClientSession` belonging to this class.

        .. note::
            Safe to call more than once; the session is cleared once closed.

        .. versionchanged:: 5.0.0
            `logout` also resets the stored session, and skips `Core/Logout` when there is no session to end.

        Parameters
        ----------
        logout : :class:`bool`, optional
            Call `Core/Logout` first, so AMP ends the login session instead of leaving it to expire, by default False.
            A failed logout is logged as a warning and the session is still closed.

        """
        stored: Union[APISession, None] = self._bridge._sessions.get(self._instance_id)  # pyright: ignore[reportPrivateUsage]
        # Without a stored session the dead-session retry in `_post` would log in only to log out.
        if logout is True and (stored is None or stored.id == "0"):
            LOGGER.debug("<%s.%s> | No stored session, skipping `Core/Logout`", __class__.__name__, "clean_up")
        elif logout is True:
            try:
                await self._post(url="Core/Logout", no_data=True)
            except Exception:
                LOGGER.warning("<%s.%s> | `Core/Logout` failed, closing the session anyway", __class__.__name__, "clean_up", exc_info=True)
            # Logged out or not, the stored session is no use to the next call.
            self._reset_session()
        LOGGER.debug("<%s.%s> | Closing any open `aiohttp.ClientSession`", __class__.__name__, "clean_up")
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def __aenter__(self) -> Self:
        """|coro|

        Enter the async context manager.

        .. note::
            Nothing is opened here; the :class:`aiohttp.ClientSession` is created lazily on the first
            request. This exists so the session is always closed on the way out.


        Returns
        -------
        :class:`Self`
            The class that entered the context manager.

        """
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """|coro|

        Exit the async context manager, closing any open session.

        .. note::
            Exceptions are not suppressed; this returns None so any error propagates.


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

    # TODO: See about supporting automatic login handling like other Endpoints.
    # See about re-writing the logic to allow setting the URL and other parameters.
    async def _call_end_point(
        self,
        endpoint: str,
        parameters: dict[str, Any] | None = None,
        *,
        # api_session: Optional[APISession] = None,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ResponseTypeAlias | str | bool | None:
        """|coro|

        Generic function for calling any API endpoint; a dev tool for testing endpoints that have no wrapper yet.
        Some API endpoints require the Instance module type to be ADS. \n
        See `docs/api_spec_sheets/<AMP version>/ADS_api_spec.md` or `Minecraft_api_spec.md` for the full API endpoints
        and parameter information.


        .. note::
            The session is handled for you.


        .. warning::
            DO NOT include the full URL - *Exclude: www.yourAMPURL.com/API/*\n



        Parameters
        ----------
        endpoint : :class:`str`
            The AMP API endpoint to call. eg "Core/GetModuleInfo"
        parameters : None | dict[:class:`str`, Any], optional
            The parameters to pass to the API endpoint, by default is None.
        request_params : :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded to :meth:`aiohttp.ClientSession.post`, by default None.
        **response_params : :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ResponseTypeAlias` | :class:`str` | :class:`bool` | None
           The JSON response from the API endpoint.

        """
        await self._reauth()
        return await self._post(url=endpoint, parameters=parameters, request_params=request_params, **response_params)

    @staticmethod
    def camel_to_snake_re(data: str) -> str:
        """A simple regex pattern applied to a string to remove Camel Casing and apply snake_case.

        .. note::
            This will fail on entries with an underscore between to capital characters. |  *eg (Tool_Version = tool__version)*\n

        Parameters
        ----------
        data : :class:`str`
            The string to be converted.

        Returns
        -------
        :class:`str`
            The converted string from CamelCase to snake_case.

        """
        # Pre-pass: collapse plural acronyms so e.g. "IDs" -> "Ids" and "CPUs" -> "Cpus"
        # before the main passes split them incorrectly into "i_ds" / "cp_us".
        # data = re.sub(
        #     pattern=r"([A-Z]{2,})(s)(?=[^a-z]|$)",
        #     repl=lambda m: m.group(1)[0] + m.group(1)[1:].lower() + m.group(2),
        #     string=data,
        # )
        # data = re.sub(pattern="(.)([A-Z][a-z]+)", repl=r"\1_\2", string=data)
        # return re.sub(pattern="([a-z0-9])([A-Z])", repl=r"\1_\2", string=data).lower()
        data = _PLURAL_ACRONYM_PATTERN.sub(repl=_plural_acronym_repl, string=data)
        data = _WORD_BOUNDARY_PATTERN.sub(repl=r"\1_\2", string=data)
        return _LOWER_UPPER_PATTERN.sub(repl=r"\1_\2", string=data).lower()

    @staticmethod
    def camel_case_data(data: dict[str, Any]) -> dict[str, Any]:
        """Calls the :meth:`title` on every dict key.

        Parameters
        ----------
        data : dict[:class:`str`, Any]
            The dictionary to camel case.

        Returns
        -------
        dict[:class:`str`, Any]
            The camel cased dict.

        """
        res: dict[str, str | bool | int] = {}
        for key, value in data.items():
            if value is not None:
                res[key.title()] = value
        return res

    @staticmethod
    def json_to_typeddict(name: str, data: dict[str, Any], *, include_imports: bool = False) -> str:
        r"""Generate the source code for a :class:`TypedDict` class from a JSON dict.

        Recursively infers types from values. Nested :class:`dict` entries produce their own
        named :class:`TypedDict` class using a PascalCase derivation of the parent key,
        ordered so dependencies appear before the class that references them.

        When a field is `None` in some list items but has a real type in others, the inferred
        type is ``RealType | None``. Dict values whose keys are not valid Python identifiers
        (e.g. ``{"0": "Equals", "1": "NotEquals"}``) are emitted as ``dict[str, V]`` rather
        than a :class:`TypedDict`.

        The returned string can be printed or written directly to a ``.py`` file.

        Parameters
        ----------
        name : :class:`str`
            The class name for the root :class:`TypedDict`.
        data : dict[:class:`str`, Any]
            The JSON dict whose keys and values define the fields and their types.
        include_imports : :class:`bool`, optional
            To include "from typing import Any\n\nfrom typing_extensions import TypedDict\n" at the top of the file, by default False.

        Returns
        -------
        :class:`str`
            Python source code containing one or more :class:`TypedDict` class definitions
            preceded by the necessary imports.

        """
        class_defs: list[str] = []
        seen: set[str] = set()

        def _infer(value: Any, key: str) -> str:
            if value is None:
                return "None"
            if isinstance(value, bool):
                return "bool"
            if isinstance(value, int):
                return "int"
            if isinstance(value, float):
                return "float"
            if isinstance(value, str):
                return "str"
            if isinstance(value, dict):
                if not all(k.isidentifier() for k in value):  # type: ignore  # noqa: PGH003
                    val_types = {_infer(v, key) for v in value.values()} if value else {"Any"}  # pyright: ignore[reportUnknownVariableType]
                    val_type = next(iter(val_types)) if len(val_types) == 1 else "Any"
                    return f"dict[str, {val_type}]"
                child_name = "".join(part.title() for part in key.split("_"))
                _build(child_name, value)  # pyright: ignore[reportUnknownArgumentType]
                return child_name
            if isinstance(value, list):
                return _infer_list(value, key)  # pyright: ignore[reportUnknownArgumentType]
            return "Any"

        def _infer_list(items: list[Any], key: str) -> str:
            if not items:
                return "list[Any]"
            non_none = [v for v in items if v is not None]
            if not non_none:
                return "list[None]"
            has_none = len(non_none) < len(items)
            if all(isinstance(v, dict) for v in non_none):
                child_name = "".join(part.title() for part in key.split("_"))
                _build_merged(child_name, non_none)
                elem = child_name
            else:
                elem_types = {_infer(v, key) for v in non_none}
                elem = next(iter(elem_types)) if len(elem_types) == 1 else "Any"
            if has_none:
                elem = f"{elem} | None"
            return f"list[{elem}]"

        def _build_merged(cls_name: str, items: list[dict[str, Any]]) -> None:
            if cls_name in seen:
                return
            seen.add(cls_name)
            key_values: dict[str, list[Any]] = {}
            for item in items:
                for k, v in item.items():
                    key_values.setdefault(k, []).append(v)
            field_lines: list[str] = []
            for k, values in key_values.items():
                non_none = [v for v in values if v is not None]
                has_none = len(non_none) < len(items)
                if not non_none:
                    type_str = "None"
                elif all(isinstance(v, list) for v in non_none):
                    # Flatten all list values to infer a single unified element type,
                    # so mixed empty/non-empty lists don't produce list[Any] | list[X].
                    combined: list[Any] = [elem for v in non_none for elem in v]
                    type_str = _infer_list(combined, k)
                    if has_none:
                        type_str = f"{type_str} | None"
                else:
                    types: set[str] = {_infer(v, k) for v in non_none}
                    type_str = next(iter(types)) if len(types) == 1 else " | ".join(sorted(types))
                    if has_none:
                        type_str = f"{type_str} | None"
                field_lines.append(f"    {k}: {type_str}")
            body = "\n".join(field_lines) if field_lines else "    ..."
            class_defs.append(f"class {cls_name}(TypedDict):\n{body}")

        def _build(cls_name: str, fields: Any | dict[str, Any]) -> None:
            if cls_name in seen:
                return
            seen.add(cls_name)
            field_lines = [f"    {k}: {_infer(v, k)}" for k, v in fields.items()]
            body = "\n".join(field_lines) if field_lines else "    ..."
            class_defs.append(f"class {cls_name}(TypedDict):\n{body}")

        _build(name, data)
        imports = "from typing import Any\n\nfrom typing_extensions import TypedDict\n" if include_imports is True else ""
        return imports + "\n\n\n" + "\n\n\n".join(class_defs)

    def parse_bridge(self, bridge: Bridge) -> None:
        """Takes the :class:`Bridge` object and set's the :attr:`~Base.url` and sets :attr:`_bridge` to our Bridge object.

        .. note::
            Also validates the 2FA token.


        Parameters
        ----------
        bridge : :class:`Bridge`
            The :class:`Bridge` object to parse.

        Raises
        ------
        :exc:`ValueError`
            If 2FA Token is not provided and :attr:`_use_2fa` == True.\n
            If 2FA Token is not enclosed in single(',') or double(",") quotes.

        """
        # We use this later on in _connect to update `_session_id`;
        # so all connections will use the same session ID (if possible)
        self._bridge = bridge
        self._endpoint_url = bridge.url
        if bridge.use_2fa is True:
            if bridge.token == "":
                err = "You must provide a 2FA Token if you are using 2FA."
                raise ValueError(err)
            # elif bridge.token.startswith(("'", '"')) is False or bridge.token.endswith(("'", '"')) is False:
            #     raise ValueError("2FA Token must be enclosed in quotes.")
            # Removed starting and ending quotes
            if len(bridge.token) < 8:
                err = "Your 2FA token appears to be too short (<8 characters). Please use the code that generates the timed based tokens."
                raise ValueError(err)

    def parse_data(self, data: Union[Status, Updates]) -> Self:
        """Takes in a :class:`DataclassInstance` and iterates through it's :meth:`fields` and
        set's the values as attributes of the :class:`DataclassInstance` that called this function.

        Parameters
        ----------
        data : Union[:class:`Status`, :class:`Updates`]
            The :class:`DataclassInstance` to parse.

        Returns
        -------
        :class:`Self`
            Returns the class that called this function.

        """
        for field in fields(class_or_instance=data):
            setattr(self, field.name, getattr(data, field.name))
        return self

    # TODO: Better type hinting parameters.
    @classmethod
    def sanitize_json(cls, json: Any) -> Any:
        """|classmethod|

        Replaces spaces and underscores in the JSON response dict keys while also formatting keys to `snake_case`.

        Keys containing a ``.`` are AMP setting nodes (eg. ``ADSModule.Defaults.DefaultAuthServerURL``) and are
        left exactly as sent. Their values are still sanitized.

        Also supports a single string and will replace any of these chars ``_ ' ( )`` with nothing.

        Parameters
        ----------
        json : Any
            The JSON response data to be sanitize.

        Returns
        -------
        Any
            The JSON response data cleaned up.

        """
        if isinstance(json, list):
            # Bind the narrowed value to a typed local; `json` is Any, so everything derived from it
            # would otherwise be Unknown under strict mode.
            source_list: list[Any] = json  # pyright: ignore[reportUnknownVariableType]
            # entries: list[Any] = copy.copy(x=source_list)
            # for index, entry in enumerate(source_list):
            #     # If any of our entries are a dictionary; let's go through them.
            #     if isinstance(entry, dict):
            #         entries[index] = cls.sanitize_json(json=entry)
            # return entries
            # Only dictionary entries are sanitized. Anything else (nested lists included) is kept as is.
            return [cls.sanitize_json(json=entry) if isinstance(entry, dict) else entry for entry in source_list]

        if isinstance(json, dict):
            source_map: dict[str, Any] = json  # pyright: ignore[reportUnknownVariableType]
            # new_map: dict[str, Any] = copy.copy(x=source_map)
            # for old_key, old_value in source_map.items():
            #     new_map.pop(old_key)
            #     # AMP setting nodes (eg. `ADSModule.Defaults.DefaultAuthServerURL`) are the only dotted keys AMP sends.
            #     # None of the captured responses has a dotted field name, so a dotted key is kept exactly as sent.
            #     if "." in old_key:
            #         new_map[old_key] = cls.sanitize_json(json=old_value) if isinstance(old_value, (list, dict)) else old_value
            #         continue
            #     # To handle keys with spaces and to remove underscores that exist already.
            #     new_key: str = old_key.replace(" ", "").replace("_", "")
            #     if new_key in cls.json_key_mapping:
            #         new_key = cls.json_key_mapping[new_key]
            #     new_key = cls.camel_to_snake_re(data=new_key)
            #     new_value: Any = cls.sanitize_json(json=old_value) if isinstance(old_value, (list, dict)) else old_value
            #     new_map[new_key] = new_value
            # return new_map
            # Build a fresh dict rather than copying and popping. The key conversion is cached per key string.
            new_map: dict[str, Any] = {}
            for old_key, old_value in source_map.items():
                new_value: Any = cls.sanitize_json(json=old_value) if isinstance(old_value, (list, dict)) else old_value
                # AMP setting nodes (eg. `ADSModule.Defaults.DefaultAuthServerURL`) are the only dotted keys AMP sends.
                # None of the captured responses has a dotted field name, so a dotted key is kept exactly as sent.
                new_key: str = old_key if "." in old_key else _snake_key(old_key)
                new_map[new_key] = new_value
            return new_map

        if isinstance(json, str):
            # Typical use is to make attributes PEP8 compliant for a class.
            _new_data = copy.copy(json)
            _new_data = _new_data.replace(" ", "_")
            _new_data = _new_data.replace("(", "").replace(")", "")
            _new_data = _new_data.replace("'", "")
            if _new_data.endswith("."):
                _new_data = _new_data[:-1].lower()
            return _new_data.lower()
        return json

    @staticmethod
    def sanitize_path(path: str) -> str:
        """|classmethod|

        The path is relative to the Instances home directory. eg "/myInstanceName/" \n
        You do not need to include "." to specify the current directory as all path's start from root/home.

        .. note::
            Example `await Instance.copyFile("eula.txt", "test")` would move `./eula.txt` to `./test/eula.txt`


        .. note::
            Leading slashes are dropped, so `/` means the Instance root. Everything else is sent to AMP as given.

        .. versionchanged:: 5.0.0
            Only drops leading slashes. 4.x refused any `_`, turned `..` into `.` and stripped a leading `.`.


        Parameters
        ----------
        path : str
            The path to be sanitized.

        Returns
        -------
        :class:`str`
            Return the path without its leading slashes.

        """
        # if "_" in path:
        #     msg = "You cannot use '_' in path strings."
        #     raise ValueError(msg)

        # path = path.replace("//", "/")
        # path = path.replace("\\", "/")
        # path = path.replace("..", ".")

        # # Remove starting periods as they are un-needed when being passed into an API
        # path = path.removeprefix(".")

        # Remove starting slashes, all paths start relative to Instance root.
        return path.lstrip("/")

    @staticmethod
    def to_snake_case(data: str, /) -> str:
        """Quick function to return snake_case from camelCase.

        Parameters
        ----------
        data : :class:`str`
            The string to convert.

        Returns
        -------
        :class:`str`
            The camelCase string.

        """
        fmt: list[str] = []
        for character in data:
            if character.isupper():
                fmt.append(f"_{character.lower()}")
                continue
            fmt.append(character)
        return "".join(fmt)

    async def version_validation(self, version: BuildInfo, endpoint: str) -> None:
        """Checks the AMP version against the version an endpoint was removed in.

        Parameters
        ----------
        version : :class:`BuildInfo`
            The AMP version the endpoint was removed in.
        endpoint : :class:`str`
            The endpoint being guarded, named in the error. (eg. `"Core/GetWebserverMetrics"`)

        Raises
        ------
        :exc:`RuntimeError`
            The AMP version is `version` or newer, so it no longer has the endpoint.

        """
        result: ResponseAliasFull = await self._post(
            url="Core/GetDiagnosticsInfo",
        )

        if not isinstance(result, dict) or not is_response_type(
            result,
            DiagnosticsResponse,
            DIAGNOSTICS_REQUIRED_KEYS,
            DIAGNOSTICS_EXCLUDED_KEYS,
        ):
            LOGGER.warning("Unable to validate version Info, the API call %s may raise an error", "`Core/GetDiagnosticsInfo`")
            return
        # to_dataclass hands back the raw str when it cannot parse the version; comparing that against a
        # BuildInfo raises a TypeError, so bail out the same way an unusable response does.
        _version: BuildInfo | str = BuildInfo.to_dataclass(data=result["application_version"])
        if isinstance(_version, str):
            LOGGER.warning(
                "Unable to parse the application version %r from %s, skipping the version check.",
                _version,
                "`Core/GetDiagnosticsInfo`",
            )
            return
        # The endpoint only exists before the version it was removed in.
        if not _version < version:
            raise RuntimeError(self._version_unavailable % (f"`{endpoint}`", _version))

    def write_data_to_file(
        self,
        file_name: str,
        data: EndpointResponseError | ResponseTypeAlias | str | bool,
        path: Path = Path(__file__).parent,
        *,
        mode: str = "w+",
        **kwargs: Unpack[DumpParameters],
    ) -> None:
        """Basic file dump with json handling. If the data parameter is of type `dict`, `json.dumps()` will be used with an indent of 4.

        A `str` also goes through `json.dumps()` when `file_name` ends in `.json`.

        Parameters
        ----------
        path : :class:`Path`, optional
            The Path to write the data, default's to `Path(__file__).parent`.
        file_name : :class:`str`
            The name of the file, include the file extension.
        data : :class:`bytes | dict | str | list | bool`
            The data to write out to the path and file_name provided.
        mode : :class:`str`, optional
            The mode to open the provided file path with using `<Path.open()>`.
        **kwargs : :class:`Unpack[DumpParameters]`
            Any additional kwargs to be supplied to `<json.dumps()>`, if applicable.

        """
        kwargs["indent"] = 4

        with path.joinpath(file_name).open(mode=mode) as file:
            LOGGER.debug("<%s.%s> | Wrote data to file %s located at: %s", __name__, "write_data_to_file", path, file_name)
            if isinstance(data, bytes):
                file.write(data.decode(encoding="utf-8"))
            # elif isinstance(data, (dict, list)):
            elif isinstance(data, (dict, list)) or file_name.endswith(".json"):
                file.write(json.dumps(data, **kwargs))
            else:
                file.write(data)
        LOGGER.info(
            "<%s.%s> | File write successful to path: %s ",
            __name__,
            "write_data_to_file",
            path.joinpath(file_name).as_posix(),
        )

    @staticmethod
    def timestamp_converter(timestamp: str) -> datetime.datetime:
        """Convert either the ``C#`` date str into a Python :class:`datetime` object or the ISO format.

        .. note::
            This is for older than 2.6.0.0 AMP Installs.


        Parameters
        ----------
        timestamp : :class:`str`
            The date string to convert.

        Returns
        -------
        :class:`datetime`
            The converted string as a :class:`datetime` object.

        """
        return timestamp_converter(timestamp=timestamp)
