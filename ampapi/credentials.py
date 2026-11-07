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
    from ._types import CredentialKind, CredentialRequest, CredentialResponse, CredentialVisibility

__all__ = ("CredentialModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class CredentialModule(Base):
    """The calls for stored secrets that shards can use, such as a Steam login.

    AMP never sends a secret back once it's stored.

    .. versionadded:: 6.0.0

    """

    async def create_credential(
        self,
        kind: CredentialKind,
        title: str,
        username: str,
        secret: str,
        *,
        visibility: Optional[CredentialVisibility] = None,
    ) -> CredentialResponse:
        """Store a secret for shards to use.

        |coro|

        Endpoint: ``POST /api/credentials``

        Parameters
        ----------
        kind : :class:`CredentialKind`
            What it's for: ``"SteamCmd"``, ``"Smtp"``, ``"DiscordWebhook"`` or ``"ApiKey"``.
        title : :class:`str`
            A name for it.
        username : :class:`str`
            The account name that goes with the secret.
        secret : :class:`str`
            The secret itself, eg. a password.
        visibility : Union[:class:`CredentialVisibility`, None], optional
            ``"Private"`` or ``"Public"``, by default None. Without one AMP makes it ``"Private"``.

        Returns
        -------
        :class:`CredentialResponse`
            The credential, without its secret.

        """
        data: CredentialRequest = {"kind": kind, "title": title, "username": username, "secret": secret}

        if visibility is not None:
            data["visibility"] = visibility

        return await self._request(method="POST", path="/api/credentials", data=data)

    async def delete_credential(self, credential_id: str) -> None:
        """Delete a stored secret.

        |coro|

        Endpoint: ``DELETE /api/credentials/{credential_id}``

        Parameters
        ----------
        credential_id : :class:`str`
            The credential's ID.

        """
        await self._request(method="DELETE", path=f"/api/credentials/{credential_id}")

    async def get_credentials(self) -> list[CredentialResponse]:
        """Get the stored secrets the logged in user can see, without the secrets themselves.

        |coro|

        Endpoint: ``GET /api/credentials``

        Returns
        -------
        list[:class:`CredentialResponse`]
            The credentials.

        """
        return await self._request(method="GET", path="/api/credentials")

    async def set_credential_secret(self, credential_id: str, secret: str) -> None:
        """Replace a credential's secret.

        |coro|

        Endpoint: ``PUT /api/credentials/{credential_id}/secret``

        Parameters
        ----------
        credential_id : :class:`str`
            The credential's ID.
        secret : :class:`str`
            The new secret.

        Raises
        ------
        AMPAPIRequestError
            If AMP refuses the secret (400, ``"credentials.error.invalid"``), eg. an empty one.

        """
        await self._request(method="PUT", path=f"/api/credentials/{credential_id}/secret", data={"secret": secret})

    async def set_credential_visibility(self, credential_id: str, visibility: CredentialVisibility) -> None:
        """Set who can see and use a credential.

        |coro|

        Endpoint: ``PUT /api/credentials/{credential_id}/visibility``

        Parameters
        ----------
        credential_id : :class:`str`
            The credential's ID.
        visibility : :class:`CredentialVisibility`
            ``"Private"`` or ``"Public"``.

        """
        await self._request(method="PUT", path=f"/api/credentials/{credential_id}/visibility", data={"visibility": visibility})
