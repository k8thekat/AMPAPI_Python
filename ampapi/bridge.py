from dataclasses import fields
from typing import TYPE_CHECKING, Self

from .types import APIParams

__all__ = ("Bridge",)


class Bridge(APIParams):
    """
    Handles the API login credentials for connecting to AMP.

    Simply create the class similar to the example and then access any other API class you wish.\n
        *eg* `_bridge: Bridge | None = Bridge(apiparams= <class APIparams>)`
                `APICore = Core() #this will pull login details from the Bridge class`

    """
    apiparams: APIParams

    @classmethod
    def get_bridge(cls) -> Self:
        """
        Retrieves an existing Bridge class object.\n
        **`DO NOT CALL THIS METHOD OUTSIDE OF AN API CLASS (ADSModule, Core, etc..)`**

        Raises:
            ValueError: If the Bridge class does not exist.

        Returns:
            Bridge: A singleton class of Bridge
        """
        if cls._instance == None:
            raise ValueError("Failed to setup connection. You need to initiate `<class Bridge>` first.")
        return cls._instance

    def __new__(cls, api_params: APIParams | None = None, *args, **kwargs) -> Self | None:
        if not hasattr(cls, "_instance"):
            cls._instance = super(Bridge, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, api_params: APIParams, *args, **kwargs) -> None:
        # print("DEBUG Bridge __init__")
        self.api_params: APIParams = api_params
        # We parse the api params for easier usage.
        for field in fields(api_params):
            setattr(self, field.name, getattr(self.api_params, field.name))
