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
    from ._types import PermissionsResponse, ProfileResponse, RecoveryCodesResponse, RecoveryCodesStatusResponse

__all__ = ("AccountModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class AccountModule(Base):
    """The calls for user accounts, starting with the logged in user's own.

    .. versionadded:: 6.0.0

    """

    # TODO: Add the users, roles, invites and the rest of the profile calls (#47.9).

    async def generate_recovery_codes(self) -> RecoveryCodesResponse:
        """Make a new set of recovery codes for the logged in account, for :meth:`Session.second_factor`.

        |coro|

        Endpoint: ``POST /api/profile/recovery-codes``

        AMP wants a recent proof of the password for this. A fresh login counts; later on, call :meth:`Session.reauth`
        first if AMP answers ``"auth.error.recentProofRequired"``.

        .. warning::
            A new set replaces the old one, and AMP never shows the codes again. Keep them somewhere safe.

        Returns
        -------
        :class:`RecoveryCodesResponse`
            The new codes.

        """
        return await self._request(method="POST", path="/api/profile/recovery-codes", data={})

    async def get_permissions(self) -> PermissionsResponse:
        """Get the logged in user's grants, along with every permission AMP knows about.

        |coro|

        Endpoint: ``GET /api/me/permissions``

        Returns
        -------
        :class:`PermissionsResponse`
            The grants, the catalog and the user's role IDs.

        """
        return await self._request(method="GET", path="/api/me/permissions")

    async def get_profile(self) -> ProfileResponse:
        """Get the logged in user's own account.

        |coro|

        Endpoint: ``GET /api/profile``

        Returns
        -------
        :class:`ProfileResponse`
            The user's ID, names and email.

        """
        return await self._request(method="GET", path="/api/profile")

    async def get_recovery_codes_status(self) -> RecoveryCodesStatusResponse:
        """Get how many of the logged in account's recovery codes are left.

        |coro|

        Endpoint: ``GET /api/profile/recovery-codes``

        Returns
        -------
        :class:`RecoveryCodesStatusResponse`
            The codes left out of the set, when it was made, and if it is running low.

        """
        return await self._request(method="GET", path="/api/profile/recovery-codes")
