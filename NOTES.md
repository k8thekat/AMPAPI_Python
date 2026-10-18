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

Some shapes differ by instance type. The ADS reports `physical_ram_usage` and `swap_usage` metrics,
Minecraft instances do not, and some modded ones add `tps`; `Metrics` only requires the three every
instance sends. A stopped instance reports its `metrics` as `{}`.


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

`unit_test.py` at the repo root is untracked and hits a live AMP instance - do not run it
unattended.

Captured responses live in `_responses/`. A TypedDict built from a dataclass definition instead of
a captured payload is a guess; `getscheduledata.json` exposed two dataclasses (`Methods`, `Triggers`)
that raised `TypeError` on their own documented response because fields were missing.



## Building VMs

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