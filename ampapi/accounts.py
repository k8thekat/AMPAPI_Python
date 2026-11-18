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
    from collections.abc import Mapping

    from ._types import (
        DeletedUserResponse,
        InviteRequest,
        InviteResponse,
        InviteTokenResponse,
        PasskeyFlowResponse,
        PasskeyRegisteredResponse,
        PasskeyRegisterRequest,
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
        RoleUpdateRequest,
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

    Taking an invite needs no account yet, so it's :meth:`Session.accept_invite`.

    .. versionadded:: 6.0.0

    """

    async def add_favourite(self, template_slug: str) -> PreferencesResponse:
        """Add a template to the logged in user's favourites.

        |coro|

        Endpoint: ``POST /api/users/me/preferences/favourites/{template_slug}``

        AMP puts the new favourite at the front of the list. Adding a favourite that's already there changes nothing.
        AMP doesn't check that the slug names a template.

        Parameters
        ----------
        template_slug : :class:`str`
            The template's slug, eg. ``"teeworlds"``.

        Returns
        -------
        :class:`PreferencesResponse`
            All of the logged in user's preferences.

        """
        return await self._request(method="POST", path=f"/api/users/me/preferences/favourites/{template_slug}")

    async def add_ssh_key(self, key: str, label: Optional[str] = None, *, expires_at: Optional[str] = None) -> SSHKeyResponse:
        """Add an SSH key to the logged in user's account, for SFTP.

        |coro|

        Endpoint: ``POST /api/profile/sshkeys``

        Parameters
        ----------
        key : :class:`str`
            The public key line, eg. ``"ssh-ed25519 AAAA... laptop"``.
        label : Union[:class:`str`, None], optional
            A name for the key, by default None.
            - Without a label AMP names the key after the key line's comment, eg. ``"laptop"``.
            - A key line with no comment is named after its key type, eg. ``"ssh-ed25519"``.
        expires_at : Union[:class:`str`, None], optional
            When the key stops working, ISO 8601 like ``"2027-01-01T00:00:00Z"``, by default None.
            - Without an expiry the key never runs out.

        Returns
        -------
        :class:`SSHKeyResponse`
            The key AMP added.

        Raises
        ------
        AMPAPIRequestError
            **400** - If AMP doesn't support the key `sshKeys.error.unsupported`.\n
            **400** - If an RSA key is smaller than AMP's minimum size, from AMP's docs and not seen live.\n
            **409** - If the key is already on this account or another account `sshKeys.error.alreadyRegistered`.

        """
        data: SSHKeyRequest = {"key": key, "label": label, "expiresAt": expires_at}
        return await self._request(method="POST", path="/api/profile/sshkeys", data=data)

    async def begin_passkey_registration(self) -> PasskeyFlowResponse:
        """Start adding a passkey to the logged in user's account.

        |coro|

        Endpoint: ``POST /api/profile/passkeys/register/begin``

        The library holds no passkeys. Hand `options` to a WebAuthn authenticator, eg. a browser's
        ``navigator.credentials.create``, then send its answer to :meth:`complete_passkey_registration` with `flowId`.

        .. note::
            Passkeys only work through the panel's public HTTPS address, so the session's `url` has to be that address.
            :meth:`Session.get_capabilities` reads ``"Eligible"`` in `passkeyStatus` there.

        Returns
        -------
        :class:`PasskeyFlowResponse`
            The flow's ID and the WebAuthn creation options.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the session hasn't proved the password or a passkey recently, see :meth:`Session.reauth`. From
            AMP's docs and not seen live.\n
            **409** - If passkeys don't work at the panel's public address. The error's `code` says why. From AMP's
            docs and not seen live.\n
            **429** - If the caller's IP address has too many passkey flows open, from AMP's docs and not seen live.

        """
        return await self._request(method="POST", path="/api/profile/passkeys/register/begin", data={})

    async def complete_passkey_registration(
        self,
        flow_id: str,
        response: Mapping[str, Any],
        *,
        name: str = "",
    ) -> PasskeyRegisteredResponse:
        """Finish adding a passkey with the authenticator's answer to :meth:`begin_passkey_registration`.

        |coro|

        Endpoint: ``POST /api/profile/passkeys/register/complete``

        When the `Session` holds an enrolment-only session (see :attr:`Session.enrolment_only`), AMP ends that session and
        hands over a full session in its place. The `Session` keeps the full session's token.

        .. warning::
            AMP 3.0.0.6 refuses an answer without `transports` in `response["response"]`, and a browser can leave
            `transports` out. Add ``"transports": []`` when the authenticator gives none.

        Parameters
        ----------
        flow_id : :class:`str`
            The `flowId` from :meth:`begin_passkey_registration`.
        response : Mapping[:class:`str`, Any]
            The authenticator's answer, the WebAuthn `PublicKeyCredential` as JSON with base64url values:
            `id`, `rawId`, `type`, `extensions` and `response` (`attestationObject`, `clientDataJSON`, `transports`).
        name : :class:`str`, optional
            A name for the passkey, by default "".

        Returns
        -------
        :class:`PasskeyRegisteredResponse`
            The new passkey, and the full session's token when the `Session` held an enrolment-only session.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `response` has no `transports`. AMP answers with a ProblemDetails naming
            ``Response.Response.Transports``.\n
            **400** - If AMP refuses the attestation. The error's `code` says why. From AMP's docs and not seen live.\n
            **403** - If the session hasn't proved the password or a passkey recently, see :meth:`Session.reauth`. From
            AMP's docs and not seen live.

        """
        data: PasskeyRegisterRequest = {"flowId": flow_id, "response": response, "name": name}
        result: PasskeyRegisteredResponse = await self._request(method="POST", path="/api/profile/passkeys/register/complete", data=data)

        # AMP swaps an enrolment-only session for a full session here, so we keep the new token
        if result["session"] is not None:
            self.session._store_token(data=result["session"])  # pyright: ignore[reportPrivateUsage]
        return result

    async def change_password(self, current_password: str, new_password: str) -> None:
        """Change the logged in user's password.

        |coro|

        Endpoint: ``POST /api/profile/password``

        AMP ends every other session of the logged in user and keeps the current session. The new password is kept for later
        logins.

        - AMP also ends the logged in user's SFTP connections to this spire.
        - A forced password change on the account is cleared.
        - The password's age starts again, for `passwordExpires`.

        Parameters
        ----------
        current_password : :class:`str`
            The logged in user's current password.
        new_password : :class:`str`
            The new password; it has to pass :meth:`Session.get_password_policy`.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `current_password` is wrong `profile.error.wrongPassword`.\n
            **400** - If `new_password` is too weak `profile.error.weakPassword`. The error names only the first rule
            the password fails.

        """
        data: PasswordChangeRequest = {"currentPassword": current_password, "newPassword": new_password}
        await self._request(method="POST", path="/api/profile/password", data=data)
        self.session._keep_password(password=new_password)  # pyright: ignore[reportPrivateUsage]

    async def create_invite(
        self,
        user_name: str,
        role_ids: list[str],
        expires_in_hours: int,
        *,
        display_name: Optional[str] = None,
    ) -> InviteTokenResponse:
        """Invite someone to make an account, see :meth:`Session.accept_invite`.

        |coro|

        Endpoint: ``POST /api/invites``

        Parameters
        ----------
        user_name : :class:`str`
            The username the new account gets.
        role_ids : list[:class:`str`]
            The roles the new account gets; AMP wants at least one role that exists.
        expires_in_hours : :class:`int`
            How long the invite code works for. AMP keeps the value between 1 and 720, so 0 becomes 1.
        display_name : Union[:class:`str`, None], optional
            The new account's display name, by default None.

        Returns
        -------
        :class:`InviteTokenResponse`
            The invite and its code.

        Raises
        ------
        AMPAPIRequestError
            **400** - If no ID in `role_ids` matches a role `access.error.inviteRoleRequired`.\n
            **403** - If a role in `role_ids` carries a permission the logged in user doesn't hold, from AMP's docs and
            not seen live.\n
            **409** - If a user already has `user_name`.\n
            **409** - If an invite for `user_name` is still pending, from AMP's docs and not seen live.

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
            The role's name; no two roles can share a name.
        permissions : list[:class:`str`]
            The permission strings, eg. ``["users.read", "spire.*.shard.*.view"]``; a leading ``-`` denies that
            permission. AMP doesn't check that the permissions exist, so a typo grants nothing.
        description : :class:`str`, optional
            A description of the role, by default "".

        Returns
        -------
        :class:`RoleResponse`
            The new role.

        Raises
        ------
        AMPAPIRequestError
            **400** - If a role already has `name`. The error's `errors` names the role.\n
            **403** - If `permissions` grants a permission the logged in user doesn't hold, from AMP's docs and not seen
            live.

        """
        data: RoleRequest = {"name": name, "description": description, "permissions": permissions}
        return await self._request(method="POST", path="/api/roles", data=data)

    async def create_user(
        self,
        user_name: str,
        password: str,
        *,
        email: Optional[str] = None,
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
        email : Union[:class:`str`, None], optional
            The new user's email address, by default None for a user without an email address.
        display_name : Union[:class:`str`, None], optional
            The new user's display name, by default None.
        role_ids : Union[list[:class:`str`], None], optional
            The roles to give the new user, by default None.
            - A user can have no roles, and AMP drops an ID that matches no role without an error.
        password_expires : :class:`bool`, optional
            If the password runs out after the platform's maximum age or not, by default False.
        require_password_change : :class:`bool`, optional
            If the new user has to change the password at their first login or not, by default False.

        Returns
        -------
        :class:`UserResponse`
            The new user.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the username is taken.\n
            **400** - If the password is too weak. The error's `errors` holds every rule the password fails.

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

        Taking out a favourite that isn't there changes nothing.

        Parameters
        ----------
        template_slug : :class:`str`
            The template's slug, eg. ``"teeworlds"``.

        Returns
        -------
        :class:`PreferencesResponse`
            All of the logged in user's preferences.

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
        """End every session of the logged in user except this session.

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

        AMP wants a recent proof of the password to remove a passkey; call :meth:`Session.reauth` first if AMP answers
        ``"auth.error.recentProofRequired"``.

        Parameters
        ----------
        passkey_id : :class:`str`
            The passkey's `id` from :meth:`get_passkeys`.

        Raises
        ------
        AMPAPIRequestError
            **409** - If the passkey is the only passkey while the passkey policy is ``"Required"``, from AMP's docs and
            not seen live.\n
            **409** - If the passkey is the only way into an account with no password, from AMP's docs and not seen live.

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

        Raises
        ------
        AMPAPIRequestError
            **403** - If the role carries a permission the logged in user doesn't hold, from AMP's docs and not seen live.\n
            **404** - If there's no role with that ID.\n
            **409** - If deleting the role would take permissions away from the logged in user, from AMP's docs and not
            seen live.

        """
        await self._request(method="DELETE", path=f"/api/roles/{role_id}")

    async def delete_ssh_key(self, ssh_key_id: str) -> None:
        """Remove one of the logged in user's SSH keys.

        |coro|

        Endpoint: ``DELETE /api/profile/sshkeys/{ssh_key_id}``

        AMP ends any SFTP session the key opened.

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

        AMP also deletes:

        - The user's passkeys.
        - The user's preferences.
        - Every schedule that runs as the user.

        Parameters
        ----------
        user_id : :class:`str`
            The user's ID.

        Returns
        -------
        :class:`DeletedUserResponse`
            The parts of the clean up that failed, if any. The user is deleted either way.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `user_id` is the logged in user's ID, from AMP's docs and not seen live.\n
            **404** - If there's no user with that ID.

        """
        return await self._request(method="DELETE", path=f"/api/users/{user_id}")

    async def generate_recovery_codes(self) -> RecoveryCodesResponse:
        """Make a new set of recovery codes for the logged in account, for :meth:`Session.second_factor`.

        |coro|

        Endpoint: ``POST /api/profile/recovery-codes``

        AMP wants a recent proof of the password to make new codes. A fresh login counts; later on, call
        :meth:`Session.reauth` first if AMP answers ``"auth.error.recentProofRequired"``.

        .. warning::
            AMP never shows the codes again, so keep them somewhere safe. The new set replaces the old set.

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
            The invites; a revoked invite isn't listed.

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
            The grants, the catalog and the logged in user's role IDs.

        """
        return await self._request(method="GET", path="/api/me/permissions")

    async def get_preferences(self) -> PreferencesResponse:
        """Get the logged in user's web panel preferences.

        |coro|

        Endpoint: ``GET /api/users/me/preferences``

        Returns
        -------
        :class:`PreferencesResponse`
            The preferences; a preference never set is `None`.

        """
        return await self._request(method="GET", path="/api/users/me/preferences")

    async def get_profile(self) -> ProfileResponse:
        """Get the logged in user's account.

        |coro|

        Endpoint: ``GET /api/profile``

        Returns
        -------
        :class:`ProfileResponse`
            The logged in user's ID, names and email.

        """
        return await self._request(method="GET", path="/api/profile")

    async def get_profile_sessions(self) -> list[ProfileSessionResponse]:
        """Get the logged in user's sessions, this session included.

        |coro|

        Endpoint: ``GET /api/profile/sessions``

        Returns
        -------
        list[:class:`ProfileSessionResponse`]
            The sessions, with `isCurrent` set on this session.

        """
        return await self._request(method="GET", path="/api/profile/sessions")

    async def get_recovery_codes_status(self) -> RecoveryCodesStatusResponse:
        """Get how many of the logged in account's recovery codes are left.

        |coro|

        Endpoint: ``GET /api/profile/recovery-codes``

        Returns
        -------
        :class:`RecoveryCodesStatusResponse`
            The codes left out of the set, when the set was made, and if the set is running low.

        """
        return await self._request(method="GET", path="/api/profile/recovery-codes")

    async def get_role(self, role_id: str) -> RoleResponse:
        """Get one role.

        |coro|

        Endpoint: ``GET /api/roles/{role_id}``

        Parameters
        ----------
        role_id : :class:`str`
            The role's ID.

        Returns
        -------
        :class:`RoleResponse`
            The role.

        Raises
        ------
        AMPAPIRequestError
            **404** - If there's no role with that ID.\n
            **404** - If the ID names the hidden role AMP keeps for each user, from AMP's docs and not seen live.

        """
        return await self._request(method="GET", path=f"/api/roles/{role_id}")

    async def get_roles(self) -> list[RoleResponse]:
        """Get the roles. A fresh panel has no roles.

        |coro|

        Endpoint: ``GET /api/roles``

        Returns
        -------
        list[:class:`RoleResponse`]
            The roles by name, ignoring case. The hidden role AMP keeps for each user isn't listed.

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
            The users by username.

        """
        return await self._request(method="GET", path="/api/users")

    async def logout_user(self, user_id: str) -> None:
        """End every session of a user.

        |coro|

        Endpoint: ``POST /api/users/{user_id}/logout``

        Ending the logged in user's sessions ends this session too; the next call logs in again.
        The user can log straight back in.

        Parameters
        ----------
        user_id : :class:`str`
            The user's ID.

        """
        await self._request(method="POST", path=f"/api/users/{user_id}/logout", data={})

    async def rearm_invite(self, invite_id: str, expires_in_hours: Optional[int] = None) -> InviteTokenResponse:
        """Give an invite a new code, which stops the old code from working.

        |coro|

        Endpoint: ``POST /api/invites/{invite_id}/rearm``

        The logged in user becomes the invite's creator.

        Parameters
        ----------
        invite_id : :class:`str`
            The invite's ID.
        expires_in_hours : Union[:class:`int`, None], optional
            How long the new code works for, by default None for AMP's 72 hours.
            - AMP keeps the value between 1 and 720.

        Returns
        -------
        :class:`InviteTokenResponse`
            The invite and its new code.

        Raises
        ------
        AMPAPIRequestError
            **400** - If none of the invite's roles exist any more, from AMP's docs and not seen live.\n
            **404** - If there's no invite with that ID.\n
            **409** - If the invite was already accepted.

        """
        # With no body AMP uses its own default lifetime
        data: Optional[dict[str, int]] = None if expires_in_hours is None else {"expiresInHours": expires_in_hours}
        return await self._request(method="POST", path=f"/api/invites/{invite_id}/rearm", data=data)

    async def reset_user_password(self, user_id: str, new_password: str) -> None:
        """Set a user's password, which ends every session they have.

        |coro|

        Endpoint: ``POST /api/users/{user_id}/reset-password``

        Resetting the logged in user's password keeps the new password for later logins.

        - AMP also ends the user's SFTP connections.
        - A forced password change on the account stays in place, so the new password can be a temporary password.

        Parameters
        ----------
        user_id : :class:`str`
            The user's ID.
        new_password : :class:`str`
            The new password; it has to pass :meth:`Session.get_password_policy`.

        """
        await self._request(method="POST", path=f"/api/users/{user_id}/reset-password", data={"newPassword": new_password})

        if user_id == self.session.user_id:
            self.session._keep_password(password=new_password)  # pyright: ignore[reportPrivateUsage]

    async def set_passkey_name(self, passkey_id: str, name: str) -> None:
        """Rename one of the logged in user's passkeys.

        |coro|

        Endpoint: ``PATCH /api/profile/passkeys/{passkey_id}``

        Parameters
        ----------
        passkey_id : :class:`str`
            The passkey's `id` from :meth:`get_passkeys`.
        name : :class:`str`
            The new name. AMP trims the name and keeps its first 64 characters, and takes an empty name as ``""``.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the passkey isn't one of the logged in user's passkeys.

        """
        await self._request(method="PATCH", path=f"/api/profile/passkeys/{passkey_id}", data={"name": name})

    async def update_preferences(self, values: PreferencesChanges) -> PreferencesResponse:
        """Change some of the logged in user's web panel preferences.

        |coro|

        Endpoint: ``PATCH /api/users/me/preferences``

        .. note::
            AMP ignores a preference name it doesn't know.

        Parameters
        ----------
        values : :class:`PreferencesChanges`
            The preferences to change, named as in :class:`PreferencesResponse`, eg. ``{"theme": "dark"}``.


        Returns
        -------
        :class:`PreferencesResponse`
            All of the logged in user's preferences.

        """
        return await self._request(method="PATCH", path="/api/users/me/preferences", data=values)

    async def update_profile(self, display_name: Optional[str] = None, *, email: Optional[str] = None) -> ProfileResponse:
        """Change the logged in user's display name and email. Anything left as `None` stays as it is.

        |coro|

        Endpoints: ``GET /api/profile`` when `display_name` is `None`, then ``PUT /api/profile``

        AMP clears the display name whenever the body leaves it out, so with `display_name` as `None` we read the
        current display name first and send it back. Pass ``""`` to clear the display name.

        Parameters
        ----------
        display_name : Union[:class:`str`, None], optional
            The new display name, ``""`` to clear it, by default None.
        email : Union[:class:`str`, None], optional
            The new email address, by default None. AMP doesn't check that the value is an email address.

        Returns
        -------
        :class:`ProfileResponse`
            The logged in user's account.

        Raises
        ------
        AMPAPIRequestError
            **400** - If another account already has `email`, from AMP's docs and not seen live.

        """
        if display_name is None:
            display_name = (await self.get_profile())["displayName"]
        data: ProfileRequest = {"displayName": display_name}

        if email is not None:
            data["email"] = email

        return await self._request(method="PUT", path="/api/profile", data=data)

    async def update_role(
        self,
        role_id: str,
        name: Optional[str] = None,
        permissions: Optional[list[str]] = None,
        *,
        description: Optional[str] = None,
    ) -> RoleResponse:
        """Change a role's name, description and permissions. Anything left as `None` stays as it is.

        |coro|

        Endpoint: ``PUT /api/roles/{role_id}``

        Parameters
        ----------
        role_id : :class:`str`
            The role's ID.
        name : Union[:class:`str`, None], optional
            The role's new name, by default None.
        permissions : Union[list[:class:`str`], None], optional
            The permission strings, which replace the role's old permissions, by default None.
            - A leading ``-`` denies that permission.
            - An empty list removes every permission.
        description : Union[:class:`str`, None], optional
            The role's new description, ``""`` to clear it, by default None.

        Returns
        -------
        :class:`RoleResponse`
            The changed role.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the change adds or removes a permission the logged in user doesn't hold, from AMP's docs and
            not seen live.\n
            **404** - If there's no role with that ID.\n
            **409** - If the change would take permissions away from the logged in user, from AMP's docs and not seen
            live.

        """
        data: RoleUpdateRequest = {"name": name, "description": description, "permissions": permissions}

        # We only send what changes. AMP keeps a value that's left out.
        return await self._request(method="PUT", path=f"/api/roles/{role_id}", data=self._without_none(mapping=data))

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
            The new display name, ``""`` to clear it, by default None.
        email : Union[:class:`str`, None], optional
            The new email address, by default None. AMP doesn't check that the value is an email address.
        role_ids : Union[list[:class:`str`], None], optional
            The roles to give the user, which replace their old roles, by default None.
            - An empty list removes every role.
        suspended : Union[:class:`bool`, None], optional
            If the user is suspended or not, by default None.
            - Suspending a user ends their sessions, and those sessions stay ended once the user is let back in.
        password_expires : Union[:class:`bool`, None], optional
            If the password runs out after the platform's maximum age or not, by default None.
        require_password_change : Union[:class:`bool`, None], optional
            If the user has to change their password at their next login or not, by default None.
            - Turning `require_password_change` on ends the user's sessions, SFTP included, the same way suspending
              does.

        Returns
        -------
        :class:`UserResponse`
            The changed user.

        Raises
        ------
        AMPAPIRequestError
            **404** - If there's no user with that ID.\n
            **409** - If the change would take permissions away from the logged in user, from AMP's docs and not seen
            live.

        """
        data: UserUpdateRequest = {
            "displayName": display_name,
            "email": email,
            "roleIds": role_ids,
            "suspended": suspended,
            "passwordExpires": password_expires,
            "requirePasswordChange": require_password_change,
        }

        # We only send what changes. AMP keeps a value that's left out.
        return await self._request(method="PUT", path=f"/api/users/{user_id}", data=self._without_none(mapping=data))
