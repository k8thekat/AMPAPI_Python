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
        HealthStatusResponse,
        HTTPSCheckResponse,
        HTTPSSetupStatusResponse,
        HTTPSStateResponse,
        LicenceAgreementResponse,
        LicenceQueryResponse,
        LicenceResponse,
        LicenceStatusResponse,
        LicenceTermsAcceptance,
        LicenceTermsRequest,
        MessageBusStatsResponse,
        MonitoringThresholdsResponse,
        SettingActionResponse,
        SettingsManifestResponse,
        SettingValues,
        UpdateStatusResponse,
    )

__all__ = ("PlatformModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class PlatformModule(Base):
    """The panel-wide calls: health, branding, licences, settings, HTTPS, monitoring, updates and support.

    Networking is :class:`NetworkModule`, and the message bus a new spire joins over is :class:`EnrollmentModule`.

    .. versionadded:: 6.0.0

    """

    # TODO: Type the reply once AMP is seen answering it live (#3-47.10).
    # Only refusals are known; the reply to accepted terms isn't.
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
            The licence key.
        terms : :class:`LicenceTermsAcceptance`
            The terms acceptance, filled from :meth:`get_licence_agreement`.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If the licence needs no terms (400, ``"licence.error.termsNotApplicable"``), which is the case when
            :meth:`query_licence` reads `termsRequired` as `False`. A wrong `key` gets 502
            (``"licence.error.termsUnavailable"``), as AMP asks the licensing service before it checks the key.

        """
        data: LicenceTermsRequest = {**terms, "key": key}
        return await self._request(method="POST", path=f"/api/licence/{spire_id}/{grade_id}/terms", data=data)

    # TODO: Reword the docstring once AMP refuses an unknown warning ID (U20a).
    # AMP 3.0.0.6 answers 200 with the warnings as they are.
    # TODO: Type the items once AMP is seen listing one live (#3-47.10).
    # The item shape isn't known yet; the items are those of `get_platform_warnings`.
    async def acknowledge_platform_warning(self, warning_id: str) -> list[dict[str, Any]]:
        """Dismiss one of the panel's warnings.

        |coro|

        Endpoint: ``POST /api/monitoring/platform-warnings/acknowledge``

        An unknown `warning_id` is not an error; AMP answers with the warnings as they are.

        Parameters
        ----------
        warning_id : :class:`str`
            The warning's `id` from :meth:`get_platform_warnings`.

        Returns
        -------
        list[dict[:class:`str`, Any]]
            The warnings left, as :meth:`get_platform_warnings` lists them.

        """
        return await self._request(method="POST", path="/api/monitoring/platform-warnings/acknowledge", data={"id": warning_id})

    # TODO: Drop the note once AMP answers with the whole licence (U19b).
    # AMP 3.0.0.6 answers before the licence service does, with the limit, totals, issue date and terms all `None`.
    async def activate_licence(self, key: str, *, terms: Optional[LicenceTermsAcceptance] = None) -> LicenceResponse:
        """Activate a licence key on this panel.

        |coro|

        Endpoint: ``POST /api/licence``

        .. note::
            The reply comes back before the licence service answers, so its `shardLimit`, `keyShardsTotal`, `issuedAt`
            and terms versions are `None` and `limitKnown` is `False`. :meth:`get_licence_status` has them a few
            seconds later.

        The panel can restart once licensed: :meth:`get_health_status` reads ``"starting"`` until it is ``"ready"``
        again, and a setting read before then can look unapplied.

        Parameters
        ----------
        key : :class:`str`
            The licence key.
        terms : Union[:class:`LicenceTermsAcceptance`, None], optional
            The licence terms acceptance, by default None.
            Only a key whose `LicenceQueryResponse.termsRequired` is `True` needs one, see :meth:`query_licence`.

        Returns
        -------
        :class:`LicenceResponse`
            The licence AMP activated (201).

        """
        return await self._request(method="POST", path="/api/licence", data={"key": key, "terms": terms})

    # TODO: Type the reply once AMP is seen answering it live (#3-47.10).
    # Only the refusal for no newer version is known; the reply to a real update isn't.
    async def apply_panel_update(self) -> Any:
        """Update the panel's AMP to the latest version on its stream; the panel restarts.

        |coro|

        Endpoint: ``POST /api/updates/apply``

        The web panel then watches :meth:`get_health_status` and :meth:`get_update_status` while the panel restarts.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If there's no newer version on the stream (400, ``"updates.error.noUpdate"``); nothing restarts then.

        """
        return await self._request(method="POST", path="/api/updates/apply", data={})

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

    async def delete_licence(self, spire_id: str, grade_id: str) -> None:
        """Remove a licence from the panel.

        |coro|

        Endpoint: ``DELETE /api/licence/{spire_id}/{grade_id}``

        With no licence left, :meth:`get_health_status` reads ``"preview-licence"`` until one is activated again.

        Parameters
        ----------
        spire_id : :class:`str`
            The licence's `spireId`.
        grade_id : :class:`str`
            The licence's `gradeId`.

        Raises
        ------
        AMPAPIRequestError
            If the panel has no such licence, eg. it was removed already (404).

        """
        await self._request(method="DELETE", path=f"/api/licence/{spire_id}/{grade_id}")

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

    async def delete_setting_secret(self, field_name: str) -> None:
        """Clear a stored secret setting.

        |coro|

        Endpoint: ``DELETE /api/settings/secrets/{field_name}``

        Clearing one that holds no value is fine too.

        Parameters
        ----------
        field_name : :class:`str`
            The setting's `fieldName`, one in `SettingsManifestResponse.secretHasValue`.

        Raises
        ------
        AMPAPIRequestError
            If there's no such setting (400, ``"settings.error.unknownNode"``) or it isn't a secret
            (400, ``"settings.error.notASecret"``).

        """
        await self._request(method="DELETE", path=f"/api/settings/secrets/{field_name}")

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

    async def get_diagnostics_bundle(self) -> bytes:
        """Get the diagnostics bundle a support request asks for, a zip of logs and details.

        |coro|

        Endpoint: ``GET /api/support/diagnostics/bundle``

        AMP sends it as an attachment named ``"amp-diagnostics-<yyyymmdd-hhmmss>.zip"``, a few KB.

        Returns
        -------
        :class:`bytes`
            The zip as it came.

        """
        return await self._request(method="GET", path="/api/support/diagnostics/bundle", raw_bytes=True)

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

    # TODO: Type the items once AMP is seen listing one live (#3-47.10).
    # The item shape isn't known yet; the web panel reads each one's `id`.
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

    async def run_setting_action(self, action_id: str) -> SettingActionResponse:
        """Run one of the settings page's buttons, eg. sending a test email.

        |coro|

        Endpoint: ``POST /api/settings/actions/{action_id}``

        Parameters
        ----------
        action_id : :class:`str`
            The action's `id` from `SettingsManifestResponse.actions`, eg. ``"templates.sync"``.

        Returns
        -------
        :class:`SettingActionResponse`
            What the action did, as a sentence.

        Raises
        ------
        AMPAPIRequestError
            If there's no such action (400, ``"settings.error.unknownAction"``) or the action failed, eg. Steam
            refused the key that ``"steam-key.check"`` tests (400, ``"settings.analytics.error.steamKeyRejected"``).

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

    async def set_settings(self, values: SettingValues) -> None:
        """Change one or more platform settings.

        |coro|

        Endpoint: ``POST /api/settings/values``

        Parameters
        ----------
        values : :class:`SettingValues`
            Each setting's `SettingSpec.fieldName` to its new value, a string like the manifest's values,
            eg. ``{"public-address.publicUrl": "https://amp.example.com"}``. A secret setting takes its value here
            too; the manifest then shows it in `secretHasValue`, never the value.

        Raises
        ------
        AMPAPIRequestError
            If there's no such setting (400, ``"settings.error.unknownNode"``) or a value doesn't fit it
            (400, ``"settings.error.invalidValue"``).

        """
        await self._request(method="POST", path="/api/settings/values", data=values)

    async def set_update_stream(self, stream: str) -> UpdateStatusResponse:
        """Move the panel to another release stream.

        |coro|

        Endpoint: ``PUT /api/updates/stream``

        Parameters
        ----------
        stream : :class:`str`
            One of `UpdateStatusResponse.availableStreams`, eg. ``"Mainline"`` or ``"Preview"``, in any case.

        Returns
        -------
        :class:`UpdateStatusResponse`
            The update status on the new stream. A stream with no build yet has an empty `latestVersion` and the
            `note` ``"updates.error.streamMissing"``.

        Raises
        ------
        AMPAPIRequestError
            If the panel can't follow that stream (400, ``"updates.error.streamInvalid"``).

        """
        return await self._request(method="PUT", path="/api/updates/stream", data={"stream": stream})

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
