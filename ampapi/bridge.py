from typing import Self
from .types import APIparams

__all__ = ("Bridge",)


class Bridge():
    """
    Handles the API login credentials for connecting to AMP.

    Simply create the class similar to the example and then access any other API class you wish.\n
        *eg* `_bridge: Bridge | None = Bridge(apiparams= <class APIparams>)`
                `APICore = Core() #this will pull login details from the Bridge class`

    """
    apiparams: APIparams

    @classmethod
    def get_bridge(cls) -> Self:
        """
        Retrieves an existing Bridge class object.\n
        **`DO NOT CALL THIS METHOD OUTSIDE OF API CLASSES`**

        Raises:
            ValueError: If the Bridge class does not exist.

        Returns:
            Bridge: A singleton class of Bridge
        """
        if cls._instance == None:
            raise ValueError("Failed to setup connection. You need to initiate `<class Bridge>` first.")
        return cls._instance

    def __new__(cls, apiparams: APIparams | None = None, *args, **kwargs) -> Self | None:
        if not hasattr(cls, "_instance"):
            cls._instance = super(Bridge, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, apiparams: APIparams, *args, **kwargs) -> None:
        self.apiparams: APIparams = apiparams
