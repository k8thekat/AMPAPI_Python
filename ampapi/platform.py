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
from typing import TYPE_CHECKING, Any, Optional, Union

from .base import Base

if TYPE_CHECKING:
    from ._types import (
        BrandingResponse,
        DiagnosticsResponse,
        FirewallResponse,
        GatewayEligibilityResponse,
        HealthStatusResponse,
        HTTPSSetupStatusResponse,
        HTTPSStateResponse,
        LicenceAgreementResponse,
        LicenceQueryResponse,
        LicenceResponse,
        LicenceStatusResponse,
        LicenceTermsAcceptance,
        MessageBusStatsResponse,
        MonitoringThresholdsResponse,
        SettingsManifestResponse,
        SystemBusResponse,
        UpdateStatusResponse,
    )

__all__ = ("PlatformModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class PlatformModule(Base):
    """The panel-wide calls: health, branding, licences, settings, HTTPS, networking, monitoring, updates and support.

    .. versionadded:: 6.0.0

    """

    # TODO: The diagnostics bundle download, which comes back as a zip (#47.7's raw replies).

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The body comes from the web panel's code; no capture shows the response yet.
    async def accept_licence_terms(self, spire_id: str, grade_id: str, key: str, terms: LicenceTermsAcceptance) -> Any:
        """Accept the terms for a licence that is already active, eg. one whose `standing` is ``"TermsRequired"``.

        |coro|

        Endpoint: ``POST /api/licence/{spire_id}/{grade_id}/terms``

        Parameters
        ----------
        spire_id : :class:`str`
            The licence's `spireId`.
        grade_id : :class:`str`
            The licence's `gradeId`.
        key : :class:`str`
            The licence key; a wrong one gets its own error code.
        terms : :class:`LicenceTermsAcceptance`
            The terms acceptance, filled from :meth:`get_licence_agreement`.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        data: dict[str, Any] = {**terms, "key": key}
        return await self._request(method="POST", path=f"/api/licence/{spire_id}/{grade_id}/terms", data=data)

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The web panel reads the warnings that are left from it; no capture shows the response yet.
    async def acknowledge_platform_warning(self, warning_id: str) -> Any:
        """Dismiss one of the panel's warnings.

        |coro|

        Endpoint: ``POST /api/monitoring/platform-warnings/acknowledge``

        Parameters
        ----------
        warning_id : :class:`str`
            The warning's `id` from :meth:`get_platform_warnings`.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path="/api/monitoring/platform-warnings/acknowledge", data={"id": warning_id})

    async def activate_licence(self, key: str, *, terms: Optional[LicenceTermsAcceptance] = None) -> LicenceResponse:
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
        terms : Union[:class:`LicenceTermsAcceptance`, None], optional
            The licence terms acceptance, by default None.
            Only a key whose `LicenceQueryResponse.termsRequired` is `True` needs one, see :meth:`query_licence`.
            Sending one is not yet seen live.

        Returns
        -------
        :class:`LicenceResponse`
            The licence AMP activated.

        """
        return await self._request(method="POST", path="/api/licence", data={"key": key, "terms": terms})

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The body comes from the web panel's code; no capture shows the response yet.
    async def apply_panel_update(self) -> Any:
        """Update the panel's AMP to the latest version on its stream; the panel restarts.

        |coro|

        Endpoint: ``POST /api/updates/apply``

        The web panel then watches :meth:`get_health_status` and :meth:`get_update_status` while the panel restarts.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path="/api/updates/apply", data={})

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The body comes from the web panel's code; no capture shows the response yet.
    async def check_https(self, host_name: str) -> Any:
        """Check a domain name is ready for AMP's own HTTPS setup, before :meth:`start_https_setup`.

        |coro|

        Endpoint: ``POST /api/https/check``

        Parameters
        ----------
        host_name : :class:`str`
            The domain name, which has to point at this panel.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path="/api/https/check", data={"hostName": host_name})

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The body comes from the web panel's code; it needs a second spire to capture.
    async def create_gateway(self, shard_id: str, front_spire_id: str) -> Any:
        """Bind a shard to a front spire, so players reach it through that spire.

        |coro|

        Endpoint: ``POST /api/networking/gateways``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        front_spire_id : :class:`str`
            The front spire's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        data: dict[str, Any] = {"shardId": shard_id, "frontSpireId": front_spire_id}
        return await self._request(method="POST", path="/api/networking/gateways", data=data)

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The body comes from the web panel's code; it needs a second spire to capture.
    async def create_publication(self, front_spire_id: str, public_port: int, shard_id: str, port_reference: str) -> Any:
        """Forward a public port on a front spire to a shard's port.

        |coro|

        Endpoint: ``POST /api/networking/publications``

        Parameters
        ----------
        front_spire_id : :class:`str`
            The front spire's ID.
        public_port : :class:`int`
            The port players connect to.
        shard_id : :class:`str`
            The shard's ID.
        port_reference : :class:`str`
            The shard port's name in its template, eg. ``"ServerPort"``.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        data: dict[str, Any] = {"frontSpireId": front_spire_id, "publicPort": public_port, "shardId": shard_id, "portRef": port_reference}
        return await self._request(method="POST", path="/api/networking/publications", data=data)

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The path comes from the web panel's code; it needs a second spire to capture.
    async def delete_gateway(self, gateway_id: str) -> Any:
        """Remove a gateway.

        |coro|

        Endpoint: ``DELETE /api/networking/gateways/{gateway_id}``

        Parameters
        ----------
        gateway_id : :class:`str`
            The gateway's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="DELETE", path=f"/api/networking/gateways/{gateway_id}")

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The path comes from the web panel's code; no capture shows the response yet.
    async def delete_licence(self, spire_id: str, grade_id: str) -> Any:
        """Remove a licence from the panel.

        |coro|

        Endpoint: ``DELETE /api/licence/{spire_id}/{grade_id}``

        Parameters
        ----------
        spire_id : :class:`str`
            The licence's `spireId`.
        grade_id : :class:`str`
            The licence's `gradeId`.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="DELETE", path=f"/api/licence/{spire_id}/{grade_id}")

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The path comes from the web panel's code; the POST to it answers with the HTTPS state.
    async def delete_own_proxy(self) -> Any:
        """Stop trusting the reverse proxy :meth:`set_own_proxy` set.

        |coro|

        Endpoint: ``DELETE /api/https/own-proxy``

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="DELETE", path="/api/https/own-proxy")

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The path comes from the web panel's code; it needs a second spire to capture.
    async def delete_publication(self, publication_id: str) -> Any:
        """Remove a public port forward.

        |coro|

        Endpoint: ``DELETE /api/networking/publications/{publication_id}``

        Parameters
        ----------
        publication_id : :class:`str`
            The publication's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="DELETE", path=f"/api/networking/publications/{publication_id}")

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The path comes from the web panel's code; no capture shows the response yet.
    async def delete_setting_secret(self, field_name: str) -> Any:
        """Clear a stored secret setting.

        |coro|

        Endpoint: ``DELETE /api/settings/secrets/{field_name}``

        Parameters
        ----------
        field_name : :class:`str`
            The setting's `fieldName`, one in `SettingsManifestResponse.secretHasValue`.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="DELETE", path=f"/api/settings/secrets/{field_name}")

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The body comes from the web panel's code; no capture shows the response yet.
    async def expand_message_bus(self) -> Any:
        """Open the message bus to other machines, which a new spire needs to join.

        |coro|

        Endpoint: ``POST /api/system/bus/expand``

        .. warning::
            It changes how the panel is reached, and there's no call to close the bus again.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path="/api/system/bus/expand")

    async def get_branding(self) -> BrandingResponse:
        """Get the names and logo the login page shows.

        |coro|

        Endpoint: ``GET /api/branding``

        Returns
        -------
        :class:`BrandingResponse`
            The product name, welcome text, logo and default theme.

        """
        return await self._request(method="GET", path="/api/branding")

    async def get_diagnostics(self) -> DiagnosticsResponse:
        """Get the details a support request asks for.

        |coro|

        Endpoint: ``GET /api/support/diagnostics``

        Returns
        -------
        :class:`DiagnosticsResponse`
            AMP's version, the machine, the message bus and the container runtime.

        """
        return await self._request(method="GET", path="/api/support/diagnostics")

    async def get_firewall(self) -> FirewallResponse:
        """Get the firewall rules AMP keeps on the host.

        |coro|

        Endpoint: ``GET /api/networking/firewall``

        Returns
        -------
        :class:`FirewallResponse`
            The rules applied and anything held back.

        """
        return await self._request(method="GET", path="/api/networking/firewall")

    async def get_gateway_eligibility(self) -> GatewayEligibilityResponse:
        """Get the shards and front spires that can take part in a gateway.

        |coro|

        Endpoint: ``GET /api/networking/gateway-eligibility``

        Returns
        -------
        :class:`GatewayEligibilityResponse`
            The shard and front spire IDs.

        """
        return await self._request(method="GET", path="/api/networking/gateway-eligibility")

    # TODO: Type the items once AMP is seen listing one live (#47.10).
    # Only seen empty, as a gateway needs a second spire.
    async def get_gateways(self) -> list[dict[str, Any]]:
        """Get the gateways, each binding a shard to a front spire.

        |coro|

        Endpoint: ``GET /api/networking/gateways``

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The gateways.

        """
        return await self._request(method="GET", path="/api/networking/gateways")

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

    async def get_licence_agreement(self, version: int, *, language: Optional[str] = None) -> LicenceAgreementResponse:
        """Get the licence terms a key may need accepted.

        |coro|

        Endpoint: ``GET /api/licence/terms/agreement``

        Parameters
        ----------
        version : :class:`int`
            The terms version, a licence's `requiredTermsVersion`. An unknown one gets 404
            (``"licence.error.termsUnknownVersion"``).
        language : Union[:class:`str`, None], optional
            The language to read them in, eg. ``"fr"``, by default None.
            AMP sends English when it has no copy in that language.

        Returns
        -------
        :class:`LicenceAgreementResponse`
            The terms, with the hash and attestation a :class:`LicenceTermsAcceptance` sends back.

        """
        parameters: dict[str, Union[str, int]] = {"version": version}
        if language is not None:
            parameters["lang"] = language

        return await self._request(method="GET", path="/api/licence/terms/agreement", parameters=parameters)

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

    async def get_message_bus(self) -> SystemBusResponse:
        """Get the state of the message bus spires talk to the panel over.

        |coro|

        Endpoint: ``GET /api/system/bus``

        Returns
        -------
        :class:`SystemBusResponse`
            If AMP runs the bus, if it's public and how to join it.

        """
        return await self._request(method="GET", path="/api/system/bus")

    async def get_message_bus_stats(self) -> MessageBusStatsResponse:
        """Get the message bus's figures, for support.

        |coro|

        Endpoint: ``GET /api/support/message-bus-stats``

        Returns
        -------
        :class:`MessageBusStatsResponse`
            The bus's state, storage and process.

        """
        return await self._request(method="GET", path="/api/support/message-bus-stats")

    async def get_monitoring_thresholds(self) -> MonitoringThresholdsResponse:
        """Get when the web panel warns about load, from the monitoring settings.

        |coro|

        Endpoint: ``GET /api/monitoring/thresholds``

        Returns
        -------
        :class:`MonitoringThresholdsResponse`
            The processor, memory and disk limits.

        """
        return await self._request(method="GET", path="/api/monitoring/thresholds")

    # TODO: Type the items once AMP is seen listing one live (#47.10).
    # Only seen empty; the web panel reads each one's `id`.
    async def get_platform_warnings(self) -> list[dict[str, Any]]:
        """Get the panel's warnings for whoever runs it.

        |coro|

        Endpoint: ``GET /api/monitoring/platform-warnings``

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The warnings.

        """
        return await self._request(method="GET", path="/api/monitoring/platform-warnings")

    # TODO: Type the items once AMP is seen listing one live (#47.10).
    # Only seen empty, as a publication needs a second spire.
    async def get_publications(self) -> list[dict[str, Any]]:
        """Get the public port forwards from front spires to shards.

        |coro|

        Endpoint: ``GET /api/networking/publications``

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The publications.

        """
        return await self._request(method="GET", path="/api/networking/publications")

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

    # TODO: Type the items once AMP is seen listing one live (#47.10).
    # Only seen empty, as a tunnel front needs a second spire.
    async def get_tunnel_fronts(self) -> list[dict[str, Any]]:
        """Get the spires that can front a tunnel.

        |coro|

        Endpoint: ``GET /api/networking/tunnel-fronts``

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The tunnel fronts.

        """
        return await self._request(method="GET", path="/api/networking/tunnel-fronts")

    # TODO: Type the items once AMP is seen listing one live (#47.10).
    # Only seen empty, as a tunnel needs a second spire.
    async def get_tunnels(self) -> list[dict[str, Any]]:
        """Get the network tunnels between spires.

        |coro|

        Endpoint: ``GET /api/networking/tunnels``

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The tunnels.

        """
        return await self._request(method="GET", path="/api/networking/tunnels")

    async def get_update_status(self) -> UpdateStatusResponse:
        """Get the panel's AMP version against the latest one.

        |coro|

        Endpoint: ``GET /api/updates/check``

        Returns
        -------
        :class:`UpdateStatusResponse`
            The versions, the release stream and what can be updated.

        """
        return await self._request(method="GET", path="/api/updates/check")

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The web panel reads a `conflicts` list from it; it needs a second spire to capture.
    async def preflight_gateway(self, shard_id: str, front_spire_id: str) -> Any:
        """Check a gateway can be made, before :meth:`create_gateway`.

        |coro|

        Endpoint: ``POST /api/networking/gateways/preflight``

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        front_spire_id : :class:`str`
            The front spire's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        data: dict[str, Any] = {"shardId": shard_id, "frontSpireId": front_spire_id}
        return await self._request(method="POST", path="/api/networking/gateways/preflight", data=data)

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

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The path comes from the web panel's code; no capture shows the response yet.
    async def recheck_https(self) -> Any:
        """Check AMP's own HTTPS again, eg. its certificate.

        |coro|

        Endpoint: ``POST /api/https/recheck``

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path="/api/https/recheck")

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
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

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The web panel reads a `detail` text from it; no capture shows the response yet.
    async def run_setting_action(self, action_id: str) -> Any:
        """Run one of the settings page's buttons, eg. sending a test email.

        |coro|

        Endpoint: ``POST /api/settings/actions/{action_id}``

        Parameters
        ----------
        action_id : :class:`str`
            The action's `id` from `SettingsManifestResponse.actions`, eg. ``"smtp.test"``.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="POST", path=f"/api/settings/actions/{action_id}")

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

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The web panel reads the new update status from it, likely an `UpdateStatusResponse`; not captured yet.
    async def set_update_stream(self, stream: str) -> Any:
        """Move the panel to another release stream.

        |coro|

        Endpoint: ``PUT /api/updates/stream``

        Parameters
        ----------
        stream : :class:`str`
            One of `UpdateStatusResponse.availableStreams`, eg. ``"Mainline"`` or ``"Preview"``.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="PUT", path="/api/updates/stream", data={"stream": stream})

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The body comes from the web panel's code; a LAN panel can't finish it, so no capture shows the response yet.
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

        """
        return await self._request(method="POST", path="/api/https/setup", data={"hostName": host_name})

    # TODO: Type the reply once AMP is seen answering it live (#47.10).
    # The body comes from the web panel's code; it needs a second spire to capture.
    async def update_publication(self, publication_id: str, *, enabled: Optional[bool] = None, public_port: Optional[int] = None) -> Any:
        """Turn a public port forward on or off, or move it to another port.

        |coro|

        Endpoint: ``PUT /api/networking/publications/{publication_id}``

        The web panel sends one change at a time.

        Parameters
        ----------
        publication_id : :class:`str`
            The publication's ID.
        enabled : Union[:class:`bool`, None], optional
            If the forward is on or not, by default None.
        public_port : Union[:class:`int`, None], optional
            The new public port, by default None.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        data: dict[str, Any] = {"enabled": enabled, "publicPort": public_port}
        # We only send what changes, as the web panel does.
        data = {key: value for key, value in data.items() if value is not None}
        return await self._request(method="PUT", path=f"/api/networking/publications/{publication_id}", data=data)
