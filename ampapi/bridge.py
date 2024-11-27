import logging
from dataclasses import fields
from typing import Any, Union

from .dataclass import APIParams

__all__ = ("Bridge",)


class Bridge(APIParams):
    """
    Handles the API login credentials for connecting to AMP.

    Simply create the class similar to the example below and then access any other API class you wish.\n
    Then when creating any API class,  this will pull login details from the :py:class:`Bridge`.

    .. code-block:: python
        :linenos:


        # This is to handle login details.
        _params = APIParams(url="http://192.168.13.130:8080", user="bot_username", password="bot_password")
        _bridge: Bridge = Bridge(ap_params=_params)
        del _params



    """

    api_params: APIParams
    _logger: logging.Logger = logging.getLogger()

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
        """
        Retrieves the singleton :class:`Bridge` object.\n

        .. warning::
            **DO NOT CALL THIS FUNCTION OUTSIDE OF AN API CLASS (:class:`ADSModule`, :class:`Core`, etc..)**


        Raises
        ------
        :exc:`ValueError`
            If the :class:`Bridge` has not been created yet.

        Returns
        --------
        :class:`Bridge`:
                A singleton class of Bridge
        """
        if cls._instance is None:
            raise ValueError("Failed to setup connection. You need to initiate `<class Bridge>` first.")
        return cls._instance
