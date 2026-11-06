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
    "AnalyticsAddressUsersResponse",
    "AnalyticsPeriod",
    "AnalyticsProfilesResponse",
    "AnalyticsRule",
    "AnalyticsServerInfo",
    "AnalyticsSessionsResponse",
    "AnalyticsTotals",
    "AnalyticsUserAddressesResponse",
    "AnalyticsUserSessionsResponse",
    "AnalyticsUsersResponse",
    "AuditActionCount",
    "AuditEvent",
    "AuditFacetsResponse",
    "AuditOriginCount",
    "AuditPageResponse",
    "AuditRoot",
    "AuditRootsPageResponse",
    "AuditTreeNode",
    "AuditTreeResponse",
    "AuditUserCount",
    "BrandingResponse",
    "BusJoinInfo",
    "CapabilitiesResponse",
    "CodedErrorResponse",
    "CredentialResponse",
    "DatastoreResponse",
    "DatastoreUsage",
    "DeletedUserResponse",
    "DiagnosticsResponse",
    "FirewallResponse",
    "FirewallRule",
    "FirewallStatus",
    "GatewayEligibilityResponse",
    "HTTPSSetupStatusResponse",
    "HTTPSStateResponse",
    "HealthStatusResponse",
    "HubTokenResponse",
    "InviteAcceptedResponse",
    "InvitePreviewResponse",
    "InviteResponse",
    "InviteTokenResponse",
    "LicenceAgreementResponse",
    "LicenceQueryResponse",
    "LicenceResponse",
    "LicenceStatusResponse",
    "LicenceTermsAcceptance",
    "LoginResponse",
    "MessageBusService",
    "MessageBusStatsResponse",
    "MessageErrorResponse",
    "MonitoringThresholdsResponse",
    "PasskeyFlowResponse",
    "PasskeyRegisteredResponse",
    "PasskeyRequiredResponse",
    "PasskeyResponse",
    "PasswordChangeRequiredResponse",
    "PasswordPolicyResponse",
    "PermissionNode",
    "PermissionsResponse",
    "PortClaimResponse",
    "PreferencesResponse",
    "PreviewStatus",
    "PreviewUpdate",
    "Principal",
    "ProblemDetailsResponse",
    "ProfileResponse",
    "ProfileSessionResponse",
    "QueryParameters",
    "ReasonErrorResponse",
    "RecoveryCodesResponse",
    "RecoveryCodesStatusResponse",
    "RevokedSessionsResponse",
    "RoleResponse",
    "RunningTaskResponse",
    "SSHKeyResponse",
    "SettingAction",
    "SettingSpec",
    "SettingsManifestResponse",
    "ShardUsage",
    "SpireCPU",
    "SpireEnrollmentHostResponse",
    "SpireIPAddress",
    "SpireIPOptionResponse",
    "SpireImportScanResponse",
    "SpirePlatform",
    "SpirePortResponse",
    "SpireResponse",
    "SpireRosterResponse",
    "SpireStartupEntry",
    "SpireStartupResponse",
    "SpireStateResponse",
    "SpireStorageResponse",
    "SpireUsageIntervalResponse",
    "SpireUsageResponse",
    "SystemBusResponse",
    "TokenResponse",
    "UpdateStatusResponse",
    "UserResponse",
    "ValidationErrorResponse",
    "WrappedID",
)


class AnalyticsAddressUsersResponse(TypedDict):
    """``GET /api/analytics/addresses/users``, the players seen at one address.

    Only seen with no players, so the shape of a user is unknown.
    """

    address: str
    network: str
    kind: str
    """Seen as ``"Public"``."""
    users: list[Any]
    "Only seen empty."
    serverInfo: dict[str, AnalyticsServerInfo]
    "A shard ID to the shard's name and game."
    isDemo: bool


class AnalyticsPeriod(TypedDict):
    """A stretch of time and the players in it, from `AnalyticsSessionsResponse`."""

    start: str
    end: str
    users: int


class AnalyticsProfilesResponse(TypedDict):
    """``GET /api/analytics/profiles``, players' Steam and Minecraft profiles.

    Only seen with no players, so the shape of a profile is unknown.
    """

    steam: dict[str, Any]
    "Only seen empty."
    minecraft: dict[str, Any]
    "Only seen empty."
    state: str
    """Seen as ``"complete"``."""
    isDemo: bool


class AnalyticsRule(TypedDict):
    """How many visits in how many days make a player active, from the analytics settings."""

    visits: int
    days: int


class AnalyticsServerInfo(TypedDict):
    """A shard's name and game, from an analytics reply's `serverInfo`."""

    name: str
    game: str
    """The template slug, eg. ``"teeworlds"``."""
    gameName: str
    image: str
    """eg. ``"steam:380840"``."""


class AnalyticsSessionsResponse(TypedDict):
    """``GET /api/analytics/sessions``, the player summary for the analytics page.

    Only seen with no players, so every list was empty and every total 0.
    """

    window: dict[str, str]
    """``"from"`` and ``"to"``, ISO 8601; the last 30 days unless asked."""
    current: AnalyticsTotals
    previous: AnalyticsTotals
    change: dict[str, Optional[float]]
    "The `AnalyticsTotals` keys, only seen as `None`."
    activity: list[AnalyticsPeriod]
    "One a day."
    countries: list[Any]
    "Only seen empty."
    topUsers: list[Any]
    "Only seen empty."
    busiest: AnalyticsPeriod
    quietest: AnalyticsPeriod
    servers: list[Any]
    "Only seen empty."
    games: list[Any]
    "Only seen empty."
    isDemo: bool
    serverInfo: dict[str, AnalyticsServerInfo]
    "A shard ID to the shard's name and game."
    rule: AnalyticsRule


class AnalyticsTotals(TypedDict):
    """Player totals from `AnalyticsSessionsResponse` and `AnalyticsUserSessionsResponse`; every one only seen as 0."""

    sessions: int
    uniqueUsers: int
    newUsers: int
    minutes: float
    bounceRatePercent: float
    averageSessionMinutes: float
    sessionsPerUser: float
    longestSessionMinutes: float
    activeUsers: int
    activeRatePercent: float


class AnalyticsUserAddressesResponse(TypedDict):
    """``GET /api/analytics/users/{key}/addresses``, the addresses one player was seen at.

    Only seen for an unknown player, so the shape of an address is unknown.
    """

    addresses: list[Any]
    "Only seen empty."
    serverInfo: dict[str, AnalyticsServerInfo]
    isDemo: bool


class AnalyticsUserSessionsResponse(TypedDict):
    """``GET /api/analytics/sessions/users/{key}``, one player's history.

    An unknown player answers 200 with everything empty, and that is the only one seen.
    """

    userKey: str
    displayName: Optional[str]
    "Only seen as `None`."
    totals: AnalyticsTotals
    servers: list[Any]
    "Only seen empty."
    sessions: list[Any]
    "Only seen empty."
    firstSeen: Optional[str]
    "Only seen as `None`."
    lastSeen: Optional[str]
    "Only seen as `None`."
    isActive: bool
    recentVisits: int
    rule: AnalyticsRule
    serverInfo: dict[str, AnalyticsServerInfo]
    isDemo: bool


class AnalyticsUsersResponse(TypedDict):
    """``GET /api/analytics/users``, a player search.

    Only seen with no players, so the shape of a user is unknown.
    """

    users: list[Any]
    "Only seen empty."
    serverInfo: dict[str, AnalyticsServerInfo]
    isDemo: bool
    address: Optional[Any]
    "Only seen as `None`."


class AuditActionCount(TypedDict):
    """One action and how often it was logged, from `AuditFacetsResponse.actions`."""

    action: str
    count: int


class AuditEvent(TypedDict):
    """One audit log entry, from `AuditPageResponse.items`."""

    id: str
    tenantId: str
    timestamp: str
    severity: int
    """Seen as 0, 1 and 2; the `min_severity` filter takes the names ``"Info"``, ``"Warning"`` and ``"Security"``."""
    principal: Principal
    "Who or what did it."
    action: str
    """eg. ``"ShardCreated"`` or ``"SharedCredentialDeleted"``."""
    targetType: str
    """eg. ``"Shard"``, ``"User"`` or ``"Setting"``."""
    targetId: str
    taskId: Optional[str]
    correlationId: WrappedID
    "Shared by every event in one flow, see `AnalyticsModule.get_audit_tree`."
    actionId: WrappedID
    causationActionId: Optional[WrappedID]
    origin: int
    """Seen as 0, 1 and 2, which the `origin` filter takes as ``"System"``, ``"User"`` and ``"UserFlow"``."""
    rootPrincipal: Principal
    details: Optional[str]
    "More about the event, as JSON in a string."
    originIp: Optional[str]
    originSpireId: str
    originNode: str
    "The spire's host name."


class AuditFacetsResponse(TypedDict):
    """``GET /api/audit/facets``, what the audit log's filters can choose from."""

    actions: list[AuditActionCount]
    users: list[AuditUserCount]
    targetTypes: list[str]
    origins: list[AuditOriginCount]


class AuditOriginCount(TypedDict):
    """One origin and how often it was logged, from `AuditFacetsResponse.origins`."""

    origin: int
    count: int


class AuditPageResponse(TypedDict):
    """``GET /api/audit``, one page of the audit log, newest first unless asked."""

    total: int
    "How many events match, over every page."
    page: int
    pageSize: int
    "50 unless asked; AMP caps it at 200."
    caughtUp: bool
    items: list[AuditEvent]


class AuditRoot(TypedDict):
    """One flow of events, from `AuditRootsPageResponse.items`."""

    correlationId: str
    "The ID `AnalyticsModule.get_audit_tree` takes."
    root: AuditEvent
    "The event that started the flow."
    eventCount: int
    startedAt: str
    endedAt: str
    maxSeverity: int
    rootMissing: bool


class AuditRootsPageResponse(TypedDict):
    """``GET /api/audit/roots``, one page of the audit log grouped into flows."""

    total: int
    page: int
    pageSize: int
    caughtUp: bool
    items: list[AuditRoot]


class AuditTreeNode(TypedDict):
    """One event in a flow and the events it led to, from `AuditTreeResponse.root`."""

    event: AuditEvent
    children: list[AuditTreeNode]


class AuditTreeResponse(TypedDict):
    """``GET /api/audit/tree/{correlation_id}``, every event in one flow."""

    correlationId: str
    rootMissing: bool
    eventCount: int
    startedAt: str
    endedAt: str
    root: AuditTreeNode


class AuditUserCount(TypedDict):
    """One user and how many events they caused, from `AuditFacetsResponse.users`."""

    userId: str
    name: str
    count: int


class BrandingResponse(TypedDict):
    """``GET /api/branding``, the names and logo the login page shows."""

    productName: str
    "Empty for AMP's own."
    loginWelcomeText: str
    logoUrl: str
    defaultTheme: str
    """Seen as ``"proteus"``, lower case where the settings say ``"Proteus"``."""


class BusJoinInfo(TypedDict):
    """What another machine needs to reach the message bus, from `SystemBusResponse.joinInfo`."""

    servers: list[str]
    """eg. ``["tls://127.0.0.1:4222"]``."""
    prefix: str
    hostCandidates: list[str]
    caCert: str
    joinBlob: str
    "Empty while the bus isn't open to other machines."


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
    """Values for the `code` translation, eg. ``{"scope": "shard"}``; often `None`."""
    message: str
    "The English text of `code`."


class CredentialResponse(TypedDict):
    """One stored secret shards can use, from ``GET /api/credentials``; AMP never sends the secret back."""

    id: str
    title: str
    kind: str
    """Seen as ``"SteamCmd"``; AMP also takes ``"Smtp"``, ``"DiscordWebhook"`` and ``"ApiKey"``."""
    visibility: str
    """``"Private"`` or ``"Public"``."""
    mine: bool
    username: str
    shardCount: int
    createdAt: str
    updatedAt: str


class DatastoreResponse(TypedDict):
    """One of a spire's datastores, the folders shards are kept in, from ``GET /api/spires/{id}/datastores``."""

    id: str
    name: str
    path: str
    """eg. ``"/opt/cubecoders/amp3/data/Datastores/Default"``. AMP doesn't check the folder exists."""
    isDefault: bool
    enabled: bool
    softLimitMb: int
    "Only seen as 0."
    tags: list[str]
    """AMP sets these itself, eg. ``["HDD"]``."""


class DatastoreUsage(TypedDict):
    """One datastore's disk use, from `SpireUsageResponse.datastores`."""

    datastoreId: str
    totalUsedMb: int
    driveFreeMb: int
    driveTotalMb: int
    shards: list[ShardUsage]


class DeletedUserResponse(TypedDict):
    """``DELETE /api/users/{id}``, which answers 200 with a body where other deletes answer 204."""

    warnings: list[Any]
    "Only seen empty."


class DiagnosticsResponse(TypedDict):
    """``GET /api/support/diagnostics``, the details a support request asks for."""

    ampVersion: str
    codename: str
    buildCommit: str
    configuration: str
    """Seen as ``"Production"``."""
    operatingSystem: str
    architecture: str
    hardwarePlatform: str
    cpuModel: str
    cpuTopology: str
    """Sockets, cores and threads, eg. ``"2S/1C/1T"``."""
    hostname: str
    totalRamMb: int
    virtualization: str
    """eg. ``"QEMU_KVM"``."""
    natsStatus: str
    """The message bus, seen as ``"Connected"``."""
    uptimeSeconds: int
    "Only seen as 0, even 40 minutes after the panel started."
    auditOrphanWrites: int
    auditRelaunchCarriedWrites: int
    ipv6: str
    """Seen as ``"Unavailable"``, with the reason in `ipv6Detail`."""
    ipv6Detail: str
    containerRuntime: str
    """Seen as ``"Podman"``."""
    containerRuntimeVersion: str
    containerRuntimeVerdict: str
    """Seen as ``"Usable"``."""
    containerRuntimeReason: Optional[str]
    "Only seen as `None`."


class FirewallResponse(TypedDict):
    """``GET /api/networking/firewall``, the firewall rules AMP keeps on the host."""

    running: bool
    status: FirewallStatus
    withheld: list[Any]
    "Only seen empty."


class FirewallRule(TypedDict):
    """One port AMP opened, from `FirewallStatus.applied`."""

    port: int
    protocol: str
    """Seen as ``"Tcp"``."""
    tag: str
    """eg. ``"panel-web"``, ``"nats"`` or ``"sftp"``."""
    label: str
    """eg. ``"AMP panel"``."""
    scope: str
    """Seen as ``"Any"`` and ``"HostOnly"``."""


class FirewallStatus(TypedDict):
    """The firewall's state, from `FirewallResponse.status`. The lists past `applied` were only seen empty."""

    schema: int
    generation: int
    backend: str
    """eg. ``"iptables+ip6tables"``."""
    healthy: bool
    applied: list[FirewallRule]
    rejected: list[Any]
    wireGuardApplied: list[Any]
    wireGuardRejected: list[Any]
    wireGuardPeersApplied: list[Any]
    wireGuardPeersRejected: list[Any]
    gatewayApplied: list[Any]
    gatewayRejected: list[Any]
    advisories: list[Any]
    error: Optional[str]
    "Only seen as `None`."
    updatedAt: str
    agentVersion: str


class GatewayEligibilityResponse(TypedDict):
    """``GET /api/networking/gateway-eligibility``, what can take part in a gateway. Both were only seen empty."""

    containerShardIds: list[str]
    gatewayFrontSpireIds: list[str]


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


class HTTPSSetupStatusResponse(TypedDict):
    """``GET /api/https/setup/status``, the progress of AMP's own HTTPS setup."""

    phase: str
    """Seen as ``"idle"``."""
    hostName: Optional[str]
    "Only seen as `None`."
    checks: list[Any]
    "Only seen empty."
    url: Optional[str]
    "Only seen as `None`."
    certificateVerified: bool
    updatedUtc: str
    """``"0001-01-01T00:00:00+00:00"`` before any setup."""


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


class InviteAcceptedResponse(TypedDict):
    """``POST /api/invites/accept``, which needs no session. It makes the account and logs it in.

    The token is a live session for the new user, like `TokenResponse`.
    """

    token: str
    expiration: str
    droppedRoles: list[Any]
    "Only seen empty, even when one of the invite's roles had been deleted."


class InvitePreviewResponse(TypedDict):
    """``POST /api/invites/preview``, which needs no session."""

    userName: str
    displayName: Optional[str]


class InviteResponse(TypedDict):
    """One invite from ``GET /api/invites``."""

    id: str
    userName: str
    "The username the new account gets."
    displayName: Optional[str]
    roleIds: list[str]
    createdByName: str
    createdAt: str
    expiresAt: str
    accepted: bool
    acceptedAt: Optional[str]
    status: str
    """Seen as ``"pending"`` and ``"accepted"``. A revoked invite leaves the list."""


class InviteTokenResponse(TypedDict):
    """``POST /api/invites`` (201) and ``POST /api/invites/{id}/rearm``."""

    invite: InviteResponse
    token: str
    "The invite code to hand to the new user; a rearm makes the old one stop working."


class LicenceAgreementResponse(TypedDict):
    """``GET /api/licence/terms/agreement``, the licence terms a key may need accepted."""

    version: int
    "Seen as 2, the current `termsVersion`."
    language: str
    title: str
    """eg. ``"AMP 2 to AMP 3 Licence Migration"``."""
    markdown: str
    "The terms, as Markdown."
    hash: str
    "The `agreementHash` a `LicenceTermsAcceptance` sends back."
    fallbackFrom: Optional[str]
    """The language asked for when AMP had to send English instead, eg. ``"fr"``."""
    attestation: str
    "The sentence the user agrees to, sent back in a `LicenceTermsAcceptance`."


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
    "`None` until the licence service has answered, eg. 50."
    keyShardsTotal: Optional[int]
    "`None` until the licence service has answered."
    issuedAt: Optional[str]
    "`None` until the licence service has answered."
    termsVersion: Optional[int]
    "`None` until the licence service has answered."
    requiredTermsVersion: Optional[int]
    "`None` until the licence service has answered."


class LicenceStatusResponse(TypedDict):
    """``GET /api/licence``, the panel's licences and how many shards they allow."""

    licences: list[LicenceResponse]
    "Empty until a key is activated."
    shardCount: int
    otherInstallationShards: int
    licensed: bool
    confirmed: bool
    shardLimit: Optional[int]
    "Seen as 0 with no licence, `None` just after activating one and 50 once the licence service answered."
    shardCeiling: Optional[int]
    "Seen as 0 with no licence, `None` just after activating one and 57 with a limit of 50."
    lastVerifiedAt: Optional[str]
    "`None` until the licence service has answered."
    usingMockClient: bool


class LicenceTermsAcceptance(TypedDict):
    """The terms acceptance `PlatformModule.activate_licence` and `PlatformModule.accept_licence_terms` send.

    Its keys come from the web panel's code; not yet seen live. Fill it from `LicenceAgreementResponse`.
    """

    termsVersion: int
    "The agreement's `version`."
    agreementHash: str
    "The agreement's `hash`."
    attestation: str
    "The agreement's `attestation`."
    locale: str
    """The language the user read it in, eg. ``"en"``."""
    clickedAt: str
    "When the user agreed, ISO 8601."


class MessageBusService(TypedDict):
    """The message bus's own process, from `MessageBusStatsResponse.service`."""

    condition: str
    """Seen as ``"Running"``."""
    pid: int
    startedAtUtc: str
    binaryVersion: str
    configHash: str
    configCurrent: bool
    fileStoreBytes: int
    lastExitReason: Optional[str]
    "Only seen as `None`."
    updatedAtUtc: str
    serviceVersion: str
    """eg. ``"amp3-host 3.0.0.6+f3d1a77cea"``."""
    serviceUp: bool


class MessageBusStatsResponse(TypedDict):
    """``GET /api/support/message-bus-stats``, the NATS message bus's figures."""

    state: str
    """Seen as ``"Open"``."""
    serverId: str
    serverName: str
    serverVersion: str
    clusterName: Optional[str]
    "Only seen as `None`."
    rttMs: float
    jetStreamAvailable: bool
    jsStreams: int
    jsConsumers: int
    jsStorageBytes: int
    jsApiTotal: int
    jsApiErrors: int
    service: MessageBusService


class MessageErrorResponse(TypedDict):
    """The body of a refused ``POST /api/Auth/login`` (401); the same text for a wrong password or an unknown user."""

    message: str


class MonitoringThresholdsResponse(TypedDict):
    """``GET /api/monitoring/thresholds``, when the web panel warns about load, from the monitoring settings."""

    cpuWarningPercent: int
    cpuHighPercent: int
    ramWarning: str
    """Free memory with its unit, eg. ``"20%"``."""
    ramHigh: str
    diskWarning: str
    """Free disk with its unit, eg. ``"16GB"``."""
    diskHigh: str
    diskWarningShare: int
    diskHighShare: int


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


class PortClaimResponse(TypedDict):
    """One port something holds on a spire, from ``GET /api/networking/spires/{id}/port-claims``.

    An idle spire lists hundreds, mostly for WireGuard tunnels.
    """

    kind: str
    """Seen as ``"SpireService"``."""
    port: int
    protocol: str
    """Seen as ``"Both"``."""
    shardId: Optional[str]
    "Only seen as `None`."
    holderName: str
    """eg. ``"the AMP panel"`` or ``"a WireGuard tunnel"``."""


class PreferencesResponse(TypedDict):
    """``GET /api/users/me/preferences``, the logged in user's web panel preferences.

    Changing them (``PATCH /api/users/me/preferences``) and adding or removing a favourite answer with all of them too.
    A preference never set is `None`.
    """

    theme: Optional[str]
    """Seen as ``"dark"``."""
    locale: Optional[str]
    "Only seen as `None`."
    favouriteAppSlugs: list[str]
    "Template slugs; AMP doesn't check them against the templates."
    pinnedShardIds: list[str]
    notifyOnStateChange: Optional[bool]
    "Only seen as `None`."
    notifyOnUpdateAvailable: Optional[bool]
    "Only seen as `None`."
    compactShardHeader: Optional[bool]
    hideUnroutedShards: Optional[bool]
    "Only seen as `None`."
    hidePrivatePorts: Optional[bool]
    "Only seen as `None`."
    fileDetailsWidth: Optional[int]
    "Only seen as `None`."
    ampExperience: Optional[str]
    "Only seen as `None`."
    showTutorials: Optional[bool]
    "Only seen as `None`."
    tutorialPromptDismissed: Optional[bool]
    "Only seen as `None`."
    tutorialsCompleted: list[str]
    "Only seen empty."
    accessibilityHintsEnabled: Optional[bool]
    "Only seen as `None`."
    onboardingCompleted: Optional[bool]
    "Only seen as `None`."
    reducedMotion: Optional[bool]
    "Only seen as `None`."
    analyticsEnabled: Optional[bool]
    "Only seen as `None`."
    streamerMode: Optional[bool]
    "Only seen as `None`."
    timeFormat: Optional[str]
    "Only seen as `None`."


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


class Principal(TypedDict):
    """Who or what did something, from a running task or an audit event."""

    kind: int
    "Seen as 0 for a user and 1 for AMP itself."
    userId: Optional[str]
    userDisplayName: Optional[str]
    onBehalfOfUserId: Optional[str]
    "Only seen as `None`."
    onBehalfOfUserDisplayName: Optional[str]
    "Only seen as `None`."
    systemSource: Optional[str]
    """The part of AMP that did it, eg. ``"Auth"`` or ``"Reconciler"``, when `kind` is 1."""


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
    "AMP doesn't check it's an email address."
    emailConfirmed: bool
    "Only seen as `False`."


class ProfileSessionResponse(TypedDict):
    """One of the logged in user's sessions, from ``GET /api/profile/sessions``."""

    id: str
    createdAt: str
    lastSeenAt: str
    expiresAt: str
    remoteIp: str
    """IPv4 comes as an IPv6 mapped address, eg. ``"::ffff:192.168.4.51"``."""
    userAgent: str
    isCurrent: bool
    "If it's the session this request came from."


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


class RevokedSessionsResponse(TypedDict):
    """``DELETE /api/profile/sessions/others``, which answers 200 with a body."""

    revoked: int
    "How many sessions it ended."


class RoleResponse(TypedDict):
    """One role from ``GET /api/roles``; creating or updating one answers with it too."""

    id: str
    name: str
    description: str
    permissions: list[str]
    """Permission strings, eg. ``"users.read"`` or ``"spire.*.shard.*.view"``; a leading ``-`` denies.

    AMP stores them as given, without checking they exist.
    """
    ownerUserId: str
    createdAt: str


class RunningTaskResponse(TypedDict):
    """One long job, such as a shard update, from ``GET /api/running-tasks``.

    A finished task leaves the list on its own after about 7 seconds.
    """

    id: str
    tenantId: str
    type: str
    """Seen as ``"ApplicationUpdate"``."""
    name: str
    """eg. ``"Update my-shard"``."""
    nameCode: Optional[str]
    "Only seen as `None`."
    nameParams: Optional[dict[str, Any]]
    "Only seen as `None`."
    message: Optional[str]
    "The current step, eg. a download; `None` once it finishes."
    messageCode: Optional[str]
    "Only seen as `None`."
    messageParams: Optional[dict[str, Any]]
    "Only seen as `None`."
    speed: Optional[Any]
    "Only seen as `None`."
    progressPercent: int
    isIndeterminate: bool
    state: int
    "Seen as 1 at the start, 0 while running and 3 when finished."
    isCancellable: bool
    "Only seen as `False`."
    isPrimary: bool
    principal: Principal
    visibility: int
    targetType: str
    """Seen as ``"Shard"``."""
    targetId: str
    correlationId: WrappedID
    causationActionId: WrappedID
    actionId: WrappedID
    origin: int
    rootPrincipal: Principal
    ownerSpireId: str
    runId: str
    subTasks: list[Any]
    "Only seen empty."
    startedAt: str
    completedAt: Optional[str]
    cancellationRequestedAt: Optional[str]
    "Only seen as `None`."
    updatedAt: str
    isTerminal: bool
    "If the task has finished; only a finished task can be dismissed."


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
    ``"password"``, ``"credential:Smtp"`` and, for a spire, ``"ipbinding"``."""
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


class ShardUsage(TypedDict):
    """One shard's disk use, from `DatastoreUsage.shards`. A deleted shard stays until it is purged."""

    kind: str
    """Seen as ``"Shard"``."""
    shardId: str
    name: str
    "The shard's folder name in the datastore."
    sizeMb: int
    deleted: bool
    deletedAt: Optional[str]
    displayName: str
    limitMb: int
    "Only seen as 0."
    limitLevel: str
    """Seen as ``"None"``."""


class SpireCPU(TypedDict):
    """The spire's processor, from `SpirePlatform.cpu`."""

    sockets: int
    cores: int
    threads: int
    modelName: str
    vendor: str
    totalCores: int
    totalThreads: int


class SpireEnrollmentHostResponse(TypedDict):
    """One address a new spire could join on, from ``GET /api/spires/enrollments/hosts``."""

    host: str
    kind: str
    """Seen as ``"internal"`` and ``"external"`` (the public address)."""
    interfaceName: str
    isPrimary: bool
    suggested: bool
    note: Optional[str]
    """Seen as ``"needsForward"`` on the public address."""


class SpireImportScanResponse(TypedDict):
    """``POST /api/spires/{id}/import/scan``, game servers from other panels that could be imported.

    Every list was empty on the test spire, so the shape of a found server is unknown.
    """

    servers: list[Any]
    "Only seen empty."
    unreadable: list[Any]
    "Only seen empty."
    truncatedRoots: list[Any]
    "Only seen empty."
    timedOut: bool


class SpireIPAddress(TypedDict):
    """One of the spire's addresses, from `SpirePlatform.reportedIps`."""

    address: str
    isV6: bool
    isInternal: bool
    isDhcp: Optional[bool]
    "Only seen as `None`."
    isPrimary: bool
    isTunnel: bool
    interfaceName: str


class SpireIPOptionResponse(SpireIPAddress):
    """One address a shard can bind to, from ``GET /api/spires/{id}/ip-options``."""

    role: str
    """Seen as ``"all"`` (``"0.0.0.0"``), ``"localhost"``, ``"address"`` and ``"auto"`` (``"@auto-pool"``)."""


class SpirePlatform(TypedDict):
    """The machine a spire runs on, from `SpireStateResponse.platform`."""

    os: int
    "Seen as 2 on Ubuntu."
    architecture: int
    "Seen as 1 on x86_64."
    osName: str
    hardwareName: str
    hostname: str
    cpu: SpireCPU
    installedRamMb: int
    virtualization: int
    "Seen as 5 on a QEMU/KVM VM."
    reportedIps: list[SpireIPAddress]
    installedJava: list[Any]
    "Only seen empty."
    externalIp: str
    reachability: str
    """Seen as ``"Nat"``."""
    freeDiskMb: int
    totalDiskMb: int
    freeRamMb: int
    loadAvgPercent: int
    reportedAt: str


class SpirePortResponse(TypedDict):
    """One port a shard uses on a spire, from ``GET /api/spires/{id}/ports``."""

    port: int
    protocol: str
    """Seen as ``"TCP"`` and ``"UDP"``."""
    ref: str
    """The port's name in the template, eg. ``"ServerPort"``."""
    name: str
    shardId: str
    shardName: str
    ipBinding: str
    running: bool
    listening: bool
    conflict: bool


class SpireResponse(TypedDict):
    """One spire, AMP 3's name for an ADS or Target, from ``GET /api/spires``."""

    id: str
    tenantId: str
    """Seen as ``"_root"``."""
    displayName: str
    description: str
    isLocal: bool
    "If it's the machine the panel runs on."
    platform: int
    "Seen as 2 on Ubuntu, the same number as `SpirePlatform.os`."
    architecture: int
    tags: list[str]
    "Only seen empty."
    ipPool: list[str]
    "Only seen empty."
    natsPrefix: str
    allocatablePortRange: str
    """eg. ``"1024:65535"``."""
    acceptsDeployments: bool
    maxShards: int
    defaultContainerMode: str
    """Seen as ``"Podman"``; the spire settings offer ``"Native"``, ``"Docker"`` and ``"Podman"``."""
    defaultContainerModeChosen: bool
    preferredContainerMode: str
    defaultShardIpBinding: str
    createdAt: str
    panelPort: int
    busPort: int
    identityPublicKey: str
    role: int
    "Only seen as 0."
    publicHost: str
    sftpEnabled: bool
    sftpPort: int
    sftpBindAddress: str
    sftpHoneypot: bool
    sftpIdleTimeoutSeconds: int
    sftpMaxSessionsPerUser: int
    shardSigningKeyPublic: str
    busUserPublicKey: str
    captureAgentOutput: bool
    logProcessLaunches: bool
    isPubliclyRoutable: bool
    isPublicEntryNode: bool
    canHostShards: bool
    acceptsNewShards: bool


class SpireRosterResponse(TypedDict):
    """One spire and if it's online, from ``GET /api/spires/roster``."""

    spire: SpireResponse
    online: bool
    lastSeen: str
    version: str
    behind: bool
    "If the spire runs an older AMP than the panel."
    installationVersion: str


class SpireStartupEntry(TypedDict):
    """One shard in the list `SpireModule.set_spire_startup` sends."""

    shardId: str
    startOnBoot: bool


class SpireStartupResponse(TypedDict):
    """One shard in a spire's start order, from ``GET /api/spires/{id}/startup``."""

    shardId: str
    shardName: str
    startOnBoot: bool
    order: int
    "A new shard has 100; saving the list sets each one to its place in it."


class SpireStateResponse(TypedDict):
    """``GET /api/spires/{id}/state``, a spire's live load.

    An unknown spire ID answers 200 with `online` `False`, zeros and no `platform`, not 404.
    """

    spireId: str
    online: bool
    lastHeartbeat: str
    shardCount: int
    cpuUsagePercent: float
    memoryUsedMb: int
    memoryTotalMb: int
    networkInKBps: float
    networkOutKBps: float
    diskActivePercent: Optional[float]
    busLatencyMs: float
    platform: Optional[SpirePlatform]


class SpireStorageResponse(TypedDict):
    """``PUT /api/spires/{id}/usage/interval``, a spire's storage settings. Reading the interval gives only `minutes`."""

    spireId: str
    tenantId: str
    datastores: list[DatastoreResponse]
    usageScanIntervalMinutes: int
    resolvedUsageScanInterval: str
    """The same interval as a time span, eg. ``"00:10:00"``."""
    updatedAt: str
    updatedByUserId: str


class SpireUsageIntervalResponse(TypedDict):
    """``GET /api/spires/{id}/usage/interval``, how often a spire measures its disk use."""

    minutes: int


class SpireUsageResponse(TypedDict):
    """``GET /api/spires/{id}/usage``, a spire's disk use per datastore from its last scan."""

    spireId: str
    scannedAt: str
    datastores: list[DatastoreUsage]


class SSHKeyResponse(TypedDict):
    """One of the logged in user's SFTP keys, from ``GET /api/profile/sshkeys``; adding one answers with it too."""

    id: str
    label: str
    keyType: str
    """Seen as ``"ssh-ed25519"``."""
    fingerprint: str
    """eg. ``"SHA256:MDGpHMbb3VwX0o1eKeHlX3rRfBMWpZmlRlINSshWK28"``."""
    bits: int
    addedAt: str
    lastUsedAt: Optional[str]
    "Only seen as `None`."
    expiresAt: Optional[str]


class SystemBusResponse(TypedDict):
    """``GET /api/system/bus``, the message bus spires talk to the panel over."""

    managed: bool
    "If AMP runs the bus itself."
    isPublic: bool
    "If other machines can reach it; a new spire can only join once it's public."
    joinInfo: BusJoinInfo
    servers: list[Any]
    "Only seen empty."


class TokenResponse(TypedDict):
    """A new session token, from a login, `renew`, ``change-expired-password`` or the first-run admin setup.

    The token is a JWT sent back as ``Authorization: Bearer <token>``.
    It lasts 8 hours, or 28 days when the login asked for `rememberMe`.
    """

    token: str
    expiration: str
    "ISO 8601 in UTC, eg. ``2026-11-07T04:51:17.405287Z``."


class UpdateStatusResponse(TypedDict):
    """``GET /api/updates/check``, the panel's AMP version against the latest one."""

    currentVersion: str
    stream: str
    """Seen as ``"Preview"``."""
    availableStreams: list[str]
    """eg. ``["Mainline", "Preview"]``."""
    latestVersion: str
    updateAvailable: bool
    mandatory: bool
    codename: str
    """eg. ``"Neptune"``."""
    releaseNotesUrl: str
    supervised: bool
    canApply: bool
    "If the panel can update itself; only seen as `False`."
    canChangeStream: bool
    note: Optional[str]
    "Only seen as `None`."
    installationVersion: str
    spiresBehind: list[Any]
    "Only seen empty."
    canUpdateSpires: bool
    packageManaged: bool
    rolledBack: Optional[bool]
    "Only seen as `None`."


class UserResponse(TypedDict):
    """One user from ``GET /api/users``; getting, creating or updating one answers with it too."""

    id: str
    userName: str
    displayName: Optional[str]
    email: str
    "AMP doesn't check it's an email address."
    roleIds: list[str]
    "A deleted role's ID stays here."
    isAdmin: bool
    suspended: bool
    passwordExpires: bool
    requirePasswordChange: bool
    createdAt: str
    lastLoginAt: Optional[str]


class ValidationErrorResponse(TypedDict):
    """A list of refusals, eg. a password the policy rejects (400)."""

    errors: list[str]


class WrappedID(TypedDict):
    """An ID AMP sends inside an object, eg. a running task's `correlationId`."""

    value: str


LoginResponse = Union[TokenResponse, PasswordChangeRequiredResponse, PasskeyRequiredResponse]
# A query string; a list value repeats its key, so {"shard": ["a", "b"]} is sent as shard=a&shard=b.
QueryParameters = Mapping[str, Union[str, int, Sequence[str]]]
