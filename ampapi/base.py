from __future__ import annotations
from typing import Union, Any
import json
import traceback
import logging

import aiohttp
from aiohttp import ClientResponse

from pyotp import TOTP  # 2Factor Authentication Python Module

from .types import *

__all__ = ("Base",)


class Base():
    _logger = logging.getLogger()
    _logger.setLevel(logging.INFO)

    def __init__(self, url: str, amp_user: str, amp_password: str, amp_2fa: bool = False, amp_2fa_token: str = "", instance_url: None | str = None) -> None:
        self._url: str = url + "/API/"
        self._amp_user: str = amp_user
        self._amp_password: str = amp_password
        self._amp_2fa: bool = amp_2fa
        self._amp_2fa_token: str = amp_2fa_token
        self._session_id: str = "0"

        if self._amp_2fa == True:
            if self._amp_2fa_token == "":
                raise ValueError("You must provide a 2FA Token if you are using 2FA.")
            if self._amp_2fa_token.startswith(("'", '"')) == False or self._amp_2fa_token.endswith(("'", '"')) == False:
                raise ValueError("2FA Token must be enclosed in quotes.")

        # self.FAILED_LOGIN: str = ""
        self.NO_DATA: str = "Failed to recieve any data from post request."
        self.ADS_ONLY: str = "This API call is only available on ADS instances."
        self.UNAUTHORIZED_ACCESS: str = f"{self._amp_user} user does not have the required permissions to interact with this instance."

    async def _call_api(self, api: str, parameters: None | dict[str, Any] = None) -> None | str | bool | dict | list[Any]:
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

        if self._session_id != "0":
            parameters["SESSIONID"] = self._session_id

        json_data = json.dumps(parameters)

        # _url = self._url + "/API/" + api
        print(api, self._url + api)
        async with aiohttp.ClientSession() as session:
            try:
                post_req = await session.post(self._url + api, headers=header, data=json_data)
            # TODO - Need to not catch all Excepts..
            except Exception as e:
                # So I can handle each exception properly.
                print("_call_api exception type:", type(e))
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
        print("API CALL---->", api, type(post_req_json))

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
                    self._session_id = "0"
                    raise PermissionError(self.UNAUTHORIZED_ACCESS)
            else:
                return post_req_json
        else:
            print("_call_api -> else `return post_req_json`")
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
        amp_2fa_code: Union[str, TOTP] = ""
        if isinstance(self._session_id, str) == False:
            raise ValueError("You must provide a session id as a string.")
        if self._session_id == "0":
            if self._amp_2fa == True:
                try:
                    # Handles time based 2Factory Auth Key/Code
                    amp_2fa_code = TOTP(self._amp_2fa_token)
                    amp_2fa_code.now()

                except AttributeError:
                    raise ValueError("Please check your 2 Factor Code, should not contain spaces, escape characters and it must be enclosed in quotes!")
            else:
                try:

                    parameters = {
                        'username': self._amp_user,
                        'password': self._amp_password,
                        'token': amp_2fa_code,
                        'rememberMe': True}

                    result = await self._call_api('Core/Login', parameters)
                    if isinstance(result, Union[None, bool, int, str]):
                        return result

                    # result = await self.login(amp_user=self._amp_user, amp_password=self._amp_password, token=amp_2fa_code, rememberME=True)

                    if isinstance(result, LoginResults):
                        self._session_id = result.sessionID
                    # if type(result) == dict and "sessionID" in result:
                    #     self._session_id = result['sessionID']

                    else:
                        self._logger.warning("Failed response from Instance")

                except Exception as e:
                    self._logger.warning(f'Core/Login Exception: {traceback.format_exc()}')

    async def callEndPoint(self, api: str, parameters: None | dict[str, Any] = None) -> list | dict | str | bool | int | None:
        """
        Universal API method for calling any API endpoint. Some API endpoints require ADS and some may require an Instance ID. \n

        Args:
            api (str): API endpoint to call. `eg "Core/GetModuleInfo"` (Assume this starts with www.yourAMPURL.com/API/)
            parameters (None | dict[str, str]): Parameters to pass to the API endpoint. Session ID is already handled for you. Defaults to None

        Returns:
            list | dict | str | bool | int | None: Returns the JSON response from the API call.
        """
        await self._connect()
        result = await self._call_api(api, parameters)
        return result
