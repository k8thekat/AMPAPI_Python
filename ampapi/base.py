from __future__ import annotations

import json
import logging
import traceback
from dataclasses import fields
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Union

import aiohttp
from aiohttp import ClientResponse
from dataclass_wizard import fromdict
from pyotp import TOTP

from ampapi.types import APISession  # 2Factor Authentication Python Module

from .bridge import Bridge
from .types import *

if TYPE_CHECKING:
    from typing import Self

__all__ = ("Base",)

FORMAT_DATA: bool = True


class Base():
    """
    Contains the base functions for all AMP API endpoints and handles the parsing of Bridge data.

    """
    _logger: logging.Logger = logging.getLogger()
    InstanceID: str = "0"
    Module: str = ""
    # Seconds (Typically a session expires after 5 minutes of inactivity.)
    session_ttl: int = 240
    url: str = ""

    NO_DATA: str = "Failed to receive any data from post request."
    ADS_ONLY: str = "This API call is only available on ADS instances."
    UNAUTHORIZED_ACCESS: str = "The user does not have the required permissions to interact with this instance."
    NO_BRIDGE: str = "Failed to setup connection. You need to initiate `<class Bridge>` first."
    MINECRAFT_ONLY: str = "This API call is only available on Minecraft instances."
    FAILED_API: str = "The API call returned a non-proper response."

    def __init__(self) -> None:
        bridge: Bridge = Bridge.get_bridge()
        # Validate the bridge object is at the same memory address.
        self._logger.debug(f"bridge object -> {bridge}")
        if bridge == None:
            raise ValueError(self.NO_BRIDGE)

        if isinstance(bridge, Bridge):
            self.parse_bridge(bridge=bridge)  # type:ignore

    @property
    def format_data(self) -> bool:
        """
        Controls whether the data returned from the API endpoint is formatted or not. \n
        `True` = formatted \n
        `False` = unformatted

        Returns:
            bool: `True` or `False`, defaults to `True`.
        """
        global FORMAT_DATA
        return FORMAT_DATA

    @format_data.setter
    def format_data(self, value: bool):
        global FORMAT_DATA
        FORMAT_DATA = value

    # def set_format_data(self, value: bool = True) -> bool:
    #     """
    #     Controls whether the data returned from the API endpoint is formatted or not. \n
    #     `True` = formatted \n
    #     `False` = unformatted

    #     Returns:
    #         bool: `True` or `False`, defaults to `True`.
    #     """
    #     FORMAT_DATA: bool = value
    #     return FORMAT_DATA

    def parse_bridge(self, bridge: Bridge):
        """
        Takes the Bridge class object and pulls the APIparams data from it and set's the class attributes for API usage.

        Args:
            bridge (Bridge): The Bridge class object to parse.

        Raises:
            ValueError: If 2FA Token is not provided and `_use_2fa == True`.
            ValueError: If 2FA Token is not enclosed in single(',') or double(",") quotes.
        """
        # We use this later on in _connect to update `_session_id`;
        # so all connections will use the same session id (if possible)
        self._bridge: Bridge = bridge
        self.url = bridge.url
        if bridge.use_2fa == True:
            if bridge.token == "":
                raise ValueError("You must provide a 2FA Token if you are using 2FA.")
            if bridge.token.startswith(("'", '"')) == False or bridge.token.endswith(("'", '"')) == False:
                raise ValueError("2FA Token must be enclosed in quotes.")

    def parse_data(self, data: Controller | Instance | AppStatus | Updates) -> Self:
        """
        Takes in a Controller or Instance dataclass and iterates through it's attributes and 
        set's the values as attributes of the class that called this function.

        Args:
            data (Controller | Instance): The Controller or Instance dataclass.

        Returns:
            Self: Returns the class that called this function.
        """
        for field in fields(data):
            # This is to deal with improperly cased InstanceId.
            if field.name == "InstanceId":
                setattr(self, "InstanceID", getattr(data, field.name))
                continue
            setattr(self, field.name, getattr(data, field.name))
        return self

    def camel_case_data(self, data: dict[str, str | bool | int | None]) -> dict[str, str | int | bool]:
        """
        Camel case the keys of a dictionary.

        Args:
            data (dict[str, str  |  bool  |  None]): The dictionary to camel case.

        Returns:
            dict[str, str | bool]: The camel cased dictionary.
        """
        new: dict[str, str | bool | int] = {}
        for key, value in data.items():
            if value is not None:
                new[key.title()] = value
        return new

    def dataclass_to_dict(self, dataclass: Any) -> dict[Any, Any]:
        """
        Convert a dataclass to a dictionary.

        Args:
            dataclass (Any): The dataclass to convert.

        Returns:
            dict[Any, Any]: The converted dataclass as a dictionary.
        """
        parameters = {}
        for field in fields(dataclass):
            value = getattr(dataclass, field.name)
            if value == None:
                continue
            parameters[field.name] = value
        return parameters

    def json_to_dataclass(self, json: Any, format: Any, _use_from_dict: bool, _auto_unpack: bool) -> Any | list[Any]:
        """
        Format the JSON response data to a dataclass.

        Args:
            json (Any): JSON data to format.
            format (Any): Dataclass or similar to unpack the JSON data into.
            _use_from_dict (bool): Use dataclass wizard `fromdict()` or not.
            _auto_unpack (bool): Use **data or not to unpack the data.

        Returns:
            Any | list[Any]: A list of the format object or a single format object.

        """
        if isinstance(json, list):
            if _use_from_dict is True:
                return list(fromdict(format, data) for data in json)

            elif _auto_unpack is True:
                return list(format(**data)for data in json)

            else:
                return list(format(data)for data in json)
        else:
            if _use_from_dict is True:
                return fromdict(format, json)

            elif _auto_unpack is True:
                return format(**json)

            else:
                return format(json)

    async def _call_api(self, api: str, parameters: Union[None, dict[str, Any]] = None, format_data: Union[bool, None] = None, format: Any = None, _use_from_dict: bool = True, _auto_unpack: bool = True) -> Any:
        # TODO - Possibly convert the ending args to *args or similar.
        """
        Uses aiohttp.ClientSession() post request to access the AMP API endpoints. \n
        Will automatically populate the `SESSIONID` parameter if it is not provided.

        Args:
            api (str): The API endpoint to call. eg `Core/GetModuleInfo`
            parameters (dict[str, str]): The parameters to pass to the API endpoint.
            format_data (Union[bool, None]): Controls whether the data returned from the API endpoint is formatted or not. Defaults to `None`.
            format (Any): The dataclass the Response json will return. Defaults to `None`.
            _use_from_dict (bool): Controls whether the data will use `fromdict` of dataclass wizard to unpack the data. Typical usage case is nested Dataclasses. Defaults to `True`.
            _auto_unpack (bool): Controls whether the data will be unpacked automatically. Defaults to `True`.

        Raises:
            ValueError: When the API call returns no data or raises any exception.
            ConnectionError: When the API call returns a status code other than 200.
            PermissionError: When the API call returns a `Unauthorized Access` error or permission related error.

        Returns:
            Any: Returns the JSON response, either formatted or unformatted depending on `format_data`.
        """
        global FORMAT_DATA
        header: dict = {"Accept": "text/javascript"}
        post_req: ClientResponse | None
        self._logger.debug(f"_call_api -> {api} was called with {parameters}")

        # This should save us some boiler plate code throughout our API calls.
        if parameters == None:
            parameters = {}

        api_session: APISession = self._bridge._sessions.get(self.InstanceID, APISession(id="0", ttl=datetime.now()))
        if isinstance(api_session, APISession):
            parameters["SESSIONID"] = api_session.id

        json_data = json.dumps(parameters)

        _url: str = self.url + "/API/" + api
        # print("DEBUG", self.InstanceID, api, _url)
        async with aiohttp.ClientSession() as session:
            try:
                post_req = await session.post(_url, headers=header, data=json_data)
            # TODO - Need to not catch all Excepts..
            # So I can handle each exception properly.
            except Exception as e:
                self._logger.error(f"DEBUG _call_api exception type: {type(e)}")
                raise ValueError(e)

            if post_req.content_length == 0:
                raise ValueError(self.NO_DATA)

            if post_req.status != 200:
                raise ConnectionError(self.NO_DATA)

            post_req_json: Any = await post_req.json()

        if post_req_json == None:
            raise ConnectionError(self.NO_DATA)

        # They removed "result" from all replies thus breaking most if not all future code.
        # This was an old example from pre 2.3 AMP API that could have the following return:
        # `{'resultReason': 'Internal Auth - No reason given', 'success': False, 'result': 0}`
        # print("DEBUG", "API CALL---->", api, type(post_req_json), parameters)
        # print("DEBUG", post_req_json)
        if isinstance(post_req_json, dict):
            if api == "Core/Login":
                return LoginResults(**post_req_json)

            elif "result" in post_req_json:
                post_req_json = post_req_json["result"]

            elif "Title" in post_req_json:
                post_req_json = post_req_json["Title"]
                if isinstance(post_req_json, str) and post_req_json == "Unauthorized Access":
                    self._logger.error(f'{api} failed because of {post_req_json}')
                    api_session = APISession(id="0", ttl=datetime.now())
                    self._bridge._sessions.update({self.InstanceID: api_session})
                    raise PermissionError(self.UNAUTHORIZED_ACCESS)

            elif isinstance(post_req_json, bool) and post_req_json == False:
                self._logger.error(f"{api} failed because of {post_req_json}")
                raise ConnectionError(self.FAILED_API)

            elif isinstance(post_req_json, dict) and "Status" in post_req_json and post_req_json["Status"] == False:
                self._logger.error(f"{api} failed because of Status: {post_req_json}")
                return ConnectionError(self.FAILED_API)

        # print("DEBUG", "FORMAT->", format_data, format)
        if format is None or format_data is False:
            return post_req_json

        elif format_data is True or format_data is None and FORMAT_DATA is True:
            return self.json_to_dataclass(json=post_req_json, format=format, _use_from_dict=_use_from_dict, _auto_unpack=_auto_unpack)

    async def _connect(self) -> LoginResults | None:
        """
        Handles your 2FA code and logging into AMP while also handling the session ID. \n

        Raises:
            ValueError: If session ID is not a string or 2FA code is not a formatted properly.
            TypeError: If the session is not an APISession object.

        Returns:
            bool | None: Returns False if an exception is thrown or the login attempt fails to provide a sessionID value. \n
            Otherwise returns true and sets the class's sessionID value.
        """
        code: Union[str, TOTP] = ""

        # get our InstanceID and use it to key for session_id
        session: APISession = self._bridge._sessions.get(self.InstanceID, APISession(id="0", ttl=datetime.now()))
        if isinstance(session, APISession):
            ttl: timedelta = datetime.now() - session.ttl
            if ttl.seconds > 240:
                sessionID = "0"
            else:
                sessionID: str = session.id
        else:
            raise TypeError(f"session must be of type APISession. Received {type(session)}")

        if sessionID == "0":
            if self._bridge.use_2fa == True:
                try:
                    # Handles time based 2Factory Auth Key/Code
                    code = TOTP(self._bridge.token).now()

                except AttributeError:
                    raise ValueError("Please check your 2 Factor Code, should not contain spaces, escape characters and it must be enclosed in quotes!")
            else:
                try:

                    parameters = {
                        'username': self._bridge.user,
                        'password': self._bridge.password,
                        'token': code,
                        'rememberMe': True}

                    result = await self._call_api(api='Core/Login', parameters=parameters, format_data=True, format=LoginResults)
                    if isinstance(result, LoginResults):
                        # This is our new sessions table to correlate InstanceID to a sessionID.
                        api_session = APISession(id=result.sessionID, ttl=datetime.now())
                        self._bridge._sessions.update({self.InstanceID: api_session})
                        return result

                    else:
                        self._logger.warning("Failed response from Core/Login in _connect()")
                        return result

                except Exception as e:
                    self._logger.warning(f'Core/Login Exception: {traceback.format_exc()}')
        else:
            return

    async def call_end_point(self, api: str, parameters: None | dict[str, Any] = None) -> Any:
        """
        Universal API method for calling any API endpoint. Some API endpoints require ADS and some may require an Instance ID. \n

        The Data returned will be unmodified. No DATACLASS returns.

        Args:
            api (str): API endpoint to call. `eg "Core/GetModuleInfo"` (Assume this starts with www.yourAMPURL.com/API/)
            parameters (None | dict[str, str]): Parameters to pass to the API endpoint. Session ID is already handled for you. Defaults to None

        Returns:
            Any: Returns the JSON response from the API call.
        """

        result = await self._call_api(api=api, parameters=parameters)
        return result
