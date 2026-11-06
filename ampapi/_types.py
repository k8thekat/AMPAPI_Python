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

from typing import Any, Literal, Optional, TypedDict, Union

__all__ = (
    "CapabilitiesResponse",
    "CodedErrorResponse",
    "HealthStatusResponse",
    "HubTokenResponse",
    "LoginResponse",
    "MessageErrorResponse",
    "PasskeyRequiredResponse",
    "PasswordChangeRequiredResponse",
    "PasswordPolicyResponse",
    "PermissionNode",
    "PermissionsResponse",
    "PreviewStatus",
    "ProblemDetailsResponse",
    "ProfileResponse",
    "TokenResponse",
    "ValidationErrorResponse",
)


class CapabilitiesResponse(TypedDict):
    """``GET /api/auth/capabilities``, which needs no session."""

    passkeysAvailable: bool
    passkeyStatus: str
    """Seen as ``"NotConfigured"`` on a panel served over plain HTTP."""
    passkeyMessageKey: Optional[str]
    "A translation key for the passkey status, not a message."
    rpId: Optional[str]
    "The WebAuthn relying party ID, `None` until passkeys are configured."
    expectedOrigin: Optional[str]
    passkeyPolicy: str
    """Seen as ``"Optional"``."""


class CodedErrorResponse(TypedDict):
    """The error body AMP builds itself, eg. a wrong `reauth` password or a missing setup code."""

    code: str
    "A dotted translation key, eg. ``auth.error.reproofRejected``."
    params: Optional[dict[str, Any]]
    "Values for the `code` translation; only seen as `None`."
    message: str
    "The English text of `code`."


class HealthStatusResponse(TypedDict):
    """``GET /api/health/status``, which needs no session.

    `phase` runs through the first-run setup (``"setup-database"``, ``"setup-admin"``, ``"preview-licence"``) to ``"ready"``.
    """

    phase: str
    message: Optional[str]
    preview: Optional[PreviewStatus]
    "Set on a preview build."
    messageParams: Optional[dict[str, Any]]
    "Only seen as `None`."
    plainText: bool


class HubTokenResponse(TypedDict):
    """``POST /api/auth/hub-token``, a short lived token for the SignalR hub (about 60 seconds)."""

    token: str
    expiresAt: str


class MessageErrorResponse(TypedDict):
    """The body of a refused ``POST /api/Auth/login`` (401); the same text for a wrong password or an unknown user."""

    message: str


class PasskeyRequiredResponse(TypedDict):
    """A ``POST /api/Auth/login`` answer for an account that needs a second factor; it carries no token.

    .. warning::
        Not yet seen live. The shape is from the web panel's own check, ``passkeyRequired === true``.
        Passkeys need the panel on HTTPS.
    """

    passkeyRequired: Literal[True]


class PasswordChangeRequiredResponse(TypedDict):
    """A ``POST /api/Auth/login`` answer for an account that has to change its password first; it carries no token."""

    passwordChangeRequired: Literal[True]
    reason: str
    """Seen as ``"forced"``, for a user created with `requirePasswordChange`."""


class PasswordPolicyResponse(TypedDict):
    """``GET /api/Auth/password-policy``, which needs no session."""

    requiredLength: int
    requiredUniqueChars: int
    requireUppercase: bool
    requireLowercase: bool
    requireDigit: bool
    requireNonAlphanumeric: bool


class PermissionNode(TypedDict):
    """One permission AMP knows about, from `PermissionsResponse.catalog`."""

    node: str
    "eg. ``power.start``."
    scope: str
    """``"Platform"``, ``"Shard"`` or ``"Spire"``."""
    dangerous: bool
    pathScopable: bool
    byNameOnly: bool


class PermissionsResponse(TypedDict):
    """``GET /api/me/permissions``, the session user's grants plus the whole permission catalog."""

    grants: list[str]
    "``>`` is every permission (the admin); a user with no roles has none."
    catalog: list[PermissionNode]
    roleIds: list[str]


class PreviewStatus(TypedDict):
    """The preview build's countdown in `HealthStatusResponse`."""

    expiresAt: str
    daysRemaining: int
    reason: Optional[str]
    "Only seen as `None`."
    update: Optional[Any]
    "Only seen as `None`, so the shape of an offered update is unknown."


class ProblemDetailsResponse(TypedDict):
    """ASP.NET's validation error body (RFC 9110), eg. a ``POST /api/Auth/login`` with no username (400)."""

    type: str
    title: str
    status: int
    errors: dict[str, list[str]]
    """The field name, as AMP spells it (``"Username"``), to its errors."""
    traceId: str


class ProfileResponse(TypedDict):
    """``GET /api/profile``, the session user's own account."""

    id: str
    userName: str
    displayName: Optional[str]
    email: str
    emailConfirmed: bool


class TokenResponse(TypedDict):
    """A new session token, from a login, `renew`, ``change-expired-password`` or the first-run admin setup.

    The token is a JWT sent back as ``Authorization: Bearer <token>``.
    It lasts 8 hours, or 28 days when the login asked for `rememberMe`.
    """

    token: str
    expiration: str
    "ISO 8601 in UTC, eg. ``2026-11-07T04:51:17.405287Z``."


class ValidationErrorResponse(TypedDict):
    """A list of refusals, eg. a password the policy rejects (400)."""

    errors: list[str]


LoginResponse = Union[TokenResponse, PasswordChangeRequiredResponse, PasskeyRequiredResponse]
