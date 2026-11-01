# Version - 5.0.0 - [f5610b6](https://github.com/k8thekat/AMPAPI_Python/commit/f5610b6)
## A dead session on an ActionResult endpoint logs in again (#44)


## base.py *w/Claude
- `_response_handler` treats a `Status` False whose reason names `Session.Exists` as a dead session, so `_post` logs in again and resends the call.
	- Plain `ActionResult` endpoints answer a dead session that way instead of with "Unauthorized Access", so those calls raised without logging in again.
- `ResponseHandlerOptions` drops `sanitize_json`, since every endpoint method checks the sanitized key names.
	- With AMP's names those methods raised a misleading `AMPAPITypeError`, even with `format_data=False`.
- `_post` takes `sanitize_json` as its own keyword.
- `_response_handler`'s error checks read a sanitized copy, so a raw answer still raises on a failure and still logs in again on a dead session.
- A root dict with a key that can't be a field is written as Name = dict[str, V], the same rule nested dicts follow.
	- The role IDs, live settings and settings spec categories differ per panel, so a map is their honest type and key drift skips it.
	- 13 of the 246 captures gave invalid code before, and they are the only ones whose output changed.
- A Python keyword such as from can't be a field either, since isidentifier() is True for it.
- pascal_case splits on any character that can't go in a name and prefixes a leading digit with Key, so class names are always valid.
- The imports leave out TypedDict when the output has no class.
- Replaced the four closures of json_to_typeddict with the private _TypedDictWriter class above Base.
	- The old body is commented out above the new one, without its ignore pragmas, which pyright and Ruff flag inside a comment.
- A class name already taken by a different body gets the parent class name in front, then a number.
	- Two nested dicts under the same key used to share the first one's class.
- A key missing from some dicts of a list is NotRequired, and a key that is None in some is X | None.
- Mixed types are a sorted union everywhere, and Any is only used for an empty list or dict.
- Dicts held by one key across the items of a list are merged into one class, so the first shape no longer wins.
- The output no longer opens with blank lines, and the imports name only what the classes use.
- json_to_typeddict has a versionadded 5.0.0 directive.
- sanitize_json has overloads, so a str gives a str and any other value keeps its type.
	- The list and dict branches bind typed locals so strict pyright stays clean.
- _response_handler drops a None check the typed result made redundant.
- Removed the _call_end_point TODO.
- `sanitize_json` converts each key once and remembers it.
	- Bounded `functools.lru_cache` (4096), as some answers are keyed by player ID.
	- Builds fresh dicts and lists instead of copying then popping and re-adding.
- `camel_to_snake_re` patterns are compiled once as module constants.
- Follows the TypedDict renames.
- `route_by_target` sets a per-object `_route_override`; the `_route_by_target` ClassVar stays as the default.
- The login error names AMP result codes 0 (Failure), 5 (NoInstanceAccess) and 100 (PassthruDisabled), confirmed in AMP's logs.
	- Every other code stays its number.
- `clean_up` takes a keyword-only `logout` that calls `Core/Logout` before closing the session.
	- A failed logout is logged as a warning and the session is still closed.
- Corrected the `instance_id` docstring: the default is "0", a login does not set it, and a Controller keeps "0".
- `version_validation` takes the `endpoint` it guards and names it in the error instead of a hard-coded `Core/GetWebserverMetrics`.

## NOTES.md
- The `ActionResult` form of a dead session, and the sweep of every spec method that found it.
- Why `sanitize_json` left the endpoint methods, and the `ActionResult` form of a dead session.
- The datastore crash, its cause and the live check.
- What UpdateDatastore did to vm1's ADS and how it was recovered.
- OPWhitelistResponse can't be confirmed, since GetOPWhitelist was removed in AMP 2.6.5.0.
	- AMP 2.8.0.8 answers Missing Method, checked on FTBEvolution01.
- Recorded what AMP did with AutoConfigure True and a given InstanceName.
- Recorded the creation task's lifecycle on the local and a remote Target, and how a remote creation changes the request.
- Recorded what AMP did on vm1 for ReleaseFileUploadLock, OIDCLogin, SetConfig and CreateInstance.
- Recorded the nested TypedDicts and why four dataclasses have none.
- Recorded the survey of values against hints and what it found.
- "Version directives" and "Class order" keep only what is particular to this library and point to CLAUDE.md and CODING_STYLE.md §21 for the rules.
- "Verification" points to CLAUDE.md's checks instead of listing older commands.
- Only `ProvisionResponse` and `OPWhitelistResponse` are still unconfirmed; the 2.8.0.8 captures settled the other three.
- Dropped the old two-VM build script, which `.local_data/plans/headless_vms.md` holds.
- Replaced two em dashes.
- The "Class order" section says `BaseArgs` was removed.
- "Class order" says private classes go by what uses them, and that the future import only defers annotations.
- Added "Class order": alphabetical, a same-file base first, and `APISpec` below the TypedDicts it is built from.
- Rewrote "Wrapper parameter gaps" with what #13 found live: AMP ignores parameter-name case, ignores a POSIX timestamp for a DateTime, and `take_backup(dirty_only=True)` can answer an ActionResult.
- The `Messages.from_response` map lists the two new messages.
- The fake game server on CustomTest01: how to run it, what it prints, the events it gives and how to change it.
- Push events from #30: `userlistchanged`, `ServerInfoChanged`, `ServerAuthURLPrompt` and `remotePairStatus`.
	- `instdelete` and `enumrefresh` never came, even for a delete on vm2 or a selection setting change.
	- AMP sends both `refreshGroup` and `refreshgroup`.
- Provisioning fitness stays null after an ADS restart, so #3 and the #29 return wait.
- The `_responses/` layout by AMP version and kind, and what each version folder holds.
- `InstanceInfo` with only `instance_id` and `description` changed only the description.
- `deploy_template` reached AMP's Target check with the new keys, then failed because no Target reports provisioning fitness, so its return is unconfirmed (#30).
- How `Messages.from_response` builds `parameters`, and the live results for #26, #27 and #28.
- `deploy_template` has the same key problem as `update_instance_info` (#29).
- What each `get_updates` push event sends, captured by triggering each one on vm1.
	- `ConsoleEntry` and Core `Metrics` look websocket-only. A delete sends `instupdate` and `refresh`, not `instdelete`.
- Found on the way: `update_instance_info` sends snake_case keys, and the `CreateInstance.ip_binding` default only fits one network.
- The `GetRemoteLoginToken` finding is recorded as fixed, with the vm1 check.
- Removed the ADS proxy session warnings, which are noise.
- `Messages.parameters` per message type, found live on vm1 with a backup and `refresh_remote_config_stores`.
	- `removeTask` sends the finished task's ID as a string, `refreshTask` a whole running task, `metrics` the `MessageParameters` dict.
- Calls through the ADS proxy log a session warning on the ADS, although they succeed.
- `GetRemoteLoginToken` without `is_temporary` fails in AMP.
- `from_response` replaces `build` in the dataclass notes.
	- The base needs `__slots__ = ()`, overrides call `super(TheClass, cls)` on 3.12, and the timings.
- An unconfirmed string `Messages.parameters` seen live on vm1.
- Sessions: the reset now happens in _post, only for the session that died.
- Sessions: one login for concurrent calls, measured on vm1 (20 logins before, 1 after), and a wrong password.
- How key_drift now sees inside result, and that a new ActionResult<object> wrapper wants an envelope.
- upgrade_instance named in place of update_instance, one sentence reworded.
- check_key_drift can't see inside an ActionResult<object> result (#20).
- build stores a dict for a str hint as is, the spec's ActionResult<T> list, and the two shapes.
- Sessions: AMP takes the same TOTP code twice in one window, and a 2FA retry logs in (checked on vm1).
- Sessions: what each restart kills (measured on vm1/vm2), the Session.Exists marker, the retry and reset, no lock.
- restart_amp note no longer names the removed Core.restart_instance.
- Two sentences reworded.
- What restart_amp restarts, measured on vm1.
- Response narrowing: the container check, what no_data still checks, bool captures, the Pass key, restart_amp's ads_only guard.
- How `GetUserDetails` answers, from FTBEvolution01 with Analytics turned on.
- `UserApplicationData` is no longer unpacked with `**`.
- Points at the finished plan.
- Where a response's time goes, what the key cache and build plans changed, and how to clear the cache.
- Added the slots measurements and why `Instance.__slots__` stays a field list.
- Which response fields stay dicts on purpose, the `APISpec` / `ActionSpec` aliases, and `get_user_list`'s `{}`.
- How `ParameterMapping` converts each `value_type`, from the vm1 probe and Moogles' `convert_values`.
- Naming rule: dataclass `X`, raw TypedDict `XResponse`; why `Module` stays out of `modules.__all__`.
- `session_percent` note says it was renamed.
- How `DCParameterMapping` was derived, and what to do when a plugin adds a method.
- "Dataclasses vs. the raw JSON" describes `build`, dynamic-key fields and the keys AMP 2.8 added.
- "Captured responses" points at the 2026-10-20 VM and live captures, the `[LIVE]` 2FA login and the `GetOIDCLogoutUrl` casing.
- How to write an AMP version in a version directive.
- Which objects 5.0.0 tags, and the AMP version on `get_webserver_metrics`.
- Version directives: what Sphinx and furo already support, checked with a test build.
- `vms.py role` sets the ADS role right after install, like AMP's setup wizard, and the order for a fresh pair.
- Which Instance fields AMP sends as null, and their defaults.
- How a TargetADS gets its Target data, and which fields come from which side.
- Why the library always sends ForceIncludeSelf True.
- The path forms AMP's file manager takes.
- ForceIncludeSelf False still sends a local Target that holds game Instances, on a Controller or a hybrid.
- The endpoint shapes confirmed on the VMs, and `sanitize_path` refusing underscores.
- Generic Instances stay a plain Instance.
- A new Instance takes the default auth server of the ADS that receives the create call, and the Controller's is
  localhost after `ampinstmgr quick`.
	- Sending the create through the TargetADS, or setting the Controller's default to its own URL, fixes it.
	- ApplyInstanceConfiguration repairs one Instance through the API; AccessMode changes nothing.
	- A user created through the TargetADS lives only on the Target.
- Generic Instances: modules, the shared extra API sections, Void replies and `config_version`.
- The wrapper parameter gaps against the 2.8.0.8 spec.
- CreateInstanceFromSpec ignores the Target's DefaultAuthServerURL, and GenericModule diagnostics add config_version.
- An Instance goes through the ADS that holds it, checked live with same-named Instances on vm1 and vm2.
- The Controller's copy of a Target's Instances is never converted, and a stopped Target leaves an empty TargetADS.
- The library only talks to the Controller's URL, and every AccessMode keeps its calls working.
	- Calls to an Instance fail with "Instance Unavailable" for a few seconds after restart_instance.
- A TargetADS reaches its Target, and its get_instances gives the right target_id.
- A Target's game Instances carry the Controller's ADS ID as `target_id` when relayed by the Controller.
- "Instance" and "URL" in prose.
- "ID", "GUID", "Instance"; the RepairAuth role answers in backticks.
- Same wording, and get_instance on the Controller's own id now says it returns self once the id is known.
- StartInstance("ADS01") sent to the Controller acts on the Controller's own ADS01; Instance's self-acting start/stop/restart go through the Controller by name, so on a TargetADS they hit the Controller.
- GetModuleInfo gives the logged-in ADS's own id and is_remote_instance (True only on a Target).
- New "Non-admin users" section: what a user with no roles can call, and that Targets refuse them on Professional.
- Nothing in GetInstance, GetInstances or GetTargetInfo names an ADS's role; ADSModule.ADS.Mode does, and is_remote from a Controller.
- Creating an Instance needs NewInstanceKey on the ADS that runs it; CreateInstance needs a Guid NewInstanceId and an AdminUsername.
- The Target's Instances log in through the Target's ADS, which fails; ampinstmgr --RepairAuth points the ADS and every Instance at the Controller.
- A Minecraft Instance on the Target comes back as a MinecraftInstance from both sides, and proxied formatted reads work.
- A paired Target needs the Controller as its auth server, and the Controller needs passthru auth, or polls fail with "Token Rejected".
- New "Controller and Target data" section: what GetInstances / GetInstance return on each side, and what ForceIncludeSelf False drops.
- The KVM test VMs: what `.scripts/vms.py` manages, the getamp.sh unattended-install gotcha, and setting the ADS mode before pairing.
- `sanitize_json` is not safe to run twice on keys, and where it runs.
- Key drift usage now lives in CONTRIBUTING.md.
- How to run the key drift check.
- Added AMP's key drift between versions and the per-instance-type metrics to "Dataclasses vs. the raw JSON".
- Added a "Captured responses" section: how to capture, the shapes not yet confirmed live, the failed-login payload and the doc generators' repo-checkout limit.

## TODO.md
- Removed #44.
- Added #44, the `ActionResult` form of a dead session.
- Removed #43.
- (#43) update_datastore and add_datastore send snake_case keys AMP reads as a datastore with no name.
- Removed #41.
- Added #41: json_to_typeddict writes invalid code for a root dict whose keys aren't identifiers.
- Removed #37.
- Added #37, an opt-in wait on create_instance's RunningTask.
- Even spacing between the sections.
- Removed #33.
- Added #33, to put the classes of `base.py` in alphabetical order.
- Removed #4, #7 and #13.
- Removed #32.
- Added #32 for the push events #30 captured.
- Removed #29 and added #30, the VM repairs for the remaining captures.
- Removed #26, #27 and #28, and added #29.
- Removed #25.
- (#25) `get_remote_login_token` sends `IsTemporary` as null.
- (#26) `Messages.parameters` depends on the message type.
- #20 done.
- #20 added.
- #18 done.
- #18, the stored session when AMP's side of it dies.
- #11 done.
- Removed #6, confirmed live.
- #6 needs an Instance with Analytics and user-specific data enabled.
- Removed #5, confirmed live. #6 notes that AMP still answers null with a player online.
- Removed #9.
- Added #17, orjson as an optional extra.
- Removed #16.
- Added #16, the raw dicts left in responses.
- Removed #1 and #8.
- Removed (#14), done.
- (#14) Mark per-object changes with Sphinx version directives.
- Dropped #2 (vms.py role at install) and #10 (every endpoint method names its endpoint).
- Each open item has a `(#N)` reference, tracked with its type and status in `.local_data/plans/todo_index.md`.
- Dropped the #10 item.
- The item is now to remove `create_local_instance`, or fix it once AMP's shape is known.
- Dropped the `sanitize_path` underscore item.
- Dropped the items this batch finished, reworded the open confirmations, added the `sanitize_path` underscore item.
- APIParams / Bridge don't strip a trailing slash from the URL.
- Dropped the GenericModule/SteamCMD item, added the parameter gaps.
- `create_local_instance` sends the wrong shape, and GenericModule and SteamCMDPlugin have no wrappers.
- Dropped the util.py `instance.instances` item.
- Dropped the routing item, and noted util.py's loops over `instance.instances` miss a Target's Instances.
- Route by the Target that lists the Instance.
- "Impliment" -> "Implement".
- Dropped the PostCreateActionsState item.
- Dropped the duplicate member docs item.
- Dropped the items this batch finished; added `PostCreateActionsState` not matching AMP, and the shapes left to confirm.
- Dropped the version_validation item.
- Added the check_code.py findings left in backoff.py, emailsender.py and filemanager.py.
- "URL" in prose.
- "GUID".
- Same wording.
- Dropped get_instance on the Controller's own id (it now returns self).
- Added planning what else TargetADS should mirror from Controller.
- Route Instance's start/stop/restart to the ADS in the row's target_id.
- _reauth's login error should name AMP's known result codes (5 is NoInstanceAccess).
- get_permissions_spec takes no format_data and passing it raises a bare TypeError.
- Dropped the cache guard and `include_self` doc items.
- Controller._initialized is only set when built with data, so the cache guard never runs on Controller(bridge=...).
- sanitize_json mangles dotted keys in deployment_args.
- create_instance raises AMPAPIKeyError on success (AMP 2.8 answers with a RunningTask).
- CreateInstance defaults AMP rejects: new_instance_id and admin_username.
- .scripts/vms.py: set the ADS role at install time with ampinstmgr --RepairAuth.
- ampapi/instance.py: get_instances(include_self=False) leaves self unpopulated, get_instance on the Controller's own id returns a TargetADS, hybrid ForceIncludeSelf unchecked.
- Docs: Base.instance_id docstring default and login claim.
- The eight remaining Minecraft methods return nothing, a bool or a str, so they need no TypedDicts; the real issue is `mc_reject_eula` returning None.
- `get_tasks` names no TypedDict, so the check cannot cover it.
- Removed the `_reauth` item.
- Entries are one-line tasks; the findings and history behind them moved to NOTES.md.
- Removed the duplicate `Methods.consumes` entry and the local dump path.
- `add_datastore` is a concrete task now: switch to `to_dict()`.
- The `Backup` shape and `Instance.metrics` keys are confirmed against AMP 2.8.0.8.
- Removed the `call_end_point` item.
- Removed the `get_oidc_login_url` item.
- `Updates.console_entries` is converted.
- `InstanceResponse.metrics` keys are unconfirmed.
- Added moving `find_parameter_mismatches` to url matching.
- Removed the regenerate-report item.
- Updated the missing wrapper lists to match the new report.
- Removed the landed code blockers (installed import, PR #27, narrowing, `cast`, util.py pyright, OIDC parameter, docstring names).
- Added the follow-ups found during the fixes.
- Removed the release blockers that landed (packaging, docs build, changelog generator, docs names).
- Added the remaining doc page and duplicate-member notes.

## sanitize_json is only for the raw spec dumps


## core.py *w/Claude
- `get_api_spec` takes `sanitize_json`, for `util.py`'s raw spec dumps.
- edit_interval_trigger checks each list with a plain loop per range, below Kat's commented-out checks.
- get_settings_spec splits categories and modules in one loop instead of two dict comprehensions.
- set_configs builds its data dict in a loop.
- The "uniquely identifies" union comments read "Only X has key".
- oidc_login returns a LoginResults and keeps a shorter TODO for the unconfirmed success payload.
- set_config and set_configs send a list, tuple or dict value as a JSON string, and the hints take bool and int.
	- Live check on AMP-2.8.0.8: AMP takes a JSON bool and int as they are, so those are not converted.
- Removed the set_configs TODO.
- A parameter left as None isn't sent, and AMP takes its default.
	- AMP rejected the null `IsTemporary`, so the call failed without `is_temporary`. The old line stays commented out.
- `build(X, data)` calls (70) are `X.from_response(data)`.
- `build` is no longer imported from `.modules`.
- `get_user_list` treats AMP's empty list answer as no players (an empty `Players`, `{}` raw).
- `get_configs` and `get_provision_spec` raw arm is `list[SettingSpecResponse]`.
- `get_api_spec` returns `APISpec` and `get_user_action_spec` returns `ActionSpec`.
- `get_structured_diagnostics` and `get_permissions_spec` take `format_data` and return their dataclasses.
- `get_module_info` is annotated `modules.Module`, since `Module` now resolves to two documented classes.
- Follows the TypedDict renames.
- `get_structured_diagnostics` returns `StructuredDiagnosticsResponse`.
- Added `add_interval_trigger`, taking the Int32 lists AMP expects.
- Added `convert_user_to_oidc`, `update_oidc_sub` and `revert_user_from_oidc`.
- Added `sleep` and `update_tools`.
- Added `get_structured_diagnostics`, returning the raw dict until the shape is confirmed.
- `get_webserver_metrics` raises the `RuntimeError` from `version_validation` instead of returning it, and documents it under Raises.
- `get_api_spec` is annotated `dict[str, Any]`, which is what it returns.
- `get_tasks` returns `list[RunningTask] | list[RunningTaskResponse]`, each item narrowed with the RunningTask keys.
- Replaced the `Core/ActionResult` label in 38 narrowing errors with each method's own endpoint URL.
- `get_triggers` keeps `Core/GetScheduleData`, which is the call it makes.

## docs/upgrading.rst
- Noted `get_api_spec`'s `sanitize_json`.
- Noted the datastore key names.
- Notes that every Enum is exported from `ampapi`.
- The Enum links point at `ampapi._enums`, where the docs define them, so they resolve.
- The `take_backup` bullet says when it returns an `ActionResult`.
- A note for each change.
- The new InstanceInfo fields, the oidc_login state parameter and the new keyword-only parameters.
- The two removals, and create_local_instance dropped from the PostCreateState note.
- Added the two messages to the `Messages.parameters` bullet.
- Noted that `deploy_template` sends AMP's parameter names and returns a `RunningTask`.
- Noted that `InstanceInfo` needs only `instance_id`.
- The `Messages.parameters` sub-bullets are a nested list, not a definition list.
- The `update_instance_info` bullet says it returns a `RunningTask`.
- Added a bullet for the new `ip_binding` default.
- Added a bullet for `update_instance_info` sending AMP's parameter names.
- Reworded the `Messages.parameters` bullet to say what it holds per message, and noted the two new classes.
- Noted the fix under "Changed methods".
- Response dataclasses inherit `ResponseData`, and `from_response` builds one with its nested dataclasses.
- `DeploymentTemplate` is a dataclass that logs an unknown key instead of raising.
- `TimedTrigger.tasks` is a list of `TriggerTasks`.
- `id`, `input` and `platform` don't link to Python's builtins. They are AMP field and argument names, written `!name`.
- Names take single backticks, literal values keep double ones.
- Two semicolons replaced with full stops.
- The two return changes and ActionResult.result.
- Errors: a dead session is logged in again and the call sent once more, and "Instance Unavailable" no longer forces a new login.
- Two notes reworded.
- The rename, the two removals and TargetADS.upgrade_instance.
- restart_amp no longer raises on an Instance that is not an ADS.
- Noted the `run_security_check` return and the `Pass` to `passed` key.
- Noted the five ActionResult returns and the two Void returns.
- Noted that methods returning None now raise on an AMP failure.
- Noted the new `display_name` and the 4.x TypeError.
- Noted that response dataclasses have no `__dict__`, take no extra attributes and can't be weakly referenced.
- Notes for `TriggerTasks.parameter_mapping` (raw dict) and `RemoteTargetInfo.datastores` (`TargetDatastore`).
- Notes for `get_setting_spec`, `get_webauthn_credential_ids`, `take_backup` and the `Instance` response parameters.
- The `dataclass-wizard` note says unknown keys were already dropped in 4.x and are now logged once, and is rewrapped.
- Noted that `dataclass-wizard` is no longer a dependency and that unknown keys are dropped and logged.
- `Instance.url` is `Union[str, None]` with a None default, and null Instance fields hold their documented default.
- Noted the TargetADS Target data and the in place `get_instances` updates.
- `create_local_instance` is deprecated.
- `get_instances` no longer takes `include_self`.
- `sanitize_path` no longer refuses `_`, rewrites `..` or strips a leading `.`.
- `include_self=False` only leaves the Controller's data unset when its local Target holds nothing but its own ADS.
- `Instance` has the Generic endpoints instead of a new `GenericInstance`.
- `apply_instance_configuration` joins the methods that return a `RunningTask`.
- Noted that Generic Instances now come back as `GenericInstance`.
- `create_instance_from_spec` returns a `RunningTask`.
- Dropped the `route_by_target` mention, which never existed in 4.x.
- Replaced the routing bullet with the `Instance.ads`, `Controller.targets` and `Controller.get_instance` changes.
- Notes the removal and what to use instead.
- Routed start/stop/restart and `route_by_target`, `get_provision_fitness` returning None, `DeploymentTemplate.setting_mappings`, the fixed `version_validation`, and dotted keys keeping AMP's spelling.
- Added notes for the `create_instance` return type, `mc_reject_eula`, the `CreateInstance` defaults, `version_validation` / `get_webserver_metrics` raising and the `clean_up` `logout` option.
- Moved modules: util is no longer star-imported; use `from ampapi import util`.
- Errors: every error class imports from `ampapi`.
- Renamed classes lists `APISPecEndpointData` -> `APISpecEndpointData`.
- "ADS ID".
- Same wording in the Returned data and Target ADS sections.
- Target ADS section wrapped like the rest of the page, and its last sentence split.
- `get_instance` on the Controller's or a Target's own ADS id returns that object itself.
- `TargetADS.get_instances` and `TargetADS.instances`.
- `TargetADS` gains the ADSModule methods.
- `start_instance`, `stop_instance` and `restart_instance` on `TargetADS` now take an `instance_name`.
- Controller attributes raise until `get_instances()` runs and warn once older than 300 seconds.
- Added the get_instances change; 4.x returned an `AMPADSInstance` for every ADS row.
- Added the `call_end_point` rename.
- Added `User` -> `UserInfo` and the five renamed attributes (`Base.url`, `FileChunk.base_64_data`, `InstanceDatastore.sanitized_name`, `Module.end_point_ur`, `PortInfo.us_user_defined`).
- Added a Changed methods section: the removed `Base` dataclass helpers, `login`'s `remember_me`, `get_oidc_login_url`, the dropped `format_data` parameters and `Bridge.api_params`.
	- Each one checked against `main` (4.6.0) with a public API diff.
- Added a Returned data section: `Updates` lists and `Status.metrics` are dataclasses now, where 4.x left them as dicts.
- Added `Metric` -> `Metrics`.
- New page listing what 5.0.0 changed from 4.x: requirements, renamed classes, moved modules and errors.

## The datastore calls send AMP's key names (#43)


## modules.py *w/Claude
- `InstanceDatastore.to_dict()` sends the keys AMP's panel sends (`FriendlyName`, `SoftLimitMB`, ...), not the attribute names.
	- The snake_case keys saved a datastore with no name, and the ADS then crashed on every start.
- `_dataclass_to_dict` is commented out, since nothing uses it.
- CreateInstance.instance_name and port_number are required and follow module.
	- Their "" and 8001 defaults are commented out above.
- Removed the to_dict check that raised a ValueError for an empty instance_name with auto_configure False.
	- A remote Target names an Instance with an empty name itself (p37empty01), and create_instance's wait raises for a local one.
- The class note and the auto_configure docs say AMP keeps a given name and picks the port (measured on vm1).
- CreateInstance.to_dict raises a ValueError when instance_name is empty and auto_configure is False.
	- AMP took that call and only reported it through the failed RunningTask (measured on vm1).
- The CreateInstance note and instance_name docs say what AMP refuses and what it picks with auto_configure.
- SettingSpec.current_value takes dict[str, str], and the Enum conversion skips a bool.
- Removed the LoginUserInfo.last_login TODO.
- AnalyticsSummary.country_data and top_players, and SettingSpec.actions, attributes and selection_source, accept the dataclass or the raw TypedDict, the dataclass first.
- BuildInfo docstring names its real users and lists major_revision.
- BukkitPlugin docstring says tested_versions.
- SettingSpec.actions is list[SettingSpecAction], so from_response builds SettingSpecAction instead of keeping dicts.
	- list[str] came first in the union and accepted every list.
- SettingSpec.current_value gains None and holds list[str]; meta, placeholder and suffix gain None.
- SettingSpec.min_value and max_value are int, float or None.
- DeploymentTemplate setting_mappings, tags and zip_overlay_path gain None.
- UserInfo.email_address is str or None; TriggerTasks.created_by gains None.
- TimedTrigger.enabled_state is int, as AMP sends 0 or 1.
- ProvisionSettingInfo.default_value also takes a list.
- AnalyticsCountryData.session_time_percent and AnalyticsTopPlayers.percent also take the string "Infinity".
- Version directives on each public type that differs from 4.6.0.
- New `AppSummary` dataclass for `ADSModule.get_supported_app_summaries`, with the 13 keys AMP sends.
	- It was built as an `Application`, which filled `module_name`, `settings` and `is_multi_ip_aware` with made-up defaults.
- `Application.module_name` is required again, as in 4.6.0; `get_supported_applications` sends it in every entry.
- `Application`'s docstring names `ADSModule.get_supported_applications` and lists `deprecated_reason`, `is_multi_ip_aware` and `resource_usage_info`.
- Removed the temporary `build` forwarder. Every caller uses `Cls.from_response(data)`.
- `TimedTrigger.tasks` has a `versionchanged` directive for the list built from AMP's dict.
- `TimedTrigger.from_response` turns AMP's `tasks`, which is keyed by task ID, into a list of `TriggerTasks`.
	- Every `GetTimeIntervalTrigger` capture sends a dict. The `__post_init__` removed in phase A made it a list of the ID strings.
- `from_response` reads the plan cache before calling `_build_plan`, and a nested class's `from_response` is bound once when the plan is built.
	- Updates 210 to 199 us and Status 30.8 to 29.4 us per call against `build` at 2785a7a. Phase A alone was 4% slower than `build`.
- Added the `ResponseData` base class, with `__slots__ = ()` so the slotted subclasses keep no `__dict__`.
	- It owns `from_response`, which is the old `build` body with the same unknown-key warning.
	- `_reported_unknown_keys` and the per-class build plan cache are `ClassVar` state on it.
	- `_converter` is a static method and `_field_types` is folded into `_build_plan`, so `functools` is no longer imported.
- Made the 67 response classes inherit `ResponseData`, including `Fitness` and `DeploymentTemplate`.
- Kept `build` as a one-line forwarder to `from_response` until the callers are converted.
- Removed the nested builds from `__post_init__` in `LoginResults`, `Status`, `Updates` and `TimedTrigger`.
	- `Status` keeps its `InstanceState` conversion.
- Moved the `SettingsSpecParent` nested builds into a `from_response` override, which builds `modules` after the base.
- Turned `DeploymentTemplate` into a `slots=True` dataclass built with `from_response`.
	- The hand-written class stays commented out above it.
	- Corrected the `zip_overlay_path` docstring type to `str`.
- New `RoleMember` dataclass (`id`, `name`), added to `__all__`.
- `Role.members` is `list[RoleMember]`, it was hinted `list[str]` but AMP sends `{id, name}` objects.
- `build` works out each class's field names and one converter per field once, instead of reading the type hints per value.
	- `_convert` replaced by `_converter` and `_build_plan`.
- `Consumes.enum_values` is `Union[dict[str, str], None]` and defaults to None (was a `str` arm and "").
- `SettingSpec.enum_values` is `Union[dict[str, str], None]`.
- `Diagnostics.hardware_platform` and `network_mode` are `str`, `Module.feature_set` is `list[str]`.
- New dataclasses: `AnalyticsGraphData`, `Branding`, `Uptime`, `MessageParameters`, `StructuredDiagnostics` and `PermissionNode` (recursive).
- `AnalyticsSummary.busiest_time`, `quietest_time` and `graph_data` hold `AnalyticsGraphData`.
- `Module.branding` is a `Branding`.
- `Messages.parameters` is a `MessageParameters`, `state` converts to `InstanceState` as `Status.state` does.
	- Removed the stale comment about the metrics carrying a different key set than `Metrics`.
- `Application` builds the `get_supported_app_summaries` entries: `module_name` is defaulted (moved below the required fields), `settings` is `dict[str, str]`.
- `__all__` lists all 68 public classes bar `Module`, which stays out because `ampapi._enums.Module` is the one exported as `ampapi.Module`.
- `# noqa: D105` and `# noqa: D107` on the magic methods the wider `__all__` brings under those rules.
- Docstrings for `SettingSpecTable` and `UserApplicationData`, which autodoc skipped without one.
- `ParameterMapping.__post_init__` converts `operation` to `IfOperators`, `priority` to `MailPriority` and `when` to a naive `datetime`.
	- A value that doesn't parse stays the string AMP sent; an empty string becomes None.
	- `when` tries ISO first, then the `%m/%d/%Y %H:%M:%S` form AMP rewrites a value with seconds into.
- `DCConsumes` is now `Consumes` and `DCParameterMapping` is now `ParameterMapping`.
- Fixed the stale `state`, `operation` and `priority` docstrings.
- `DCParameterMapping` converts its typed arguments from AMP's strings in a new `__post_init__`.
	- Booleans ("true"/"false" in any case), ints, floats and `state` (to `InstanceState` by its number).
	- An empty string in those fields becomes None. A value that doesn't parse stays the string AMP sent.
	- The field groups are `ClassVar` tuples, so `build` still skips them.
- Field hints and docstring types widened to `Union[<type>, str, None]`.
- `AnalyticsCountryData.sessions_percent` is required and replaces `session_percent`, which AMP never sent.
	- The old field is kept commented out.
- `DCParameterMapping` declares the 62 arguments of every task method in AMP 2.8.0.8, each `Union[str, None]`, default None.
	- Names are the snake_cased `consumes` of `get_schedule_data`'s `available_methods`; each docstring names the methods that take it.
- `TriggerTasks.parameter_mapping` is `DCParameterMapping | ParameterMapping` and is built by `build`.
- `APIParams` strips a trailing `/` from `url`, so every URL built from it is right.
- Added `FolderUploadFile` (`relative_path`, `data`) with `to_dict()` giving AMP's `RelativePath` and `Base64Data`.
- DeploymentTemplate: attribute `settings_mappings` is now `setting_mappings`, and the null-able fields are typed so.
- TimedTrigger: added `last_executed`, default None.
- `CreateInstance.new_instance_id` defaults to the zero GUID, which lets AMP pick the ID.
- `CreateInstance.admin_username` defaults to "admin".
- `CreateInstance.admin_password` defaults to a generated `secrets.token_urlsafe(18)` value.
	- AMP rejects an empty username or password, and the generated password is ignored when `auto_configure` is True.

## adsmodule.py *w/Claude
- `update_datastore` runs a raw `InstanceDatastoreResponse` through `InstanceDatastore` to get AMP's names.
- `add_datastore` and `update_datastore` have their version directives.
- get_mode uses try/except ValueError in place of contextlib.suppress.
- update_datastore builds its data with an if/else block.
- _wait_for_task has a one line docstring.
- _wait_for_task and the create_instance wait block have blank lines between their steps, and a comment on the success case.
- The calls in them pass keyword arguments, and the TimeoutError is bound as e.
- create_instance takes a keyword-only wait (default False) and wait_timeout (default 300 seconds).
	- With wait, it polls Core/GetTasks once a second and raises AMPAPIResponseError when the task fails, or TimeoutError after wait_timeout.
	- AMP drops a task that succeeds from the list and keeps a failed one with its reason (measured on vm1).
- Added _wait_for_task above create_instance.
- `get_supported_app_summaries` returns `list[AppSummary] | list[AppSummaryResponse]`.
- `build(X, data)` calls are `X.from_response(data)`.
- `get_deployment_templates` builds `DeploymentTemplate.from_response(entry)`, the old call left commented out.
- Dropped `build` from the `.modules` import.
- `get_datastore_instances` is annotated and documented as returning the raw `list[InstanceResponse]`.
- `get_supported_app_summaries` takes `format_data` and returns `Application`.
- `get_group` returns `ControllerResponse` or None (`allow_null`).
- `servers` docstring warns it is AMP's proxy route and fails as an endpoint.
- Added `clone_instance`, returning a RunningTask.
	- `post_create` takes PostCreateState, the enum whose values match the spec's PostCreateAppActions.
- Added `get_instance_live_settings`, returning a dict of setting node names and values.
- Added `prepare_file_transfer`, returning an ActionResult.
- get_provision_fitness: returns None when AMP answers JSON null instead of raising.
	- Only the "JSON returned <None>" AMPAPIResponseError is caught, every other error is raised.
- `add_datastore` sends `new_datastore.to_dict()` like `update_datastore`, and the TODO about verifying the conversion is gone.
- `create_instance` returns `RunningTask | RunningTaskResponse`, narrowed like `delete_instance`.
	- AMP 2.8 answers with a RunningTask that carries the ActionResult keys.

## The datastore payload bug the #42 live check found is written down


## unit_test.py
- The rewritten capture comments read as full sentences.
- The 12 em dashes are gone, the skip messages read "..., run capture_responses() first".
- Dropped "without cast" from the test docstrings and the "(#31)" capture comment.

## The util, key drift and TypedDict comments read as Kat's (#42)
- No VM, capture or measurement references, shorter comments in her voice.

## util.py *w/Claude
- One _node_endpoint_urls walk serves _get_endpoint_urls and find_parameter_mismatches, in place of two copies.
- One line docstrings on the private helpers.
- Commented out the srcds branch and its src_ flag, since AMP 2.8 has no srcds module.
- Removed the TODO about .rst spec sheets.
- `str_sanitizer_sphinx` keeps the special character and wraps it in a literal up to the next space (`a *b c` -> ``a ``*b`` c``).
	- It dropped the character before, which left a stray closing literal in the generated Setting Nodes page.
	- A literal still open at the end of the string is closed.
- The two `generate_docs_rst` handlers log with `logger.exception`, so the traceback reaches the log.
	- They passed `traceback.print_exc()` as an argument, which printed to stderr and logged "None".
- Added the GPL header the other modules carry.
- `_wildcard_nodes` is split over two adjacent literals to fit the line length; its value is unchanged.
- The `# TODO -` comment uses the colon form.
- The `docs.samples` imports are marked `# noqa: PLC0415`, as `docs/` is not part of the package. The first one already was.
- The two `except Exception` catch-alls in the docs generator are marked `# noqa: BLE001`, so one failed page doesn't stop the rest.
- Removed the two `index = index` self-assignments.
- `str_sanitizer_sphinx` documents `special_chars` and builds each character in `piece` instead of rebinding the loop variable.
	- Its output is unchanged.
- Pyright suppressions adjusted for the typed API spec.
- Reads the permission nodes raw (`format_data=False`) and types them `PermissionNodeResponse`.
- Follows the TypedDict renames.
- The original `amp_api_update` version check and `find_parameter_mismatches` method lookup are kept commented out above their rewrites.
- `find_parameter_mismatches` matches spec endpoints to Python methods by the URL they post to, like `find_missing_endpoints`.
	- Compares only the newest spec version directory (int tuples) instead of a merge where the oldest won.
	- `request_params` joins `_PYTHON_ONLY_PARAMS`.
	- The report links are relative to the report.

## _types.py
- The key set notes and TypedDict docstrings keep the facts without the capture counts.
- OPWhitelistResponse has the same directive.
- The OP whitelist keys' TODO is now a note that the endpoint was removed, so they come from the OPWhitelist dataclass.
- `AppSummaryResponse` builds `AppSummary`.
- The TypedDicts are in alphabetical order, which moved 19 of them.
	- `APISpec` stays right below `APISpecEndpointData` and `APISpecEndpointParameters`, as it is built from them at import.
- The commented-out `AvailableTriggersResponse` sits above `TriggersResponse`, which replaced it.
- `TimedTriggerResponse.tasks` is a dict of `TriggerTasksResponse` keyed by task ID, as AMP sends it.

## key_drift.py
- One line docstrings on the private helpers, shorter comments.
- 2 blank lines.
- 10 blank lines.
- `LOGGER` sits right after `__all__`, above the module constants.

## __init__.py
- Shorter noqa comment.

## The session, cache and Instance comments read as Kat's (#42)
- No TODO numbers or change history, shorter comments in her voice, no semicolons in runtime strings.

## base.py
- The unbounded RuntimeError retry is a TODO instead of a "#18" note.
- _login_failed, _stale_cache and the key drift log read without semicolons.
- One line docstrings on _snake_key, _plural_acronym_repl and the cache helpers.
- 10 blank lines.
- 8 blank lines.
- Removed `BaseArgs`, which nothing used.
- The TypedDicts that type `Base`'s parameters are in alphabetical order above it: `BaseArgs`, `DumpParameters`, `ResponseHandlerOptions`.
- `_SessionDeadError` stays right above `Base`, its only user.
- Docstring names take single backticks.
- The `_post` note says it calls `login` again.
- `sanitize_path` carries `.. versionchanged:: 5.0.0`.
- Trimmed the `generic_only` and `sanitize_path` notes, restored the original `_call_end_point` note.

## instance.py
- The TargetADS start, stop, restart and upgrade versionchanged notes say what they act on now.
- get_instance's ValueError reads as a flat constraint.
- 1 blank line.
- 2 blank lines.
- 4 blank lines after the format_data block.
- The port directives say what changed, not why.
- port is documented as an int in the three Instance docstrings.
- Three names in the `Controller.get_instances` docstring take single backticks.
- The bases `ADSData` and `Instance` come first, then `Controller`, `MinecraftInstance` and `TargetADS`.
- `Controller.instances` and `TargetADS.start_instance`, `stop_instance` and `restart_instance` carry `.. versionchanged:: 5.0.0`.
- `Controller.targets` carries `.. versionadded:: 5.0.0`.
- Trimmed the `ads` routing notes on `Instance`, `ads` and the start, stop, restart, update and status calls to what they do.
- `ADSData` and `TargetADS` notes reworded, the "no longer" wording is gone.
- `TargetADS.url` is documented as `Union[str, None]`, matching `ADSData`.
- `Controller.get_instances` and `TargetADS.get_instances` summaries no longer list `TargetADS` in the returned set.
- Renamed `TargetData` to `ADSData`.
- `get_instances` docstring: `include_self=False` only drops the local Target when it holds just the Controller's own ADS.

## The response dataclasses' comments read as Kat's (#42)
- No capture, server or version-history references, shorter comments in her voice.

## modules.py
- "Its meaning is unconfirmed" / "Only seen as null" fields are UNK.
- InstanceInfo and InstanceUpdate attributes end "default is None.", the class note says None isn't sent.
- The bare "intentionally unhashable" docstrings are a comment above `__hash__ = None`.
- The unknown-key warning reads "We encountered an unknown key %r on %s and left it out."
- One line docstrings on the private helpers.
- 9 blank lines.
- OPWhitelist has the same directive.
- BuildInfo's docstring names Diagnostics.application_version, which is where it is built.
- SettingSpec.actions keeps one commented-out line, the hint from before this batch.
- The SettingSpec.current_value directive says what changed, not why.
- Relative imports come before the `if TYPE_CHECKING:` block.
- `LOGGER`, `SettingSpecTableAliases` and `_reported_unknown_keys` sit after `__all__`, above every function.
- The `build` helpers moved up with the other functions, above every class.
- Classes are in alphabetical order. `Consumes`, `ParameterMapping`, `FolderUploadFile`, `Uptime`, `PortInfo`, `TargetDatastore`, `SettingSpecSelectionSource`, `SettingSpecTable`, `UserInfo` and `BuildInfo` moved.
	- No code changed. The only text change is single backticks around `__repr__` in the `BuildInfo` note.
- Single backticks in the `APIParams.url` docstring.

## The plugin modules' comments read as Kat's (#42)
- No VM, date or measurement references, no "which leaves AMP's default" tails, shorter comments.

## minecraft.py
- The 16 deprecated bodies read "Removed in AMP v2.6.5.0.", matching the decorators.
- The 16 deprecated methods warn "Removed in AMP v2.6.5.0", and the TODO above each decorator is gone.
- The other 15 methods marked Removed in AMP API 2.6.5.0 have a deprecated directive naming their removed endpoint.
	- The OP list and whitelist methods, the mc_buk_* plugin methods and mc_get_head_by_uuid.
- mc_get_op_whitelist has a deprecated directive saying GetOPWhitelist was removed in AMP 2.6.5.0.
- 21 blank lines.

## generic.py
- Imperative docstring summaries.
- 6 blank lines.

## steamcmd.py
- Imperative docstring summaries, one comment for the lowercase module name.

## filebackup.py
- The DirtyOnly note sits once in Returns.
- 2 blank lines.
- 12 blank lines.

## filemanager.py
- Shorter notes, no measurement reference.
- 39 blank lines.
- Removed the release_file_upload_lock TODO and noted that AMP answers success whether or not a lock was held.
- `write_file_chunk` carries `.. versionchanged:: 5.0.0` for the `append` -> `final_chunk` rename.
- `final_chunk` reads "If this is the last chunk of the file or not", trimmed the `append_file_chunk` warning.

## analytics.py
- Shorter notes on get_user_details.
- 5 blank lines, the wrapper spacing from 07be36b.

## emailsender.py
- Shorter noqa comment.
- 2 blank lines.

## Comments in core.py read as Kat's (#42)
- No process or history references, shorter comments in her voice, no "which leaves AMP's default" tails.

## The test and dump scripts read as Kat's (#42)
- Em dashes, process references, `# *` markers and banners removed; comments shortened.

## controller_dump.py *w/Claude
- Plain comments in place of the `# *` markers and dashed banners, shorter docstrings.
- Copyright line, D107 noqa and three pyright ignores, so check_code passes on the whole file.
- Added a stdlib-only script to dump Controller responses into `_responses/`.

## The densest remaining blocks get blank lines between their steps
- A second pass over runs of statements with no break, eg. _permission_node_parse's three index branches. Only blank lines changed.

## util.py
- 16 blank lines.
- 5 blank lines.

## adsmodule.py
- 2 blank lines.
- 101 blank lines.
- Blank lines between the narrowing checks and returns in `add_datastore`, `apply_instance_configuration` and `apply_template`.
- Permission nodes take single backticks.
- Shortened the `get_mode` and `get_provision_fitness` notes.
- `get_group` documents `group_id` as the Target's ADS ID (checked on the VMs, the numeric `id` is refused).
- Trimmed the `get_instances` and `get_group` notes, the reasons stay in NOTES.md.

## The helpers and the files the wrapper pass missed share the library's body spacing
- Blank lines after guard clauses and blocks, to the CODING_STYLE.md section 21 rates. Only blank lines changed.

## core.py
- 4 blank lines.
- get_webserver_metrics warns "Removed in AMP v2.6.0.0".
- 58 blank lines.
- The set_config and set_configs docstrings spell out the value types instead of the unexported alias.
- `get_webserver_metrics` names the AMP version it was removed in, `AMP-2.6.0.0`.

## bridge.py
- 1 blank line.

## Deprecation warnings name the AMP version as vX.X.X.X, since "AMP API" read as this library


## unit_test.py capture helpers call get_instances without include_self


## unit_test.py *w/Claude
- capture_ads_responses and capture_instance_responses no longer pass include_self, which get_instances dropped.
	- get_instances always sends ForceIncludeSelf now, so the old call raised a TypeError.
- The UserInfo, Diagnostics and Module key tests let a 2.6.5 capture lack a field when the dataclass gives it a default.
	- oidc_sub, config_version and local_login_enabled came with newer AMP versions, and each has a default.
- The ActionResult field test expects support_url and support_title.
- The ScheduleData tests build it from the response and compare against its __slots__, since it isn't a dataclass.
- `_response_dir` points at `_responses/2.6.5/ads`, where its captures are since #31.
- Added the live-instance response capture tests moved out of `local.py`.

## unit_test.py matches the 5.0.0 response classes


## Every method AMP removed in 2.6.5.0 says so in its docs


## upgrading.rst
- One bullet lists all 16 deprecated MinecraftModule methods with OPWhitelist and OPWhitelistResponse.
- mc_get_op_whitelist, OPWhitelist and OPWhitelistResponse are deprecated.
- The CreateInstance note covers the required fields instead of the ValueError.
- A note for create_instance's wait.
- A note for the CreateInstance check.
- Notes for the oidc_login return and the set_config value conversion.
- The hints note is a nested list, with each field linked to its class.
- One note listing the fields whose hints changed against 4.6.0.
- Note for `Role.members`.
- Note for the `APISpec` and `ActionSpec` shapes.
- Note for `Consumes.enum_values`.
- Notes for the new dataclasses and the changed attribute types.
- The TypedDict rename note names 4.x's `types_` module and says `Consumes` / `ParameterMapping` are now dataclasses.
- Listed the `DCConsumes` and `DCParameterMapping` renames, the TypedDict renames and the extra converted `ParameterMapping` fields.
- `DCParameterMapping` bullet notes the conversion.
- Rename note.
- `DCParameterMapping` note replaces the raw-dict one.
- Notes for `get_group`, `write_file_chunk` and the trailing slash.
- The routing note says to set `route_by_target` on the Controller or an Instance.

## The OP whitelist is marked deprecated, since AMP removed GetOPWhitelist in 2.6.5.0


## json_to_typeddict writes valid code for any JSON keys


## json_to_typeddict names colliding classes apart and marks missing keys NotRequired


## The endpoint wrappers share one spacing
- Every wrapper has a blank line after its type guard and after its format_data block, as create_instance has.
- A blank line sits before the _post call when a block of parameter checks ends right above it.

## The create_instance wait reads like the rest of the library


## CreateInstance requires a name and port instead of checking for an empty name


## create_instance can wait for its creation task


## CreateInstance refuses an empty name it can't use


## The older TODO notes are settled


## Review of the nested TypedDicts


## Key drift sees inside the Analytics and SettingSpec lists


## _types.py *w/Claude
- Added AnalyticsCountryDataResponse, AnalyticsTopPlayersResponse, SettingSpecActionResponse, SettingSpecSelectionSourceResponse and SettingsSpecAttributeResponse, shaped from the 2.8.0.8 captures.
- AnalyticsSummaryResponse.country_data and top_players, and SettingSpecResponse.actions, selection_source and attributes, now use them instead of list[Any] and dict[str, Any].
- Matched the TypedDict hints to the captures.
	- SettingSpecResponse, UserInfoResponse, TimedTriggerResponse and TriggerTasksResponse.
	- DeploymentTemplateResponse, ProvisionSettingInfoResponse, ControllerResponse and MetricsDataResponse.
	- AnalyticsStatsResponse.difference can be a str, and InstanceResponse.port is an int.
- New `RoleMemberResponse`, `RoleResponse.members` is `list[RoleMemberResponse]`.
- `APISpec` is `dict[str, dict[str, APISpecEndpointData]]`, `ActionSpec` is `dict[str, dict[str, str]]`.
- `APISpecEndpointData` and `APISpecEndpointParameters` follow getapispec.json.
	- The old classes are kept commented out.
- `DiagnosticsResponse.hardware_platform` and `network_mode` are `str`, `ModuleResponse.feature_set` is `list[str]` and `branding` is `BrandingResponse`.
- `SettingSpecResponse.enum_values` is `Union[dict[str, str], None]` (getprovisionspec sends a dict).
- `ApplicationResponse.settings` is `dict[str, str]`.
- New `BrandingResponse`, `UptimeResponse` and `MessageParametersResponse`.
- `PermissionNode` renamed `PermissionNodeResponse`.
- `StructuredDiagnosticsResponse.application` is `dict[str, Any]` (`server_type` is an int).
- `InstanceResponse.metrics` is `MetricsResponse` (an empty object when stopped).
- Raw response TypedDicts renamed to `<Dataclass>Response`.
	- `ParameterMapping` -> `ParameterMappingResponse`, `ConsumeResponse` -> `ConsumesResponse`, `AnalyticsStatResponse` -> `AnalyticsStatsResponse`, `DiagnosticsInfoResponse` -> `DiagnosticsResponse`, `LoginResponse` -> `LoginResultsResponse`, `ModuleInfoResponse` -> `ModuleResponse`, `ConfigResponse` -> `SettingSpecResponse`, `TriggersTasksResponse` -> `TriggerTasksResponse`, `MCUserData` -> `MCUserResponse`, `MetricsKeyResponse` -> `MetricsDataResponse`.
- `AvailableMethodsResponse` is now `MethodsResponse` and `TriggersResponse` is kept, matching the AMP-2.8.0.8 captures.
	- `MethodsData` and `AvailableTriggersResponse` are commented out.
- `ParameterMapping` lists the same 62 keys as NotRequired[str].
- Added `StructuredDiagnosticsResponse` and `ControllerResponse.push_is_current`.
- DeploymentTemplateResponse: AMP sends `setting_mappings`, so the key is renamed from `settings_mappings`.
	- `description`, `module`, `template_role` and `template_base_app` are `Union[str, None]`, confirmed live.
- TimedTriggerResponse: added `last_executed`.
- TriggersResponse: added `last_run`; `last_execute_error` and `last_error_reason` were already NotRequired.
- Added `BackupResponse` and `BACKUP_REQUIRED_KEYS` / `BACKUP_EXCLUDED_KEYS`.
	- Built from the `Backup` dataclass, since the captured GetBackups response is an empty list.

## Review of the hint fixes


## The hints match what AMP sends


## get_supported_app_summaries builds its own dataclass


## Version numbers are bold in the docs


## conf.py *w/Claude
- `bold_directive_versions` bolds the version number in every `versionadded`, `versionchanged`, `deprecated` and `versionremoved` label once a page is built.
	- Sphinx reads no markup in the version argument, so `**5.0.0**` in a directive shows the asterisks.
- Added the GPL header and typed `intersphinx_mapping`'s values.

## Tidied NOTES.md and TODO.md before the push


## The changelog leaves out commits already on main


## gen_changelog.py *w/Claude
- Commits reachable from `origin/main` are left out of the new version's entry.
	- `Refactor` merged `main` in, so the 5.0.0 entry would have listed 34 commits from 4.x again, 17 of them with text.
	- A dry run in a clone without a remote gives 210 commits and no repeats.

## pyproject.toml
- Ruff skips the workflow scripts, as they carry a blanket `# ruff: noqa`.
- Ruff excludes `unit_test.py`, and `force-exclude` applies that when the file is named on the command line.
- `[tool.check_code] skip_pyright` skips `unit_test.py` too.
- Removed the `dataclass-wizard` dependency.
- Ignored ruff `FURB122`; `for ... file.write()` loops stay as they are instead of becoming `file.writelines()`.
- Added `typing_extensions` to `dependencies`; `core.py` and `minecraft.py` import `deprecated` from it at runtime.
- Shipped `py.typed` through `[tool.setuptools.package-data]`.
- Changelog URL points at `main` instead of `master`.
- Moved `select` / `ignore` under `[tool.ruff.lint]`; the top-level keys are deprecated.
- Bumped `requires-python` to 3.12.

## Removed the unused BaseArgs


## Docstring names take single backticks
- Every name written in double backticks is in single backticks, across adsmodule, analytics, base, bridge, core, instance, modules, _types and util.
	- `type` and `platform` are written `!type` and `!platform`, as they would link to Python's builtin and module.
	- Literal values keep double backticks: JSON `null`, the example outputs of `_normalize_endpoint`, the `api_spec_sheets` directory, the `ads_module` section key and the `Minecraft` module value.
	- backoff.py keeps its text, as it is copied from discord.py.

## Every Enum can be imported from ampapi


## _enums.py
- `__all__` lists every Enum, so the ten it left out are exported from `ampapi` too.
- The nine that 4.6.0 already had say so in a `versionchanged` directive, and `Protocols` has its `versionadded`.
- `ContainerMemoryPolicyState` has a docstring.
- `IfOperators`, `InstanceState` and `MailPriority` moved down into alphabetical order.

## docs/types.rst
- The Enums are listed in the module's order, and `Protocols` is listed.
- Dropped the `PostCreateActionsState` entry.
- Pointed `currentmodule` at `ampapi._enums` and `ampapi._types`.
- Renamed `AMPInstanceState` to `InstanceState` and added `Module`.
- Replaced the hand-listed TypedDicts with an `automodule` of `ampapi._types`, which also drops the removed `Consumes`, `ScheduleDataData`, `TriggersData` and `TriggerTasksData`.
- Split `Player` out of the `ampapi.modules` automodule so its `uuid` and `name` are not documented twice.

## Fixed two bugs in the docs generator


## base.py's classes are placed by what uses them


## Recorded the class order rule


## key_drift.py follows the CODING_STYLE file anatomy


## The package is clean under Ruff and pyright


## Classes are in alphabetical order, as modules.py is
- A base class defined in the same file still comes first. No code or text changed; every class is byte-identical.

## errors.py
- `AMPAPIKeyError` and `AMPAPIResponseError` swapped places; the base `AMPAPIError` stays first.

## Review and live check of #13 on vm1


## ampapi/filebackup.py *w/Claude
- `take_backup` returns an `ActionResult` when `dirty_only` is True and no file changed, which is what AMP answers.
	- It raised before, because AMP takes no backup then and sends no running task.
- take_backup takes was_created_automatically, dirty_only and backup_while_running.
- delete_local_backup and set_backup_sticky get the blank lines between checks the other wrappers use.
- `delete_local_backup` and `set_backup_sticky` return an `ActionResult` and take `format_data`.
- `take_backup` narrows to `RunningTaskResponse` and builds a `RunningTask`.
- Response dataclasses are built with `build`.
- Replaced the 3 `"status" not in result` checks with `is_response_type()`.
- Moved `ActionResultResponse` out of the `TYPE_CHECKING` block.
- Migrated all 9 endpoints to `_post`.

## ampapi/core.py
- The version directives on `get_audit_log_entries`, `oidc_login` and `refresh_setting_value_list` say what changed, not why.
- `get_audit_log_entries`' `before` is marked optional.
- upgrade_amp and update_amp_instance note that the stored session is reset.
- upgrade_amp's warning block indented like the others.
- Removed restart_instance and kill_instance, deprecated in 4.6.0 for restart_application and kill_application.
	- No concrete class reached Core.restart_instance, every one overrides it.
- Removed the unused warnings import.
- Every endpoint method's docstring has an `Endpoint:` line after its summary.
- Dropped the Attributes section that only repeated the `triggers` property.
- "Instance" in prose.
- "role ID", "Application User ID", "UUID".
- Spacing after a comma and before an inline comment.
- Corrected the `login` TOTP comment; an empty token does not raise.
- The `NARROW-REFACTOR` notes keep their reason and drop the marker.
- Converted 342 field lines to `name : type`.

## Fixed the wrong parameter types and the refresh_setting_value_list key (#13)


## ampapi/core.py *w/Claude
- edit_interval_trigger takes lists of ints for the five schedule parameters and checks each element against its range.
	- 4.x sent single ints, which AMP always rejected. The old single-int checks stay commented out above.
- get_audit_log_entries takes before as a datetime (None is the time of the call) and sends it as an ISO string.
	- AMP ignores the POSIX timestamp 4.x sent, and the 4.x default was fixed at import time.
- refresh_setting_value_list sends Node. 4.x sent Name, so AMP always rejected it.
- create_user takes is_oidc_user and oidc_sub.
- get_setting_values takes with_refresh.
- oidc_login takes the required state parameter after instance_id, which AMP requires and 4.x never sent.
- enable_two_factor and activate_amp_license narrow to those envelopes. key_drift then compares the keys inside result.
- enable_two_factor returns a TwoFactorSetupInfo, and activate_amp_license a LicenceInfo, not the ActionResult around them.
	- A failure already raises, and the ActionResult carried nothing more than the result.
- `restart_amp`, `upgrade_amp` and `update_amp_instance` reset the caller's stored session once they succeed.
- `logout` resets the stored session after the call, and its docstring gains a `versionchanged` line.
- `restart_amp`: the note about "Unauthorized Access" after a restart now says the next call logs in again by itself.
- restart_amp is no longer ads_only, the decorator is left commented out.
	- AMP restarts the AMP process of whichever Instance gets the call, checked on vm1 by process ID.
- Docstring notes: the application is stopped and not started again, the first call after it raises "Unauthorized Access", restart_application restarts the application.
- restart_amp, upgrade_amp, update_amp_instance and run_security_check get the blank lines between checks the other wrappers use.
- login's Returns is written Union[LoginResults, None].
- `run_security_check` returns `list[SecurityCheck] | list[SecurityCheckResponse]` and takes `format_data`.
- Removed its TODO about getting proper data back.
- `restart_amp`, `upgrade_amp` and `update_amp_instance` return an `ActionResult` and take `format_data`.
- `refresh_settings_source_cache` returns None (AMP answers JSON null) and no longer takes `format_data`.
- Fixed the `Returns` of `get_all_amp_user_info`, `get_amp_user_info`, `get_amp_users_summary`, `get_new_guid`, `get_active_amp_sessions`, `get_amp_role_permissions` and `login`.
- Added the missing `Returns` to `end_user_session`.
- `get_user_info` builds `UserApplicationData` with `build`.
- `get_setting_spec` splits the colon categories into `modules` before `build`.
- `get_webauthn_credential_ids` returns `WebauthnCredentialIDsResponse`.
- `get_oidc_logout_url` calls `Core/GetOIDCLogoutUrl`.
- Response dataclasses are built with `build`.
- `edit_interval_trigger`'s days and hours checks raise with their message.
- `get_oidc_login_url` returns the URL as a `str`, matching `get_oidc_logout_url`; it posted with `no_data=True`, so the URL AMP sent back was thrown away and it always returned None.
- `get_oidc_login_url` now sends `redirect_uri` in `parameters` and no longer accepts `state`.
	- The 2.8.0.8 spec lists one optional `redirect_uri` String. The key is lowercase like `get_oidc_logout_url`, the spec sheet keeps raw names (`serverId` is not snake_cased).
- Kept the `# TODO: Need to finish validation.` since the return value is still unchecked.
- Migrated every endpoint to `_post` and wired in the new Response types.

## ampapi/analytics.py *w/Claude
- get_analytics_summary sends start_date as an ISO string.
- get_analytics_summary takes player_count.
- `get_user_details` takes `format_data` and returns `AnalyticsUserDetails`.
	- Notes that the Instance needs Analytics and user-specific data turned on, and that AMP looks players up by name.
- Response dataclasses are built with `build`.
- Replaced the `"stats" not in result` check and the `cast("dict[str, Any]", result)` with `is_response_type(result, AnalyticsSummaryResponse, ...)`.
- Removed the unused `timezone` and `cast` imports.
- Migrated to `_post`, added `AnalyticsSummaryResponse`.

## ampapi/adsmodule.py *w/Claude
- create_instance_from_spec annotates target_datastore as an int, which is AMP's Int32.
- apply_template takes new_friendly_name, secret and restart_if_previously_running.
- upgrade_instance takes restart_if_running.
- set_instance_suspended takes suspend_reason.
- set_instance_network_info takes advertised_address and advertised_address_includes_port.
- Each is keyword-only, defaults to None and is not sent when None, so AMP keeps its own default.
- `deploy_template` returns `RunningTask | RunningTaskResponse`, which is what AMP's spec names.
	- The old `ActionResult` check stays commented out above the new one.
- Removed the comment about the parameter keys being cased wrongly.
- `update_instance_info` returns a `RunningTask`, which is what AMP 2.8.0.8 answers.
	- The spec names `ActionResult`, but AMP sends a "Reconfiguring Instance" task, so the call raised after it had worked.
- The 11 list endpoints check `isinstance(result, list)`, the dict check from #11 rejected every answer.
	- get_application_endpoints, get_datastores, get_datastore_instances, get_deployment_templates, get_instances,
	- get_instance_network_info, get_instance_statuses, get_local_instances, get_provision_arguments,
	- get_supported_app_summaries and get_supported_applications.
- `cancel_pairing` returns None (AMP answers JSON null) and no longer takes `format_data`.
- The `(str, bool)` narrowing checks are `if not isinstance(result, dict):`, as in the other modules.
	- A list response now raises `AMPAPITypeError` where the 36 methods with a `status` check raised `AMPAPIKeyError`.
- Response dataclasses are built with `build`.
- `create_local_instance` is `@deprecated`, with a `.. deprecated::` note saying why.
	- AMP 2.8.0.8 answers a null reference to every Instance shape sent, its LocalAMPInstance is undocumented, and the
   panel never calls it. `create_instance` and `create_instance_from_spec` are the working paths.
- `get_instances` drops `include_self` and always sends `ForceIncludeSelf` as True.
- `apply_instance_configuration` returns a `RunningTask`, which AMP 2.8 sends. It raised on that reply before.
	- Its docstring says what `args` takes, eg. the `Core.Login.*` nodes that repair an Instance's logins.
- `create_instance_from_spec` returns a `RunningTask`, like `create_instance`. It raised on AMP 2.8's reply before.
- `create_instance_from_spec` and `create_local_instance` take `PostCreateState`.
- `get_provision_fitness` uses `allow_null` instead of catching the error by its message text.
	- The old way logged an ERROR line on the expected path and depended on the error's wording.
- Its note no longer says "a Controller with no Targets"; vm1 has a Target and still answered null.
- get_mode converts with ADSModeState(value) inside the ValueError suppress, so the isinstance check and its Any annotation go.
	- An unknown number, a string, None or a list all raise ValueError there and fall through to the warning.
- Docstring sentences no longer comma spliced.
- Added `ADSModule.get_mode`, which reads `ADSModule.ADS.Mode` through `Core/GetConfig` and returns an `ADSModeState`.
	- A value the enum lacks, or that is not an int, logs a warning and returns `ADSModeState.not_set`.
	- Not cached, and available on a `TargetADS` through the `ADSModule` mixin.
- Added a module `LOGGER`.
- Migrated every endpoint to `_post` and wired in the new Response types.
- Fixed `PortInfo.us_user_defined` typo, added `is_firewall_target` and the `Protocols` conversion.
- Added `to_dict()` to `Template`, `InstanceInfo` and `InstanceDatastore`.

## ampapi/modules.py *w/Claude
- InstanceInfo.container_max_cpu is a float, AMP's Single, and its comment now says what the field is.
- InstanceInfo gains container_swap, container_cpu_set, custom_mount_bindings, extra_container_packages, is_multi_ip_aware, use_host_mode_network, display_group and save_only.
	- to_dict sends them under AMP's names and omits them when None.
- `Messages.from_response` builds ADSModule `remotePairStatus` as `ActionResult` and Core `userlistchanged` as `UserApplicationData`.
	- Both records captured in #30 match those classes key for key, so no new class was needed.
- Widened `Messages.parameters` and its docstring.
- `Template.to_dict()` builds the dict with AMP's parameter names (eg. `TemplateID`, `NewUsername`).
	- Attributes set to None are omitted, and `post_create` is sent as its value.
- Added a `.. versionchanged:: 5.0.0` to its docstring.
- `InstanceInfo` requires only `instance_id`; every other field defaults to None.
	- A field left as None is not sent, so AMP leaves that value unchanged.
	- `memory_policy` is unwrapped to its value only when it is set.
- Added a `.. versionchanged:: 5.0.0` and the optional wording to the docstring.
- `CreateInstance.ip_binding` defaults to "0.0.0.0" instead of "192.168.0.1".
	- AMP's create task fails on a machine without that address, and "0.0.0.0" worked on vm1.
- Updated the attribute docstring with the new default and a version directive.
- `InstanceInfo.to_dict` builds the dict by hand with AMP's parameter names (eg. `InstanceId`, `FriendlyName`).
	- Attributes set to None are left out and `memory_policy` is sent as its value.
	- In 4.x the attribute names were sent, so AMP always answered that `InstanceId` is required.
- Added a `Messages.from_response` override that builds `parameters` by (source, message).
	- ADSModule `metrics` and LocalFileBackupPlugin `BackupFailed` build `MessageParameters`, Core `refreshTask` builds `RunningTask`.
	- Core `settingValueUpdate` and ADSModule `instupdate` build the new `SettingValueUpdate` and `InstanceUpdate`.
	- Any other message keeps what AMP sent, and the caller's dict is never changed.
- Added the `SettingValueUpdate` and `InstanceUpdate` dataclasses.
- Widened `Messages.parameters` and reworded the `MessageParameters` note.
- New TwoFactorSetupInfo (url, manual_key) and LicenceInfo dataclasses, shapes from vm1.
	- Both keep their secret out of repr. LicenceInfo.expires is converted to a datetime.
- ActionResult.result can be a dict, where AMP answers an object.
- Added the `SecurityCheck` dataclass and listed it in `__all__`.
- Added `AnalyticsUserDetails`, with `first_session` and `last_session` converted to UTC datetimes.
- `UserApplicationData` is a slotted dataclass built with `build`, with the new `display_name`.
	- AMP-2.8.0.8 sends `DisplayName`, and `get_user_info(format_data=True)` raised a TypeError on it (live, FTBEvolution01).
	- The hand-written class is kept commented out above it.
- Added `slots=True` to all 68 dataclasses, `Players` included.
- Added `_field_values`, the field values of a dataclass as a dict.
	- The 12 `__repr__` methods use it in place of `vars(self)`, which raises on a slotted class.
- `UserInfo.oidc_sub`, `Module.local_login_enabled`, `SettingSpec.warn_text` and `warn_when_value`, `Methods.notice` are fields.
- `SettingsSpecParent` gains `backups`, `meta_config`, `minecraft` and `modules`.
	- `modules` holds the categories with a colon in the name, and `__post_init__` builds their entries.
- `DCConsumes` gains `locked`, `locked_value` and `locked_reason`.
- `SettingsSpecAttribute` gains `key_enum_values` and `key_enum_source`.
- `AnalyticsStats.raw_name`, `AnalyticsCountryData.sessions_percent`.
- `TriggerTasks` gains `error_behaviour`, `wait_for_complete`, `last_execute_error` and `last_error_reason`.
- `TriggerTasks.parameter_mapping` is typed `ParameterMapping` only, so `build` leaves the task's own arguments in place.
	- Its docstring says the keys are the argument names of the task's method.
- `_is_json_object` docstring no longer joins clauses with a semicolon.
- New `build(cls, data)` unpacks a response into a dataclass and builds nested dataclasses from the field type hints.
	- Keys the dataclass doesn't declare are dropped and logged once per class and key, instead of raising a `TypeError`.
	- Not in `__all__`, which exports only classes.
- `DCConsumes` gains `placeholder`, `suffix`, `display_name` and `selection_source`, and `enum_values` can be None.
- New `TargetDatastore` dataclass, `RemoteTargetInfo` holds `PlatformInfo` and `TargetDatastore`.
- `LoginResults`, `ScheduleData`, `SettingsSpecParent`, `Triggers`, `Updates` and `Status` build their nested data with `build`.
	- `Status.metrics` is one `build(Metrics, ...)` call.
- `BuildInfo.to_dataclass` no longer catches `MissingFields`, and the `dataclass_wizard` import is gone.
- `ImportConfig` defaults use `dict[str, Any]` / `list[Any]` like the rest of the file.
- Added the `ImportConfig` dataclass.
- `Diagnostics` gains `config_version`, which GenericModule Instances send.
- `CreateInstance.post_create` and `DeploymentTemplate.post_create` take `PostCreateState`.
- `BuildInfo.__lt__` compares the four version parts in order; it needed every part to be smaller, so 2.5.0.0 < 2.6.0.0 was False.
- `BuildInfo.to_dataclass` falls back to the string for a non-numeric part or the wrong number of parts instead of raising.
- `ActionResult` gains `support_url` and `support_title`; AMP 2.8 sends both, so every method returning a formatted ActionResult raised a TypeError after AMP had already done the action.
- `LoginResults` allows None for `permissions`, `session_id` and `remember_me_token`.
- `Metrics` requires only active_users, cpu_usage and memory_usage; physical_ram_usage, swap_usage and the new tps default to None.
	- The ADS sends the two usage metrics, Minecraft instances do not, and some modded ones add tps; the five required keys raised a KeyError on every Minecraft instance.
- `Status` gains `ports`, converted into `Port`; AMP 2.8 sends them, so `get_status` and `get_updates` raised a TypeError on game instances.
- `Port` gains `listening_count`, `range` and `min_listening`; `get_port_summaries` and `Updates.ports` raised a TypeError.
- `Backup` gains `compressed_size_bytes`, `hash_sha1`, `meta`, `parent_manifest` and `remote_store_id`; `get_backups` raised a TypeError for anyone with a backup.
	- Every new field is defaulted so older responses still construct.
- `Updates.__post_init__` converts `console_entries`, `messages`, `ports` and `tasks`; only `status` was converted, so `updates.console_entries[0].contents` raised an AttributeError.
- `ConsoleEntries` gains `source_id` and `Messages` gains `parameters`; AMP sends both, so building either from a real response raised a TypeError.
	- Both are defaulted so older responses still construct; `Messages.parameters` stays a dict, its metrics carry a different key set than `Metrics`.
- `Metric` is renamed `Metrics` and carries all five metrics AMP sends; `Status.metrics` converts into it.
	- Each key is named in `__post_init__`; looping a TypedDict's `.items()` types the values as `object`, which `**` cannot unpack.
- Removed dead commented-out code (`SettingsLogin`, old TypeVars and aliases) and comments that described already fixed bugs.
- Docstrings no longer name `get_op_whitelist`, `PostCreateActionState`, `AMPVersionInfo`, `SESSIONID` or `Login`.
- `ScheduleData` list attributes are annotated `list[Methods]` and `list[Triggers]`, matching what `__init__` builds.
- Removed the unused `AvailableMethodsResponse` import.
- Widened `AnalyticsSummary.stats`, `graph_data`, `quietest_time` and `busiest_time` to also accept `AnalyticsStatResponse` and `AnalyticsGraphDataResponse`.
	- Nothing converts these fields into dataclasses, so the raw TypedDicts are what the dataclass really holds. The `cast` was hiding the mismatch.
- Added `is_smart_excluded_from_backups` to the `Directory` dataclass, defaulting to `False`, plus its `Attributes` entry.
	- Newer AMP sends the field and `Directory(**result)` raised `TypeError` without it. Older AMP omits it, so it needs the default.
- Refreshed the dataclasses that no longer matched the live API.
- Added `__post_init__` conversions for enum and nested fields.

## Added the parameters AMP's spec lists that our wrappers lacked (#13)


## ampapi/filemanager.py *w/Claude
- create_archive takes overwrite_existing.
- Response dataclasses are built with `build`.
- Replaced the 15 `"status" not in result` checks with `is_response_type(result, ActionResultResponse, ...)`.
	- The `in` check never narrowed the `_post` union, so `ActionResult(**result)` failed type checking.
- Moved `ActionResultResponse` out of the `TYPE_CHECKING` block, it is now used at runtime.
- Migrated to `_post`, added `DirectoryResponse` and `FileChunkResponse`.
- Fixed the `base_64_data` key check, the payload key is `base64_data`.

## Removed create_local_instance and append_file_chunk (#13, #4, #7)


## ampapi/adsmodule.py
- Removed create_local_instance, deprecated in 5.0.0 because AMP 2.8.0.8 answers a null reference to every Instance shape sent.
- Removed the unused deprecated import.
- Every endpoint method's docstring has an `Endpoint:` line after its summary.
- The `servers` warning uses single backticks like the rest of the docstrings.
- `create_local_instance` carries a TODO: AMP rejects every shape we send, and the decision is Kat's.
- "Instance" and "URL" in prose.
- "The Template ID", "Target dicts", "standalone".
- get_instances note says the standalone ADS returns its own ADS Instance.
- The `include_self` note says AMP sends it as `ForceIncludeSelf`, and a standalone ADS returns its own row either way.
- Converted 278 field lines to `name : type`.
- Changed `AMPADSInstance` to `TargetADS` and `AMPInstance` to `Instance` in docstrings.

## ampapi/filemanager.py
- Removed append_file_chunk, which has no visible effect on AMP 2.8.0.8.
- Added the missing `Returns` to `append_file_chunk`.
- Each endpoint method's docstring has an `Endpoint:` line.

## Messages.parameters builds remotePairStatus and userlistchanged (#32)


## ampapi/_types.py *w/Claude
- Widened `MessagesResponse.parameters` with `ActionResultResponse` and `UserApplicationDataResponse`.
- Added the `SettingValueUpdateResponse` and `InstanceUpdateResponse` TypedDicts.
- Widened `MessagesResponse.parameters` to match.
- TwoFactorSetupResultResponse and LicenceResultResponse, an ActionResult whose result names the inner shape.
- TwoFactorSetupInfoResponse and LicenceInfoResponse with their key tuples.
- ActionResultResponse.result can be a dict.
- Added `SecurityCheckResponse` and the `SECURITY_CHECK_REQUIRED_KEYS` / `SECURITY_CHECK_EXCLUDED_KEYS` key sets.
- `SETTINGS_SPEC_PARENT_REQUIRED_KEYS` is `system_settings` and `security_and_privacy`, and `SettingsSpecParentResponse` marks the other categories `NotRequired`.
- New `WebauthnCredentialIDsResponse` and its required keys.
- `NotRequired` keys matching the new dataclass fields on the TypedDicts.
- `settings` is a required `ImportConfig` key, as in the live reply.
- Added `ImportConfigResponse` and the `IMPORT_CONFIG_*_KEYS` sets.
- `APISPecEndpointData` -> `APISpecEndpointData`.
- TypedDict attribute docstrings use the spaced `name : :class:` separator (52 lines).
- `ActionResultResponse` gains the same two keys.
- `InstanceResponse.metrics` uses `Union[X, None]`.
- Added the `KeyDrift` TypedDict.
- `LoginResponse` allows None for `permissions`, `remember_me_token`, `session_id` and `user_info`, as a failed login sends.
- `MetricsResponse` marks physical_ram_usage, swap_usage and tps as NotRequired; `StatusResponse` and `PortResponse` gain the 2.8 keys.
- Added `ConsoleEntriesResponse` and `MessagesResponse`, confirmed against `getupdates.json`.
- `UpdatesResponse` lists are typed with their entry shapes instead of `list[Any]`.
- `MetricsResponse` is the five key `metrics` shape, with `MetricsKeyResponse` for each entry.
- `StatusResponse.metrics` is a `MetricsResponse`; `InstanceResponse.metrics` stays a dict keyed by metric name.
- The `NARROW-REFACTOR` notes keep their reason and drop the revert steps.
- `PermissionNode.children` is now `Union[list[PermissionNode], None]`.
	- 55 nodes in `getpermissionsspec.json` carry `children: null`.
- Added `ANALYTICS_SUMMARY_REQUIRED_KEYS` and `ANALYTICS_SUMMARY_EXCLUDED_KEYS`.
- Added `is_smart_excluded_from_backups` to `DirectoryResponse` as `NotRequired[bool]`.
- Added `OPWhitelistResponse` with `OP_WHITELIST_REQUIRED_KEYS` and `OP_WHITELIST_EXCLUDED_KEYS`.
	- Built from the `OPWhitelist` dataclass, the captured `getopwhitelist.json` is a "Missing Method" error. Tagged with a `# TODO:` to confirm.
- Added the `*Response` TypedDicts, built from captured responses where one exists.
- Added `is_response_type()` and `is_response_list()` with the `*_REQUIRED_KEYS` / `*_EXCLUDED_KEYS` tuples.

## unit_test.py reads the regrouped captures, and the linters skip it as a test file (#31)


## VM captures for the remaining push events (#30) and captures grouped by AMP version and kind (#31)


## CONTRIBUTING.md
- Described the `_responses/` layout and pointed the capture examples at it.
- "Minecraft Instance".
- New guide: setup, the checks to run before a pull request, code style, the commit message format and live server safety.
- Dev tools with examples: `_call_end_point`, capturing responses with `to_file`, key drift checks (`check_key_drift` and `KeyDriftCheck`) and the AMP update utilities.

## Live check of the InstanceInfo follow-up and #29 on vm1


## Template sends AMP's parameter names and deploy_template returns a RunningTask (#29)


## InstanceInfo needs only instance_id (#27 follow-up)


## Review and live check of #26, #27 and #28 on vm1


## ampapi/modules.py
- Fixed a comma splice in the `ip_binding` version directive and gave `SettingValueUpdate.node` a real example node.
- SecurityCheck.passed docstring uses single backticks.
- LicenceInfo.expires says it is converted to a naive datetime.
- SecurityCheck.severity docstring reworded.
- Reworded the `_converter` docstring.
- `.. versionadded:: 5.0.0` on the four `DCConsumes` fields new since 4.6.0 and on `TargetDatastore`.
- `.. versionchanged:: 5.0.0` on `RemoteTargetInfo.datastores` and `TriggerTasks.parameter_mapping`.
- `UserInfo.oidc_sub` carries no directive, `UserInfo` is new in 5.0.0.
- `SettingsSpecParent` docstring: one blank line before each directive, `modules` reworded.
- `build` comments and docstrings say what the code does without "so" clauses.
- "Instance" and "URL" in prose.
- "type ID", "Instance type", "Minecraft Instances"; `description` / `id` named in backticks.
- Converted 498 field lines to `name : type`.
- Changed `AMPInstance` to `Instance` in the `Triggers` docstring.

## CreateInstance binds every IPv4 address by default (#28)


## update_instance_info sends AMP's parameter names (#27)


## Messages.parameters is built by the message type (#26)


## Push events captured on vm1 for #26


## `get_remote_login_token` works without `is_temporary` (#25)


## What `Messages.parameters` holds per push event, and two findings from vm1's AMP log


## #24 phase C: `build` is gone, and the docs and notes describe `from_response`


## Responses in adsmodule, filemanager, minecraft, filebackup and instance build with `from_response` (#24 phase B2)


## filemanager.py *w/Claude
- `build(X, data)` calls are `X.from_response(data)`.
- Dropped `build` from the `.modules` import.
- `write_file_chunk` renamed `append` to `final_chunk`, the `FinalChunk` AMP always received.
- `upload_folder` takes a list of `FolderUploadFile`.
- `append_file_chunk` docstring warns it has no visible effect on AMP 2.8.0.8.
- Added `download_folder_as_zip` and `upload_folder`.
	- `upload_folder` passes `files` through as given, the FolderUploadFile keys are unconfirmed.
	- `dummy` is skipped, it is a no-op placeholder in the spec.
- Added the license header, wrapped the long class notes and added the colon to the TODO lines.
- append_file_chunk: documented `delete` as unconfirmed, the spec gives no description.

## minecraft.py *w/Claude
- `build(X, data)` calls are `X.from_response(data)`.
- Dropped `build` from the `.modules` import.
- `mc_reject_eula` returns a bool like `mc_accept_eula`, and raises when AMP answers with anything else.
- `mc_get_op_whitelist` already carries the `Removed in AMP API 2.6.5.0` deprecation, so it is unchanged.

## filebackup.py *w/Claude
- `build(X, data)` calls are `X.from_response(data)`.
- Dropped `build` from the `.modules` import.
- Added `backup_will_stop_server`, returning a bool.
- `get_backups` returns `list[Backup] | list[BackupResponse]`, narrowing each item with the Backup keys.

## instance.py *w/Claude
- `build(X, data)` calls are `X.from_response(data)`.
- Dropped `build` from the `.modules` import.
- `Instance.metrics` is `Metrics` (None for an empty object), `application_endpoints` is `list[Endpoints]`.
- `ADSData.platform` is `PlatformInfo` and `ADSData.datastores` is `list[TargetDatastore]`.
- Follows the TypedDict renames.
- Added the `TargetData` mixin holding the Target field annotations, the `__getattribute__` cache guard and `_parse_target_data`.
	- Moved out of `Controller`; `_parse_controller_data` is now `_parse_target_data`.
	- The guard reads `type(self)._cached_names`, so each class guards its own names.
- `TargetADS` guards the Target fields minus `friendly_name`, `description` and `tags`, which stay the Instance's values.
- `Controller.get_instances` gives a `TargetADS` the Controller's copy of its Target entry, then `TargetADS.get_instances` parses its own view over it.
- `Controller.get_instances` and `TargetADS.get_instances` update existing objects in place, matched by `instance_id`.
	- `_targets`, `_instances` and `TargetADS._instances` stay the same objects; new ones are added and ones AMP no longer lists are dropped.
	- An object whose `module` changed is replaced.
- Added `Controller._sync_instances` for the in place update.
- `Instance.route_by_target` falls back to its Controller's value, so setting it on the Controller covers every Instance it holds.
- `start_instance`, `stop_instance`, `restart_instance` and `_routed_ads` drop the `route_by_target` parameter.

## Responses in core, analytics, emailsender and generic build with `from_response` (#24 phase B1)


## analytics.py *w/Claude
- `build(X, data)` calls (2) are `X.from_response(data)`.
- `get_user_details` returns None when AMP answers null.
- Added `get_user_details`, returning the raw dict until the shape is confirmed.

## emailsender.py *w/Claude
- `build(X, data)` call (1) is `X.from_response(data)`.

## generic.py *w/Claude
- `build(X, data)` calls (3) are `X.from_response(data)`.

## Review of #24 phase A: timed trigger tasks build as a list, and `from_response` is faster than `build` was


## Response dataclasses build with `from_response` on a `ResponseData` base (#24 phase A)


## modules.py follows the CODING_STYLE file anatomy


## Single backticks for names in the docs


## docs/index.rst
- Same.
- Added an Upgrading toctree and a note under Installing that 5.0.0 breaks 4.x code.
- Changed the minimum to Python 3.12.
- Fixed the key features and basic usage text and links to `Controller` and `Instance`.

## docs/modules.rst
- Same.
- Added the Generic Module and SteamCMD Plugin sections.
- `Base` and `Core` no longer exclude those members, so their own docstrings show.
- Added Response Handler Options, Exponential Backoff and Error Classes sections.
- Excluded `session_ttl` and `instance_id` from `Base`, and `triggers` from `Core`, to clear the duplicate object warnings.

## Single backticks for names in today's docstrings


## ampapi/_types.py
- LicenceInfoResponse, LicenceResultResponse, SecurityCheckResponse, TwoFactorSetupInfoResponse and
	- TwoFactorSetupResultResponse docstrings use single backticks around names.
- The "Not total=False" comment is back above UpdateInfoResponse.
- Added `AnalyticsUserDetailsResponse` and its key check.
- Added `display_name` to `UserApplicationDataResponse`.
- `DiagnosticsInfoResponse` gains `config_version` as NotRequired.
- `PermissionNode` docstring: "struction" -> "structure".
- The BackupResponse keys are confirmed against a live GetBackups response.
- Copyright module docstring.
- Dropped a pyright ignore strict no longer needs.
- "Minecraft Instances".
- Converted 4 field lines to `name : type`.

## ampapi/base.py
- Base.module's Returns uses single backticks.
- Three comments split into sentences.
- Wording of the new comments and docstrings, no code change.
- Reworded four comments and docstrings in the key cache and `sanitize_json`.
- `write_data_to_file`: the old `elif` kept commented out, a blank line after the docstring summary.
- `session_ttl` and `instance_id` left the `Base` Attributes section; `instance_id`'s property docstring carries what that entry said.
- Dropped three pyright ignores strict no longer needs.
- "URL" in prose.
- "session ID", "Instance ID".
- `json_to_typeddict` docstring is raw, so its `\n` example no longer splits the docstring; Sphinx is back to 0 warnings.
- `include_imports` is marked optional with its default.
- Converted 33 field lines to `name : type`.
- Changed the `_no_controller` message and the `ads_only` docstring to `Controller` and `TargetADS`.

## Review of #22: comment wording, live results in the notes


## One login for concurrent calls on a dead session (#22)


## ampapi/base.py *w/Claude
- Added `Base._login_pending`, a future that marks a login in progress on this object.
	- `_reauth` waits on it first, then re-reads the stored session and logs in only if there is still none.
	- The marker is set only when a login is needed, and cleared and resolved with None in a `finally`, so only the call that logged in sees an error.
	- A failed login wakes the waiting calls, which each try their own, one at a time.
- Moved the dead-session reset from `_response_handler` to the `_post` branch.
	- It resets only when the stored session is still the one that pass sent, so a slow dead answer cannot wipe a fresh login.
	- A second dead answer, or a dead answer to `Core/Login`, still raises without a reset.
- Split the 2FA error message across two lines to stay under the line length.
- The RuntimeError retry waits at least one second, and its log line says which retry it is.
	- The backoff handed back 0 seconds for half of all first retries. Kat's two lines are left commented out.
- _post works on a copy of request_params. A dict the caller passed again carried the last call's headers and data.
	- Kat's setdefault("headers") line is left commented out above the rebuilt headers.
- clean_up(logout=True) skips Core/Logout when no session is stored, instead of logging in only to log out.
- The dead-session warning no longer says "logging in again", since `_post` may raise instead.
- Two comments reworded, one of them inaccurate about the RuntimeError retry having a limit.
- The dead-session check runs before the Unauthorized Access / Instance Unavailable error log, and logs a warning.
	- A session that is logged in again is expected. Only a second dead answer is an error, and `_post` raises and logs that one.
- _SessionDeadError skips AMPAPIResponseError's error log.
- One comment split in two.
- version_validation's response check is formatted the way ruff format and COM812 both accept.
- Added `_reset_session`, which stores `APISession(id="0")` under the caller's own key.
- `_response_handler`: "Unauthorized Access" naming `Session.Exists` resets the session and raises a private `_SessionDeadError`.
	- Any other permission node still raises at once, with no reset.
	- "Instance Unavailable" still raises but no longer resets the session.
	- The inline reset is commented out above the helper call.
- `_post`: catches `_SessionDeadError` once, logs in again with `_reauth` and sends the same request once more.
	- A second dead answer raises a plain `AMPAPIResponseError`, and `Core/Login` is never retried.
	- The Authorization header is rebuilt on the resend, headers the caller passed are left as given.
	- The send is now a loop, so the RuntimeError retry shares the one-resend limit and the two can't loop.
- `clean_up`: resets the stored session after the logout attempt when `logout=True`.
- `_post` with `no_data=True` runs `_response_handler` with `allow_null`, so an error title or `Status: false` raises `AMPAPIResponseError`.
- `_response_handler` writes a bool to file (`to_file`) before returning it.
- `write_data_to_file` accepts a bool.
- `Pass` maps to `passed` in `Base.json_key_mapping`.
- The `get_diagnostics_info` check narrows with `isinstance(result, dict)`.
- Docstring fixes for `no_data`, `Base.module` and `Base.sanitize_json`.
- `write_data_to_file` writes a `str` through `json.dumps` when the file name ends in `.json`.
- `sanitize_path` only drops leading slashes, the old guard rails are commented out.
	- AMP takes `_`, `..`, `./`, `\` and dot-folders as given, and only a bare `/` fails.
- `_call_end_point` logs in first, like every wrapper, so it can test any endpoint on its own.
	- `_reauth` posts `Core/Login` directly, since going through `_call_end_point` would call itself again.
- Added `generic_only`, which lets a call through only on module "GenericModule" or "Generic", like `ads_only`.
- Removed `route_by_target`, `_route_by_target` and `_route_override`.
- New `allow_null` response option: `_response_handler` returns None for a JSON null instead of raising.
- Added the global `route_by_target` setting (`_route_by_target` ClassVar, property and setter), mirroring `format_data`.
- `sanitize_json` leaves any key containing "." exactly as sent.
	- AMP setting nodes such as `ADSModule.Defaults.DefaultAuthServerURL` were being turned into `ads_module._defaults._default_auth_server_url`.
	- The value of a dotted key is still sanitized recursively.
- `version_validation` raises when AMP is at or past the version the endpoint was removed in; it raised for older AMP before.
	- `GetWebserverMetrics` was removed in 2.6.0.0, so the old check blocked the versions that still had it.
- Its error message is formatted (the message and values were passed to RuntimeError separately).
- Docstring names `version` as the removal version and `BuildInfo` as its type.
- A response with `status: false` raises with AMP's own `reason` instead of "Status is False".
	- eg. RegisterTargetWithCode says the Controller's ADS mode is not set yet.
- `_key_drift_check` and the `_reauth` return docstring use `Union[X, None]`.
- `_response_handler` takes a `check_key_drift` dev parameter that runs with `to_file`; on drift it logs a warning and writes `<endpoint>.key_drift.json` beside the capture.
- The `ResponseHandlerOptions` entries use numpydoc's spaced separator.
- `_reauth` raises `AMPAPIResponseError("Login Failed")` when AMP refuses the login, using the new `_login_failed` string; it stored the `None` session and the next call failed as "Unauthorized Access".
	- AMP sends no reason; a wrong password and a wrong 2FA code both answer `result: 40`, so the message names the user and the result code.
- Removed the blind `except Exception`; network and response errors during login reach the caller with the Core/Login url, instead of a warning followed by a second error.
- A bad 2FA token shows the friendly message; pyotp raises `binascii.Error` (a ValueError), not the AttributeError it caught.
- `call_end_point` is now `_call_end_point`; it is for testing endpoints that have no wrapper yet.
- Its docstring points at the versioned spec sheet folders and no longer mentions `SESSIONID`.
- Added `__aenter__` / `__aexit__` and `clean_up()`.
- Fixed `BuildInfo.to_dataclass()` returning `str` into a `BuildInfo` and raising `TypeError` on the version check.

## key_drift sees inside the two ActionResult<object> answers (#20), a floor under the RuntimeError retry (#21)


## Code analysis of today's work: fixes from three read-only reviews


## enable_two_factor and activate_amp_license return what AMP sends, typed (#19)


## #18 done


## Review of #18: a recovered session logs one warning, not two errors


## The calls that end the caller's own session reset it (#18)


## A dead session is logged in again and the call sent once more (#18)


## Review of today: wording, #18 added


## Redundant endpoint methods removed, upgrade_instance named like its endpoint


## ampapi/instance.py *w/Claude
- Instance.update_instance is renamed upgrade_instance, matching ADSModule.upgrade_instance and ADSModule/UpgradeInstance.
- TargetADS.upgrade_instance takes an instance_name and upgrades that Instance on the Target, like its start, stop and restart.
- `Instance.get_updates` and `get_application_status` take `request_params` and `**response_params`.
- `BuildInfo` is built with `build`.
- `_parse_instance_data` keeps the old skip-on-null logic commented out above the new default.
- Comments no longer join clauses with semicolons or trail off into "so ..." clauses.
- The `__getattribute__` docstring uses single backticks.
- `_parse_instance_data` sets every field, using the documented default when AMP sends null.
	- `description`, `display_image_source` and `module_display_name` fall back to "", everything else to None.
- `Instance.url` defaults to None, since AMP never sends one for an Instance. A TargetADS gets its Target's.
	- `TargetData.url` is `Union[str, None]` to match, and the TargetADS own-view merge keeps a set URL only.
- `TargetADS.get_instances` keeps the Controller's `url`, `is_remote` and `id` when it applies the Target's own view.
	- From the Target itself `url` is localhost, `is_remote` is False and `id` is its own numbering (vm2, live).
- `Controller.get_instances` and `TargetADS.get_instances` drop `include_self`, overloads included.
	- False only ever dropped a Controller's local Target, leaving its own data and ADS ID unset.
- `Instance` mixes in `GenericModule` and `SteamCMDPlugin`, and `GenericInstance` is gone.
	- Generic Instances come back as a plain `Instance` again; Minecraft and TargetADS raise on the Generic calls.
- Added `GenericInstance(GenericModule, SteamCMDPlugin, Instance)`.
- `Controller.instance_conversion` builds it for module "GenericModule" and "Generic".
- The Target fill pairs each TargetADS with its result through `zip(..., strict=True)`.
- Added `Controller.targets`, a read-only property over the remote `TargetADS` objects keyed by ADS ID.
	- `Controller.instances` now holds only the Controller's own Instances.
- Added `Instance.ads` and the `ads` argument on `Instance.__init__`, `TargetADS.__init__` and `Controller.instance_conversion`.
- `Controller.get_instances` builds a `TargetADS` per remote Target and fills them all with `asyncio.gather`.
	- A Target that fails logs a warning and keeps an empty `instances`.
	- A Target missing its own ADS Instance is skipped with a warning.
- `Controller.get_instance` returns the cached `TargetADS` for a Target ADS ID and raises `ValueError` for a Target's Instance.
- `TargetADS.get_instance` and `get_instances` convert with `ads=self` and refresh `self` from the Target's own data.
- `Instance.start_instance`, `stop_instance`, `restart_instance`, `update_instance` and `get_instance_status` go through `Instance.ads`.
- Removed `Instance._routed_ads` and the `Instance.route_by_target` override.
- `_routed_ads` asks `get_instance` for `format_data=True`, so a global `format_data=False` can't turn the TargetADS into a raw dict and send the call to the Controller by name.
- If it still gets no TargetADS, it logs a warning before falling back to the Controller.
- `ADS01` in single backticks in its docstring.
- `Instance.start_instance`, `stop_instance` and `restart_instance` take a keyword `route_by_target` (None uses the global).
	- AMP looks the Instance name up on the ADS that receives the call, and names repeat across Targets.
	- A remote Instance is called through its `TargetADS`, found in `instances` or fetched once with `get_instance`.
	- False keeps the old Controller path.
- Added `Instance._routed_ads` to pick the ADS for those calls.
- Added `Controller._learn_ads_instance_id`, now shared with `get_instance(auto_detect=True)`.
- "id" -> "ID" in the TargetADS / Controller docstrings, comments and the get_instance warning.
- "target dicts" -> "Target dicts"; the `instances` attribute named in backticks.
- Docstrings, comments and the get_instance warning say ADS Instance / Instance, and Target / local Target for an item of a GetInstances result.
- Loop names follow: `entry` -> `target`, `rows` -> `available_instances`, `row` -> `instance`.
- TargetADS overrides document request_params as Union[AioHTTPRequestOptions, None], per the library's style.
- The unknown own id warning reads as one sentence.
- `Controller` keeps its own ADS id in `_ads_instance_id`, stored by `get_instances` from the local entry (raw path included).
- `Controller.get_instance` takes `auto_detect`.
	- An ADS row matching the Controller's own ADS id returns `self`.
	- With the id unknown, `auto_detect=True` looks it up once through `get_module_info`.
	- With the id still unknown, it logs a warning and returns a `TargetADS`.
- `TargetADS.get_instance` returns `self` for its own id and converts other rows through the Controller.
- `TargetADS.get_instances` returns the Instances on that Target without its own row and keeps them on `TargetADS.instances`.
- `TargetADS` is now `TargetADS(ADSModule, Instance)`, so a Target ADS has every ADSModule endpoint.
- `start_instance`, `stop_instance`, `restart_instance` and `delete_instance_users` are defined on `TargetADS` under `@override`.
	- Each takes ADSModule's signature and delegates to it, acting on an Instance of this Target.
- Updated the `TargetADS` class docstring.
- Removed `Controller._initialized`; the guard now keys off `_is_cached` alone.
	- `_initialized` was only set when built with `data`, which nothing does, so a `Controller(bridge=...)` never got the
	- unpopulated message or the stale warning.
- `get_instances` docstring notes that `include_self=False` leaves the Controller's own attributes unset.
- `Controller.get_instances` skips the local entry's own ADS row (its instance_id matches the entry's); that row is the Controller, whose data is already copied onto self.
	- It came back as a TargetADS in both a standalone and a Controller/Target setup; remote entries' own ADS rows stay TargetADS.
	- Checked against the controller_setup dump and Kat's live standalone setup.
- The Controller docstring and the instance_conversion comment say which ADS rows reach TargetADS.
- `Controller` is the API client again, `Controller(ADSModule, Core, EmailSenderPlugin, FileManagerPlugin)`.
- Added the cached-attribute guard using `_is_cached` and `_cache_timeout`.
- `instance_conversion()` builds `TargetADS` for ADS rows.

## restart_amp runs on any Instance


## #11 done


## Review of #11: list endpoints in adsmodule check for a list again


## Review of #11: spacing in the new wrappers, login's Returns type


## run_security_check returns typed SecurityCheck results (#11)


## Wrapper returns match what AMP sends, and one narrowing check everywhere (#11)


## ampapi/minecraft.py
- Added the missing `Returns` to `mc_remove_op_entry` and `mc_remove_whitelist_entry`.
- Each endpoint method's docstring has an `Endpoint:` line.
- Copyright module docstring.
- Wrapped the Bukkit categories note.
- "ADS Instances".
- One-line class docstring.

## Methods that return None still check AMP's answer for errors (#11)


## Player Analytics details are typed, from a live response (#6)


## Player info from AMP-2.8.0.8 builds again (#5)


## #9 done


## Review of #9: comment wording, notes on where a response's time goes


## Role members become RoleMember dataclasses


## Response pipeline speed: cached key conversion and per-class build plans


## Slotted response dataclasses (#9)
- Every response dataclass is `slots=True`: 11-14% less memory per object, 40-66% on classes with many defaulted fields.

## ampapi/util.py *w/Claude
- `_settings_node_parse` reads the `SettingsSpecParent` field names with `fields()` in place of `vars()`.
- Added `generic_module` and `steamcmdplugin` to `_SPEC_MODULE_MAP`.
- `amp_api_update` moves on to the next Minecraft Instance after a version mismatch instead of always raising.
	- The wrong-type check runs first, and raises a formatted `msg`.
	- The mismatch warning names the ADS and Instance versions the right way round.
- `generate_docs_rst` matches Generic Instances by `GenericModule`, the module name AMP 2.8 reports.
	- The `srcds` branch has a TODO, as AMP 2.8 has no `srcds` module.
- `amp_api_update` and `generate_docs_rst` loop over the Controller's Instances and each `TargetADS.instances`.
	- A remote Target's Instances are no longer in `Controller.instances`.
- `find_missing_endpoints` now matches the `url=` / `endpoint=` literals each module posts to instead of method names.
	- Renamed wrappers (`activate_amp_license`, `get_setting_spec`, ...) no longer show as missing.
	- Spec names and url parts are compared lowercased with underscores removed; the section must match the url's module part.
	- Added `_get_endpoint_urls` and `_normalize_endpoint`; removed `_get_implemented_methods`, `_METHOD_RE` and `_ENCAPSULATED_ENDPOINTS`.
	- `suffix_aliases` is still accepted but unused here; `find_parameter_mismatches` still uses it.
- The report's file links are now relative to the report.
- Named the `consumes` comprehension variable instead of `x`.
- Imported `Base` (its import was commented out, `Base.camel_to_snake_re` raised `NameError`) and changed `AMPControllerInstance` to `Controller`.
- Removed the stray `print("file_a path", file_a)` and the 9 unused imports.
- Replaced `fromdict(ScheduleData, data)  # type: ignore` with `ScheduleData(data=data)`, `ScheduleData` is no longer a dataclass.
- Rewrote `dict_merge` to extend the three `ScheduleDataResponse` keys by name instead of looping over `str` keys, dropping its `# type: ignore`.
- Narrowed `get_diagnostics_info`, `get_setting_spec` and `get_schedule_data` results with `isinstance` and `AMPAPITypeError`.
- `_method_event_parse` reads `Methods.consumes` entries as dicts, since `Methods(**entry)` leaves them raw.
- Removed the always-true `isinstance(entry, dict)` and `description is not None` checks, and `special_chars` is now `tuple[str, ...]`.
- Updated stale class names in the docstrings of `_parse_get_api_spec_to_file`, `amp_api_update`, `generate_docs_rst` and `dict_merge`.
- Moved the module-level `from docs.samples.method_event_usage import example_note` into `_method_event_parse`.
	- `docs/` is not packaged, so `import ampapi` raised `ModuleNotFoundError` once installed. The other three doc imports were already function-local.

## #16 done: notes on the raw dicts that stay raw


## Side bugs and stale TypedDicts


## Tighter type hints, checked against every 2.8.0.8 capture


## Fixed-shape raw dicts become dataclasses


## #15 done: notes on task argument conversion and the `XResponse` naming rule


## Every public dataclass in modules.py is exported and documented


## types.rst
- Documents `ampapi.modules.Module` explicitly, after the modules automodule.
- Added `IfOperators` and `MailPriority`.

## Task parameter mappings convert operation, priority and when; dataclasses and their raw TypedDicts share a name


## _enums.py *w/Claude
- Added `IfOperators` and `MailPriority`, the values AMP lists in `enum_values`.

## Task arguments convert to bool, int, float and InstanceState from AMP's strings


## Country analytics: `session_percent` is renamed `sessions_percent`, the key AMP sends


## Task parameter mappings build into `DCParameterMapping` again, which now holds every task method's arguments


## #1 and #8 done: notes on `build`, the 2.8 keys and the response captures


## Review of #8 and #1: version directives against 4.6.0, docstring wording, uv.lock


## ampapi/core.py, ampapi/filebackup.py, ampapi/_types.py
- Comment and directive wording.

## uv.lock
- `uv lock`: dataclass-wizard removed.
- Locked `typing_extensions`, bumped `multidict` 6.6.0 -> 6.9.1 as 6.6.0 was yanked.

## Response refresh: declare the keys AMP 2.8.0.8 sends, fix the wrappers that raised on every call (#1)


## Review fixes: task parameter mappings stay raw, upgrading note compares with 4.x


## Responses build their dataclasses with `build`, unknown keys are logged instead of raising (#8)


## ampapi/minecraft.py *w/Claude
- Response dataclasses are built with `build`.
- Replaced the 2 `"status" not in result` checks with `is_response_type()`.
- Narrowed `mc_get_op_whitelist` to `OPWhitelistResponse` and changed its return annotation to `OPWhitelist | OPWhitelistResponse`.
- Marked the 16 endpoints removed in AMP API 2.6.5.0 as `@deprecated`.

## ampapi/generic.py *w/Claude
- Response dataclasses are built with `build`.
- Every GenericModule endpoint is `@Base.generic_only`.
- New `GenericModule` with `import_config`, `refresh_remote_options`, `refresh_tool_discovery`, `reload_generic_config` and `request_server_info`.
	- The two Void endpoints use `no_data=True` and return None.

## ampapi/emailsender.py *w/Claude
- Response dataclasses are built with `build`.
- Added the copyright module docstring.
- Targeted `noqa: N802` on `test_SMTP_settings`, it mirrors the AMP `TestSMTPSettings` endpoint and renaming is breaking.
- Replaced the `"status" not in result` check in `test_SMTP_settings` with `is_response_type()`.

## Version directives on the objects 5.0.0 changes (#14)


## TODO #14: version directives


## Docstring once-over: notes say what the code does, not why it changed


## TODO #2 and #10 done


## Merged #10 worker C (plugins and modules): docstrings name their API endpoint


## Merged #10 worker B (adsmodule.py): docstrings name their API endpoint


## Merged #10 worker A (core.py): docstrings name their API endpoint


## Plugin and module docstrings name their API endpoint


## ampapi/filebackup.py
- Each endpoint method's docstring has an `Endpoint:` line.
- Copyright module docstring.
- One-line class docstring.

## ampapi/generic.py
- Endpoint moved from the end of the summary sentence to its own `Endpoint:` line.

## ampapi/steamcmd.py
- Endpoint moved from the end of the summary sentence to its own `Endpoint:` line.

## ampapi/analytics.py
- Each endpoint method's docstring has an `Endpoint:` line.

## ampapi/emailsender.py
- The endpoint method's docstring has an `Endpoint:` line.

## core.py docstrings name their API endpoint


## adsmodule.py docstrings name their API endpoint


## TODO items carry stable numbers


## CLAUDE.md audit fixes for the recent instance.py changes


## Instance fields AMP sends as null hold their documented default


## Review fix for target_data: a TargetADS keeps the Controller's view of url, is_remote and id


## Merged the target_data worker: TargetADS carries its Target's data, and get_instances updates in place


## A TargetADS carries its Target's data, and get_instances updates objects in place


## docs/instances.rst
- The TargetADS intro mentions the flat Target data.
- The Generic Instance section describes the Generic endpoints, and the GenericInstance section is gone.
- Added the GenericModule Instance section.
- Controller and TargetADS intros describe `targets` and the Instances a Target holds.
- `Instance` and `TargetADS` no longer exclude `app_state`.
	- `Player` keeps its exclusion: it is a NamedTuple, whose field docstrings are only "Alias for field number 0".
- Added the Target ADS Instance section.
- Changed the autoclass targets to `Controller`, `Instance` and `MinecraftInstance`.
- Removed the `AMPADSInstance` section, its replacement `TargetADS` is not exported.
- Excluded `app_state` from the `Instance` members, its Attributes entry already documents it.

## create_local_instance is deprecated


## get_instances always includes the ADS's own Target


## sanitize_path leaves paths to AMP


## Review fixes for todo_batch_2, _call_end_point logs in, and the batch's notes


## Merged the todo_batch_2 worker: trailing slash URL, live shape confirmations and the parameter report


## TODO batch 2: trailing slash URL, shape confirmations and parameter report


## Generic endpoints live on Instance, guarded like the ADS check


## ampapi/steamcmd.py *w/Claude
- Every SteamCMDPlugin endpoint is `@Base.generic_only`.
- New `SteamCMDPlugin` with `steam_username_password`, `steam_guard_code` and `cancel_steam_guard`.
	- URLs use the lowercase `steamcmdplugin/` prefix, because AMP names the module that way.

## Auth evaluation: which ADS a new Instance authenticates with


## Review fixes for the generic_module merge, and the Generic notes


## Merged the generic_module worker: GenericModule and SteamCMDPlugin wrappers, and GenericInstance


## GenericModule and SteamCMDPlugin wrappers, and GenericInstance


## ampapi/_enums.py *w/Claude
- Added `Module.GenericModule`.
- Removed `PostCreateActionsState`; its values never matched AMP's `PostCreateAppActions` (0-5) in any spec from 2.6.2.0 on.
	- Its `start_instance` (1) was AMP's `update_once`, and `every_time` (16) doesn't exist.
- `PostCreateState`'s docstring names every PostCreate parameter it serves.

## ampapi/__init__.py *w/Claude
- Star imports for `generic` and `steamcmd`.
- Dropped `from .util import *`; util's dev functions and its leaked imports (os, re, Path, ...) are no longer on `ampapi`.
	- `from ampapi import util` still works.
- Added `from .errors import *`, so every error class is importable from `ampapi`.
	- `AMPAPITypeError` was only there through util's star import; the other four never were.
- The blanket `ruff: noqa` names its four rules and why.
- Version bump to `5.0.0`; `version_info` now matches it with `releaseLevel="release"`.

## Source (srcds) game spec sheet, and what creating one found


## docs/api_spec_sheets/2.8.0.8/GenericModule_api_spec.md
- The API spec of a Counter-Strike: Source Instance, the template every Source game uses in AMP 2.8.

## docs/api_spec_sheets/README.md
- Lists the GenericModule sheet and why there is no srcds one.
- Added a README covering the `2.6.2.0`, `2.6.5.0` and `2.8.0.8` version directories.
- Documented the gitignored `diffs/` directory and the `amp_api_update`, `compare_api_spec_versions`, `find_missing_endpoints` and `find_parameter_mismatches` functions that build the sheets.

## util.py fixes for amp_api_update and generate_docs_rst


## util.py looks through every Target's Instances


## Review fixes for the TargetADS ownership merge, and the notes it changes


## Merged the TargetADS ownership worker: a Target's Instances belong to its TargetADS


## A Target's Instances belong to its TargetADS


## Remote Instance access modes


## Controller and Target findings


## Routing is a per-object toggle, not a per-call parameter


## Typo fixes


## Post-create actions use AMP's own values


## Each member is documented once, by its own docstring


## ampapi/instance.py
- `app_state` left the `Instance`, `MinecraftInstance` and `TargetADS` Attributes sections; its property documents it.
- Replaced `AMPInstanceState` with `InstanceState` in docstrings.
- Wrapped a long `instances` docstring line and two long lines in the commented-out old get_instances block.
- Removed the commented-out old `__repr__` body.
- `get_instance` docstring spells "ID" in its notes and the `auto_detect` description.
- "Instance" and "URL" in prose.
- `TargetADS` is exported.
- Removed the commented-out old body of `instance_conversion`.
- The `metrics` docstrings give the raw dict type.
- Converted 102 field lines to `name : type`.
- Changed `AMPControllerInstance` to `Controller`, `AMPInstance` to `Instance` and `AMPMinecraftInstance` to `MinecraftInstance` in docstrings.

## Review fixes for C1, the batch's upgrade notes, and TODO caught up


## Merged Worker C1: 2.8.0.8 wrappers, live-payload fixes, filemanager cleanup


## File manager: new 2.8.0.8 wrappers and check_code findings


## Missing 2.8.0.8 wrappers: analytics and backup


## Missing 2.8.0.8 wrappers: Core


## Missing 2.8.0.8 wrappers: ADS module


## Review fix: routed start/stop/restart never fall back silently


## Instance start, stop and restart go to the ADS that holds the Instance


## Live-payload fixes: deployment templates, trigger timestamps, null provision fitness


## AMP setting nodes keep their dotted names


## Review fixes: the AMP version guard works


## Merged Worker B: docs pages, docstring fixes, backoff and emailsender check_code findings


## Upgrade notes: user-visible changes in the 5.0.0 fix batch


## Base and datastore: clearer login errors, opt-in logout, to_dict


## Backups: typed response for GetBackups


## Version checks: the error names the endpoint it guards


## Docs: pages for ResponseHandlerOptions, ExponentialBackoff, the errors and TargetADS


## CreateInstance: defaults AMP accepts


## Minecraft: EULA rejection returns a bool


## Return types: annotations name what AMP sends


## check_code.py findings in backoff.py and emailsender.py


## ampapi/backoff.py *w/Claude
- Moved `Callable` into a `TYPE_CHECKING` block.
- `ExponentialBackoff` uses the Python 3.12 generic class syntax in place of `Generic[T]` and the module level `T`.
	- The constraints and `ExponentialBackoff[bool]` subscripting are unchanged, so the public API is the same.
- Added the `__init__` docstring.
- Targeted `noqa: S311` on the jitter `random.Random()`, it is not cryptographic.

## Docstring fixes: stale enum name and Bridge default


## ampapi/bridge.py
- `Bridge` docstring now says `singleton` defaults to True, matching the signature.
- Converted 6 field lines to `name : type`.
- Fixed the `ap_params` typo in the example to `api_params`.
- Replaced the "Version 5.0" note with `.. versionadded:: 5.0.0`.
- Renamed the `Parameter` heading to `Parameters` so numpydoc parses it.

## Error labels: narrowing errors name the endpoint that was called


## util is a dev module again, errors are importable from ampapi, and older checker findings are cleared
- check_code.py reports zero findings for every file changed since 0303cf2 except util.py, which stays as it is.

## Controller cleanup: old __repr__ notes removed, get_instance says ID


## Instance and URL spelled the library's way across older prose, and _types.py docstrings follow numpydoc
- "instance" -> "Instance" where it means an AMP Instance; Python object senses and parameter names stay lowercase.
- "url" -> "URL" in prose; the `url` parameter stays.

## ampapi/util.py
- "Instance" and "URL" in prose.
- The deferred `docs.samples` import is marked `noqa: PLC0415`.
- Converted 14 field lines to `name : type`.
- Added the API spec sheet parsing and missing endpoint comparison.

## ampapi/key_drift.py
- "URL" in prose.

## README.md
- "Instance" in prose; the APIParams fields named as code.
- The contributing section points to CONTRIBUTING.md; the commit format moved there.
- The upgrade section is now a one-line note under Installing that links the docs page, also linked from the Table of Contents.
- Added a Table of Contents with Issues and Changelog links.
- The 5.0.0 breaking-change note moved out of Installing into its own "Upgrading from 4.x" section.
	- Says 5.0.0 is a major version bump because it breaks backwards compatibility with 4.x, and to pin `cc-ampapi<5` until ready.
	- Lists the new Python 3.12 and AMP 2.6.2.8 minimums.
	- Corrected the moved modules to what 4.6.0 shipped (`controller`, `enums_`, `types_`); `ampapi.dataclass` predates 4.x.
- Pointed the PyPI badge at `cc-ampapi`.
- Added a 5.0.0 breaking release note listing the renamed classes and moved modules.
- Replaced `AMP*Instance` and `AMPInstanceState` with `Controller`, `Instance`, `MinecraftInstance` and `InstanceState` in the feature list, usage steps and Quick Example.
- Fixed the Quick Example imports (`ampapi.dataclass` and `ampapi.enums` are gone), `.available_instances` is now `.instances`, and the instance lookup in the analytics example no longer indexes a set.
- Fixed `AnalyticsFilter(country=...)` and `AnalyticsFilter(username=...)` casing and `top_players`.
- Replaced `.status.state` and `.status.metrics` with the `Status` returned by `get_status()`.
- Fixed the `amp_api_update` note to the real function and signature.

## ID, Instance and Target spelled the library's way in prose


## ampapi/key_drift.py *w/Claude
- `_ENDPOINT_URL_RE` -> `_ENDPOINT_URL_PATTERN`, `out` -> `report_path`.
- `Optional[X]` is written `Union[X, None]`, in signatures and docstrings.
- New dev module. `key_drift()` / `declared_keys()` compare payloads with a TypedDict, the same functions as Minerva's and Python_Template's copies.
- `KeyDriftCheck` reads which TypedDict each endpoint narrows to from the wrapper source (147 endpoints), so nothing is registered by hand.
	- `check()` compares one response; `check_directory()` runs over saved captures and writes a `key_drift.md` report.
	- Run over `_responses/`: 32 captures checked, none drifted after the 2.8 fixes.

## Call them Instances and Targets, not rows and entries


## Review fixes for the TargetADS / get_instance / get_mode work


## get_mode: read the role of the ADS we log in to


## Own ADS id: get_instance returns self, TargetADS gets get_instances


## TargetADS gains the ADSModule methods


## Name-based instance actions resolve on the ADS they are sent to


## ruff format on the five files it flagged; whitespace only


## ampapi/_enums.py
- Blank line before `Module`.

## ampapi/errors.py
- Blank line after the module docstring.

## What a non-admin AMP user can reach, and where an ADS's own id comes from


## The Controller cache guard runs on every Controller


## Where an ADS's role shows, and the Controller cache guard gap


## A Target's Instance on the test VMs, and what its setup needed


## Controller/Target behaviour checked on the test VMs


## ActionResult matches AMP 2.8, and a failed ActionResult says why


## .gitignore
- Ignored `.scripts/`, the dev helpers for the KVM test VMs.
- Ignored `_responses/` and `.local_data/`; untracked `_responses/login.json`.

## Nullable types follow the library's Union[X, None] style


## Contributor guide with the dev tools


## KeyDriftCheck notices AMP changing its response keys


## Controller.get_instances leaves the Controller's own ADS row out


## A failed login raises with a clear reason instead of being swallowed


## TODO.md holds tasks, NOTES.md holds the context behind them


## Status, Port, Backup and Metrics match what AMP 2.8.0.8 sends


## call_end_point is a private dev tool


## Upgrading page covers the method and attribute changes from 4.6.0


## get_oidc_login_url returns the login URL


## Updates holds dataclasses instead of raw dicts


## Status metrics are a Metrics dataclass and the refactor notes are cleaned up


## Upgrading from 4.x is its own docs page


## Merged the docstring separator pass and the url-matched endpoint report
- Docstring field lines use numpydoc's spaced `name : type`, so Pylance links their types.
- The missing endpoint report matches the urls the wrappers post to, regenerated against `2.8.0.8`.

## Missing endpoint report matches on the endpoint url


## docs/api_spec_sheets/missing_endpoints.md
- Regenerated against `2.8.0.8`.

## Docstring parameters use numpydoc's spaced separator


## ampapi/backoff.py
- Converted 2 field lines to `name : type`.

## Merged the 5.0.0 code fixes
- Pyright is at 0 errors for the package, down from 166, and an installed `ampapi` imports again.

## Bridge docstring renders correctly for the 5.0.0 release


## Docstrings and annotations use the current class names


## get_oidc_login_url forwards redirect_uri, matching the 2.8.0.8 spec


## util.py type checks clean: undefined names, schedule data and spec parsing


## docs/samples/sample.py *w/Claude
- Back to `logger.error` in the `except` blocks, matching the original sample.
- Replaced the six removed imports with `Controller`, `Instance`, `MinecraftInstance`, `InstanceState` and `AMPAPIError`.
- Replaced the `ActionResultError` isinstance checks with `try`/`except AMPAPIError`, since errors are raised now.
- Fixed the stale comments about `.Running`, `get_status()` and `State_enum`, and the double space in `players: Players`.

## Merged the 5.0.0 docs refresh
- README, samples and the Sphinx pages now use the 5.0.0 names; the docs build has 0 warnings, down from 37.

## Changelog headers follow the commit's own depth


## .github/workflows/scripts/gen_changelog.py *w/Claude
- Headers are one `#` deeper than the commit line and always spaced, so `# file.py` becomes `## file.py` and `## Sub` nests as `### Sub`.
	- Lines written `#file.py` with no space come out as `## file.py` too.
- Fixed the root of the dropped first line; `git log` was passed `'--format="%B"'`, and without a shell the quotes are literal.
	- Every commit's theme line started with `"`, so it was never read as a header and a `$` first line was never skipped.
	- Uses `--format=%B` now; the per-line `strip('"')` added earlier also cut a real quote off the end of a bullet.
- Replaced the em dash in the version search comment.
- Version lookup accepts both `# Version -` and the older `## Version -` headers.
	- Without this every header missed and the script took the initial-repo path, writing the whole log as one entry.
- Fixed the first line of every commit being dropped; `--format="%B"` quotes it, so theme headers and `$` lines were missed.
- Branch check uses `git branch --show-current` instead of the first line of `git branch`.
- Version lookup searches for the header instead of assuming line 0.

## Analytics summary narrowed with is_response_type instead of typing.cast


## Spec sheet directory explained


## Sphinx docs pointed at the 5.0.0 names


## Directory listings accept IsSmartExcludedFromBackups from newer AMP (PR #27 port)


## ActionResult and OPWhitelist responses narrowed with is_response_type


## README and sample updated to the 5.0.0 API


## docs/samples/settings_node_usage.py
- Fixed the `set_instance_config` examples to await the call on a `Controller` with a `str` value.

## Installed package imports again: dev-only doc import moved into its function


## Changelog generator fixes


## docs/conf.py
- Set `default_role = "py:obj"`; single backticks now cross-reference instead of rendering in italics.

## Packaging and CI for 5.0.0


## ampapi/py.typed
- Added the PEP 561 marker to match the `Typing :: Typed` classifier.

## .readthedocs.yaml
- Removed the root `requirements.txt` install, the file no longer exists.

## docs/requirements.txt
- Pinned `sphinx<9`; Sphinx 9 removed `sphinx.ext.autodoc.logger`, which `enum_tools.autoenum` imports.

## Merged `main` into `Refactor`
- Kept the `Refactor` tree whole; the 4.x changes on `main` are superseded by the rewrite.
- PR #27 (`is_smart_excluded_from_backups` on `Directory`) is ported by hand in a later commit.

## Refactor baseline for 5.0.0
- Every endpoint now goes through `_post`, with its response narrowed to a per-endpoint `*Response` TypedDict.
- Removed `controller.py`; `Controller`, `Instance`, `MinecraftInstance` and `TargetADS` live in `instance.py`.
- Python 3.12 is now the minimum.

## ampapi/_enums.py, errors.py, emailsender.py, bridge.py, backoff.py, __init__.py
- Formatting and docstring updates.

## NOTES.md, TODO.md, numpy_template/, docs/
- Added developer notes, the docstring attribute tool and the 2.8.0.8 spec sheets.

## Further Refactor Changes
- Fixed recursion bug in `call_end_point` function.
- Added a `clean_up()` function to `Base()` to close open session connection.
- Renamed `types_.py` and `enums_.py` to `_types.py` and `_enums.py` for consistency.
- Updated License block in multiple files.
- Added debug logic and futher response handling to `Base()._response_handler()`
- Began commenting out older code and un-used functions soon to be replaced.

#### Finilazed Bridge Singleton structure.
- Added launch.json and settings.json for .vscode setups.
- Plan to provide local scripting file in future releases to assist with other developers for testing.

## Bridge.py
- Added support for multi instance <Bridge> construction or Singleton approach. Default is still Singleton.

## Base.py
- Changed from a GLOBAL attribute to using a ClassVar for handling data formatting.
- Updated "__init__" to support non Singleton Bridge type setups.
- Updated multiple private/public attributes to property's without setters for a more "pythonic" approach.
- Updated LOGGER calls throughout file.

## Begining of the Rewrite...
- Added new aiohttp.ClientRequest function called "_post".
- Response handling from "_post" is now done by "_response_handler" and both functions have multiple **kwargs to control the flow and results.
- Added functionality during response handling to allow writing the JSON response to a file.
- Rewrote Login endpoint as a test with the new post function handling.

## Refactor [Implement request, API handling]
- Added functionality to parse differences between AMP API versions.
- Added a "missing" endpoint comparison tool.
- General NumPy formatting changes.
- Added versioning breakdowns for API spec sheets (endpoint collection).
- Added functionality to check function parameters vs API endpoints.

## Version - 4.6.1 - [74ee99a](https://github.com/k8thekat/AMPAPI_Python/commit/74ee99a)
#### Changelog.md
- Version info from `4.5.3` added.

#### __init__.py
- Version bump to `4.6.1`

#### Overall
Merge pull request #25 from k8thekat/23-getting-deprecated-warning-when-using-library
Updated support for AMPs new Authorization Header.
Updated support for AMPs new Authorization Header.
Developer"
Developer"
Developer"
Developer

## Version - 4.5.3 - [7e4ebc5](https://github.com/k8thekat/AMPAPI_Python/commit/7e4ebc5)
#### Changelog.md
- Version info from `4.5.2` added.

#### __init__.py
- Version bump to `4.5.3`

#### v4.5.3
- Brief formatting update to logger statements throughout.
- Added `__name__` to all Loggers.
- Overwrote the dunder method for `ActionResultError.__str__()`.

## Version - 4.5.2 - [76c4c13](https://github.com/k8thekat/AMPAPI_Python/commit/76c4c13)
#### Changelog.md
- Version info from `4.5.1` added.

#### __init__.py
- Version bump to `4.5.2`

#### base.py
- Changed format of debug logger statements.
- Fixed logic handling for closed sessions and attempting to re-create a ClientSession().

#### instance.py
- Removed unneeded debug print in it's init.

## Version - 4.5.1 - [87e6630](https://github.com/k8thekat/AMPAPI_Python/commit/87e6630)
#### Changelog.md
- Version info from `4.5.0` added.

#### __init__.py
- Version bump to `4.5.1`

#### base.py
- Pulled back connection closing via `Base` to be controlled by the AMPControllerInstance instead.

## Version - 4.5.0 - [99b12f5](https://github.com/k8thekat/AMPAPI_Python/commit/99b12f5)
#### Changelog.md
- Version info from `4.4.0` added.

#### __init__.py
- Version bump to `4.5.0`

#### base.py
- Implemented a backoff class from `discord.py`-> ExponentialBackoff.
- Improved logic handling for `aiohttp.ClientSession` requests upon failure or similar.
- Added logic to attempt to reopen the ClientSession should it become closed.

## Version - 4.4.0 - [886b0e4](https://github.com/k8thekat/AMPAPI_Python/commit/886b0e4)
#### Changelog.md
- Version info from `4.3.0` added.

#### __init__.py
- Version bump to `4.4.0`

#### Overall
- Added logic to support a single `aiohttp.ClientSession` at runtime while allowing an existing ClientSession to be supplied at the class `AMPControllerInstance` level.
- Updated the `sample.py` to show existing session usage.

## Version - 4.3.0 - [d2e2634](https://github.com/k8thekat/AMPAPI_Python/commit/d2e2634)
#### Changelog.md
- Version info from `4.2.0` added.

#### __init__.py
- Version bump to `4.3.0`

#### Overall
- Fixed Type annotations on multiple modules which was breaking data building.

## Version - 4.2.0 - [7afa8d7](https://github.com/k8thekat/AMPAPI_Python/commit/7afa8d7)
#### Changelog.md
- Version info from `4.1.2` added.

#### __init__.py
- Version bump to `4.2.0`

#### adsmodule.py
- Docstring change.

#### base.py
- Fixed parameter type for `parse_data` as it was refrencing the wrong data module.

#### core.py
- Fixed function `get_status`, the data module it was returning was incorrect and failing. Changed from `InstanceStatus` to just `Status`.
	- Updated docstring to match.

#### instance.py
- Fixed function `get_application_status` in tangent to `Core.get_status` as both were incorrect.
	- Updated docstring to match.
	- Added a warning in regards to using this function on an Controller/Target Instance.

## Version - 4.1.2 - [dc08462](https://github.com/k8thekat/AMPAPI_Python/commit/dc08462)
#### Changelog.md
- Version info from `4.1.1` added.

#### __init__.py
- Version bump to `4.1.2`

#### Overall
- Added a `_no_data` check to `_call_api` function to return None early.

## Version - 4.1.1 - [c12da9f](https://github.com/k8thekat/AMPAPI_Python/commit/c12da9f)
#### Changelog.md
- Version info from `4.1.0` added.

#### __init__.py
- Version bump to `4.1.1`

#### controller.py
- Return type handling for `get_instance` via overloads added.

## Version - 4.1.0 - [a93505e](https://github.com/k8thekat/AMPAPI_Python/commit/a93505e)
#### Changelog.md
- Version info from `4.0.0` added.

#### __init__.py
- Version bump to `4.1.0`

#### Overall
- Hotfix for import errors and docs.
- Implemented `ActionResultError` class to handle any Exceptions inside of `_call_api` which all endpoints use.

#### controller.py
- Created overloads for `instance_conversion` function and added logic to handle a single `Instance` class.
- Created a function `get_instance` to get a single Instance via "Instance ID" and convert the Instance to it's respective class.

## Version - 4.0.0 - [426bad9](https://github.com/k8thekat/AMPAPI_Python/commit/426bad9)
#### Changelog.md
- Version info from `2.0.0` added.

#### __init__.py
- Version bump to `4.0.0`

#### adsmodule.py
- Partial refactor of parameter key values as AMP refactors the API parameters to match PascalCase..lol
- `attach_ads()` has new parameters and was merged with `attach_ads_with_pairing_code` to simplfy code.
- `set_instance_network_info` has new parameters, "must_stop" and "application_ip".
- Added new functions!
	- `cancel_pairing`
	- `create_instance_from_spec`
	- `get_target_pairing_code`
	- `register_target_with_code`

#### core.py
- Updated `get_oidc_login_url` with new parameters as the API was updated.
- New function, `oidc_login` and `update_public_key`.

#### filebackup.py
- Updated `take_backup` with new parameters, "local" and "s3".

#### minecraft.py
- New function `mc_reject_eula`.

#### modules.py'
- Added a new function to `CreateInstance` to convert the class into a useable datastructure for the API.

#### utils.py
- Updated `amp_api_update` function to get the most current version of any Instance as long as it matches the ADS version.

#### Overall
- Updated docs.
- Relocated classes from `dataclass.py` file into `modules.py`.
- Added attributes to docstring of `AMPControllerInstance` and any other classes that inherit from `Instance` dataclass.
- Updated docs to reflect changes.
- Updated `sample.py` to reflect changes.

## Version - 2.0.0 - [c765d8f](https://github.com/k8thekat/AMPAPI_Python/commit/c765d8f)
#### Changelog.md
- Version info from `1.3.2` added.

#### __init__.py
- Version bump to `2.0.0`

#### base.py
- Updated formatting of `debug` logger statements in `_call_api()`.
- Fixed logic error when handling api response not returning the data correctly.(This may break older versions of AMP)
- Updated logic inside `json_to_dataclass` as it was returning None on certain edge cases when it should just return the data.

## Version - 1.3.2 - [ac4118a](https://github.com/k8thekat/AMPAPI_Python/commit/ac4118a)
#### Changelog.md
- Version info from `1.3.1` added.

#### __init__.py
- Version bump to `1.3.2`

#### controller.py
- Updated type definitions for `get_instances()` via overloads.

#### Readme.md
- Formatting change to Contributing to the Project section.

## Version - 1.3.1 - [cad740f](https://github.com/k8thekat/AMPAPI_Python/commit/cad740f)
#### Changelog.md
- Version info from `1.3.0` added.

#### __init__.py
- Version bump to `1.3.1`

#### Overall
- Updated Readme with better examples of importing the package.
- Fixed Example URL being broken and now re-directs to github Sample.

## Version - 1.3.0 - [24d971b](https://github.com/k8thekat/AMPAPI_Python/commit/24d971b)
#### Changelog.md
- Version info from `1.2.1` added.

#### __init__.py
- Version bump to `1.3.0`

#### base.py
- Fixed logic error in `_connect()` method not handling 2FA codes properly.

## Version - 1.2.1 - [1b814ff](https://github.com/k8thekat/AMPAPI_Python/commit/1b814ff)
#### Changelog.md
- Version info from `1.2.0` added.

#### __init__.py
- Version bump to `1.2.1`

#### Overall
- Updated `docs/events` and `/docs/nodes` rst files.
- Fixed missing dynamic entry for dependencies.

#### core.py
- Fixed typo in docstring for `get_user_list()`.

#### dataclass.py
- Changed formatting of `__repr__` for the `Instance` class.

#### minecraft.py
- Formatted imports and updated docstrings as this file was ommitted from the docs.

#### index.rst
- Fixed link for `Quick Example`.

#### instances.rst
- Changed wording to not be as confusing/redundant.

#### modules.rst
- Added the missing *Minecraft Module*.

## Version - 1.2.0 - [7be6620](https://github.com/k8thekat/AMPAPI_Python/commit/7be6620)
#### Changelog.md
- Version info from `1.1.2` added.

#### __init__.py
- Version bump to `1.2.0`

#### Overall
- Updated for v`2.6.0.12`
- Updated API Spec Sheets and RST files.

#### Core.py
- New fucntion `get_oidc_login_url()` to work with AMPs OIDC support.

#### Util.py
- Sorted Imports.
- Fixed logic inside `_permission_node_parse()` which could make it fail if no children attributes existed for the Permission Node.

## Version - 1.1.2 - [212fecc](https://github.com/k8thekat/AMPAPI_Python/commit/212fecc)
#### Changelog.md
- Version info from `1.1.1` added.

#### __init__.py
- Version bump to `1.1.2`

#### pyproject.toml
- Removed unsed lint rule.

#### samples.py
- Fixed example of using Players from a Minecraft server updated to reflect changes due to #16 .

## Version - 1.1.1 - [bac0a57](https://github.com/k8thekat/AMPAPI_Python/commit/bac0a57)
#### Changelog.md
- Version info from `1.1.0` added.

#### __init__.py
- Version bump to `1.1.1`

#### Overall
Initialise self.sorted"
Issue fixes and documentation update."
Developer"
Removed merg notes from changelog"
Developer

## Version - 1.1.0 - [2c8094f](https://github.com/k8thekat/AMPAPI_Python/commit/2c8094f)
#### Changelog.md
- Version info from `1.0.7` added.

#### __init__.py
- Version bump to `1.1.0`

#### __init__.py
- Version bump to `1.1.0`
- Version bump to `1.1.0`

#### nodes
- Updated documentation for permission and setting nodes.
- Removed merge messages.

#### pyproject.toml
- Changed the readme property's file extension and content-type.
- Removed comment.

#### build.yml
- Removed comment.

#### core.py
- Fixed issue mentioned in #13
	- All connected players are represented in a `Players` dataclass. You can access the list via the `sorted` attribute.
- Fixed typo on LN1459.

#### dataclass.py
- New `Players` Dataclass and a `Player` NamedTuple to house the data.
	- `Players.get_player(name_or_uuid: str)` now exists to allow for searching of players by name or uuid.

#### index.rst
- Fixed incorrect information throughout.

#### types.rst
- Added API Modules.

#### README.md
- Fixed incorrect information throughout.

## Version - 1.0.7 - [8bb2fdc](https://github.com/k8thekat/AMPAPI_Python/commit/8bb2fdc)
#### Changelog.md
- Version info from `1.0.6` added.

#### __init__.py
- Version bump to `1.0.7`

#### Overall
- config changes for pyproject.toml to support dynamic versions.

## Version - 1.0.6 - [069d040](https://github.com/k8thekat/AMPAPI_Python/commit/069d040)
#### Changelog.md
- Version info from `1.0.4` added.

#### __init__.py
- Version bump to `1.0.6`

#### conf.py
- Changed conf.py path's to relative.

#### core.py
- Removed un-used imports.
- Removed `events` property as I did not want to support them as MC support is changing via the API.

#### modules.py
- Updated docstring for `TriggerID`.
- Update/fixed pyproject.toml definitions.
- Fixed comparison logic on multiple files.
- Removed un-used imports.

## Version - 1.0.4 - [778c229](https://github.com/k8thekat/AMPAPI_Python/commit/778c229)
#### Changelog.md
- Version info from `1.0.3` added.

#### __init__.py
- Version bump to `1.0.4`

#### Overall
- Updating project metadata and configs for RTD and Pypi.

## Version - 1.0.3 - [b06f874](https://github.com/k8thekat/AMPAPI_Python/commit/b06f874)
#### Changelog.md
- Version info from `1.0.2` added.

#### __init__.py
- Version bump to `1.0.3`

#### readme.md
- Updated content regarding contributing and git commit formatting.

## Version - 1.0.2 - [08eaab4](https://github.com/k8thekat/AMPAPI_Python/commit/08eaab4)
#### Changelog.md
- Version info from `1.0.1` added.
#### __init__.py
- Version bump to `1.0.2`

#### Overall
- Changed the Pypi project name from `cubecoders_amp_api_wrapper` to `cc-ampapi`. Thanks @fret
- Added rdt.yaml.

## Version - 1.0.1 - [448e6ee](https://github.com/k8thekat/AMPAPI_Python/commit/448e6ee)
#### Changelog.md
- Version info from `1.0.0` added.
#### __init__.py
- Version bump to `1.0.1`

#### Overall
- Version bump v`1.0.1`
- Finished numpy docstring conversion throughout codebase.
	- implemented a different numpy-template for better Sphinx autodoc support and layout.
- Began conversion of data returns from Dataclasses to something simpler like TypedDicts and class definitions.
- Developed functions to generate .rst and API docs.
- Changed parameters of multiple functions for similarity and ease of understanding.
- updated docstring numpy format.
- added .rst files for Trigger events.
- added .rst files for Method events.
- added `types_.py` to further define JSON response data.

## Version - 1.0.0 - [922a08b](https://github.com/k8thekat/AMPAPI_Python/commit/922a08b)
#### Changelog.md
- Version info from `0.3.0` added.
#### __init__.py
- Version bump to `1.0.0`

#### Overall
- Implementation of Sphinx documentation.
- Added `gitHub` actions to handle changelog building.
- Switched to `pyproject.toml` and `ruff`.
	- Changed docStrings to `numpy`.
- Added LICENSES for MIT for borrowed libraries.
- Restructured dataclass file layout and enums.
- Auto-generator for Setting Nodes/Permission Node rst files.

## Version - 0.3.0 - [68556f7](https://github.com/k8thekat/AMPAPI_Python/commit/68556f7)
#### Changelog.md
- Version info from `0.2.0` added.
#### __init__.py
- Version bump to `0.3.0`

#### Overall
- Fixed script patths
- Updated to `2.5.1.4` | Build: `20240731.1`

#### __init__.py
- Version bump `0.3.0`.

#### ads.py
- Updated docstring to better communicate the point/usage of the `class ADSInstance()`.
- Updated function docstring's to a better format.
- Changed `AvailableInstances()` to a set.
- Changed
- Updated `property AvailableInstances()` docstring to give better information/understanding of what it returns.
	- Improved logic to include the `ADSInstance()` class to our `AMPMinecraftInstance()` and `AMPInstance()` inits.
- Added `AppState` property.

#### adsmodule.py
- Added `ADSonly` decorator to every function to validate the Module is correct before making the API call.
- Updated function docstring's to a better format.
- Changed logic handling for passed in dataclass's for multiple methods.
- Added type hinting throughout.

#### analytics.py
- Implementation of `class AnalyticsPlugin()`.
	- Added a `get_analytics_summary()` function which supports a `period_days`, `start_date` and `filters`.

#### base.py
- Updated function docstring's to a better format.
- Added `ADSonly()` decorator to validate the Module is of `ADS`.
- Added `online()` decorator to check if the Instance is `Running`.
- Added a length check to the `token` parameter of the Bridge.
- Added type hinting throughout.
- Added debug prints to `_call_api()`
- Added a `_no_data` parameter to `_call_api()` to support endpoints without data returns.

#### bridge.py
- Updated function docstring's to a better format.

#### core.py
- Updated function docstring's to a better format.
- Made `start_instance()`, `stop_instance()`, `restart_instance()` and `kill_instance()` deprecated.
	- Replaced with `start_application()`, `stop_application()`, `restart_application()` and `kill_application()`.
- Added `run_security_check()` - UNK data return, waiting on info.
- Made `update_amp_instance()`, `restart_amp()` and `upgrade_amp()` ADS only methods as that is their intention.

#### emailsender.py
- Updated function docstring's to a better format.

#### filebackup.py
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### filemanager.py
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### instance.py
- Added a `debug` print to the `__init__()`.
- Fixed attribute access issues and added docstring's to commonly used properties for better clarification.
- Added `start()`, `stop()`, `restart()` and `update()` functions to control the Instance from inside the Instance.
- Added `online()` decorators to validate an instance is `Running`.
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### minecraft.py
- Added a `MConly()` decorator to check the instance Module is `Minecraft`.
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### types.py
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### util.py
- Updated function docstring's to a better format.
- Added type hinting throughout.

#### docs/
- Updated ADS API Spec
- Updated Minecraft API Spec
- Version info from `0.2.0` added.

## Version - 0.2.0 - [4b70f0d](https://github.com/k8thekat/AMPAPI_Python/commit/4b70f0d)
#### Changelog.md
- Version info from `0.1.11` added.
#### __init__.py
- Version bump to `0.2.0`

#### Readme.md
- Updated naming of methods in Quick Example.
	- Added a Sample_Analytics_API() method.
- Added a section called Basic Usage to help people understand how to setup the Bridge and API Params.

#### __init__.py
- Version bump `0.2.0` release.

#### ads.py
- Removed `LocalFileBackupPlugin` from ADSInstance class inheritance as the ADS no longer has backup functionality.
- Removed un-used imports.

#### analytics.py
- New API class to support AMP `2.5.1.0` Update which introduces Analytics!
- Added `get_analytics_summary()` method to retrieve the Instance Analytics Summary.

#### core.py
- Added `get_authentication_requirements()` method to retrieve a users Auth requirements.

#### emailsender.py
- Added `test_SMTP_settings()` method to validate SMTP settings for an Instance.

#### filebackup.py
- Added `refresh_backup_list()` method to refresh the list of backups an Instance has.

#### instance.py
- Added `AnalyticsPlugin()` API class to `AMPInstance` class inheritance for the new Analytics feature from `2.5.1.0`.

#### base.py
- Fixed typo in `parse_data()` docstring.

#### types.py
- Added dataclasses for Analytics.
	- Added `Analytics_Filter()` to assist with filtering Analytics API call.
	- Added `Analytics_Summary()` to handle the data from `get_analytics_summary()` method call.
	- Added `Analytics_Country_data()`, `Analytics_Stats()` and `Analytics_Top_Players()`  to assist attributes of `Analytics_Summary()`.

#### util.py
- Added an `AMP_to_API_update()` method to wrap over `parse_get_api_spec()`. *No current usage at this time*
- Changed `parse_get_api_spec()` to a staticmethod.
- Fixed typo in version syntax.

#### Changelog.md
- Version info from `0.1.11`.

## Version - 0.1.11 - [4b8c37a](https://github.com/k8thekat/AMPAPI_Python/commit/4b8c37a)
#### requirements.txt
- Changed all version checks to be equal to or greater than the package version.

#### Changelog.md
- Version info from `0.1.1`.

#### __init__.py
- Version bump `0.1.11`

#### Overall
- Added `ADS_api_spec.md` document.

## Version - 0.1.1 - [0cf953e](https://github.com/k8thekat/AMPAPI_Python/commit/0cf953e)
#### __init__.py
- Version bump `0.1.1`
- Changed formatting of releaseLevel and `__version__` to match *PEP440*

#### changelog.md
- Version info from `0.0.42b` and `0.1.0r`

## Version - 0.1.0r - [ac16314](https://github.com/k8thekat/AMPAPI_Python/commit/ac16314)
#### __init__.py
- Version bump to `0.1.0r`
- Changed `releaseLevel` to "release"
- Version bump `0.1.0r`

#### setup.py
- Changed classifiers from "Alpha" to "Production/Stable"

#### ads.py
- Added `_AvailableInstances` as an attribute to better handle population of `AvailableInstances` attribute.
- Added `_Controller_exists` as an attribute to catch attribute errors for the Controller dataclass that ADSInstance inherits from when accessed prior to class creation/population.

#### adsmodule.py
- Updated `detatch_target` to `detach_target` to align with the `v2.5.0.12` AMP Update.
- Updated the API endpoint for `detach_target` to align with the `v2.5.0.12` AMP Update.

#### base.py
- Added parameter declaration to the `fields()` method.

#### core.py
- Formatting change on one line.
- Updated return type for `get_api_spec()`

#### types.py
- Added `to_str()` method to the `AMP_Version()` dataclass to be used for future plans.
- Removed an un-needed `# type:ignore`

#### util.py
- Formatting changes on multiple lines.
- Re-wrote logic for `parse_get_api_spec()`
	- Added the `@classmethod` decorator for usage prior to `APIUtil` class generation.
	- Added Instance Type, Version and Build strings to the output document to better compare API changes between versions.
	-- Improved formatting of data output from API parsing.

## Version - 0.0.42b - [2bf7996](https://github.com/k8thekat/AMPAPI_Python/commit/2bf7996)
#### Changelog.md
- Version info from `0.0.41b`

#### __init__.py
- Version bump `0.0.42b`

#### README.md
- Added missing `await` in Quick Example - Sample_API().

#### ads.py
- Changed some prints to `_logger.debug()`.
- Type-hinted `ads_list` inside `get_instances()` method.
- Added logic check to `get_instances()` when not formatting data to prevent error.

#### base.py
- Removed `type:ignore` from `__init__()`.
- Added return value to `format_data` setter.
- Added `_logger.debug()` for monitoring data formatting.
- Fixed logic when formatting data causing return failure using the `ADSInstance` class.
- Improved readability of format logic of `_call_api()`.

#### bridge.py
- Added logging.
- Changed `apiparams` to `api_params`.
- Added type-hinting to `__new__()`.
- Added `_logger.debug()` to `__init__()`.

#### minecraft.py
- Removed unused imports.

#### types.py
- added `repr = False` to the `Controller()` dataclass.

## Version - 0.0.41b - [5b0aed8](https://github.com/k8thekat/AMPAPI_Python/commit/5b0aed8)
#### __init__.py
- Version bump `0.0.41b

#### types.py
- Added `LastExecuteError` and `LastErrorReason` to `Triggers()` dataclass.

#### base.py
- Removed un-used code.

#### Changelog.md
- Version log - `0.0.40b`

## Version - 0.0.40b - [b055fb3](https://github.com/k8thekat/AMPAPI_Python/commit/b055fb3)
#### Readme.md
- Changed TestPypi to Pypi
	- Updated bash commands for installing package.

#### init.py
- Version bump `0.0.40b`

#### Overall
- `isort` imports

## Version - 0.0.39b - [778bb87](https://github.com/k8thekat/AMPAPI_Python/commit/778bb87)
#### __init__.py
- Version bump `0.0.39b`
- Added `MANIFEST.in`

#### setup.py
- Re-added requirements.txt

## Version - 0.0.38b - [970db4b](https://github.com/k8thekat/AMPAPI_Python/commit/970db4b)
#### setup.py
- Changed `install_requires` to a list instead of a prepopulated list.

#### __init__.py
- Version bump `0.0.38b`

## Version - 0.0.37b - [63121cc](https://github.com/k8thekat/AMPAPI_Python/commit/63121cc)
#### __init__.py
- Version bump `0.0.37b`

#### requirements.txt
- Removed `setuptools`

## Version - 0.0.36b - [c9417a3](https://github.com/k8thekat/AMPAPI_Python/commit/c9417a3)
#### __init__.py
- Version bump `0.0.36b`

#### Changelog.md
- Fixed typos.

## Version - 0.0.35b - [585ecf3](https://github.com/k8thekat/AMPAPI_Python/commit/585ecf3)
#### __init__.py
- Version bump `0.0.35b`

#### README.md
- Updated description and key features.
- Added coding examples.

#### requirements.txt
- Added `setuptools` to requirements.

#### ads.py
- Removed unused methods.

#### base.py
- Changed type check of `parse_data()` data parameter.

#### core.py
- Changed return type `Status` to `AppStatus`.

#### types.py
- Changed `Status` to `AppStatus`.

#### instance.py
- Added `State` property to return `AppState`
- Added `AppStatus` and `Updates` to class inheritance.
- Added `.get_status()` methods to AMPInstance to set self class attributes.
- Added `get_updates()` methods to AMPInstance to set self class attributes.

## Version - 0.0.34b - [9ac1e3c](https://github.com/k8thekat/AMPAPI_Python/commit/9ac1e3c)
#### __init__.py
- Switched from `ALPHA` to `BETA`
- Version bump `0.0.34b`

#### Readme.md
- Updated documentation.
- Referenced the package as a wrapper now.

#### setup.py
- Updated name and description to properly represent the package as a wrapper.

#### ads.py
- Removed prints from development.
- Updated doc strings and methods for `format_data` parameter.
- Added logic for when there is no instances from `get_instances()`

#### adsmodule.py
- Added all endpoints for "API/ADSModule/".
- Formatted `get_instance()` to pep8.

#### base.py
- Added global var `FORMAT_DATA`
- Added time to live value for sessions. See `session_ttl`, default 240 seconds.
- Added `FAILED_API` for exception raising.
- Added `format_data` property to access the global `FORMAT_DATA`
- Added `camel_case_data()` method to camel case keys of a dictionary.
- Added `dataclass_to_dict()` to unpack a dataclass into a dictionary.
- Added `json_to_dataclass()` to format the JSON response from API calls into dataclasses.
- Refactored `_call_api()` and added support for `FORMAT_DATA`.
	- Moved data formatting into `json_to_dataclass()` method.
- Refactored `_connect()` and improved session handling.

#### bridge.py
- Removed commented out code and commented out print statements.
- Revered `Self` change due to import error.

#### core.py
- Added remaining `API/Core` endpoints and added `format_data` functionality.
- Updated doc strings.

#### filebackup.py
- Updated method functionality to support `format_data`.
	- Updated doc strings to match.
- Finished remaining API endpoints.
	- TODO - Finish return types.

#### filemanager.py
- Updated method functionality to support `format_data`.
	- Updated doc strings to match.
- Finished remaining API endpoints.
	- TODO - Finish return types.

#### instance.py
- Commented out print statements.

#### minecraft.py
- Updated method functionality to support `format_data`.
	- Updated doc strings to match.

#### types.py
- Added multiple dataclasses to support added Endpoints.
- Added `APIParams()` to better assist users with connection setup.
- Added `APISession()` to better handle session TTL values.
- Updated multiple dataclasses to better handle data formatting.

# Overall
- Removed `api_spec.md` and created Instance Module specific documents.

#### utils.py
- Added `instance_type` parameter to `parse_get_api_spec()` to differentiate API endpoint specs in files.

# setup.py
- Added `CHANGELOG.md` to packages.

#### Changelog.md
- Version bump `0.0.33a`.

## Version - 0.0.33a - [4df55fa](https://github.com/k8thekat/AMPAPI_Python/commit/4df55fa)
#### __init__.py
- Version bump `0.0.33a`.

#### Changelog.md
- Version bump `0.0.33a`.

#### ads.py
- Added `if TYPE_CHECKING` for Self

#### bridge.py
- Added `if TYPE_CHECKING` for Self

## Version - 0.0.32a - [a3973cc](https://github.com/k8thekat/AMPAPI_Python/commit/a3973cc)
#### __init__.py
- Version bump to `0.0.32a`.
- Version bump `0.0.31a`

#### Changelog.md
- Fixed layout of Version line.

#### ads.py
- Added logic to check `Instance.Module` attribute to create `AMPMinecraftInstance`.
- Updated `ADSInstance.AvailableInstances` return types to include `AMPMinecraftInstance`.

#### adsmodule.py
- Added docstring to `add_datastore()`.
- Added `await self._connect()` to all methods.

#### base.py
- Added `MINECRAFT_ONLY` attribute for logic checks.
- Removed `await self._connect()` from `_call_api()`.

#### core.py
- Added `await self._connect()` to all methods.

#### filebackup.py
- Added `await self._connect()` to all methods.

#### filemanager.py
- Added `await self._connect()` to all methods.
- Added comments for remaining filemanager methods.

#### instance.py
- Updated `__init__()` print debug for better naming conventions.
- Added `__all__` property to include `AMPInstance` and `AMPMinecraftInstance`.
- Added `AMPMinecraftInstance` class.

#### minecraft.py
- Creation of all Minecraft specific API endpoints and methods pertaining to them.
- Partial completion of dataclasses, docstrings and return types.
- Implemented logic to check `.Module` != `Minecraft` on all calls to prevent failure outside of the Instance class.
- Prefixed all methods with `mc_`.

#### types.py
- Added `BukkitPlugin()` dataclass.

# Changelog.md
- Creation of Changelog.md and added `0.0.30a` under `0.0.31a`

#### Setup.py
- Added `project_urls` to `setup()`
	- Github and Changelog links

#### Base.py
- Added `TYPE_CHECKING` to fix `Self` import at runtime error.

## Version - 0.0.31a - [8dce4d6](https://github.com/k8thekat/AMPAPI_Python/commit/8dce4d668550a3dd2794c4040596d9f5077aba02)
#### Overall Changes -
- Update "DEBUG" prints to provide better information. 
- Added *ADS Only* requirements to specific end points to prevent failure. -
- Version bumped `__init__.py`

#### Setup.py
- Added `project_urls=`
    - Added *Github* and *Changelog* links for Pypi.

#### Core.py -
- Added `Core.add_datastore()`. 
- Added `Core.get_api_spec()` to access API information for an ADS or Instance.

#### Base.py -
- Moved `Base._on_connect()` into `Base._call_api()` to simply code. 
- Added docstring to `Base.parse_data()`
- Fixed camelcase issue with `Base.InstanceId` to `Base.InstanceID` to match Controller to Instance dataclass. 

#### Util.py -
- Added `APIUtil.parse_get_api_spec()` to create the `./docs/api_spec.md` 
- Fixed filepaths for `APIUtil` functions to point to `../docs/`

#### Instance.py -
- Added `AMPInstance` class to bring together API and Instance dataclass similar to `ADSInstance`

#### Minecraft.py -
- Added `minecraft.py` to house `MinecraftModule` API endpoints. (Still needs dataclasses/returns finished) 
