# AMP API Notes

Developer context for the library. Anything useful that is not a task (`TODO.md`) or a
released change (`CHANGELOG.md`).


## Response narrowing

`Base._post` returns `ResponseTypeAlias | str | bool | None`. Endpoints narrow that union down
to one TypedDict before touching it, using the `is_response_type()` / `is_response_list()`
predicates in `_types.py` paired with the `*_REQUIRED_KEYS` / `*_EXCLUDED_KEYS` tuples.

Both predicates return a `TypeGuard`, which replaces the type outright. A TypedDict therefore
does **not** have to be a `ResponseTypeAlias` member to be a narrowing target. `TimedTriggerResponse`,
`SettingsSpecParentResponse` and `UserApplicationDataResponse` are all narrowed to without joining
the union, which keeps them out of the key-collision problem below.

The `*_EXCLUDED_KEYS` tuples exist because several responses share a key. `status` is the worst
offender - `ActionResultResponse`, `RunningTaskResponse` and `UpdatesResponse` all carry one, so
the first is identified by excluding the other two's unique keys rather than by a key of its own.
Adding a TypedDict to `ResponseTypeAlias` can force an existing excluded tuple to grow; adding one
outside the union cannot.

The first check after `_post` is on the container type the endpoint sends: `if not isinstance(result, dict):` for an
object, `if not isinstance(result, list):` for an array. Until #11, adsmodule used `isinstance(result, (str, bool)) or
result is None`, which let both through. Swapping all of them to the dict form broke the 11 list endpoints
(`get_instances` rejected every answer, caught live on vm1, 2026-10-23). Match the check to the `expec_type` of the
raise below it.

`no_data=True` is for an endpoint that answers JSON null (spec `Void`). `_post` still runs `_response_handler` for it
with `allow_null`, because AMP reports a failure in the body with HTTP 200 (`{"Status": false, ...}` or an error
`Title`). Before #11 `_post` returned None without reading the body, as 4.x's `_call_api` did: a bogus backup ID
for `set_backup_sticky` or a removed Minecraft method returned None as if it worked. An endpoint whose spec type is
`ActionResult` never takes `no_data`, even when the caller only needs success or failure.

A bool answer (spec `Boolean`, AMP sends a bare `true`) is written by `to_file` before `_response_handler` returns it.

`Core/RunSecurityCheck` sends `Pass`, which snake_cases to the keyword `pass`. `Base.json_key_mapping` renames it to
`passed` for every endpoint. It is the only keyword key seen in the specs and captures so far. A new one goes in the
same mapping.

`Core/RestartAMP` restarts the AMP process of whichever Instance gets the call. `restart_amp` is no longer
`@Base.ads_only` (4.x and the 5.0.0 baseline had it). Checked on vm1, 2026-10-23, by the process ID on the VM:
CustomTest01 and MCTest01 each got a new process, and the ADS01 holding them kept its own. A running application
(MCTest01's Minecraft server) is stopped and was still stopped 80 seconds later. The session dies with the process
(see "Sessions"). The application inside an Instance is restarted with `restart_application` (`Core/Restart`).


## Sessions

Stored per Bridge in `_sessions`, keyed by the object's `_instance_id` (the Controller's key is "0"). Each holds the
session ID and its login time. `_reauth` logs in when the key is missing, its ID is "0", or it is older than
`session_ttl` (240 seconds from login, not from the last call).

**A session lives and dies with the one AMP process that issued it** (vm1 + vm2, 2026-10-23, process IDs over SSH):
- An Instance reached through the Controller's proxy (`/API/ADSModule/Servers/<InstanceID>/`) logs in through it and
  gets its own session. That session doesn't depend on the session of whoever is logged in to the ADS.
- Restarting the Controller's AMP kills only the Controller's session. Its Instances, the Target and the Target's
  Instances keep theirs, even across the second hop. The same holds for restarting a Target.
- Restarting an Instance (`restart_amp`, the ADS's `restart_instance`, `ampinstmgr -r`) kills only that Instance's.
- `logout` ends the session on AMP's side.

**A dead session** answers "Unauthorized Access" with "This method requires the Session.Exists permission".
`Session.Exists` is the node for having a session at all. A missing permission names its own node instead (a vm1
user with no roles got `Core.RoleManagement.ViewRoles` from `get_role_ids`).
- `_response_handler` logs a warning for that answer and raises a private `_SessionDeadError`. `_post` resets the
  stored session only when it is still the one it sent (#22), logs in again and resends the request once. A late
  dead answer from a slow call therefore can't wipe a session another call just stored. A second dead answer raises
  `AMPAPIResponseError`, and `Core/Login` is never resent. AMP refuses the call before running it. A resend
  can't run anything twice.
- `restart_amp`, `upgrade_amp`, `update_amp_instance`, `logout` and `clean_up(logout=True)` reset the caller's own
  session when they finish. The next call logs in first instead of sending one that fails.
- A permission error raises at once, with no login and the session untouched. "Instance Unavailable" (an ADS
  booting, or a stopped Instance) raises and keeps the session, since it is still alive.
- One login for concurrent calls (#22, Kat's idea of checking the object's own state): a call that logs in sets
  `_login_pending` on the object, and the other calls on it wait for that login and use the session it stored.
  There's no lock to outlive an event loop, since the marker only exists while a login runs. If that login fails,
  each waiting call tries its own login, one at a time (Kat's choice). Live on vm1 after an `ampinstmgr -r`: 20
  concurrent calls made 20 logins before, and 1 after. With a wrong password, 5 calls made 5 failed logins, one at
  a time, and all raised.
- Measured after #18 (vm1/vm2): a reset recovers in two requests (login, then the call) with no log line, and a
  retry in three (the call, login, the resend) with one warning.
- With `use_2fa`, a retry logs in again with a fresh TOTP code, often the same code as the login before it. AMP
  takes the same code twice in one 30-second window. Checked on vm1, 2026-10-23, with a throwaway 2FA user: a
  login right after `logout` and a retry's login after a dead session both worked in the window of the login
  before them. `EnableTwoFactor` answers `result` with `url` (the authenticator link) and `manual_key` (the secret).
- `Core/GetRemoteLoginToken` rejects a null `IsTemporary`. AMP logs "Unable to convert parameter 'IsTemporary' with
  value '' to type 'Boolean'" and "Can not convert Null to Boolean" (vm1 ADS01, 2026-10-24). The spec marks both
  parameters optional, and AMP takes its default when one is left out, so the wrapper doesn't send one that is None
  (#25). Checked on vm1: no argument, `is_temporary` True or False, and both arguments each return a token.


## Dataclasses vs. the raw JSON

Response dataclasses inherit `ResponseData` and are built with `Cls.from_response(result)` (`modules.py`), never
`Cls(**result)` and never `cast` (#24, 2026-10-23; it was the module function `build(Cls, result)` until then).
`sanitize_json` has already snake_cased the keys by then. `from_response` reads the field type hints (cached per class)
and builds nested dataclasses through lists and unions, trying a union's members in order, so the dataclass goes first
(`list[Consumes] | list[ConsumesResponse]`). A key the dataclass doesn't declare is dropped and logged once per
class and key at WARNING. 4.x used dataclass-wizard's `fromdict`, which dropped them silently, and the 5.0.0 baseline's
`Cls(**result)` raised on them. `DeploymentTemplate` and `UserApplicationData` were the last two unpacked with `**`,
and the second raised once AMP-2.8.0.8 added `display_name` (live, 2026-10-21).

`ResponseData` sets `__slots__ = ()`. Without it every `slots=True` subclass gets a `__dict__` back (measured), which
would undo #9. A subclass that needs more than its hints overrides `from_response` (`SettingsSpecParent` builds the
`modules` dict, which the converter doesn't look inside, and `TimedTrigger` turns `tasks` into a list). The override
calls `super(TheClass, cls)`: a bare `super()` in a classmethod of a `slots=True` dataclass raises `TypeError` on
3.12, because `slots=True` builds a new class and the `__class__` cell still names the old one. `Players`,
`ScheduleData` and `TriggerID` keep their own `__init__(data)`, since each takes a whole answer, not one object's keys.
`Core.get_time_interval_trigger` sends `tasks` as a dict keyed by task ID (each task carries its `id` too), in every
2.8.0.8 capture; the other `tasks` keys AMP sends are lists. Moving `build` onto the class first cost ~4%; reading the
plan cache inline and binding each nested `from_response` once made it ~5% faster than `build` (Updates 210 -> 199 us).
`Messages` are AMP's push events, and what `parameters` holds depends on `message` (#26). Captured live on vm1,
2026-10-23/24, by triggering each event and polling `get_updates`. One raw example of each is in
`_responses/2.8.0.8/push_events/` (`ads.json`, `target.json`, `minecraft.json`, `generic.json`), and the full table is
in the #26 plan.
- `ADSModule/metrics` sends the `MessageParameters` dict.
- `Core/refreshTask` sends a whole running task (the `RunningTask` keys), and `Core/removeTask` sends the finished
  task's ID as a string.
- `Core/settingValueUpdate` sends `node` and `new_value`.
- `ADSModule/instupdate` sends `id`, `target` and `instance`, which is the Instance dict `GetInstances` sends.
- `ADSModule/refreshGroup` sends the Target ADS's GUID, and `ADSModule/refresh` sends null or a GUID.
- `Core/schedulemodified`, `Core/sessionslistchanged`, `Core/PermissionsNodeCacheInvalidated` (after an
  `update_instance_info`) and `ADSModule/refreshAppList` send null.
- From CustomTest01's fake game (#30, `push_events/generic.json`):
  - `Core/userlistchanged` sends one player record: `id` and `uid` (the `userid` group), `name` and `display_name`
    (the `username` group), `user_session_id`, `session_id`, `join_time`, `time_logged_in`, `tags`, `ip_address`
    and `port`. It comes for a join line and again for the leave line, with the same record.
  - `GenericModule/ServerInfoChanged` sends a dict keyed by the `Console.ServerInfoRegex` group names, lower-cased.
  - `GenericModule/ServerAuthURLPrompt` sends `url`, often twice for one console line. The panel ignores a URL that
    isn't https.
- `ADSModule/remotePairStatus` (with a capital P) reaches the Controller, not the Target, as soon as a Target registers
  with a pairing code. Its parameters are the `ActionResult` keys: `status`, `reason`, `support_url` and
  `support_title` (#30, re-pairing vm2).
- AMP sends both `refreshGroup` and `refreshgroup` (each a Target ADS GUID) for one delete on a Target, so a check on
  the message name needs to ignore case, as `Messages.from_response` does.
- Not seen even where the panel expects them: `instdelete` (a delete on vm2 through the Controller sent `instupdate`,
  `refreshGroup` and `refresh`, as on vm1) and `enumrefresh` (changing MCTest01's `ReleaseStream`, `ServerType` and
  `SpecificVersion` sent only `settingValueUpdate`). Both are most likely websocket-only on 2.8.0.8.

The fake game on CustomTest01 that produced these is described in "The fake game server on CustomTest01 (vm1)".

`Messages.from_response` builds `parameters` from a map keyed by `(source, message)`, with the message lower-cased
as the panel does: `metrics` and `BackupFailed` build `MessageParameters`, `refreshTask` builds `RunningTask`,
`settingValueUpdate` builds `SettingValueUpdate`, `instupdate` builds `InstanceUpdate`, `remotePairStatus` builds
`ActionResult` and `userlistchanged` builds `UserApplicationData` (#32; both records match those classes key for key,
so no new class was needed). Any other message keeps
what AMP sent, so a new shape is never dropped; add it to the map once it has been captured. `InstanceUpdate.instance`
stays a dict, because an `Instance` needs a bridge. Live on vm1, 2026-10-24, 276 messages built with no warning.

`ConsoleEntry` and Core `Metrics` never came through `get_updates`. The panel reads `Messages` only when websockets
are off, and then takes console lines and metrics from `ConsoleEntries` and `Status`, so both are most likely
websocket-only. A delete sent `instupdate` and `refresh`, not `instdelete`. The panel's handler for the Core ones
is `handleNotify` in `WebRoot/Scripts/AMP.js`, which also lists `schedulemodified`, `userlistchanged`, `enumrefresh`
and `settingValueUpdate` (`node` plus `newValues` / `newValue`), `ConsoleEntry` (a console entry),
`PermissionsNodeCacheInvalidated` and `Metrics`. Other sources go to each plugin's own handler. Until #26 the hint
allowed only `MessageParameters`, so a `refreshTask` was built as one and lost 20 task keys. AMP's logs record none of
these events.

Found while triggering them (vm1, 2026-10-24):
- `update_instance_info` couldn't succeed in 4.6.0 or before #27. `InstanceInfo.to_dict()` sent the field names
  (`instance_id`, ...), and AMP answered "UpdateInstanceInfo method requires InstanceId(String) argument". The
  endpoint takes flat parameters (`InstanceId`, `FriendlyName`, ...), not one nested object. With AMP's names it
  works, and AMP answers with a "Reconfiguring Instance" `RunningTask`, although the spec names `ActionResult`.
  `ContainerMaxCPU` was accepted as a string and as a float. Since 67be1d5 only `instance_id` is required, and a
  field left as None isn't sent. Live, an `InstanceInfo` with only `instance_id` and `description` changed the
  description and no other `GetInstances` key.
- `Template.to_dict()` had the same problem for `deploy_template` (#29, fixed in 247f4a4). That endpoint also takes
  flat parameters (`TemplateID`, `NewUsername`, ...). With AMP's names, AMP read the template and looked for a Target,
  then failed: "No viable deployment target could be found ... target reported no provisioning fitness data", for
  both Targets. Both Targets' `fitness` is null in `GetInstances`, and `GetProvisionFitness` answers null too (#3), so
  the `RunningTask` return the spec names is unconfirmed until a Target reports fitness (#30).
  What fills fitness is unknown (#30 phase B, 2026-10-24). `ADSModule.dll` has `UpdateLocalFitness` and the
  messages "Provision fitness score: {0}" and "Failed to get fitness from remote instance", but neither VM's ADS log
  has ever logged one. Restarting vm1's ADS01 left fitness null after two minutes. No setting names fitness, both
  VMs allow 32 Instances and local creation, and their Professional licence's `feature_set` is `RunAMP`,
  `ControllerTargetMode` and `InstanceCloning`. Untried: a different licence edition, and reading the DLL's code.
  `InstanceDatastore.to_dict()` is fine, because `add_datastore` and `update_datastore` send it as one nested object.
- `CreateInstance.ip_binding` defaulted to `"192.168.0.1"`, as in 4.6.0. AMP's create task fails on a machine without
  that address. It is `"0.0.0.0"` since #28, and an Instance created with the default worked on vm1.
- `Controller.instance_id` is `'0'`. The local ADS's ID, which `target_ads_instance` needs, is the "Local Instances"
  Target's `instance_id`.

`from_response` checks nothing for a plain hint: a dict AMP sends for a `str` field is stored as is. That is how
`ActionResult.result` (typed `str` until #19) held a dict for two endpoints. The spec types the result per endpoint as
`ActionResult<T>`. In 2.8.0.8, T is `String` (8 endpoints), `Guid` (`create_role`, `create_user`), `TwoFactorSetupInfo`
(`enable_two_factor`) and `JObject` (`activate_amp_license`). The last two answer an object, and their wrappers
return it typed (`TwoFactorSetupInfo`, `LicenceInfo`), since a failure already raises and the `ActionResult` around
it carries nothing more. Shapes from vm1, 2026-10-23: `EnableTwoFactor` sends `url` and `manual_key` (the secret).
`ActivateAMPLicence` sends `licence_key` (the key, echoed back), `grade`, `grade_name`, `product`, `product_name`,
`expires` (ISO, no timezone) and `usage`. Both dataclasses keep their secret out of `repr`.

`check_key_drift` compares each shape an endpoint narrows to with the whole answer and keeps the closest. Narrowed
to `ActionResultResponse`, whose `result` names no TypedDict, the inner keys were never compared. The two wrappers
narrow to `TwoFactorSetupResultResponse` and `LicenceResultResponse` instead (#20), whose `result` names the inner
shape, and `key_drift` follows it like any nested TypedDict (`result.manual_key`). A new `ActionResult<object>`
wrapper wants the same envelope.

A field whose keys are dynamic stays a raw dict and must not name a dataclass in its hint, or `from_response` drops the data.
`TriggerTasks.parameter_mapping` is keyed by the snake_cased `consumes` names of the task's method (eg. `seconds` for
`Event.CommonCorePlugin.Wait`), checked against 117 live tasks. The `ParameterMapping` dataclass declares the union of
those names across every task method in the 2.8.0.8 captures (`get_schedule_data`'s `available_methods`), 62 of them.
AMP's `ParameterMapping` is a `Dictionary<String, String>` and stores whatever a client sends (probed on vm1,
2026-10-20). `__post_init__` converts by each argument's `value_type`: Boolean, Int32, Double / Single, the enums
(ApplicationState -> `InstanceState`, `IfOperators`, `MailPriority`, by the numeric key the panel stores) and DateTime
(`fromisoformat`, then AMP's `%m/%d/%Y %H:%M:%S` rewrite of an ISO time with seconds). An empty string becomes None and
a value that doesn't parse stays the string, as in Moogles' `Builder.convert_values`. A method outside that list (eg. a
new plugin) has its arguments dropped and logged. Add them to both the dataclass and `ParameterMappingResponse`.

Naming: a dataclass `X` in `modules.py` pairs with its raw TypedDict `XResponse` in `_types.py` (5.0.0, Kat). The
`Module` dataclass stays out of `modules.__all__`: `ampapi` star-imports `_enums` after `modules`, and
`_enums.Module` would shadow it. `docs/types.rst` documents it with its own `autoclass`.

Raw dicts that stay raw on purpose (#16, 2026-10-21): maps with dynamic keys and `str` values (`Application.settings`,
`SettingSpec.enum_values`, `SettingsSpecAttribute.key_enum_values`, `Consumes.enum_values`, `Instance.deployment_args`,
`get_instance_live_settings`, `get_role_ids`), `StructuredDiagnostics.application` (keys differ per module), and
`ADSData.available_instances` (an `Instance` needs a bridge, not a dataclass). `APISpec` and `ActionSpec` are type
aliases over dynamic module and method keys; `automodule` skips aliases, so they are not in the docs. Fields AMP has
never sent in a capture stay `Any` (Bukkit, `ImportConfig`, `Fitness`, `Backup.meta`, `SettingSpec.warn_when_value`).
`Core.get_user_list` answers `{}` with no players in every capture; `[]` is handled as empty too.

Where a field is richer than the wire format (an enum, or a nested dataclass), the annotation is
widened to `Rich | Raw`. `from_response` builds a nested dataclass from the hint, and `__post_init__` converts an
enum (`Port.protocol`, `Status.state`). `Updates.status`, `TimedTrigger.tasks` and every `SettingsSpecParent`
category follow this shape. Built directly from a dict (`Status(**raw)`), the nested fields stay raw, as in 4.x.

Container fields are spelled as a **union of containers**, `list[SettingSpec] | list[SettingSpecResponse]`,
not `list[SettingSpec | SettingSpecResponse]`. `list` and `dict` are invariant in their element type, so
the raw response is not assignable to the combined form.

An annotation that the runtime does not honour is worse than a loose one; several were found
claiming a nested dataclass that nothing ever built. Where the nested shape is still unconfirmed
the field is left raw and tagged, rather than annotated aspirationally.

Key drift only compares keys, so a value whose type the hint doesn't allow passes it unnoticed (#34, 2026-10-24). A
survey checked every value in the 151 captures from 2.8.0.8 against both the TypedDict and the dataclass hint, and found:
- `SettingSpec.actions` was `list[str] | list[SettingSpecAction]`. `list[str]` accepts any list, so the actions stayed
  dicts until the dataclass went first. It was the only union with that order.
- AMP sends null for fields hinted as plain values: `UserInfo.email_address` is null for a user without one,
  `TriggerTasks.created_by` for some tasks, `SettingSpec.meta`/`placeholder`/`suffix` in the "updates" category and a
  new `DeploymentTemplate`'s `setting_mappings`, `tags` and `zip_overlay_path`.
- `TimedTrigger.enabled_state` is 0 or 1 and `Instance.port` is an int.
- `SettingSpec.min_value`/`max_value` are numbers in about 140 specs.
- Analytics percentages can be the string "Infinity" when AMP divides by a zero session time (one live capture,
  VaskelsServer).
Key drift couldn't see inside `list[Any]` fields, so #35 gave the nested Analytics and `SettingSpec` items their own
TypedDicts (`AnalyticsCountryDataResponse`, `AnalyticsTopPlayersResponse`, `SettingSpecActionResponse`,
`SettingSpecSelectionSourceResponse`, `SettingsSpecAttributeResponse`). `BuildInfo`, `BukkitPlugin`, `OPList` and
`Fitness` have none: AMP sends a version string for `BuildInfo`, the endpoints behind `BukkitPlugin` and `OPList`
were removed in 2.6.5.0, and `fitness` is null in every capture.
The survey script (`dc_survey.py`) lived in a session scratchpad; it pairs each wrapper's narrowing check with its
`from_response` call and needs `key_drift.declared_keys`, because `__required_keys__` ignores `Required`/`NotRequired`
under string annotations on 3.12.

Where a response's time goes (#9, measured 2026-10-21 on vm1 bodies, this box): before 5.0.0's changes, key
sanitising was 67-77% of decode + sanitise + check + build, because `camel_to_snake_re` ran three `re.sub` per key on
every response. `format_data=False` only skips the build, and its dict was the heaviest form (a new string per key per
dict: Updates 36 KB as a dict, 11 KB as dataclasses). `_snake_key` now caches the whole key conversion per key string
(`lru_cache(maxsize=4096)`, bounded because some answers are keyed by player ID) and `from_response` works out each
class's converters once (`ResponseData._build_plan`). `get_updates` went from ~2.8 ms to ~0.38 ms of library time, PermissionsSpec from
15.5 ms to 1.7 ms. The cache reads `Base.json_key_mapping` directly: change that mapping at runtime and call
`_snake_key.cache_clear()`. msgspec would be ~100x faster again but needs per-class rename maps (AMP sends both `ID`
and `Id`) and a rewrite; orjson is TODO #17.

The response dataclasses are `slots=True` (5.0.0, #9, Kat 2026-10-21). Measured with tracemalloc on vm1 bodies: 11-14%
less per object on most classes, 40-66% on classes with many defaulted fields (`ParameterMapping` 1860 -> 764 bytes,
`Triggers` 2857 -> 1680). A slotted dataclass has no `__dict__`: `__repr__` goes through `_field_values` and code
reads `fields()` rather than `vars()`. `__post_init__` can only set declared fields. `Instance.__slots__` is
different: its 28 names are real slots, but `Base` and the mixins have none and an Instance keeps a `__dict__` for its
8 private attributes. Slotting that whole chain saves 48 bytes per Instance, which isn't worth it. The tuple stays as
`_parse_instance_data`'s field list. Plan and numbers: `.local_data/plans/finished/memory_overhead/plan.md`.

AMP adds keys between versions. AMP 2.8 added `ports` to the status, three keys to each port and five to
each backup, plus `oidc_sub` (users), `local_login_enabled` (module info), `warn_text` / `warn_when_value` (every
setting), `notice` (schedule methods), `locked*` (method arguments) and four error keys on trigger tasks. New fields
go in defaulted so older responses still construct. A dropped-key WARNING from `from_response` is the cue to declare one.

`Core.get_setting_spec` categories vary by ADS, Instance and licence: only `system_settings` and
`security_and_privacy` are always sent. The VMs send no `branding`, Kat's live Instances do. Module categories have
a colon in the name (`valheim:stadiacontroller`, `valheim_plus:extension`) and go into `SettingsSpecParent.modules`.
`AnalyticsCountryData.session_percent` was never sent, AMP's key is `sessions_percent` (renamed for 5.0.0).

`Base.sanitize_json` is not safe to run twice on keys: a second pass strips the underscores
(`active_users` -> `activeusers`). The library sanitizes each response once, in `_response_handler`, and
`controller_dump.py` sanitizes its own raw fetches once; `Core.get_triggers` only runs it on strings, which
come out the same. Don't sanitize a capture or a `format_data=False` result again.

Some shapes differ by Instance type. The ADS reports `physical_ram_usage` and `swap_usage` metrics,
Minecraft Instances do not, and some modded ones add `tps`; `Metrics` only requires the three every
Instance sends. A stopped Instance reports its `metrics` as `{}`.


## Captured responses

`controller_dump.py -section LIVE -out ./_responses` captures responses from a live setup (it hits
the server, so not unattended). The `[LIVE]` login needs `bridge.use_2fa = True`, its TOKEN is the TOTP secret.

`_responses/` is grouped by AMP version and then by kind (#31, 2026-10-24; Kat: "naming the instance for a response
seems un-needed"). CONTRIBUTING.md shows the layout. In each version folder, `ads/`, `minecraft/` and `generic/` hold
one capture per endpoint, and a Target's, a live panel's or another game's answer sits in a subfolder (`target/`,
`live/`, `tf2/`, ...) only where its shape differs. `push_events/` holds the `get_updates` push event examples by kind.
- `2.6.5/` is the old Controller run that was at the root; `unit_test.py` reads `2.6.5/ads/`.
- `2.8.0.4/ads/` is the old `controller_setup/` dump.
- `2.8.0.8/` merges the 2026-10-20 VM refresh (#1: vm1 Controller, vm2 direct and through the Controller, seven
  Instances), Kat's live captures from 2026-10-18 to 2026-10-21 (without sessions or file contents), and the #26 and
  #30 push events. Base files come from vm1 first; CustomTest01 is the `generic/` base.

Of 675 files, 264 were kept and 407 same-shaped copies dropped. The key drift check over the new `2.8.0.8/` finds the
same 15 drifted keys as over the old folders. The old tree is archived in `.local_data/responses_before_31.tar.gz`.

`Core/GetOIDCLogoutUrl` is spelled `Url`, unlike `Core/GetOIDCLoginURL`. The spec sheets snake_case method names, so
they can't show the casing; "No such web method" on a method the spec lists is the sign of a casing mismatch.

Shapes not yet confirmed against a live payload:

- `ProvisionResponse`, derived from the dataclass and docs. `GetProvisionFitness` answers null on the VMs (#3).
- `OPWhitelistResponse`, built from the `OPWhitelist` dataclass; `GetOPWhitelist` answers
  "Missing Method" and is in no spec sheet.

`DeploymentTemplateResponse`, `TimedTriggerResponse` and `UserApplicationDataResponse` were on this list until the
2.8.0.8 captures. The key drift check finds no drift for any of them.

`ampapi/key_drift.py` notices AMP changing its keys; usage is in CONTRIBUTING.md ("Checking for key
drift"). `key_drift()` / `declared_keys()` are the same functions as Minerva's and Python_Template's
copies, so keep them in step.

A failed login (wrong password or wrong 2FA code alike) answers `success: false`, `result: 40`, an
empty `result_reason` and `session_id: None` on AMP 2.8.0.8, so AMP gives no reason to pass on.

The doc generators in `util.py` import their notes from `docs/samples/`, which is not packaged, so
they only run from a repo checkout.


## Verification

The checks to run before a change lands are in CLAUDE.md ("Before reporting work as done"); `land_check.py` runs
Ruff, pyright, Sphinx and the style rules together.

`unit_test.py` at the repo root is untracked and hits a live AMP Instance - do not run it
unattended.

Captured responses live in `_responses/`. A TypedDict built from a dataclass definition instead of
a captured payload is a guess; `getscheduledata.json` exposed two dataclasses (`Methods`, `Triggers`)
that raised `TypeError` on their own documented response because fields were missing.



## The fake game server on CustomTest01 (vm1)

Use CustomTest01 whenever a test needs a running game: player joins and leaves, server info, a sign-in prompt, console
output, or an app that starts, runs and stops cleanly. It is a Generic "Custom Application" Instance with no real game
behind it, so it starts in a second, needs no download, and nothing breaks if it's stopped mid-run (#30, 2026-10-24).

- **Run it:** `start_application()` on the CustomTest01 Instance, then poll `get_updates`. `stop_application()` sends
  `stop` on the console and the script exits cleanly (app state 80, then 0). The Instance itself stays running.
- **What it prints:** `GenericApplication/fakegame.sh` prints `FakeGame ready`, then 40 rounds, 4 seconds apart, of:
  - `FakeGame: player FakePlayerN joined with id 76561198000000N`
  - `FakeGame: server info Version=1.N`
  - `FakeGame: open https://example.com/auth?user_code=FAKEN to sign in`
  - `FakeGame: player FakePlayerN left id 76561198000000N`

  After that it idles until stopped.
- **What AMP makes of it** (examples in `_responses/2.8.0.8/push_events/generic.json`): `Core/userlistchanged`
  for each join and leave, `GenericModule/ServerInfoChanged` (`server_version`) and
  `GenericModule/ServerAuthURLPrompt` (`url`), plus console entries in `get_updates` and the usual task events.
- **The patterns** are in `GenericModule.kvp`. `App.ExecutableLinux=fakegame.sh`, `Console.AppReadyRegex`,
  `UserJoinRegex` and `UserLeaveRegex` (groups `username`, `userid`), `ServerInfoRegex` (any group names become the
  keys) and `ServerAuthURLPromptRegex` (group `url`, https only). The file from before #30 is
  `GenericModule.kvp.pre30a`.
- **Changing it:** these Generic app settings aren't in the settings spec, and `get_config` answers "No such node". So
  stop the Instance (`ampinstmgr -q CustomTest01`), edit the kvp or the script as the amp user, and start it again
  (`ampinstmgr -s CustomTest01`). After that the Controller may still show it as stopped until `start_instance` is
  called once. A new console line plus a matching pattern is all a new event needs.
- **What it can't do:** Analytics on the VMs runs in demo mode (`is_demo: true`, about 30 made-up players), so the fake
  players never reach `get_user_details` or `get_user_list`. A demo player's `get_user_details` answer matches
  `AnalyticsUserDetails` key for key.

## Building VMs

On Kat's rig the KVM test VMs are managed by `.scripts/vms.py` (gitignored, like `local.py`): `vm1` AMP2 Controller,
`vm2` AMP2 Target, `vm3` AMP3 beta. `.venv/bin/python .scripts/vms.py status|start|stop|refresh-urls|...`; their AMP
logins are the `[VM_*]` sections of `local.ini`. The host setup is in `.local_data/plans/headless_vms.md`.
`getamp.sh` installs AMP unattended with `USE_ANSWERS=1`, but always pass `ANSWER_SYSPASSWORD`: left empty it stays
empty and the install fails creating the `amp` user. A fresh ADS has no mode; set `ADSModule.ADS.Mode` to
Controller before pairing a Target.

A pairing code alone is not enough (AMP 2.8.0.8): the Controller's polls fail with "Token Rejected", and the remote
Target lists no Instances. The Controller logs in to the Target with a token from its own `AMP_SYSTEM` user, so the
Target has to check logins with the Controller (`Core.Login.UseAuthServer` True, `Core.Login.AuthServerURL` the
Controller's URL), and the Controller has to answer them (`Core.Security.EnablePassthruAuth` True, else "Passthru
Disabled"). Restart both ADSs after. From then on the Target takes the Controller's logins, not its own.
`vms.py role` does this right after the install, the way AMP's setup wizard does (one `SetConfigs`, then an ADS
restart, then it waits for the panel): the role, `Core.Login.*`, `DefaultAuthServerURL` and passthru. `vms.py pair`
runs it for both ADSs, then pairs. Order for a fresh pair: create, install-amp, activate, role, pair.

The Target's Instances need the same: an Instance created on the Target authenticates with the Target's ADS
(`Login.AuthServerURL=http://localhost:8080/`), and that hop fails even with passthru on. AMP's own fix is
`ampinstmgr --RepairAuth <mode> <controller url>` (alias `-magic`, run as `amp` with ADS stopped): it points the ADS
and every Instance at the Controller, and sets `Defaults.DefaultAuthServerURL` so new Instances start that way. It
asks the same two questions as the role choice in the web setup (`standalone` / `controller` / `target` / `hybrid`, and the
Controller's URL). Run on vm2 as `target`, it fixed `MCTest01`; not yet run on a Controller.

A new Instance's auth server comes from the ADS that receives the create call (VM pair, 2026-10-19):
- Its `Login.AuthServerURL` is the receiving ADS's `ADSModule.Defaults.DefaultAuthServerURL`. Sent to the Controller
  for a Target, that is the Controller's default. `ampinstmgr quick` leaves it as `http://localhost:8080/`, which on
  the Target means the Target, so the Instance's logins through the Controller fail (result 0).
- Same CreateInstanceFromSpec sent through the `TargetADS`: the Target's own default (the Controller's URL), correct.
- `CreateInstance` with `Core.Login.*` in `ProvisionSettings` still got the Controller's default. ProvisionSettings
  don't override it.
- AMP's setup wizard (`/Plugins/ADSModule/Plugin.js`, `finish`) sets a Controller's or Hybrid's DefaultAuthServerURL
  and `Core.Login.AuthServerURL` to its own URL, and a Target's to the Controller's URL. With vm1's default set to its
  own URL, Instances created through either route log in.
- `ApplyInstanceConfiguration` with `Args` `{"Core.Login.UseAuthServer": "True", "Core.Login.AuthServerURL": url}`,
  sent through the `TargetADS`, repairs one Instance, like `RepairAuth` does for all. It answers a RunningTask.
  `RepairAuth target <vm1 url>` (on vm2) also works, and stops vm2's Instances, which need starting again after.
- `ADSModule.Network.AccessMode` (0/10/20) doesn't change any of it: a wrongly pointed Instance fails and a right one
  logs in, in every mode.
- Users: one created through the `TargetADS` lives in vm2's own user database (vm1's `GetAMPUserInfo` doesn't know
  it). With a role it logs in to vm2 directly, to vm2 through the Controller's proxy, and to vm2's Instances, but not
  to vm1 (result 5). One created on the Controller with a role logs in everywhere. vm2 reports the same role IDs as
  vm1. Without a role, either gets result 5 on Instances. Deleting a user needs it disabled first.

A GenericModule Instance's `GetDiagnosticsInfo` adds `config_version` (eg. "3"), like Minecraft adds `server_type`,
`server_jar` and `java_version`.

Creating an Instance needs a licence key in `ADSModule.Defaults.NewInstanceKey` on the ADS that runs it, the Target
when creating from the Controller; `vms.py activate` sets it. AMP accepts the `CreateInstance` call and queues it as a
task, and only the Controller's log says it failed for want of a key. `CreateInstance` also needs a GUID in
`NewInstanceId` (all zeros lets AMP pick) and a non-empty `AdminUsername`, even with `AutoConfigure`.

## Controller and Target data

Checked on the VM pair, AMP 2.8.0.8, one Controller with only its ADS and one Target with only its ADS:
- `GetInstances` sends one Target per ADS. The local Target's `friendly_name` is "Local Instances", and each Target
  lists its own ADS Instance, the one whose `instance_id` matches the Target's.
- `ForceIncludeSelf` False on a Controller drops the whole local Target only when it holds nothing but the
  Controller's own ADS, which would leave the Controller's cached data unset. So the library always sends True and
  `get_instances` has no `include_self` (2026-10-19).
  With local game Instances (2026-10-19, vm1 with six) the local Target is sent anyway, ADS01 included, in controller
  mode and in hybrid mode alike. On a Target or a standalone ADS it changes nothing.
- `GetInstance` on the Controller's own ADS ID, or on a Target's ADS ID, returns that ADS Instance. Nothing in it
  says which. `Controller.get_instance` returns `self` for its own ID once it knows that ID (from `get_instances()` or
  `auto_detect=True`), and a `TargetADS` otherwise. A `TargetADS` for either ID proxies fine (`get_updates`).
- `GetInstance` on an ID AMP doesn't know returns JSON `null`, which `_response_handler` raises as
  "JSON returned <None>".
- `Controller.instance_id` stays "0" after `get_instances()`. That is the Controller's session key, not a missing value.
- With a Minecraft Instance on the Target, both sides return it as a `MinecraftInstance`, and formatted
  `get_status` / `get_updates` work through the Controller (vm1 -> vm2 -> Instance) once the auth chain is repaired.
  Instance order is not fixed: the Target lists its Minecraft Instance before its ADS Instance, the Controller after.
- Nothing in an ADS's data names its role. The `GetInstance` ADS Instances, the local `GetInstances` Target and
  `GetTargetInfo` match field for field between the Controller and the Target, bar the IP lists. `deployment_args`
  holds `core._login._use_auth_server` only in the Target's own view, and only once `RepairAuth` wrote it. The role
  lives in `ADSModule.ADS.Mode` (`get_config`, an `ADSModeState`); from a Controller, `is_remote` True also marks a Target.
- `Core/GetModuleInfo` gives the logged-in ADS's own ID (`instance_id`) and `is_remote_instance`: True on a Target,
  False on a Controller and on a standalone ADS (Kat's live capture), so it tells a Target apart but nothing else.

- `ADSModule/StartInstance` and its siblings pick the Instance by name, on the ADS the call is sent to. Sent to the
  Controller, `"ADS01"` is the Controller's own ADS even when the caller means a Target's `ADS01` (vm1 logged the
  request, vm2 nothing). So an Instance stores the ADS that holds it (`Instance.ads`): the Controller for its own, the
  `TargetADS` for a Target's. `start_instance()` / `stop_instance()` / `restart_instance()` / `upgrade_instance()` and
  `get_instance_status()` go through it. Checked live (2026-10-19) with a same-named `MCTest01` on vm1 and vm2:
  stopping and starting each one through its object left the other running.
- A Target's game Instances carry the wrong `target_id` when read through the Controller (2026-10-19). vm2 lists
  MCTest01 with `target_id` = vm2's ADS ID, but vm1's `GetInstances` and `GetInstance` relay it with vm1's own ADS ID,
  while the Target's ADS Instance keeps its own ID. The Controller answers from its own copy of a Target's Instances,
  and other fields differ too (`deployment_args`, `application_endpoints`, `is_multi_ip_aware`, `order`). So
  `Controller.get_instances()` never builds objects from that copy: it builds a `TargetADS` per remote Target and fills
  each from the Target itself, all at once. `Controller.get_instance()` raises for an ID a cached `TargetADS` holds.
- Through the Target's own ADS the data is right. `Controller.get_instances()` builds a `TargetADS` for a Target's ADS
  Instance (endpoint `ADSModule/Servers/<Target ADS ID>`), and vm2 answers its calls: `get_module_info` gives vm2's ID
  with `is_remote_instance` True, and `get_mode()` gives `target`. `TargetADS.get_instances()` and
  `TargetADS.get_instance()` return MCTest01 with `target_id` = vm2's ID.
- A Target whose ADS is stopped is still listed by the Controller's `GetInstances` (from its copy, `state` 20, with its
  Instances). Its `TargetADS.get_instances()` fails at once with "Instance Unavailable", so `Controller.get_instances()`
  logs a warning, keeps that `TargetADS` with empty `instances`, and returns as normal.
- AMP sends some Instance fields as null (on the VMs: `description` on all 8 Instances, `module_display_name` on 4,
  `display_image_source` on 1), and never sends `url` for an Instance. `_parse_instance_data` sets them to their
  documented default (`""` for those three, None otherwise), so no Instance field raises AttributeError.
- A `TargetADS` keeps its Target's data flat like the Controller (2026-10-19). It first gets the Controller's copy of
  the Target entry, then the Target's own view from its own `GetInstances`. The own view is fresher, but three fields
  depend on who is asking: from the Target itself `url` is `http://localhost:8080`, `is_remote` is False and `id` is
  its own numbering. So those three stay the Controller's. `friendly_name`, `description` and `tags` stay the ADS
  Instance's (ADS01), not the Target's (amp-target).
- The library only ever talks to the Controller's URL. A `TargetADS` calls `ADSModule/Servers/<Target ADS ID>/API/...`
  and an Instance calls `ADSModule/Servers/<Instance ID>/API/...`, both on the Controller, which passes them on.
- `ADSModule.Network.AccessMode` (`AccessModeState`, set on the Controller) is how the Controller reaches a remote
  Instance: 0 "Via Target" (the Target relays, the default), 10 "Direct from Controller" (the Controller connects to the
  Instance's port), 20 "Bypass Controller" (the browser talks to the Target's ADS, which needs HTTPS and CORS). See
  https://discourse.cubecoders.com/t/2268. On the VM pair (2026-10-19) every mode left the library's calls working:
  `TargetADS` `get_module_info` / `get_instances` / `restart_instance`, MCTest01's own `get_module_info` / `get_status`,
  and `Controller.restart_instance` by name. Nothing in the settings spec stops a Target managing its own Instances.
- For a few seconds after `restart_instance`, calls to that Instance fail with "Instance Unavailable" ("The requested
  instance is not available at this time"), and so does the library's re-login.

## Endpoint shapes confirmed on the VMs (2026-10-19)

- `ADSModule/GetGroup` (`groupId` = a Target's ADS ID, the Controller's own too): the Target item, the shape of one
  `GetInstances` entry (`ControllerResponse`), JSON null for an unknown ID. The panel calls it to refresh one Target.
- `ADSModule/Servers` is AMP's proxy route (`ADSModule/Servers/<ID>/API/...`). Called as an endpoint it answers
  "Index was outside the bounds of the array".
- `Core/GetStructuredDiagnostics`: `{"core": <the GetDiagnosticsInfo keys>, "application": {...}}`. `application` is
  `{}` on an ADS and `{"config_version": "1"}` on a Generic Instance.
- `FileManagerPlugin/WriteFileChunk`: `Data` is base64, `FinalChunk` True only on the last chunk (the panel's upload).
- `FileManagerPlugin/UploadFolder`: each file is `{"RelativePath": str, "Base64Data": str}`, into an existing
  `TargetDirectory`; subfolders in `RelativePath` are created. The panel uploads folders file by file instead.
- `FileManagerPlugin/AppendFileChunk`: answers null and has no visible effect. It creates no file, doesn't append to
  one WriteFileChunk made, and `Delete` True leaves it alone. The panel never calls it.
- `ADSModule/GetProvisionFitness`: JSON null on the VMs (no fitness data), so its shape is still unknown.
- `AnalyticsPlugin/GetUserDetails` (confirmed live 2026-10-21, FTBEvolution01): null unless the Instance has
  `AnalyticsPlugin.Privacy.EnableAnalytics` and `UserSpecificData` on (neither needs a restart, and a session already
  running when they were turned on was recorded). It takes the player name, a UUID answers null. Times are minutes,
  `first_session` / `last_session` have no timezone but match `GetUserInfo`'s UTC `JoinTime`. `recent_sessions` is
  keyed by session start time; `sanitize_json` leaves those keys alone only because the 7-digit fraction puts a `.`
  in them, which it treats as a setting node.
- File paths: AMP's file manager takes `\`, `//`, `./`, `../` (it stays inside the Instance), `_` and dot-folders
  like `.trash` as given. Only a bare `/` fails ("Index was outside the bounds of the array"), so
  `Base.sanitize_path` just drops leading slashes.

## Generic Instances

Surveyed 2026-10-19 on TF2, Valheim, ET: Legacy, Custom Application and CS:Source (AMP 2.8.0.8):
- Every game template reports `module` "GenericModule", a Custom Application reports "Generic". Both stay a plain
  `Instance`, which carries the GenericModule and SteamCMDPlugin endpoints behind `Base.generic_only`, so a Minecraft
  Instance or a `TargetADS` raises instead of asking AMP. AMP 2.8 has no `srcds` module.
- Every one serves the same extra API sections, Steam or not: `GenericModule` (5), `steamcmdplugin` (3) and
  `RCONPlugin` (`Dummy`, a placeholder). The SteamCMD URL is lowercase `steamcmdplugin/...`.
- The Void endpoints answer JSON null. `RefreshRemoteOptions` / `RefreshToolDiscovery` need a setting that has a
  remote option source / tool discovery, otherwise status False ("No remote option source found for ''").
- `GetDiagnosticsInfo` adds `config_version` on the game templates (TF2 "7", CS:Source "3"), not on Custom Application.

## Wrapper parameter gaps

`find_parameter_mismatches(spec_path=docs/api_spec_sheets/2.8.0.8)` compares argument names with the spec's, so most
of what it lists is a rename (`file_path`, `instance_id`) or a parameter carried by a dataclass (`create_instance`,
`deploy_template`). Leave out `spec_path` and it merges every version with "first file seen wins", so 2.6.2.0 shadows
2.8.0.8. #13 (2026-10-24) compared the keys each method actually posts with the 2.8.0.8 spec instead, and added the
26 parameters that were missing in 12 methods. A new optional parameter is keyword-only, defaults to None, and isn't
sent when None.

What the live checks on vm1 showed (2026-10-24):
- **AMP matches parameter names regardless of case.** `groupId`, `GroupId` and `groupid` all worked on `GetGroup`, so
  the nine methods whose keys differ from the spec only in case are left as they are. A wrong name fails with
  "<Method> method requires <Name>(<Type>) argument".
- **Fixed, because they always failed:** `refresh_setting_value_list` sent `Name` for `Node`, and
  `edit_interval_trigger` sent single ints where AMP takes `Int32[]`.
- **Fixed, because AMP ignored the value:** a `DateTime` parameter sent as a POSIX timestamp is ignored, and an ISO 8601
  string is honoured. `get_audit_log_entries(before=...)` answered the newest entries whatever `before` was, and
  `get_analytics_summary` sent `StartDate` the same way. Both send `isoformat()` now.
- **`take_backup(dirty_only=True)`** answers an `ActionResult` and takes no backup when no file changed, instead of a
  `RunningTask`.
- **`update_instance_info` can't clear a value back to null:** None isn't sent, so restoring an empty `group` sends
  `""`, which AMP stores as `""`.
- Left alone: `ADSModule.servers` is AMP's proxy route and already warns that calling it fails.
- Not checked against a spec: the sixteen `mc_*` wrappers in `minecraft.py`, whose endpoints the 2.8.0.8 Minecraft
  spec doesn't list.

## Non-admin users

Tested with a user holding no roles, then a role with `Instances.<id>` nodes (AMP 2.8.0.8, Professional licence):
- On the ADS it logs in to, it can call `GetModuleInfo`, `GetConfig` (`ADSModule.ADS.Mode` included), `GetInstances`
  and `GetInstance`. `GetTargetInfo` needs `ADS.InstanceManagement.CreateInstance`. The spec's empty
  `required_permissions` lists are no guide: `SetConfig` is empty too.
- It cannot reach a Target's ADS or a Target's Instance, directly or through the Controller: the login fails with
  result 5 (`NoInstanceAccess`), even with `Instances.<id>` granted on the Controller, and the Controller's
  `GetInstances` leaves the Target out. Shared roles, which carry permissions to Targets, are refused on Professional
  ("Common/shared roles are not available on this edition of AMP").
- `Settings.<Module>.<Category>.<Name>` nodes decide who may change a setting, per the permissions spec.

## Version directives

How to write them is in CLAUDE.md ("Version Directives"). What the #14 test build showed (2026-10-20, Sphinx 8.2.3
and furo):
- Napoleon passes them through from a numpy docstring, in the body or nested under a parameter's description, and
  `:attr:` / `:meth:` references inside them resolve. They render as "Added in version 5.0.0:" and so on.
- `docs/extensions/prettyversion.py` (from dpy/Umbra, commented out in `conf.py`) swaps them for boxes with
  Font Awesome icons. The docs don't load Font Awesome, so the icons would be blank without it.
- 5.0.0 tags only the objects whose use changed (Kat, 2026-10-20): `Controller.instances` / `targets`,
  `TargetADS` start, stop and restart, `write_file_chunk` and `sanitize_path`. `docs/upgrading.rst` stays the full
  4.x -> 5.0.0 record. Later changes get their tag as they are made.

## Class order

The rule is in CODING_STYLE.md §21 (2785a7a for `modules.py`, b9367bd for the rest). Where it lands in this library:
- The same-file base classes that come first are `ResponseData`, `AMPAPIError`, `ADSData` and `Instance`.
- `_SessionDeadError` sits right above `Base`, its only user. The TypedDicts in `base.py` type `Base`'s parameters, so
  they sit above `Base` as its helpers, in alphabetical order among themselves.
- `APISpec` in `_types.py` is built from two TypedDicts when the module is imported, so it sits right below them.
  Every other annotation is a string under `from __future__ import annotations`, so its order doesn't matter.
- `docs/conf.py` sets `autodoc_member_order = "bysource"`, so `automodule` pages (`_types`, `modules`, `errors`)
  list the classes in this order. The `autoclass` pages in `docs/*.rst` keep their own order.
