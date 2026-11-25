# AMP API Notes

Developer context for the AMP 3 (6.0.0 beta) branch. AMP 2 support stays on `Refactor`/`developer` (5.x).

## Test panel (vm3)

- `vm3` (`amp3-beta`) runs AMP `3.0.2` from the `preview` channel. AMP `3.0.0` was installed 2026-11-06 with
  `getamp3.sh -y` (rootless Podman, panel on `:8443`, no HTTPS), updated to `3.0.1` through the panel on
  2026-11-14 and to `3.0.2` on 2026-11-20 (#3-65). Its login is `[VM_AMP3]` in `local.ini`, its licence `[LICENSE] amp3`.
- Later on 2026-11-20 AMP was wiped and installed fresh on `3.0.2` (#3-65s), on the same VM, address and Caddy. Its
  spire ID, SFTP host key and shard IDs are new: the test shard "API Test MC" is `35313623-...`.
- The licence is the "Beta Preview" grade, 50 Instances, valid to 2027-02-04. The preview build itself runs out
  2026-12-07 (`HealthStatusResponse.preview`).
- HTTPS for passkeys (2026-11-06): Caddy on vm3 serves `https://amp3-beta.anime` with its own local CA
  (`tls internal`) and proxies to `127.0.0.1:8443`. The router's DNS already answers `amp3-beta.Anime` (the LAN search
  domain). AMP has `public-address.publicUrl` set to that address and trusts Caddy through
  `POST /api/https/own-proxy {"address": "127.0.0.1", "apiOnly": false}`. AMP's own `POST /api/https/setup` wants
  Let's Encrypt, which can't reach a LAN VM. A browser needs Caddy's root CA trusted
  (`/var/lib/caddy/.local/share/caddy/pki/authorities/local/root.crt` on vm3) before it will use passkeys there.
- `vm4` (`amp3-beta2`) is a second AMP3 panel for running tests in parallel, built the same way by
  `.scripts/amp3/build_vm.py` (#3-47.4), with HTTPS at `https://amp3-beta2.anime`. Its login is `[VM_AMP3_B]` in the
  worktree's `local.ini`. The same beta key activated there too (the query showed `usage: 1` first), so one key covers
  several installations. Each panel throttles sign-ins on its own, which is the main reason to have two.
- `vm5` (`amp3-spire`, 192.168.4.235) is not a panel of its own: it joined vm4 as a second spire on 2026-11-07
  (#3-47.15), for moving and cloning shards between spires. Its VM login is `[VM_AMP3_SPIRE]`; it serves vm4's panel
  API too, with vm4's admin login.
- A panel restarted once on its first licensing (`phase: "starting"`); a setting checked before it reads `ready` can
  look unapplied. Activating again after `DELETE /api/licence` (vm4, 2026-11-07) stayed `ready` with no restart.
- Captures live in `_responses/<AMP version>/<kind>/` (gitignored), one file per call: the request (secrets redacted), status,
  kept headers and body.

## Tooling in this worktree

**Capture redaction.** `capture.py` hides values under secret-looking keys (by length) and blanks public IP addresses
under address keys (`host`, `display`, ...). It uses the library's `ampapi.redact` (in `session.py`), so the project
script hides the same secrets and addresses as `Session.capture`. The script's copy of the rules was dropped on
2026-11-14, after the script's `redact` and the library's gave identical results over all 2,972 saved captures. A scrub on 2026-11-06 ~22:55 UTC took four-part version strings for IP
addresses and ran redaction twice, so captures saved before then show `<redacted str len=22>` instead of the original
length, and some `agentVersion` values carry a "version lost to a scrub" marker. The build is `3.0.0.6+f3d1a77cea`.

The worktree carries its own copies, all gitignored, so nothing reaches back into the Refactor checkout:
- `.venv`: the main venv's packages (aiohttp, ruff, pyright, sphinx, pytest, ...) plus `cryptography`.
- `local.ini`: a copy of the main one, with `[VM_AMP3]` and `[VM_AMP3_B]`. The two now differ, so AMP3 logins live here.
- `.scripts/vms.py`: a copy. The landing check is the shared `~/.claude/hooks/land_check.py`, set up by
  `[tool.land_check]` in `pyproject.toml`, as in the Refactor checkout. The `vms.py` copy lists only the AMP3 VMs (vm3, vm4, vm5) and
  keeps only the VM lifecycle (status, start, stop, create, remove, refresh-urls); its AMP2 steps are gone (Kat), so
  the AMP2 pair is still run from the Refactor checkout.
- `.scripts/amp3/`: `capture.py` (one call, or `--poll=FIELD`), the live checks `session_check.py` (`Session`),
  `panel_check.py` (the modules), `shard_check.py` (shards and templates, on vm3's test shard), `hub_check.py` (live
  events, on vm3, with a throwaway second shard; can't run while the hubs are set aside, #3-50.1), `move_check.py`
  (clones and moves between vm4's and vm5's spires) and `datastore_check.py` (a move between datastores on vm4),
  `passkey_check.py` (a software passkey), `build_vm.py` (a whole AMP3 VM), `join_spire.py` (a new VM joining a panel
  as a spire) and `hook_check.py` (pyright as the end-of-turn hook runs it). `AMP3_VM=vm3|vm4|vm5` picks the panel for all of them.
    - `spec_diff.py OLD.json NEW.json [--json OUT.json]` compares two of AMP's OpenAPI documents, eg. 3.0.1's and
      3.0.2's in `.local_data/amp3/openapi/` (#3-65n). It talks to no panel.
- `.local_data/amp3/`: their private files (per-VM tokens, setup codes and Caddy root CAs, the passkey test state,
  the vetted `getamp3.sh`) and the upstream report drafts for CubeCoders (`upstream_issues/`).
- `.local_data/plans/todo_index.md`: the AMP3 TODO index.
- There is no OpenAPI document. `/openapi/v1.json` is 401 without a token and 404 with one, so the types come from
  captures plus the web panel's own JS (`main-*.js` and its `chunk-*.js`).

## Library layout (#3-47.13, #3-47.14)

Kat's decisions of 2026-11-06 (the plan is `.local_data/plans/amp3_exploration/plan.md`, Decisions 4-7):
- `Session` is the connection: login, renewal, logout, reauth, second factor, the hub token. It is not renamed `Bridge`.
- Each API area is a `...Module` mixin on `Base` (`AccountModule`, `PlatformModule`, then shards, spires, templates
  and the rest), composed into `Panel`, the way 5.x composes `Controller`.
- A module method carries the resource noun and takes IDs (`panel.start_shard(shard_id)`); a `Shard` or `Spire`
  object's method drops both (`shard.start()`) and calls the module method, so no method name has two meanings.
- Calls return TypedDicts, except where a reply has the same shape as a hub event: then it's the event's object
  (`objects.py`, an `AMPObject` with snake_case attributes and the raw dict on `.data`), eg. `get_shard_state` gives
  a `ShardStatus` (Kat, 2026-11-07). `Shard` and `Spire` are classes too. There is no `format_data`.
    - Settings a user reads and then changes are `AMPSettings` objects (#3-51.11, Kat 2026-11-22): `ShardInfraSettings`,
      `ShardInfraSaveResult` and `Preferences`, with `ShardInfra` holding the infra settings. Each is read from AMP or
      made from typed keyword arguments, and an update sends only the fields set on it.
- `Session._send` waits out a 503 whose `code` is `session.storeUnavailable` or `common.error.busUnavailable` (1, 2,
  4, 8, 8 seconds, as the web panel does), so logins, renewals and the session's own calls get it too, and every
  module call goes through `Session`'s single relogin on a dead session; `Base._request` only hands the call over
  (#3-51.1k).
- No per-call `request_params` (Kat, 2026-11-06): the `ClientSession` handed to `Session` already carries SSL,
  timeouts and proxies for every call.
- The modules: `AccountModule`, `AnalyticsModule` (player analytics), `AuditModule`, `CredentialModule`,
  `EnrollmentModule` (spire enrolments and the message bus, everything for joining a new spire), `HTTPSModule` and
  `LicenceModule` (split out of `PlatformModule`, #3-51.3m), `NetworkModule` (gateways, publications, tunnels,
  firewall), `PlatformModule`, `ShardModule` (with `Shard`), `SpireModule` (with `Spire`, in `spires.py` to avoid a
  circular import), `TaskModule` and `TemplateModule` (#3-50).
- `Panel` holds the calls that make a shard and hand back a `Shard`: `create_shard` and `clone_shard` (#3-51.1g), so
  every module works on its own with a `Session`.
- AMP's own OpenAPI document (#3-56) is served at `/openapi/v1.json` and Scalar at `/scalar/v1` when the panel runs
  `ASPNETCORE_ENVIRONMENT=Development`; the same document ships beside the binary as `webapi.json`. A type taken from
  it alone carries a `# TODO:` until a capture confirms it (Kat, 2026-11-12). Its `required` lists only C# `required`
  members, so it isn't evidence that AMP leaves a field out.
- There is no kill and no update abort in AMP 3.0.0 and 3.0.1 (#3-56.4c, #3-64): neither route is in their OpenAPI,
  `stop_shard` kills a game that outlasts its template's `exitTimeout`, and a schedule's `power.kill` step kills at
  once. The Tasks cancel (`cancel_task`) answers 202 for an update and is ignored (upstream U33); a failed task leaves
  the running list after about 30 minutes. AMP 3.0.2 adds both routes, as `kill_shard` and `abort_shard_update` (#3-65a).
- Writes that replace a whole record (#3-56.4b, #3-56.7): a datastore POST carrying an `id` resets every field it
  isn't sent (`softLimitMb` 0, `tags` [], `enabled` true), and an unknown `id` creates one, so
  `update_spire_datastore` reads first and refuses an ID the spire doesn't list. AMP adds the storage medium it detects
  (eg. `"HDD"`) to a datastore's tags. Creating a gateway deletes the shard's publications (upstream U31).
- Chunked uploads (#3-51.9, checked live 2026-11-11, upstream U30): `upload-start` hands back an unfinished upload's
  session for any start on the same path (vm3, whatever the size), AMP keeps it 24 hours, and no call cancels it, so
  `upload_shard_file` refuses to carry on an upload AMP holds part of unless `resume=True`. On a remote spire
  (`via: "agent"`) the file at the path is resized as the upload starts, and a failed upload leaves it padded with
  zeros; on the panel's own spire it is untouched until the commit. A move onto an existing file is refused. AMP 3.0.1
  still does all of this (#3-64), and codes two refusals: a short commit is 400 `files.error.uploadIncomplete`
  (`params` `{expected, received}`), and a chunk to a finished upload is 404 `files.error.uploadSessionGone`.
- A failed call that leaves something behind says so: `AMPAPIUploadError` carries the upload's session and bytes
  held, and an `AMPAPIRequestError` mid-upload or in `clone_shard`'s read-back gains a note (`add_note`) naming the
  session or the copy's ID.
- A TypedDict holds only what AMP sends (Kat, 2026-11-11, #3-51.9g): no enums in `_types.py`, which imports nothing
  from `_enums`, so `typing.get_type_hints` resolves every type (#3-51.4m). A closed set is the plain `str` / `int`
  with a field doc naming its enum, eg. a gateway's `status.state` is ``"Active"``, and `GatewayState(state)` gives the
  member (a `StrEnum` compares equal to its string). Request bodies take the enum's value; the method parameters keep
  the enum types. Converting into enums is the `AMPObject`s' job, from their hints.
    - An `AMPSettings` field typed with an enum takes the member or a plain `str`, and the update call sends the
      member's value (`container_mode`, `amp_experience`, `time_format`).
- A `bool` in a query is sent as `"true"` / `"false"` by `Session._send`, as yarl (aiohttp's query builder) refuses a
  `bool` (#3-51.4j). Calls send their flags every time, eg. `demo=false`, where they used to leave a `False` one out.
- `Session` holds `accept_invite` and `preview_invite`, as the invitee has no account yet (#3-50.7). `accept_invite`
  previews the invite for its username, sends the session's own password, and keeps the token, so the session is
  logged in as the new account (live on vm4, 2026-11-08). A session it already held is logged out once the account
  exists, best effort (#3-51.5).
- **A call goes where its target is, not where its route prefix is** (#3-50, 2026-11-08; plan
  `.local_data/plans/module_layout/plan.md`). `ShardModule` / `SpireModule` hold only calls that take that shard's or
  spire's ID. The calls over all of the panel's shards or spires (`get_shards`, `get_shard`, `create_shard`,
  `get_shards_awaiting_action`, `get_all_shard_endpoints`, `get_spires`, `get_spire`, `get_spire_roster`) are
  `Panel`'s own. The #3-47.13 layout had sorted by prefix, which is how they ended up in the per-item modules.
- The `Panel` keeps one `Shard` / `Spire` per ID (`_shards`, `_spires`, Kat's #3-50a): a lookup or listing hands back
  the kept object with `data` and `display_name` brought up to date. A shard belongs to a spire, so `Spire` has
  `get_shards` (the panel's list filtered by `spireId`, as AMP has no per-spire route) and `create_shard`.
  `create_shard` and `clone_shard` return a `Shard`.
- Keeping the objects current (#3-51.6): `Shard._update_data` / `Spire._update_data` is the one place `data` and
  `display_name` change, used by the panel's lookups and by the six `Shard` calls AMP answers with the shard
  (`set_details`, `delete`, `restore`, `suspend`, `unsuspend`, `acknowledge_disk_warning`); a subclass overrides it to
  refresh what it derives. `refresh()` reads either object again, and `get_spire_roster` refreshes the kept spires. The
  panel's `purge_shard` and `delete_spire` override the module calls to drop what's gone from its registry, a deleted
  spire's shards too.
- The rest of `create_shard`'s reply rides on the `Shard` it returns (#3-50.11, Kat 2026-11-08): read-only
  `infra_settings`, `app_config`, `port_assignments`, `port_outcomes` and `over_licence_limit`, all `None` on a shard
  `create_shard` didn't make. `port_outcomes` and `over_licence_limit` exist only in that reply; the other three are a
  snapshot from creation, kept when the panel hands the object out again (`get_infra` / `get_settings` / `get_ports`
  give current values). Live on vm4, `infra_settings` equals `get_infra()["settings"]` straight after creation.
  `infra_settings` is a `ShardInfraSettings` built from the reply since #3-66. `ShardCreatedResponse.infraSettings`
  is the raw `ShardInfraSettingsResponse` (Kat's #3-66d), as `_types.py` imports nothing from `objects.py`.
- `Shard` and `Spire` are equal and hash the same by ID, and sort by `display_name` (#3-50.10, Kat 2026-11-08). The
  registry stays a dict, as a set can't hand back the object it holds without a scan. discord.py pairs a dict
  registry with equal-by-ID objects the same way. The check is `isinstance(other, Shard)`, not `self.__class__`, so the panel's `shard_class` subclass and a
  plain `Shard` agree both ways.
- A reply never seen live gets a `# TODO:` above its method naming the index entry, and the method returns `Any`; a
  list only ever seen empty is `list[Any]` (Kat, 2026-11-07: a TODO, not a docstring warning). A `.. warning::` is
  kept for behaviour a user must know, eg. a file ACL deny that can't be undone (U24a) or a call that changes how the
  panel is reached. Each one is typed properly once a capture shows it.
- Numbers AMP sends for states are the web panel's own enums in `_enums.py` (`ShardState`, `SnapshotKind`,
  `TaskState`, ...). `AMPObject._convert` converts them where they're returned and keeps a number it doesn't know as
  a plain `int`, so a new AMP state can't break a read; the fields are typed `Union[Enum, int]`.
- A bodiless POST sends what the web panel sends (#3-51.2q): some calls send `{}` (the renew, logout and hub token,
  task cancels, recovery codes, updates, a shard's suspend, unsuspend, disk warning, snapshot restore and schedule
  run), the rest no body at all.
- Downloads come back as `bytes` (`_request(raw_bytes=True)`); they need the Bearer header, as AMP takes no other
  credential, and are held whole in memory. Uploads send the web panel's form (`files`) or, for a big file, the
  chunked upload in 8 MiB chunks.
- `PATCH /infra` (#3-64c, Kat 2026-11-19): AMP 3.0.1 changes only the top-level fields it is sent, where 3.0.0 reset
  every field the body left out (U13, fixed). It still ignores a `settings` wrapper, fields and all.
    - `update_shard_infra` sends only the changes in one PATCH. Until 3.0.1 it read the settings first, sent them back
      whole, and held a lock per shard so two calls in one program didn't undo each other; the read and the lock are
      gone.
    - `set_shard_infra` and `Shard.set_infra` were removed (Kat, 2026-11-19, while 6.0.0 is a beta): on 3.0.1 they sent
      the same PATCH as `update_shard_infra`.
    - `AMPSettings` objects since #3-51.11 (Kat, 2026-11-22, a breaking change while 6.0.0 is a beta), replacing
      #3-66's keyword arguments and object sent whole: `update_shard_infra(shard_id, settings)`,
      `Shard.update_infra(settings)` and `update_preferences(preferences)`.
        - `AMPSettings` (`objects.py`) is under `typing.dataclass_transform`, so pyright and Pylance build a typed
          keyword constructor from the fields: one field list, where #3-66 kept `ShardInfraChanges` /
          `PreferencesChanges` beside the objects by hand. Both TypedDicts are gone.
        - Each field's class default is `UNSET`, for the type checker only; `__init_subclass__` removes it, so a field
          never set raises `AttributeError` (Kat: safer, should a value ever take a `None` setting).
        - The library builds the objects from AMP's replies through `from_data`, with no field recorded. The other
          `AMPObject` classes keep `Cls(data=...)`.
        - The object records each field set after it was made; the update sends only those, so a setting another
          program changed since the read stays. The recorded fields are cleared once AMP accepts, and kept on a refusal.
        - Nothing recorded, or only `None` or AMP's own fields, is a `ValueError` before sending (#3-66b).
        - AMP's `shardId`, `tenantId`, `updatedAt`, `updatedByUserId` and a save's `clampRefused` are never sent.
        - `container_image_override` set to `None` is sent as `""`, as AMP reads `null` as "keep". Any other `None` is
          left out, as AMP's own PATCH contract says for both routes (OpenAPI `ShardInfraPatch` and
          `PatchPreferencesRequest`). `Base._key_name` turns each name back into AMP's camelCase.
        - `__getattr__` and `__setattr__` sit under `if not TYPE_CHECKING:`, as either one makes pyright accept any
          attribute name, a misspelt one too.
        - Live on vm3 (3.0.2), `scripts/live_3_51_11.py`: read-edit-send and keyword objects change only their fields,
          a list empties, `None` brings back the template's image, preferences through a throwaway user.
    - `ShardInfraSettings` (the TypedDict), `ShardInfraResponse`, `ShardInfraUpdateResponse`, `PreferencesResponse`,
      `ShardInfraUpdateRequest` and `PreferencesUpdateRequest` went in #3-66.
    - Checked live on vm3 (3.0.1) 2026-11-19: a `{}` PATCH answers 200 on both routes and changes nothing, but the infra
      one still stamps `updatedAt` and `updatedByUserId`. Kat chose a `ValueError` before sending for an update with
      no arguments (#3-66b), on both routes.
    - Also live on vm3:
        - Each of the 25 infra fields changes alone.
        - `containerImageOverride` sent as `""` reads back `None`.
        - `extraEnvironment` and the country lists replace the stored ones.
        - A `null` field keeps its value on both routes, so a preference can't go back to `None`.
        - A preference list replaces the stored list, and `add_favourite` puts the new slug first.
    - `Preferences.default()` (#3-67) sends the value the web panel shows for each `null` preference, read from the
      panel's 3.0.2 bundle (`.local_data/plans/preferences_default/panel_defaults.md`); live on vm3 7/7.
        - AMP stores `""` for `theme` and `locale`, and doesn't check a theme's name or a pinned shard's ID.
        - The panel reads an empty theme as none chosen, so `default()` sends `theme=""`.
        - The panel reads an empty locale as English, not the browser's language, so `default()` leaves `locale` out
          (Kat's #3-67e).
        - The panel never reads `notifyOnStateChange` or `notifyOnUpdateAvailable`, so `default()` leaves them out
          (#3-67d).
    - What each infra field does on a running game is in `.local_data/plans/settings_objects/findings/infra_fields.md`
      (#3-66 Phase 2). On vm3 a Podman shard's memory and CPU limits aren't enforced, as rootless Podman falls back to
      cgroupfs without a systemd user session for `amp`; that's the host's setup, so the docs say only what AMP sets.
- Writes that replace a whole record, and how the library keeps what the caller didn't name (#3-51.7, checked live on
  vm4 2026-11-09):
    - A schedule PUT replaces everything it's sent (a `timeout` of `null` goes back to 30 minutes) and ignores
      `retryPolicy` / `misfirePolicy`; `update_shard_schedule` reads the schedule first, so `None` keeps.
    - `PUT /api/profile` clears the display name whenever it's left out, so `update_profile` reads it first; `""`
      clears it. The admin's `PUT /api/users/{id}` keeps it for `null`, and `""` clears it.
    - `set_settings` returns AMP's `notices`. AMP's own doc comment (`HttpsSetupService.FollowExposureAsync`, read
      from the webapi binary, UTF-16) says a refused removal of the ports 80/443 front comes back as one; every save
      seen so far answered 204.
- `.scripts/amp3/session_check.py`, `panel_check.py`, `shard_check.py`, `move_check.py`, `datastore_check.py` and
  `hub_check.py` are the live checks; each removes what it makes. `hub_check.py` waits for the hubs (#3-50.1), and
  no check covers the invite calls yet: #3-50.7 was checked live with a one-off script.

## AMP 3.0.2 "Neptune" (#3-65)

The findings are `.local_data/plans/amp302/findings/spec_302_diff.md` and `recheck_302.md`. The library follows the
latest AMP, so a field AMP 3.0.2 added is typed as always sent, and a 3.0.1 panel's reply lacks it.
- Breaking while 6.0.0 is a beta (Kat's #3-65o, follow AMP's names), told here as this branch has no
  `docs/upgrading.rst`:
    - `Snapshot.failure_reason` (a `str`) is now `Snapshot.failure`, and `ScheduleExecution.error_message` is now
      `ScheduleExecution.error`. Each is AMP's `ApiError` (`code`, `params`, `message`) as a `CodedErrorResponse`, or
      `None`.
    - `ScheduleStepOutcome.detail` and `ScheduleStatus.lastError` are a `CodedErrorResponse` too, where they were a string.
    - `SpireImportReadyItem.unavailableReason` is now `unavailable`, and its `liveness` a list of `CodedErrorResponse`.
      `SpireImportBlockedItem.detail` is a `CodedErrorResponse`. `SpireImportLiveness` is gone, as AMP 3.0.2 dropped
      `LivenessEvidence` for `ApiError`.
    - `TemplateMetadata.arch` and `HTTPSCheck.detail` are gone, as AMP 3.0.2 dropped both.
- `kill_shard` / `Shard.kill` and `abort_shard_update` / `Shard.abort_update` are new (U12, fixed in 3.0.2). Both answer
  202 when there's nothing to kill or abort, and 404 `shards.error.notFound` for an unknown shard.
- `allow_lan_access` (AMP's `allowLanAccess`) is in `ShardInfraSettings` and `ShardInfraSettingsResponse`
  (`ShardInfraChanges` too, until #3-51.11 removed it).
    - Before it, `update_shard_infra(allow_lan_access=...)` raised the library's `TypeError`, and an object read on
      3.0.2 was sent without it, so AMP kept the stored value.
    - Off by default. Off, a Podman container on vm3 reached 1.1.1.1:443 and the router's DNS but not dotHack's SSH
      port. On, dotHack answered after a stop and a start; a restart reuses the container and kept it closed.
- The analytics `steam` and `minecraft` keys (`AnalyticsProfilesResponse`, `AnalyticsConnectedResponse`) stay, with a
  `# TODO:`. AMP 3.0.2's OpenAPI dropped them, but `GET /api/analytics/profiles` still sends both.
- Seen on 3.0.2 and still open: U14 (an update's stop sends no quiesce), U15 (a never-updated shard starts and fails),
  U22a and U22b (moves), U24a and U24b (file ACL), U26b and U26e (gateway states), U31 (a gateway deletes the
  publications), U34 (the panel update's task reads 404). Their comments name 3.0.2 now.
- Fixed in 3.0.2: a start waits for its gateway's route (#3-65f, `pre_start` with `agent.msg.gatewayConnecting`), moves
  and clones keep config files between spires (U22), and U32 (moving a running shard). U25 is fixed for a clone on one
  spire only; a clone to another spire still ignores its cancel, and the docs say so.
- U37, new on 3.0.2 (#3-65p, draft in `.local_data/amp3/upstream_issues/`): on a panel updated from 3.0.1 that holds
  schedule runs 3.0.1 stored, every schedule history read is 500 and a purge answers 202 but leaves the record deleted.
  vm3 had it until its fresh install; vm4, also updated from 3.0.1, doesn't. `get_shard_schedule_history`
  and the purge calls carry a warning.
- U39 (not sent): the `amp3base:debian` and `java-lts` builds published on the morning of 2026-11-20 had no `nft`, so
  AMP refused every container shard with `allowLanAccess` off (`shards.error.containerLanFilterFailed`). AMP runs the
  filter in a helper container from the shard's image. CubeCoders rebuilt both with `nft` that evening. A spire keeps
  the image it pulled, so one holding a broken build needs a `podman pull` as AMP's `amp` user. `allow_lan_access`'s
  docs say what the refusal is.

## Code analysis groups E, F and H, and settings objects (#3-51.10, #3-51.11)

- Breaking while 6.0.0 is a beta, told here as this branch has no `docs/upgrading.rst`:
    - An `AMPObject` is read by attribute only (Kat's #3-51.1i): `state["status"]` is now `state.status`, and `data`
      holds the dict as AMP sent it. A TypedDict reply is still read by key.
    - `create_gateway` and `create_publication` take every parameter by keyword (#3-51.3d), so the shard and front
      spire IDs can't be swapped.
    - The infra and preference updates take an `AMPSettings` object only (#3-51.11), see "`PATCH /infra`" above.
    - The audit calls' `origin`, `min_severity` and `sort` take `AuditOrigin`, `AuditSeverity` and `AuditSort`
      members (Kat: an Enum where a key's range of values won't change). The `AuditOriginName` and
      `AuditSeverityName` Literals are gone. AMP 3.0.2 reads an origin or severity as its number or its name, in any
      case, and answers 400 for a number it doesn't know.
- AMP 3.0.2 answers a cancel with no move running 409 `{code: "shards.error.moveNotRunning", message}`, where 3.0.0
  sent `{error: "shards.migration.notRunning"}`. No `{error}` body is in the 3.0.2 captures, so which calls still send
  that shape is unchecked.

## Live events (#3-47.2)

The design is Kat's (`.local_data/plans/prompt.md`, reviewed in `.local_data/plans/amp3_exploration/hub_design_review.md`).
What the endpoints do, checked live on vm3 and vm4:
- `POST /api/auth/hub-token` gives a 60 second token per socket, checked only when a socket opens.
- Three WebSocket hubs: `/hubs/shard` (one subscribe message per shard; one socket carries any number of shards),
  `/hubs/spire` (the network, plus one per spire) and `/hubs/tasks` (no subscribe). There are 14 event types.
- **State reaches every shard socket for every shard**, even one subscribed to nothing, and unsubscribing doesn't stop
  it. **A console line names no shard**, so a socket with several shards mixes their consoles.

**Set aside since #3-50.1 (Kat, 2026-11-08).** `Panel`, `Shard` and `Spire` no longer build on the hub classes,
`auto_state` is commented out, nothing imports `hubs.py` (pyright excludes it) and `hub_check.py` can't run. What
follows is how the hub layer worked before that, kept for when it comes back.

How the library uses that (`hubs.py`):
- `Hub` holds the `Session` and does the socket work; `Panel`, `Spire` and `Shard` build on `PanelHub`, `SpireHub` and
  `ShardHub`. Listeners are class-level methods (`@ShardHub.listener(name="console")`, called `(self, data)`) or
  instance-level functions (`obj.listen(name)`, `add_listener`, `remove_listener`, called `(obj, data)`).
- The `Panel` holds three shared sockets, one per hub. A `ShardHub` with a `console` listener also opens its own shard
  socket, so its console lines are its own; above the shard level console lines arrive unattributed.
- `add_subscribers` / `remove_subscribers` take shards, spires and IDs mixed. `None` means every one, following new
  ones; an empty list raises `ValueError`; removing a few while "every one" is on leaves a plain list of the rest.
- Every state frame goes through one `_apply_state`, which updates an object only if its `revision` is newer, so copies
  from other sockets never apply twice. Listener delivery keeps its own seen-set.
- `auto_state` (an init parameter and a read-only property) keeps an object's `state` current. Every `get_*` call and
  every `Shard` / `Spire` made by hand takes the panel's value, and the panel's defaults to `False`. A setter waits for
  Kat.
- A `shard_class` with class-level listeners turns every shard `get_shards()` returns into a listener, with its own
  console socket if it listens to `console`. `hub_check.py` polls through a plain `Panel` for that reason.

## A second spire joining a panel (#3-47.15)

Seen live on 2026-11-07, vm5 joining vm4; `.scripts/amp3/join_spire.py` runs steps 2 to 4:
1. The panel's message bus must be open to other hosts first, `POST /api/system/bus/expand`. There is no call to
   close it again.
2. The panel issues an enrolment, `POST /api/spires/enrollments {label, expiresInHours, hosts}`, answered with
   `{enrollment, joinBlob}`. `GET /api/spires/enrollments/hosts` lists the addresses it can offer.
3. The new machine is installed without its own first-run setup. Its setup database step takes the blob instead of
   database servers, `POST /api/auth/setup/database {"servers": [], "blob": ...}` (with `X-Setup-Token`), after which
   its health reads `starting` with `auth.setup.joining.awaitingApproval` and a `fingerprint` to compare.
4. The panel approves, `POST /api/spires/enrollments/{id}/approve`; the enrolment goes `awaitingapproval`, `approved`,
   `redeemed` (with `redeemedSpireId`) within a minute, the new machine reads `ready`, and `GET /api/spires` lists both.

Once joined, every spire serves the whole panel API: vm5 answers `http://amp3-spire.anime:8443` with vm4's accounts,
spires, shards and tasks. Only a spire's `isLocal` differs, as it means "the machine that answered this call".

What the two spires showed (2026-11-07, `findings/vm4_vm5_multi_spire.md`):
- A shard is made on either spire from vm4 (`targetSpireId`); the first one on a new spire waits about 2 minutes while
  that spire prepares its container image.
- A clone to the other spire finishes in seconds and is not installed yet (`installedAt: null`).
- A move between spires (`POST /migration/spire`) switches the shard over at once and leaves the source copy as an
  orphan folder on the old spire until its datastore's orphan purge runs; dismissing the move doesn't remove it. Ports
  are re-allocated on the target. `/migration/targets` lists other datastores on the same spire, not other spires.
- A publication through the shard's own spire needs no public host; a gateway or a publication through another spire
  needs that spire's `spire.publicHost` set, which hasn't been tried yet.

## Removing a spire, denying a join, importing servers (#3-53)

Seen live on 2026-11-09, vm5 against vm4 (`.local_data/plans/spire_lifecycle/findings/vm4_vm5_spire_lifecycle.md`):
- `DELETE /api/spires/{id}` answers 204. A spire that still holds shards is refused without `force` (409
  `spire.error.hasShards`, `params.count` a string). The removed machine's health reads `waiting`. vm5 was then wiped and
  reinstalled before it joined again, and it came back as a **new spire with a new ID** (`9464ff1f-...`, was
  `17d1d1e7-...`), taking its enrolment's label as its name.
- `POST /api/spires/enrollments/{id}/deny` answers 204. The enrolment reads `denied`, and the machine's health reads
  `auth.setup.joining.refused` within seconds; it takes a new join file without a reinstall.
- `POST /api/updates/spires/{id}` answers 400 `updates.error.spireCurrent` for a spire on the panel's version. No older
  AMP 3 release exists to install (the installer has no version option, the apt preview suite holds only 3.0.0), so
  the success reply is unseen.
- A panel update from 3.0.0 to 3.0.1 was watched on vm3 on 2026-11-14, polled every 2 seconds
  (`_responses/3.0.0/platform_writes/update_301_vm3/`):
    - `POST /api/updates/apply` answers 200 `{"taskId": ...}`, the same reply vm4's update gave.
    - The panel answers nothing for about 8 seconds. Health reads `starting` on the new version 13 seconds after the
      call, and `ready` 23 seconds after the call.
    - The `taskId` can't be followed: `GET /api/tasks/{tenant_id}/{task_id}` is a 404 with no AMP code before and
      after the restart, and the running tasks list is empty minutes later (upstream U34). Watch health and the update status instead, as the
      web panel does.
- Import: the automatic scan looks only in other panels' fixed folders, not LinuxGSM's. Any other folder must be in
  `AllowedImportRoots` in the spire's `/etc/amp3/sysagent.conf`, and the agent runs with `ProtectHome=yes`, so it can't
  see `/home` at all. The import itself answers 202 `{taskId}` and works in a `ServerImport` running task.
- Suspected AMP bugs, not drafted upstream yet: `ProtectHome=yes` hiding `/home`; a copy through the agent failing
  with EEXIST when the template pre-makes a folder (and leaving an orphan); a successful import's task never finishing
  (100%, not terminal, dismiss refused with 409 for minutes); the same folder importing twice unmarked.

## The last untyped replies, live (#3-54)

Seen on 2026-11-09 on vm3, vm4 and vm5 (`.local_data/plans/live_todos/findings/live_todos.md`). AMP's webapi binary
(`/opt/cubecoders/amp3/seed/3.0.0/webapi/webapi` on a panel) carries its own XML doc comments for every controller,
body, enum and reply, which settled several of these before any call.
- A shard keeps names, countries, addresses and profiles only with `userSpecificData` on. "Kat MC World" had it off,
  so Kat's player had a key and sessions only, and no public IP was stored. With it turned on and Kat online, the
  connected-player reply, her Minecraft profile (`skinHash`, 64 hex digits) and her skin (a PNG) were all seen; the
  `connected` route takes the player's `id`, not their name (404).
- The analytics avatar and skin routes take a Steam avatar hash and a Mojang texture hash, and `connected` is
  `connected/{shard_id}?user=<id>`; the library had all three keyed by the player's key until #3-54.
- Every analytics range search (CIDR, prefix, wildcard) answers 500 on AMP 3.0.0 (a NATS consumer error in its
  address service), and still on 3.0.1 (`common.error.unexpected`, vm3, 2026-11-19); a whole address works. Erasing
  a player left them in the sessions summary for at least 11 minutes.
- A platform warning is raised by conditions such as a spire whose IPv6 goes nowhere (`ipv6BlackHoled`), not by an
  offline spire. A warning that needs action can't be acknowledged (400 `platform.error.warningNotDismissable`).
- `uptimeSeconds` in `GET /api/support/diagnostics` isn't the panel's uptime (U11). AMP 3.0.0 sent 0. On 3.0.1
  (vm3, 2026-11-19) it counted up with the clock, but read 5 about 5 seconds after the first diagnostics request in a
  long while, on a panel whose services had run for 4.7 days.
- A shard waiting on a user (status 110): a `hytale` shard's update waits for a device sign-in, and the sign-in code
  shows in the running task's `message`. `stop` aborts the update; `update/abort` and `kill` still answer 404 (U12).
- `ShardPortOutcome.reason` is always 0 from `POST /api/shards`, which silently drops unknown keys such as
  `preferredPorts`; AMP's docs name 0 to 4.
- Only `minecraft-java` claims sleep among 248 templates, and AMP refused it on the VMs for starting slower than its
  25 second limit, so `wake`'s success is unseen. On 3.0.1 (#3-64) a running shard's state has `sleep: null` where 3.0.0
  gave the reason, and a sleep with sleep mode on answers 202 while the console says the server can't sleep (U18b).

## AMP 3 API shape

- REST under `/api/`, JSON bodies, camelCase keys. AMP 2's `POST /API/Module/Method` is gone.
- An Instance is a **shard** (`/api/shards/{id}/...`) and an ADS/Target is a **spire** (`/api/spires/{id}/...`).
- AMP's routes ignore case; the library sends every route in lower case (checked live 2026-11-07).
- AMP 3.0.1 removed `POST /api/shards/{id}/files/zip`, which now answers 404. `download_shard_files` uses the 3.0.1
  zip ticket instead: `POST .../files/zip-ticket` with the paths, then `GET .../files/zip?ticket=...` at once (#3-60a).

## Sessions (#3-47)

- Login is `POST /api/auth/login` with `{username, password, rememberMe}`, answered with `{token, expiration}`.
  The token is an HS256 JWT sent as `Authorization: Bearer`. Its claims carry the user ID, name, email and a `sid`.
- A token lasts **8 hours**, or **28 days** with `rememberMe`.
- `POST /api/auth/renew` swaps the token for a new one in the same session (same `sid`). The old token keeps working
  until the session ends. The web panel renews at 75% of the lifetime, and `Session` does the same.
- A session is one login. `POST /api/auth/logout` ends it: every token it was given gets 401 with
  `WWW-Authenticate: Bearer error="invalid_token"`. Other logins of the same user carry on.
  An admin's `POST /api/users/{id}/logout` ends all of that user's sessions the same way.
- A login can answer 200 without a token:
    - `{passwordChangeRequired: true, reason: "forced"}` for a user made with `requirePasswordChange`.
      `POST /api/auth/change-expired-password` with `{username, currentPassword, newPassword}` logs in.
      AMP took the old password again as the new one, so there's no reuse check.
    - `{passkeyRequired: true}`, only that key, when the passkey policy is `Required` and the account has a passkey.
      `POST /api/auth/login/second-factor` takes `{username, password, code, rememberMe}` where `code` is a
      recovery code. There's no TOTP in AMP 3. See "Passkeys and recovery codes" below.
- `POST /api/auth/reauth` with `{password}` answers 204; AMP asks for it ("reproof") before sensitive changes.
- `POST /api/auth/hub-token` gives a 60 second token for the SignalR hub (WebSockets), which is where live events
  come from.
- A wrong password and an unknown user get the same 401 `{code: "auth.login.errorInvalid", params: null, message:
  "Invalid username or password."}` on AMP 3.0.1; AMP 3.0.0 sent the `message` alone. One wrong attempt of each did
  not lock the admin out; lockout wasn't tested further.

How `Session` handles them (#3-51.5, 2026-11-08):
- Calls queued on a login that fails raise that login's error rather than each sending it again, as a busy program
  with a wrong password would otherwise trip AMP's per-IP sign-in throttle. A later, separate call tries again.
- A renew refused with anything but 401 (eg. a 503) is a warning: the token works until it runs out, so we keep it and
  try the renew again a minute later. A 401 renew means the session ended, and we log in again without an ERROR line.
- A new login logs out the token it replaces (a `login()` on a logged-in session, `accept_invite` on one), best effort.
- A reply body that isn't JSON is kept as text: an HTML 502 from a proxy is an `AMPAPIRequestError` with the page as
  its `data`, and a 2xx with a text body hands the text back.
- A login finished with `second_factor` can't be made again on its own; once AMP ends it, the next call raises
  `AMPAPIPasskeyRequiredError` and needs a new recovery code.

## Passkeys and recovery codes (#3-47.1)

Tested 2026-11-06 with a software authenticator (`.scripts/amp3/passkey_check.py`) on throwaway users.
- Passkeys need `public-address.publicUrl` set to an HTTPS domain (not an IP). `GET /api/auth/capabilities` judges
  each request by the address it came in on: `Eligible` through `https://amp3-beta.anime`, `OriginMismatch` on
  `http://192.168.4.231:8443`, `NotConfigured` with no public address.
- The rpId is the public address's host name, credentials are discoverable (`allowCredentials: []`) and user
  verification is `required`.
- Register: `POST /api/profile/passkeys/register/begin` gives `{flowId, options}`, then
  `POST /api/profile/passkeys/register/complete {flowId, response, name}` gives `{passkey, session}`.
  AMP 3.0.0 answered 400 to an answer with no `response.transports`, and the web panel never sends one, so `[]` had to
  be added (upstream report 01). AMP 3.0.1 accepts the answer with or without the key (vm3, 2026-11-19, a new key for
  each; AMP refuses the same key twice with 400 `passkeys.error.registrationRejected`). Captures beside each other in
  `_responses/3.0.0/auth/` and `_responses/3.0.1/auth/`.
- Sign in: `POST /api/auth/passkey/begin` then `POST /api/auth/passkey/complete {flowId, response, rememberMe}`
  gives a normal `{token, expiration}`. `POST /api/auth/passkey/reauth {flowId, response}` (204) proves a session like
  a password `reauth`. `POST /api/auth/passkey/abandon {flowId}` (204) ends a flow.
- Policy (`security.passkeyPolicy`): `Optional` and `Encouraged` change nothing at password login. AMP refuses
  `Required` (`settings.security.error.needYourOwnPasskey`) until the admin setting it has a passkey. Under
  `Required`, a password login for an account with a passkey answers `{passkeyRequired: true}`; an account with no
  passkey gets a token with the claim `amp:scope: "enrol"` (the panel's `enrolmentOnly()`, `Session.enrolment_only`).
  Sessions that already exist carry on.
- Recovery codes: `POST /api/profile/recovery-codes` gives `{codes}`, 10 codes of 14 characters, replacing any older
  set; `GET` gives `{remaining, total, generatedAt, low}`. Each code works once at `/api/auth/login/second-factor`;
  a wrong or used one gets 401 `{message, reason: "auth.login.recoveryCodeRejected"}`.
- AMP refuses assertions with the wrong origin, the wrong rpId or no user verification
  (`passkeys.error.assertionRejected`). A genuine signature whose counter went backwards gets
  `passkeys.error.cloneDetected` **and AMP deletes that passkey**. A forged signature with a low counter is only
  `assertionRejected` and the passkey stays, so AMP checks the signature first and nobody without the key can get a
  passkey deleted. The same answer sent twice works once (then `passkeys.error.ceremonyExpired`, a misleading "took
  too long"), and an answer sent to a different sign-in flow from the flow that asked for it is refused.
- Failed sign-ins are throttled per client IP (it honours the trusted proxy's forwarded address): 429
  `auth.login.errorThrottled`, with no `Retry-After` header. It also blocks `passkey/begin`.

## Error shapes

AMP 3 answers errors in six shapes, so `AMPAPIRequestError` reads whichever keys are there:
- `{code, params, message}`, AMP's own: `code` is a dotted translation key, eg. `auth.error.reproofRejected`.
- `{message, reason}`, only for a refused recovery code; `reason` holds the dotted key.
- `{errors: [str]}`, eg. a password the policy refuses at setup. AMP 3.0.0 used it for `POST /api/users` too, where
  AMP 3.0.1 answers 400 `users.error.passwordTooShort` in AMP's own shape (#3-64; setup wasn't rechecked).
- `{message}`, only for a refused login on AMP 3.0.0. AMP 3.0.1 answers it in AMP's own shape,
  `auth.login.errorInvalid`.
- ASP.NET ProblemDetails `{type, title, status, errors: {Field: [str]}, traceId}` for a malformed body.
- No body at all: 401 (with `WWW-Authenticate`) and 403 (no permission).

An AMP 2 panel answers each AMP 3 route with **200** and `{Title: "Invalid Module", Message: "No such module loaded:
'auth'"}` (checked on vm1, 2026-11-23), as its API is `/API/<Module>/<Method>`. Without a check the login read that
as a success; `Session._send` raises `AMPAPIPanelVersionError` on it instead (#3-69), for every request.

## Releases: the AMP 2 and AMP 3 lines (Kat, 2026-11-23)

Both lines publish as `cc-ampapi` on PyPI: 5.x for AMP 2 (`main`, then a `5.x` branch), 6.x for AMP 3 (AMP3-beta).
Nothing in `pyproject.toml` picks the line. A user picks it with the version they ask pip for.
- A version with `b` in it (`6.0.0b6`) is a pre-release. `pip install cc-ampapi` skips it, so the betas can be on
  PyPI while the default install stays 5.x. A beta is installed with `pip install --pre cc-ampapi` or
  `cc-ampapi==6.0.0b6`.
- Once 6.0.0 is out, the default install is AMP 3. AMP 2 users pin `cc-ampapi~=5.0` (`>=5.0, <6.0`). The README and
  the 6.0.0 release notes say so.
- A 5.x fix after 6.0.0 is released from the 5.x branch as 5.0.1, etc. PyPI takes an older line's version at any time,
  and the `~=5.0` pin picks it up.
- Each line raises a clear error on the other line's panel: #3-69 here, 5.x #47 on the AMP 2 line.
- One package name means AMP 2 and AMP 3 can't be driven from one program. Two names would allow it, at the cost of
  splitting the users and the docs, so it waits until someone needs it.

Publishing a beta (#3-70): `.github/workflows/build.yml` publishes on any published GitHub release, from the commit
the release's tag points at, with PyPI's trusted publishing (environment `release`), so AMP3-beta needs no new setup.
1. Bump `__version__` and `version_info` (eg. `6.0.0b6`) and commit.
2. Push AMP3-beta (`git push origin AMP3-beta`).
3. On GitHub, draft a release with a new tag (eg. `v6.0.0b6`) targeting AMP3-beta, and tick "Set as a pre-release".
   Publishing it runs the build and the upload. pip treats it as a beta from the `b` in the version, whatever the
   tick says; the tick keeps GitHub's "latest release" on the 5.x line.
4. Check `pip install --pre cc-ampapi` in a scratch venv.

The order:
- 5.0.0 from `main` first.
- Then the 6.0.0 betas from AMP3-beta.
- At AMP 3's release, 6.0.0 final, and the AMP 3 line becomes `main`, and the AMP 2 line moves to a `5.x` branch.

## First-run setup

Done through the API on vm3, with the setup code from `/opt/cubecoders/amp3/data/setup-token.txt` sent as
`X-Setup-Token`: `GET /api/auth/setup/code`, `POST /api/auth/setup/database/provision` (AMP sets up its own database,
done in seconds), `POST /api/auth/setup/admin` (returns the first token), then `POST /api/licence` with
`{key, terms}`. `POST /api/licence/query` checks a key without using it. The privacy, network and HTTPS steps are
browser-only and optional; `GET /api/health/status` read `ready` after the licence.
