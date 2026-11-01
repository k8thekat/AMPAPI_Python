# AMP API TODO

A small todo list local to the project.
Items carry a stable number (#N) for reference; `.local_data/plans/todo_index.md` tracks their type and status.


## ampapi/adsmodule.py

---

- (#3) Confirm `ProvisionResponse` against a live payload; AMP answers `GetProvisionFitness` with null on the VMs.
- (#43) `update_datastore` and `add_datastore` send `InstanceDatastore.to_dict()`'s snake_case keys, which AMP reads as a datastore with no name.

## ampapi/instance.py

---

## ampapi/base.py

---

## ampapi/core.py

---

## ampapi/analytics.py

---

## ampapi/filemanager.py, filebackup.py, emailsender.py, minecraft.py

---

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

- (#17) Offer orjson as an optional extra (`ampapi[speed]`) for `_response_handler`'s JSON decode.
- (#12) Store plugin (17 endpoints) and Webhook plugin (`trigger_webhook_event`) have no wrapper module.
