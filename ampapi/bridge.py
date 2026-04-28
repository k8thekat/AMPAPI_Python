import logging
from dataclasses import fields
from typing import Any, Union

from .modules import APIParams

__all__ = ("Bridge",)


class Bridge(APIParams):
    """Handles the API login credentials for connecting to AMP.

    Simply create the class similar to the example below and then access any other API class you wish.\n
    Then when creating any API class,  this will pull login details from the :py:class:`Bridge`.

    .. code-block:: python
        :linenos:


        # This is to handle login details.
        _params = APIParams(url="http://192.168.13.130:8080", user="bot_username", password="bot_password")
        _bridge: Bridge = Bridge(ap_params=_params)
        del _params

    For OIDC authentication, set :attr:`APIParams.auth_mode` to :attr:`AuthMode.oidc` and complete the IdP flow
    externally. The library will skip the standard ``Core/Login`` step; you must call :meth:`Core.oidc_login`
    once with the authorization code to populate the session before any other API call will succeed.

    .. code-block:: python
        :linenos:


        _params = APIParams(url="http://192.168.13.130:8080", auth_mode=AuthMode.oidc)
        _bridge: Bridge = Bridge(api_params=_params)
        core = Core()
        # User performs the IdP flow externally and obtains `code`.
        await core.oidc_login(code=code, redirect_uri="http://192.168.13.130:8080/", instance_id="null")

    Parameter
    ----------
    api_params: :class:`APIParams`
        The prebuilt class to handle login credentials.

    """

    api_params: APIParams
    _logger: logging.Logger = logging.getLogger(__name__)

    def __new__(cls, api_params: Union[APIParams, None] = None, *args: Any, **kwargs: Any) -> Union["Bridge", None]:
        if not hasattr(cls, "_instance"):
            cls._instance: Bridge = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, api_params: APIParams, *args: Any, **kwargs: Any) -> None:
        self._logger.debug("DEBUG %s __init__ %s", type(self).__name__, id(self))
        self.api_params: APIParams = api_params
        # We parse the api params for easier usage.
        for field in fields(class_or_instance=api_params):
            setattr(self, field.name, getattr(self.api_params, field.name))

    @classmethod
    def _get_bridge(cls) -> "Bridge":
        """Retrieves the singleton :class:`Bridge` object.\n

        .. warning::
            **DO NOT CALL THIS FUNCTION OUTSIDE OF AN API CLASS (:class:`ADSModule`, :class:`Core`, etc..)**


        Raises
        ------
        :exc:`ValueError`
            If the :class:`Bridge` has not been created yet.

        Returns
        -------
        :class:`Bridge`:
                A singleton class of Bridge

        """
        if cls._instance is None:
            raise ValueError("Failed to setup connection. You need to initiate `<class Bridge>` first.")
        return cls._instance
