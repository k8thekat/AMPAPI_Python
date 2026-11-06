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

from collections.abc import Mapping, Sequence
from typing import Any, Literal, Optional, TypedDict, Union

__all__ = (
    "CapabilitiesResponse",
    "CodedErrorResponse",
    "HTTPSStateResponse",
    "HealthStatusResponse",
    "HubTokenResponse",
    "LicenceQueryResponse",
    "LicenceResponse",
    "LicenceStatusResponse",
    "LoginResponse",
    "MessageErrorResponse",
    "PasskeyFlowResponse",
    "PasskeyRegisteredResponse",
    "PasskeyRequiredResponse",
    "PasskeyResponse",
    "PasswordChangeRequiredResponse",
    "PasswordPolicyResponse",
    "PermissionNode",
    "PermissionsResponse",
    "PreviewStatus",
    "PreviewUpdate",
    "ProblemDetailsResponse",
    "ProfileResponse",
    "QueryParameters",
    "ReasonErrorResponse",
    "RecoveryCodesResponse",
    "RecoveryCodesStatusResponse",
    "SettingAction",
    "SettingSpec",
    "SettingsManifestResponse",
    "TokenResponse",
    "ValidationErrorResponse",
)


class CapabilitiesResponse(TypedDict):
    """``GET /api/auth/capabilities``, which needs no session."""

    passkeysAvailable: bool
    "If passkeys work for this request; it depends on the address the request came in on."
    passkeyStatus: str
    """``"NotConfigured"`` (no public address set), ``"OriginMismatch"`` (not asked at that address) or ``"Eligible"``."""
    passkeyMessageKey: Optional[str]
    """A translation key for the status, eg. ``"passkeys.origin.notConfigured"``, not a message."""
    rpId: Optional[str]
    "The WebAuthn relying party ID, the public address's host name; `None` until one is set."
    expectedOrigin: Optional[str]
    passkeyPolicy: str
    """``"Optional"``, ``"Encouraged"`` or ``"Required"``."""


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


class HTTPSStateResponse(TypedDict):
    """``GET /api/https``, the panel's HTTPS setup. ``POST /api/https/own-proxy`` answers with it too."""

    mode: str
    """Seen as ``"none"`` and ``"ownProxy"``."""
    hostName: Optional[str]
    "Only seen as `None`."
    url: Optional[str]
    "Only seen as `None`."
    certificateVerified: bool
    agentPresent: bool
    agentSupported: bool
    panelExposed: bool
    entryNode: bool
    externalAddress: str
    "The panel's public IP address."
    reachability: str
    """Seen as ``"Nat"``."""
    internalAddress: str
    "The panel's address on its own network."
    ipv6Address: Optional[str]
    "Only seen as `None`."
    trustedProxies: list[str]
    "The reverse proxies AMP takes forwarded headers from, set by `PlatformModule.set_own_proxy`."
    serveFrontend: bool
    "If AMP serves the web app as well as its API or not."
    running: bool


class HubTokenResponse(TypedDict):
    """``POST /api/auth/hub-token``, a short lived token for the SignalR hub (about 60 seconds)."""

    token: str
    expiresAt: str


class LicenceQueryResponse(TypedDict):
    """``POST /api/licence/query``, what a key gives, without activating it."""

    productName: str
    gradeName: str
    expires: str
    usage: int
    "How many installations already use the key; one key covers several."
    alreadyActive: bool
    eligible: bool
    termsRequired: bool
    "If activating the key needs a terms acceptance."
    termsVersion: int
    requiredTermsVersion: int
    issuedAt: str


class LicenceResponse(TypedDict):
    """One licence from `LicenceStatusResponse.licences`, or the one ``POST /api/licence`` activated (201)."""

    spireId: str
    "The spire the licence is active on."
    spireName: str
    gradeId: str
    productName: str
    gradeName: str
    """eg. ``"Beta Preview"``."""
    state: str
    """Seen as ``"Valid"``."""
    standing: str
    """Seen as ``"Active"``; the web panel also checks for ``"TermsRequired"``."""
    expires: str
    graceEnds: Optional[str]
    "Only seen as `None`; the web panel shows it as a date."
    usage: int
    limitKnown: bool
    shardLimit: Optional[int]
    "Only seen as `None`."
    keyShardsTotal: Optional[int]
    "Only seen as `None`."
    issuedAt: Optional[str]
    "Only seen as `None` here."
    termsVersion: Optional[int]
    "Only seen as `None` here."
    requiredTermsVersion: Optional[int]
    "Only seen as `None` here."


class LicenceStatusResponse(TypedDict):
    """``GET /api/licence``, the panel's licences and how many shards they allow."""

    licences: list[LicenceResponse]
    "Empty until a key is activated."
    shardCount: int
    otherInstallationShards: int
    licensed: bool
    confirmed: bool
    shardLimit: Optional[int]
    "Seen as 0 with no licence, and `None` with the Beta Preview licence."
    shardCeiling: Optional[int]
    "Seen as 0 with no licence, and `None` with the Beta Preview licence."
    lastVerifiedAt: Optional[str]
    "Only seen as `None`."
    usingMockClient: bool


class MessageErrorResponse(TypedDict):
    """The body of a refused ``POST /api/Auth/login`` (401); the same text for a wrong password or an unknown user."""

    message: str


class PasskeyFlowResponse(TypedDict):
    """``POST /api/auth/passkey/begin`` and ``POST /api/profile/passkeys/register/begin``, a WebAuthn ceremony to answer."""

    flowId: str
    "Sent back with the answer to ``.../complete`` (or ``/api/auth/passkey/abandon``)."
    options: dict[str, Any]
    "The WebAuthn options, base64url encoded, for ``navigator.credentials.get`` or ``navigator.credentials.create``."


class PasskeyRegisteredResponse(TypedDict):
    """``POST /api/profile/passkeys/register/complete``."""

    passkey: PasskeyResponse
    session: Optional[TokenResponse]
    "Only seen as `None` from a full session."


class PasskeyRequiredResponse(TypedDict):
    """A ``POST /api/Auth/login`` answer for an account that needs a second factor; it carries no token.

    AMP sends it when the passkey policy is ``"Required"`` and the account has a passkey. A recovery code to
    ``POST /api/Auth/login/second-factor`` finishes the login.
    """

    passkeyRequired: Literal[True]


class PasskeyResponse(TypedDict):
    """One passkey from ``GET /api/profile/passkeys``."""

    id: str
    credentialId: str
    "The WebAuthn credential ID, base64url."
    name: str
    createdAt: str
    lastUsedAt: Optional[str]
    backupEligible: bool
    usable: bool


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
    update: Optional[PreviewUpdate]
    "Often `None`."


class PreviewUpdate(TypedDict):
    """The preview build's update check in `PreviewStatus`; only seen with no update on offer."""

    state: str
    """Seen as ``"current"``."""
    version: Optional[str]
    "Only seen as `None`."
    stream: Optional[str]
    "Only seen as `None`."
    reason: Optional[str]
    "Only seen as `None`."


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


class ReasonErrorResponse(TypedDict):
    """The body of a refused ``POST /api/Auth/login/second-factor`` (401), eg. a wrong or already used recovery code."""

    message: str
    reason: str
    """A dotted translation key, eg. ``"auth.login.recoveryCodeRejected"``; other errors send it as `code`."""


class RecoveryCodesResponse(TypedDict):
    """``POST /api/profile/recovery-codes``, a new set of codes. It replaces any earlier set."""

    codes: list[str]
    "10 codes of 14 characters; each works once, and AMP never shows them again."


class RecoveryCodesStatusResponse(TypedDict):
    """``GET /api/profile/recovery-codes``."""

    remaining: int
    total: int
    generatedAt: Optional[str]
    low: bool
    "Set when few codes remain (and when none were ever made)."


class SettingAction(TypedDict):
    """A button from `SettingsManifestResponse.actions`, run by ``POST /api/settings/actions/{id}``."""

    id: str
    """eg. ``"smtp.test"`` or ``"templates.sync"``."""
    category: str
    "The `SettingSpec.category` it sits under."


class SettingsManifestResponse(TypedDict):
    """``GET /api/settings/manifest``, every platform setting with its current value."""

    specs: list[SettingSpec]
    values: dict[str, str]
    """A setting's `fieldName` to its value. Every value is a string, eg. ``"587"``, ``"true"`` or ``"[]"``."""
    secretHasValue: dict[str, bool]
    "A secret setting's `fieldName` to if it holds a value."
    actions: list[SettingAction]
    unavailable: dict[str, str]
    """A setting that can't be changed, to a translation key saying why, eg. ``"preview.crashReportsLocked"``."""


class SettingSpec(TypedDict):
    """One setting from `SettingsManifestResponse.specs`."""

    fieldName: str
    """The setting's key in `SettingsManifestResponse.values`, eg. ``"smtp.host"``."""
    paramFieldName: str
    effectiveKey: str
    required: bool
    hidden: bool
    platform: int
    deployment: int
    conditionSetting: str
    conditionValue: str
    defaultValue: Optional[Any]
    "Only seen as `None`."
    meta: str
    category: str
    """eg. ``"email"`` or ``"security"``."""
    subcategory: str
    special: str
    displayName: str
    """A translation key, eg. ``"settings.smtp.host.name"``, not the name itself."""
    description: str
    "A translation key, like `displayName`."
    keywords: str
    inputType: str
    """Seen as ``"text"``, ``"multiline"``, ``"number"``, ``"quantity"``, ``"checkbox"``, ``"select"``, ``"list"``,
    ``"password"`` and ``"credential:Smtp"``."""
    isSecret: bool
    placeholder: str
    suffix: str
    order: int
    readOnly: bool
    isFlagArgument: bool
    flagValue: str
    includeInCommandLine: bool
    includeInConfigFile: bool
    skipIfEmpty: bool
    enumValues: dict[str, str]
    """A value to its label: a translation key for a ``"select"``, the unit itself for a ``"quantity"``. Often empty."""
    valueSourceId: str
    minValue: Optional[float]
    "Only seen as `None`."
    maxValue: Optional[float]
    "Only seen as `None`."
    isHostCap: bool
    multiplier: Optional[Any]
    "Only seen as `None`."
    multipleOf: Optional[float]
    "Only seen as `None`."
    maxLength: int
    listValuePrefix: str
    listValueSeparator: str
    excludeFromImport: bool


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
# A query string; a list value repeats its key, so {"shard": ["a", "b"]} is sent as shard=a&shard=b.
QueryParameters = Mapping[str, Union[str, int, Sequence[str]]]
