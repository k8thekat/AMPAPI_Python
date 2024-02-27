from __future__ import annotations
from datetime import timedelta
from typing import Union, Any, TYPE_CHECKING
import json
import traceback
import logging
from dataclasses import fields

import aiohttp
from aiohttp import ClientResponse

from pyotp import TOTP

from ampapi.types import APISession  # 2Factor Authentication Python Module
from .types import *
from .bridge import Bridge

if TYPE_CHECKING:
    from typing import Self

__all__ = ("Base",)


class Base():
    """
    Contains the base functions for all AMP API endpoints and handles the parsing of Bridge data.

    """
    _logger: logging.Logger = logging.getLogger()
    InstanceID: str = "0"
    Module: str = ""
    session_ttl: int = 240  # Seconds (Typically a session expires after 5 minutes of inactivity.)
    url: str = ""

    # self.FAILED_LOGIN: str = ""
    NO_DATA: str = "Failed to recieve any data from post request."
    ADS_ONLY: str = "This API call is only available on ADS instances."
    UNAUTHORIZED_ACCESS: str = "The user does not have the required permissions to interact with this instance."
    NO_BRIDGE: str = "Failed to setup connection. You need to initiate `<class Bridge>` first."
    MINECRAFT_ONLY: str = "This API call is only available on Minecraft instances."
    # NO_VALID_SESSION: str = "Failed to find a valid session id, please login again."

    def __init__(self) -> None:
        bridge: Bridge = Bridge.get_bridge()
        # Validate the bridge object is at the same memory address.
        self._logger.debug(f"bridge object -> {bridge}")
        print("DEBUG", f"bridge object -> {bridge}")
        if bridge == None:
            raise ValueError(self.NO_BRIDGE)

        if isinstance(bridge, Bridge):
            self.parse_bridge(bridge=bridge)  # type:ignore

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

    def parse_data(self, data: Controller | Instance) -> Self:
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

    async def _call_api(self, api: str, parameters: None | dict[str, Any] = None) -> None | str | bool | dict[str, Any] | list[Any]:
        """
        Uses aiohttp.ClientSession() post request to access the AMP API endpoints. \n
        Will automatically populate the `SESSIONID` parameter if it is not provided.

        Args:
            api (str): The API endpoint to call. eg `Core/GetModuleInfo`
            parameters (dict[str, str]): The parameters to pass to the API endpoint.

        Raises:
            ValueError: When the API call returns no data or raises any exception.
            ConnectionError: When the API call returns a status code other than 200.
            PermissionError: When the API call returns a `Unauthorized Access` error or permission related error.

        Returns:
            None | str | bool | dict | list[Any]: Returns unmodified JSON response from the API call. Typically a string or dict.
        """

        header: dict = {"Accept": "text/javascript"}
        post_req: ClientResponse | None
        self._logger.debug(f"_call_api -> {api} was called with {parameters}")

        # This should save us some boiler plate code throughout our API calls.
        if parameters == None:
            parameters = {}

        # TODO - New sessionId implementation
        api_session: APISession = self._bridge._sessions.get(self.InstanceID, APISession(id="0", ttl=datetime.now()))
        if isinstance(api_session, APISession):
            parameters["SESSIONID"] = api_session.id

        json_data = json.dumps(parameters)

        _url: str = self.url + "/API/" + api
        print("DEBUG", self.InstanceID, api, _url)
        async with aiohttp.ClientSession() as session:
            try:
                post_req = await session.post(_url, headers=header, data=json_data)
            # TODO - Need to not catch all Excepts..
            except Exception as e:
                # So I can handle each exception properly.
                print("DEBUG", "_call_api exception type:", type(e))
                raise ValueError(e)

            if post_req.content_length == 0:
                raise ValueError(self.NO_DATA)

            if post_req.status != 200:
                raise ConnectionError(self.NO_DATA)

            post_req_json = await post_req.json()

        if post_req_json == None:
            raise ConnectionError(self.NO_DATA)
        # I should force return Data classes with this to help better handle the API change. See types.py
        # They removed "result" from all replies thus breaking most if not all future code.
        # Core/Login can trigger this because it has a key "result" near the end.
        # TODO -- This will need to be tracked and see what triggers what.
        # Possibly catch failed login's sooner; check `Core/Login` after the dict check.
        # `{'resultReason': 'Internal Auth - No reason given', 'success': False, 'result': 0}`
        # See about returning None or similar and use `if not None` checks on each API return.
        print("DEBUG", "API CALL---->", api, type(post_req_json), parameters)

        if isinstance(post_req_json, dict):
            if "result" in post_req_json:
                data = post_req_json["result"]

                if isinstance(data, bool) and data == False:
                    self._logger.error(f"{api} failed because of {post_req_json}")
                    return data

                elif isinstance(data, dict) and "Status" in data and data["Status"] == False:
                    self._logger.error(f"{api} failed because of Status: {post_req_json}")
                    return data["Status"]

                # This is to handle the new API Core/Login
                elif api == "Core/Login":
                    return post_req_json

                else:
                    # Return our dict keyed data.
                    return data

            elif "Title" in post_req_json:
                data = post_req_json["Title"]
                if isinstance(data, str) and data == "Unauthorized Access":
                    self._logger.error(f'{api} failed because of {post_req_json}')
                    # self._session_id = "0"
                    # TODO - New sessionID implementation.
                    api_session = APISession(id="0", ttl=datetime.now())
                    self._bridge._sessions.update({self.InstanceID: api_session})
                    raise PermissionError(self.UNAUTHORIZED_ACCESS)
            else:
                return post_req_json
        else:
            print("DEBUG", "_call_api -> else `return post_req_json`")
            return post_req_json

    async def _connect(self) -> LoginResults | str | int | dict | list | bool | None:
        """
        Handles your 2FA code and logging into AMP while also handling the session ID. \n

        Raises:
            ValueError: If session ID is not a string or 2FA code is not a formatted properly.

        Returns:
            bool | None: Returns False if an exception is thrown or the login attempt fails to provide a sessionID value. \n
            Otherwise returns true and sets the class's sessionID value.
        """
        code: Union[str, TOTP] = ""

        # TODO - New Session handling
        # get our InstanceID and use it to key for session_id
        session: APISession = self._bridge._sessions.get(self.InstanceID, APISession(id="0", ttl=datetime.now()))

        if isinstance(session, APISession):
            ttl: timedelta = datetime.now() - session.ttl
            if ttl.seconds > 240:
                sessionID = "0"
            else:
                sessionID: str = session.id

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

                    result = await self._call_api('Core/Login', parameters)
                    if isinstance(result, Union[None, bool, int, str]):
                        return result

                    elif isinstance(result, dict):
                        login = LoginResults(**result)
                        # This is local for any re-occurence of class usage.
                        # self._session_id = login.sessionId

                        # This is the Bridge object; so any other API class will use an existing sessionId.
                        # self._bridge.apiparams._session_id = login.sessionId

                        # TODO - New Session handling
                        # This is our new sessions table to correlate InstanceId to a sessionId.
                        api_session = APISession(id=login.sessionID, ttl=datetime.now())
                        self._bridge._sessions.update({self.InstanceID: api_session})
                        return login

                    else:
                        self._logger.warning("Failed response from Instance")

                except Exception as e:
                    self._logger.warning(f'Core/Login Exception: {traceback.format_exc()}')

    async def call_end_point(self, api: str, parameters: None | dict[str, Any] = None) -> list | dict | str | bool | int | None:
        """
        Universal API method for calling any API endpoint. Some API endpoints require ADS and some may require an Instance ID. \n

        The Data returned will be unmodified. No DATACLASS returns.

        Args:
            api (str): API endpoint to call. `eg "Core/GetModuleInfo"` (Assume this starts with www.yourAMPURL.com/API/)
            parameters (None | dict[str, str]): Parameters to pass to the API endpoint. Session ID is already handled for you. Defaults to None

        Returns:
            list | dict | str | bool | int | None: Returns the JSON response from the API call.
        """

        result = await self._call_api(api, parameters)
        return result
