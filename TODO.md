# AMP API TODO

A small todo list local to the project.


- Wrap the endpoints added by AMP API `2.8.0.8` (see `docs/api_spec_sheets/2.8.0.8/`).
- `_responses/` needs a fresh non-Controller (ADS) pass; the 2.6.5.0 dumps were overwritten by the
  Controller run. Use `controller_dump.py -section LIVE -out ./_responses`.


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

- Fix the blind exception catch in `_reauth` (`base.py:639`).
- `version_validation` needs updating for the new data structure handling (`base.py:1155`).
- Possibly get active AMP Sessions and close them during `clean_up()`?

## ampapi/core.py

---

- Narrowing sites raise with `end_point="Core/ActionResult"` instead of the endpoint's own url.
- `get_api_spec` is annotated `APISpec | dict[str, Any]` but always returns a plain `dict(result)`.
- `TimedTriggerResponse` / `UserApplicationDataResponse` are derived from the `TimedTrigger` /
  `UserApplicationData` definitions, not a live payload; there is no `_responses/` dump for
  `Core/GetTimeIntervalTrigger` or `Core/GetUserInfo`. Their key sets are unverified.
- Missing wrappers from `2.8.0.8`: `add_interval_trigger`, `convert_user_to_oidc`, `get_structured_diagnostics`,
  `revert_user_from_oidc`, `sleep`, `update_oidc_sub`, `update_tools`.

## ampapi/analytics.py

---

- Missing wrapper from `2.8.0.8`: `get_user_details`.

## ampapi/filemanager.py, filebackup.py, emailsender.py, minecraft.py

---

- `OPWhitelistResponse` is built from the `OPWhitelist` dataclass, not a live payload; `getopwhitelist.json`
  is a "Missing Method" error and the endpoint is in no spec sheet.
- `BackupResponse` TypedDict is still missing; `getbackups.json` returned empty `[]` from the tested
  server. Needs a server with actual backups to dump the item structure.
- What does the `delete` parameter do on `filemanager.py:35`?
- Missing wrappers from `2.8.0.8`: `download_folder_as_zip`, `dummy` (a no-op placeholder in the spec), `upload_folder` (file manager), `backup_will_stop_server` (backup).
- The 8 surviving Minecraft methods still need TypedDict work once response dumps are available.
- The 16 deprecated Minecraft endpoints are absent from the `2.8.0.8` sheet too; decide when to remove them.

## ampapi/modules.py

---

- Nested shapes still assigned as raw dicts with no `__post_init__` conversion; see the in-file
  `# TODO:` tags on `Methods.consumes`, `Triggers.tasks` and `TriggerTasks.parameter_mapping`.
- `InstanceResponse.metrics` keys are unconfirmed; `getinstances.json` sent an empty dict, so `Instance.metrics` stays a raw dict.

## ampapi/util.py

---

- The doc generators import their notes from `docs/samples/`, which is not packaged, so they only run from a repo checkout.
- `ScheduleData` is no longer a dataclass, but `Methods.consumes` still has an open `# TODO:` to convert into `DCConsumes`.
- `find_parameter_mismatches` still matches endpoints by method name (`suffix_aliases`) and writes `ampapi/x.py` links that
  break from `docs/api_spec_sheets/`; move it to the url matching `find_missing_endpoints` uses.

## Docs

---

- Add pages for `ResponseHandlerOptions`, `ExponentialBackoff`, `errors` and `TargetADS`.
- `Base.session_ttl` / `instance_id`, `Core.triggers`, `Instance.app_state` and `Player.uuid` / `name` are documented
  twice, in the class Attributes section and on the member. The rst `:exclude-members:` hides the member's own docstring.
- `AMPInstanceState` is still named in docstrings (`instance.py` ~95, 562, 638, 742); the enum is `InstanceState`.
- `Bridge` docstring says `singleton` defaults to False; the code defaults to True.

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
