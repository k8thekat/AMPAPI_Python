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
from typing import TYPE_CHECKING, Optional

from .base import Base

if TYPE_CHECKING:
    from ._types import (
        BrandingResponse,
        CodedErrorResponse,
        DiagnosticsResponse,
        HealthStatusResponse,
        MessageBusStatsResponse,
        MonitoringThresholdsResponse,
        PanelUpdateResponse,
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
    # As of AMP 3.0.1 an unknown ID is still answered 200 with the warnings as they are.
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
            **400** - If the warning needs action and can't be dismissed `platform.error.warningNotDismissable`. The
            warning's `dismissable` is `False`, and the error's `params` holds the warning's `code`.

        """
        return await self._request(method="POST", path="/api/monitoring/platform-warnings/acknowledge", data={"id": warning_id})

    # As of AMP 3.0.2 the update's task still can't be read through the Tasks API (upstream U34).
    async def apply_panel_update(self) -> PanelUpdateResponse:
        """Update the panel's AMP to the latest version on its stream; the panel restarts.

        |coro|

        Endpoint: ``POST /api/updates/apply``

        AMP tells every other spire to follow. Shards keep running.

        The reply's `taskId` can't be followed, as :meth:`TaskModule.get_task` answers 404 for the task before and after
        the restart. Watch :meth:`get_health_status` and :meth:`get_update_status` instead, as the web panel does.

        - :meth:`get_health_status` can still read ``"ready"`` on the old version at once, then the panel answers nothing
          for about 10 seconds.
        - :meth:`get_health_status` reads ``"starting"`` on the new version about 15 seconds after the call, and
          ``"ready"`` about 20 seconds after it.

        Returns
        -------
        :class:`PanelUpdateResponse`
            The update's task ID.

        Raises
        ------
        AMPAPIRequestError
            **400** - If there's no newer version on the stream `updates.error.noUpdate`. Nothing restarts.\n
            **400** - If AMP doesn't run under its supervisor, see `UpdateStatusResponse.supervised`.\n
            **400** - If the new version fails its checks.

        """
        return await self._request(method="POST", path="/api/updates/apply", data={})

    async def delete_setting_secret(self, field_name: str) -> None:
        """Clear a stored secret setting.

        |coro|

        Endpoint: ``DELETE /api/settings/secrets/{field_name}``

        Clearing a secret setting that holds no value is fine too.

        Parameters
        ----------
        field_name : :class:`str`
            The setting's `fieldName`, one of the names in `SettingsManifestResponse.secretHasValue`.

        Raises
        ------
        AMPAPIRequestError
            **400** - If there's no setting with that name `settings.error.unknownNode`.\n
            **400** - If the setting isn't a secret `settings.error.notASecret`.

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

        AMP sends the bundle as an attachment named ``"amp-diagnostics-<yyyymmdd-hhmmss>.zip"``, a few KB.

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

        This call needs no session, so it works before anyone logs in.

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

        AMP measures the round trip on the call. With no connection to the bus AMP answers an empty shell, not an
        error.

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
        """Get the panel's warnings for whoever runs the panel, eg. a spire whose IPv6 goes nowhere.

        |coro|

        Endpoint: ``GET /api/monitoring/platform-warnings``

        An offline spire isn't a platform warning; see :meth:`Panel.get_spire_roster` for offline spires. The warnings
        cover the message bus running without credentials or its storage not answering, and an update that failed or
        was taken back.

        Returns
        -------
        list[:class:`PlatformWarningResponse`]
            The warnings the logged in user hasn't dismissed, empty when there are no warnings. A user who can't change
            the platform settings always gets an empty list.

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
        """Get the panel's AMP version against the latest version.

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
            **400** - If there's no action with that ID `settings.error.unknownAction`.\n
            **400** - If the action failed, eg. Steam refused the key that ``"steam-key.check"`` tests
            `settings.analytics.error.steamKeyRejected`.

        """
        return await self._request(method="POST", path=f"/api/settings/actions/{action_id}")

    # TODO: Check the notices against a live capture; AMP's OpenAPI alone says each is an `ApiError` (#3-51.7, #3-56.2ak).
    # Every save so far answered 204; the web panel shows each notice as a save error.
    async def set_settings(self, values: SettingValues) -> list[CodedErrorResponse]:
        """Change one or more platform settings.

        |coro|

        Endpoint: ``POST /api/settings/values``

        A save whose changes stand but where something that follows from them couldn't be done answers with `notices`,
        eg. ports 80 and 443 left open when the panel stops being exposed and AMP's own HTTPS can't be removed; a full
        save answers with nothing. A refused save changes nothing.

        A change to the security policy ends this spire's SFTP sessions for the accounts the new policy puts on hold.

        Parameters
        ----------
        values : :class:`SettingValues`
            Each setting's `SettingSpec.fieldName` to its new value, a string like the manifest's values,
            eg. ``{"public-address.publicUrl": "https://amp.example.com"}``. A secret setting takes its value here
            too; the manifest then shows the secret in `secretHasValue`, never its value. An empty value for a secret
            keeps the stored value; :meth:`delete_setting_secret` clears the secret.

        Returns
        -------
        list[:class:`CodedErrorResponse`]
            AMP's notices, each still to put right; empty for a save that went through whole.

        Raises
        ------
        AMPAPIRequestError
            **400** - If there's no setting with that name `settings.error.unknownNode`.\n
            **400** - If a value doesn't fit its setting `settings.error.invalidValue`.\n
            **400** - If the setting is fixed on this build `settings.error.locked`.\n
            **400** - If the logged in user may not choose that credential `settings.error.credentialNotUsable`.\n
            **409** - If the machine can't take the setting, eg. the panel's exposure on a public entry node.

        """
        result: Optional[SettingsSaveResponse] = await self._request(method="POST", path="/api/settings/values", data=values)
        # A full save is an empty 204, so there's no reply to read
        return result["notices"] if result is not None else []

    async def set_update_stream(self, stream: str) -> UpdateStatusResponse:
        """Move the panel to another release stream.

        |coro|

        Endpoint: ``PUT /api/updates/stream``

        It moves every spire to the stream and installs nothing. Only a version newer than the running one is ever
        offered, so moving to another stream can't go back a version.

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
            **400** - If the panel can't follow that stream `updates.error.streamInvalid`.

        """
        return await self._request(method="PUT", path="/api/updates/stream", data={"stream": stream})
