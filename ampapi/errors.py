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

__all__ = (
    "AMPAPIError",
    "AMPAPIKeyError",
    "AMPAPINetworkError",
    "AMPAPIOIDCSessionError",
    "AMPAPIPanelVersionError",
    "AMPAPIResponseError",
    "AMPAPITypeError",
)

LOGGER = logging.getLogger("AMPAPI_Python.errors")


class AMPAPIError(Exception):
    pass


class AMPAPIKeyError(AMPAPIError):
    def __init__(self, key_name: str, end_point: str, *args: object) -> None:  # noqa: D107
        message = "We encountered an KeyError in our response data from the AMP API Endpoint %s. | Missing Key Name: %s | Args: %s"
        super().__init__(message % (end_point, key_name, args))
        LOGGER.error(message, end_point, key_name, *args)


class AMPAPINetworkError(AMPAPIError):
    def __init__(self, status: int, url: str, reason: str) -> None:  # noqa: D107
        message = "We encountered an error during a post request to an AMP API Endpoint. Reason: %s | URL: %r | Status: %s"
        super().__init__(message % (reason, url, status))
        LOGGER.error(message, reason, url, status)


class AMPAPIResponseError(AMPAPIError):
    def __init__(self, title: str, url: str, reason: str) -> None:  # noqa: D107
        message = "We encountered an error handling a response from an AMP API Endpoint. Reason: %s | URL: %s | Title: %s"
        super().__init__(message % (reason, url, title))
        LOGGER.error(message, reason, url, title)


class AMPAPIOIDCSessionError(AMPAPIResponseError):
    """Raised in the OIDC mode when there is no session, so a new login through the provider is needed.

    It's raised on the call itself, for any call made before :meth:`~ampapi.Core.oidc_login`, after
    :meth:`~ampapi.Core.logout`, or after AMP ended the session.
    Send the browser to the URL from :meth:`~ampapi.Core.get_oidc_login_url`, then call :meth:`~ampapi.Core.oidc_login` again.

    .. versionadded:: 5.0.0
    """


class AMPAPIPanelVersionError(AMPAPIError):
    """Raised when the `url` in :class:`~ampapi.APIParams` is an AMP 3 panel. This library, cc-ampapi 5.x, is for AMP 2.

    For an AMP 3 panel, install cc-ampapi 6.0.0 or newer in place of 5.x: ``pip install --pre "cc-ampapi>=6"``.
    Until 6.0.0 is released, every 6.x version is a beta, and pip installs a beta only with ``--pre``.

    .. versionadded:: 5.0.1

    Attributes
    ----------
    url : :class:`str`
        The panel URL from :class:`~ampapi.APIParams`.
    phase : :class:`str`
        The setup stage the AMP 3 panel reports, eg. ``"ready"``.\n
        - For diagnosis only.

    """

    url: str
    phase: str

    def __init__(self, url: str, phase: str) -> None:  # noqa: D107
        self.url = url
        self.phase = phase
        message = 'The panel is AMP 3, and this library is for AMP 2. For AMP 3: pip install --pre "cc-ampapi>=6" | URL: %s | Phase: %s'
        super().__init__(message % (url, phase))
        LOGGER.error(message, url, phase)


class AMPAPITypeError(AMPAPIError):
    def __init__(self, end_point: str, cur_type: object, expec_type: object) -> None:  # noqa: D107
        cur_name = cur_type.__class__.__name__
        expec_name = expec_type.__name__ if isinstance(expec_type, type) else expec_type.__class__.__name__
        message = "We encountered a TypeError, the response data from an AMP API Endpoint is invalid in %s. | Response: %s | Expected: %s"
        super().__init__(message % (end_point, cur_name, expec_name))
        LOGGER.error(message, end_point, cur_name, expec_name)
