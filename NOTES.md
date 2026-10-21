# AMP API Notes

Developer context for the library. Anything useful that is not a task (`TODO.md`) or a
released change (`CHANGELOG.md`).


## Response narrowing

`Base._post` returns `ResponseTypeAlias | str | bool | None`. Endpoints narrow that union down
to one TypedDict before touching it, using the `is_response_type()` / `is_response_list()`
predicates in `_types.py` paired with the `*_REQUIRED_KEYS` / `*_EXCLUDED_KEYS` tuples.

Both predicates return a `TypeGuard`, which replaces the type outright. A TypedDict therefore
does **not** have to be a `ResponseTypeAlias` member to be a narrowing target — `TimedTriggerResponse`,
`SettingsSpecParentResponse` and `UserApplicationDataResponse` are all narrowed to without joining
the union, which keeps them out of the key-collision problem below.

The `*_EXCLUDED_KEYS` tuples exist because several responses share a key. `status` is the worst
offender - `ActionResultResponse`, `RunningTaskResponse` and `UpdatesResponse` all carry one, so
the first is identified by excluding the other two's unique keys rather than by a key of its own.
Adding a TypedDict to `ResponseTypeAlias` can force an existing excluded tuple to grow; adding one
outside the union cannot.


## Dataclasses vs. the raw JSON

Response dataclasses are built with `build(Cls, result)` (`modules.py`), never `Cls(**result)` and never `cast`.
`sanitize_json` has already snake_cased the keys by then. `build` reads the field type hints (cached per class) and
builds nested dataclasses through lists and unions, trying a union's members in order, so the dataclass goes first
(`list[DCConsumes] | list[ConsumeResponse]`). A key the dataclass doesn't declare is dropped and logged once per
class and key at WARNING. 4.x used dataclass-wizard's `fromdict`, which dropped them silently, and the 5.0.0 baseline's
`Cls(**result)` raised on them. `build` rejects a non-dataclass: `DeploymentTemplate` and `UserApplicationData` are
still unpacked with `**`.

A field whose keys are dynamic stays a raw dict and must not name a dataclass in its hint, or `build` drops the data.
`TriggerTasks.parameter_mapping` is keyed by the snake_cased `consumes` names of the task's method (eg. `seconds` for
`Event.CommonCorePlugin.Wait`), checked against 117 live tasks. `DCParameterMapping` declares the union of those names
across every task method in the 2.8.0.8 captures (`get_schedule_data`'s `available_methods`), 62 of them, all `str`:
AMP's `ParameterMapping` is a `Dictionary<String, String>`: booleans and numbers arrive as `"true"` / `"55"`. A
method outside that list (eg. a new plugin) has its arguments dropped and logged. Add them to both `DCParameterMapping`
and the `ParameterMapping` TypedDict.

Where a field is richer than the wire format (an enum, or a nested dataclass), the annotation is
widened to `Rich | Raw` and `__post_init__` does the conversion. `Port.protocol`, `Status.state`,
`Updates.status`, `TimedTrigger.tasks` and every `SettingsSpecParent` category follow this shape.

Container fields are spelled as a **union of containers** — `list[SettingSpec] | list[ConfigResponse]`,
not `list[SettingSpec | ConfigResponse]`. `list` and `dict` are invariant in their element type, so
the raw response is not assignable to the combined form.

An annotation that the runtime does not honour is worse than a loose one; several were found
claiming a nested dataclass that nothing ever built. Where the nested shape is still unconfirmed
the field is left raw and tagged, rather than annotated aspirationally.

AMP adds keys between versions. AMP 2.8 added `ports` to the status, three keys to each port and five to
each backup, plus `oidc_sub` (users), `local_login_enabled` (module info), `warn_text` / `warn_when_value` (every
setting), `notice` (schedule methods), `locked*` (method arguments) and four error keys on trigger tasks. New fields
go in defaulted so older responses still construct. A dropped-key WARNING from `build` is the cue to declare one.

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
the server, so not unattended). The 2.6.5.0 dumps at the root of `_responses/` are a Controller run. The
2026-10-20 refresh (#1) is in `_responses/vm_2.8.0.8_20261020/` (vm1 Controller, vm2 direct and through the
Controller, seven Instances) and `_responses/live_2.8.0.8_20261020/` (Kat's ADS and three running Minecraft
Instances, without sessions or file contents). The `[LIVE]` login needs `bridge.use_2fa = True`, its TOKEN is the
TOTP secret.

`Core/GetOIDCLogoutUrl` is spelled `Url`, unlike `Core/GetOIDCLoginURL`. The spec sheets snake_case method names, so
they can't show the casing; "No such web method" on a method the spec lists is the sign of a casing mismatch.

Shapes not yet confirmed against a live payload:

- `DeploymentTemplateResponse` / `ProvisionResponse`, derived from the dataclasses and docs; both
  endpoints returned empty on every setup dumped so far.
- `TimedTriggerResponse` / `UserApplicationDataResponse`, derived from their dataclasses; there is no
  dump for `Core/GetTimeIntervalTrigger` or `Core/GetUserInfo`.
- `OPWhitelistResponse`, built from the `OPWhitelist` dataclass; `GetOPWhitelist` answers
  "Missing Method" and is in no spec sheet.

`ampapi/key_drift.py` notices AMP changing its keys; usage is in CONTRIBUTING.md ("Checking for key
drift"). `key_drift()` / `declared_keys()` are the same functions as Minerva's and Python_Template's
copies, so keep them in step.

A failed login (wrong password or wrong 2FA code alike) answers `success: false`, `result: 40`, an
empty `result_reason` and `session_id: None` on AMP 2.8.0.8, so AMP gives no reason to pass on.

The doc generators in `util.py` import their notes from `docs/samples/`, which is not packaged, so
they only run from a repo checkout.


## Verification

```bash
.venv/bin/python -c "import ampapi; import ampapi.util"
~/.local/bin/uvx ruff check ampapi/
~/.local/bin/uvx pyright ampapi/
```

`unit_test.py` at the repo root is untracked and hits a live AMP Instance - do not run it
unattended.

Captured responses live in `_responses/`. A TypedDict built from a dataclass definition instead of
a captured payload is a guess; `getscheduledata.json` exposed two dataclasses (`Methods`, `Triggers`)
that raised `TypeError` on their own documented response because fields were missing.



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
  `TargetADS` for a Target's. `start_instance()` / `stop_instance()` / `restart_instance()` / `update_instance()` and
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
- `AnalyticsPlugin/GetUserDetails` and `ADSModule/GetProvisionFitness`: JSON null on the VMs (no player data, no
  fitness data), so their shapes are still unknown.
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

`find_parameter_mismatches(spec_path=docs/api_spec_sheets/2.8.0.8)`, 2026-10-19. Leave out `spec_path` and it merges
every version with "first file seen wins", so 2.6.2.0 shadows 2.8.0.8. It also lists `request_params` everywhere.
Renames like `file_path` and `instance_id` are on purpose (`ForceIncludeSelf` is always True). The real gaps:
- core: `create_user` (IsOIDCUser, OIDCSub), `disable_two_factor` (Password, TwoFactorCode), `get_setting_values`
  (WithRefresh), `oidc_login` (state, serverId).
- ads_module: `apply_template` (NewFriendlyName, Secret, RestartIfPreviouslyRunning), `upgrade_instance`
  (RestartIfRunning), `set_instance_suspended` (SuspendReason), `set_instance_network_info` (AdvertisedAddress,
  AdvertisedAddressIncludesPort). `create_instance_from_spec` types `target_datastore` as str, the spec says Int32.
- `get_analytics_summary` (PlayerCount), `take_backup` (BackupWhileRunning, DirtyOnly, WasCreatedAutomatically, and
  Title vs `name`), `write_file_chunk` (FinalChunk), `create_archive` (OverwriteExisting).

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

The original two-VM build, for reference:

```bash
#!/bin/bash
# Dev-VMs
for vm in vm1 vm2; do
  virt-install --name $vm --memory 4096 --vcpus 2 \
    --disk /var/lib/libvirt/vm-ware/images/$vm.qcow2,bus=virtio \
    --network network=default,model=virtio \
    --os-variant ubuntu24.04 \
    --import --cloud-init user-data=/home/kat/vm-user-data.yaml \
    --graphics none --console pty,target_type=serial \
    --noautoconsole
done
```
## Version directives

Checked 2026-10-20 (#14) with a test build of a scratch copy, Sphinx 8.2.3 and furo:
- `.. versionadded:: X`, `.. versionchanged:: X`, `.. deprecated:: X` and `.. versionremoved:: X` are built into
  Sphinx (`versionremoved` since 7.3), so `conf.py` needs nothing. Napoleon passes them through from a numpy docstring,
  in the body or nested under a parameter's description, and `:attr:` / `:meth:` references inside them resolve.
- `docs/_static/styles/furo.css` already styles `div.versionadded`, `div.versionchanged` and `div.versionremoved`.
  They render as "Added in version 5.0.0:", "Changed in version 5.0.0:" and "Removed in version 5.0.0:".
- Already in use: `Bridge` (`versionadded`) and `create_local_instance` (`deprecated`).
- `docs/extensions/prettyversion.py` (from dpy/Umbra, commented out in `conf.py`) swaps them for boxes with
  Font Awesome icons. The docs don't load Font Awesome, so the icons would be blank without it.
- The version is compared against the last release (4.6.0). Things added and changed inside the 5.0.0 work
  (`route_by_target`, `Controller.targets`) never shipped, so they are `versionadded:: 5.0.0` at most.
- 5.0.0 tags only the objects whose use changed (Kat, 2026-10-20): `Controller.instances` / `targets`,
  `TargetADS` start, stop and restart, `write_file_chunk` and `sanitize_path`. `docs/upgrading.rst` stays the full
  4.x -> 5.0.0 record. Later changes get their tag as they are made.
- An AMP version in a directive is written `AMP-2.6.0.0` (`Core.get_webserver_metrics`). Sphinx takes the first word
  as the version and the rest as the text, so `AMP 2.6.0.0` renders "Removed in version AMP: 2.6.0.0".
