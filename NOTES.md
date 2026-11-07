# AMP API Notes

Developer context for the AMP 3 (6.0.0b0) branch. AMP 2 support stays on `Refactor`/`developer` (5.x).

## Test panel (vm3)

- `vm3` (`amp3-beta`) runs AMP `3.0.0` from the `preview` channel, installed 2026-11-06 with `getamp3.sh -y`
  (rootless Podman, panel on `:8443`, no HTTPS). Its login is `[VM_AMP3]` in `local.ini`, its licence `[LICENSE] amp3`.
- The licence is the "Beta Preview" grade, 50 Instances, valid to 2027-02-04. The preview build itself runs out
  2026-12-07 (`HealthStatusResponse.preview`).
- HTTPS for passkeys (2026-11-06): Caddy on vm3 serves `https://amp3-beta.anime` with its own local CA
  (`tls internal`) and proxies to `127.0.0.1:8443`. The router's DNS already answers `amp3-beta.Anime` (the LAN search
  domain). AMP has `public-address.publicUrl` set to that address and trusts Caddy through
  `POST /api/https/own-proxy {"address": "127.0.0.1", "apiOnly": false}`. AMP's own `POST /api/https/setup` wants
  Let's Encrypt, which can't reach a LAN VM. A browser needs Caddy's root CA trusted
  (`/var/lib/caddy/.local/share/caddy/pki/authorities/local/root.crt` on vm3) before it will use passkeys there.
- `vm4` (`amp3-beta2`) is a second AMP3 panel for running tests in parallel, built the same way by
  `.scripts/amp3/build_vm.py` (#47.4), with HTTPS at `https://amp3-beta2.anime`. Its login is `[VM_AMP3_B]` in the
  worktree's `local.ini`. The same beta key activated there too (the query showed `usage: 1` first), so one key covers
  several installations. Each panel throttles sign-ins on its own, which is the main reason to have two.
- `vm5` (`amp3-spire`, 192.168.4.235) is not a panel of its own: it joined vm4 as a second spire on 2026-11-07
  (#47.15), for moving and cloning shards between spires. Its VM login is `[VM_AMP3_SPIRE]`; its API is vm4's.
- A panel restarts once licensed (`phase: "starting"`); a setting checked before it reads `ready` can look unapplied.
- Captures live in `_responses/3.0.0/auth/` (gitignored), one file per call: the request (secrets redacted), status,
  kept headers and body.

## Tooling in this worktree

**Capture redaction.** `capture.py` hides values under secret-looking keys (by length) and blanks public IP addresses
under address keys (`host`, `display`, ...). A scrub on 2026-11-06 ~22:55 UTC took four-part version strings for IP
addresses and ran redaction twice, so captures saved before then show `<redacted str len=22>` instead of the original
length, and some `agentVersion` values carry a "version lost to a scrub" marker. The build is `3.0.0.6+f3d1a77cea`.

The worktree carries its own copies, all gitignored, so nothing reaches back into the Refactor checkout:
- `.venv`: the main venv's packages (aiohttp, ruff, pyright, sphinx, pytest, ...) plus `cryptography`.
- `local.ini`: a copy of the main one, with `[VM_AMP3]` and `[VM_AMP3_B]`. The two now differ, so AMP3 logins live here.
- `.scripts/vms.py` and `.scripts/land_check.py`: copies. The `vms.py` copy lists only the AMP3 VMs (vm3, vm4, vm5) and
  keeps only the VM lifecycle (status, start, stop, create, remove, refresh-urls); its AMP2 steps are gone (Kat), so
  the AMP2 pair is still run from the Refactor checkout.
- `.scripts/amp3/`: `capture.py` (one call, or `--poll=FIELD`), the live checks `session_check.py` (`Session`),
  `panel_check.py` (the modules) and `shard_check.py` (shards and templates, on vm3's test shard), `passkey_check.py`
  (a software passkey), `build_vm.py` (a whole AMP3 VM), `join_spire.py` (a new VM joining a panel as a spire) and
  `hook_check.py` (pyright as the end-of-turn hook runs it). `AMP3_VM=vm3|vm4|vm5` picks the panel for all of them.
- `.local_data/amp3/`: their private files (per-VM tokens, setup codes and Caddy root CAs, the passkey test state,
  the vetted `getamp3.sh`) and the upstream report drafts for CubeCoders (`upstream_issues/`).
- `.local_data/plans/todo_index.md`: the AMP3 TODO index.
- There is no OpenAPI document. `/openapi/v1.json` is 401 without a token and 404 with one, so the types come from
  captures plus the web panel's own JS (`main-*.js` and its `chunk-*.js`).

## Library layout (#47.13, #47.14)

Kat's decisions of 2026-11-06 (the plan is `.local_data/plans/amp3_exploration/plan.md`, Decisions 4-7):
- `Session` is the connection: login, renewal, logout, reauth, second factor, the hub token. It is not renamed `Bridge`.
- Each API area is a `...Module` mixin on `Base` (`AccountModule`, `PlatformModule`, then shards, spires, templates
  and the rest), composed into `Panel`, the way 5.x composes `Controller`.
- A module method carries the resource noun and takes IDs (`panel.start_shard(shard_id)`); a `Shard` or `Spire`
  object's method drops both (`shard.start()`) and calls the module method, so no name means two things.
- Calls return TypedDicts. Only `Shard` and `Spire` (and later a task) are classes. There is no `format_data`.
- `Base._request` waits out a 503 whose `code` is `session.storeUnavailable` or `common.error.busUnavailable` (1, 2,
  4, 8, 8 seconds, as the web panel does), and every module call goes through `Session`'s single relogin on a dead
  session.
- No per-call `request_params` (Kat, 2026-11-06): the `ClientSession` handed to `Session` already carries SSL,
  timeouts and proxies for every call.
- The modules: `AccountModule`, `AnalyticsModule` (audit and player analytics), `CredentialModule`, `PlatformModule`,
  `ShardModule` (with `Shard`), `SpireModule` (with `Spire`, in `spires.py` to avoid a circular import), `TaskModule`
  and `TemplateModule`.
- A reply never seen live gets a `# TODO:` above its method naming the index entry, and the method returns `Any`; a
  list only ever seen empty is `list[Any]` (Kat, 2026-11-07: a TODO, not a docstring warning). A `.. warning::` is
  kept for behaviour a user must know, eg. `kill_shard` answering 404 (U12) or a call that changes how the panel is
  reached. Each one is typed properly once a capture shows it.
- Numbers AMP sends for states are the web panel's own enums in `_enums.py` (`ShardState`, `SnapshotKind`,
  `TaskState`, ...). `Base._to_enum` converts them where they're returned and keeps a number it doesn't know as a
  plain `int`, so a new AMP state can't break a read; the fields are typed `Union[Enum, int]`.
- Downloads come back as `bytes` (`_request(raw_bytes=True)`); they need the Bearer header, as AMP takes no other
  credential, and are held whole in memory. Uploads send the web panel's form (`files`) or, for a big file, the
  chunked upload in 8 MiB chunks.
- `set_shard_infra` refuses settings with a field missing before sending, as AMP resets any field a `PATCH /infra`
  leaves out (U13); `update_shard_infra` reads the settings first and sends them back whole with the changes.
- `.scripts/amp3/session_check.py`, `panel_check.py` and `shard_check.py` are the live checks.

## A second spire joining a panel (#47.15)

Seen live on 2026-11-07, vm5 joining vm4; `.scripts/amp3/join_spire.py` runs steps 2 to 4:
1. The panel's message bus must be open to other hosts first, `POST /api/system/bus/expand`. There is no call to
   close it again.
2. The panel issues an enrolment, `POST /api/spires/enrollments {label, expiresInHours, hosts}`, answered with
   `{enrollment, joinBlob}`. `GET /api/spires/enrollments/hosts` lists the addresses it can offer.
3. The new machine is installed without its own first-run setup. Its setup database step takes the blob instead of
   database servers, `POST /api/Auth/setup/database {"servers": [], "blob": ...}` (with `X-Setup-Token`), after which
   its health reads `starting` with `auth.setup.joining.awaitingApproval` and a `fingerprint` to compare.
4. The panel approves, `POST /api/spires/enrollments/{id}/approve`; the enrolment goes `awaitingapproval`, `approved`,
   `redeemed` (with `redeemedSpireId`) within a minute, the new machine reads `ready`, and `GET /api/spires` lists both.

## AMP 3 API shape

- REST under `/api/`, JSON bodies, camelCase keys. AMP 2's `POST /API/Module/Method` is gone.
- An Instance is a **shard** (`/api/shards/{id}/...`) and an ADS/Target is a **spire** (`/api/spires/{id}/...`).
- Path casing is mixed (`/api/Auth/login` and `/api/auth/logout`); both casings answer, we send the panel's own.

## Sessions (#47)

- Login is `POST /api/Auth/login` with `{username, password, rememberMe}`, answered with `{token, expiration}`.
  The token is an HS256 JWT sent as `Authorization: Bearer`. Its claims carry the user ID, name, email and a `sid`.
- A token lasts **8 hours**, or **28 days** with `rememberMe`.
- `POST /api/Auth/renew` swaps the token for a new one in the same session (same `sid`). The old token keeps working
  until the session ends. The web panel renews at 75% of the lifetime, and `Session` does the same.
- A session is one login. `POST /api/auth/logout` ends it: every token it was given gets 401 with
  `WWW-Authenticate: Bearer error="invalid_token"`. Other logins of the same user carry on.
  An admin's `POST /api/users/{id}/logout` ends all of that user's sessions the same way.
- A login can answer 200 without a token:
    - `{passwordChangeRequired: true, reason: "forced"}` for a user made with `requirePasswordChange`.
      `POST /api/Auth/change-expired-password` with `{username, currentPassword, newPassword}` logs in.
      AMP took the old password again as the new one, so there's no reuse check.
    - `{passkeyRequired: true}`, only that key, when the passkey policy is `Required` and the account has a passkey.
      `POST /api/Auth/login/second-factor` takes `{username, password, code, rememberMe}` where `code` is a
      recovery code. There's no TOTP in AMP 3. See "Passkeys and recovery codes" below.
- `POST /api/auth/reauth` with `{password}` answers 204; AMP asks for it ("reproof") before sensitive changes.
- `POST /api/auth/hub-token` gives a 60 second token for the SignalR hub (WebSockets), which is where live events
  come from.
- A wrong password and an unknown user get the same 401 `{message: "Invalid username or password."}`.
  One wrong attempt of each did not lock the admin out; lockout wasn't tested further.

## Passkeys and recovery codes (#47.1)

Tested 2026-11-06 with a software authenticator (`.scripts/amp3/passkey_check.py`) on throwaway users.
- Passkeys need `public-address.publicUrl` set to an HTTPS domain (not an IP). `GET /api/auth/capabilities` judges
  each request by the address it came in on: `Eligible` through `https://amp3-beta.anime`, `OriginMismatch` on
  `http://192.168.4.231:8443`, `NotConfigured` with no public address.
- The rpId is the public address's host name, credentials are discoverable (`allowCredentials: []`) and user
  verification is `required`.
- Register: `POST /api/profile/passkeys/register/begin` gives `{flowId, options}`, then
  `POST /api/profile/passkeys/register/complete {flowId, response, name}` gives `{passkey, session}`.
  **It refuses an answer with no `response.transports` (400), and the web panel never sends one**, so `[]` has to be
  added (upstream report 01).
- Sign in: `POST /api/auth/passkey/begin` then `POST /api/auth/passkey/complete {flowId, response, rememberMe}`
  gives a normal `{token, expiration}`. `POST /api/auth/passkey/reauth {flowId, response}` (204) proves a session like
  a password `reauth`. `POST /api/auth/passkey/abandon {flowId}` (204) ends a flow.
- Policy (`security.passkeyPolicy`): `Optional` and `Encouraged` change nothing at password login. AMP refuses
  `Required` (`settings.security.error.needYourOwnPasskey`) until the admin setting it has a passkey. Under
  `Required`, a password login for an account with a passkey answers `{passkeyRequired: true}`; an account with no
  passkey gets a token with the claim `amp:scope: "enrol"` (the panel's `enrolmentOnly()`, `Session.enrolment_only`).
  Sessions that already exist carry on.
- Recovery codes: `POST /api/profile/recovery-codes` gives `{codes}`, 10 codes of 14 characters, replacing any older
  set; `GET` gives `{remaining, total, generatedAt, low}`. Each code works once at `/api/Auth/login/second-factor`;
  a wrong or used one gets 401 `{message, reason: "auth.login.recoveryCodeRejected"}`.
- AMP refuses assertions with the wrong origin, the wrong rpId or no user verification
  (`passkeys.error.assertionRejected`). A genuine signature whose counter went backwards gets
  `passkeys.error.cloneDetected` **and AMP deletes that passkey**. A forged signature with a low counter is only
  `assertionRejected` and the passkey stays, so AMP checks the signature first and nobody without the key can get a
  passkey deleted. The same answer sent twice works once (then `passkeys.error.ceremonyExpired`, a misleading "took
  too long"), and one flow's answer sent to another is refused.
- Failed sign-ins are throttled per client IP (it honours the trusted proxy's forwarded address): 429
  `auth.login.errorThrottled`, with no `Retry-After` header. It also blocks `passkey/begin`.

## Error shapes

AMP 3 answers errors in six shapes, so `AMPAPIRequestError` reads whichever keys are there:
- `{code, params, message}`, AMP's own: `code` is a dotted translation key, eg. `auth.error.reproofRejected`.
- `{message, reason}`, only for a refused recovery code; `reason` holds the dotted key.
- `{errors: [str]}`, eg. a password the policy refuses.
- `{message}`, only for a refused login.
- ASP.NET ProblemDetails `{type, title, status, errors: {Field: [str]}, traceId}` for a malformed body.
- No body at all: 401 (with `WWW-Authenticate`) and 403 (no permission).

## First-run setup

Done through the API on vm3, with the setup code from `/opt/cubecoders/amp3/data/setup-token.txt` sent as
`X-Setup-Token`: `GET /api/Auth/setup/code`, `POST /api/Auth/setup/database/provision` (AMP sets up its own database,
done in seconds), `POST /api/Auth/setup/admin` (returns the first token), then `POST /api/licence` with
`{key, terms}`. `POST /api/licence/query` checks a key without using it. The privacy, network and HTTPS steps are
browser-only and optional; `GET /api/health/status` read `ready` after the licence.
