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

        Any logged in user can store credentials of their own.

        Parameters
        ----------
        kind : :class:`CredentialKind`
            What the credential is for: ``"SteamCmd"``, ``"Smtp"``, ``"DiscordWebhook"`` or ``"ApiKey"``.
        title : :class:`str`
            A name for the credential.
        username : :class:`str`
            The account name that goes with the secret.
        secret : :class:`str`
            The secret itself, eg. a password.
        visibility : Union[:class:`CredentialVisibility`, None], optional
            ``"Private"`` or ``"Public"``, by default None. Without a visibility AMP makes the credential ``"Private"``.

        Returns
        -------
        :class:`CredentialResponse`
            The credential, without its secret.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the title, username or secret isn't valid for the `kind` `credentials.error.invalid`.

        """
        data: CredentialRequest = {"kind": kind, "title": title, "username": username, "secret": secret}

        if visibility is not None:
            data["visibility"] = visibility

        return await self._request(method="POST", path="/api/credentials", data=data)

    async def delete_credential(self, credential_id: str) -> None:
        """Delete a stored secret.

        |coro|

        Endpoint: ``DELETE /api/credentials/{credential_id}``

        Shards that used this credential are left without a credential until their next game update picks a replacement.

        Parameters
        ----------
        credential_id : :class:`str`
            The credential's ID.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the logged in user didn't create the credential and lacks `credentials.manage`.\n
            **404** - If there's no credential with that ID.

        """
        await self._request(method="DELETE", path=f"/api/credentials/{credential_id}")

    async def get_credentials(self) -> list[CredentialResponse]:
        """Get the stored secrets the logged in user can see, without the secrets themselves.

        |coro|

        Endpoint: ``GET /api/credentials``

        Returns
        -------
        list[:class:`CredentialResponse`]
            The credentials, newest first. Only the user who created the credential sees its `username`.

            - The credentials the logged in user created.
            - Every ``"Public"`` credential.
            - Every credential, when the logged in user holds `credentials.manage`.

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
            **400** - If AMP refuses the secret, eg. an empty secret `credentials.error.invalid`.\n
            **403** - If the logged in user didn't create the credential and lacks `credentials.manage`.\n
            **404** - If there's no credential with that ID.

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

        Raises
        ------
        AMPAPIRequestError
            **403** - If the logged in user didn't create the credential and lacks `credentials.manage`.\n
            **404** - If there's no credential with that ID.

        """
        await self._request(method="PUT", path=f"/api/credentials/{credential_id}/visibility", data={"visibility": visibility})
