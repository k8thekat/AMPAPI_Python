# AMP API TODO

A small todo list local to the project.


- Refresh `_responses/` from a non-Controller (ADS) setup; see NOTES.md "Captured responses".
- `.scripts/vms.py`: set the ADS role at install time like the web setup does (`ampinstmgr --RepairAuth`), not after pairing.


## ampapi/adsmodule.py

---

- Confirm `ProvisionResponse` against a live payload; AMP answers `GetProvisionFitness` with null on the VMs.
- `create_local_instance` is deprecated: remove it, or fix it once AMP's `LocalAMPInstance` shape is known.

## ampapi/instance.py

---


## ampapi/base.py

---


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
