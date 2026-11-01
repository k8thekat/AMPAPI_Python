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
import keyword
import logging
import re
import time
from collections.abc import Callable
from dataclasses import fields
from json import JSONEncoder
from pathlib import Path

# from pprint import pformat
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Optional, ParamSpec, TypedDict, TypeGuard, Union, Unpack, overload

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


# These are the three passes of `Base.camel_to_snake_re`
_PLURAL_ACRONYM_PATTERN: re.Pattern[str] = re.compile(r"([A-Z]{2,})(s)(?=[^a-z]|$)")
_WORD_BOUNDARY_PATTERN: re.Pattern[str] = re.compile("(.)([A-Z][a-z]+)")
_LOWER_UPPER_PATTERN: re.Pattern[str] = re.compile("([a-z0-9])([A-Z])")


def _plural_acronym_repl(match: re.Match[str]) -> str:
    """Lower an acronym's trailing letters, eg. `IDs` -> `Ids`."""
    return match.group(1)[0] + match.group(1)[1:].lower() + match.group(2)


# This is bounded because some responses are keyed by player ID
@functools.lru_cache(maxsize=4096)
def _snake_key(key: str) -> str:
    """Convert one AMP response key to `snake_case`."""
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
    to_file : :class:`bool`
        ...
    path : :class:`pathlib.Path`
        ...
    check_key_drift : :class:`bool`
        Dev check, only with `to_file`: compare the capture with the TypedDict its endpoint narrows to.
    allow_null : :class:`bool`
        Return None when AMP answers JSON null, and raise otherwise.

    """

    # The endpoint methods check the sanitized key names, so only `_post` and `Core.get_api_spec` take `sanitize_json`
    # sanitize_json: bool
    to_file: bool
    path: pathlib.Path
    check_key_drift: bool
    allow_null: bool


class _SessionDeadError(AMPAPIResponseError):
    """Raised by :meth:`Base._response_handler` when AMP says the stored session does not exist.

    :meth:`Base._post` catches it once to log in again and resend. It is private. Anything that gets past
    :meth:`Base._post` is a plain :exc:`AMPAPIResponseError`.
    """

    def __init__(self, title: str, url: str, reason: str) -> None:
        self.title: str = title
        self.url: str = url
        self.reason: str = reason
        # We skip `AMPAPIResponseError`'s error log, as `_post` logs in again
        AMPAPIError.__init__(self, f"{title} | URL: {url} | Reason: {reason}")


class _TypedDictWriter:
    """Writes the :class:`TypedDict` classes for :meth:`Base.json_to_typeddict`."""

    def __init__(self, root_name: str) -> None:
        self.root_name: str = root_name
        self.class_bodies: dict[str, str] = {}
        # This is a `dict[str, V]` when a root key can't be a field
        self.root_alias: str | None = None

    def write_root(self, data: dict[str, Any]) -> None:
        # A root keyed by role IDs or setting names is written as a map
        # Each value is named after its own key
        for key in data:
            if self.is_field_name(key=key) is False:
                value_types: set[str] = set()
                for entry_key, entry_value in data.items():
                    value_types.add(self.infer_type(value=entry_value, key=entry_key, parent_name=self.root_name))

                self.root_alias = f"dict[str, {self.join_types(types=value_types)}]"
                return

        # Root goes last so its classes are above it
        self.class_bodies[self.root_name] = self.dict_body(class_name=self.root_name, data=data)

    def dict_body(self, class_name: str, data: dict[str, Any]) -> str:
        field_lines: list[str] = []
        for key, value in data.items():
            field_type = self.infer_type(value=value, key=key, parent_name=class_name)
            field_lines.append(f"    {key}: {field_type}")

        if len(field_lines) == 0:
            return "    ..."
        return "\n".join(field_lines)

    def infer_type(self, value: Any, key: str, parent_name: str) -> str:
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

        if self.is_dict(value):
            return self.infer_dict_type(entries=value, key=key, parent_name=parent_name)

        if self.is_list(value):
            return self.infer_list_type(items=value, key=key, parent_name=parent_name)
        return "Any"

    def infer_dict_type(self, entries: dict[str, Any], key: str, parent_name: str) -> str:
        if len(entries) == 0:
            return "dict[str, Any]"

        for entry_key in entries:
            if self.is_field_name(key=entry_key) is False:
                value_types: set[str] = set()
                for entry_value in entries.values():
                    value_types.add(self.infer_type(value=entry_value, key=key, parent_name=parent_name))
                return f"dict[str, {self.join_types(types=value_types)}]"

        class_name = self.pascal_case(key=key)
        body = self.dict_body(class_name=class_name, data=entries)
        return self.claim_name(candidate=class_name, parent_name=parent_name, body=body)

    def infer_list_type(self, items: list[Any], key: str, parent_name: str) -> str:
        if len(items) == 0:
            return "list[Any]"

        present = [item for item in items if item is not None]
        if len(present) == 0:
            return "list[None]"

        element_types: set[str] = set()
        dict_items = self.only_dicts(values=present)
        flattened = self.flatten_lists(values=present)
        if dict_items is not None:
            element_types.add(self.merged_dict_type(dicts=dict_items, key=key, parent_name=parent_name))
        elif flattened is not None:
            element_types.add(self.infer_list_type(items=flattened, key=key, parent_name=parent_name))
        else:
            for item in present:
                element_types.add(self.infer_type(value=item, key=key, parent_name=parent_name))

        if len(present) < len(items):
            element_types.add("None")
        return f"list[{self.join_types(types=element_types)}]"

    def merged_dict_type(self, dicts: list[dict[str, Any]], key: str, parent_name: str) -> str:
        for entries in dicts:
            if len(entries) > 0:
                return self.write_merged_class(class_name=self.pascal_case(key=key), items=dicts, parent_name=parent_name)
        return "dict[str, Any]"

    def write_merged_class(self, class_name: str, items: list[dict[str, Any]], parent_name: str) -> str:
        values_by_key: dict[str, list[Any]] = {}
        for item in items:
            for key, value in item.items():
                if key not in values_by_key:
                    values_by_key[key] = []
                values_by_key[key].append(value)

        field_lines: list[str] = []
        for key, values in values_by_key.items():
            field_lines.append(self.merged_field_line(class_name=class_name, key=key, values=values, item_count=len(items)))

        body = "\n".join(field_lines) if len(field_lines) > 0 else "    ..."
        return self.claim_name(candidate=class_name, parent_name=parent_name, body=body)

    def merged_field_line(self, class_name: str, key: str, values: list[Any], item_count: int) -> str:
        present = [value for value in values if value is not None]
        field_types: set[str] = set()
        # Flatten the lists across items so we don't get `list[Any] | list[X]`
        # Merge the dicts across items into one class
        flattened = self.flatten_lists(values=present)
        dict_values = self.only_dicts(values=present)

        if len(present) == 0:
            field_types.add("None")
        elif flattened is not None:
            field_types.add(self.infer_list_type(items=flattened, key=key, parent_name=class_name))
        elif dict_values is not None:
            field_types.add(self.merged_dict_type(dicts=dict_values, key=key, parent_name=class_name))
        else:
            for value in present:
                field_types.add(self.infer_type(value=value, key=key, parent_name=class_name))

        # An explicit `None` makes it optional, and a key some items lack makes it `NotRequired`
        if len(present) < len(values):
            field_types.add("None")
        field_type = self.join_types(types=field_types)

        if len(values) < item_count:
            field_type = f"NotRequired[{field_type}]"
        return f"    {key}: {field_type}"

    def claim_name(self, candidate: str, parent_name: str, body: str) -> str:
        """Store a class body under the first free name and return that name."""
        name = candidate
        if self.is_taken(name=name, body=body):
            name = f"{parent_name}{candidate}"

        base_name = name
        number = 2
        while self.is_taken(name=name, body=body):
            name = f"{base_name}{number}"
            number += 1

        self.class_bodies[name] = body
        return name

    def is_taken(self, name: str, body: str) -> bool:
        if name == self.root_name:
            return True
        return name in self.class_bodies and self.class_bodies[name] != body

    def join_types(self, types: set[str]) -> str:
        names = sorted(name for name in types if name != "None")
        if len(names) == 0:
            return "None" if "None" in types else "Any"

        # Empty lists and dicts only say `Any` if nothing else gave a type
        for placeholder, prefix in (("dict[str, Any]", "dict["), ("list[Any]", "list[")):
            specific = [name for name in names if name.startswith(prefix) and name != placeholder]
            if placeholder in names and len(specific) > 0:
                names.remove(placeholder)

        if "None" in types:
            names.append("None")
        return " | ".join(names)

    # These give pyright the JSON shapes
    @staticmethod
    def is_dict(value: Any) -> TypeGuard[dict[str, Any]]:
        return isinstance(value, dict)

    @staticmethod
    def is_list(value: Any) -> TypeGuard[list[Any]]:
        return isinstance(value, list)

    @staticmethod
    def is_field_name(key: str) -> bool:
        # `isidentifier()` is True for keywords too, but `from: str` is a SyntaxError
        return key.isidentifier() is True and keyword.iskeyword(key) is False

    @staticmethod
    def pascal_case(key: str) -> str:
        # Characters that can't go in a name split the key, so `et_legacy:stadia controller` is `EtLegacyStadiaController`
        class_name = "".join(part.title() for part in re.split(r"[\W_]+", key))
        if class_name.isidentifier() is False:
            return f"Key{class_name}"
        return class_name

    def only_dicts(self, values: list[Any]) -> list[dict[str, Any]] | None:
        """The values as a list of dicts, or `None` unless every value is a dict whose keys can all be fields."""
        dicts = [value for value in values if self.is_dict(value)]
        if len(dicts) < len(values):
            return None

        for entries in dicts:
            for entry_key in entries:
                if self.is_field_name(key=entry_key) is False:
                    return None
        return dicts

    def flatten_lists(self, values: list[Any]) -> list[Any] | None:
        """Every list in `values` joined into one list, or `None` unless every value is a list."""
        flattened: list[Any] = []
        list_count = 0
        for value in values:
            if self.is_list(value):
                flattened.extend(value)
                list_count += 1

        if list_count < len(values) or list_count == 0:
            return None
        return flattened

    def render(self, *, include_imports: bool) -> str:
        blocks: list[str] = []
        imports = self.imports()
        if include_imports is True and len(imports) > 0:
            blocks.append(imports)

        for class_name, body in self.class_bodies.items():
            blocks.append(f"class {class_name}(TypedDict):\n{body}")

        if self.root_alias is not None:
            blocks.append(f"{self.root_name} = {self.root_alias}")
        return "\n\n\n".join(blocks) + "\n"

    def imports(self) -> str:
        # A root map of plain values, like `dict[str, str]`, needs no import
        typing_extensions_names: list[str] = []
        if self.uses_name(name="NotRequired") is True:
            typing_extensions_names.append("NotRequired")
        if len(self.class_bodies) > 0:
            typing_extensions_names.append("TypedDict")

        import_lines: list[str] = []
        if self.uses_name(name="Any") is True:
            import_lines.append("from typing import Any")
        if len(typing_extensions_names) > 0:
            import_lines.append(f"from typing_extensions import {', '.join(typing_extensions_names)}")
        return "\n\n".join(import_lines)

    def uses_name(self, name: str) -> bool:
        pattern = re.compile(rf"\b{name}\b")
        if self.root_alias is not None and pattern.search(self.root_alias) is not None:
            return True

        for body in self.class_bodies.values():
            for field_line in body.splitlines():
                # We only check the annotation
                if pattern.search(field_line.split(": ", 1)[-1]) is not None:
                    return True
        return False


class Base:
    """Contains the base functions for all AMP API endpoints and handles the parsing of Bridge data.

    .. warning::
        Do not overwrite or alter the :attr:`instance_id`.


    .. note::
        A session expires after 240sec of inactivity per Cube Coders AMP.
        If for any reason you want to change that value, set the attribute :attr:`session_ttl`.\n


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
    # Other calls wait on this while a login runs, and it only exists during a login
    _login_pending: Union[asyncio.Future[None], None]

    # This is the cache state for attributes filled from an API response instead of __init__
    # `_is_cached` is set once data is applied and `_cached_at` is when
    _is_cached: bool = False
    _cached_at: Optional[datetime.datetime] = None
    # This is a monotonic copy of `_cached_at`, which is cheaper to check on every attribute access
    _cached_monotonic: Optional[float] = None
    _cache_timeout: ClassVar[int] = 300
    # These are named in the cache messages, and `_cache_sources` overrides `_cache_source` per attribute
    _cache_source: ClassVar[str] = "the API call that populates it"
    _cache_sources: ClassVar[dict[str, str]] = {}
    # This is built on the first `check_key_drift` call and shared by every instance
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
    _login_failed: ClassVar[str] = "Failed to login to AMP as '%s' (AMP result %s). Check the user, password and 2FA token."
    # These are the login result codes, and any other code is reported as its number
    _login_result_names: ClassVar[dict[int, str]] = {0: "Failure", 5: "NoInstanceAccess", 100: "PassthruDisabled"}
    _no_cache: ClassVar[str] = "'%s.%s' has not been populated yet. You must call <%s>.%s first."
    _stale_cache: ClassVar[str] = (
        "'%s.%s' was cached %s seconds ago and the timeout is %s seconds. The value may be stale. Call <%s>.%s to refresh it."
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
        sanitize_json: bool = True,
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
        sanitize_json: bool = True,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ResponseTypeAlias | str | bool | None: ...

    async def _post(
        self,
        url: str,
        parameters: Union[dict[str, Any], None] = None,
        *,
        no_data: bool = False,
        request_params: Optional[AioHTTPRequestOptions] = None,
        sanitize_json: bool = True,
        **response_params: Unpack[ResponseHandlerOptions],
    ) -> ResponseTypeAlias | str | bool | None:
        """|coro|

        Makes a POST request via :class:`aiohttp.ClientSession` and passes the response to :meth:`_response_handler`.

        .. warning::
            Will raise :exc:`AMPAPINetworkError` or :exc:`AMPAPIResponseError` if any errors occur when attempting to call the API.

        .. note::
            When AMP says the stored session does not exist, this logs in again and sends the request once more.
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

        sanitize_json : :class:`bool`, optional
            Run the parsed JSON through :meth:`sanitize_json`, by default True.
            The endpoint methods need the sanitized keys, so only the dev tools turn it off.
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
        # We copy it because we fill in the headers and data below
        request_params = request_params.copy()

        # Only headers we build follow a new login, so the caller's are kept
        library_headers: bool = "headers" not in request_params

        # A dead session gets one login and one resend per call
        # TODO: The RuntimeError retry below has no limit
        session_retried: bool = False
        # This counts the retries for the log line
        runtime_retries: int = 0

        while True:
            api_session: APISession = self._bridge._sessions.get(  # pyright: ignore[reportPrivateUsage]
                self._instance_id,
                APISession(id="0", ttl=datetime.datetime.now(tz=datetime.UTC)),
            )
            if self.session is None:
                self.session = aiohttp.ClientSession()

            # request_params.setdefault("headers", {"Accept": "text/javascript", "Authorization": f"Bearer {api_session.id}"})
            # Rebuilt every pass so a resend carries the new session ID
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
                # Backoff can return 0, so we wait at least 1 second
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
                # This does the same as the old recursive call
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
                            # A Void endpoint answers JSON null, but a failure still comes back in the body with a 200
                            response_params["allow_null"] = True
                            await self._response_handler(response=response, sanitize_json=sanitize_json, **response_params)
                            return None
                        return await self._response_handler(response=response, sanitize_json=sanitize_json, **response_params)

                    except _SessionDeadError as dead_session:
                        # A second dead answer, or one to the login itself, is a real failure
                        if session_retried is True or url == "Core/Login":
                            raise AMPAPIResponseError(
                                title=dead_session.title,
                                url=dead_session.url,
                                reason=dead_session.reason,
                            ) from dead_session

                        # Only reset if the stored session is the one we sent
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
            The error checks always read a sanitized copy.
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

        # if sanitize_json is True:
        #     response_json = self.sanitize_json(response_json)
        # The error checks below read the sanitized key names, so raw JSON is kept apart for the caller
        result_json = response_json
        response_json = self.sanitize_json(response_json)
        if sanitize_json is True:
            result_json = response_json

        # None was already returned or raised above
        # if to_file is True and path is not None and response_json is not None:
        if to_file is True and path is not None:
            # ? SUGGESTION: May have to make this async in the future if it becomes blocking.
            if path.exists() is False:
                msg = "The path provided does not exist. %s"
                raise FileNotFoundError(msg, path)
            # self.write_data_to_file(file_name=response.url.name.lower() + ".json", data=response_json, path=path)
            self.write_data_to_file(file_name=response.url.name.lower() + ".json", data=result_json, path=path)

        # A bool has no title or status
        if isinstance(response_json, bool):
            return response_json

        # This is the logic gate for when we have an "EndpointResponseError" typically.
        if isinstance(response_json, dict) and "title" in response_json:
            title: str = response_json.get("title")

            # Missing `Session.Exists` means a dead session
            # The call never ran, so `_post` logs in again and resends it
            if title == "Unauthorized Access" and "Session.Exists" in str(response_json.get("message", "")):
                LOGGER.warning(
                    "<%s.%s> | AMP does not know the stored session. | URL: %s",
                    __class__.__name__,
                    "_response_handler",
                    response.url,
                )
                # self._reset_session()
                # `_post` resets the session
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

        # A failed ActionResult, eg. RegisterTargetWithCode against a Controller with no ADS mode set
        # AMP puts the cause in `reason`
        if isinstance(response_json, dict) and "status" in response_json and response_json["status"] is False:
            reason: str = str(response_json.get("reason") or "Status is False")

            # An `ActionResult` endpoint answers a dead session here instead of with a title
            # The call never ran, so `_post` logs in again and resends it like the title form above
            if "Session.Exists" in reason:
                LOGGER.warning(
                    "<%s.%s> | AMP does not know the stored session. | URL: %s",
                    __class__.__name__,
                    "_response_handler",
                    response.url,
                )
                raise _SessionDeadError(title="Unauthorized Access", url=str(response.url), reason=reason)

            LOGGER.error("%s failed because of Status: %s | Reason: %s", response.url, response_json["status"], reason)
            raise AMPAPIResponseError(title="Status False", url=str(response.url), reason=reason)

        # Errors were already raised, so we only compare good captures
        if check_key_drift is True and to_file is True and path is not None:
            self._check_key_drift(response=response, data=result_json, path=path, sanitized=sanitize_json)

        # return response_json
        # An error answer was raised above from the sanitized copy, which pyright can't follow to the raw one
        return result_json  # pyright: ignore[reportReturnType]

    def _check_key_drift(self, response: ClientResponse, data: object, path: pathlib.Path, *, sanitized: bool) -> None:
        """Dev check: compare a captured response with the TypedDict its endpoint narrows to.

        On drift, logs a warning and writes ``<endpoint>.key_drift.json`` beside the capture.
        See :class:`~ampapi.key_drift.KeyDriftCheck` for how an endpoint's TypedDict is found.

        Parameters
        ----------
        response : :class:`aiohttp.ClientResponse`
            The response the capture came from. Its URL names the endpoint.
        data : :class:`object`
            The captured JSON response.
        path : :class:`pathlib.Path`
            The directory the capture was written to.
        sanitized : :class:`bool`
            If the JSON was sanitized or not. The TypedDicts use the sanitized `snake_case` keys.

        """
        # The endpoint is at the end, after any ADSModule/Servers/<id>/ prefix
        match = re.search(r"API/([A-Za-z]+/[A-Za-z0-9]+)$", response.url.path)
        if match is None:
            return

        endpoint: str = match.group(1)
        if sanitized is False:
            LOGGER.warning("<%s.%s> | Skipped %s as the TypedDicts use sanitized keys.", __class__.__name__, "_check_key_drift", endpoint)
            return

        if Base._key_drift_check is None:
            Base._key_drift_check = KeyDriftCheck()

        found = Base._key_drift_check.check(endpoint=endpoint, data=data)
        if found is None:
            LOGGER.debug("<%s.%s> | No TypedDict known for %s.", __class__.__name__, "_check_key_drift", endpoint)
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
        # Wait on a login already running, then check the stored session again
        # If that login failed there is still no session, so we try our own
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
            # There is no `await` since the check above, and other calls wait on this until the login is done
            pending: asyncio.Future[None] = asyncio.get_running_loop().create_future()
            self._login_pending = pending
            try:
                if self._bridge.use_2fa is True:
                    try:
                        # Handles time based 2Factory Auth Key/Code
                        code = TOTP(self._bridge.token).now()

                    # pyotp raises binascii.Error (a ValueError) for a bad base32 token
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

                # Network and response errors raise straight through, and their URL names Core/Login
                # We post directly because `_call_end_point` would log in again
                result = await self._post(url="Core/Login", parameters=parameters)
                if not isinstance(result, dict) or "remember_me_token" not in result or result["success"] is not True:
                    # AMP sends no reason, and a wrong password and a wrong 2FA code both give `result: 40`
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
            # Waiters get None, and only the caller that logged in sees the error
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
            Returns False when nothing is cached yet. Check :attr:`_is_cached` to tell the two apart.


        Returns
        -------
        :class:`bool`
            True when the data is stale.

        """
        age: Optional[float] = self.cache_age
        return age is not None and age > self._cache_timeout

    @classmethod
    def _cache_hint(cls, name: str) -> str:
        """Get the call that populates a cached attribute."""
        return cls._cache_sources.get(name, cls._cache_source)

    def _mark_cached(self) -> None:
        """Mark this class as holding fresh API data."""
        self._is_cached = True
        self._cached_at = datetime.datetime.now(tz=datetime.UTC)
        self._cached_monotonic = time.monotonic()

    async def clean_up(self, *, logout: bool = False) -> None:
        """|coro|

        Close any open :class:`aiohttp.ClientSession` belonging to this class.

        .. note::
            Safe to call more than once, since the session is cleared once closed.

        .. versionchanged:: 5.0.0
            `logout` also resets the stored session and skips `Core/Logout` if there is no session.

        Parameters
        ----------
        logout : :class:`bool`, optional
            If to call `Core/Logout` first or not, by default False.
            A failed logout is logged as a warning and the session is still closed.

        """
        stored: Union[APISession, None] = self._bridge._sessions.get(self._instance_id)  # pyright: ignore[reportPrivateUsage]
        # There is no session to end, so we skip the logout
        if logout is True and (stored is None or stored.id == "0"):
            LOGGER.debug("<%s.%s> | No stored session, skipping `Core/Logout`", __class__.__name__, "clean_up")
        elif logout is True:
            try:
                await self._post(url="Core/Logout", no_data=True)
            except Exception:
                LOGGER.warning("<%s.%s> | `Core/Logout` failed, closing the session anyway", __class__.__name__, "clean_up", exc_info=True)
            # Reset the stored session either way
            self._reset_session()

        LOGGER.debug("<%s.%s> | Closing any open `aiohttp.ClientSession`", __class__.__name__, "clean_up")
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def __aenter__(self) -> Self:
        """|coro|

        Enter the async context manager.

        .. note::
            Nothing is opened here. The :class:`aiohttp.ClientSession` is created on the first
            request. This makes sure the session is closed on the way out.


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
            Exceptions are not suppressed, so any error propagates.


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

        Generic function for calling any API endpoint, a dev tool for testing endpoints with no wrapper yet.
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

        When a name is used by a class with a different body, the parent class's name goes in
        front of it (`SecondInfo`), then a number if that is taken too (`SecondInfo2`). A class with an
        identical body is reused.

        A list of dicts produces one merged class. A key missing from some of the dicts is
        ``NotRequired[X]``, a key that is `None` in some of them is ``X | None``, and a key that is both is
        ``NotRequired[X | None]``. Mixed types are a sorted union (``int | str``), and `Any` is only used when
        there is nothing to infer, such as an empty list or dict. A dict with a key that can't be a field, because
        it is not a valid Python identifier (e.g. ``{"0": "Equals", "1": "NotEquals"}``) or is a keyword such as
        `from`, is emitted as ``dict[str, V]``, not a :class:`TypedDict`. That includes the root, which is
        then written as ``Name = dict[str, V]``, as for the role IDs of `get_role_ids`.

        The returned string starts with the first class, or with the imports, and can be printed or written
        directly to a ``.py`` file.

        .. versionadded:: 5.0.0

        Parameters
        ----------
        name : :class:`str`
            The class name for the root :class:`TypedDict`.
        data : dict[:class:`str`, Any]
            The JSON dict whose keys and values define the fields and their types.
        include_imports : :class:`bool`, optional
            To put the imports the classes use at the top of the output, by default False.
            `Any` is only imported when a class uses it, and `NotRequired` likewise.

        Returns
        -------
        :class:`str`
            Python source code containing one or more :class:`TypedDict` class definitions,
            preceded by the imports when `include_imports` is True.

        """
        # class_defs: list[str] = []
        # seen: set[str] = set()
        #
        # def _infer(value: Any, key: str) -> str:
        #     if value is None:
        #         return "None"
        #     if isinstance(value, bool):
        #         return "bool"
        #     if isinstance(value, int):
        #         return "int"
        #     if isinstance(value, float):
        #         return "float"
        #     if isinstance(value, str):
        #         return "str"
        #     if isinstance(value, dict):
        #         if not all(k.isidentifier() for k in value):
        #             val_types = {_infer(v, key) for v in value.values()} if value else {"Any"}
        #             val_type = next(iter(val_types)) if len(val_types) == 1 else "Any"
        #             return f"dict[str, {val_type}]"
        #         child_name = "".join(part.title() for part in key.split("_"))
        #         _build(child_name, value)
        #         return child_name
        #     if isinstance(value, list):
        #         return _infer_list(value, key)
        #     return "Any"
        #
        # def _infer_list(items: list[Any], key: str) -> str:
        #     if not items:
        #         return "list[Any]"
        #     non_none = [v for v in items if v is not None]
        #     if not non_none:
        #         return "list[None]"
        #     has_none = len(non_none) < len(items)
        #     if all(isinstance(v, dict) for v in non_none):
        #         child_name = "".join(part.title() for part in key.split("_"))
        #         _build_merged(child_name, non_none)
        #         elem = child_name
        #     else:
        #         elem_types = {_infer(v, key) for v in non_none}
        #         elem = next(iter(elem_types)) if len(elem_types) == 1 else "Any"
        #     if has_none:
        #         elem = f"{elem} | None"
        #     return f"list[{elem}]"
        #
        # def _build_merged(cls_name: str, items: list[dict[str, Any]]) -> None:
        #     if cls_name in seen:
        #         return
        #     seen.add(cls_name)
        #     key_values: dict[str, list[Any]] = {}
        #     for item in items:
        #         for k, v in item.items():
        #             key_values.setdefault(k, []).append(v)
        #     field_lines: list[str] = []
        #     for k, values in key_values.items():
        #         non_none = [v for v in values if v is not None]
        #         has_none = len(non_none) < len(items)
        #         if not non_none:
        #             type_str = "None"
        #         elif all(isinstance(v, list) for v in non_none):
        #             # Flatten all list values to infer a single unified element type,
        #             # so mixed empty/non-empty lists don't produce list[Any] | list[X].
        #             combined: list[Any] = [elem for v in non_none for elem in v]
        #             type_str = _infer_list(combined, k)
        #             if has_none:
        #                 type_str = f"{type_str} | None"
        #         else:
        #             types: set[str] = {_infer(v, k) for v in non_none}
        #             type_str = next(iter(types)) if len(types) == 1 else " | ".join(sorted(types))
        #             if has_none:
        #                 type_str = f"{type_str} | None"
        #         field_lines.append(f"    {k}: {type_str}")
        #     body = "\n".join(field_lines) if field_lines else "    ..."
        #     class_defs.append(f"class {cls_name}(TypedDict):\n{body}")
        #
        # def _build(cls_name: str, fields: Any | dict[str, Any]) -> None:
        #     if cls_name in seen:
        #         return
        #     seen.add(cls_name)
        #     field_lines = [f"    {k}: {_infer(v, k)}" for k, v in fields.items()]
        #     body = "\n".join(field_lines) if field_lines else "    ..."
        #     class_defs.append(f"class {cls_name}(TypedDict):\n{body}")
        #
        # _build(name, data)
        # imports = "from typing import Any\n\nfrom typing_extensions import TypedDict\n" if include_imports is True else ""
        # return imports + "\n\n\n" + "\n\n\n".join(class_defs)
        writer = _TypedDictWriter(root_name=name)
        writer.write_root(data=data)
        return writer.render(include_imports=include_imports)

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

    @overload
    @classmethod
    def sanitize_json(cls, json: str) -> str: ...

    @overload
    @classmethod
    def sanitize_json[JsonT](cls, json: JsonT) -> JsonT: ...

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
            # This is a typed local for pyright
            source_list: list[Any] = json  # pyright: ignore[reportUnknownVariableType]

            # entries: list[Any] = copy.copy(x=source_list)
            # for index, entry in enumerate(source_list):
            #     # If any of our entries are a dictionary; let's go through them.
            #     if isinstance(entry, dict):
            #         entries[index] = cls.sanitize_json(json=entry)
            # return entries

            # Only dicts get sanitized, and the rest is kept
            # return [cls.sanitize_json(json=entry) if isinstance(entry, dict) else entry for entry in source_list]
            cleaned_list: list[Any] = []
            for entry in source_list:
                if isinstance(entry, dict):
                    entry_map: dict[str, Any] = entry  # pyright: ignore[reportUnknownVariableType]
                    cleaned_list.append(cls.sanitize_json(json=entry_map))
                else:
                    cleaned_list.append(entry)
            return cleaned_list

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

            # We build a fresh dict, and the key conversion is cached
            new_map: dict[str, Any] = {}
            for old_key, old_value in source_map.items():
                # new_value: Any = cls.sanitize_json(json=old_value) if isinstance(old_value, (list, dict)) else old_value
                new_value: Any = old_value
                if isinstance(old_value, (list, dict)):
                    nested: Any = old_value  # pyright: ignore[reportUnknownVariableType]
                    new_value = cls.sanitize_json(json=nested)

                # AMP setting nodes are dotted, so we keep those keys as sent
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
            Only leading slashes are dropped. `_`, `..` and a leading `.` are left as given.


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
            If the AMP version is `version` or newer.

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

        # to_dataclass returns a str if it can't parse, so we skip the check
        _version: BuildInfo | str = BuildInfo.to_dataclass(data=result["application_version"])
        if isinstance(_version, str):
            LOGGER.warning(
                "Unable to parse the application version %r from %s, skipping the version check.",
                _version,
                "`Core/GetDiagnosticsInfo`",
            )
            return

        # The endpoint only exists before the removal version
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
