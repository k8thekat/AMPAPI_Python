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
from typing import Any, Literal, NotRequired, Optional, TypedDict, Union

# Only the `*Changes` keyword argument types use these. Imported normally, so `typing.get_type_hints` still resolves them.

# Typed, as pyright stops inferring a tuple's items past 256 of them
__all__: tuple[str, ...] = (
    "AnalyticsAddressGroup",
    "AnalyticsAddressSearchResponse",
    "AnalyticsAddressSummary",
    "AnalyticsAddressUser",
    "AnalyticsAddressUsersResponse",
    "AnalyticsConnectedResponse",
    "AnalyticsConnectedUser",
    "AnalyticsCountryUsage",
    "AnalyticsForgetResponse",
    "AnalyticsGameUsage",
    "AnalyticsMinecraftProfile",
    "AnalyticsPeriod",
    "AnalyticsProfilesResponse",
    "AnalyticsRule",
    "AnalyticsServerInfo",
    "AnalyticsServerUsage",
    "AnalyticsSession",
    "AnalyticsSessionsResponse",
    "AnalyticsSteamBans",
    "AnalyticsSteamProfile",
    "AnalyticsTopUser",
    "AnalyticsTotals",
    "AnalyticsUserAddress",
    "AnalyticsUserAddressesResponse",
    "AnalyticsUserMatch",
    "AnalyticsUserSessionsResponse",
    "AnalyticsUsersResponse",
    "AuditActionCount",
    "AuditEvent",
    "AuditFacetsResponse",
    "AuditOriginCount",
    "AuditOriginName",
    "AuditPageResponse",
    "AuditRoot",
    "AuditRootsPageResponse",
    "AuditSeverityName",
    "AuditTreeNode",
    "AuditTreeResponse",
    "AuditUserCount",
    "BrandingResponse",
    "BusExpandResponse",
    "BusFirewallOutcome",
    "BusJoinInfo",
    "CapabilitiesResponse",
    "CodedErrorResponse",
    "CredentialKind",
    "CredentialRequest",
    "CredentialResponse",
    "CredentialVisibility",
    "DatastoreRequest",
    "DatastoreResponse",
    "DatastoreUsage",
    "DeletedUserResponse",
    "DiagnosticsResponse",
    "DownloadTicketResponse",
    "ExpiredPasswordRequest",
    "FileACLChange",
    "FilePrincipal",
    "FileVerb",
    "FirewallGatewayRoute",
    "FirewallGatewayRouteKey",
    "FirewallRejectedGatewayRoute",
    "FirewallRejectedInterface",
    "FirewallRejectedPeer",
    "FirewallRejectedRule",
    "FirewallResponse",
    "FirewallRule",
    "FirewallStatus",
    "FirewallWireGuardInterface",
    "FirewallWireGuardInterfaceStatus",
    "FirewallWireGuardPeer",
    "FirewallWithheldRule",
    "GatewayConflict",
    "GatewayEgressRequest",
    "GatewayEligibilityResponse",
    "GatewayPreflightResponse",
    "GatewayRequest",
    "GatewayResponse",
    "GatewayStatus",
    "HTTPSCheck",
    "HTTPSCheckResponse",
    "HTTPSSetupStatusResponse",
    "HTTPSStateResponse",
    "HealthStatusResponse",
    "HubTokenResponse",
    "InviteAcceptRequest",
    "InviteAcceptedResponse",
    "InvitePreviewResponse",
    "InviteRequest",
    "InviteResponse",
    "InviteTokenResponse",
    "LicenceAgreementResponse",
    "LicenceQueryResponse",
    "LicenceResponse",
    "LicenceStatusResponse",
    "LicenceTermsAcceptance",
    "LicenceTermsRequest",
    "LoginRequest",
    "LoginResponse",
    "MessageBusService",
    "MessageBusStatsResponse",
    "MessageErrorResponse",
    "MonitoringThresholdsResponse",
    "NetworkProbe",
    "PanelUpdateResponse",
    "PasskeyFlowResponse",
    "PasskeyLoginRequest",
    "PasskeyRegisterRequest",
    "PasskeyRegisteredResponse",
    "PasskeyRequiredResponse",
    "PasskeyResponse",
    "PasswordChangeRequest",
    "PasswordChangeRequiredResponse",
    "PasswordPolicyResponse",
    "PermissionNode",
    "PermissionsResponse",
    "PlatformWarningResponse",
    "PortClaimResponse",
    "PortProtocol",
    "PreferencesChanges",
    "PreviewStatus",
    "PreviewUpdate",
    "Principal",
    "ProblemDetailsResponse",
    "ProfileRequest",
    "ProfileResponse",
    "ProfileSessionResponse",
    "PublicationRequest",
    "PublicationResponse",
    "PublicationStatus",
    "PublicationUpdateRequest",
    "QueryParameters",
    "ReasonErrorResponse",
    "RecoveryCodesResponse",
    "RecoveryCodesStatusResponse",
    "RevokedSessionsResponse",
    "RoleRequest",
    "RoleResponse",
    "RoleUpdateRequest",
    "SSHKeyRequest",
    "SSHKeyResponse",
    "ScheduleCatalogResponse",
    "ScheduleCatalogTask",
    "ScheduleCatalogTrigger",
    "ScheduleCondition",
    "ScheduleDefinition",
    "ScheduleEmit",
    "ScheduleRefusal",
    "ScheduleRetryPolicy",
    "ScheduleRunResponse",
    "ScheduleStatus",
    "ScheduleStep",
    "ScheduleStepOutcome",
    "ScheduleSwitchCase",
    "ScheduleTaskParameter",
    "ScheduleTrigger",
    "ScheduleWithheld",
    "SecondFactorRequest",
    "SettingAction",
    "SettingActionResponse",
    "SettingCandidate",
    "SettingSpec",
    "SettingValues",
    "SettingsManifestResponse",
    "SettingsSaveResponse",
    "SetupAdminRequest",
    "SetupNetworkResponse",
    "SetupProvisionStatusResponse",
    "ShardAddress",
    "ShardAgentResponse",
    "ShardAppConfig",
    "ShardArchiveInfoResponse",
    "ShardArchiveRequest",
    "ShardAttentionResponse",
    "ShardCloneRequest",
    "ShardCloneResponse",
    "ShardConfigImportResponse",
    "ShardConsoleRequest",
    "ShardCreateRequest",
    "ShardCreatedResponse",
    "ShardCredentialResponse",
    "ShardCustomPort",
    "ShardCustomPortRequest",
    "ShardDetailsRequest",
    "ShardEndpointResponse",
    "ShardExtractRequest",
    "ShardExtractResponse",
    "ShardFileACLResponse",
    "ShardFileContentResponse",
    "ShardFileIgnoresResponse",
    "ShardFileResponse",
    "ShardFileStartResponse",
    "ShardImportResponse",
    "ShardImportSkippedFile",
    "ShardInfraChanges",
    "ShardInfraSettingsResponse",
    "ShardManagedFileResponse",
    "ShardMigrationRequest",
    "ShardMigrationTargetResponse",
    "ShardPortAssignments",
    "ShardPortOutcome",
    "ShardPortResponse",
    "ShardResponse",
    "ShardSFTPResponse",
    "ShardScheduleRequest",
    "ShardScheduleResponse",
    "ShardSettingCandidatesResponse",
    "ShardSettingResponse",
    "ShardSleepStatus",
    "ShardStateMetrics",
    "ShardUpdateResponse",
    "ShardUploadChunkResponse",
    "ShardUploadSessionResponse",
    "ShardUsage",
    "SnapshotMetaRequest",
    "SnapshotRequest",
    "SnapshotSettingsRequest",
    "SnapshotSettingsResponse",
    "SpireCPU",
    "SpireEnrollmentAdmission",
    "SpireEnrollmentCreatedResponse",
    "SpireEnrollmentHostResponse",
    "SpireEnrollmentRequest",
    "SpireEnrollmentResponse",
    "SpireEnrollmentRevokeRequest",
    "SpireExpiredPurgeResponse",
    "SpireIPAddress",
    "SpireIPOptionResponse",
    "SpireImportBlockedItem",
    "SpireImportDiscoveredPort",
    "SpireImportEvidence",
    "SpireImportItem",
    "SpireImportLiveness",
    "SpireImportMatch",
    "SpireImportPreflightResponse",
    "SpireImportReadyItem",
    "SpireImportRecovery",
    "SpireImportRequest",
    "SpireImportResponse",
    "SpireImportScanRequest",
    "SpireImportScanResponse",
    "SpireImportScanServer",
    "SpireImportSize",
    "SpireImportUnreadable",
    "SpireJavaRuntime",
    "SpirePlatform",
    "SpirePortResponse",
    "SpireResponse",
    "SpireStartupEntry",
    "SpireStartupResponse",
    "SpireStorageResponse",
    "SpireUsageIntervalResponse",
    "SpireUsageResponse",
    "SystemBusResponse",
    "TaskResponse",
    "TaskStep",
    "TaskStepProgress",
    "TemplateConfigFile",
    "TemplateConfigSection",
    "TemplateConsole",
    "TemplateEvent",
    "TemplateLifecycle",
    "TemplateManagement",
    "TemplateMetadata",
    "TemplatePort",
    "TemplatePortReferences",
    "TemplateResponse",
    "TemplateSourceResponse",
    "TemplateSyncResponse",
    "TemplateUpdateStage",
    "TemplateVersionSource",
    "TokenClaims",
    "TokenResponse",
    "TunnelEnd",
    "TunnelFrontHost",
    "TunnelFrontResponse",
    "TunnelResponse",
    "TunnelStatus",
    "UpdateRolledBack",
    "UpdateSpireBehind",
    "UpdateStatusResponse",
    "UserCreateRequest",
    "UserResponse",
    "UserUpdateRequest",
    "ValidationErrorResponse",
    "WrappedID",
)


# TODO: Check against a live capture; typed from AMP's OpenAPI `AddressGroup` alone (#3-56.3af).
# Every address search so far found no address, and AMP 3.0.0 and 3.0.1 answer a range search with a 500.
class AnalyticsAddressGroup(TypedDict):
    """One address an address search found and the players seen at it, from `AnalyticsAddressSearchResponse.addresses`."""

    address: str
    network: str
    kind: str
    """``"Public"``, ``"Tunnel"``, ``"Shared"`` (carrier-grade NAT), ``"Private"`` or ``"Loopback"``."""
    recovered: bool
    "If AMP followed every session at the address back through its own relays or not."
    users: list[AnalyticsAddressUser]


class AnalyticsAddressSearchResponse(TypedDict):
    """``GET /api/analytics/addresses``, the addresses matching one address searched for, and their players."""

    range: str
    "What AMP searched, eg. the address as given."
    kind: str
    """``"Public"``, ``"Tunnel"``, ``"Shared"`` (carrier-grade NAT), ``"Private"`` or ``"Loopback"``."""
    users: int
    "How many players were seen across every address found."
    serverInfo: dict[str, AnalyticsServerInfo]
    "A shard ID to the shard's name and game."
    isDemo: bool
    addresses: list[AnalyticsAddressGroup]
    "The addresses found, the most recently used address first."


class AnalyticsAddressSummary(TypedDict):
    """An address searched for, from `AnalyticsUsersResponse.address`."""

    range: str
    kind: str
    """``"Public"``, ``"Tunnel"``, ``"Shared"`` (carrier-grade NAT), ``"Private"`` or ``"Loopback"``."""
    addresses: int
    users: int


# TODO: Check against a live capture; typed from AMP's OpenAPI `AddressUser` alone (#3-56.3af).
# Every address read so far listed no players.
class AnalyticsAddressUser(TypedDict):
    """One player seen at an address, from `AnalyticsAddressUsersResponse.users` and `AnalyticsAddressGroup.users`."""

    userKey: str
    "The key the other analytics calls take."
    displayName: Optional[str]
    "`None` unless the logged in user may see names on the player's shards."
    firstSeen: str
    lastSeen: str
    sessions: int
    shards: list[str]
    "The shard IDs the player was seen on from the address."


class AnalyticsAddressUsersResponse(TypedDict):
    """``GET /api/analytics/addresses/users``, the players seen at one address."""

    address: str
    network: str
    "What AMP matched on: the address itself, or an IPv6 address's /64 network."
    kind: str
    """``"Public"``, ``"Tunnel"``, ``"Shared"`` (carrier-grade NAT), ``"Private"`` or ``"Loopback"``."""
    users: list[AnalyticsAddressUser]
    "The players, the most recently seen player first."
    serverInfo: dict[str, AnalyticsServerInfo]
    "A shard ID to the shard's name and game."
    isDemo: bool


class AnalyticsConnectedResponse(TypedDict):
    """``GET /api/analytics/connected/{shard_id}``, what a shard knows about one player connected to it now."""

    user: AnalyticsConnectedUser
    minecraft: Optional[AnalyticsMinecraftProfile]
    "`None` for a player who isn't on Minecraft."
    profileState: str
    """How far the profile lookups got, as `AnalyticsProfilesResponse.state`, or ``"none"`` for a player with no ID
    AMP can look up."""
    analyticsKey: Optional[str]
    "`None` unless analytics has seen the player and the logged in user may see who the shard's players are."
    userKey: Optional[str]
    "The key the other analytics calls take, `None` unless the logged in user may see addresses."
    addressKind: Optional[str]
    """``"Public"``, ``"Tunnel"``, ``"Shared"`` (carrier-grade NAT), ``"Private"`` or ``"Loopback"``. `None` when AMP
    doesn't know the address, or the logged in user may not see addresses."""
    # TODO: Check these three against a live capture; typed from AMP's OpenAPI `ConnectedProfile` alone (#3-56.3af).
    # A Minecraft player alone at a LAN address left them `None`.
    steam: Optional[AnalyticsSteamProfile]
    "The player's Steam profile, `None` unless the player has a Steam ID that AMP could look up."
    othersAtAddress: Optional[int]
    """How many other players connected from the player's address. `None` unless the logged in user holds
    `analytics.addresses` on the shard and the address is a kind where the count means something."""
    recoveredAddress: Optional[str]
    "The address the player really connected from, when the shard saw a relay's address and AMP followed the relay back."


class AnalyticsConnectedUser(TypedDict):
    """The player in `AnalyticsConnectedResponse.user`, as the shard lists them (see `ShardPlayer`)."""

    name: str
    id: str
    sessionId: str
    endpoint: Optional[str]
    "The address and port the player connected from, `None` when the app doesn't report an address."
    joinedAt: str
    idKind: str
    """eg. ``"minecraft-uuid"``."""


class AnalyticsCountryUsage(TypedDict):
    """One country the players came from, from `AnalyticsSessionsResponse.countries`."""

    country: str
    """A lower-case ISO 3166-1 alpha-2 code, eg. ``"us"``. A player on a LAN address was counted as ``"xx"``."""
    sessions: int
    sessionsPercent: float
    minutes: float
    minutesPercent: float
    users: Optional[int]
    "How many players the country sent, `None` when AMP answered from its precomputed totals."


class AnalyticsForgetResponse(TypedDict):
    """``DELETE /api/analytics/sessions/users/{key}``, what was erased about one player."""

    records: int
    days: int


class AnalyticsGameUsage(TypedDict):
    """One game the players played, across every shard running the game, from `AnalyticsSessionsResponse.games`."""

    game: str
    """The template slug, eg. ``"minecraft-java"``."""
    sessions: int
    sessionsPercent: float
    minutes: float
    minutesPercent: float
    users: int
    "How many players, counting a player on two shards of the game once."
    servers: int
    "How many of the game's shards had a player on them."


class AnalyticsMinecraftProfile(TypedDict):
    """A player's Minecraft profile, from `AnalyticsProfilesResponse.minecraft` and `AnalyticsConnectedResponse`."""

    uuid: str
    name: str
    skinHash: Optional[str]
    "What `AnalyticsModule.get_analytics_skin` takes, `None` for a default skin."
    slim: bool
    "If the skin uses the slim arms model or not."
    hasCape: bool


class AnalyticsPeriod(TypedDict):
    """A stretch of time and the players in it, from `AnalyticsSessionsResponse`."""

    start: str
    end: str
    users: int


class AnalyticsProfilesResponse(TypedDict):
    """``GET /api/analytics/profiles``, players' Steam and Minecraft profiles, keyed by the player's key.

    A shard only keeps profiles with its `userSpecificData` setting on.
    """

    # TODO: Check against a live capture; typed from AMP's OpenAPI `ProfilesAnswer` and `SteamProfile` alone (#3-56.3af).
    # Only a Minecraft player has been seen, so every capture has `steam` empty.
    steam: dict[str, AnalyticsSteamProfile]
    minecraft: dict[str, AnalyticsMinecraftProfile]
    state: str
    """How far the profile lookups got.

    - ``"complete"``.
    - ``"pending"``: some players are still to be looked up, a few at a time.
    - ``"keyRejected"``: Steam refused the Web API key, so AMP read the slower community profile instead.
    - ``"unreachable"``.
    - ``"off"``: the lookups are turned off in the settings.
    - ``"notLicensed"``: the licence doesn't include profiles, which need AMP Professional Edition or above.
    """
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


class AnalyticsServerUsage(TypedDict):
    """How busy one shard was, from `AnalyticsSessionsResponse.servers` and `AnalyticsUserSessionsResponse.servers`."""

    shardId: str
    sessions: int
    sessionsPercent: float
    minutes: float
    minutesPercent: float
    users: int
    "How many players were on the shard."


class AnalyticsSession(TypedDict):
    """One player's time on one shard, from `AnalyticsUserSessionsResponse.sessions`."""

    sessionRef: str
    shardId: str
    userKey: str
    idKind: str
    """What the player's ID is, eg. ``"minecraft-uuid"``."""
    country: str
    """A lower-case ISO 3166-1 alpha-2 code, eg. ``"us"``. A player on a LAN address was counted as ``"xx"``."""
    startedAt: str
    endedAt: str
    running: bool
    "If the session was still open when AMP read the records or not."
    displayName: Optional[str]
    "`None` when the shard stores no user-specific data."


class AnalyticsSessionsResponse(TypedDict):
    """``GET /api/analytics/sessions``, the player summary for the analytics page."""

    window: dict[str, str]
    """``"from"`` and ``"to"``, ISO 8601; the last 30 days unless asked."""
    current: AnalyticsTotals
    previous: AnalyticsTotals
    change: dict[str, Optional[float]]
    "The `AnalyticsTotals` keys, each the percentage change; `None` where the previous window had nothing to compare."
    activity: list[AnalyticsPeriod]
    "One a day."
    countries: list[AnalyticsCountryUsage]
    topUsers: list[AnalyticsTopUser]
    busiest: AnalyticsPeriod
    quietest: AnalyticsPeriod
    servers: list[AnalyticsServerUsage]
    "The busiest shard first."
    games: list[AnalyticsGameUsage]
    "The busiest game first."
    isDemo: bool
    """`True` when the numbers are made up: the licence doesn't include analytics, or a debug build of AMP was asked
    for its demo data."""
    serverInfo: dict[str, AnalyticsServerInfo]
    "A shard ID to the shard's name and game."
    rule: AnalyticsRule


# TODO: Check against a live capture; typed from AMP's OpenAPI `SteamBans` alone (#3-56.3af).
# No Steam player has been seen.
class AnalyticsSteamBans(TypedDict):
    """What Steam says about a player's bans, from `AnalyticsSteamProfile.bans`. Bans are public on a private profile too."""

    vacBanned: bool
    vacBans: Optional[int]
    "How many VAC bans, `None` when AMP read the community profile, which only says if there's a ban."
    gameBans: Optional[int]
    "How many bans the games' own developers gave, `None` when not known."
    daysSinceLastBan: Optional[int]
    "`None` when not known, or when there's no ban."
    communityBanned: Optional[bool]
    "`None` when not known."
    tradeBanned: bool
    any: bool
    "If there's a ban of any kind on record or not."


# TODO: Check against a live capture; typed from AMP's OpenAPI `SteamProfile` alone (#3-56.3af).
# No Steam player has been seen.
class AnalyticsSteamProfile(TypedDict):
    """A player's Steam profile, from `AnalyticsProfilesResponse.steam` and `AnalyticsConnectedResponse.steam`."""

    steamId: str
    "The Steam64 ID."
    personaName: Optional[str]
    "The name the player goes by on Steam now."
    avatarHash: Optional[str]
    "What `AnalyticsModule.get_analytics_avatar` takes, `None` for Steam's default avatar."
    visibility: str
    """Who may see the profile's details: ``"Unknown"``, ``"Private"``, ``"FriendsOnly"`` or ``"Public"``."""
    createdAt: Optional[str]
    "When the Steam account was made, `None` unless the profile is public."
    countryCode: Optional[str]
    "The lower-case ISO 3166-1 code on the profile, `None` unless the profile is public and has a country set."
    bans: Optional[AnalyticsSteamBans]
    "`None` when Steam didn't answer."
    limited: Optional[bool]
    """If the account never spent money on Steam or not. Only the community profile says, so a profile read from the
    Steam Web API holds `None`."""
    source: str
    "Where AMP read the profile from, the Steam Web API or the community profile page."
    profileUrl: Optional[str]
    "The profile page by Steam64 ID, so the link survives a rename."


class AnalyticsTopUser(TypedDict):
    """A player who spent the most time on the shards, from `AnalyticsSessionsResponse.topUsers`."""

    userKey: str
    "The key the other analytics calls take."
    displayName: Optional[str]
    "`None` when the shard stores no user-specific data."
    sessions: int
    minutes: float
    percent: float
    servers: int
    """How many shards the time was spent on. AMP only counts several shards for an ID that names the same player
    on every shard, eg. a Steam ID. A player's name is only matched within a single shard."""
    online: bool
    "If the player is connected right now or not."


class AnalyticsTotals(TypedDict):
    """Player totals from `AnalyticsSessionsResponse` and `AnalyticsUserSessionsResponse`."""

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


class AnalyticsUserAddress(TypedDict):
    """One address a player was seen at, from `AnalyticsUserAddressesResponse.addresses`."""

    address: str
    network: str
    token: str
    kind: str
    """eg. ``"Private"`` or ``"Public"``."""
    country: str
    firstSeen: str
    lastSeen: str
    sessions: int
    shards: list[str]
    "The shard IDs the player was seen on from it."
    recovered: bool
    # TODO: Check against a live capture; typed from AMP's OpenAPI `AddressUse` alone (#3-56.3af).
    # A player alone at an address left it `None`.
    otherUsers: Optional[int]
    """How many other players the logged in user can see connected from the address, `None` where AMP doesn't match
    players by the address."""


class AnalyticsUserAddressesResponse(TypedDict):
    """``GET /api/analytics/users/{key}/addresses``, the addresses one player was seen at.

    A shard only keeps addresses with its `userSpecificData` setting on.
    """

    addresses: list[AnalyticsUserAddress]
    serverInfo: dict[str, AnalyticsServerInfo]
    isDemo: bool


class AnalyticsUserSessionsResponse(TypedDict):
    """``GET /api/analytics/sessions/users/{key}``, one player's history.

    An unknown player answers 200 with everything empty.
    """

    userKey: str
    displayName: Optional[str]
    totals: AnalyticsTotals
    servers: list[AnalyticsServerUsage]
    "The shards the player spent the window on, the busiest shard first."
    sessions: list[AnalyticsSession]
    "The player's sessions in the window, the newest session first."
    firstSeen: Optional[str]
    lastSeen: Optional[str]
    isActive: bool
    recentVisits: int
    rule: AnalyticsRule
    serverInfo: dict[str, AnalyticsServerInfo]
    isDemo: bool
    """`True` for a made-up player from a debug build of AMP's demo data."""


class AnalyticsUserMatch(TypedDict):
    """A player a search found, from `AnalyticsUsersResponse.users`."""

    userKey: str
    "The key the other analytics calls take."
    displayName: Optional[str]
    "`None` when the shard stores no user-specific data."
    userId: Optional[str]
    idKind: str
    """What the player's ID is, eg. ``"minecraft-uuid"``."""
    shards: list[str]
    "The shard IDs the player was seen on."
    lastSeen: str


class AnalyticsUsersResponse(TypedDict):
    """``GET /api/analytics/users``, a player search."""

    users: list[AnalyticsUserMatch]
    serverInfo: dict[str, AnalyticsServerInfo]
    isDemo: bool
    address: Optional[AnalyticsAddressSummary]
    "A summary of the address when the search text is an address, else `None`."


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
    """An `AuditSeverity` number: 0 ``"Info"``, 1 ``"Warning"`` or 2 ``"Security"``, the names the `min_severity` filter
    takes."""
    principal: Principal
    "Who or what did it."
    action: str
    """eg. ``"ShardCreated"`` or ``"SharedCredentialDeleted"``."""
    targetType: str
    """eg. ``"Shard"``, ``"User"`` or ``"Setting"``."""
    targetId: str
    taskId: Optional[str]
    correlationId: Optional[WrappedID]
    """Shared by every event in one flow, see `AuditModule.get_audit_tree`. `None` only for an event written before
    AMP kept flows."""
    actionId: Optional[WrappedID]
    "`None` only for an event written before AMP kept actions."
    causationActionId: Optional[WrappedID]
    "The action that led to this event's action, `None` for the event that started the flow."
    origin: int
    """An `AuditOrigin` number: 0 ``"System"``, 1 ``"User"``, 2 ``"UserFlow"``, 3 ``"Scheduled"`` or 4
    ``"Impersonation"``, the names the `origin` filter takes."""
    rootPrincipal: Optional[Principal]
    "Who started the flow. `None` only for an event written before AMP kept flows, where `principal` stands in."
    details: Optional[str]
    "More about the event, as JSON in a string."
    originIp: Optional[str]
    "The address of the request behind the event, `None` for an event AMP raised by itself."
    originSpireId: Optional[str]
    "The spire that raised the event, `None` only for an event written before AMP kept the spire."
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
    """An `AuditOrigin` number, eg. 1 for ``"User"``."""
    count: int


class AuditPageResponse(TypedDict):
    """``GET /api/audit``, one page of the audit log, newest first unless asked."""

    total: int
    "How many events match, over every page."
    page: int
    pageSize: int
    "50 unless asked; AMP caps it at 200."
    caughtUp: bool
    "`False` while AMP is still loading the audit log into its index, so the page may be missing events."
    items: list[AuditEvent]


class AuditRoot(TypedDict):
    """One flow of events, from `AuditRootsPageResponse.items`."""

    correlationId: str
    "The ID `AuditModule.get_audit_tree` takes."
    root: AuditEvent
    "The event that started the flow."
    eventCount: int
    startedAt: str
    endedAt: str
    maxSeverity: int
    "The highest `AuditSeverity` number of any event in the flow."
    rootMissing: bool
    """`True` when AMP's index no longer holds the flow's first events, so the earliest event it holds is `root`."""


class AuditRootsPageResponse(TypedDict):
    """``GET /api/audit/roots``, one page of the audit log grouped into flows."""

    total: int
    page: int
    pageSize: int
    caughtUp: bool
    "`False` while AMP is still loading the audit log into its index, so the page may be missing flows."
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
    """eg. ``"proteus"``, lower case where the settings say ``"Proteus"``."""


class BusExpandResponse(TypedDict):
    """``POST /api/system/bus/expand``, the message bus once it's open to other machines."""

    joinInfo: BusJoinInfo
    "How to reach the bus now, as `SystemBusResponse.joinInfo` reads from then on."
    firewall: BusFirewallOutcome


class BusFirewallOutcome(TypedDict):
    """The port AMP opened on the host for the message bus, from `BusExpandResponse.firewall`."""

    outcome: str
    """``"Open"``, ``"NotManaged"``, ``"Pending"`` or ``"WriteFailed"``."""
    port: int
    "eg. 4222."
    generation: Optional[int]
    """The firewall state that opens the port, `None` unless `outcome` is ``"Open"``."""
    agentRunning: bool
    "If AMP's system agent, which opens the port, was running; without it the port has to be opened by hand."


class BusJoinInfo(TypedDict):
    """What another machine needs to reach the message bus, from `SystemBusResponse.joinInfo`."""

    servers: list[str]
    """eg. ``["tls://127.0.0.1:4222"]``, then the machine's own network address once the bus is open to other machines."""
    prefix: str
    hostCandidates: list[str]
    caCert: str
    joinBlob: str
    "Empty, even with the bus open; the join file comes from `EnrollmentModule.create_spire_enrollment`."


class CapabilitiesResponse(TypedDict):
    """``GET /api/auth/capabilities``, which needs no session."""

    passkeysAvailable: bool
    "If passkeys work for this request; it depends on the address the request came in on."
    passkeyStatus: str
    """eg. ``"NotConfigured"`` (no public address set), ``"OriginMismatch"`` (not asked at that address),
    ``"IpAddressHost"`` (the public address is an IP address) or ``"Eligible"``."""
    passkeyMessageKey: str
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


class CredentialRequest(TypedDict):
    """The body of ``POST /api/credentials``."""

    kind: CredentialKind
    title: str
    username: str
    secret: str
    visibility: NotRequired[CredentialVisibility]


class CredentialResponse(TypedDict):
    """One stored secret shards can use, from ``GET /api/credentials``; AMP never sends the secret back."""

    id: str
    title: str
    kind: str
    """One of ``"SteamCmd"``, ``"Smtp"``, ``"DiscordWebhook"`` or ``"ApiKey"``."""
    visibility: str
    """``"Private"`` or ``"Public"``."""
    mine: bool
    "If the logged in user made it."
    username: Optional[str]
    "`None` for anyone but the user who made it."
    shardCount: Optional[int]
    "How many shards use it; `None` for anyone but the user who made it and a ``credentials.manage`` holder."
    createdAt: str
    updatedAt: str


class DatastoreRequest(TypedDict):
    """The body of ``POST /api/spires/{id}/datastores``, which makes a datastore, or with `id` replaces that datastore whole."""

    id: NotRequired[str]
    "The datastore to replace. AMP makes a new datastore with this ID when the spire has no datastore by that ID."
    name: str
    path: str
    isDefault: bool
    enabled: bool
    softLimitMb: int
    tags: list[str]


class DatastoreResponse(TypedDict):
    """One of a spire's datastores, the folders shards are kept in, from ``GET /api/spires/{id}/datastores``."""

    id: str
    name: str
    path: str
    """eg. ``"/opt/cubecoders/amp3/data/Datastores/Default"``. AMP doesn't check the folder exists."""
    isDefault: bool
    enabled: bool
    "If new shards can be put here or not."
    softLimitMb: int
    """0 for no limit. Once the scanned use reaches it, AMP refuses new shards here (the import preflight's
    `batchBlock` 3); the shards already here keep running and can still grow."""
    tags: list[str]
    """The user's own labels, eg. ``["scratch"]``, and the storage medium where AMP detected it (``"NVMe"``, ``"SSD"``
    or ``"HDD"``), as on a spire's ``"Default"`` datastore."""


class DatastoreUsage(TypedDict):
    """One datastore's disk use, from `SpireUsageResponse.datastores`."""

    datastoreId: str
    totalUsedMb: int
    driveFreeMb: int
    driveTotalMb: int
    shards: list[ShardUsage]


class DeletedUserResponse(TypedDict):
    """``DELETE /api/users/{id}``, which answers 200 with a body where other deletes answer 204."""

    # TODO: Check against a live capture; typed from AMP's OpenAPI `UserDeletedDto` and `ApiError` alone (#3-56.3ab).
    # Every delete so far had no warnings; a warning needs a cleanup step to fail.
    warnings: list[CodedErrorResponse]
    "The parts of the user's data AMP couldn't remove. The user is deleted either way."


class DiagnosticsResponse(TypedDict):
    """``GET /api/support/diagnostics``, the details a support request asks for."""

    ampVersion: str
    codename: str
    buildCommit: str
    configuration: str
    """eg. ``"Production"``."""
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
    """The message bus, ``"Connected"`` or ``"Disconnected"``."""
    # TODO: Drop the field doc once AMP reports its uptime (U11).
    # AMP 3.0.0 sends 0. AMP 3.0.1 counted from about the first diagnostics request on a panel up for days.
    uptimeSeconds: int
    """Not the panel's uptime.
    - AMP 3.0.0 sends 0 however long the panel has run.
    - AMP 3.0.1 counts up, but not from when the panel started."""
    auditOrphanWrites: int
    auditRelaunchCarriedWrites: int
    ipv6: str
    """``"Unknown"``, ``"Unavailable"``, ``"Working"`` or ``"BlackHoled"``, with the reason in `ipv6Detail`."""
    ipv6Detail: str
    containerRuntime: str
    """``"Podman"`` or ``"Docker"``, empty when neither answered."""
    containerRuntimeVersion: str
    containerRuntimeVerdict: str
    """``"Unknown"`` before the first check, then ``"NotFound"``, ``"Usable"`` or ``"Unusable"``."""
    # TODO: Check against a live capture; typed from AMP's OpenAPI `DiagnosticsDto` alone (#3-56.2h).
    # Every capture has it `None`, with the runtime usable.
    containerRuntimeReason: Optional[CodedErrorResponse]
    "The coded reason behind `containerRuntimeVerdict`, when AMP gives a reason."


class DownloadTicketResponse(TypedDict):
    """A download ticket, from ``POST /api/shards/{id}/files/download-ticket`` and the other ``download-ticket`` routes."""

    ticket: str
    """Sent as the download's `ticket` query parameter. AMP takes a ticket once, from the session that asked for it."""
    expiresAt: str
    """When AMP stops taking the ticket, 60 seconds after it was made."""


class ExpiredPasswordRequest(TypedDict):
    """The body of ``POST /api/auth/change-expired-password``."""

    username: str
    currentPassword: str
    newPassword: str


class FileACLChange(TypedDict):
    """One change `ShardModule.set_shard_file_acl` sends, as the web panel sends it."""

    principalId: str
    "A user's or a role's ID, a `FilePrincipal.id`."
    verb: Literal["read", "write", "delete"]
    state: Literal["allow", "deny", "inherit"]
    """``"inherit"`` clears an explicit state, so the path follows its folder again."""


class FilePrincipal(TypedDict):
    """A user or role and what they may do to a path, from `ShardFileACLResponse.principals`."""

    id: str
    name: str
    isUser: bool
    verbs: list[FileVerb]


class FileVerb(TypedDict):
    """One action a principal may or may not take on a path, from `FilePrincipal.verbs`."""

    verb: str
    """``"read"``, ``"write"`` or ``"delete"``."""
    state: str
    """eg. ``"allow"`` or ``"deny"``."""
    explicit: bool
    "If it's set on this path rather than inherited."
    source: Optional[str]
    "The path that sets it, once `explicit`; `None` otherwise."
    inheritedState: str
    "What the verb falls back to once this path's own rule is cleared, from the folders above."
    inheritedSource: Optional[str]
    """The folder whose rule gives `inheritedState`, eg. ``"my_folder"``; `None` when none does."""


class FirewallGatewayRoute(TypedDict):
    """A gateway's port AMP's system agent forwards on the front spire, from `FirewallStatus.gatewayApplied`."""

    interfaceName: str
    """The WireGuard tunnel it goes over, eg. ``"amp-7f7e2fff"``."""
    publicPort: int
    protocol: str
    """``"Tcp"`` or ``"Udp"``."""
    targetIp: str
    "The shard's address on the tunnel, its gateway's `GatewayStatus.address`."
    targetPort: int
    key: FirewallGatewayRouteKey


class FirewallGatewayRouteKey(TypedDict):
    """The protocol and port that tell gateway routes apart on the front spire, from `FirewallGatewayRoute.key`."""

    protocol: str
    """``"Tcp"`` or ``"Udp"``."""
    publicPort: int


# TODO: Check against a live capture; typed from AMP's OpenAPI `RejectedGatewayRoute` alone (#3-56.2ap).
# Every capture has `gatewayRejected` empty.
class FirewallRejectedGatewayRoute(TypedDict):
    """A gateway route AMP's system agent couldn't apply, from `FirewallStatus.gatewayRejected`."""

    route: FirewallGatewayRoute
    reason: str


class FirewallRejectedInterface(TypedDict):
    """A WireGuard tunnel AMP's system agent couldn't bring up, from `FirewallStatus.wireGuardRejected`."""

    interface: FirewallWireGuardInterface
    reason: str
    """eg. ``"The file does not exist."`` while a new tunnel is set up."""


# TODO: Check against a live capture; typed from AMP's OpenAPI `RejectedPeer` alone (#3-56.2ap).
# Every capture has `wireGuardPeersRejected` empty.
class FirewallRejectedPeer(TypedDict):
    """A WireGuard peer AMP's system agent couldn't add, from `FirewallStatus.wireGuardPeersRejected`."""

    peer: FirewallWireGuardPeer
    reason: str


# TODO: Check against a live capture; typed from AMP's OpenAPI `RejectedRule` alone (#3-56.2ap).
# Every capture has `rejected` empty.
class FirewallRejectedRule(TypedDict):
    """A port AMP's system agent couldn't open, from `FirewallStatus.rejected`."""

    rule: FirewallRule
    reason: str


class FirewallResponse(TypedDict):
    """``GET /api/networking/firewall``, the firewall rules AMP's system agent keeps on the panel's own spire.

    Another spire's firewall can't be read yet.
    """

    running: bool
    "If AMP's system agent runs here; `False` when none is installed, or its status is over five minutes old."
    status: Optional[FirewallStatus]
    "What the agent last applied, `None` when no agent has run here and AMP manages no firewall rules."
    # TODO: Check against a live capture; typed from AMP's OpenAPI `FirewallStatusDto` alone (#3-56.2ap).
    # Every capture has it empty; AMP refuses a shard port it holds itself up front (`shards.error.portReservedByAmp`).
    withheld: list[FirewallWithheldRule]
    "A shard's ports AMP left closed, as it holds the numbers itself."


class FirewallRule(TypedDict):
    """One port AMP opened, from `FirewallStatus.applied`."""

    port: int
    protocol: str
    """``"Tcp"`` or ``"Udp"``."""
    tag: str
    """eg. ``"panel-web"``, ``"nats"`` or ``"sftp"``."""
    label: str
    """eg. ``"AMP panel"``."""
    scope: str
    """``"Any"`` or ``"HostOnly"``."""


class FirewallStatus(TypedDict):
    """The firewall's state as AMP's system agent last applied it, from `FirewallResponse.status`."""

    schema: int
    generation: int
    backend: str
    """eg. ``"iptables+ip6tables"``."""
    healthy: bool
    applied: list[FirewallRule]
    # TODO: Check these two against a live capture; typed from AMP's OpenAPI `NetworkStatus` alone (#3-56.2ap).
    # Every capture has them empty, a gateway's tunnel included.
    rejected: list[FirewallRejectedRule]
    wireGuardApplied: list[FirewallWireGuardInterfaceStatus]
    wireGuardRejected: list[FirewallRejectedInterface]
    "The tunnels it couldn't bring up, eg. a new gateway's while AMP puts its agent in place."
    # TODO: Check these two against a live capture; typed from AMP's OpenAPI `NetworkStatus` alone (#3-56.2ap).
    # Every capture has them empty, a gateway's tunnel included.
    wireGuardPeersApplied: list[FirewallWireGuardPeer]
    wireGuardPeersRejected: list[FirewallRejectedPeer]
    gatewayApplied: list[FirewallGatewayRoute]
    "The gateway ports it forwards, on a front spire."
    # TODO: Check these two against a live capture; typed from AMP's OpenAPI `NetworkStatus` alone (#3-56.2ap).
    # Every capture has them empty.
    gatewayRejected: list[FirewallRejectedGatewayRoute]
    advisories: list[str]
    error: Optional[str]
    updatedAt: str
    agentVersion: str
    # TODO: Check against a live capture; typed from AMP 3.0.1's OpenAPI `NetworkStatus` alone (#3-60).
    # AMP's docs give it no description.
    launchContract: int


class FirewallWireGuardInterface(TypedDict):
    """A WireGuard tunnel's interface on the host, from `FirewallRejectedInterface.interface`."""

    interfaceName: str
    """eg. ``"amp-7f7e2fff"``."""


# TODO: Check against a live capture; typed from AMP's OpenAPI `WireGuardInterfaceStatus` alone (#3-56.2ap).
# Every capture has `wireGuardApplied` empty.
class FirewallWireGuardInterfaceStatus(FirewallWireGuardInterface):
    """A WireGuard tunnel AMP's system agent brought up, from `FirewallStatus.wireGuardApplied`."""

    installed: bool


# TODO: Check against a live capture; typed from AMP's OpenAPI `WireGuardPeer` and `WireGuardPeerStatus` alone (#3-56.2ap).
# Every capture has `wireGuardPeersApplied` and `wireGuardPeersRejected` empty.
class FirewallWireGuardPeer(TypedDict):
    """The other end of a WireGuard tunnel, from `FirewallStatus.wireGuardPeersApplied` and `FirewallRejectedPeer.peer`."""

    interfaceName: str
    publicKey: str
    allowedIp: str


# TODO: Check against a live capture; typed from AMP's OpenAPI `WithheldPortRule` alone (#3-56.2ap).
# Every capture has `withheld` empty.
class FirewallWithheldRule(TypedDict):
    """A shard's port AMP left closed as it holds the number itself, from `FirewallResponse.withheld`.

    The shard can't be reached on that port until it moves to another.
    """

    shardId: str
    shardName: str
    source: str
    """What asked for the rule: ``"Shard"``, ``"Publication"`` or ``"Gateway"``."""
    port: int
    protocol: str
    """``"TCP"`` or ``"UDP"``."""
    kind: str
    """Which of AMP's own listeners holds the port: ``"Panel"``, ``"Bus"``, ``"Sftp"``, ``"EntryNodeBootstrap"``,
    ``"WireGuardTunnel"`` or ``"TunnelProbe"``."""


class GatewayConflict(TypedDict):
    """A shard port that clashes on the front spire, from `GatewayPreflightResponse.conflicts`.

    A gateway maps the shard's ports one to one onto the front spire, so it is the shard's port that has to move.
    """

    port: int
    protocol: str
    """``"TCP"``, ``"UDP"`` or ``"Both"``."""
    portRef: str
    """The shard port's name in its template, eg. ``"ServerPort"``."""
    heldBy: str
    """What holds the port on the front spire, eg. ``"Publication"``."""
    holderName: str
    "Its name, eg. the shard a publication forwards to."
    suggestedPort: int
    "A port that is free on the front spire."


class GatewayEgressRequest(TypedDict):
    """The body of ``PUT /api/networking/gateways/{id}/egress``."""

    egressAllowList: list[str]


class GatewayEligibilityResponse(TypedDict):
    """``GET /api/networking/gateway-eligibility``, what can take part in a gateway."""

    containerShardIds: list[str]
    gatewayFrontSpireIds: list[str]
    """A spire is listed once its ``"spire.publicHost"`` setting is set."""


class GatewayPreflightResponse(TypedDict):
    """``POST /api/networking/gateways/preflight``, what stands in the way of a gateway."""

    # TODO: Drop the field doc once AMP's preflight checks what the create checks (U20b, U20c).
    # AMP 3.0.0 and 3.0.1 send no conflicts for gateways the create refuses.
    conflicts: list[GatewayConflict]
    """The shard's ports a publication on the front spire already holds; a shard's own port there isn't one. Empty even
    for a gateway `NetworkModule.create_gateway` refuses, see `NetworkModule.preflight_gateway`."""


class GatewayRequest(TypedDict):
    """The body of ``POST /api/networking/gateways`` and ``POST /api/networking/gateways/preflight``."""

    shardId: str
    frontSpireId: str


class GatewayResponse(TypedDict):
    """One gateway from ``GET /api/networking/gateways``; making one answers with it too (201).

    A gateway is a shard's route over a WireGuard tunnel between its spire and a front spire.
    """

    id: str
    shardId: str
    shardName: str
    frontSpireId: str
    frontSpireName: str
    enabled: bool
    egressAllowList: list[str]
    """The private IPv4 networks the shard may reach through the front spire, eg. ``["192.168.4.0/24"]``; see
    `NetworkModule.set_gateway_egress`. Empty for the internet only."""
    createdAt: str
    status: Optional[GatewayStatus]
    "`None` when it's new; the list fills it in once AMP has set the route up."
    # TODO: Reword the field doc once a running shard routes without a restart (U26e).
    # AMP 3.0.0 and 3.0.1 route a shard that was running only after it restarts.
    runningWithoutRoute: bool
    "If the shard was running before the route existed; it routes only once it restarts."


class GatewayStatus(TypedDict):
    """A gateway's state, from `GatewayResponse.status`."""

    bindingId: str
    "The gateway's `id`."
    state: str
    """As AMP sends it, a `GatewayState` value, eg. ``"Active"``; `GatewayState(state)` gives the member."""
    address: Optional[str]
    """The shard's address on the tunnel, eg. ``"10.83.0.10"``, `None` until AMP gives it one; every capture had it
    from the first status."""
    error: Optional[str]
    """Why it's at `GatewayState.fault`, eg. ``"The tunnel this server routes over is not up."``."""
    updatedAt: str


class HealthStatusResponse(TypedDict):
    """``GET /api/health/status``, which needs no session.

    `phase` runs through the first-run setup (``"setup-database"``, ``"setup-admin"``, ``"preview-licence"``) to ``"ready"``.
    Right after AMP has set up its own message bus, `phase` reads ``"starting"`` for a few seconds before ``"setup-admin"``.
    A panel with no licence reads ``"preview-licence"`` again.
    A machine joining as a spire reads ``"starting"`` until its enrolment is approved.
    """

    phase: str
    message: Optional[str]
    """A translation key, eg. ``"auth.setup.joining.awaitingApproval"`` while a joining machine waits for
    `EnrollmentModule.approve_spire_enrollment`."""
    preview: Optional[PreviewStatus]
    "Set on a preview build."
    messageParams: Optional[dict[str, str]]
    """Values for the `message` translation, eg. the `fingerprint` the panel's admin compares before approving."""
    plainText: bool
    "If this request came over plain HTTP from a public address, which the login page warns about."


class HTTPSCheck(TypedDict):
    """One check from `HTTPSCheckResponse.checks`."""

    key: str
    "Which check it is; its values weren't recorded yet."
    state: int
    "eg. 2 for a pass and 3 for a fail."
    code: Optional[str]
    """A translation key for the result, eg. ``"https.check.resolved"`` or ``"https.check.addressMismatch"``."""
    params: Optional[dict[str, str]]
    "Values for the `code` translation, eg. `host`, `expected` and `found` on an address mismatch."
    detail: Optional[str]


class HTTPSCheckResponse(TypedDict):
    """``POST /api/https/check``, if a domain name is ready for AMP's own HTTPS setup."""

    hostName: Optional[str]
    """The name as AMP normalised it, `None` for one that isn't a domain name (`outcome` ``"invalid"``)."""
    outcome: str
    """eg. ``"elsewhere"``, for a name that points at another address than the panel's public one, or ``"invalid"``,
    with the first check's `code` saying why, eg. ``"https.name.characters"``."""
    checks: list[HTTPSCheck]
    reachability: str
    """``"Unknown"``, ``"Direct"``, ``"Nat"`` or ``"Cgnat"``."""
    externalAddress: Optional[str]
    """The panel's public IP address, `None` when AMP didn't learn it, eg. for an ``"invalid"`` name."""
    internalAddress: Optional[str]
    """The panel's address on its own network, `None` when AMP didn't learn it, eg. for an ``"invalid"`` name."""
    addresses: list[str]
    "The addresses the name resolved to."


class HTTPSSetupStatusResponse(TypedDict):
    """``GET /api/https/setup/status``, the progress of AMP's own HTTPS setup."""

    phase: str
    """``"idle"``, ``"running"``, ``"done"`` (configured) or ``"failed"`` (nothing configured)."""
    hostName: Optional[str]
    checks: list[HTTPSCheck]
    url: Optional[str]
    "The panel's address through AMP's own HTTPS once it's configured."
    certificateVerified: bool
    updatedUtc: str
    """``"0001-01-01T00:00:00+00:00"`` before any setup."""


class HTTPSStateResponse(TypedDict):
    """``GET /api/https``, the panel's HTTPS setup. Setting and clearing the own proxy answer with it too."""

    mode: str
    """``"none"``, ``"managed"`` (AMP's own HTTPS, through Caddy) or ``"ownProxy"`` (`HTTPSModule.set_own_proxy`)."""
    hostName: Optional[str]
    url: Optional[str]
    certificateVerified: bool
    agentPresent: bool
    agentSupported: bool
    panelExposed: bool
    entryNode: bool
    externalAddress: str
    "The panel's public IP address."
    reachability: str
    """``"Unknown"``, ``"Direct"``, ``"Nat"`` or ``"Cgnat"``."""
    internalAddress: str
    "The panel's address on its own network."
    ipv6Address: Optional[str]
    "A public IPv6 address of the machine's, `None` when the machine has no public IPv6 address."
    trustedProxies: list[str]
    "The reverse proxies AMP takes forwarded headers from, set by `HTTPSModule.set_own_proxy`."
    serveFrontend: bool
    "If AMP serves the web app as well as its API or not."
    running: bool
    "If a setup is running."


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
    droppedRoles: list[str]
    """The names of the invite's roles the new user didn't get, as the inviting admin no longer holds every permission
    in the role. A role deleted since the invite was made is left out without being listed."""


class InviteAcceptRequest(TypedDict):
    """The body of ``POST /api/invites/accept``."""

    token: str
    email: str
    password: str
    displayName: Optional[str]
    locale: str


class InvitePreviewResponse(TypedDict):
    """``POST /api/invites/preview``, which needs no session."""

    userName: str
    displayName: Optional[str]


class InviteRequest(TypedDict):
    """The body of ``POST /api/invites``."""

    userName: str
    displayName: Optional[str]
    roleIds: list[str]
    expiresInHours: int


class InviteResponse(TypedDict):
    """One invite from ``GET /api/invites``."""

    id: str
    userName: str
    "The username the new account gets."
    displayName: Optional[str]
    roleIds: list[str]
    createdByName: Optional[str]
    "The name of the admin who made or last rearmed the invite, `None` when AMP didn't record the admin."
    createdAt: str
    expiresAt: str
    accepted: bool
    acceptedAt: Optional[str]
    status: str
    """``"pending"``, ``"expired"`` or ``"accepted"``. A revoked invite leaves the list."""


class InviteTokenResponse(TypedDict):
    """``POST /api/invites`` (201) and ``POST /api/invites/{id}/rearm``."""

    invite: InviteResponse
    token: str
    "The invite code to hand to the new user; a rearm makes the old one stop working."


class LicenceAgreementResponse(TypedDict):
    """``GET /api/licence/terms/agreement``, the licence terms a key may need accepted."""

    version: int
    "The current `termsVersion`, eg. 2."
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
    "The sentence the person accepting the terms agrees to, sent back in a `LicenceTermsAcceptance`."


class LicenceQueryResponse(TypedDict):
    """``POST /api/licence/query``, what a key gives, without activating it."""

    productName: str
    gradeName: str
    expires: Optional[str]
    "`None` for a lifetime licence."
    usage: int
    "How many installations already use the key; one key covers several."
    alreadyActive: bool
    "If the key's edition is active here already; activating it again refreshes it."
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
    """What the activation file says alone: ``"Valid"``, ``"Expired"`` or ``"Invalid"``."""
    standing: str
    """What counts, with the licence service's last answer: ``"Active"``, ``"Grace"``, ``"Lapsed"``, ``"Revoked"``,
    ``"Disabled"``, ``"Unrecognised"``, ``"OutOfTouch"``, ``"Invalid"`` or ``"TermsRequired"``. Only ``"Active"`` and
    ``"Grace"`` allow shards."""
    expires: Optional[str]
    "`None` for a lifetime licence."
    graceEnds: Optional[str]
    "The web panel shows it as a date."
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
    "0 with no licence, and `None` just after activating one until the licence service answers."
    shardCeiling: Optional[int]
    "0 with no licence, and `None` just after activating one until the licence service answers. It can be above the limit."
    lastVerifiedAt: Optional[str]
    "`None` until the licence service has answered."
    usingMockClient: bool


class LicenceTermsAcceptance(TypedDict):
    """The terms acceptance `LicenceModule.activate_licence` and `LicenceModule.accept_licence_terms` send.

    Its keys come from the web panel's code. AMP's checks on `LicenceModule.accept_licence_terms` require `agreementHash`,
    `attestation` and `locale`, not `termsVersion` or `clickedAt`. Fill it from `LicenceAgreementResponse`.
    """

    termsVersion: int
    "The agreement's `version`."
    agreementHash: str
    "The agreement's `hash`."
    attestation: str
    "The agreement's `attestation`."
    locale: str
    """The language the terms were read in, eg. ``"en"``."""
    clickedAt: str
    "When the terms were accepted, ISO 8601."


class LicenceTermsRequest(LicenceTermsAcceptance):
    """The body of ``POST /api/licence/{spire_id}/{grade_id}/terms``: the acceptance and the key."""

    key: str


class LoginRequest(TypedDict):
    """The body of ``POST /api/auth/login``."""

    username: str
    password: str
    rememberMe: bool


class MessageBusService(TypedDict):
    """The message bus's own process, from `MessageBusStatsResponse.service`, as the record it leaves says.

    The fields AMP reads from that record are `None` while there's none, `condition` ``"Absent"``.
    """

    condition: str
    """``"Absent"``, ``"Stale"``, ``"Stopped"``, ``"Idle"``, ``"Blocked"``, ``"Running"``, ``"Backoff"`` or
    ``"CrashLoop"``."""
    pid: int
    startedAtUtc: Optional[str]
    binaryVersion: Optional[str]
    configHash: Optional[str]
    configCurrent: bool
    "If the bus runs the config file as it is now; `False` while a restart AMP asked for is pending."
    fileStoreBytes: Optional[int]
    lastExitReason: Optional[str]
    "Why the last bus process is gone, or what the service waits for."
    updatedAtUtc: Optional[str]
    serviceVersion: Optional[str]
    """eg. ``"amp3-host 3.0.0.6+f3d1a77cea"``."""
    serviceUp: bool


class MessageBusStatsResponse(TypedDict):
    """``GET /api/support/message-bus-stats``, the NATS message bus's figures.

    With no connection to the bus, AMP answers with a shell rather than an error: `state` isn't ``"Open"``, and the
    server's details, figures and `service` are `None`.
    """

    state: str
    """``"Open"``, ``"Closed"``, ``"Reconnecting"`` and the like."""
    serverId: Optional[str]
    "The first 8 characters of the server's ID."
    serverName: Optional[str]
    serverVersion: Optional[str]
    clusterName: Optional[str]
    "`None` for a server that isn't in a cluster."
    rttMs: Optional[float]
    "Measured on the call."
    jetStreamAvailable: bool
    jsStreams: int
    jsConsumers: int
    jsStorageBytes: Optional[int]
    jsApiTotal: Optional[int]
    jsApiErrors: Optional[int]
    service: Optional[MessageBusService]


class MessageErrorResponse(TypedDict):
    """The body of a refused ``POST /api/auth/login`` (401); the same text for a wrong password or an unknown user."""

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


class NetworkProbe(TypedDict):
    """How the panel's machine reaches the internet, from `SetupNetworkResponse.probe`."""

    type: str
    """``"Unknown"``, ``"Direct"``, ``"Nat"`` or ``"Cgnat"``. AMP's docs say game servers behind ``"Nat"`` need a port
    forward, and game servers behind ``"Cgnat"`` need a tunnel."""
    internalIp: Optional[str]
    "The machine's network address, `None` when AMP couldn't work the address out."
    externalIp: Optional[str]
    "The machine's public address, `None` when AMP couldn't work the address out."


class PanelUpdateResponse(TypedDict):
    """``POST /api/updates/apply``, the panel's update to a newer AMP."""

    taskId: str
    """The update's task, which can't be followed: `TaskModule.get_task` answers 404 for the task, before the panel
    restarts and after. Watch `PlatformModule.get_health_status` instead."""


class PasskeyFlowResponse(TypedDict):
    """``POST /api/auth/passkey/begin`` and ``POST /api/profile/passkeys/register/begin``, a WebAuthn ceremony to answer."""

    flowId: str
    "Sent back with the answer to ``.../complete`` (or ``/api/auth/passkey/abandon``)."
    options: dict[str, Any]
    "The WebAuthn options, base64url encoded, for ``navigator.credentials.get`` or ``navigator.credentials.create``."


class PasskeyLoginRequest(TypedDict):
    """The body of ``POST /api/auth/passkey/complete``."""

    flowId: str
    response: Mapping[str, Any]
    "The WebAuthn assertion, as the browser's `PublicKeyCredential` JSON."
    rememberMe: bool


class PasskeyRegisteredResponse(TypedDict):
    """``POST /api/profile/passkeys/register/complete``."""

    passkey: PasskeyResponse
    session: Optional[TokenResponse]
    "A full session in place of an enrolment-only session, `None` from a full session."


class PasskeyRegisterRequest(TypedDict):
    """The body of ``POST /api/profile/passkeys/register/complete``."""

    flowId: str
    response: Mapping[str, Any]
    "The WebAuthn attestation, as the browser's `PublicKeyCredential` JSON."
    name: str


class PasskeyRequiredResponse(TypedDict):
    """A ``POST /api/auth/login`` answer for an account that needs a second factor; it carries no token.

    AMP sends it when the passkey policy is ``"Required"`` and the account has a passkey. A recovery code to
    ``POST /api/auth/login/second-factor`` finishes the login.
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
    """A ``POST /api/auth/login`` answer for an account that has to change its password first; it carries no token."""

    passwordChangeRequired: Literal[True]
    reason: str
    """eg. ``"forced"``, for a user created with `requirePasswordChange`."""


class PasswordChangeRequest(TypedDict):
    """The body of ``POST /api/profile/password``."""

    currentPassword: str
    newPassword: str


class PasswordPolicyResponse(TypedDict):
    """``GET /api/auth/password-policy``, which needs no session."""

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
    "``>`` is every permission (the admin); a user with no roles has no grants."
    catalog: list[PermissionNode]
    roleIds: list[str]


class PlatformWarningResponse(TypedDict):
    """One of the panel's warnings, from ``GET /api/monitoring/platform-warnings``."""

    id: str
    """The warning's code and its params joined, eg. ``"platform.warning.ipv6BlackHoled|vm5"``; what
    `PlatformModule.acknowledge_platform_warning` takes."""
    code: str
    """A dotted key, eg. ``"platform.warning.ipv6BlackHoled"``."""
    params: dict[str, str]
    """Values for `code`'s text, eg. ``{"machine": "vm5"}``."""
    message: str
    dismissable: bool
    "If it can be acknowledged or not; one that needs action can't."


class PortClaimResponse(TypedDict):
    """One port something holds on a spire, from ``GET /api/networking/spires/{id}/port-claims``.

    An idle spire lists hundreds, mostly for WireGuard tunnels.
    """

    kind: str
    """eg. ``"SpireService"``."""
    port: int
    protocol: str
    """eg. ``"Both"``."""
    shardId: Optional[str]
    holderName: str
    """eg. ``"the AMP panel"`` or ``"a WireGuard tunnel"``."""


class PreferencesChanges(TypedDict, total=False):
    """The preferences `AccountModule.update_preferences` takes as keyword arguments, each described there."""

    theme: str
    locale: str
    favourite_app_slugs: list[str]
    pinned_shard_ids: list[str]
    notify_on_state_change: bool
    notify_on_update_available: bool
    compact_shard_header: bool
    hide_unrouted_shards: bool
    hide_private_ports: bool
    file_details_width: int
    amp_experience: str
    "A `UserExperienceLevel` member or its value."
    show_tutorials: bool
    tutorial_prompt_dismissed: bool
    tutorials_completed: list[str]
    accessibility_hints_enabled: bool
    onboarding_completed: bool
    reduced_motion: bool
    analytics_enabled: bool
    streamer_mode: bool
    time_format: str
    "A `TimeFormat` member or its value."


class PreviewStatus(TypedDict):
    """The preview build's countdown in `HealthStatusResponse`."""

    expiresAt: str
    daysRemaining: Optional[int]
    "Counted from the time the licence service vouched for, not the machine's clock; `None` until it first answers."
    reason: Optional[str]
    """Why the build is blocked, ``"expired"``, ``"clockWrong"``, ``"unreachable"`` or ``"unstamped"``; `None` while it
    runs normally."""
    update: Optional[PreviewUpdate]
    "Often `None`."


class PreviewUpdate(TypedDict):
    """The preview build's update check in `PreviewStatus`."""

    state: str
    """``"current"``, ``"available"``, ``"installing"`` (an expired build putting the newer one in place) or ``"failed"``."""
    version: Optional[str]
    "The newer version, when a newer version exists."
    stream: Optional[str]
    reason: Optional[str]
    """An ``"updates.error.*"`` key on ``"failed"``."""


class Principal(TypedDict):
    """Who or what did something, from a running task or an audit event."""

    kind: int
    "eg. 0 for a user and 1 for AMP itself."
    userId: Optional[str]
    userDisplayName: Optional[str]
    onBehalfOfUserId: Optional[str]
    onBehalfOfUserDisplayName: Optional[str]
    systemSource: Optional[str]
    """The part of AMP that did it, eg. ``"Auth"`` or ``"Reconciler"``, when `kind` is 1."""


class ProblemDetailsResponse(TypedDict):
    """ASP.NET's validation error body (RFC 9110), eg. a ``POST /api/auth/login`` with no username (400)."""

    type: str
    title: str
    status: int
    errors: dict[str, list[str]]
    """The field name, as AMP spells it (``"Username"``), to its errors."""
    traceId: str


class ProfileRequest(TypedDict):
    """The body of ``PUT /api/profile``."""

    displayName: Optional[str]
    email: NotRequired[str]


class ProfileResponse(TypedDict):
    """``GET /api/profile``, the session user's own account."""

    id: str
    userName: str
    displayName: Optional[str]
    email: Optional[str]
    "`None` when the account has no email address. AMP doesn't check that the value is an email address."
    emailConfirmed: bool


class ProfileSessionResponse(TypedDict):
    """One of the logged in user's sessions, from ``GET /api/profile/sessions``."""

    id: str
    createdAt: str
    lastSeenAt: str
    expiresAt: str
    remoteIp: str
    """IPv4 comes as an IPv6 mapped address, eg. ``"::ffff:192.0.2.1"``."""
    userAgent: str
    isCurrent: bool
    "If it's the session this request came from."


class PublicationRequest(TypedDict):
    """The body of ``POST /api/networking/publications``."""

    frontSpireId: str
    publicPort: int
    shardId: str
    portRef: str
    frontPublicHost: NotRequired[str]
    """The front spire's ``"spire.publicHost"`` setting to keep, when the front spire has no public host yet."""


class PublicationResponse(TypedDict):
    """One public port forward from ``GET /api/networking/publications``; making or changing one answers with it too."""

    id: str
    frontSpireId: str
    "The spire players connect to; it can be the shard's own spire."
    publicPort: int
    protocol: str
    """eg. ``"UDP"`` or ``"Both"`` (TCP and UDP), taken from the shard's port."""
    shardId: str
    portRef: str
    """The shard port's name in its template, eg. ``"ServerPort"``."""
    enabled: bool
    createdAt: str
    # TODO: Drop the last sentence once AMP answers a change with the new status (U26c).
    # AMP 3.0.0 and 3.0.1 answer a publication turned off with its old `Active` status.
    status: Optional[PublicationStatus]
    """`None` when it's new; the list fills it in once AMP has checked the forward. A change's reply can carry the
    old one."""


class PublicationStatus(TypedDict):
    """A port forward's state, from `PublicationResponse.status`."""

    publicationId: str
    state: str
    """As AMP sends it, a `PublicationState` value, eg. ``"Active"``; `PublicationState(state)` gives the member."""
    targetSpireId: str
    "The shard's spire; all zeros while the forward is disabled."
    resolvedPort: int
    "The shard's port now, which can differ from the one it had when the forward was made, eg. after a move; 0 while disabled."
    bytesIn: int
    bytesOut: int
    activeFlows: int
    tunnelPhase: Optional[str]
    """The tunnel's `TunnelStatus.phase` through another spire, eg. ``"Provisioning"`` or ``"AgentRejected"``; `None` once
    active."""
    faultSpireId: Optional[str]
    "The spire at fault, with `error` saying why."
    error: Optional[str]
    """eg. ``"The file does not exist."`` while a first tunnel's agent is set up."""
    updatedAt: str


class PublicationUpdateRequest(TypedDict):
    """The body of ``PUT /api/networking/publications/{id}``; a `None` field is left out."""

    enabled: Optional[bool]
    publicPort: Optional[int]


class ReasonErrorResponse(TypedDict):
    """The body of a refused ``POST /api/auth/login/second-factor`` (401), eg. a wrong or already used recovery code."""

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


class RoleRequest(TypedDict):
    """The body of ``POST /api/roles``."""

    name: str
    description: str
    permissions: list[str]


class RoleResponse(TypedDict):
    """One role from ``GET /api/roles`` or ``GET /api/roles/{id}``. Creating or updating a role answers with the role too."""

    id: str
    name: str
    description: Optional[str]
    "`None` for a role made with no description."
    permissions: list[str]
    """Permission strings, eg. ``"users.read"`` or ``"spire.*.shard.*.view"``; a leading ``-`` denies.

    AMP stores them as given, without checking they exist.
    """
    ownerUserId: Optional[str]
    "The ID of the user who made the role, `None` when AMP didn't record the role's creator."
    createdAt: str


class RoleUpdateRequest(TypedDict):
    """The body of ``PUT /api/roles/{id}``. A `None` field is left out, so AMP keeps the role's value."""

    name: Optional[str]
    description: Optional[str]
    permissions: Optional[list[str]]


class ScheduleCatalogResponse(TypedDict):
    """``GET /api/shards/{id}/schedules/catalog``, the triggers and tasks a shard's schedules can use."""

    triggers: list[ScheduleCatalogTrigger]
    tasks: list[ScheduleCatalogTask]
    commonEmits: list[ScheduleEmit]
    "The values every trigger hands to its steps."


class ScheduleCatalogTask(TypedDict):
    """A task a schedule step can run, from `ScheduleCatalogResponse.tasks`."""

    id: str
    """The step's `taskType`, eg. ``"power.restart"`` or ``"app.consoleSend"``."""
    category: str
    isAsync: bool
    defaultFailure: str
    """``"Abort"`` or ``"Continue"``."""
    parameters: list[ScheduleTaskParameter]


class ScheduleCatalogTrigger(TypedDict):
    """An event a schedule can wait for, from `ScheduleCatalogResponse.triggers`."""

    id: str
    """The trigger's `eventType`, eg. ``"player.joined"``."""
    category: str
    emits: list[ScheduleEmit]
    "The values it hands to the schedule's steps."
    label: str
    "A translation key, empty for the built in triggers."
    description: str


class ScheduleCondition(TypedDict):
    """One test an ``"if"`` step makes, from its `conditions`, eg. ``{"value": "{@State}", "operator": "Equals", ...}``."""

    value: str
    """The left side, which can use the trigger's values, eg. ``"{@State}"``."""
    operator: str
    """``"Equals"``, ``"NotEquals"``, ``"Contains"``, ``"NotContains"``, ``"StartsWith"``, ``"EndsWith"``,
    ``"MatchesRegex"``, ``"GreaterThan"``, ``"GreaterOrEqual"``, ``"LessThan"``, ``"LessOrEqual"``, ``"IsEmpty"`` or
    ``"IsNotEmpty"``. The text tests ignore case; a number test on a value that isn't a number doesn't match."""
    comparand: str
    """The right side, unused by ``"IsEmpty"`` and ``"IsNotEmpty"``."""


class ScheduleDefinition(TypedDict):
    """A schedule as it was saved, from `ShardScheduleResponse.definition`."""

    id: str
    tenantId: str
    shardId: str
    name: str
    description: str
    "Empty when it was made with `None`."
    trigger: ScheduleTrigger
    steps: list[ScheduleStep]
    retryPolicy: ScheduleRetryPolicy
    misfirePolicy: str
    """``"Skip"`` or ``"FireOnce"``."""
    timeout: str
    """A time span, ``"00:30:00"`` when it was made with `None`."""
    enabled: bool
    createdAt: str
    updatedAt: str
    createdByUserId: str
    runAsUserId: str


class ScheduleEmit(TypedDict):
    """A value a trigger hands to the schedule's steps, eg. the user who joined."""

    name: str
    label: str
    "A translation key, or empty."
    description: str


# TODO: Check against a live capture; typed from AMP's OpenAPI `StepRefusal` alone (#3-56.1z).
# A refused step needs one AMP won't run, eg. a webhook to a destination its owner may not call.
class ScheduleRefusal(TypedDict):
    """A step AMP refused and skipped on a schedule's latest run, from `ScheduleStatus.refusal`.

    The rest of the run carries on, and the refusal is audited once.
    """

    notice: CodedErrorResponse
    "Why AMP refused it."
    stepId: str
    "The refused step's `id`."


class ScheduleRetryPolicy(TypedDict):
    """How a schedule tries again after a failed run, from `ScheduleDefinition.retryPolicy`."""

    maxAttempts: int
    initialDelay: str
    """A time span, eg. ``"00:00:05"``."""
    backoffMultiplier: float
    "1.0 waits the same each time, 2.0 doubles the wait each time."
    maxDelay: str


class ScheduleRunResponse(TypedDict):
    """``POST /api/shards/{id}/schedules/{id}/run`` (202)."""

    executionId: str
    "The run's `id` in `ScheduleExecution`."


class ScheduleStatus(TypedDict):
    """How a schedule's last run went, from `ShardScheduleResponse.status`."""

    scheduleId: str
    lastRunAt: str
    lastRunStatus: str
    """``"Queued"``, ``"Running"``, ``"Succeeded"``, ``"CompletedWithErrors"``, ``"Failed"``, ``"TimedOut"`` or
    ``"Skipped"``."""
    lastError: Optional[str]
    lastExecutionId: str
    consecutiveFailures: int
    # TODO: Check these two against a live capture; typed from AMP's OpenAPI `ScheduleStatus` alone (#3-56.1z).
    # Every capture has them `None`: AMP hasn't turned a schedule off or refused a step on the test VMs.
    turnedOff: Optional[CodedErrorResponse]
    """Why AMP turned the schedule off, `None` while AMP hasn't.
    - The schedule stays off until someone who can manage the shard's schedules turns the schedule back on."""
    refusal: Optional[ScheduleRefusal]
    "A step AMP refused and skipped on the latest run, `None` when it refused none."
    refusalAudited: bool
    "If the refusal has been audited since the schedule was last changed; a refusal on every run is audited once."


# One schedule step, for `ShardScheduleRequest.steps`; the functional form, as two of its keys are `await` and `else`.
# Each `type` uses its own keys, and AMP gives every step an `id` when it is left out, eg.
#    {"type": "task", "taskType": "app.consoleSend", "parameters": {"command": "say hi"}, "await": True}
#    {"type": "if", "conditions": [{"value": "{@State}", "operator": "Equals", "comparand": "Ready"}],
#     "match": "All", "then": [<steps>], "else": [{"type": "stop"}]}
ScheduleStep = TypedDict(
    "ScheduleStep",
    {
        # "task", "if", "switch" or "stop" (which ends the steps it is among).
        "type": str,
        "id": str,
        # A "task" step's keys.
        "taskType": str,
        "parameters": dict[str, Any],
        "await": bool,
        "onSuccess": list["ScheduleStep"],
        "onFailure": list["ScheduleStep"],
        # "Continue" or "Abort", overriding the task's own `defaultFailure`, or `None` for that.
        "failureOverride": Optional[str],
        # An "if" step's keys; `match` is "All" or "Any".
        "conditions": list[ScheduleCondition],
        "match": str,
        "then": list["ScheduleStep"],
        "else": list["ScheduleStep"],
        # TODO: Check a "switch" step against a live capture; typed from AMP's OpenAPI `StepSwitchStep` alone (#3-56.1k).
        # It runs the first case whose test matches `value`, else `default`.
        "value": str,
        "cases": list["ScheduleSwitchCase"],
        "default": list["ScheduleStep"],
    },
    total=False,
)


class ScheduleStepOutcome(TypedDict):
    """How one step of a run went, from `ScheduleExecution.step_outcomes`."""

    stepId: str
    "AMP's own ID for the step, not the one it was saved with."
    lane: str
    """eg. ``"main"``, or ``"bg:<step id>"`` for the steps an un-awaited task runs after it."""
    status: str
    """``"Succeeded"``, ``"Failed"``, ``"Skipped"`` or ``"NotReached"``."""
    detail: str
    """eg. ``"Sent: say hello"``."""
    startedAt: str
    duration: str


# TODO: Check against a live capture; typed from AMP's OpenAPI `SwitchCase` alone (#3-56.1k).
# No "switch" step has been saved on the test VMs.
class ScheduleSwitchCase(TypedDict):
    """One case of a ``"switch"`` step, from its `cases`; any `ScheduleCondition.operator` works, not only equality."""

    operator: str
    "A `ScheduleCondition.operator`."
    comparand: str
    steps: list[ScheduleStep]
    "What runs when it matches."


class ScheduleTaskParameter(TypedDict):
    """A value a schedule task takes, from `ScheduleCatalogTask.parameters`."""

    name: str
    """eg. ``"command"`` for ``"app.consoleSend"``."""
    inputType: str
    """eg. ``"template"`` (text that can use the trigger's values) or ``"number"``."""
    required: bool


class ScheduleTrigger(TypedDict):
    """When a schedule runs, from `ScheduleDefinition.trigger`; also what `ShardModule.create_shard_schedule` takes.

    Each `type` uses its own keys: ``"interval"`` takes `interval`, ``"cron"`` takes `expression` and `timeZoneId`,
    and ``"event"`` takes `eventType`.
    """

    type: str
    """``"interval"``, ``"cron"`` or ``"event"``."""
    interval: NotRequired[str]
    """A time span, eg. ``"01:00:00"``; runs line up with `anchor`."""
    anchor: NotRequired[str]
    """AMP adds it to an interval, eg. ``"1970-01-01T00:00:00+00:00"``."""
    expression: NotRequired[str]
    """A cron expression, eg. ``"0 3 * * *"``."""
    timeZoneId: NotRequired[str]
    """eg. ``"UTC"``."""
    eventType: NotRequired[str]
    """A `ScheduleCatalogTrigger.id`, eg. ``"player.joined"``."""


class ScheduleWithheld(TypedDict):
    """A step parameter AMP hides from the caller, from `ShardScheduleResponse.withheld`, eg. a webhook's `url`."""

    stepId: str
    parameter: str
    """The parameter's name, eg. ``"url"`` or ``"body"``."""


class SecondFactorRequest(LoginRequest):
    """The body of ``POST /api/auth/login/second-factor``: a login with one of the account's recovery codes."""

    code: str


class SettingAction(TypedDict):
    """A button from `SettingsManifestResponse.actions`, run by ``POST /api/settings/actions/{id}``."""

    id: str
    """eg. ``"smtp.test"`` or ``"templates.sync"``."""
    category: str
    "The `SettingSpec.category` it sits under."
    # TODO: Check against a live capture; typed from AMP 3.0.1's OpenAPI `SettingsActionInfo` alone (#3-60).
    subcategory: str
    "The `SettingSpec.subcategory` the button sits at the end of, empty when the button follows the whole `category`."


class SettingActionResponse(TypedDict):
    """``POST /api/settings/actions/{id}``, what a settings page button did."""

    detail: str
    """An English sentence with the counts, eg. ``"Synced 2 source(s), 0 updated - N templates available."``."""


class SettingCandidate(TypedDict):
    """One value a shard setting can take, from `ShardSettingCandidatesResponse.candidates`."""

    value: str
    """What to set, eg. ``"[Latest]"``."""
    display: str
    """What the web panel shows, eg. ``"26.3"``."""
    fields: dict[str, str]
    "More about the value, eg. its download `url`."


class SettingsManifestResponse(TypedDict):
    """``GET /api/settings/manifest``, every platform setting with its current value."""

    specs: list[SettingSpec]
    values: SettingValues
    """A setting's `fieldName` to its value. Every value is a string, eg. ``"587"``, ``"true"`` or ``"[]"``."""
    secretHasValue: dict[str, bool]
    "A secret setting's `fieldName` to if it holds a value."
    actions: list[SettingAction]
    unavailable: dict[str, str]
    """A setting that can't be changed, to a translation key saying why, eg. ``"preview.crashReportsLocked"``."""


class SettingSpec(TypedDict):
    """One setting from `SettingsManifestResponse.specs`; shard settings and templates use the same shape."""

    fieldName: str
    """The setting's key in `SettingsManifestResponse.values`, eg. ``"smtp.host"``.

    A shard field starting with ``$`` is one AMP keeps for every template, eg. ``"$MaxUsers"``.
    """
    paramFieldName: str
    effectiveKey: str
    "`paramFieldName` when it's set, else `fieldName`."
    required: bool
    hidden: bool
    platform: int
    deployment: int
    conditionSetting: str
    """Another setting's `fieldName` this one depends on, eg. ``"ServerType"``."""
    conditionValue: str
    """The value `conditionSetting` needs for this one to apply, eg. ``"Paper"``."""
    defaultValue: Optional[str]
    "`None` for no default; always `None` on the platform settings."
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
    """eg. ``"text"``, ``"multiline"``, ``"number"``, ``"quantity"``, ``"checkbox"``, ``"select"``, ``"list"``,
    ``"password"``, ``"credential:Smtp"``, ``"ipbinding"`` (spires), or ``"enum"``, ``"combo"`` and ``"Password"`` (templates)."""
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
    """Where the candidate values come from, eg. ``"mojang.versions"``; see `ShardModule.get_shard_setting_candidates`."""
    minValue: Optional[float]
    "`None` for no lower limit."
    maxValue: Optional[float]
    "`None` for no upper limit."
    isHostCap: bool
    # TODO: Check against a live capture; typed from AMP's OpenAPI `SettingSpec` alone (#3-56.1z).
    # Every capture has it `None`.
    multiplier: Optional[float]
    "AMP reads a template's value but doesn't use it yet."
    multipleOf: Optional[float]
    "`None` for any step."
    maxLength: int
    listValuePrefix: str
    listValueSeparator: str
    excludeFromImport: bool


class SettingsSaveResponse(TypedDict):
    """``POST /api/settings/values`` when the save went through only in part (AMP's `SettingsSaveResult`).

    A full save answers 204 with nothing.
    """

    # TODO: Check against a live capture; typed from AMP's OpenAPI `SettingsSaveResult` alone (#3-51.7, #3-56.2ak).
    # AMP's docs say one comes back when exposure is turned off and the agent refuses to remove ports 80 and 443.
    notices: list[CodedErrorResponse]
    "What followed from the change and couldn't be done, each still to put right; the change itself stands."


class SetupAdminRequest(TypedDict):
    """The body of ``POST /api/auth/setup/admin``, the panel's first admin."""

    username: str
    email: str
    password: str


class SetupNetworkResponse(TypedDict):
    """``GET /api/auth/setup/network``, what the first-run setup's network step shows."""

    probe: NetworkProbe
    busExpandable: bool
    "If AMP runs the message bus, so `SetupModule.expand_setup_network` can open the message bus to other machines."
    busPublic: bool
    "If other machines can reach the message bus already."


class SetupProvisionStatusResponse(TypedDict):
    """``GET /api/auth/setup/database/provision/status``, how far AMP has got setting up its own message bus."""

    step: str
    """``"idle"``, ``"downloading"``, ``"configuring"``, ``"testing"``, ``"done"`` or ``"error"``.
    Only ``"idle"``, ``"downloading"``, ``"testing"`` and ``"done"`` were seen live.
    - AMP 3.0.1 reads ``"testing"`` (`percent` 100) between ``"downloading"`` and ``"done"``; AMP 3.0.0 went straight
      to ``"done"``.
    - Provisioning took about 5 seconds."""
    percent: int
    """0 to 100, eg. 0 while ``"downloading"`` and 100 at ``"done"``."""
    # TODO: Check `error` and type `failure` once a capture shows a provisioning that failed (#3-56.9).
    # Both were `None` in every capture. The web panel shows `failure` as a coded error, else `error` as text.
    error: Optional[str]
    """Why the provisioning failed as text, when `step` is ``"error"``, else `None`."""
    failure: Any
    """Why the provisioning failed as a coded error, when `step` is ``"error"``, else `None`."""


class ShardAddress(TypedDict):
    """One address a shard's port is reached at, from `ShardEndpointResponse.addresses`."""

    reach: str
    """``"Public"`` or ``"Local"``."""
    host: str
    port: int
    showPort: bool
    display: str
    """The address as the web panel shows it, eg. ``"192.0.2.1:25565"``."""
    source: str
    """``"Advertised"`` (the shard's `ShardInfraSettings.advertised_address`), ``"Published"`` (a publication through
    another spire), ``"Gateway"`` (the shard's gateway), ``"SpirePublicHost"``, ``"SpireAddress"``, ``"ExternalProbe"``
    or ``"LocalAddress"``."""
    uri: Optional[str]
    notes: list[str]
    """Each of ``"NeedsForward"``, ``"Cgnat"``, ``"NoHairpin"``, ``"ViaFront"`` (served by another spire),
    ``"Declared"``, ``"NotReady"`` (its tunnel still connecting) or ``"Paused"`` (a disabled publication)."""
    viaSpireId: Optional[str]
    "The front spire, on a published or gateway address."
    viaSpireName: Optional[str]
    # TODO: Drop the disabled publication sentence once AMP stops reading `Fault` on a disabled endpoint (U26d).
    # AMP 3.0.0 and 3.0.1 read `Fault` on a disabled publication's endpoint though its tunnel is up.
    tunnelState: Optional[str]
    """eg. ``"Connecting"``, ``"Fault"`` or ``"Ok"`` on a published or gateway address. A disabled publication's
    reads ``"Fault"`` though its tunnel is up."""


class ShardAgentResponse(TypedDict):
    """``GET /api/shards/{id}/agent``, the AMP agent that runs the shard."""

    runningVersion: Optional[str]
    "`None` while the shard is stopped."
    availableVersion: Optional[str]
    "The agent a restart would start, `None` when AMP can't tell."
    outOfDate: bool
    "`True` only for a running shard whose agent is older; `False` whenever either version is unknown."
    spireId: str
    spireName: str
    spireVersion: Optional[str]
    "The AMP version the shard's spire reports, `None` when it's unknown."
    installationVersion: str
    "The newest AMP version any spire reports."
    spireBehind: bool
    "If the shard's spire runs an older AMP than the rest; it needs updating before a restart can help."


class ShardAppConfig(TypedDict):
    """A new shard's game settings, from `ShardCreatedResponse.appConfig`."""

    shardId: str
    tenantId: str
    values: dict[str, str]
    "Each setting's `fieldName` to its value, all strings."
    updatedAt: str
    updatedByUserId: str


class ShardArchiveInfoResponse(TypedDict):
    """``GET /api/shards/{id}/files/archive-info``, what an archive holds."""

    entries: int
    totalSize: int
    "In bytes, unpacked."


class ShardArchiveRequest(TypedDict):
    """The body of ``POST /api/shards/{id}/files/archive``."""

    paths: list[str]
    destination: str


class ShardAttentionResponse(TypedDict):
    """A shard waiting on a user, from ``GET /api/shards/attention``, eg. a game's update waiting for a sign-in."""

    shardId: str
    name: str
    message: str
    "What it waits for, as AMP shows it, eg. a sign-in URL."


class ShardCloneRequest(TypedDict):
    """The body of ``POST /api/shards/{id}/clone``."""

    newName: str
    content: int
    "A `CloneContent` value."
    targetSpireId: Optional[str]


class ShardCloneResponse(TypedDict):
    """``POST /api/shards/{id}/clone``; the copy appears at once, with `installedAt` `None`."""

    shardId: str
    "The copy's ID."


class ShardConfigImportResponse(TypedDict):
    """``POST /api/shards/{id}/config/import``, the settings read back from a config file."""

    applied: list[str]
    "The settings whose values came from the file."
    excluded: list[str]
    "Settings AMP keeps for itself, eg. ports."
    missing: list[str]
    "Settings the file doesn't have."


class ShardConsoleRequest(TypedDict):
    """The body of ``POST /api/shards/{id}/console``."""

    command: str
    promptReply: bool


class ShardCreatedResponse(TypedDict):
    """``POST /api/shards`` (201), the new shard with its first settings and ports."""

    shard: ShardResponse
    infraSettings: ShardInfraSettingsResponse
    "How the shard runs, read as a `ShardInfraSettings` through `Shard.infra_settings`."
    appConfig: ShardAppConfig
    ports: ShardPortAssignments
    portOutcomes: list[ShardPortOutcome]
    overLicenceLimit: bool


class ShardCreateRequest(TypedDict):
    """The body of ``POST /api/shards``."""

    templateSlug: str
    displayName: str
    description: str
    spireId: Optional[str]
    "`None` for the panel's own spire."
    startNow: bool
    startOnBoot: bool
    credentialId: NotRequired[str]


class ShardCredentialResponse(TypedDict):
    """``GET /api/shards/{id}/credential``, the stored secret a shard uses, eg. a Steam login."""

    required: bool
    "If the game can only be downloaded by an account that owns it, so an update needs a credential."
    credential: Optional[CredentialResponse]
    """The credential the shard uses, `None` when the shard has no credential. The credential's `username` is there
    only for the user who created the credential."""
    usable: list[CredentialResponse]
    "The credentials the logged in user may give the shard: their own credentials and the public credentials."


# TODO: Check against a live capture; typed from AMP's OpenAPI `CustomPortDef` alone (#3-56.1z).
# Every `ShardPortAssignments` captured has an empty `customPorts`.
class ShardCustomPort(TypedDict):
    """A port a user added to a shard, from `ShardPortAssignments.customPorts`; its number is in `assignments`."""

    ref: str
    name: str
    protocol: str
    """``"Both"``, ``"TCP"`` or ``"UDP"``."""
    createdAt: str
    createdByUserId: str


class ShardCustomPortRequest(TypedDict):
    """The body of ``POST /api/shards/{id}/ports/custom``."""

    name: str
    protocol: PortProtocol
    port: Optional[int]
    "`None` lets AMP pick a free port."


class ShardDetailsRequest(TypedDict):
    """The body of ``PATCH /api/shards/{id}``; a `None` field is left out."""

    displayName: Optional[str]
    description: Optional[str]
    tags: Optional[list[str]]


class ShardEndpointResponse(TypedDict):
    """One public port of a shard and where players reach it, from ``GET /api/shards/{id}/endpoints``."""

    portRef: str
    name: str
    "A translation key, or the port's own name."
    port: int
    protocol: str
    isPrimary: bool
    isPublic: bool
    addresses: list[ShardAddress]


class ShardExtractRequest(TypedDict):
    """The body of ``POST /api/shards/{id}/files/extract``."""

    path: str
    destination: Optional[str]
    "`None` for the archive's own folder."
    overwrite: bool


class ShardExtractResponse(TypedDict):
    """``POST /api/shards/{id}/files/extract``, how many files came out of an archive; a copy out of one answers it too."""

    extracted: int
    skippedOnDisk: int
    "Files already there that weren't overwritten, or no longer in the archive."
    skippedDenied: int
    "Files the logged in user may not write at the destination."
    skippedBlocked: int
    "Files of a type the panel blocks."
    skippedManaged: int
    "Files AMP writes itself from the shard's settings."
    # TODO: Check against a live capture; typed from AMP's OpenAPI `ExtractResultDto` alone (#3-56.1z).
    # Every capture has it empty.
    examples: list[str]
    "A few of the skipped paths."


class ShardFileACLResponse(TypedDict):
    """``GET /api/shards/{id}/files/acl``, who may do what to a path."""

    path: str
    principals: list[FilePrincipal]
    canEdit: bool


class ShardFileContentResponse(TypedDict):
    """``GET /api/shards/{id}/files/content``, a text file's content."""

    content: str


class ShardFileIgnoresResponse(TypedDict):
    """``GET /api/shards/{id}/files/ignore``, the ignored entries among a folder's children."""

    amp: list[str]
    """The ones AMP ignores itself, eg. ``"server.jar"``."""
    user: list[str]
    "The ones a user set, see `ShardModule.set_shard_file_ignored`."


class ShardFileResponse(TypedDict):
    """One file or folder, from ``GET /api/shards/{id}/files``."""

    path: str
    "Relative to the shard's folder, not to the folder listed."
    name: str
    isDirectory: bool
    isLink: bool
    size: int
    "In bytes."
    modified: str


class ShardFileStartResponse(TypedDict):
    """``GET /api/shards/{id}/files/start``, the folder the web panel's file manager opens at."""

    path: str
    "Relative to the shard's folder, empty for the shard's folder itself."


class ShardImportResponse(TypedDict):
    """``GET /api/shards/{id}/import``, what the import that made the shard brought across."""

    importedAt: str
    sourcePath: str
    "The folder it was imported from, on the spire."
    source: int
    """Where AMP found it, the web panel's numbers: eg. 0 a folder named by hand, 8 LinuxGSM."""
    recovered: int
    refused: int
    nameOrigin: int
    # TODO: Check these against a live capture; typed from AMP's OpenAPI `ImportChangeRecord` alone (#3-53, #3-56.1z).
    # Every capture has them empty; they need an import that moves a port or leaves something behind.
    portsMoved: list[ShardPortOutcome]
    "The ports that couldn't be kept, with the old and new numbers and why."
    settingsExcluded: list[str]
    "Settings AMP kept for itself rather than taking from the files."
    settingsMissing: list[str]
    "Settings the files didn't have."
    settingsRefused: list[str]
    "Settings AMP refused, as the value names a path outside the shard or a program to run."
    filesSkipped: list[ShardImportSkippedFile]
    hasAnythingToSay: bool


# TODO: Check against a live capture; typed from AMP's OpenAPI `ImportSkippedFile` alone (#3-53, #3-56.1z).
# Every capture has `filesSkipped` empty.
class ShardImportSkippedFile(TypedDict):
    """A file an import left behind, from `ShardImportResponse.filesSkipped`."""

    path: str
    "Relative to the server's folder, with forward slashes."
    reason: str
    "AMP's token for why."


class ShardInfraChanges(TypedDict, total=False):
    """The settings `ShardModule.update_shard_infra` takes as keyword arguments, each described there."""

    start_on_boot: bool
    auto_restart_on_crash: bool
    startup_order: int
    sleep_mode: bool
    advertised_address: str
    advertised_address_includes_port: bool
    container_mode: str
    "A `ShardContainerMode` member or its value."
    container_image_override: str
    memory_limit_mb: int
    memory_reservation_mb: int
    memory_swap_mb: int
    cpu_limit: float
    max_users_cap: int
    enable_analytics: bool
    user_specific_data: bool
    minimum_session_time_for_retention: int
    enable_geo_filtering: bool
    blocked_countries: list[str]
    allowed_countries: list[str]
    block_unknown_countries: bool
    geo_filter_kick_message: str
    geo_filter_kick_command: str
    disk_limit_mb: int
    import_config_files_from_sftp: bool
    extra_environment: dict[str, str]


class ShardInfraSettingsResponse(TypedDict):
    """A shard's settings for how it runs, as AMP sends them in `ShardCreatedResponse.infraSettings`.

    `Shard.infra_settings` reads them as a `ShardInfraSettings`, which describes each setting.
    """

    shardId: str
    tenantId: str
    startOnBoot: bool
    autoRestartOnCrash: bool
    startupOrder: int
    sleepMode: bool
    advertisedAddress: str
    advertisedAddressIncludesPort: bool
    containerMode: str
    containerImageOverride: Optional[str]
    memoryLimitMb: int
    memoryReservationMb: int
    memorySwapMb: int
    cpuLimit: float
    maxUsersCap: int
    enableAnalytics: bool
    userSpecificData: bool
    minimumSessionTimeForRetention: int
    enableGeoFiltering: bool
    blockedCountries: list[str]
    allowedCountries: list[str]
    blockUnknownCountries: bool
    geoFilterKickMessage: str
    geoFilterKickCommand: str
    diskLimitMb: int
    importConfigFilesFromSftp: bool
    extraEnvironment: dict[str, str]
    updatedAt: str
    updatedByUserId: str


class ShardManagedFileResponse(TypedDict):
    """One file AMP writes itself from a shard's settings, from ``GET /api/shards/{id}/files/managed``."""

    path: str
    """Relative to the shard's root, eg. ``"server.properties"``."""
    kind: str
    """eg. ``"merged"`` (AMP merges its settings into the file, eg. ``"server.properties"``) or ``"generated"``
    (AMP writes the whole file, eg. ``"eula.txt"``)."""
    importable: bool
    "`True` on a merged file and `False` on a generated one."
    source: str
    """eg. ``"config"``."""
    fieldName: Optional[str]


class ShardMigrationRequest(TypedDict):
    """The body of ``POST /api/shards/{id}/migration/spire``."""

    targetSpireId: str
    targetDatastoreId: str
    bringBackups: bool
    stopIfRunning: bool
    startAfterMove: NotRequired[bool]
    "Left out, AMP uses `stopIfRunning`."


class ShardMigrationTargetResponse(TypedDict):
    """One datastore a shard could move to, from ``GET /api/shards/{id}/migration/targets``.

    The spire's other datastores, without the one the shard is in.
    """

    id: str
    name: str
    path: str
    """eg. ``"/opt/cubecoders/amp3/data/Datastores/my_store"``."""


class ShardPortAssignments(TypedDict):
    """The ports a new shard was given, from `ShardCreatedResponse.ports`."""

    shardId: str
    tenantId: str
    assignments: dict[str, int]
    """A port's `ref` to its number, eg. ``{"ServerPort": 25565}``."""
    customPorts: list[ShardCustomPort]
    privatePortRefs: list[str]
    assignedAt: str
    assignedBySpireId: str


class ShardPortOutcome(TypedDict):
    """How one of a new shard's ports was given out, from `ShardCreatedResponse.portOutcomes`."""

    ref: str
    requested: Optional[int]
    assigned: int
    reason: int
    """Why the port is what it is, AMP's own numbers: 0 nothing found to keep, 1 kept as it was, 2 taken by another
    server, 3 outside the range AMP hands out, 4 unavailable. A shard made by `Panel.create_shard` always reads 0, as
    only an import finds ports to keep; 1 to 4 come from AMP's docs and haven't been seen live."""
    moved: bool


class ShardPortResponse(TypedDict):
    """One of a shard's ports, from ``GET /api/shards/{id}/ports``."""

    ref: str
    """eg. ``"ServerPort"``; a custom port's is ``"Custom"`` and its name without spaces."""
    name: str
    "A translation key for a template's port, the given name for a custom one."
    description: str
    protocol: str
    """``"Both"``, ``"TCP"`` or ``"UDP"``."""
    port: int
    isPublic: bool
    custom: bool
    primary: bool


class ShardResponse(TypedDict):
    """One shard, AMP 3's name for an Instance, from ``GET /api/shards``."""

    id: str
    tenantId: str
    displayName: str
    description: str
    name: str
    "A short name made from the first display name; renaming doesn't change it."
    templateSlug: str
    displayImageSource: str
    """eg. ``"steam:380840"`` or ``"internal:MinecraftJava"``."""
    spireId: str
    datastoreId: str
    workingDirName: str
    createdByUserId: str
    createdAt: str
    installedAt: Optional[str]
    "`None` until the first update installs the game."
    installedVersion: Optional[str]
    "`None` even after an update."
    startAfterUpdateTaskId: Optional[str]
    tags: list[str]
    suspended: bool
    diskWarningAcked: bool
    deleted: bool
    "A deleted shard stays until it is purged; most calls on it answer 409."
    deletedAt: Optional[str]


class ShardScheduleRequest(TypedDict):
    """The body of ``POST /api/shards/{id}/schedules`` and ``PUT /api/shards/{id}/schedules/{schedule_id}``."""

    name: str
    description: Optional[str]
    trigger: ScheduleTrigger
    steps: list[ScheduleStep]
    timeout: Optional[str]
    enabled: bool


class ShardScheduleResponse(TypedDict):
    """One of a shard's schedules, from ``GET /api/shards/{id}/schedules``; making or changing one answers with it too.

    ``GET /api/shards/{id}/schedules/{schedule_id}`` answers one alone.
    """

    definition: ScheduleDefinition
    """The schedule. A parameter listed in `withheld` reads ``"[withheld]"``, and sending that back keeps what AMP
    holds."""
    status: Optional[ScheduleStatus]
    "`None` until it has run."
    nextFireTime: Optional[str]
    "`None` while it's off, or for an event trigger."
    withheld: list[ScheduleWithheld]
    """The step parameters AMP hides from a user who can't change schedules, eg. a webhook's `url` and `body`; empty
    for one who can."""


class ShardSettingCandidatesResponse(TypedDict):
    """``GET /api/shards/{id}/settings/{field}/candidates``, the values a setting can take, eg. game versions."""

    candidates: list[SettingCandidate]
    fetchedAt: str
    failureReason: Optional[str]
    fromCache: bool
    age: str
    "How old the list is, as a time span."


class ShardSettingResponse(TypedDict):
    """One of a shard's game settings and its value, from ``GET /api/shards/{id}/settings``."""

    spec: SettingSpec
    value: str
    """Every value is a string, eg. ``"true"`` or ``"10"``."""


class ShardSFTPResponse(TypedDict):
    """``GET /api/shards/{id}/sftp``, how to reach a shard's files over SFTP."""

    enabled: bool
    host: str
    port: int
    userName: str
    folder: str
    hostKeyFingerprint: Optional[str]
    "The spire's SSH host key, to check on the first connect; `None` for a shard on another spire than the panel's."
    hasKeys: bool
    "If the logged in user has an SSH key added, see `AccountModule.add_ssh_key`."


class ShardSleepStatus(TypedDict):
    """If a shard can sleep, from `ShardStatus.sleep`."""

    available: bool
    reason: Optional[str]
    "Why it can't, in English; `None` when it can."
    reasonCode: Optional[str]
    """A translation key for `reason`, eg. ``"agent.msg.sleepUnavailable"``."""
    reasonParams: Optional[dict[str, str]]
    reportedAt: str


class ShardStateMetrics(TypedDict):
    """A running shard's load, from `ShardStatus.metrics`. The key names differ from `ShardMetrics`."""

    cpuUsagePercent: float
    memoryUsageMB: int
    memoryLimitMB: int
    activeConnections: int
    networkInKBps: int
    networkOutKBps: int
    diskReadKBps: int
    diskWriteKBps: int
    taskQueueLength: int


class ShardUpdateResponse(TypedDict):
    """``POST /api/shards/{id}/update`` (202); follow it with `TaskModule.get_running_tasks`."""

    taskId: str


class ShardUploadChunkResponse(TypedDict):
    """``POST /api/shards/{id}/files/upload-chunk``."""

    received: int
    "How many bytes AMP holds so far, all chunks counted."


class ShardUploadSessionResponse(TypedDict):
    """``POST /api/shards/{id}/files/upload-start``, a chunked upload to send to."""

    sessionId: str
    received: int
    "How many bytes AMP already holds, so an upload can carry on from there."
    via: str
    """eg. ``"direct"``."""


class ShardUsage(TypedDict):
    """One shard's disk use, from `DatastoreUsage.shards`, or `ShardModule.get_shard_disk`. A deleted shard stays until it is purged."""

    kind: str
    """``"Shard"``, ``"Backups"`` or ``"Orphan"``, a folder no shard owns, eg. the copy a move leaves on the old spire.
    An orphan's `shardId` is all zeros and its `displayName` empty."""
    shardId: str
    name: str
    "The shard's folder name in the datastore."
    sizeMb: int
    deleted: bool
    deletedAt: Optional[str]
    displayName: str
    limitMb: int
    """The shard's disk limit, its `ShardInfraSettings.disk_limit_mb`; 0 for none, and 0 too until the next measure after
    one is set."""
    limitLevel: str
    """``"None"``, ``"Warning"``, ``"Critical"`` or ``"Exceeded"``, against `limitMb` once the disk use is measured."""


class SnapshotMetaRequest(TypedDict):
    """The body of ``PUT /api/shards/{id}/snapshots/{snapshot_id}/meta``.

    AMP replaces all three, so a field left out or `None` is cleared.
    """

    name: str
    description: str
    sticky: bool


class SnapshotRequest(TypedDict):
    """The body of ``POST /api/shards/{id}/snapshots``."""

    kind: int
    "A `SnapshotKind` value."
    content: int
    "A `SnapshotContent` value."
    name: Optional[str]
    """`None` lets AMP name it, eg. ``"Manual Backup - admin"``."""
    description: Optional[str]
    "`None` or empty lets AMP describe it."
    sticky: bool


class SnapshotSettingsRequest(TypedDict):
    """The body of ``PUT /api/shards/{id}/snapshots/settings``."""

    maxBackupSizeMb: int
    maxTotalStorageMb: int
    stopWhenNoQuiesce: bool


class SnapshotSettingsResponse(TypedDict):
    """``GET /api/shards/{id}/snapshots/settings``, a shard's snapshot limits."""

    maxBackupSizeMb: int
    "0 for no limit."
    maxTotalStorageMb: int
    "0 for no limit."
    stopWhenNoQuiesce: bool


class SpireCPU(TypedDict):
    """The spire's processor, from `SpirePlatform.cpu`."""

    sockets: int
    cores: int
    threads: int
    modelName: str
    vendor: str
    totalCores: int
    totalThreads: int


class SpireEnrollmentAdmission(TypedDict):
    """The machine that used the enrolment's join file, from `SpireEnrollmentResponse.admission`."""

    fingerprint: str
    """eg. ``"4W26-457D-1PBK"``; the joining machine shows the same one in `HealthStatusResponse.messageParams`."""
    machineName: str
    sourceAddress: Optional[str]
    """The address and port it came from, eg. ``"192.0.2.1:33002"``; `None` when AMP couldn't ask the message bus."""
    requestedAt: str
    lastSeenAt: str
    expiresAt: str
    approvedAt: Optional[str]
    approvedByName: Optional[str]
    deniedAt: Optional[str]
    deniedByName: Optional[str]
    suspect: bool
    "If another machine presented the same join file, from the web panel's text."
    replayCount: int
    "How many times another machine presented it."
    replayFingerprint: Optional[str]
    "The latest other machine's fingerprint."


class SpireEnrollmentCreatedResponse(TypedDict):
    """``POST /api/spires/enrollments`` (201), a new join file."""

    enrollment: SpireEnrollmentResponse
    joinBlob: str
    "The join file itself, a secret the new machine's setup takes. The enrolment list doesn't send it again."


class SpireEnrollmentHostResponse(TypedDict):
    """One address a new spire could join on, from ``GET /api/spires/enrollments/hosts``."""

    host: str
    kind: str
    """eg. ``"internal"`` or ``"external"`` (the public address)."""
    interfaceName: str
    isPrimary: bool
    suggested: bool
    note: Optional[str]
    """eg. ``"needsForward"`` on the public address."""


class SpireEnrollmentRequest(TypedDict):
    """The body of ``POST /api/spires/enrollments``."""

    label: str
    hosts: list[str]
    expiresInHours: NotRequired[int]
    entryNode: NotRequired[bool]
    publicHost: NotRequired[str]
    "The entry node's public address; AMP ignores it on a standard enrolment."


class SpireEnrollmentResponse(TypedDict):
    """One join file from ``GET /api/spires/enrollments``, newest first. Approving one answers with it too."""

    id: str
    label: str
    createdByName: str
    createdAt: str
    expiresAt: str
    status: str
    """``"pending"`` (made), ``"awaitingapproval"`` (a machine used it), ``"approved"``, ``"denied"``,
    ``"redeemed"`` (the machine joined), ``"expired"`` or ``"revoked"``."""
    redeemedAt: Optional[str]
    redeemedSpireId: Optional[str]
    """The spire the machine became, once `status` is ``"redeemed"``."""
    revokedAt: Optional[str]
    revokedReason: Optional[str]
    "`None` when the revoke sent no reason."
    role: str
    """``"standard"``, or ``"publicentrynode"`` for a public entry node, which hosts no shards."""
    entryNodeHost: Optional[str]
    """The public address AMP dials for an entry node, eg. ``"203.0.113.10"``; `None` on a standard enrolment."""
    entryNodeState: Optional[str]
    """How AMP's last try to reach the entry node went: ``"waiting"``, ``"unreachable"``, ``"notpasted"``,
    ``"wrongsecret"`` or ``"collected"``. It stays ``"waiting"`` after a revoke."""
    entryNodeStateCode: Optional[str]
    "A translation key with more about `entryNodeState`, when there is more to say."
    # TODO: Check against a live capture; typed from AMP's OpenAPI `EnrollmentDto` alone (#3-56.2z).
    # Every capture has it `None`; an entry node only fills it once AMP has reached the machine.
    entryNodeStateParams: Optional[dict[str, str]]
    "Values for the `entryNodeStateCode` translation."
    entryNodeObservedHost: Optional[str]
    "The address the entry node says it has, when it differs from `entryNodeHost`; `None` until it answers."
    entryNodeBlockedPort: Optional[int]
    "The tunnel port the entry node can't bind, `None` when it can."
    # TODO: Check these two against a live capture; typed from AMP's OpenAPI `EnrollmentDto` alone (#3-56.2at).
    # Every capture has them `None`; they need an entry node AMP has reached.
    tunnelPhase: Optional[str]
    "How far the entry node's tunnel has got, a `TunnelStatus.phase`; `None` before AMP collects its details."
    tunnelFault: Optional[str]
    "What is wrong at the panel's end, eg. its system agent not running; `None` when nothing is, or the fault is elsewhere."
    admission: Optional[SpireEnrollmentAdmission]
    "The machine that used the join file; `None` until one does."


class SpireEnrollmentRevokeRequest(TypedDict):
    """The body of ``DELETE /api/spires/enrollments/{id}``."""

    reason: str


class SpireExpiredPurgeResponse(TypedDict):
    """``POST /api/spires/{id}/purge-expired-shards``, how many deleted shards AMP is purging."""

    purging: int
    "A shard deleted but not past its keeping time stays, and isn't purged."


class SpireImportBlockedItem(TypedDict):
    """A server the import can't take, from `SpireImportPreflightResponse.blocked`."""

    candidatePath: str
    reason: int
    "Why, as a number; 1 was seen for a folder outside every import root."
    detail: str


# TODO: Check against a live capture; typed from AMP's OpenAPI `DiscoveredPort` alone (#3-53, #3-56.2i).
# Both captures have `portsDiscovered` empty.
class SpireImportDiscoveredPort(TypedDict):
    """A port number a scan read from a found server's own config file, from `SpireImportRecovery.portsDiscovered`."""

    ref: str
    """The template port it belongs to, eg. ``"ServerPort"``."""
    port: int
    configFile: str
    "The file it was read from."
    address: str
    "The key in that file."


class SpireImportEvidence(TypedDict):
    """A clue a scan read a server or a template match from, in `SpireImportScanServer.evidence` and `SpireImportMatch.evidence`."""

    detail: str
    relativePath: str
    weight: int


class SpireImportItem(TypedDict):
    """One server in the body of ``POST /api/spires/{id}/import`` and ``POST /api/spires/{id}/import/preflight``.

    Its keys come from the web panel's code.
    """

    path: str
    "The server's folder, from `SpireModule.scan_spire_imports`."
    templateSlug: str
    "The template to import it as."
    content: int
    """What to bring across, bit flags as the web panel's code has them: 1 the game's state, 2 its settings, 4 its
    network setup, so 7 is all of it."""


# TODO: Check against a live capture; typed from AMP's OpenAPI `LivenessEvidence` alone (#3-53, #3-56.2ar).
# A running server left `liveness` empty on AMP 3.0.0, and so did a stand-in listening on the game's port on 3.0.1.
class SpireImportLiveness(TypedDict):
    """A sign a found server is still running, from `SpireImportReadyItem.liveness`."""

    code: str
    "A translation key for the reason."
    message: str
    "The English text, naming what was found."


class SpireImportMatch(TypedDict):
    """A template a found server could be imported as, from `SpireImportScanServer.matches`."""

    templateSlug: str
    displayName: str
    confidence: int
    "How sure AMP is, as a number; 1 (weak in the web panel's names) was seen."
    evidence: list[SpireImportEvidence]


class SpireImportPreflightResponse(TypedDict):
    """``POST /api/spires/{id}/import/preflight``, if the servers can be imported, before `SpireModule.import_spire_servers`."""

    ready: list[SpireImportReadyItem]
    blocked: list[SpireImportBlockedItem]
    requiredBytes: int
    availableBytes: int
    batchBlock: int
    """What stops the whole batch, the web panel's numbers: 0 nothing, 1 the licence's shard limit, 2 not enough space,
    3 the datastore's soft limit, 4 nothing importable."""
    shortfallBytes: int
    licenceHeadroom: Optional[int]
    "How many more shards the licence allows, `None` with no limit."
    sizesAreUnderstated: bool
    links: int
    canProceed: bool


class SpireImportReadyItem(TypedDict):
    """A server the import can take, from `SpireImportPreflightResponse.ready`."""

    candidatePath: str
    size: SpireImportSize
    exists: bool
    # TODO: Check these against a live capture; typed from AMP's OpenAPI `PreflightCandidate` alone (#3-53, #3-56.2ar).
    # A running server, and a folder imported before, both still left them empty on AMP 3.0.0 and 3.0.1.
    liveness: list[SpireImportLiveness]
    "Signs the server is still running, empty when AMP found no such signs."
    unavailableReason: Optional[str]
    "Why the folder couldn't be read at all, in the words of what read it; `None` when it could."
    alreadyImportedAs: Optional[str]
    "The name of the shard already made from this folder, `None` when there's none."


class SpireImportRecovery(TypedDict):
    """What an import of a found server could bring back, from `SpireImportScanServer.recovery`."""

    available: int
    "The parts that can be brought back, the same bit flags as `SpireImportItem.content`."
    settingsRecovered: int
    "How many settings were read from the server's own config files."
    # TODO: Check against a live capture; typed from AMP's OpenAPI `ImportRecoveryReport` alone (#3-53, #3-56.2i).
    # Both captures have it empty.
    portsDiscovered: list[SpireImportDiscoveredPort]
    "The ports read from the server's config files."
    portsNotDiscovered: list[str]
    """The template's port names nothing on disk gave, eg. ``"Voice"``; they get new numbers."""
    primaryPortRecovered: bool
    "If the port players connect to was kept."
    settings: int
    defaultSelection: int
    "What the import takes unless told otherwise, the same bit flags as `SpireImportItem.content`: all of `available`."
    hasCaveats: bool


class SpireImportRequest(TypedDict):
    """The body of ``POST /api/spires/{id}/import`` and ``POST /api/spires/{id}/import/preflight``."""

    items: list[SpireImportItem]
    enterOtherVolumes: bool


class SpireImportResponse(TypedDict):
    """``POST /api/spires/{id}/import`` (202): the import runs as a ``"ServerImport"`` running task."""

    taskId: str


class SpireImportScanRequest(TypedDict):
    """The body of ``POST /api/spires/{id}/import/scan``."""

    roots: list[str]
    automatic: NotRequired[bool]


class SpireImportScanResponse(TypedDict):
    """``POST /api/spires/{id}/import/scan``, game servers from other panels that could be imported."""

    servers: list[SpireImportScanServer]
    unreadable: list[SpireImportUnreadable]
    "Folders AMP couldn't look in, eg. one outside every import root."
    # TODO: Check against a live capture; typed from AMP's OpenAPI `DiscoveryResult` alone (#3-53, #3-56.2ar).
    # Every capture has it empty.
    truncatedRoots: list[str]
    "The roots where a cap stopped the scan."
    timedOut: bool


class SpireImportScanServer(TypedDict):
    """A game server a scan found, from `SpireImportScanResponse.servers`."""

    path: str
    rootPath: str
    source: int
    """Where AMP found it, the web panel's numbers: eg. 0 a folder named by hand, 8 LinuxGSM."""
    matches: list[SpireImportMatch]
    evidence: list[SpireImportEvidence]
    suggestedName: str
    installedVersion: Optional[str]
    installedVersionIsBuildId: bool
    recovery: SpireImportRecovery
    listingTruncated: bool
    links: int
    # TODO: Check these against a live capture; typed from AMP's OpenAPI `DiscoveredServer` alone (#3-53, #3-56.2ar).
    # A folder imported before still left them empty on AMP 3.0.0.
    unmatchedSteamAppIds: list[str]
    "Steam apps found that no template covers."
    alreadyImportedShardId: Optional[str]
    "The shard already made from this folder, `None` when there's none."
    alreadyImportedAs: Optional[str]
    "That shard's name."


class SpireImportSize(TypedDict):
    """A found server's size, from `SpireImportReadyItem.size`."""

    bytes: int
    files: int
    truncated: bool
    links: int
    isUnderstated: bool
    # TODO: Check against a live capture; typed from AMP's OpenAPI `CandidateSize` alone (#3-53, #3-56.2ar).
    # Every capture has it empty.
    unreadableDirectories: list[str]
    "Folders that couldn't be read, so their files aren't counted."


class SpireImportUnreadable(TypedDict):
    """A folder a scan couldn't look in, from `SpireImportScanResponse.unreadable`."""

    path: str
    code: str
    """eg. ``"discovery.error.accessDenied"``."""
    message: str


class SpireIPAddress(TypedDict):
    """One of the spire's addresses, from `SpirePlatform.reportedIps`."""

    address: str
    isV6: bool
    isInternal: bool
    isDhcp: Optional[bool]
    isPrimary: bool
    isTunnel: bool
    interfaceName: str


class SpireIPOptionResponse(SpireIPAddress):
    """One address a shard can bind to, from ``GET /api/spires/{id}/ip-options``."""

    role: str
    """eg. ``"all"`` (``"0.0.0.0"``), ``"localhost"``, ``"address"`` or ``"auto"`` (``"@auto-pool"``)."""


class SpireJavaRuntime(TypedDict):
    """A Java installed on the spire's machine, from `SpirePlatform.installedJava`, for a game that isn't in a container."""

    path: str
    """The Java program, the value a setting takes, eg. ``"/usr/lib/jvm/java-21-openjdk-amd64/bin/java"``, or
    ``"$PATH/java"`` for whichever Java the machine finds at launch."""
    majorVersion: int
    "eg. 21; 0 when AMP couldn't tell."
    vendor: str
    """eg. ``"OpenJDK"`` or ``"Adoptium"``; empty when AMP couldn't tell."""
    kind: str
    """``"JDK"`` or ``"JRE"``, empty when AMP couldn't tell. A JRE package can read ``"JDK"``."""
    name: str
    """The install folder's name, eg. ``"java-21-openjdk-amd64"``."""
    isDefault: bool
    "If it's the Java the machine's PATH finds."
    isSystemDefault: bool
    """If it's the ``"$PATH/java"`` entry rather than a fixed install."""


class SpirePlatform(TypedDict):
    """The machine a spire runs on, from `SpireStatus.platform`."""

    os: int
    "eg. 2 on Ubuntu."
    architecture: int
    "eg. 1 on x86_64."
    osName: str
    hardwareName: str
    hostname: str
    cpu: SpireCPU
    installedRamMb: int
    virtualization: int
    "eg. 5 on a QEMU/KVM VM."
    reportedIps: list[SpireIPAddress]
    installedJava: list[SpireJavaRuntime]
    "Empty with no Java installed."
    externalIp: str
    "The address the internet sees the machine as, empty when AMP couldn't find it."
    reachability: str
    """``"Unknown"``, ``"Direct"``, ``"Nat"`` (needs a port forward) or ``"Cgnat"`` (only a tunnel works)."""
    freeDiskMb: int
    totalDiskMb: int
    freeRamMb: int
    loadAvgPercent: int
    reportedAt: str


class SpirePortResponse(TypedDict):
    """One port a shard uses on a spire, from ``GET /api/spires/{id}/ports``."""

    port: int
    protocol: str
    """eg. ``"TCP"`` or ``"UDP"``."""
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
    """eg. ``"_root"``."""
    displayName: str
    """The enrolment's `label` on a spire that joined."""
    description: str
    """eg. ``"Enrolled machine."`` on a spire that joined."""
    isLocal: bool
    """If it's the machine that answered the call. A spire that joined serves the whole panel API too, so the same
    spire reads `True` from itself and `False` from the others."""
    platform: int
    "eg. 2 on Ubuntu, the same number as `SpirePlatform.os`."
    architecture: int
    tags: list[str]
    ipPool: list[str]
    natsPrefix: str
    allocatablePortRange: str
    """eg. ``"1024:65535"``."""
    acceptsDeployments: bool
    maxShards: int
    defaultContainerMode: str
    """One of ``"Native"``, ``"Docker"`` or ``"Podman"``, as the spire settings offer."""
    defaultContainerModeChosen: bool
    preferredContainerMode: str
    defaultShardIpBinding: str
    createdAt: str
    panelPort: int
    busPort: int
    "eg. 4222 on the panel's own spire, and 0 on one that joined."
    identityPublicKey: str
    role: int
    publicHost: str
    sftpEnabled: bool
    sftpPort: int
    sftpBindAddress: str
    sftpHoneypot: bool
    sftpIdleTimeoutSeconds: int
    sftpMaxSessionsPerUser: int
    shardSigningKeyPublic: str
    "Empty on the panel's own spire, set on one that joined."
    busUserPublicKey: str
    "Empty on the panel's own spire, set on one that joined."
    captureAgentOutput: bool
    logProcessLaunches: bool
    isPubliclyRoutable: bool
    isPublicEntryNode: bool
    canHostShards: bool
    acceptsNewShards: bool


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
    "A new shard has 100; saving sets each shard sent to its place in the list sent."


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


class SSHKeyRequest(TypedDict):
    """The body of ``POST /api/profile/sshkeys``."""

    key: str
    label: Optional[str]
    expiresAt: Optional[str]


class SSHKeyResponse(TypedDict):
    """One of the logged in user's SFTP keys, from ``GET /api/profile/sshkeys``; adding one answers with it too."""

    id: str
    label: str
    keyType: str
    """eg. ``"ssh-ed25519"``."""
    fingerprint: str
    """eg. ``"SHA256:MDGpHMbb3VwX0o1eKeHlX3rRfBMWpZmlRlINSshWK28"``."""
    bits: int
    addedAt: str
    lastUsedAt: Optional[str]
    expiresAt: Optional[str]


class SystemBusResponse(TypedDict):
    """``GET /api/system/bus``, the message bus spires talk to the panel over."""

    managed: bool
    "If AMP runs the bus itself."
    isPublic: bool
    "If other machines can reach it; a new spire can only join once it's public."
    joinInfo: BusJoinInfo
    # TODO: Check against a live capture; typed from AMP's OpenAPI `BusInfo` alone (#3-56.2at).
    # Every capture is of a bus AMP runs, which leaves it empty.
    servers: list[str]
    "The bus's addresses, on a bus AMP doesn't run (`managed` False)."


class TaskResponse(TypedDict):
    """``GET /api/tasks/{tenant_id}/{task_id}``, AMP's own record of a task and its steps.

    Not the same shape as a `RunningTask`: it has no `state`, `name`, message or `progressPercent`, but it has each
    step, and it stays after the task leaves the running list.
    """

    id: str
    tenantId: str
    ownerSpireId: str
    runId: str
    type: str
    """eg. ``"ApplicationUpdate"``."""
    displayName: str
    """eg. ``"Update my-shard"``."""
    targetType: str
    """eg. ``"Shard"``."""
    targetId: str
    principal: Principal
    visibility: int
    correlationId: WrappedID
    causationActionId: WrappedID
    actionId: WrappedID
    origin: int
    rootPrincipal: Principal
    status: int
    """AMP's numbers, as seen live: 0 not started yet, 1 running, 2 succeeded, 3 failed, 4 cancel asked for (not
    finished)."""
    steps: list[TaskStep]
    currentStep: Optional[TaskStep]
    "The step running now, `None` once finished."
    createdAt: str
    startedAt: Optional[str]
    "`None` until it starts."
    completedAt: Optional[str]
    "`None` until it finishes."
    cancellationRequestedAt: Optional[str]
    "When `TaskModule.cancel_task` was sent, `None` when it wasn't; set even when the task finished anyway."
    isTerminal: bool
    "If the task has finished."


class TaskStep(TypedDict):
    """One step of a task, from `TaskResponse.steps`, eg. one of an update's download steps."""

    id: str
    index: int
    "From 0."
    handlerType: str
    """What the step does, eg. ``"FetchURL"``, ``"Executable"`` or ``"CreateDirectory"``."""
    displayName: str
    """eg. ``"Server Download"``."""
    status: int
    "AMP's numbers, as seen live: 0 not started, 1 running, 2 succeeded, 3 failed, 4 skipped (after a failed step)."
    # TODO: Type `spanId`, `input`, `output`, `children` and `stackTrace` once a capture shows them filled in (#3-56.4c).
    # Every capture has them `None`, and `children` empty; AMP's OpenAPI gives this reply no shape.
    spanId: Optional[Any]
    input: Optional[Any]
    output: Optional[Any]
    progress: Optional[TaskStepProgress]
    "`None` until the step reports any."
    children: list[Any]
    startedAt: Optional[str]
    completedAt: Optional[str]
    errorMessage: Optional[str]
    """A translation key on a failed step, eg. ``"tasks.error.stepFailed"``."""
    stackTrace: Optional[Any]
    duration: Optional[str]
    """A time span, eg. ``"00:00:00.8139796"``; `None` while it runs and on a step that never started."""


class TaskStepProgress(TypedDict):
    """How far a step has got, from `TaskStep.progress`."""

    percent: int
    "How far the whole task has got."
    message: str
    """eg. ``"Server Files Copy"`` or ``"Update complete"``."""


class TemplateConfigFile(TypedDict):
    """A config file AMP writes the settings into, from `TemplateResponse.configFileMappings`."""

    configFile: str
    configFileTemplate: str
    configFormat: str
    """eg. ``"{0}={1}"``."""
    configFormatRegex: str
    configHeaderFormat: str
    configHeaderRegex: str
    configType: str
    """eg. ``"ini"``, ``"json"``, ``"kvp"`` or ``"template"``."""
    configEncoding: str
    autoMap: bool
    importable: bool
    subsections: list[TemplateConfigSection]


class TemplateConfigSection(TypedDict):
    """One section of a config file, from `TemplateConfigFile.subsections`."""

    heading: str
    settingMappings: dict[str, str]
    "A key in the file to a setting's `fieldName`."
    autoMap: bool


class TemplateConsole(TypedDict):
    """How AMP reads a game's console, from `TemplateResponse.console`. Most are regular expressions."""

    filterMatchRegex: str
    filterMatchReplacement: str
    throwawayMessageRegex: str
    appReadyRegex: str
    serverAuthURLPromptRegex: str
    serverAuthAckRegex: str
    userJoinRegex: str
    userIdKind: str
    """eg. ``"steam64"``, ``"minecraft-uuid"`` or empty."""
    userLeaveRegex: str
    userChatRegex: str
    preConnectRegex: str
    connectIPRegex: str
    updateAvailableRegex: str
    metricsRegex: str
    downloadProgressRegex: str
    startupProgressRegex: str
    logRegex: str
    suppressLogAtStart: bool
    activateLogRegex: str
    commandTriggers: dict[str, str]
    "A console line pattern to the command AMP answers it with."


class TemplateEvent(TypedDict):
    """A game event a schedule can wait for, from `TemplateResponse.events`."""

    id: str
    name: str
    "A translation key."
    description: str
    expression: str
    "The console line pattern that raises it."
    paramMap: dict[str, dict[str, str]]
    "Each value the event hands on, to its `name` and `description` translation keys."


class TemplateLifecycle(TypedDict):
    """How AMP starts, stops and sleeps a game, from `TemplateResponse.lifecycle`."""

    rootDir: str
    baseDirectory: str
    executableWin: str
    executableLinux: str
    executableContainer: str
    workingDir: str
    compatibility: int
    linuxCommandLineArgs: str
    windowsCommandLineArgs: str
    commandLineArgs: str
    commandLineParameterFormat: str
    commandLineParameterDelimiter: str
    rapidStartup: bool
    applicationReadyMode: int
    applicationReadyTimeoutSeconds: int
    monitorChildProcessName: str
    monitorDirectChildOnly: bool
    supportsUniversalSleep: bool
    wakeupMode: int
    sleepOnStart: bool
    sleepDelayMinutes: int
    sleepDozeDelayMinutes: int
    sleepStartThresholdSeconds: int
    steamUpdateAnonymousLogin: int
    exitMethod: int
    exitMethodWindows: int
    startupAuthenticationRequired: bool
    exitTimeout: int
    "How many seconds a stop waits for the game to exit before killing it."
    exitString: str
    """The console command that stops the game, eg. ``"stop"``."""
    exitFile: str
    # TODO: Drop the update sentence once AMP quiesces the game before an update's stop (U14).
    # AMP 3.0.1 stopped a running `minecraft-java` shard for an update with no `save-off` or `save-all flush`.
    quiescenceCommand: str
    """Commands sent before a stop or snapshot, split by ``;``, eg. ``"save-off;save-all flush"``.
    - AMP 3.0.1 doesn't send them when an update stops the game, so only the game's own stop command saves its data."""
    dequiescenceCommand: str
    quiesceAckRegex: str
    quiesceSettleDelayMilliseconds: int


class TemplateManagement(TypedDict):
    """How AMP talks to a game, from `TemplateResponse.management`."""

    hasWriteableConsole: bool
    hasReadableConsole: bool
    udpLogger: bool
    supportsLiveSettingsChanges: bool
    liveSettingChangeCommandFormat: str
    adminMethod: int
    remoteAdminPassword: str
    useRandomAdminPassword: bool
    persistRandomPassword: bool
    rconConnectDelaySeconds: int
    rconHeartbeatMinutes: float
    rconHeartbeatCommand: str
    ignoreSTDOUTAfterRCON: bool
    rconSelectIPMethod: int
    telnetLoginFormat: str
    telnetNewLineType: int
    tailLogFilePath: str
    applicationIPBinding: str
    forceIPBinding: bool
    supportsIPv6: bool
    useSteamQueryForStatus: bool
    maxUsers: int
    environmentVariables: dict[str, str]


class TemplateMetadata(TypedDict):
    """A template's name, image and requirements, from `TemplateResponse.metadata`."""

    displayName: str
    "The game's name, or a translation key on the newer templates."
    description: str
    created: str
    updated: str
    os: int
    "eg. 3."
    aarchSupport: int
    arch: int
    author: str
    url: str
    displayImageSource: str
    """``"steam:<app id>"``, ``"url:<address>"`` or ``"internal:<name>"``."""
    endpointURIFormat: str
    configManifest: str
    metaConfigManifest: str
    configRoot: str
    specificDockerImage: str
    """eg. ``"cubecoders/ampbase:debian"``."""
    dockerRequired: bool
    dockerBaseReadOnly: bool
    containerPolicy: int
    containerPolicyReason: str
    extraSetupStepsURI: str
    # TODO: Check these two against a live capture; typed from AMP's OpenAPI `SpecMetadata` alone (#3-56.1z).
    # Every template captured has them empty.
    prerequisites: list[str]
    "Packages the host must have."
    extraContainerPackages: list[str]
    "Packages AMP adds to the container image."
    configReleaseState: int
    noCommercialUsage: bool
    eulaLocation: str
    configVersion: str
    releaseNotes: str
    breakingReleaseNotes: str
    deprecatedReason: str
    minAMPVersion: str
    minAgentVersion: Optional[str]
    appIsMultiIPAware: bool


class TemplatePort(TypedDict):
    """A port a game needs, from `TemplateResponse.portRequirements`."""

    name: str
    description: str
    ref: str
    """eg. ``"ServerPort"``; a shard's ports use the same names."""
    port: int
    "The default port."
    protocol: str
    """``"Both"``, ``"TCP"`` or ``"UDP"``."""
    offset: int
    range: int
    rangeSeparator: str
    required: bool
    childPorts: Optional[list[TemplatePort]]
    "Ports that follow this one, eg. a query port one above it."


class TemplatePortReferences(TypedDict):
    """Which of a template's ports does what, from `TemplateResponse.portReferences`; ``"0"`` means none."""

    adminPortRef: str
    primaryApplicationPortRef: str
    universalSleepApplicationUDPPortRef: str
    universalSleepSteamQueryPortRef: str


class TemplateResponse(TypedDict):
    """One game template, from ``GET /api/templates``: the whole definition, not a summary."""

    id: str
    schemaVersion: int
    templateSlug: str
    """The template's name in every call, eg. ``"minecraft-java"``."""
    lifecycle: TemplateLifecycle
    management: TemplateManagement
    metadata: TemplateMetadata
    console: TemplateConsole
    portReferences: TemplatePortReferences
    updateStages: list[TemplateUpdateStage]
    "The steps an update runs, in order."
    preStartStages: list[TemplateUpdateStage]
    "The steps run before each start."
    portRequirements: list[TemplatePort]
    versionSources: list[TemplateVersionSource]
    settings: list[SettingSpec]
    configFileMappings: list[TemplateConfigFile]
    events: list[TemplateEvent]
    backupExclusions: list[str]
    """Paths a snapshot leaves out, eg. ``"logs/"``."""
    locale: dict[str, dict[str, str]]
    "A language to its translation keys and text; often empty."
    containerRuntimeAvailable: bool


class TemplateSourceResponse(TypedDict):
    """A git repository templates come from, from ``GET /api/templates/sources``."""

    id: str
    """eg. ``"official"`` or ``"amp3"``."""
    url: str
    isLocal: bool
    localDirectoryName: str
    isArchive: bool
    branch: str
    localPath: Optional[str]
    priority: int
    disabled: bool


class TemplateSyncResponse(TypedDict):
    """One source's sync, from ``POST /api/templates/sources/{id}/sync``."""

    sourceId: str
    headSha: str
    "The git commit the source is now at."
    changed: bool
    error: Optional[str]


class TemplateUpdateStage(TypedDict):
    """One step of an update or pre-start, from `TemplateResponse.updateStages`.

    The text fields a template leaves out are usually empty, but can be `None`, eg. on ``"duneawakening"``'s
    ``"Run schema migrations"`` step.
    """

    updateSource: int
    "What the step does, eg. 3 downloads a Steam app; the numbers aren't named anywhere AMP shows."
    updateStageName: str
    updateStageDescription: Optional[str]
    updateSourcePlatform: int
    updateSourceArch: int
    updateSourceData: str
    updateSourceArgs: str
    updateSourceVersion: Optional[str]
    updateSourceExtra: Optional[str]
    updateSourceTarget: Optional[str]
    unzipUpdateSource: bool
    overwriteExistingFiles: bool
    forceDownloadPlatform: NotRequired[int]
    """Only on a few update steps: the system whose files a SteamCMD step downloads, eg. 1 (Windows) for a server run
    through Wine or Proton. Left out, it's the host's own."""
    updateSourceConditionSetting: Optional[str]
    updateSourceConditionValue: Optional[str]
    deleteAfterExtract: bool
    runInBackground: bool
    skipOnFailure: bool
    processToolOutput: bool
    oneShot: bool


class TemplateVersionSource(TypedDict):
    """Where a setting's candidate values come from, eg. Mojang's version list, from `TemplateResponse.versionSources`."""

    id: str
    """The `SettingSpec.valueSourceId` that uses it, eg. ``"mojang.versions"``."""
    url: str
    documents: list[dict[str, str]]
    format: int
    select: str
    value: str
    display: str
    fields: dict[str, str]
    where: dict[str, str]
    urlTemplate: str
    sort: int
    cacheMinutes: int
    dependsOn: list[str]


# The claims `Session` reads from a token; the functional form, as the keys aren't names.
TokenClaims = TypedDict(
    "TokenClaims",
    {
        "amp:scope": str,
        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": str,
        "sid": str,
    },
    total=False,
)


class TokenResponse(TypedDict):
    """A new session token, from a login, `renew`, ``change-expired-password`` or the first-run admin setup.

    The token is a JWT sent back as ``Authorization: Bearer <token>``.
    It lasts 8 hours, or 28 days when the login asked for `rememberMe`.
    """

    token: str
    expiration: str
    "ISO 8601 in UTC, eg. ``2026-01-01T12:00:00.000000Z``."


class TunnelEnd(TypedDict):
    """One spire at an end of a tunnel, from `TunnelResponse.front` and `TunnelResponse.back`."""

    spireId: str
    spireName: str
    keyPublished: bool
    agentInstalled: bool
    "If the spire's tunnel agent is in place; `False` until AMP puts it there by itself on first use."
    agentReachable: bool
    agentError: Optional[str]
    """eg. ``"The file does not exist."`` while `agentInstalled` is `False`."""


class TunnelFrontHost(SpireEnrollmentHostResponse):
    """One address a tunnel front is reached on, from `TunnelFrontResponse.hosts`; the same shape as an enrolment host."""


class TunnelFrontResponse(TypedDict):
    """One spire that can front a tunnel, from ``GET /api/networking/tunnel-fronts``.

    A spire is listed once its ``"spire.publicHost"`` setting is set.
    """

    spireId: str
    displayName: str
    declaredHost: str
    """The spire's ``"spire.publicHost"``, eg. ``"amp.example.com"``."""
    hosts: list[TunnelFrontHost]
    "The declared host, the spire's network address and its public one."


class TunnelResponse(TypedDict):
    """One WireGuard tunnel between two spires, from ``GET /api/networking/tunnels``.

    AMP makes a tunnel on demand for a publication or a gateway through another spire, and removes the tunnel some
    seconds after the last publication or gateway using it goes.
    """

    id: str
    frontSpireId: str
    backSpireId: str
    "The spire the shard runs on."
    slot: int
    frontEndpointHost: str
    """The front spire's ``"spire.publicHost"``."""
    interfaceName: str
    """eg. ``"amp-4e992d89"``, from the tunnel's `id`."""
    listenPort: int
    "eg. 51820."
    frontAddress: str
    """The front's address on the tunnel, eg. ``"10.83.0.1"``."""
    backAddress: str
    """The back's address on the tunnel, eg. ``"10.83.0.2"``."""
    front: TunnelEnd
    back: TunnelEnd
    status: Optional[TunnelStatus]
    "`None` when it's new."
    createdAt: str
    permanentForEntryNode: bool


class TunnelStatus(TypedDict):
    """A tunnel's state, from `TunnelResponse.status`."""

    tunnelId: str
    up: bool
    rttMs: float
    "The round trip over the tunnel, eg. 1.5; 0 while it's down."
    lastProbeAt: str
    phase: str
    """One of ``"Provisioning"``, ``"AgentRejected"``, ``"AgentUnreachable"``, ``"Connecting"``, ``"Up"``,
    ``"Degraded"`` or ``"Releasing"``, as the web panel's code knows them."""
    faultSpireId: Optional[str]
    "The spire at fault, with `error` saying why."
    error: Optional[str]


# TODO: Check against a live capture; typed from AMP's OpenAPI `UpdateRolledBackDto` alone (#3-47.8, #3-56.2g).
# Every capture has `rolledBack` `None`: no update has failed on the test VMs.
class UpdateRolledBack(TypedDict):
    """An update this machine tried and AMP's supervisor (``amp3-host``) took back, from `UpdateStatusResponse.rolledBack`."""

    version: str
    "The version that was taken back."
    kind: str
    """Why: ``"crash-loop"``, ``"never-ready"``, ``"revert"``, ``"payload"``, or empty when the record doesn't say."""
    atUtc: str
    reason: str
    "The reason as the supervisor logged it."


# TODO: Check against a live capture; typed from AMP's OpenAPI `SpireBehindDto` alone (#3-47.8, #3-56.2ao).
# Every capture has `spiresBehind` empty: there was no older AMP 3 release to put a spire behind.
class UpdateSpireBehind(TypedDict):
    """A spire on an older AMP than the rest, from `UpdateStatusResponse.spiresBehind`; see `SpireModule.apply_spire_update`."""

    spireId: str
    name: str
    version: Optional[str]
    "The AMP version it reports, `None` when it's unknown."
    online: bool
    "If it can be told to update now."
    rolledBackFrom: Optional[str]
    "A newer version it tried and took back, `None` when it reports none."
    rolledBackKind: Optional[str]
    "Why, an `UpdateRolledBack.kind`; `None` when it's unknown."


class UpdateStatusResponse(TypedDict):
    """``GET /api/updates/check``, the panel's AMP version against the latest one. ``PUT /api/updates/stream`` answers with it too."""

    currentVersion: str
    stream: str
    """eg. ``"Mainline"`` or ``"Preview"``."""
    availableStreams: list[str]
    """eg. ``["Mainline", "Preview"]``."""
    latestVersion: str
    "Empty on a stream with no build yet."
    updateAvailable: bool
    mandatory: bool
    "If the current version is below the stream's lowest, so the update is forced."
    codename: str
    """eg. ``"Neptune"``."""
    releaseNotesUrl: str
    supervised: bool
    "If AMP runs under its supervisor (``amp3-host``), which an update needs."
    canApply: bool
    "If the panel can update itself."
    canChangeStream: bool
    note: Optional[str]
    """A translation key, eg. ``"updates.error.streamMissing"`` on a stream with no build yet."""
    installationVersion: str
    "The highest version any spire reports."
    # TODO: Check against a live capture; typed from AMP's OpenAPI `UpdateStatusDto` alone (#3-47.8, #3-56.2ao).
    # Every capture has it empty.
    spiresBehind: list[UpdateSpireBehind]
    "The spires on an older version than `installationVersion`, each updated on its own."
    canUpdateSpires: bool
    packageManaged: bool
    "If the machine's package manager updates AMP, so nothing here can."
    # TODO: Check against a live capture; typed from AMP's OpenAPI `UpdateStatusDto` alone (#3-47.8, #3-56.2g).
    # Every capture has it `None`.
    rolledBack: Optional[UpdateRolledBack]
    "The update this machine last took back, `None` when there's none."


class UserCreateRequest(TypedDict):
    """The body of ``POST /api/users``."""

    userName: str
    password: str
    displayName: Optional[str]
    email: Optional[str]
    roleIds: list[str]
    passwordExpires: bool
    requirePasswordChange: bool


class UserResponse(TypedDict):
    """One user from ``GET /api/users``; getting, creating or updating one answers with it too."""

    id: str
    userName: str
    displayName: Optional[str]
    email: Optional[str]
    "`None` when the user has no email address. AMP doesn't check that the value is an email address."
    roleIds: list[str]
    "A deleted role's ID stays here."
    isAdmin: bool
    suspended: bool
    passwordExpires: bool
    requirePasswordChange: bool
    createdAt: Optional[str]
    "`None` when AMP didn't record when the user was made."
    lastLoginAt: Optional[str]


class UserUpdateRequest(TypedDict):
    """The body of ``PUT /api/users/{id}``; a `None` field is left out."""

    displayName: Optional[str]
    email: Optional[str]
    roleIds: Optional[list[str]]
    suspended: Optional[bool]
    passwordExpires: Optional[bool]
    requirePasswordChange: Optional[bool]


class ValidationErrorResponse(TypedDict):
    """A list of refusals, eg. a password the policy rejects (400)."""

    errors: list[str]


class WrappedID(TypedDict):
    """An ID AMP sends inside an object, eg. a running task's `correlationId`."""

    value: str


# The `origin` the audit calls filter on, the names of the `AuditOrigin` numbers.
AuditOriginName = Literal["System", "User", "UserFlow", "Scheduled", "Impersonation"]
# The `min_severity` the audit calls filter on, the names of the `AuditSeverity` numbers.
AuditSeverityName = Literal["Info", "Warning", "Security"]
# A credential's `kind`.
CredentialKind = Literal["SteamCmd", "Smtp", "DiscordWebhook", "ApiKey"]
# Who may use a credential.
CredentialVisibility = Literal["Private", "Public"]
LoginResponse = Union[TokenResponse, PasswordChangeRequiredResponse, PasskeyRequiredResponse]
# A custom port's protocol; "Both" is TCP and UDP.
PortProtocol = Literal["TCP", "UDP", "Both"]
# A query string; a list value repeats its key, so {"shard": ["a", "b"]} is sent as shard=a&shard=b.
# A `bool` is sent as "true" or "false".
QueryParameters = Mapping[str, Union[bool, str, int, Sequence[str]]]
# A settings change: each setting's `fieldName`, from its settings manifest, to the new value as a string.
SettingValues = dict[str, str]
