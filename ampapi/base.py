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
from collections.abc import Callable, Iterable
from dataclasses import fields, is_dataclass
from datetime import timezone
from json import JSONEncoder
from pathlib import Path
from pprint import pformat
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Optional, ParamSpec, TypedDict, Union

import aiohttp
from aiohttp import ClientResponse
from dataclass_wizard import fromdict
from pyotp import TOTP
from typing_extensions import Unpack, overload

from .backoff import ExponentialBackoff
from .bridge import Bridge
from .modules import ActionResult, ActionResultError, APISession, BuildInfo, Diagnostics, LoginResults, Status

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Callable, Coroutine, Iterable
    from datetime import timedelta
    from typing import Concatenate

    from _typeshed import DataclassInstance
    from aiohttp.client import _RequestOptions as AioHTTPRequestOptions  # pyright: ignore[reportPrivateUsage]
    from typing_extensions import ParamSpec, Self, TypeVar

    from ._types import ResponseTypeAlias
    from .modules import APIResponseDataTableAlias, Controller, Instance, Updates

    D = TypeVar("D", bound="Base")
    T = ParamSpec("T")
    F = TypeVar("F")
    X = TypeVar("X", bound=DataclassInstance)

__all__ = ("Base", "ResponseHandlerOptions")

LOGGER: logging.Logger = logging.getLogger(__name__)


class ResponseHandlerOptions(TypedDict, total=False):
    """Response handling parameters.

    Options:
    --------
    sanitize_json: :class:`bool`
        ...
    to_file: :class:`bool`
        ...
    path: :class:`pathlib.Path`
        ...

    """

    sanitize_json: bool
    to_file: bool
    path: pathlib.Path


class DumpParameters(TypedDict, total=False):
    skipkeys: bool
    ensure_ascii: bool
    check_circular: bool
    allow_nan: bool
    cls: type[JSONEncoder] | None
    indent: None | int | str
    separators: tuple[str, str] | None
    default: Callable[[Any], Any] | None
    sort_keys: bool


class Base:
    """Contains the base functions for all AMP API endpoints and handles the parsing of Bridge data.

    .. warning::
        Do not overwrite or alter the :attr:`instance_id`.


    .. note::
        A session expires after 240sec of inactivity per Cube Coders AMP. If for any reason you want to change that value; set the attribute :attr:`session_ttl`.\n


    Attributes
    ----------
    api_url: :class:`str`
        The URL to access the Web Panel. This comes from your :class:`APIParams`.
    session_ttl: :class:`int`
        How long before the session id expires in seconds, default is 240 seconds.
    instance_id: :class:`str`
        The Instance id is a string determined by AMP. \n
        This attribute will be set automatically after making a :meth:`login` request, default is "O".
    session: :class:`aiohttp.ClientSession`
        A static Session to use, otherwise the class will generate it's own as needed.

    """

    # Private Attributes
    _bridge: Bridge
    _backoff: ExponentialBackoff[bool]
    _module: str
    _format_data: ClassVar[bool] = True
    _url: str
    _instance_id: str
    _session_ttl: ClassVar[int] = 240

    # Error response strings.
    _ads_only: ClassVar[str] = "This API call is only available to <class:`ADSModule`> type classes."
    _failed_api: ClassVar[str] = "The API call returned a malformed response."
    _minecraft_only: ClassVar[str] = "This API call is only available on Minecraft type instances."
    _no_bridge: ClassVar[str] = "Failed to setup connection. You need to initiate `<class Bridge>` first."
    _no_controller: ClassVar[str] = "The function failed as the <class:`AMPControllerInstance`> was not properly initialized and set."
    _no_data: ClassVar[str] = "Failed to receive any data from post request."
    _unauthorized_access: ClassVar[str] = "The user does not have the required permissions to interact with this instance."
    _instance_offline: ClassVar[str] = "The requested Instance is not available at this time. | URL: %s"
    _version_unavailable: ClassVar[str] = "The API call %s is no longer available at this version of AMP %s"

    # These are used to handle JSON keys that cannot be parsed properly via regex.
    # See :func:`camel_to_snake_re`
    json_key_mapping: ClassVar[dict[str, str]] = {
        "ContainerCPUs": "container_cpus",
        "InstalledRAMMB": "installed_ram_mb",
        "FreeRAMMB": "free_ram_mb",
        "AvailableIPs": "available_ips",
        "SecurityandPrivacy": "security_and_privacy",
    }


    @property
    def module(self) -> str:
        """The AMP Instance ``type``.

        Current Values: `ADS` | `Minecraft` | `Generic` | `SRCDS`

        Returns
        -------
        :class:`str`
            The AMP Instance ``type`` as a string.

        """
        return self._module

    @property
    def format_data(self) -> bool:
        """Controls whether the data returned from an API endpoint is formatted or not.\n
        Default is ``True`` which comes from the global parameter ``FORMAT_DATA``.

        .. note::
            ``True`` = formatted \n
            ``False`` = unformatted


        Returns
        -------
        :class:`bool`
            Returns ``True`` or ``False``.

        """
        return Base._format_data

    @format_data.setter
    def format_data(self, value: bool) -> None:
        Base._format_data = value

    @property
    def session_ttl(self) -> int:
        """How long before the session id expires in seconds, default is 240 seconds."""
        return Base._session_ttl

    @session_ttl.setter
    def session_ttl(self, value: int) -> None:
        Base._session_ttl = value

    @property
    def instance_id(self) -> str:
        """AMP Instance ID."""
        return self._instance_id

    @property
    def url(self) -> str:
        """The URL to access the AMP Instance API endpoints."""
        return self._url

    def __init__(self, *, bridge: Optional[Bridge] = None, session: Optional[aiohttp.ClientSession] = None) -> None:
        self._url = ""
        self._instance_id = "0"

        if bridge is None:
            try:
                self._bridge = Bridge._get_bridge()  # pyright: ignore[reportPrivateUsage]
            except ValueError:
                LOGGER.error(
                    "<%s.%s> | Failed to initialize, you must either must use a Singleton <Bridge> object or pass into the __init__.",
                    __class__.__name__,
                    "__init__",
                )
                return
        else:
            self.parse_bridge(bridge=bridge)

        self._backoff = ExponentialBackoff(integral=True)

        LOGGER.debug("<%s.%s> | BRIDGE: %s | SESSION: %s |", __class__.__name__, "__init__", bridge, session)
        self.session: aiohttp.ClientSession | None = session


    @staticmethod
    def ads_only(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """Checks the class attribute ``.module`` and is equal to ``ADS`` or if the type of Instance using the function is AMPADSInstance.

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
            The API call is only allowed to be run on a type(:py:class:`AMPADSInstance`).

        """

        @functools.wraps(wrapped=func)
        def wrapper_ads_only(self: D, *args: T.args, **kwargs: T.kwargs) -> Coroutine[None, None, F]:
            from .adsmodule import ADSModule  # noqa: PLC0415
            from .instance import AMPADSInstance  # noqa: PLC0415

            if self.module == "ADS" or type(self) is AMPADSInstance or isinstance(self, ADSModule):
                return func(self, *args, **kwargs)
            raise RuntimeError(self._ads_only)

        return wrapper_ads_only

    # async def _call_api(
    #     self,
    #     api: str,
    #     parameters: Union[None, dict[str, Any]] = None,
    #     format_data: Union[bool, None] = None,
    #     format_: Union[type[Union[X, APIResponseDataTableAlias]], None] = None,
    #     sanitize_json: bool = True,
    #     _use_from_dict: bool = True,
    #     _auto_unpack: bool = True,
    #     _no_data: bool = False,
    # ) -> Any:
    #     """|coro|.

    #     Uses :class:`aiohttp.ClientSession` post request to access the AMP API endpoints. \n

    #     .. note::
    #         Will populate the ``SESSIONID`` key for :param:`parameters` if it is not provided. This is the default behavior.

    #     .. warning::
    #         Will return an :class:`ActionResultError` class if any errors happen when attempting to call the API.

    #     Parameters
    #     ----------
    #     api: :class:`str`
    #         The API endpoint to call, eg ``Core/GetModuleInfo``.
    #     parameters: Union[None, dict[:class:`str`, Any]], optional
    #         The parameters to pass to the API endpoint, by default None.
    #     format_data: Union[:class:`bool`, None], optional
    #         Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.
    #     format_: :py:class:`DataclassInstance`, optional
    #         The dataclass the JSON response will formatted to, by default None.
    #     sanitize_json: :class:`bool`, optional
    #         Replaces invalid characters in our JSON responses, by default True.
    #     _use_from_dict: :class:`bool`, optional
    #         Controls whether the data will use :meth:`fromdict` of dataclass wizard to unpack the data.
    #         Typical usage case is to handle nested :class:`DataclassInstance`, by default True.
    #     _auto_unpack: :class:`bool`, optional
    #         Controls whether the data will be unpacked automatically via ``(**data)``, by default True.
    #     _no_data: :class:`bool`, optional
    #         Informs the connection that the API does not have a JSON response, by default False.

    #     Returns
    #     -------
    #     Any
    #         Typical returns are of the same type that is passed in to ``format_``, either in an :class:`Iterable` or not depending on the data,
    #         otherwise returns an unformatted JSON response if :attr:`format_data` or ``FORMAT_DATA`` is False.

    #     """
    #     global FORMAT_DATA

    #     post_req: ClientResponse | None
    #     LOGGER.debug("_call_api -> %s was called with %s", api, parameters)

    #     # This should save us some boiler plate code throughout our API calls.
    #     if parameters is None:
    #         parameters = {}

    #     api_session: APISession = self._bridge._sessions.get(
    #         self._instance_id,
    #         APISession(id="0", ttl=datetime.datetime.now(tz=timezone.utc)),
    #     )  # pyright: ignore[reportPrivateUsage]

    #     # ?UPCOMING(@k8thekat): - AMP Update; moving SessionID to headers.
    #     # This is to handle AMPs updated Authorization
    #     header: dict[str, str] = {"Accept": "text/javascript"}
    #     if self._old_auth is True:
    #         parameters["SESSIONID"] = api_session.id
    #     else:
    #         header["Authorization"] = f"Bearer {api_session.id}"

    #     json_data: str = json.dumps(obj=parameters)

    #     _url: str = self._url + "/API/" + api
    #     LOGGER.debug("SESSION GET %s | API CALL: %s | API URL: %s | DATA: %s", self._instance_id, api, _url, pformat(json_data))
    #     if self.session is None:
    #         self.session = aiohttp.ClientSession()

    #     try:
    #         post_req = await self.session.post(url=_url, headers=header, data=json_data)
    #     # We have a dynamic backoff function to prevent reconnect attempts to frequently.
    #     except RuntimeError as e:
    #         # Attempting to re-open the session if it is somehow closed during usage.
    #         if isinstance(e.args[0], str) and "session is closed" in e.args[0].lower():
    #             self.session = aiohttp.ClientSession()

    #         retry: float = self._backoff.delay()
    #         LOGGER.error("<Base._call_api> encountered a <RuntimeError> and will retry in %s. | Exception: %s", retry, e)
    #         await asyncio.sleep(delay=retry)
    #         return await self._call_api(
    #             api=api,
    #             parameters=parameters,
    #             format_data=format_data,
    #             format_=format_,
    #             sanitize_json=sanitize_json,
    #             _use_from_dict=_use_from_dict,
    #             _auto_unpack=_auto_unpack,
    #             _no_data=_no_data,
    #         )

    #     except Exception as e:
    #         retry = self._backoff.delay()
    #         LOGGER.error("<Base._call_api> encountered an Exception and will retry in %s. | Exception: %s", retry, e)
    #         await asyncio.sleep(delay=retry)
    #         return ActionResultError(status=False, reason="UNK", result=ValueError(e))

    #     if post_req.content_length == 0:
    #         return ActionResultError(status=False, reason="Content Length is 0", result=ValueError(self._no_data))
    #         # raise ValueError(self._no_data)

    #     if post_req.status != 200:
    #         return ActionResultError(status=False, reason="Status Code not equal to 200", result=ConnectionError(self._no_data))
    #         # raise ConnectionError(self._no_data)

    #     post_req_json: Any = await post_req.json()

    #     if post_req_json is None and _no_data is False:
    #         return ActionResultError(status=False, reason="JSON is None and Data is None", result=ConnectionError(self._no_data))
    #         # raise ConnectionError(self._no_data)
    #     if _no_data is True:
    #         return None

    #     # They removed "result" from all replies thus breaking most if not all future code.
    #     # This was an old example from pre 2.3 AMP API that could have the following return:
    #     # `{'resultReason': 'Internal Auth - No reason given', 'success': False, 'result': 0}`
    #     LOGGER.debug(
    #         "URL: %s | aiohttp.ClientResponse.json() type: %s | _call_api parameters: %s",
    #         api,
    #         type(post_req_json),
    #         parameters,
    #     )
    #     LOGGER.debug("aiohttp.ClientResponse.json() formatted: %s", pformat(post_req_json))
    #     if sanitize_json is True:
    #         post_req_json = self.sanitize_json(post_req_json)
    #         LOGGER.debug("Sanitize json: %s | Sanitized data: %s", sanitize_json, pformat(post_req_json))

    #     if isinstance(post_req_json, dict):
    #         if "title" in post_req_json:
    #             post_req_json = post_req_json["title"]
    #             if isinstance(post_req_json, str) and (post_req_json == "Unauthorized Access" or post_req_json == "Instance Unavailable"):
    #                 LOGGER.error("%s failed because of %s", api, post_req_json)
    #                 api_session = APISession(id="0", ttl=datetime.now())
    #                 self._bridge._sessions.update({self._instance_id: api_session})
    #                 if post_req_json == "Unauthorized Access":
    #                     # New Header Auth bearer implementation.
    #                     if self._old_auth is False:
    #                         self._old_auth = True
    #                         return await self._call_api(
    #                             api=api,
    #                             parameters=parameters,
    #                             format_data=format_data,
    #                             format_=format_,
    #                             sanitize_json=sanitize_json,
    #                             _use_from_dict=_use_from_dict,
    #                             _auto_unpack=_auto_unpack,
    #                             _no_data=_no_data,
    #                         )

    #                     return ActionResultError(
    #                         status=False,
    #                         reason="Unauthorized Access",
    #                         result=PermissionError(self._unauthorized_access),
    #                     )

    #                     # raise PermissionError(self._unauthorized_access)
    #                 if post_req_json == "Instance Unavailable":
    #                     return ActionResultError(
    #                         status=False,
    #                         reason="Instance Unavailable",
    #                         result=ConnectionError(self._instance_offline, self._url),
    #                     )
    #                     # raise ConnectionError(self._instance_offline, self.url)

    #         elif api == "Core/Login":
    #             return LoginResults(**post_req_json)

    #         # ? Suggestion
    #         # This is breaking newer code as it's grabbing the inner key versus older version of AMP having two `result` keys.
    #         # We may need to re-add this fuctionality in a different manner going forward.
    #         # elif "result" in post_req_json:
    #         #     post_req_json = post_req_json["result"]

    #         #     if isinstance(post_req_json, bool) and post_req_json is False:
    #         #         LOGGER.error("%s failed because of %s", api, post_req_json)
    #         #         raise ValueError(self._failed_api)

    #         elif isinstance(post_req_json, dict) and "status" in post_req_json and post_req_json["status"] is False:
    #             LOGGER.error("%s failed because of Status: %s", api, post_req_json)
    #             return ActionResultError(status=False, reason="Status is False", result=ValueError(self._failed_api))
    #             # return ValueError(self._failed_api)

    #     LOGGER.debug(
    #         "DEBUG: FORMAT DATA | local Format Data: %s | global Format Data: %s | format_: %s | POST REQ TYPE: %s",
    #         format_data,
    #         FORMAT_DATA,
    #         format_,
    #         type(post_req_json),
    #     )
    #     if (format_ is None or format_data is False) or (format_data is None and FORMAT_DATA is False):
    #         return post_req_json

    #     if isinstance(post_req_json, (dict, list)) and ((format_data is True) or (format_data is None and FORMAT_DATA is True)):
    #         return self.json_to_dataclass(json=post_req_json, format_=format_, _use_from_dict=_use_from_dict, _auto_unpack=_auto_unpack)
    #     return post_req_json

    @overload
    async def _post(
        self,
        url: str,
        parameters: Union[None, dict[str, Any]] = None,
        *,
        no_data: Literal[True],
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResultError | None: ...

    @overload
    async def _post(
        self,
        url: str,
        parameters: Union[None, dict[str, Any]] = None,
        *,
        no_data: bool = ...,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResultError | ResponseTypeAlias | bool | None: ...

    async def _post(
        self,
        url: str,
        parameters: Union[None, dict[str, Any]] = None,
        *,
        no_data: bool = False,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResultError | ResponseTypeAlias | str | bool | None:
        """|coro|

        Makes a POST request via :class:`aiohttp.ClientSession` and passes the response to :meth:`_response_handler`.

        .. warning::
            Will return an :class:`ActionResultError` if any errors occur when attempting to call the API.


        Parameters
        ----------
        url: :class:`str`
            The API endpoint to POST to, excluding the base panel URL and ``/API/`` prefix, eg ``Core/GetModuleInfo``.
        parameters: Union[None, dict[:class:`str`, Any]], optional
            The parameters to supply to the endpoint, by default None.
        no_data: :class:`bool`, optional
            Skip processing the :class:`ClientResponse` body when the endpoint returns no data, by default False.
        request_params: :class:`AioHTTPRequestOptions` | None, optional
            Extra keyword arguments forwarded directly to :meth:`aiohttp.ClientSession.post`. The ``headers``
            and ``data`` keys are always populated automatically, by default None.

            .. code-block:: python

                headers = {"Accept": "text/javascript", "Authorization": f"Bearer {api_session.id}"}
                data = json.dumps(parameters)

        **response_params: :class:`Unpack[ResponseHandlerOptions]`
            Keyword arguments forwarded to :meth:`_response_handler`. See :class:`ResponseHandlerOptions` for details.

        Returns
        -------
        :class:`ActionResultError` | :class:`ActionResult` | :class:`ResponseTypeAlias` | None
            The processed response on a successful (2xx) status, ``None`` if ``no_data`` is ``True``,
            otherwise an :class:`ActionResultError`.

        """
        api_session: APISession = self._bridge._sessions.get(  # pyright: ignore[reportPrivateUsage]
            self._instance_id,
            APISession(id="0", ttl=datetime.datetime.now(tz=timezone.utc)),
        )
        if self.session is None:
            self.session = aiohttp.ClientSession()

        _url: str = self._url + "/API/" + url

        # Ver. 2.6.2.8 Authorization header key change.
        if request_params is None:
            request_params = {
                "headers": {"Accept": "text/javascript", "Authorization": f"Bearer {api_session.id}"},
                "data": json.dumps(parameters),
            }

        else:
            request_params["headers"] = {"Accept": "text/javascript", "Authorization": f"Bearer {api_session.id}"}
            request_params["data"] = json.dumps(parameters)

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

            retry: int | float = self._backoff.delay()
            LOGGER.error(
                "<%s.%s> encountered an <RuntimeError> and will retry in %s. | Exception: %s",
                __class__.__name__,
                "_post",
                retry,
                e,
            )
            await asyncio.sleep(delay=retry)
            # Attempt a re-call...
            return await self._post(url=url, parameters=parameters, **request_params)

        # ? Suggestion
        # Further see what exceptions may be raised to narrow this comparison as the noqa can be avoided.
        except Exception as e:  # noqa: BLE001
            LOGGER.error(
                "<%s.%s> encountered an <Exception> | Exception: %s",
                __class__.__name__,
                "_post",
                e,
            )
            return ActionResultError(status=False, reason="Exception was raised.", result=ValueError(e))

        if response.content_length == 0:
            return ActionResultError(status=False, reason="The HTTP Header content length was 0.", result=ValueError(self._no_data))

        match response.status:
            case status if 200 <= status < 300:
                if no_data is True:
                    return None
                return await self._response_handler(response=response, **response_params)

            case 400:
                return ActionResultError(status=False, reason="Bad Request", result=ValueError(f"Bad Request [400]: {url}"))
            case 401:
                return ActionResultError(status=False, reason="Unauthorized", result=PermissionError(f"Unauthorized [401]: {url}"))
            case 403:
                return ActionResultError(status=False, reason="Forbidden", result=PermissionError(f"Forbidden [403]: {url}"))
            case 404:
                return ActionResultError(status=False, reason="Not Found", result=ConnectionError(f"Not Found [404]: {url}"))
            case 408:
                return ActionResultError(status=False, reason="Request Timeout", result=TimeoutError(f"Request Timeout [408]: {url}"))
            case 429:
                return ActionResultError(
                    status=False,
                    reason="Too Many Requests",
                    result=ConnectionError(f"Too Many Requests [429]: {url}"),
                )
            case 500:
                return ActionResultError(
                    status=False,
                    reason="Internal Server Error",
                    result=ConnectionError(f"Internal Server Error [500]: {url}"),
                )
            case 502:
                return ActionResultError(status=False, reason="Bad Gateway", result=ConnectionError(f"Bad Gateway [502]: {url}"))
            case 503:
                return ActionResultError(
                    status=False,
                    reason="Service Unavailable",
                    result=ConnectionError(f"Service Unavailable [503]: {url}"),
                )
            case 504:
                return ActionResultError(status=False, reason="Gateway Timeout", result=TimeoutError(f"Gateway Timeout [504]: {url}"))
            case _:
                return ActionResultError(
                    status=False,
                    reason=f"Unexpected status [{response.status}]",
                    result=ConnectionError(f"Unexpected status [{response.status}]: {url}"),
                )

    # TODO: Flesh out responses via API calls to better type def "response_json".
    async def _response_handler(
        self,
        response: ClientResponse,
        *,
        sanitize_json: bool = True,
        to_file: bool = False,
        path: Optional[pathlib.Path] = None,
    ) -> ResponseTypeAlias | ActionResultError | str | bool | None:
        """|coro|

        Processes a :class:`aiohttp.ClientResponse` into a parsed response object.

        .. warning::
            Will return an :class:`ActionResultError` if the response JSON is ``None``,
            indicates ``"Unauthorized Access"``, ``"Instance Unavailable"``, or has ``status`` of ``False``.


        Parameters
        ----------
        response: :class:`aiohttp.ClientResponse`
            The raw HTTP response to process.
        sanitize_json: :class:`bool`, optional
            Run the parsed JSON through :meth:`sanitize_json` before returning, by default True.
        to_file: :class:`bool`, optional
            Write the response JSON to a file at ``path``, by default False.
        path: :class:`pathlib.Path` | None, optional
            Directory to write the response file to when ``to_file`` is ``True``, by default None.

        Returns
        -------
        :class:`ResponseTypeAlias` | :class:`ActionResultError` | Any
            The parsed and optionally sanitized JSON response, or an :class:`ActionResultError` on failure.

        Raises
        ------
        :exc:`ValueError`
            If ``to_file`` is ``True`` but ``path`` is ``None``.
        :exc:`FileNotFoundError`
            If the provided ``path`` does not exist.

        """
        if to_file is True and path is None:
            msg = "Please provide a valid <Path> object when using `to_file` parameter."
            raise ValueError(msg)

        try:
            response_json: ResponseTypeAlias | str | bool | None = await response.json()
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
            return ActionResultError(status=False, reason="<ClientResponse> JSON returned <None>.", result=ValueError(self._no_data))

        if sanitize_json is True:
            response_json = self.sanitize_json(response_json)
        if isinstance(response_json, bool):
            return response_json

        if to_file is True and path is not None and response_json is not None:
            # ? SUGGESTION: May have to make this async in the future if it becomes blocking.
            if path.exists() is False:
                msg = "The path provided does not exist. %s"
                raise FileNotFoundError(msg, path)
            self.write_data_to_file(file_name=response.url.name.lower() + ".json", data=response_json, path=path)

        # This will take time.
        # When getting an error, typical structure is ResponseError and will have the "title" key.
        if isinstance(response_json, dict) and "title" in response_json:
            response_json = response_json.get("title")
            if response_json == "Unauthorized Access" or response_json == "Instance Unavailable":
                LOGGER.error(
                    "<%s.%s> failed because of %s. | URL: %s",
                    __class__.__name__,
                    "_response_handler",
                    response_json,
                    response.url,
                )
                api_session = APISession(id="0", ttl=datetime.datetime.now(tz=timezone.utc))
                self._bridge._sessions.update({self._instance_id: api_session})  # pyright: ignore[reportPrivateUsage]
                if response_json == "Unauthorized Access":
                    return ActionResultError(
                        status=False,
                        reason="Unauthorized Access",
                        result=PermissionError(self._unauthorized_access),
                    )

                if response_json == "Instance Unavailable":
                    return ActionResultError(
                        status=False,
                        reason="Instance Unavailable",
                        result=ConnectionError(self._instance_offline, self._url),
                    )
                    # raise ConnectionError(self._instance_offline, self.url)
        elif isinstance(response_json, dict) and "status" in response_json and response_json["status"] is False:
            LOGGER.error("%s failed because of Status: %s", response.url, response_json["status"])
            return ActionResultError(status=False, reason="Status is False", result=ValueError(self._failed_api))

        return response_json

    async def _reauth(self) -> Any:
        """|coro|
        Logs into AMP via "API/Core/Login" endpoint using your :class:`Bridge` object.

        .. note::
            If Applicable handles your 2FA using :class:`TOTP` \n
            Stores the ``SESSIONID`` via :class:`APISession` dataclass for future usage inside the :class:`Bridge` object.


        Returns
        -------
        :class:`LoginResults` | None
            The results from ``API/Core/Login`` as a dataclass.

        Raises
        ------
        :exc:`ValueError`
            If the 2 Factor Authentication code is not a formatted properly.
            - *aka* the :attr:`~Bridge.token` when making the :class:`Bridge` object.

        """
        code: Union[str, TOTP] = ""

        # get our InstanceID and use it to key for session_id
        session: APISession = self._bridge._sessions.get(self._instance_id, APISession(id="0", ttl=datetime.datetime.now(tz=timezone.utc)))  # pyright: ignore[reportPrivateUsage]
        # if isinstance(session, APISession):
        ttl: timedelta = datetime.datetime.now(tz=timezone.utc) - session.ttl
        if ttl.seconds > self.session_ttl:
            session_id = "0"
        else:
            session_id: str = session.id

        if session_id == "0":
            if self._bridge.use_2fa is True:
                try:
                    # Handles time based 2Factory Auth Key/Code
                    code = TOTP(self._bridge.token).now()

                except AttributeError:
                    msg = "Please check your 2 Factor Code, should not contain spaces, escape characters and it must be enclosed in quotes!"
                    raise ValueError(msg) from AttributeError
            try:
                parameters: dict[str, Any] = {
                    "username": self._bridge.user,
                    "password": self._bridge.password,
                    "token": code,
                    "rememberMe": True,
                }

                result = await self.call_end_point(endpoint="Core/Login", parameters=parameters)
                if isinstance(result, dict):
                    # This is our new sessions table to correlate InstanceID to a sessionID.
                    api_session = APISession(id=result.get("session_id", "0"), ttl=datetime.datetime.now(tz=timezone.utc))
                    self._bridge._sessions.update({self._instance_id: api_session})  # pyright: ignore[reportPrivateUsage]
                    return result

            # TODO: Fix blind exception catching.
            except Exception as e:
                LOGGER.warning("Core/Login Exception:", exc_info=e)
                # print(e)

            else:
                LOGGER.warning("Failed response from '%s' in %s.%s", "Core/Login", __class__.__name__, "_reauth")
                return result
        else:
            return None


    async def clean_up(self) -> None:
        LOGGER.debug("<%s.%s> | Closing any open `aiohttp.ClientSession`", __class__.__name__, "clean_up")
        await self.session.close()


    # TODO: See about supporting automatic login handling like other Endpoints.
    async def call_end_point(
        self,
        endpoint: str,
        parameters: None | dict[str, Any] = None,
        *,
        request_params: Optional[AioHTTPRequestOptions] = None,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ActionResultError | ActionResult | ResponseTypeAlias | None:
        """|coro|

        Generic function for calling any API endpoint. Some API endpoints require the Instance module type to be ADS. \n
        See `/api_spec_sheets/ADS_api_spec.md` or `/api_spec_sheets/Minecraft_api_spec.md` for full API endpoints and parameter information.


        .. note::
            Parameter key "SESSIONID" is handled for you.


        .. warning::
            DO NOT include the full URL - *Exclude: www.yourAMPURL.com/API/*\n

        .. warning::
            You must login first prior to calling this function!



        Parameters
        ----------
        api: :class:`str`
            The AMP API endpoint to call. eg "Core/GetModuleInfo"
        parameters : None | dict[:class:`str`, Any], optional
            The parameters to pass to the API endpoint, by default is None

        Returns
        -------
        dict[:class:`str`, Any] :
           The JSON response from the API endpoint.

        """
        # await self._reauth()
        return await self._post(url=endpoint, parameters=parameters, request_params=request_params, **response_params)

    @staticmethod
    def camel_to_snake_re(data: str) -> str:
        """A simple regex pattern applied to a string to remove Camel Casing and apply snake_case.

        .. note::
            This will fail on entries with an underscore between to capital characters. |  *eg (Tool_Version = tool__version)*\n

        Parameters
        ----------
        data: :class:`str`
            The string to be converted.

        Returns
        -------
        :class:`str`
            The converted string from CamelCase to snake_case.

        """
        # Pre-pass: collapse plural acronyms so e.g. "IDs" -> "Ids" and "CPUs" -> "Cpus"
        # before the main passes split them incorrectly into "i_ds" / "cp_us".
        data = re.sub(
            pattern=r"([A-Z]{2,})(s)(?=[^a-z]|$)",
            repl=lambda m: m.group(1)[0] + m.group(1)[1:].lower() + m.group(2),
            string=data,
        )
        data = re.sub(pattern="(.)([A-Z][a-z]+)", repl=r"\1_\2", string=data)
        return re.sub(pattern="([a-z0-9])([A-Z])", repl=r"\1_\2", string=data).lower()

    @staticmethod
    def camel_case_data(data: dict[str, Any]) -> dict[str, Any]:
        """Calls the :meth:`title` on every dict key.

        Parameters
        ----------
        data: dict[:class:`str`, Any]
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

    # @staticmethod
    # def dataclass_to_dict(dataclass_: DataclassInstance) -> dict[str, Any]:
    #     """Convert a dataclass to a dictionary.

    #     Parameters
    #     ----------
    #     dataclass_: :class:`DataclassInstance`
    #         The dataclass to convert.

    #     Returns
    #     -------
    #     dict[:class:`str`, Any]
    #         The converted dataclass as a dict.

    #     Raises
    #     ------
    #     :exc:`TypeError`
    #         When the object passed in is not of type(:class:`DataclassInstance`).

    #     """
    #     parameters: dict[Any, Any] = {}
    #     if is_dataclass(dataclass_) is False:
    #         raise TypeError(f"The object {dataclass_} is not of the same type as <dataclass>.")
    #     for field in fields(class_or_instance=dataclass_):
    #         value: Any = getattr(dataclass_, field.name)
    #         if value is None:
    #             continue
    #         parameters[field.name] = value
    #     return parameters

    # @staticmethod
    # def json_to_dataclass(
    #     json: Iterable[Any],
    #     format_: type[Union[X, APIResponseDataTableAlias]],
    #     _use_from_dict: bool,
    #     _auto_unpack: bool,
    # ) -> X | list[APIResponseDataTableAlias | X] | APIResponseDataTableAlias | Iterable[Any]:
    #     """Format the JSON response data to a dataclass.

    #     .. note::
    #         All JSON response data will be sanitized before it is turned into a dataclass. See :meth:`sanitize_json`.

    #     Parameters
    #     ----------
    #     json: Any
    #         JSON response data to format.
    #     format_: Union[:class:`DataclassInstance`, class:`DeploymentTemplate`]
    #         Must be of type :class:`DataclassInstance` or similar to unpack the JSON response data.
    #     _use_from_dict: :class:`bool`
    #         Use :meth:`fromdict` from dataclass_wizard to unpack the JSON response data.
    #         - Typically this is used to handle nested :class:`DataclassInstance`.
    #     _auto_unpack: :class:`bool`
    #         Use ``**data`` to unpack the JSON response data.

    #     Returns
    #     -------
    #     X | list[:class:`DeploymentTemplate` | X] | :class:`DeploymentTemplate` | None
    #         Either a list or single entry of :class:`DataclassInstance`.

    #     """
    #     if isinstance(json, list):
    #         # _use_from_dict is to handle nested Dataclasses.
    #         if _use_from_dict is True:
    #             return [fromdict(format_, data) for data in json]

    #         # Self explanatory; uses the `**` annotation to unpack our data.
    #         if _auto_unpack is True:
    #             return [format_(**data) for data in json]

    #         return [format_(data) for data in json]  # pyright: ignore[reportCallIssue]

    #     if isinstance(json, dict):
    #         # _use_from_dict is to handle nested Dataclasses.
    #         if _use_from_dict is True:
    #             return fromdict(format_, json)  # pyright: ignore[reportUnknownArgumentType]

    #         if _auto_unpack is True:
    #             return format_(**json)  # pyright: ignore[reportUnknownArgumentType]

    #         return format_(json)  # pyright: ignore[reportCallIssue]
    #     return json

    @staticmethod
    def json_to_typeddict(name: str, data: dict[str, Any], *, include_imports: bool = False) -> str:
        """Generate the source code for a :class:`TypedDict` class from a JSON dict.

        Recursively infers types from values. Nested :class:`dict` entries produce their own
        named :class:`TypedDict` class using a PascalCase derivation of the parent key,
        ordered so dependencies appear before the class that references them.

        The returned string can be printed or written directly to a ``.py`` file.

        Parameters
        ----------
        name: :class:`str`
            The class name for the root :class:`TypedDict`.
        data: dict[:class:`str`, Any]
            The JSON dict whose keys and values define the fields and their types.
        include_imports: :class:`bool`
            To include "from typing import Any\n\nfrom typing_extensions import TypedDict\n" at the top of the file.

        Returns
        -------
        :class:`str`
            Python source code containing one or more :class:`TypedDict` class definitions
            preceded by the necessary imports.

        """
        class_defs: list[str] = []

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
                child_name = "".join(part.title() for part in key.split("_"))
                _build(child_name, value)  # pyright: ignore[reportUnknownArgumentType]
                return child_name
            if isinstance(value, list):
                if not value:
                    return "list[Any]"
                first = value[0]  # pyright: ignore[reportUnknownVariableType]
                if isinstance(first, dict):
                    child_name = "".join(part.title() for part in key.split("_"))
                    _build(child_name, first)  # pyright: ignore[reportUnknownArgumentType]
                    return f"list[{child_name}]"
                elem_types = {_infer(v, key) for v in value}  # pyright: ignore[reportUnknownVariableType]
                elem = next(iter(elem_types)) if len(elem_types) == 1 else "Any"
                return f"list[{elem}]"
            return "Any"

        def _build(cls_name: str, fields: dict[str, Any]) -> None:
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
        bridge: :class:`Bridge`
            The :class:`Bridge` object to parse.

        Raises
        ------
        :exc:`ValueError`
            If 2FA Token is not provided and :attr:`_use_2fa` == True.\n
            If 2FA Token is not enclosed in single(',') or double(",") quotes.

        """
        # We use this later on in _connect to update `_session_id`;
        # so all connections will use the same session id (if possible)
        self._bridge = bridge
        self._url = bridge.url
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

    def parse_data(self, data: Union[Controller, Instance, Status, Updates]) -> Self:
        """Takes in a :class:`DataclassInstance` and iterates through it's :meth:`fields` and
        set's the values as attributes of the :class:`DataclassInstance` that called this function.

        Parameters
        ----------
        data: Union[:class:`Controller`, :class:`Instance`, :class:`Status`, :class:`Updates`]
            The :class:`DataclassInstance` to parse.

        Returns
        -------
        :class:`Self`
            Returns the class that called this function.

        """
        for field in fields(class_or_instance=data):
            setattr(self, field.name, getattr(data, field.name))
        return self

    # @overload
    # @classmethod
    # def sanitize_json(cls, json: str) -> str: ...

    # @overload
    # @classmethod
    # def sanitize_json(cls, json: ResponseTypeAlias) -> ResponseTypeAlias: ...

    # TODO: Better type hinting parameters.
    @classmethod
    def sanitize_json(cls, json: Any) -> Any:
        """|classmethod|

        Replaces spaces and underscores in the JSON response dict keys while also formatting keys to ``snake_case``.

        Also supports a single string and will replace any of these chars ``_ ' ( )`` with nothing.

        Parameters
        ----------
        json: Any
            The JSON response data to be sanitize.

        Returns
        -------
        Iterable[Any]
            The JSON response data cleaned up.

        """
        if isinstance(json, list):
            # print("JSON is a list")
            _new_data = copy.copy(x=json)
            for i in range(0, len(json), 1):
                # If any of our entries are a dictionary; let's go through them.
                if isinstance(json[i], dict):
                    # print("List New Data", json[i])
                    _new_data[i] = cls.sanitize_json(json=json[i])
                    # print("Sanitized New Data", _new_data[i])
                    # _new_data[entry] = cls.sanitize_json(json=entry)
            return _new_data

        if isinstance(json, dict):
            # print("JSON is a dict")
            _new_data = copy.copy(x=json)
            for key, value in json.items():
                # print("DICT Not cleaned up", key, value)
                _new_data.pop(key)
                # To handle keys with spaces and to remove underscores that exist already.
                key: str = key.replace(" ", "")
                key: str = key.replace("_", "")
                if key in cls.json_key_mapping:
                    # print("KEY MAPPING OVERWRITE", key, cls.json_key_mapping[key])
                    key = cls.json_key_mapping[key]
                key = cls.camel_to_snake_re(data=key)
                if isinstance(value, (list, dict)):
                    value = cls.sanitize_json(json=value)
                _new_data[key] = value
            return _new_data

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


        Parameters
        ----------
        path: str
            The path to be sanitized.

        Raises
        ------
        :exc:`ValueError`
            If the path string contains a underscore.

        Returns
        -------
        :class:`str`
            Return the sanitized path string.

        """
        if "_" in path:
            raise ValueError("You cannot use '_' in path strings.")

        path = path.replace("//", "/")
        path = path.replace("\\", "/")
        path = path.replace("..", ".")

        # Remove starting periods as they are un-needed when being passed into an API
        path = path.removeprefix(".")

        # Remove starting slashes, all paths start relative to Instance root.
        path = path.removeprefix("/")

        return path

    @staticmethod
    def to_snake_case(data: str, /) -> str:
        """Quick function to return snake_case from camelCase.

        Parameters
        ----------
        data: :class:`str`
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

    async def version_validation(self, version: BuildInfo) -> None:
        """Compares the Version of the application/Instance against the version that is passed in.

        Parameters
        ----------
        version: :class:`VersionInfo`
            The version to compare against the application.

        Raises
        ------
        :exc:`RuntimeError`
            The application version no longer supports this API call..

        """
        result: Any = await self._call_api(
            api="Core/GetDiagnosticsInfo",
            format_data=True,
            format_=Diagnostics,
            _use_from_dict=False,
            _auto_unpack=True,
        )

        if isinstance(result, Diagnostics) and isinstance(result.application_version, BuildInfo):
            _version: BuildInfo = result.application_version
            if result.application_version < version:
                raise RuntimeError(self._version_unavailable, "`Core/GetWebserverMetrics`", _version)
        else:
            LOGGER.warning("Unable to validate version Info, the API call %s may raise an error", "`Core/GetDiagnosticsInfo`")

    def write_data_to_file(
        self,
        file_name: str,
        data: ResponseTypeAlias | str,
        path: Path = Path(__file__).parent,
        *,
        mode: str = "w+",
        **kwargs: Unpack[DumpParameters],
    ) -> None:
        """Basic file dump with json handling. If the data parameter is of type `dict`, `json.dumps()` will be used with an indent of 4.

        Parameters
        ----------
        path: :class:`Path`, optional
            The Path to write the data, default's to `Path(__file__).parent`.
        file_name: :class:`str`
            The name of the file, include the file extension.
        data: :class:`bytes | dict | str | list`
            The data to write out to the path and file_name provided.
        mode: :class:`str`, optional
            The mode to open the provided file path with using `<Path.open()>`.
        **kwargs: :class:`Unpack[DumpParameters]`
            Any additional kwargs to be supplied to `<json.dumps()>`, if applicable.

        """
        kwargs["indent"] = 4

        with path.joinpath(file_name).open(mode=mode) as file:
            LOGGER.debug("<%s.%s> | Wrote data to file %s located at: %s", __name__, "write_data_to_file", path, file_name)
            if isinstance(data, bytes):
                file.write(data.decode(encoding="utf-8"))
            elif isinstance(data, dict):
                file.write(json.dumps(data, **kwargs))
            elif isinstance(data, list):
                file.write("\n".join(data))
            else:
                file.write(data)
        LOGGER.info(
            "<%s.%s> | File write successful to path: %s ",
            __name__,
            "write_data_to_file",
            path.joinpath(file_name).as_posix(),
        )
