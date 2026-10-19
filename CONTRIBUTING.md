# Contributing to AMP API Python

Thanks for helping out~ This covers setting up, the checks to run, how commits are written, and the dev
tools the library ships for keeping up with AMP.

## Table of Contents

- [Setup](#setup)
- [Before you open a pull request](#before-you-open-a-pull-request)
- [Code style](#code-style)
- [Commit messages](#commit-messages)
- [Talking to a live AMP server](#talking-to-a-live-amp-server)
- [Dev tools](#dev-tools)
  - [Calling an endpoint that has no wrapper yet](#calling-an-endpoint-that-has-no-wrapper-yet)
  - [Capturing responses](#capturing-responses)
  - [Checking for key drift](#checking-for-key-drift)
  - [When AMP updates](#when-amp-updates)

## Setup

_Python 3.12 or higher is required._

```bash
python -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install ruff pyright -r docs/requirements.txt
```

## Before you open a pull request

```bash
.venv/bin/python -c "import ampapi; import ampapi.util"
.venv/bin/ruff check ampapi/
.venv/bin/ruff format --check ampapi/
.venv/bin/pyright ampapi/            # strict mode, configured in pyproject.toml
.venv/bin/sphinx-build -E -b html docs docs/build
```

- `CHANGELOG.md` is generated from commit messages by a GitHub workflow; don't edit it by hand.
- If your change alters what a user imports, calls or gets back, add a line to `docs/upgrading.rst`.

## Code style

- Docstrings are NumPy style, following `ampapi/docstring/template/numpy-overwrite.mustache`.
  Parameters are written `name : :class:`Type`` with a space either side of the colon.
- Nullable types are `Union[X, None]`, in the signature and the docstring.
- Responses are narrowed to a TypedDict with `is_response_type()` / `is_response_list()`, never `typing.cast`.
  See `NOTES.md` for how the response TypedDicts and dataclasses fit together.

## Commit messages

Each commit opens with a `#` theme line, then a `# file_name.py` header per file touched. The changelog
workflow turns every `#` line into a heading.

```
# A theme: what this commit was for
- Overall change not tied to one file.

# file_name.py
- Change 1
- Change 2
-- Change 2 sub-change 1

$ Only this line is omitted from the changelog, because it starts with `$`
$ A line after it is kept unless it also starts with `$`, so prefix every line to hide
```

## Talking to a live AMP server

Credentials live in `local.ini` at the repo root, which is gitignored. Each section is one AMP setup:

```ini
[LIVE]
URL = http://192.168.1.10:8080
USER = your_amp_user
PASSWORD = your_amp_password
; TOKEN is only needed when the AMP user has 2FA turned on.
TOKEN = your_2fa_secret
```

`unit_test.py` and `controller_dump.py` call a real AMP server, so point them at a setup where that is fine,
and never run them unattended. Captured responses go in `_responses/`, which is also gitignored, because
they carry session IDs and user names.

## Dev tools

### Calling an endpoint that has no wrapper yet

`_call_end_point()` posts to any endpoint, with the session handled for you. Find endpoints and their
parameters in `docs/api_spec_sheets/<AMP version>/ADS_api_spec.md` or `Minecraft_api_spec.md`.

```python
result = await controller._call_end_point(endpoint="Core/GetModuleInfo")
result = await controller._call_end_point(endpoint="Core/GetConfig", parameters={"node": "Core.Login.UseAuthServer"})
```

### Capturing responses

Every wrapper method takes `to_file` and `path`, and writes the sanitized response to
`<path>/<endpoint name>.json` (eg. `getstatus.json`):

```python
from pathlib import Path

captures = Path("_responses")
await instance.get_status(format_data=False, to_file=True, path=captures)
```

To capture a whole Controller/Target setup in one go, use `controller_dump.py`:

```bash
python controller_dump.py -section LIVE -out ./_responses
```

### Checking for key drift

AMP adds and removes response keys between versions. A dataclass built with `Dataclass(**result)` raises a
`TypeError` on a key it doesn't know, so it's worth checking captures whenever AMP updates.
`ampapi/key_drift.py` compares each response with the TypedDict its endpoint narrows to. It reads which
TypedDict that is straight from the wrapper source, so a new wrapper needs no registering.

Check a response as it is captured by adding `check_key_drift=True`. It only runs together with `to_file`:

```python
await instance.get_status(format_data=False, to_file=True, path=captures, check_key_drift=True)
```

When the keys differ it logs a warning and writes `getstatus.key_drift.json` next to the capture:

```json
{
    "endpoint": "Core/GetStatus",
    "shape": "StatusResponse",
    "missing": {"metrics.cpu_usage": 1},
    "unexpected": {"ports.added_by_amp": 1}
}
```

- `missing`: required keys AMP didn't send, with how many payloads lacked each one.
- `unexpected`: keys the TypedDict doesn't declare.
- Nested keys are dotted (`ports.added_by_amp`).

To check everything already captured, use `KeyDriftCheck`:

```python
from pathlib import Path

from ampapi.key_drift import KeyDriftCheck

checker = KeyDriftCheck()
checker.shapes["Core/GetStatus"]                 # (StatusResponse,)
checker.check("Core/GetStatus", data)            # (StatusResponse, KeyDrift), or None if no shape is known
drifted = checker.check_directory(Path("_responses"))   # writes _responses/key_drift.md
```

The report lists every drifted capture, the empty ones (`[]` or `null`), and any with no known shape. A
capture is matched to its endpoint by file name, so a renamed file lands under "No known shape", as does an
endpoint whose wrapper names no TypedDict.

When a capture drifts, update the endpoint's TypedDict in `ampapi/_types.py` and its dataclass in
`ampapi/modules.py`. Give new dataclass fields a default, so responses from older AMP versions still build.

### When AMP updates

Run these from a repo checkout, with a `Controller` logged in to the new AMP version:

```python
from ampapi import util

# 1. Write the new spec sheets to docs/api_spec_sheets/<version>/. A running Minecraft Instance adds its endpoints.
await util.amp_api_update(instance=controller, sanitize_json=True)

# 2. See what changed between two versions (writes docs/api_spec_sheets/diffs/).
util.compare_api_spec_versions(version_a="2.6.5.0", version_b="2.8.0.8", instance_type="ADS")

# 3. List the endpoints the spec has that no wrapper posts to (writes docs/api_spec_sheets/missing_endpoints.md).
util.find_missing_endpoints()

# 4. Regenerate the setting, permission, trigger and method .rst pages.
await util.generate_docs_rst(instance=controller)
```

Then capture fresh responses and run `KeyDriftCheck().check_directory(...)` over them. Upload the new spec
sheets along with any wrapper changes~
