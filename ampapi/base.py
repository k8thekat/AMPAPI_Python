from __future__ import annotations

import copy
import functools
import json
import logging
import re
from dataclasses import fields, is_dataclass
from datetime import datetime
from pprint import pformat
from typing import TYPE_CHECKING, Any, ClassVar, Union, overload

import aiohttp
from aiohttp import ClientResponse
from dataclass_wizard import fromdict
from pyotp import TOTP

from .bridge import Bridge
from .dataclass import APISession, Diagnostics, LoginResults, VersionInfo

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine, Iterable
    from datetime import timedelta
    from typing import Concatenate

    from _typeshed import DataclassInstance
    from typing_extensions import ParamSpec, Self, TypeVar

    from .dataclass import Controller, Instance, InstanceStatus, Updates
    from .modules import APIResponseDataTableAlias

    D = TypeVar("D", bound="Base")
    T = ParamSpec("T")
    F = TypeVar("F")
    X = TypeVar("X", bound=DataclassInstance)

__all__ = ("Base",)

FORMAT_DATA: bool = True


class Base:
    """
    Contains the base functions for all AMP API endpoints and handles the parsing of Bridge data.


    .. warning::
        Do not overwrite or alter the :attr:`instance_id`.


    .. note::
        A session expires after 240sec of inactivity per Cube Coders AMP. If for any reason you want to change that value; set the attribute :attr:`session_ttl`.\n


    Attributes
    -----------
    api_url: :class:`str`
        The URL to access the Web Panel. This comes from your :class:`APIParams`.
    session_ttl: :class:`int`
        How long before the session id expires in seconds, default is 240 seconds.
    instance_id: :class:`str`
        The Instance id is a string determined by AMP. \n
        This attribute will be set automatically after making a :meth:`login` request, default is "O".

    """

    # Private Attributes
    logger: logging.Logger = logging.getLogger()
    _bridge: Bridge

    # Public Attributes
    url: str = ""
    instance_id: str = "0"
    session_ttl: int = 240
    module: str  # TODO - make this var unchangeable via private attr in future release.

    # Error response strings.
    _ads_only: str = "This API call is only available to <class:`ADSModule`> type classes."
    _failed_api: str = "The API call returned a malformed response."
    _minecraft_only: str = "This API call is only available on Minecraft type instances."
    _no_bridge: str = "Failed to setup connection. You need to initiate `<class Bridge>` first."
    _no_controller: str = "The function failed as the <class:`AMPControllerInstance`> was not properly initialized and set."
    _no_data: str = "Failed to receive any data from post request."
    _unauthorized_access: str = "The user does not have the required permissions to interact with this instance."
    _instance_offline: str = "The requested Instance is not available at this time. | URL: %s"
    _version_unavailable: str = "The API call %s is no longer available at this version of AMP %s"

    # These are used to handle JSON keys that cannot be parsed properly via regex.
    # See :func:`camel_to_snake_re`
    json_key_mapping: ClassVar[dict[str, str]] = {
        "ContainerCPUs": "container_cpus",
        "InstalledRAMMB": "installed_ram_mb",
        "FreeRAMMB": "free_ram_mb",
        "AvailableIPs": "available_ips",
        "SecurityandPrivacy": "security_and_privacy",
    }

    def __init__(self) -> None:
        bridge: Bridge = Bridge._get_bridge()
        # Validate the bridge object is at the same memory address.
        self.logger.debug("DEBUG %s __init__ %s", type(self).__name__, id(self))
        self.logger.debug("bridge object -> %s", pformat(bridge))

        if isinstance(bridge, Bridge):
            self.parse_bridge(bridge=bridge)

    @property
    def format_data(self) -> bool:
        """
        Controls whether the data returned from an API endpoint is formatted or not.\n
        Default is ``True`` which comes from the global parameter ``FORMAT_DATA``.

        .. note::
            ``True`` = formatted \n
            ``False`` = unformatted


        Returns
        --------
        :class:`bool`
            Returns True or False.
        """
        global FORMAT_DATA
        return FORMAT_DATA

    @format_data.setter
    def format_data(self, value: bool) -> None:
        global FORMAT_DATA
        FORMAT_DATA = value

    @staticmethod
    def ads_only(
        func: Callable[Concatenate[D, T], Coroutine[None, None, F]],
    ) -> Callable[Concatenate[D, T], Coroutine[None, None, F]]:
        """
        Checks the class attribute ``.module`` and is equal to ``ADS`` or if the type of Instance using the function is AMPADSInstance.

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
            from .adsmodule import ADSModule
            from .instance import AMPADSInstance

            if self.module == "ADS" or type(self) is AMPADSInstance or isinstance(self, ADSModule):
                return func(self, *args, **kwargs)
            else:
                raise RuntimeError(self._ads_only)

        return wrapper_ads_only

    async def _call_api(
        self,
        api: str,
        parameters: Union[None, dict[str, Any]] = None,
        format_data: Union[bool, None] = None,
        format_: Union[type[X], type[APIResponseDataTableAlias], None] = None,
        sanitize_json: bool = True,
        _use_from_dict: bool = True,
        _auto_unpack: bool = True,
        _no_data: bool = False,
    ) -> Any:
        """|coro|
        Uses :class:`aiohttp.ClientSession` post request to access the AMP API endpoints. \n

        .. note::
            Will populate the ``SESSIONID`` key for :param:`parameters` if it is not provided. This is the default behavior.


        Parameters
        -----------
        api: :class:`str`
            The API endpoint to call, eg ``Core/GetModuleInfo``.
        parameters: Union[None, dict[:class:`str`, Any]], optional
            The parameters to pass to the API endpoint, by default None.
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data. (Uses ``FORMAT_DATA`` global constant if None), by default None.
        format_: :py:class:`DataclassInstance`, optional
            The dataclass the JSON response will formatted to, by default None.
        sanitize_json: :class:`bool`, optional
            Replaces invalid characters in our JSON responses, by default True.
        _use_from_dict: :class:`bool`, optional
            Controls whether the data will use :meth:`fromdict` of dataclass wizard to unpack the data. Typical usage case is to handle nested :class:`DataclassInstance`, by default True.
        _auto_unpack: :class:`bool`, optional
            Controls whether the data will be unpacked automatically via ``(**data)``, by default True.
        _no_data: :class:`bool`, optional
            Informs the connection that the API does not have a JSON response, by default False.

        Returns
        --------
        Any
            Typical returns are of the same type that is passed in to ``format_``, either in an :class:`Iterable` or not depending on the data,
            otherwise returns an unformatted JSON response if :attr:`format_data` or ``FORMAT_DATA`` is False.

        Raises
        ------
        :exc:`ValueError`
            When a JSON response :attr:`ClientSession.content_length` == 0 or :class:`aiohttp.ClientSession` raises an Exception.\n
            When the API endpoint returns a malformed JSON response.
        :exc:`ConnectionError`
            When an JSON response status code is not 200.\n
            When an JSON response has a dict key value of "Instance Unavailable.
        :exc:`PermissionError`
            When the JSON response has a dict key value of "Unauthorized Access" or permission related error.
        """

        global FORMAT_DATA

        header: dict = {"Accept": "text/javascript"}
        post_req: ClientResponse | None
        self.logger.debug("_call_api -> %s was called with %s", api, parameters)

        # This should save us some boiler plate code throughout our API calls.
        if parameters is None:
            parameters = {}

        api_session: APISession = self._bridge._sessions.get(self.instance_id, APISession(id="0", ttl=datetime.now()))
        if isinstance(api_session, APISession):
            parameters["SESSIONID"] = api_session.id

        json_data: str = json.dumps(obj=parameters)

        _url: str = self.url + "/API/" + api
        self.logger.debug("DEBUG %s | %s | %s | %s", self.instance_id, api, _url, pformat(json_data))
        async with aiohttp.ClientSession() as session:
            try:
                post_req = await session.post(url=_url, headers=header, data=json_data)
            # TODO - Need to not catch all Excepts..
            # So I can handle each exception properly.
            except Exception as e:
                self.logger.error("DEBUG _call_api exception type: %s", type(e))
                raise ValueError(e)

            if post_req.content_length == 0:
                raise ValueError(self._no_data)

            if post_req.status != 200:
                raise ConnectionError(self._no_data)

            post_req_json: Any = await post_req.json()

        if post_req_json is None and _no_data is False:
            raise ConnectionError(self._no_data)

        # They removed "result" from all replies thus breaking most if not all future code.
        # This was an old example from pre 2.3 AMP API that could have the following return:
        # `{'resultReason': 'Internal Auth - No reason given', 'success': False, 'result': 0}`
        self.logger.debug("DEBUG API CALL----> %s | %s | %s", api, type(post_req_json), parameters)
        self.logger.debug("DEBUG %s", pformat(post_req_json))
        if sanitize_json is True:
            post_req_json = self.sanitize_json(post_req_json)
        if isinstance(post_req_json, dict):
            if "title" in post_req_json:
                post_req_json = post_req_json["title"]
                if isinstance(post_req_json, str) and (
                    post_req_json == "Unauthorized Access" or post_req_json == "Instance Unavailable"
                ):
                    self.logger.error("%s failed because of %s", api, post_req_json)
                    api_session = APISession(id="0", ttl=datetime.now())
                    self._bridge._sessions.update({self.instance_id: api_session})
                    if post_req_json == "Unauthorized Access":
                        raise PermissionError(self._unauthorized_access)
                    elif post_req_json == "Instance Unavailable":
                        raise ConnectionError(self._instance_offline, self.url)

            elif api == "Core/Login":
                return LoginResults(**post_req_json)

            elif "result" in post_req_json:
                post_req_json = post_req_json["result"]

                if isinstance(post_req_json, bool) and post_req_json is False:
                    self.logger.error("%s failed because of %s", api, post_req_json)
                    raise ValueError(self._failed_api)

            elif isinstance(post_req_json, dict) and "status" in post_req_json and post_req_json["status"] is False:
                self.logger.error("%s failed because of Status: %s", api, post_req_json)
                return ValueError(self._failed_api)

        self.logger.debug(
            "DEBUG _call_api | format_data = %s | FORMAT_DATA = %s | FORMAT-> %s", format_data, FORMAT_DATA, format_
        )
        if (format_ is None or format_data is False) or (format_data is None and FORMAT_DATA is False):
            return post_req_json

        elif isinstance(post_req_json, (dict, list)) and (
            (format_data is True) or (format_data is None and FORMAT_DATA is True)
        ):
            return self.json_to_dataclass(
                json=post_req_json, format_=format_, _use_from_dict=_use_from_dict, _auto_unpack=_auto_unpack
            )

    async def _connect(self) -> LoginResults | None:
        """|coro|
        Logs into AMP via "API/Core/Login" endpoint using your :class:`Bridge` object.

        .. note::
            If Applicable handles your 2FA using :class:`TOTP` \n
            Stores the ``SESSIONID`` via :class:`APISession` dataclass for future usage inside the :class:`Bridge` object.


        Returns
        --------
        :class:`LoginResults` | None
            The results from ``API/Core/Login`` as a dataclass.

        Raises
        -------
        :exc:`ValueError`
            If the 2 Factor Authentication code is not a formatted properly aka the :attr:`~Bridge.token` when making the :py:class:`Bridge` object.
        """
        code: Union[str, TOTP] = ""

        # get our InstanceID and use it to key for session_id
        session: APISession = self._bridge._sessions.get(self.instance_id, APISession(id="0", ttl=datetime.now()))
        if isinstance(session, APISession):
            ttl: timedelta = datetime.now() - session.ttl
            if ttl.seconds > self.session_ttl:
                sessionID = "0"
            else:
                sessionID: str = session.id

        if sessionID == "0":
            if self._bridge.use_2fa is True:
                try:
                    # Handles time based 2Factory Auth Key/Code
                    code = TOTP(self._bridge.token).now()

                except AttributeError:
                    raise ValueError(
                        "Please check your 2 Factor Code, should not contain spaces, escape characters and it must be enclosed in quotes!"
                    )
            else:
                try:
                    parameters: dict[str, Any] = {
                        "username": self._bridge.user,
                        "password": self._bridge.password,
                        "token": code,
                        "rememberMe": True,
                    }

                    result: Any = await self._call_api(
                        api="Core/Login", parameters=parameters, format_data=True, format_=LoginResults
                    )
                    if isinstance(result, LoginResults):
                        # This is our new sessions table to correlate InstanceID to a sessionID.
                        api_session = APISession(id=result.session_id, ttl=datetime.now())
                        self._bridge._sessions.update({self.instance_id: api_session})
                        return result

                    else:
                        self.logger.warning(msg="Failed response from 'API/Core/Login' in <Base>._connect()")
                        return result

                except Exception as e:
                    self.logger.warning("Core/Login Exception:", exc_info=e)
        else:
            return

    async def call_end_point(self, api: str, parameters: None | dict[str, Any] = None) -> dict[str, Any]:
        """|coro|

        Universal API function for calling any API endpoint. Some API endpoints require the Instance module type to be ADS. \n
        See `/api_spec_sheets/ADS_api_spec.md` or `/api_spec_sheets/Minecraft_api_spec.md` for full API endpoints and parameter information.


        .. note::
            Parameter key "SESSIONID" is handled for you.


        .. warning::
            DO NOT include the full URL - *Exclude: www.yourAMPURL.com/API/*\n



        Parameters
        -----------
        api: :class:`str`
            The AMP API endpoint to call. eg "Core/GetModuleInfo"
        parameters : None | dict[:class:`str`, Any], optional
            The parameters to pass to the API endpoint, by default is None

        Returns
        --------
        dict[:class:`str`, Any] :
           The JSON response from the API endpoint.

        """
        await self._connect()
        result: Any = await self._call_api(api=api, parameters=parameters)
        return result

    @staticmethod
    def camel_to_snake_re(data: str) -> str:
        """
        A simple regex pattern applied to a string to remove Camel Casing and apply snake_case.

        .. note::
            This will fail on entries with an underscore between to capital characters. |  *eg (Tool_Version = tool__version)*\n
            Will also not format properly when handling strings that have a multiple uppercase followed by a lowercase. | *eg (ContainerCPUs = container_cp_us)*


        Parameters
        -----------
        data: :class:`str`
            The string to be converted.

        Returns
        -------
        :class:`str`
            The converted string from CamelCase to snake_case.
        """

        data = re.sub(pattern="(.)([A-Z][a-z]+)", repl=r"\1_\2", string=data)
        return re.sub(pattern="([a-z0-9])([A-Z])", repl=r"\1_\2", string=data).lower()

    @staticmethod
    def camel_case_data(data: dict[str, Any]) -> dict[str, Any]:
        """
        Calls the :meth:`title` on every dict key.

        Parameters
        -----------
        data: dict[:class:`str`, Any]
            The dictionary to camel case.

        Returns
        --------
        dict[:class:`str`, Any]
            The camel cased dict.
        """

        res: dict[str, str | bool | int] = {}
        for key, value in data.items():
            if value is not None:
                res[key.title()] = value
        return res

    @staticmethod
    def dataclass_to_dict(dataclass_: DataclassInstance) -> dict[str, Any]:
        """
        Convert a dataclass to a dictionary.

        Parameters
        -----------
        dataclass_: :class:`DataclassInstance`
            The dataclass to convert.

        Returns
        --------
        dict[:class:`str`, Any]
            The converted dataclass as a dict.

        Raises
        -------
        :exc:`TypeError`
            When the object passed in is not of type(:class:`DataclassInstance`).
        """

        parameters: dict[Any, Any] = {}
        if is_dataclass(dataclass_) is False:
            raise TypeError(f"The object {dataclass_} is not of the same type as <dataclass>.")
        for field in fields(class_or_instance=dataclass_):
            value: Any = getattr(dataclass_, field.name)
            if value is None:
                continue
            parameters[field.name] = value
        return parameters

    @staticmethod
    def json_to_dataclass(
        json: Iterable[Any],
        format_: Union[type[X], type[APIResponseDataTableAlias]],
        _use_from_dict: bool,
        _auto_unpack: bool,
    ) -> X | list[APIResponseDataTableAlias | X] | APIResponseDataTableAlias | None:
        """
        Format the JSON response data to a dataclass.

        .. note::
            All JSON response data will be sanitized before it is turned into a dataclass. See :meth:`sanitize_json`.


        Parameters
        -----------
        json: Any
            JSON response data to format.
        format: Union[:class:`DataclassInstance`, class:`DeploymentTemplate`]
            Must be of type :class:`DataclassInstance` or similar to unpack the JSON response data.
        _use_from_dict: :class:`bool`
            Use :meth:`fromdict` from dataclass_wizard to unpack the JSON response data.
            - Typically this is used to handle nested :class:`DataclassInstance`.
        _auto_unpack: :class:`bool`
            Use ``**data`` to unpack the JSON response data.

        Returns
        --------
        X | list[:class:`DeploymentTemplate` | X] | :class:`DeploymentTemplate` | None
            Either a list or single entry of :class:`DataclassInstance`.

        """
        if isinstance(json, list):
            # _use_from_dict is to handle nested Dataclasses.
            if _use_from_dict is True:
                return [fromdict(format_, data) for data in json]

            # Self explanatory; uses the `**` annotation to unpack our data.
            elif _auto_unpack is True:
                return [format_(**data) for data in json]

            else:
                return [format_(data) for data in json]  # type: ignore

        if isinstance(json, dict):
            # _use_from_dict is to handle nested Dataclasses.
            if _use_from_dict is True:
                return fromdict(format_, json)

            elif _auto_unpack is True:
                return format_(**json)

            else:
                return format_(json)  # type: ignore
        return None

    def parse_bridge(self, bridge: Bridge) -> None:
        """
        Takes the :class:`Bridge` object and set's the :attr:`~Base.url` and sets :attr:`_bridge` to our Bridge object.

        .. note::
            Also validates the 2FA token.


        Parameters
        -----------
        bridge: :class:`Bridge`
            The :class:`Bridge` object to parse.

        Raises
        -------
        :exc:`ValueError`
            If 2FA Token is not provided and :attr:`_use_2fa` == True.\n
            If 2FA Token is not enclosed in single(',') or double(",") quotes.
        """
        # We use this later on in _connect to update `_session_id`;
        # so all connections will use the same session id (if possible)
        self._bridge = bridge
        self.url = bridge.url
        if bridge.use_2fa is True:
            if bridge.token == "":
                raise ValueError("You must provide a 2FA Token if you are using 2FA.")
            elif bridge.token.startswith(("'", '"')) is False or bridge.token.endswith(("'", '"')) is False:
                raise ValueError("2FA Token must be enclosed in quotes.")
            # Removed starting and ending quotes
            elif len(bridge.token) < 8:
                raise ValueError(
                    "Your 2FA token appears to be too short (<8 characters). Please use the code that generates the timed based tokens."
                )

    def parse_data(self, data: Union[Controller, Instance, InstanceStatus, Updates]) -> Self:
        """
        Takes in a :class:`DataclassInstance` and iterates through it's :meth:`fields` and
        set's the values as attributes of the :class:`DataclassInstance` that called this function.

        Parameters
        -----------
        data: Union[:class:`Controller`, :class:`Instance`, :class:`AppStatus`, :class:`Updates`]
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
    def sanitize_json(cls, json: Iterable) -> Iterable[Any]: ...

    @classmethod
    def sanitize_json(cls, json: Iterable | str) -> Iterable[Any] | str:
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
        """
        The path is relative to the Instances home directory. eg "/myInstanceName/" \n
        You do not need to include "." to specify the current directory as all path's start from root/home.

        .. note::
            Example `await Instance.copyFile("eula.txt", "test")` would move `./eula.txt` to `./test/eula.txt`


        Parameters
        -----------
        path: str
            The path to be sanitized.

        Raises
        -------
        :exc:`ValueError`
            If the path string contains a underscore.

        Returns
        --------
        :class:`str`
            Return the sanitized path string.
        """
        if "_" in path:
            raise ValueError("You cannot use '_' in path strings.")

        path = path.replace("//", "/")
        path = path.replace("\\", "/")
        path = path.replace("..", ".")

        # Remove starting periods as they are un-needed when being passed into an API
        if path.startswith("."):
            path = path[1:]

        # Remove starting slashes, all paths start relative to Instance root.
        if path.startswith("/"):
            path = path[1:]

        return path

    @staticmethod
    def to_snake_case(data: str, /) -> str:
        """
        Quick function to return snake_case from camelCase.

        Parameters
        ----------
        data: :class:`str`
            The string to convert.

        Returns
        --------
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

    async def version_validation(self, version: VersionInfo) -> None:
        """
        Compares the Version of the application/Instance against the version that is passed in.


        Parameters
        -----------
        version: :class:`VersionInfo`
            The version to compare against the application.
        Raises
        -------
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

        if isinstance(result, Diagnostics) and isinstance(result.application_version, VersionInfo):
            _version: VersionInfo = result.application_version
            if result.application_version < version:
                raise RuntimeError(self._version_unavailable, "`Core/GetWebserverMetrics`", _version)
        else:
            self.logger.warning(
                "Unable to validate version Info, the API call %s may raise an error", "`Core/GetDiagnosticsInfo`"
            )
