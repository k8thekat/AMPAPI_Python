# AMP API TODO

A small todo list local to the project.


- Wrap the endpoints added by AMP API `2.8.0.8` (see `docs/api_spec_sheets/2.8.0.8/`).
- `_responses/` needs a fresh non-Controller (ADS) pass; the 2.6.5.0 dumps were overwritten by the
  Controller run. Use `controller_dump.py -section LIVE -out ./_responses`.
- Regenerate `docs/api_spec_sheets/missing_endpoints.md` against `2.8.0.8`.
  - `find_missing_endpoints()` matches by method name, so renamed wrappers (`activate_amp_license`,
    `get_setting_spec`, `resume_instance`, `suspend_instance`, ...) show as missing. Match on the `url=` literal instead.


## Release blockers

---

- `import ampapi` fails once installed: `util.py:17` imports `docs.samples.method_event_usage` at module level
  and `docs/` is not packaged. Same for the lazy imports at `util.py:711`, `842` and `907`.
- `Directory` / `DirectoryResponse` are missing `is_smart_excluded_from_backups`; newer AMP sends it and
  `Directory(**result)` raises `TypeError`. Fixed on `main` by PR #27 (`8d74bd9`), not carried into `Refactor`.


## ampapi/adsmodule.py

---

- Build a dataclass/TypedDict for `get_group` and `servers` once their response shapes are confirmed.
- Verify the conversion of the `new_datastore` parameter into a dict (`adsmodule.py:116`).
- `RemoteTargetInfo.platform_info` / `.datastores` are assigned raw dicts; no `__post_init__` converts them.
- `DeploymentTemplateResponse` / `ProvisionResponse` are derived from the dataclasses + docs, not a live
  payload; both endpoints return empty on every setup dumped so far. See their `# TODO:` tags in `_types.py`.
- Missing wrappers from `2.8.0.8`: `clone_instance`, `get_instance_live_settings`, `prepare_file_transfer`.

## ampapi/base.py

---

- Remove `call_end_point`; its only caller is `_reauth` for `Core/Login`, and it just forwards to `_post`.
- Fix the blind exception catch in `_reauth` (`base.py:639`).
- `version_validation` needs updating for the new data structure handling (`base.py:1155`).
- `_no_controller` message still names `AMPControllerInstance`.
- Possibly get active AMP Sessions and close them during `clean_up()`?

## ampapi/core.py

---

- `get_oidc_login_url` accepts `state` / `redirect_uri` and forwards neither. The `2.8.0.8` spec has one
  optional parameter, `redirect_uri`; drop `state` and forward it.
- `TimedTriggerResponse` / `UserApplicationDataResponse` are derived from the `TimedTrigger` /
  `UserApplicationData` definitions, not a live payload; there is no `_responses/` dump for
  `Core/GetTimeIntervalTrigger` or `Core/GetUserInfo`. Their key sets are unverified.
- Missing wrappers from `2.8.0.8`: `add_interval_trigger`, `convert_user_to_oidc`, `get_structured_diagnostics`,
  `revert_user_from_oidc`, `sleep`, `update_oidc_sub`, `update_tools`.

## ampapi/analytics.py

---

- Replace the `cast("dict[str, Any]", result)` at `analytics.py:106` with an `is_response_type()` narrow.
- Missing wrapper from `2.8.0.8`: `get_user_details`.

## ampapi/filemanager.py, filebackup.py, emailsender.py, minecraft.py

---

- `ActionResult(**result)` is built from an un-narrowed `_post` return; `"status" in result` does not narrow
  the union. Switch to `is_response_type()` like `adsmodule.py` / `core.py` do.
  - 21 sites, 87 pyright errors: filemanager 15, filebackup 3, minecraft 2, emailsender 1.
- `BackupResponse` TypedDict is still missing; `getbackups.json` returned empty `[]` from the tested
  server. Needs a server with actual backups to dump the item structure.
- What does the `delete` parameter do on `filemanager.py:35`?
- Missing wrappers from `2.8.0.8`: `download_folder_as_zip`, `upload_folder` (file manager), `backup_will_stop_server` (backup).
- The 8 surviving Minecraft methods still need TypedDict work once response dumps are available.
- The 16 deprecated Minecraft endpoints are absent from the `2.8.0.8` sheet too; decide when to remove them.

## ampapi/modules.py

---

- Nested shapes still assigned as raw dicts with no `__post_init__` conversion; see the in-file
  `# TODO:` tags on `Methods.consumes`, `Triggers.tasks`, `TriggerTasks.parameter_mapping` and `Updates.console_entries`.
- `Metric` is only referenced in docstrings now; `Status.metrics` converts to `MetricsData` per key.

## ampapi/util.py

---

- 78 pyright errors, mostly unknown types from `dict_merge` and the schedule data parsing.
- `generate_docs_rst` is annotated with the removed `AMPControllerInstance` (`util.py:1013`) and `Base` is undefined at `util.py:672`.
- Stray `print("file_a path", file_a)` at `util.py:382`.

## Docs

---

- Add pages for `ResponseHandlerOptions`, `ExponentialBackoff`, `errors` and `TargetADS`.
- `Base.session_ttl` / `instance_id`, `Core.triggers`, `Instance.app_state` and `Player.uuid` / `name` are documented
  twice, in the class Attributes section and on the member. The rst `:exclude-members:` hides the member's own docstring.
- Replace the remaining `AMP*Instance` names in docstrings (`instance.py`, `adsmodule.py`, `base.py`, `util.py`).
- `bridge.py` docstring: `ap_params` typo, "Version 5.0" note, `Parameter` heading.

## Issues

---
- N/A

## Improvements/Suggestions

---

- Impliment non-dataclass types to lower overhead and speed via Format_data arg
- Add API endpoints to the remaining function docstrings.
  - About 11 of 207 endpoint methods name their endpoint.
- Update function returns and parameters since adding `bool` to `_post`.
- Store plugin (17 endpoints) and Webhook plugin (`trigger_webhook_event`) have no wrapper module.
