# AMP API TODO

A small todo list local to the project.


- Refresh `_responses/` from a non-Controller (ADS) setup; see NOTES.md "Captured responses".
- `.scripts/vms.py`: set the ADS role at install time like the web setup does (`ampinstmgr --RepairAuth`), not after pairing.


## ampapi/adsmodule.py

---

- Build a dataclass/TypedDict for `get_group` and `servers`.
- Confirm `ProvisionResponse` against a live payload; AMP answered `GetProvisionFitness` with null on the VMs.
- `create_local_instance` sends `CreateInstance.to_dict()` as `Instance`, but AMP wants a `LocalAMPInstance`, and
  answers with a null reference (vm1, 2.8.0.8).

## ampapi/instance.py

---

- Plan what else `TargetADS` should mirror from `Controller` (eg. its Target data on `self`, the cache guard).
- Check `ForceIncludeSelf` False on a hybrid ADS with local game Instances.

## ampapi/base.py

---


## ampapi/core.py

---

- Confirm `UserApplicationDataResponse` against a live payload; `Core/GetUserInfo` needs a player online.
- Confirm the shape of `get_structured_diagnostics` (typed `dict[str, Any]` for now).

## ampapi/analytics.py

---

- Confirm the shape of `get_user_details` (typed `dict[str, Any]` for now).

## ampapi/filemanager.py, filebackup.py, emailsender.py, minecraft.py

---

- Confirm what `append_file_chunk`'s `delete` parameter does; the 2.8.0.8 spec gives no description.
- Confirm the `FolderUploadFile` keys `upload_folder` sends.

## ampapi/modules.py

---

- Nested shapes are still raw dicts (`Methods.consumes`, `Triggers.tasks`, `TriggerTasks.parameter_mapping`,
  `RemoteTargetInfo`); prototype the in-house `build(cls, data)` on one or two dataclasses for Kat's review.

## ampapi/util.py

---

- Move `find_parameter_mismatches` to the URL matching `find_missing_endpoints` uses, and fix its
  `ampapi/x.py` links, which break from `docs/api_spec_sheets/`.

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
