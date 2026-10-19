# AMP API TODO

A small todo list local to the project.


- Wrap the endpoints added by AMP API `2.8.0.8` (see `docs/api_spec_sheets/2.8.0.8/`).
- Refresh `_responses/` from a non-Controller (ADS) setup; see NOTES.md "Captured responses".
- `.scripts/vms.py`: set the ADS role at install time like the web setup does (`ampinstmgr --RepairAuth`), not after pairing.


## ampapi/adsmodule.py

---

- `create_instance` raises `AMPAPIKeyError` on success: AMP 2.8 answers with a RunningTask (ActionResult keys merged in).
- `CreateInstance` defaults AMP rejects: `new_instance_id` "" (needs a Guid) and `admin_username` "" (null fails too).
- Build a dataclass/TypedDict for `get_group` and `servers`.
- `add_datastore` sends `new_datastore.__dict__`; switch it to `to_dict()` like `update_datastore`.
- Convert `RemoteTargetInfo.platform_info` / `.datastores` in a `__post_init__`.
- Confirm `DeploymentTemplateResponse` / `ProvisionResponse` against a live payload.
- Missing wrappers from `2.8.0.8`: `clone_instance`, `get_instance_live_settings`, `prepare_file_transfer`.

## ampapi/instance.py

---

- Plan what else `TargetADS` should mirror from `Controller` (eg. its entry's data on `self`, the cache guard).
- `Instance.start_instance` / `stop_instance` / `restart_instance` pick the Instance by name on the Controller; route
  them to the ADS in the row's `target_id` so a name repeated on another ADS can't hit the wrong one.
- Check `ForceIncludeSelf` False on a hybrid ADS with local game Instances.

## ampapi/base.py

---

- `_reauth`'s login error gives AMP's result number only; name the known ones (eg. 5 is `NoInstanceAccess`).
- `sanitize_json` turns dotted keys into `ads_module._defaults._default_auth_server_url` (seen in `deployment_args`).
- `version_validation` needs updating for the new data structure handling (`base.py:1155`).
- Possibly get active AMP Sessions and close them during `clean_up()`?

## ampapi/core.py

---

- Narrowing sites raise with `end_point="Core/ActionResult"` instead of the endpoint's own url.
- `get_permissions_spec` takes no `format_data`; passing it falls through to `_response_handler` as a bare `TypeError`.
- `get_tasks` returns `list[RunningTask] | list[Any]`; name `RunningTaskResponse` so `KeyDriftCheck` can check it.
- `get_api_spec` is annotated `APISpec | dict[str, Any]` but always returns a plain `dict(result)`.
- Confirm `TimedTriggerResponse` / `UserApplicationDataResponse` against a live payload
  (`Core/GetTimeIntervalTrigger`, `Core/GetUserInfo`).
- Missing wrappers from `2.8.0.8`: `add_interval_trigger`, `convert_user_to_oidc`, `get_structured_diagnostics`,
  `revert_user_from_oidc`, `sleep`, `update_oidc_sub`, `update_tools`.

## ampapi/analytics.py

---

- Missing wrapper from `2.8.0.8`: `get_user_details`.

## ampapi/filemanager.py, filebackup.py, emailsender.py, minecraft.py

---

- Drop `OPWhitelistResponse` along with `mc_get_op_whitelist`; AMP no longer has `GetOPWhitelist`.
- Add a `BackupResponse` TypedDict and narrow `get_backups` to it.
- What does the `delete` parameter do on `filemanager.py:35`?
- Missing wrappers from `2.8.0.8`: `download_folder_as_zip`, `dummy` (a no-op placeholder in the spec), `upload_folder` (file manager), `backup_will_stop_server` (backup).
- `mc_reject_eula` returns None, but AMP's spec says it returns a Boolean like `mc_accept_eula`.
- The 16 deprecated Minecraft endpoints are absent from the `2.8.0.8` sheet too; decide when to remove them.

## ampapi/modules.py

---

- Nested shapes still assigned as raw dicts with no `__post_init__` conversion; see the in-file
  `# TODO:` tags on `Methods.consumes`, `Triggers.tasks` and `TriggerTasks.parameter_mapping`.

## ampapi/util.py

---

- Move `find_parameter_mismatches` to the url matching `find_missing_endpoints` uses, and fix its
  `ampapi/x.py` links, which break from `docs/api_spec_sheets/`.

## Docs

---

- Add pages for `ResponseHandlerOptions`, `ExponentialBackoff`, `errors` and `TargetADS`.
- `Base.session_ttl` / `instance_id`, `Core.triggers`, `Instance.app_state` and `Player.uuid` / `name` are documented
  twice, in the class Attributes section and on the member. The rst `:exclude-members:` hides the member's own docstring.
- `AMPInstanceState` is still named in docstrings (`instance.py` ~95, 562, 638, 742); the enum is `InstanceState`.
- `Bridge` docstring says `singleton` defaults to False; the code defaults to True.
- `Base.instance_id` docstring says the default is "O" (a letter) and that login sets it; it is "0" and a Controller keeps it.

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
