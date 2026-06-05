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

import logging
from dataclasses import fields
from typing import Union

from typing_extensions import Any, Self

from .modules import APIParams

__all__ = ("Bridge",)

LOGGER: logging.Logger = logging.getLogger(__name__)


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

    .. note::
        ### Version 5.0:
        - :class:`Bridge` added optional parameter to allow for non-singleton usage.

    Parameter
    ----------
    api_params: :class:`APIParams`
        The prebuilt class to pass login credentials to <Bridge>.
    singleton: :class:`bool`, optional
        If ``True``, the :class:`Bridge` will be created as a singleton, by default False.

    """

    def __new__(cls, api_params: APIParams, singleton: bool = True, *args: Any, **kwargs: Any) -> Union["Bridge", Self]:  # noqa: ARG004, D417
        """Controls instance creation, returning a shared instance when ``singleton=True``.

        Parameters
        ----------
        api_params: :class:`APIParams`
            The prebuilt class to handle login credentials.
        singleton: :class:`bool`, optional
            If ``True``, returns the existing shared instance if one exists, by default True.

        Returns
        -------
        :class:`Bridge`
            A new or existing :class:`Bridge` instance.

        """
        if singleton is True:
            if hasattr(cls, "_instance") is False:
                cls._instance: Bridge = super().__new__(cls, *args, **kwargs)
                return cls._instance
            return cls._instance

        cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, api_params: APIParams, singleton: bool = True) -> None:
        """Initializes the :class:`Bridge` with the provided API credentials.

        Skips re-initialization if this instance is already a singleton.

        Parameters
        ----------
        api_params: :class:`APIParams`
            The prebuilt class to handle login credentials.
        singleton: :class:`bool`, optional
            If ``True``, prevents re-initialization of an existing singleton instance, by default True.

        """
        LOGGER.debug("<%s.%s> | ID: %s | API_PARAMS: %s | SINGLETON: %s", __class__.__name__, "__init__", id(self), api_params, singleton)

        for field in fields(class_or_instance=api_params):
            setattr(self, field.name, getattr(api_params, field.name))

    @classmethod
    def _get_bridge(cls) -> "Bridge":
        """Retrieves the :class:`Bridge` class instance variable.\n

        .. note::
            Current usage is inside :class:`Base` only.


        Raises
        ------
        :exc:`ValueError`
            If the :class:`Bridge` has not been created yet.

        Returns
        -------
        :class:`Bridge`:
                The :class:`Bridge`._instance attribute.

        """
        if not hasattr(cls, "_instance"):
            err = "Failed to setup connection. You need to initiate <Bridge> first."
            raise ValueError(err)
        return cls._instance
