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

Response dataclasses are built by unpacking the raw dict straight in - `SettingSpec(**result)`.
No generic converter, no `cast`. `sanitize_json` has already snake_cased the keys by then.

Where a field is richer than the wire format (an enum, or a nested dataclass), the annotation is
widened to `Rich | Raw` and `__post_init__` does the conversion. `Port.protocol`, `Status.state`,
`Updates.status`, `TimedTrigger.tasks` and every `SettingsSpecParent` category follow this shape.

Container fields are spelled as a **union of containers** — `list[SettingSpec] | list[ConfigResponse]`,
not `list[SettingSpec | ConfigResponse]`. `list` and `dict` are invariant in their element type, so
the raw response is not assignable to the combined form.

An annotation that the runtime does not honour is worse than a loose one; several were found
claiming a nested dataclass that nothing ever built. Where the nested shape is still unconfirmed
the field is left raw and tagged, rather than annotated aspirationally.

AMP adds keys between versions, and `SomeDataclass(**result)` raises `TypeError` on any key the
dataclass does not declare. AMP 2.8 added `ports` to the status, three keys to each port and five to
each backup. New fields go in defaulted so older responses still construct.

`Base.sanitize_json` is not safe to run twice on keys: a second pass strips the underscores
(`active_users` -> `activeusers`). The library sanitizes each response once, in `_response_handler`, and
`controller_dump.py` sanitizes its own raw fetches once; `Core.get_triggers` only runs it on strings, which
come out the same. Don't sanitize a capture or a `format_data=False` result again.

Some shapes differ by Instance type. The ADS reports `physical_ram_usage` and `swap_usage` metrics,
Minecraft Instances do not, and some modded ones add `tps`; `Metrics` only requires the three every
Instance sends. A stopped Instance reports its `metrics` as `{}`.


## Captured responses

`controller_dump.py -section LIVE -out ./_responses` captures responses from a live setup (it hits
the server, so not unattended). The 2.6.5.0 ADS dumps in `_responses/` were overwritten by a
Controller run, so a non-Controller pass is still owed.

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
`vms.py pair` does this by setting each config node.

The Target's Instances need the same: an Instance created on the Target authenticates with the Target's ADS
(`Login.AuthServerURL=http://localhost:8080/`), and that hop fails even with passthru on. AMP's own fix is
`ampinstmgr --RepairAuth <mode> <controller url>` (alias `-magic`, run as `amp` with ADS stopped): it points the ADS
and every Instance at the Controller, and sets `Defaults.DefaultAuthServerURL` so new Instances start that way. It
asks the same two questions as the role choice in the web setup (`standalone` / `controller` / `target` / `hybrid`, and the
Controller's URL). Run on vm2 as `target`, it fixed `MCTest01`; not yet run on a Controller.

Creating an Instance needs a licence key in `ADSModule.Defaults.NewInstanceKey` on the ADS that runs it, the Target
when creating from the Controller; `vms.py activate` sets it. AMP accepts the `CreateInstance` call and queues it as a
task, and only the Controller's log says it failed for want of a key. `CreateInstance` also needs a GUID in
`NewInstanceId` (all zeros lets AMP pick) and a non-empty `AdminUsername`, even with `AutoConfigure`.

## Controller and Target data

Checked on the VM pair, AMP 2.8.0.8, one Controller with only its ADS and one Target with only its ADS:
- `GetInstances` sends one Target per ADS. The local Target's `friendly_name` is "Local Instances", and each Target
  lists its own ADS Instance, the one whose `instance_id` matches the Target's.
- `ForceIncludeSelf` False on a Controller drops the whole local Target, not just its ADS Instance, so
  `Controller.get_instances(include_self=False)` leaves `self`'s cached data unset. On a Target or a standalone ADS it
  changes nothing. Unchecked: whether it also drops local game Instances on a hybrid ADS.
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
  request, vm2 nothing). `Instance.start_instance()` / `stop_instance()` / `restart_instance()` go through the
  Controller by name, so on a `TargetADS` they act on the Controller's ADS, and any Instance whose name repeats on
  another ADS can hit the wrong one.

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