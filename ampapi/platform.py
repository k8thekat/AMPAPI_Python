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
from typing import TYPE_CHECKING, Any, Optional

from .base import Base

if TYPE_CHECKING:
    from ._types import (
        HealthStatusResponse,
        HTTPSStateResponse,
        LicenceQueryResponse,
        LicenceResponse,
        LicenceStatusResponse,
        SettingsManifestResponse,
    )

__all__ = ("PlatformModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class PlatformModule(Base):
    """The panel-wide calls: health, licences, settings and HTTPS.

    .. versionadded:: 6.0.0

    """

    # TODO: Add branding, networking, monitoring, system, updates, support and the rest of licence and settings (#47.10).

    async def activate_licence(self, key: str, *, terms: Optional[dict[str, Any]] = None) -> LicenceResponse:
        """Activate a licence key on this panel.

        |coro|

        Endpoint: ``POST /api/licence``

        .. note::
            The panel restarts once licensed. :meth:`get_health_status` reads ``"starting"`` until it is ``"ready"``
            again, and a setting read before then can look unapplied.

        Parameters
        ----------
        key : :class:`str`
            The licence key.
        terms : Union[dict[:class:`str`, Any], None], optional
            The licence terms acceptance, by default None.
            Only a key whose `LicenceQueryResponse.termsRequired` is `True` needs one, see :meth:`query_licence`.

        Returns
        -------
        :class:`LicenceResponse`
            The licence AMP activated.

        """
        # TODO: Type `terms` once the terms agreement is captured (#47.10).
        # The web panel builds it from GET /api/licence/terms/agreement: termsVersion, agreementHash, attestation,
        # locale and clickedAt.
        return await self._request(method="POST", path="/api/licence", data={"key": key, "terms": terms})

    async def delete_own_proxy(self) -> Any:
        """Stop trusting the reverse proxy :meth:`set_own_proxy` set.

        |coro|

        Endpoint: ``DELETE /api/https/own-proxy``

        .. warning::
            Not yet seen live, so the shape of AMP's reply is unknown.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="DELETE", path="/api/https/own-proxy")

    async def get_health_status(self) -> HealthStatusResponse:
        """Get the panel's state, eg. still in first-run setup or ``"ready"``.

        |coro|

        Endpoint: ``GET /api/health/status``

        This one needs no session, so it works before anyone logs in.

        Returns
        -------
        :class:`HealthStatusResponse`
            The panel's phase, plus the preview countdown on a preview build.

        """
        return await self._request(method="GET", path="/api/health/status", use_token=False)

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

    async def get_licence_status(self) -> LicenceStatusResponse:
        """Get the panel's licences and how many shards they allow.

        |coro|

        Endpoint: ``GET /api/licence``

        Returns
        -------
        :class:`LicenceStatusResponse`
            The licences, with the shard count and limit.

        """
        return await self._request(method="GET", path="/api/licence")

    async def get_settings_manifest(self) -> SettingsManifestResponse:
        """Get every platform setting with its current value.

        |coro|

        Endpoint: ``GET /api/settings/manifest``

        Returns
        -------
        :class:`SettingsManifestResponse`
            The settings and their values, plus the actions the settings page offers.

        """
        return await self._request(method="GET", path="/api/settings/manifest")

    async def query_licence(self, key: str) -> LicenceQueryResponse:
        """Check what a licence key gives, without activating it.

        |coro|

        Endpoint: ``POST /api/licence/query``

        Parameters
        ----------
        key : :class:`str`
            The licence key.

        Returns
        -------
        :class:`LicenceQueryResponse`
            The key's product, grade and expiry, and if this panel can use it.

        """
        return await self._request(method="POST", path="/api/licence/query", data={"key": key})

    async def set_own_proxy(self, address: str, *, api_only: bool = False) -> HTTPSStateResponse:
        """Trust a reverse proxy in front of the panel, such as Caddy or nginx.

        |coro|

        Endpoint: ``POST /api/https/own-proxy``

        AMP then takes the forwarded headers from that address, so sign-ins and audit entries carry the user's real
        address. Passkeys also need ``"public-address.publicUrl"`` set to the proxy's HTTPS address, see
        :meth:`set_settings`.

        Parameters
        ----------
        address : :class:`str`
            The proxy's address as AMP sees it, eg. ``"127.0.0.1"`` for a proxy on the same machine.
        api_only : :class:`bool`, optional
            If AMP should serve only its API from its next restart, leaving the web app to the proxy, or not,
            by default False.

        Returns
        -------
        :class:`HTTPSStateResponse`
            The HTTPS state, with the proxy in `trustedProxies`.

        """
        return await self._request(method="POST", path="/api/https/own-proxy", data={"address": address, "apiOnly": api_only})

    async def set_settings(self, values: dict[str, str]) -> Optional[dict[str, Any]]:
        """Change one or more platform settings.

        |coro|

        Endpoint: ``POST /api/settings/values``

        Parameters
        ----------
        values : dict[:class:`str`, :class:`str`]
            Each setting's `SettingSpec.fieldName` to its new value, a string like the manifest's values,
            eg. ``{"public-address.publicUrl": "https://amp.example.com"}``.

        Returns
        -------
        Union[dict[:class:`str`, Any], None]
            `None` for the empty 204 AMP sent in every capture so far.
            The web panel reads a `notices` list from a reply with a body, which we haven't seen yet.

        """
        return await self._request(method="POST", path="/api/settings/values", data=values)
