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

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .base import Base

if TYPE_CHECKING:
    from ._types import HTTPSCheckResponse, HTTPSSetupStatusResponse, HTTPSStateResponse

__all__ = ("HTTPSModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class HTTPSModule(Base):
    """The calls for how the panel is reached over HTTPS: AMP's own certificate setup, or a reverse proxy it trusts.

    .. versionadded:: 6.0.0

    """

    async def check_https(self, host_name: str) -> HTTPSCheckResponse:
        """Check a domain name is ready for AMP's own HTTPS setup, before :meth:`start_https_setup`.

        |coro|

        Endpoint: ``POST /api/https/check``

        Parameters
        ----------
        host_name : :class:`str`
            The domain name, which has to point at this panel.

        Returns
        -------
        :class:`HTTPSCheckResponse`
            The outcome and each check, eg. if the name points at the panel's public address.

        """
        return await self._request(method="POST", path="/api/https/check", data={"hostName": host_name})

    # TODO: Drop the note once AMP's reads follow the change at once (U19a).
    # AMP 3.0.0.6 still shows the proxy in `GET /api/https` and the passkey capabilities for a few seconds.
    async def delete_own_proxy(self) -> HTTPSStateResponse:
        """Stop trusting the reverse proxy :meth:`set_own_proxy` set.

        |coro|

        Endpoint: ``DELETE /api/https/own-proxy``

        .. note::
            For a few seconds after, :meth:`get_https_state` and :meth:`Session.get_capabilities` still show the
            proxy. Use the state this returns.

        Returns
        -------
        :class:`HTTPSStateResponse`
            The HTTPS state, with `mode` ``"none"`` and no `trustedProxies`.

        """
        return await self._request(method="DELETE", path="/api/https/own-proxy")

    async def get_https_setup_status(self) -> HTTPSSetupStatusResponse:
        """Get the progress of AMP's own HTTPS setup.

        |coro|

        Endpoint: ``GET /api/https/setup/status``

        Returns
        -------
        :class:`HTTPSSetupStatusResponse`
            The setup's phase and checks.

        """
        return await self._request(method="GET", path="/api/https/setup/status")

    async def get_https_state(self) -> HTTPSStateResponse:
        """Get the panel's HTTPS setup and the addresses it is reached on.

        |coro|

        Endpoint: ``GET /api/https``

        Returns
        -------
        :class:`HTTPSStateResponse`
            The HTTPS mode, the panel's addresses and any trusted reverse proxies.

        """
        return await self._request(method="GET", path="/api/https")

    # TODO: Type the reply once AMP is seen answering it live (#3-47.10).
    # Only the refusal for a panel without AMP's own HTTPS is known; the reply to a recheck isn't.
    async def recheck_https(self) -> Any:
        """Check AMP's own HTTPS again, eg. its certificate.

        |coro|

        Endpoint: ``POST /api/https/recheck``

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If AMP's own HTTPS isn't set up (409, ``"https.error.notConfigured"``); a proxy from :meth:`set_own_proxy`
            doesn't count.

        """
        return await self._request(method="POST", path="/api/https/recheck")

    # TODO: Type the reply once AMP is seen answering it live (#3-47.10).
    # The path comes from the web panel's code; no capture shows the response yet.
    async def remove_https(self) -> Any:
        """Remove AMP's own HTTPS; the panel stays on plain HTTP at its own port.

        |coro|

        Endpoint: ``POST /api/https/remove``

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path="/api/https/remove")

    async def set_own_proxy(self, address: str, *, api_only: bool = False) -> HTTPSStateResponse:
        """Trust a reverse proxy in front of the panel, such as Caddy or nginx.

        |coro|

        Endpoint: ``POST /api/https/own-proxy``

        AMP then takes the forwarded headers from that address, so sign-ins and audit entries carry the user's real
        address. Passkeys also need ``"public-address.publicUrl"`` set to the proxy's HTTPS address, see
        :meth:`PlatformModule.set_settings`.

        Parameters
        ----------
        address : :class:`str`
            The proxy's IP address as AMP sees it, eg. ``"127.0.0.1"`` for a proxy on the same machine, or a network
            in CIDR form.
        api_only : :class:`bool`, optional
            If AMP should serve only its API from its next restart, leaving the web app to the proxy, or not,
            by default False.

        Returns
        -------
        :class:`HTTPSStateResponse`
            The HTTPS state, with `mode` ``"ownProxy"`` and the proxy in `trustedProxies`.

        Raises
        ------
        AMPAPIRequestError
            If `address` is neither an IP address nor a network (400, ``"https.error.proxyAddressInvalid"``).

        """
        return await self._request(method="POST", path="/api/https/own-proxy", data={"address": address, "apiOnly": api_only})

    # TODO: Type the reply once AMP is seen answering it live (#3-47.10).
    # Only the refusal for a panel behind its own proxy is known; the reply to a setup that starts isn't.
    async def start_https_setup(self, host_name: str) -> Any:
        """Start AMP's own HTTPS setup, which asks Let's Encrypt for a certificate.

        |coro|

        Endpoint: ``POST /api/https/setup``

        Follow it with :meth:`get_https_setup_status`. Let's Encrypt has to reach the panel, so this can't work on a
        machine only reachable on its own network.

        Parameters
        ----------
        host_name : :class:`str`
            The domain name, which has to point at this panel.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If a proxy from :meth:`set_own_proxy` is set (409, ``"https.error.ownProxyActive"``); clear it with
            :meth:`delete_own_proxy` first.

        """
        return await self._request(method="POST", path="/api/https/setup", data={"hostName": host_name})
