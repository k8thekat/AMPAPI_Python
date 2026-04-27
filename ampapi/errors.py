"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMP_API_Python.

AMP_API_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMP_API_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMP_API_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""
import logging
from pprint import pformat
from typing import Any

__all__ = ("APINetworkError", "ActionResultError")

LOGGER = logging.getLogger("AMPapi.errors")

class ActionResultError:
    """Represents the :meth:`_call_api` response if an error happens during runtime.

    Attributes
    ----------
    status: :class:`bool`
        If the API call was successful, typically this is False.
    reason: :class:`str`
        The reason for the failure in a generic manner.
    result: Union[str, :class:`Exception`]
        The Exception or result of the Error that occured and what it means.
    result_type: Any
        Typically a string representation of the :attr:`result` to know what the Exception was.

    """

    status: bool
    reason: str
    result: str | Exception
    result_type: Any

    def __init__(self, status: bool, reason: str, result: Exception | str) -> None:
        self.status = status
        self.reason = reason
        self.result = result
        self.result_type = type(result)

    def __repr__(self) -> str:
        return pformat(vars(self))

    def __str__(self) -> str:
        return self.__repr__()


class APINetworkError(Exception):
    def __init__(self, status_code: int, url: str, error_reason: str) -> None:  # noqa: D107
        message = "We encountered an error during a request to Moogle in %s. Current URL: %r | Status Code: %s"
        super().__init__(message, error_reason, url, status_code)
        LOGGER.error(message, error_reason, url, status_code)
