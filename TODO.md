# AMP API TODO

A small todo list local to the project.


- Refresh `_responses/` from a non-Controller (ADS) setup; see NOTES.md "Captured responses".
- `.scripts/vms.py`: set the ADS role at install time like the web setup does (`ampinstmgr --RepairAuth`), not after pairing.


## ampapi/adsmodule.py

---

- Confirm `ProvisionResponse` against a live payload; AMP answers `GetProvisionFitness` with null on the VMs.
- `create_local_instance` sends `CreateInstance.to_dict()` as `Instance`, but AMP wants a `LocalAMPInstance`, and
  answers with a null reference (vm1, 2.8.0.8).

## ampapi/instance.py

---

- Plan what else `TargetADS` should mirror from `Controller` (eg. its Target data on `self`, the cache guard).

## ampapi/base.py

---

- `sanitize_path` refuses any `_` in a path, so the file wrappers can't reach eg. `AMP_Logs/`. AMP takes them fine.

## ampapi/core.py

---

- Confirm `UserApplicationDataResponse` against a live payload; `Core/GetUserInfo` needs a player online.

## ampapi/analytics.py

---

- Confirm the shape of `get_user_details` with a player who has played; AMP answers null otherwise.

## ampapi/filemanager.py, filebackup.py, emailsender.py, minecraft.py

---

- Find what `append_file_chunk` does; on 2.8.0.8 it answers null and changes no file.

## ampapi/modules.py

---

- Nested shapes are still raw dicts (`Methods.consumes`, `Triggers.tasks`, `TriggerTasks.parameter_mapping`,
  `RemoteTargetInfo`); Kat to review the `build(cls, data)` prototype on branch `prototype/nested-build`.

## ampapi/util.py

---


## Docs

---


## Issues

---
- N/A

## Improvements/Suggestions

---

- Implement non-dataclass types to lower overhead and speed via Format_data arg
- Add API endpoints to the remaining function docstrings.
  - About 11 of 207 endpoint methods name their endpoint.
- Update function returns and parameters since adding `bool` to `_post`.
- Store plugin (17 endpoints) and Webhook plugin (`trigger_webhook_event`) have no wrapper module.
- Add the spec parameters our wrappers lack (list in NOTES.md, "Wrapper parameter gaps").
