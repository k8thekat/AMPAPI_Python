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
from typing import TYPE_CHECKING

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

        It changes nothing. A name that isn't a domain name is answered rather than refused, with `outcome`
        ``"invalid"``.

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
    # As of AMP 3.0.1 the reads still show the proxy in `GET /api/https` and the passkey capabilities for a few seconds.
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

    # TODO: Check the reply against a live capture; AMP's OpenAPI alone says the 202 has no body (#3-47.10, #3-56.2al).
    # Only the refusal for a panel without AMP's own HTTPS is known; a recheck needs AMP's own HTTPS set up.
    async def recheck_https(self) -> None:
        """Check AMP's own HTTPS again for its certificate.

        |coro|

        Endpoint: ``POST /api/https/recheck``

        AMP answers at once (202); follow the recheck with :meth:`get_https_setup_status`.

        Raises
        ------
        AMPAPIRequestError
            **409** - If AMP's own HTTPS isn't set up `https.error.notConfigured`. A proxy from :meth:`set_own_proxy`
            doesn't count.\n
            **409** - If a setup is running.

        """
        await self._request(method="POST", path="/api/https/recheck")

    # TODO: Check the reply against a live capture; typed from AMP's OpenAPI `HttpsState` alone (#3-47.10, #3-56.2al).
    # Removing AMP's own HTTPS needs it set up first, which Let's Encrypt can't give the test VMs.
    async def remove_https(self) -> HTTPSStateResponse:
        """Remove AMP's own HTTPS; the panel stays on plain HTTP at its own port.

        |coro|

        Endpoint: ``POST /api/https/remove``

        AMP's system agent puts Caddy's old configuration back, or stops Caddy, and closes the ports.

        Returns
        -------
        :class:`HTTPSStateResponse`
            The HTTPS state after.

        Raises
        ------
        AMPAPIRequestError
            **409** - If AMP's own HTTPS isn't set up.\n
            **409** - If a setup is running.\n
            **409** - If the system agent couldn't remove AMP's own HTTPS.

        """
        return await self._request(method="POST", path="/api/https/remove")

    async def set_own_proxy(self, address: str, *, api_only: bool = False) -> HTTPSStateResponse:
        """Trust a reverse proxy in front of the panel, such as Caddy or nginx.

        |coro|

        Endpoint: ``POST /api/https/own-proxy``

        AMP then takes the forwarded headers from that address, so sign-ins and audit entries carry each visitor's real
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
            **400** - If `address` is neither an IP nor a network `https.error.proxyAddressInvalid`.\n
            **409** - If AMP's own HTTPS is set up.

        """
        return await self._request(method="POST", path="/api/https/own-proxy", data={"address": address, "apiOnly": api_only})

    # TODO: Check the reply against a live capture; AMP's OpenAPI alone says the 202 has no body (#3-47.10, #3-56.2al).
    # Only the refusal for a panel behind its own proxy is known; a setup that starts needs Let's Encrypt to reach the VM.
    async def start_https_setup(self, host_name: str) -> None:
        """Start AMP's own HTTPS setup, which asks Let's Encrypt for a certificate.

        |coro|

        Endpoint: ``POST /api/https/setup``

        AMP answers at once (202) and runs the checks in the background; follow the setup with
        :meth:`get_https_setup_status`. Let's Encrypt has to reach the panel, so the setup can't work on a machine only
        reachable on its own network.

        Parameters
        ----------
        host_name : :class:`str`
            The domain name, which has to point at this panel, see :meth:`check_https`.

        Raises
        ------
        AMPAPIRequestError
            **400** - If no certificate can be issued for `host_name`.\n
            **409** - If a proxy from :meth:`set_own_proxy` is set `https.error.ownProxyActive`. Clear the proxy with
            :meth:`delete_own_proxy` first.\n
            **409** - If the panel is a public entry node.\n
            **409** - If the panel is kept out of AMP's firewall.\n
            **409** - If a setup is already running.

        """
        await self._request(method="POST", path="/api/https/setup", data={"hostName": host_name})
