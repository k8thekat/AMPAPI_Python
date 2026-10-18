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

__all__ = ("AMPAPIError", "AMPAPIKeyError", "AMPAPINetworkError", "AMPAPIResponseError", "AMPAPITypeError")

LOGGER = logging.getLogger("AMPAPI_Python.errors")


class AMPAPIError(Exception):
    pass


class AMPAPIResponseError(AMPAPIError):
    def __init__(self, title: str, url: str, reason: str) -> None:  # noqa: D107
        message = "We encountered an error handling a response from an AMP API Endpoint. Reason: %s | URL: %s | Title: %s"
        super().__init__(message % (reason, url, title))
        LOGGER.error(message, reason, url, title)


class AMPAPINetworkError(AMPAPIError):
    def __init__(self, status: int, url: str, reason: str) -> None:  # noqa: D107
        message = "We encountered an error during a post request to an AMP API Endpoint. Reason: %s | URL: %r | Status: %s"
        super().__init__(message % (reason, url, status))
        LOGGER.error(message, reason, url, status)


class AMPAPIKeyError(AMPAPIError):
    def __init__(self, key_name: str, end_point: str, *args: object) -> None:  # noqa: D107
        message = "We encountered an KeyError in our response data from the AMP API Endpoint %s. | Missing Key Name: %s | Args: %s"
        super().__init__(message % (end_point, key_name, args))
        LOGGER.error(message, end_point, key_name, *args)


class AMPAPITypeError(AMPAPIError):
    def __init__(self, end_point: str, cur_type: object, expec_type: object) -> None:  # noqa: D107
        cur_name = cur_type.__class__.__name__
        expec_name = expec_type.__name__ if isinstance(expec_type, type) else expec_type.__class__.__name__
        message = "We encountered a TypeError, the response data from an AMP API Endpoint is invalid in %s. | Response: %s | Expected: %s"
        super().__init__(message % (end_point, cur_name, expec_name))
        LOGGER.error(message, end_point, cur_name, expec_name)
