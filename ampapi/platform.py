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
        BrandingResponse,
        DiagnosticsResponse,
        HealthStatusResponse,
        MessageBusStatsResponse,
        MonitoringThresholdsResponse,
        PlatformWarningResponse,
        SettingActionResponse,
        SettingsManifestResponse,
        SettingsSaveResponse,
        SettingValues,
        UpdateStatusResponse,
    )

__all__ = ("PlatformModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class PlatformModule(Base):
    """The panel-wide calls: health, branding, settings, monitoring, updates and support.

    Licences are :class:`LicenceModule`, HTTPS is :class:`HTTPSModule`, networking is :class:`NetworkModule`, and the
    message bus a new spire joins over is :class:`EnrollmentModule`.

    .. versionadded:: 6.0.0

    """

    # TODO: Reword the docstring once AMP refuses an unknown warning ID (U20a).
    # AMP 3.0.0.6 answers 200 with the warnings as they are.
    async def acknowledge_platform_warning(self, warning_id: str) -> list[PlatformWarningResponse]:
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
        list[:class:`PlatformWarningResponse`]
            The warnings left, as :meth:`get_platform_warnings` lists them.

        Raises
        ------
        AMPAPIRequestError
            If the warning needs action and can't be dismissed, its `dismissable` False
            (400, ``"platform.error.warningNotDismissable"``, its `params` holding the warning's `code`).

        """
        return await self._request(method="POST", path="/api/monitoring/platform-warnings/acknowledge", data={"id": warning_id})

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

    async def get_platform_warnings(self) -> list[PlatformWarningResponse]:
        """Get the panel's warnings for whoever runs it, eg. a spire whose IPv6 goes nowhere.

        |coro|

        Endpoint: ``GET /api/monitoring/platform-warnings``

        A spire that's offline isn't one of these; see :meth:`Panel.get_spire_roster` for that.

        Returns
        -------
        list[:class:`PlatformWarningResponse`]
            The warnings, empty when there are none.

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

    # TODO: Type the notices once AMP is seen sending one live (#3-51.7).
    # Every save so far answered 204; the web panel shows each notice as a save error.
    async def set_settings(self, values: SettingValues) -> list[Any]:
        """Change one or more platform settings.

        |coro|

        Endpoint: ``POST /api/settings/values``

        A save that went through only in part answers with `notices` saying what didn't happen, eg. ports 80 and 443
        left open; a full save answers with nothing.

        Parameters
        ----------
        values : :class:`SettingValues`
            Each setting's `SettingSpec.fieldName` to its new value, a string like the manifest's values,
            eg. ``{"public-address.publicUrl": "https://amp.example.com"}``. A secret setting takes its value here
            too; the manifest then shows it in `secretHasValue`, never the value.

        Returns
        -------
        list[Any]
            AMP's notices, empty for a save that went through whole.

        Raises
        ------
        AMPAPIRequestError
            If there's no such setting (400, ``"settings.error.unknownNode"``) or a value doesn't fit it
            (400, ``"settings.error.invalidValue"``).

        """
        result: Optional[SettingsSaveResponse] = await self._request(method="POST", path="/api/settings/values", data=values)
        # A full save is an empty 204, so there's no reply to read
        return result["notices"] if result is not None else []

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
