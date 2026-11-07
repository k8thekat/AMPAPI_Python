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
        DeletedUserResponse,
        InviteAcceptedResponse,
        InviteAcceptRequest,
        InvitePreviewResponse,
        InviteRequest,
        InviteResponse,
        InviteTokenResponse,
        PasskeyResponse,
        PasswordChangeRequest,
        PermissionsResponse,
        PreferencesChanges,
        PreferencesResponse,
        ProfileRequest,
        ProfileResponse,
        ProfileSessionResponse,
        RecoveryCodesResponse,
        RecoveryCodesStatusResponse,
        RevokedSessionsResponse,
        RoleRequest,
        RoleResponse,
        SSHKeyRequest,
        SSHKeyResponse,
        UserCreateRequest,
        UserResponse,
        UserUpdateRequest,
    )

__all__ = ("AccountModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class AccountModule(Base):
    """The calls for user accounts: users, roles, invites and the logged in user's own profile.

    .. versionadded:: 6.0.0

    """

    async def accept_invite(
        self,
        token: str,
        email: str,
        password: str,
        *,
        display_name: Optional[str] = None,
        locale: str = "en",
    ) -> InviteAcceptedResponse:
        """Make the account an invite was for, which logs it in.

        |coro|

        Endpoint: ``POST /api/invites/accept``

        This one needs no session. The account's username is the one the invite was made with, see
        :meth:`preview_invite`.

        .. note::
            The reply's token is a live session for the new account, and we don't keep it.
            To use the account, make a new :class:`Session` with its username and `password`.

        Parameters
        ----------
        token : :class:`str`
            The invite code from :meth:`create_invite` or :meth:`rearm_invite`.
        email : :class:`str`
            The new account's email address.
        password : :class:`str`
            The new account's password; it has to pass :meth:`Session.get_password_policy`.
        display_name : Union[:class:`str`, None], optional
            The new account's display name, by default None.
        locale : :class:`str`, optional
            The new account's language, by default "en".

        Returns
        -------
        :class:`InviteAcceptedResponse`
            The new account's session token.

        Raises
        ------
        AMPAPIRequestError
            If the code is wrong, used, revoked or out of date (410, ``"invalid_or_expired"``), or the password is too
            weak (400).

        """
        data: InviteAcceptRequest = {"token": token, "email": email, "password": password, "displayName": display_name, "locale": locale}
        return await self._request(method="POST", path="/api/invites/accept", data=data, use_token=False)

    async def add_favourite(self, template_slug: str) -> PreferencesResponse:
        """Add a template to the logged in user's favourites.

        |coro|

        Endpoint: ``POST /api/users/me/preferences/favourites/{template_slug}``

        Adding one already there changes nothing. AMP doesn't check the slug is a template.

        Parameters
        ----------
        template_slug : :class:`str`
            The template's slug, eg. ``"teeworlds"``.

        Returns
        -------
        :class:`PreferencesResponse`
            All of the user's preferences.

        """
        return await self._request(method="POST", path=f"/api/users/me/preferences/favourites/{template_slug}")

    async def add_ssh_key(self, key: str, label: str, *, expires_at: Optional[str] = None) -> SSHKeyResponse:
        """Add an SSH key to the logged in user's account, for SFTP.

        |coro|

        Endpoint: ``POST /api/profile/sshkeys``

        Parameters
        ----------
        key : :class:`str`
            The public key line, eg. ``"ssh-ed25519 AAAA... laptop"``.
        label : :class:`str`
            A name for the key.
        expires_at : Union[:class:`str`, None], optional
            When the key stops working, ISO 8601 like ``"2027-01-01T00:00:00Z"``, by default None.
            Without one it never runs out.

        Returns
        -------
        :class:`SSHKeyResponse`
            The key AMP added.

        Raises
        ------
        AMPAPIRequestError
            If the key is already added (409, ``"sshKeys.error.alreadyRegistered"``) or isn't one AMP supports
            (400, ``"sshKeys.error.unsupported"``).

        """
        data: SSHKeyRequest = {"key": key, "label": label, "expiresAt": expires_at}
        return await self._request(method="POST", path="/api/profile/sshkeys", data=data)

    async def change_password(self, current_password: str, new_password: str) -> None:
        """Change the logged in user's password.

        |coro|

        Endpoint: ``POST /api/profile/password``

        AMP ends every other session of the user and keeps this one. The new password is kept for later logins.

        Parameters
        ----------
        current_password : :class:`str`
            The password the user has now.
        new_password : :class:`str`
            The new password; it has to pass :meth:`Session.get_password_policy`.

        Raises
        ------
        AMPAPIRequestError
            If `current_password` is wrong (400, ``"profile.error.wrongPassword"``) or `new_password` is too weak
            (400, ``"profile.error.weakPassword"``, naming only the first rule it fails).

        """
        data: PasswordChangeRequest = {"currentPassword": current_password, "newPassword": new_password}
        await self._request(method="POST", path="/api/profile/password", data=data)
        self.session._password = new_password  # pyright: ignore[reportPrivateUsage]

    async def create_invite(
        self,
        user_name: str,
        role_ids: list[str],
        expires_in_hours: int,
        *,
        display_name: Optional[str] = None,
    ) -> InviteTokenResponse:
        """Invite someone to make an account, see :meth:`accept_invite`.

        |coro|

        Endpoint: ``POST /api/invites``

        Parameters
        ----------
        user_name : :class:`str`
            The username the new account gets.
        role_ids : list[:class:`str`]
            The roles the new account gets; AMP wants at least one that exists.
        expires_in_hours : :class:`int`
            How long the invite code works for. AMP turns 0 into 1.
        display_name : Union[:class:`str`, None], optional
            The new account's display name, by default None.

        Returns
        -------
        :class:`InviteTokenResponse`
            The invite and its code.

        Raises
        ------
        AMPAPIRequestError
            If no role in `role_ids` exists (400, ``"access.error.inviteRoleRequired"``), or a user already has
            `user_name` (409).

        """
        data: InviteRequest = {"userName": user_name, "displayName": display_name, "roleIds": role_ids, "expiresInHours": expires_in_hours}
        return await self._request(method="POST", path="/api/invites", data=data)

    async def create_role(self, name: str, permissions: list[str], *, description: str = "") -> RoleResponse:
        """Make a role.

        |coro|

        Endpoint: ``POST /api/roles``

        Parameters
        ----------
        name : :class:`str`
            The role's name; no two roles can share one.
        permissions : list[:class:`str`]
            The permission strings, eg. ``["users.read", "spire.*.shard.*.view"]``; a leading ``-`` denies one.
            AMP doesn't check that they exist, so a typo grants nothing.
        description : :class:`str`, optional
            A description of the role, by default "".

        Returns
        -------
        :class:`RoleResponse`
            The new role.

        """
        data: RoleRequest = {"name": name, "description": description, "permissions": permissions}
        return await self._request(method="POST", path="/api/roles", data=data)

    async def create_user(
        self,
        user_name: str,
        password: str,
        email: str,
        *,
        display_name: Optional[str] = None,
        role_ids: Optional[list[str]] = None,
        password_expires: bool = False,
        require_password_change: bool = False,
    ) -> UserResponse:
        """Make a user.

        |coro|

        Endpoint: ``POST /api/users``

        Parameters
        ----------
        user_name : :class:`str`
            The new user's username.
        password : :class:`str`
            The new user's password; it has to pass :meth:`Session.get_password_policy`.
        email : :class:`str`
            The new user's email address.
        display_name : Union[:class:`str`, None], optional
            The new user's display name, by default None.
        role_ids : Union[list[:class:`str`], None], optional
            The roles to give the user, by default None.
            A user can have none, and AMP drops an ID that isn't a role.
        password_expires : :class:`bool`, optional
            If the password runs out after the platform's maximum age or not, by default False.
        require_password_change : :class:`bool`, optional
            If the user has to change the password at their first login or not, by default False.

        Returns
        -------
        :class:`UserResponse`
            The new user.

        Raises
        ------
        AMPAPIRequestError
            If the username is taken, or the password is too weak (400, with every rule it fails in `errors`).

        """
        data: UserCreateRequest = {
            "userName": user_name,
            "password": password,
            "displayName": display_name,
            "email": email,
            "roleIds": role_ids if role_ids is not None else [],
            "passwordExpires": password_expires,
            "requirePasswordChange": require_password_change,
        }

        return await self._request(method="POST", path="/api/users", data=data)

    async def delete_favourite(self, template_slug: str) -> PreferencesResponse:
        """Take a template out of the logged in user's favourites.

        |coro|

        Endpoint: ``DELETE /api/users/me/preferences/favourites/{template_slug}``

        Taking out one that isn't there changes nothing.

        Parameters
        ----------
        template_slug : :class:`str`
            The template's slug, eg. ``"teeworlds"``.

        Returns
        -------
        :class:`PreferencesResponse`
            All of the user's preferences.

        """
        return await self._request(method="DELETE", path=f"/api/users/me/preferences/favourites/{template_slug}")

    async def delete_invite(self, invite_id: str) -> None:
        """Revoke an invite, so its code stops working.

        |coro|

        Endpoint: ``DELETE /api/invites/{invite_id}``

        Parameters
        ----------
        invite_id : :class:`str`
            The invite's ID.

        """
        await self._request(method="DELETE", path=f"/api/invites/{invite_id}")

    async def delete_other_profile_sessions(self) -> RevokedSessionsResponse:
        """End every session of the logged in user except this one.

        |coro|

        Endpoint: ``DELETE /api/profile/sessions/others``

        Returns
        -------
        :class:`RevokedSessionsResponse`
            How many sessions AMP ended.

        """
        return await self._request(method="DELETE", path="/api/profile/sessions/others")

    async def delete_passkey(self, passkey_id: str) -> None:
        """Remove one of the logged in user's passkeys.

        |coro|

        Endpoint: ``DELETE /api/profile/passkeys/{passkey_id}``

        AMP wants a recent proof of the password for this; call :meth:`Session.reauth` first if AMP answers
        ``"auth.error.recentProofRequired"``.

        Parameters
        ----------
        passkey_id : :class:`str`
            The passkey's `id` from :meth:`get_passkeys`.

        """
        await self._request(method="DELETE", path=f"/api/profile/passkeys/{passkey_id}")

    async def delete_profile_session(self, session_id: str) -> None:
        """End one of the logged in user's sessions.

        |coro|

        Endpoint: ``DELETE /api/profile/sessions/{session_id}``

        Parameters
        ----------
        session_id : :class:`str`
            The session's `id` from :meth:`get_profile_sessions`.

        """
        await self._request(method="DELETE", path=f"/api/profile/sessions/{session_id}")

    async def delete_role(self, role_id: str) -> None:
        """Delete a role.

        |coro|

        Endpoint: ``DELETE /api/roles/{role_id}``

        .. warning::
            AMP deletes a role that users still hold, and their `roleIds` keep the dead ID.

        Parameters
        ----------
        role_id : :class:`str`
            The role's ID.

        """
        await self._request(method="DELETE", path=f"/api/roles/{role_id}")

    async def delete_ssh_key(self, ssh_key_id: str) -> None:
        """Remove one of the logged in user's SSH keys.

        |coro|

        Endpoint: ``DELETE /api/profile/sshkeys/{ssh_key_id}``

        Parameters
        ----------
        ssh_key_id : :class:`str`
            The key's `id` from :meth:`get_ssh_keys`.

        """
        await self._request(method="DELETE", path=f"/api/profile/sshkeys/{ssh_key_id}")

    async def delete_user(self, user_id: str) -> DeletedUserResponse:
        """Delete a user; their sessions stop working.

        |coro|

        Endpoint: ``DELETE /api/users/{user_id}``

        Parameters
        ----------
        user_id : :class:`str`
            The user's ID.

        Returns
        -------
        :class:`DeletedUserResponse`
            Any warnings AMP had about the delete.

        """
        return await self._request(method="DELETE", path=f"/api/users/{user_id}")

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

    async def get_invites(self) -> list[InviteResponse]:
        """Get the invites, pending and accepted.

        |coro|

        Endpoint: ``GET /api/invites``

        Returns
        -------
        list[:class:`InviteResponse`]
            The invites; a revoked one isn't listed.

        """
        return await self._request(method="GET", path="/api/invites")

    async def get_passkeys(self) -> list[PasskeyResponse]:
        """Get the logged in user's passkeys.

        |coro|

        Endpoint: ``GET /api/profile/passkeys``

        Returns
        -------
        list[:class:`PasskeyResponse`]
            The passkeys.

        """
        return await self._request(method="GET", path="/api/profile/passkeys")

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

    async def get_preferences(self) -> PreferencesResponse:
        """Get the logged in user's web panel preferences.

        |coro|

        Endpoint: ``GET /api/users/me/preferences``

        Returns
        -------
        :class:`PreferencesResponse`
            The preferences; one never set is `None`.

        """
        return await self._request(method="GET", path="/api/users/me/preferences")

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

    async def get_profile_sessions(self) -> list[ProfileSessionResponse]:
        """Get the logged in user's sessions, this one included.

        |coro|

        Endpoint: ``GET /api/profile/sessions``

        Returns
        -------
        list[:class:`ProfileSessionResponse`]
            The sessions, with `isCurrent` set on this one.

        """
        return await self._request(method="GET", path="/api/profile/sessions")

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

    async def get_roles(self) -> list[RoleResponse]:
        """Get the roles. A fresh panel has none.

        |coro|

        Endpoint: ``GET /api/roles``

        Returns
        -------
        list[:class:`RoleResponse`]
            The roles.

        """
        return await self._request(method="GET", path="/api/roles")

    async def get_ssh_keys(self) -> list[SSHKeyResponse]:
        """Get the logged in user's SSH keys.

        |coro|

        Endpoint: ``GET /api/profile/sshkeys``

        Returns
        -------
        list[:class:`SSHKeyResponse`]
            The keys.

        """
        return await self._request(method="GET", path="/api/profile/sshkeys")

    async def get_user(self, user_id: str) -> UserResponse:
        """Get one user.

        |coro|

        Endpoint: ``GET /api/users/{user_id}``

        Parameters
        ----------
        user_id : :class:`str`
            The user's ID.

        Returns
        -------
        :class:`UserResponse`
            The user.

        """
        return await self._request(method="GET", path=f"/api/users/{user_id}")

    async def get_users(self) -> list[UserResponse]:
        """Get every user.

        |coro|

        Endpoint: ``GET /api/users``

        Returns
        -------
        list[:class:`UserResponse`]
            The users.

        """
        return await self._request(method="GET", path="/api/users")

    async def logout_user(self, user_id: str) -> None:
        """End every session of a user.

        |coro|

        Endpoint: ``POST /api/users/{user_id}/logout``

        Ending our own user's sessions ends this one too; the next call logs in again.

        Parameters
        ----------
        user_id : :class:`str`
            The user's ID.

        """
        await self._request(method="POST", path=f"/api/users/{user_id}/logout", data={})

    async def preview_invite(self, token: str) -> InvitePreviewResponse:
        """Get who an invite code is for, without using it.

        |coro|

        Endpoint: ``POST /api/invites/preview``

        This one needs no session.

        Parameters
        ----------
        token : :class:`str`
            The invite code.

        Returns
        -------
        :class:`InvitePreviewResponse`
            The username and display name the account will get.

        Raises
        ------
        AMPAPIRequestError
            If the code is wrong, used, revoked or out of date (404, ``"invalid_or_expired"``).

        """
        return await self._request(method="POST", path="/api/invites/preview", data={"token": token}, use_token=False)

    async def rearm_invite(self, invite_id: str, expires_in_hours: int) -> InviteTokenResponse:
        """Give an invite a new code, which stops the old one working.

        |coro|

        Endpoint: ``POST /api/invites/{invite_id}/rearm``

        Parameters
        ----------
        invite_id : :class:`str`
            The invite's ID.
        expires_in_hours : :class:`int`
            How long the new code works for.

        Returns
        -------
        :class:`InviteTokenResponse`
            The invite and its new code.

        Raises
        ------
        AMPAPIRequestError
            If the invite was already accepted (409).

        """
        return await self._request(method="POST", path=f"/api/invites/{invite_id}/rearm", data={"expiresInHours": expires_in_hours})

    async def reset_user_password(self, user_id: str, new_password: str) -> None:
        """Set a user's password, which ends every session they have.

        |coro|

        Endpoint: ``POST /api/users/{user_id}/reset-password``

        Resetting our own user's password keeps the new one for later logins.

        Parameters
        ----------
        user_id : :class:`str`
            The user's ID.
        new_password : :class:`str`
            The new password; it has to pass :meth:`Session.get_password_policy`.

        """
        await self._request(method="POST", path=f"/api/users/{user_id}/reset-password", data={"newPassword": new_password})

        if user_id == self.session.user_id:
            self.session._password = new_password  # pyright: ignore[reportPrivateUsage]

    # TODO: Type the reply once AMP is seen answering it live (#3-47.9).
    # The body comes from the web panel's code; no capture shows the response yet.
    async def set_passkey_name(self, passkey_id: str, name: str) -> Any:
        """Rename one of the logged in user's passkeys.

        |coro|

        Endpoint: ``PATCH /api/profile/passkeys/{passkey_id}``

        Parameters
        ----------
        passkey_id : :class:`str`
            The passkey's `id` from :meth:`get_passkeys`.
        name : :class:`str`
            The new name.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        """
        return await self._request(method="PATCH", path=f"/api/profile/passkeys/{passkey_id}", data={"name": name})

    async def update_preferences(self, values: PreferencesChanges) -> PreferencesResponse:
        """Change some of the logged in user's web panel preferences.

        |coro|

        Endpoint: ``PATCH /api/users/me/preferences``

        Parameters
        ----------
        values : :class:`PreferencesChanges`
            The preferences to change, named as in :class:`PreferencesResponse`, eg. ``{"theme": "dark"}``.
            AMP ignores a name it doesn't know.

        Returns
        -------
        :class:`PreferencesResponse`
            All of the user's preferences.

        """
        return await self._request(method="PATCH", path="/api/users/me/preferences", data=values)

    async def update_profile(self, display_name: Optional[str], *, email: Optional[str] = None) -> ProfileResponse:
        """Change the logged in user's display name and email.

        |coro|

        Endpoint: ``PUT /api/profile``

        .. note::
            AMP treats the two differently: `None` clears the display name, but leaves the email as it is.

        Parameters
        ----------
        display_name : Union[:class:`str`, None]
            The new display name, or `None` to clear it.
        email : Union[:class:`str`, None], optional
            The new email address, by default None.
            Without one the email stays as it is. AMP doesn't check it's an email address.

        Returns
        -------
        :class:`ProfileResponse`
            The user's account.

        """
        data: ProfileRequest = {"displayName": display_name}

        if email is not None:
            data["email"] = email

        return await self._request(method="PUT", path="/api/profile", data=data)

    async def update_role(self, role_id: str, name: str, permissions: list[str], *, description: str = "") -> RoleResponse:
        """Change a role's name, description and permissions.

        |coro|

        Endpoint: ``PUT /api/roles/{role_id}``

        Parameters
        ----------
        role_id : :class:`str`
            The role's ID.
        name : :class:`str`
            The role's name.
        permissions : list[:class:`str`]
            The permission strings, which replace the old ones; a leading ``-`` denies one.
        description : :class:`str`, optional
            A description of the role, by default "".

        Returns
        -------
        :class:`RoleResponse`
            The role.

        """
        data: RoleRequest = {"name": name, "description": description, "permissions": permissions}
        return await self._request(method="PUT", path=f"/api/roles/{role_id}", data=data)

    async def update_user(
        self,
        user_id: str,
        *,
        display_name: Optional[str] = None,
        email: Optional[str] = None,
        role_ids: Optional[list[str]] = None,
        suspended: Optional[bool] = None,
        password_expires: Optional[bool] = None,
        require_password_change: Optional[bool] = None,
    ) -> UserResponse:
        """Change a user. Anything left as `None` stays as it is.

        |coro|

        Endpoint: ``PUT /api/users/{user_id}``

        Parameters
        ----------
        user_id : :class:`str`
            The user's ID.
        display_name : Union[:class:`str`, None], optional
            The new display name, by default None.
        email : Union[:class:`str`, None], optional
            The new email address, by default None. AMP doesn't check it's an email address.
        role_ids : Union[list[:class:`str`], None], optional
            The roles the user has, which replace the old ones, by default None. An empty list takes them all away.
        suspended : Union[:class:`bool`, None], optional
            If the user is suspended or not, by default None.
            Suspending ends their sessions, and they stay ended once the user is let back in.
        password_expires : Union[:class:`bool`, None], optional
            If the password runs out after the platform's maximum age or not, by default None.
        require_password_change : Union[:class:`bool`, None], optional
            If the user has to change the password at their next login or not, by default None.

        Returns
        -------
        :class:`UserResponse`
            The user.

        """
        data: UserUpdateRequest = {
            "displayName": display_name,
            "email": email,
            "roleIds": role_ids,
            "suspended": suspended,
            "passwordExpires": password_expires,
            "requirePasswordChange": require_password_change,
        }

        # We only send what changes, AMP keeps a value that's left out.
        return await self._request(method="PUT", path=f"/api/users/{user_id}", data=self._without_none(mapping=data))
