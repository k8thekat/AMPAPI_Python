# API Spec Sheets

---

These are the API endpoints AMP reports for each version, saved as plain text so we can see what changed between releases.

### Version directories

- `2.6.2.0`, `2.6.5.0` and `2.8.0.8` are AMP application versions.
- Each one holds `ADS_api_spec.md` and `Minecraft_api_spec.md`, one for the Controller/ADS and one for a Minecraft Instance.
- A new directory is made for you when `amp_api_update` runs against an AMP version we have not seen yet.

### Making new sheets

- `amp_api_update(instance=controller, sanitize_json=True)` in `ampapi/util.py` is the one to run when AMP gets a version bump.
  - It finds a running Minecraft Instance on the same version as the Controller, then calls `_parse_get_api_spec_to_file` for both to write the sheets.
  - You must pass in your `Controller`.

### Diffs

- `diffs/` is gitignored, it is made locally and never committed.
- `compare_api_spec_versions(version_a, version_b, instance_type)` in `ampapi/util.py` writes `diffs/{instance_type}_{version_a}_to_{version_b}.md`.
  - `instance_type` is `"ADS"` or `"Minecraft"`.

### Checking our code against the sheets

- `find_missing_endpoints()` writes `missing_endpoints.md`, the spec endpoints we have no method for.
- `find_parameter_mismatches()` writes `parameter_mismatches.md`, the methods whose parameters do not match the spec.

Happy spec hunting~
