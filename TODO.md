# AMP API TODO

A small todo list local to the project.
Items carry a stable number (#N) for reference; `.local_data/plans/todo_index.md` tracks their type and status.


## ampapi/adsmodule.py

---

- (#3) Confirm `ProvisionResponse` against a live payload; AMP answers `GetProvisionFitness` with null on the VMs.
- (#4) `create_local_instance` is deprecated: remove it, or fix it once AMP's `LocalAMPInstance` shape is known.

## ampapi/instance.py

---


## ampapi/base.py

---


## ampapi/core.py

---

- (#5) Confirm `UserApplicationDataResponse` against a live payload; `Core/GetUserInfo` needs a player online.

## ampapi/analytics.py

---

- (#6) Confirm the shape of `get_user_details` with a player who has played; AMP answers null otherwise.

## ampapi/filemanager.py, filebackup.py, emailsender.py, minecraft.py

---

- (#7) Find what `append_file_chunk` does; on 2.8.0.8 it answers null and changes no file.

## ampapi/modules.py

---


## ampapi/util.py

---


## Docs

---


## Issues

---
- N/A

## Improvements/Suggestions

---

- (#9) Implement non-dataclass types to lower overhead and speed via Format_data arg
- (#17) Offer orjson as an optional extra (`ampapi[speed]`) for `_response_handler`'s JSON decode.
- (#11) Update function returns and parameters since adding `bool` to `_post`.
- (#12) Store plugin (17 endpoints) and Webhook plugin (`trigger_webhook_event`) have no wrapper module.
- (#13) Add the spec parameters our wrappers lack (list in NOTES.md, "Wrapper parameter gaps").
