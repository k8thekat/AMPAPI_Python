"""Capture AMP API responses from a Controller/Target setup.

Stdlib only (plus ``pyotp`` if a 2FA token is set) for the request path, so it runs on any box
that can reach the Controller and a bug in the library's request handling can't mask what the
API actually returned.

.. note::
    Responses are written **sanitized** by default - keys are run through
    :meth:`Base.sanitize_json` so the files match what the library hands back and what the
    ``*Response`` TypedDicts describe. AMP sends ``PascalCase`` on the wire; the library
    converts to ``snake_case``, so an unsanitized dump does NOT match the TypedDicts.
    Sanitizing needs ``ampapi`` importable; without it the dump falls back to raw and says so.
    Pass ``-raw`` to keep AMP's original keys deliberately.


Reads credentials from ``local.ini`` next to this file. Usage::

    python controller_dump.py                      # dumps the CONTROLLER section
    python controller_dump.py -section TARGET      # dumps the TARGET section
    python controller_dump.py -out ./_responses    # choose the output directory
    python controller_dump.py -raw                 # keep AMP's PascalCase keys

Every response is written to ``{out}/{endpoint}.json`` using the same lowercase naming the
library uses, so the files drop straight into ``_responses/``.
"""

from __future__ import annotations

import argparse
import json
import ssl
import urllib.error
import urllib.request
from configparser import ConfigParser
from pathlib import Path
from typing import Any

# * (label, endpoint, parameters). Parameters marked "<...>" are filled in at runtime from an
# * earlier response; see _resolve() below.
ENDPOINTS: list[tuple[str, str, dict[str, Any]]] = [
    # -- no parameters --------------------------------------------------------
    ("target info", "ADSModule/GetTargetInfo", {}),
    ("instances (targets)", "ADSModule/GetInstances", {"ForceIncludeSelf": True}),
    ("local instances", "ADSModule/GetLocalInstances", {}),
    ("instance statuses", "ADSModule/GetInstanceStatuses", {}),
    ("datastores", "ADSModule/GetDatastores", {}),
    ("deployment templates", "ADSModule/GetDeploymentTemplates", {}),
    ("provision fitness", "ADSModule/GetProvisionFitness", {}),
    ("supported applications", "ADSModule/GetSupportedApplications", {}),
    ("supported app summaries", "ADSModule/GetSupportedAppSummaries", {}),
    ("provision spec", "Core/GetProvisionSpec", {}),
    # -- parameterised, resolved from earlier responses -----------------------
    ("datastore", "ADSModule/GetDatastore", {"id": "<datastore_id>"}),
    ("datastore instances", "ADSModule/GetDatastoreInstances", {"datastoreId": "<datastore_id>"}),
    ("instance", "ADSModule/GetInstance", {"InstanceId": "<instance_id>"}),
    ("application endpoints", "ADSModule/GetApplicationEndpoints", {"instanceId": "<instance_id>"}),
    ("instance network info", "ADSModule/GetInstanceNetworkInfo", {"InstanceName": "<instance_name>"}),
    ("provision arguments", "ADSModule/GetProvisionArguments", {"ModuleName": "<module_name>"}),
]


def _get_sanitizer(*, raw: bool) -> Any:
    """Return the library's sanitize_json, or None when raw output was asked for or ampapi is missing."""
    if raw:
        return None
    try:
        from ampapi.base import Base  # noqa: PLC0415
    except ImportError:
        print("  ! ampapi not importable; writing RAW PascalCase keys. These will NOT match the")
        print("  ! *Response TypedDicts. Re-run from a checkout, or sanitize before deriving types.")
        return None
    return Base.sanitize_json


class Dumper:
    """Logs into an AMP instance and writes endpoint responses to disk."""

    def __init__(self, base_url: str, out_dir: Path, sanitizer: Any = None) -> None:
        self.base = base_url.rstrip("/")
        self.out = out_dir
        self.sanitizer = sanitizer
        self.session: str | None = None
        self.resolved: dict[str, Any] = {}
        # * AMP's self-signed certs are common on a LAN; don't fail the dump over them.
        self.ssl_ctx = ssl.create_default_context()
        self.ssl_ctx.check_hostname = False
        self.ssl_ctx.verify_mode = ssl.CERT_NONE

    def post(self, endpoint: str, parameters: dict[str, Any]) -> tuple[int, bytes]:
        """Send one API request and return the status code with the raw body."""
        body = dict(parameters)
        if self.session:
            body["SESSIONID"] = self.session
        request = urllib.request.Request(  # noqa: S310
            url=f"{self.base}/API/{endpoint}",
            data=json.dumps(body).encode(),
            headers={"Accept": "text/javascript", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30, context=self.ssl_ctx) as response:  # noqa: S310
            return response.status, response.read()

    def login(self, username: str, password: str, token: str) -> bool:
        """Authenticate, generating a TOTP code when a 2FA token is configured."""
        code = ""
        if token:
            try:
                from pyotp import TOTP  # noqa: PLC0415

                code = TOTP(token).now()
            except ImportError:
                print("  ! pyotp not installed and a TOKEN is set; run: pip install pyotp")
                return False
        _, raw = self.post("Core/Login", {"username": username, "password": password, "token": code, "rememberMe": False})
        data = json.loads(raw)
        self.session = data.get("sessionID")
        if not data.get("success"):
            print(f"  ! login failed (result={data.get('result')}, reason={data.get('resultReason')})")
            return False
        print(f"  login OK | AMP {data.get('result')}")
        return True

    def _resolve(self, parameters: dict[str, Any]) -> dict[str, Any] | None:
        """Substitute any ``<placeholder>`` from values discovered in earlier responses."""
        out: dict[str, Any] = {}
        for key, value in parameters.items():
            if isinstance(value, str) and value.startswith("<") and value.endswith(">"):
                found = self.resolved.get(value.strip("<>"))
                if found is None:
                    return None
                out[key] = found
            else:
                out[key] = value
        return out

    def _learn(self, endpoint: str, parsed: Any) -> None:
        """Pick IDs out of a response so later endpoints have something to ask for."""
        entries: list[dict[str, Any]] = parsed if isinstance(parsed, list) else []
        if endpoint.endswith("GetDatastores") and entries:
            first: dict[str, Any] = entries[0]
            self.resolved.setdefault("datastore_id", first.get("Id", first.get("id")))
        if endpoint.endswith("GetInstances"):
            for target in entries:
                nested: list[dict[str, Any]] = target.get("AvailableInstances", target.get("available_instances")) or []
                for inst in nested:
                    self.resolved.setdefault("instance_id", inst.get("InstanceID", inst.get("instance_id")))
                    self.resolved.setdefault("instance_name", inst.get("InstanceName", inst.get("instance_name")))
                    self.resolved.setdefault("module_name", inst.get("Module", inst.get("module")))
                    return

    def run(self) -> None:
        """Walk every endpoint, writing each response and reporting what happened."""
        self.out.mkdir(parents=True, exist_ok=True)
        written, skipped, failed = 0, 0, 0

        for label, endpoint, raw_params in ENDPOINTS:
            parameters = self._resolve(raw_params)
            if parameters is None:
                missing = [v.strip("<>") for v in raw_params.values() if isinstance(v, str) and v.startswith("<")]
                print(f"  -- {label:24} SKIPPED (never learned: {', '.join(missing)})")
                skipped += 1
                continue
            try:
                status, body = self.post(endpoint, parameters)
            except (urllib.error.URLError, TimeoutError, OSError) as err:
                print(f"  !! {label:24} {type(err).__name__}: {err}")
                failed += 1
                continue

            name = endpoint.split("/")[-1].lower() + ".json"
            note = ""
            parsed: Any = None
            try:
                parsed = json.loads(body) if body.strip() else None
            except json.JSONDecodeError:
                note = "  <- NOT VALID JSON"

            # * Match what the library writes: sanitized keys, so the file lines up with the TypedDicts.
            if parsed is not None and self.sanitizer is not None:
                parsed = self.sanitizer(json=parsed)
                (self.out / name).write_text(json.dumps(parsed, indent=4))
            else:
                (self.out / name).write_bytes(body)
            written += 1

            if parsed is None and not note:
                note = "  <- empty/null body"
            elif isinstance(parsed, list):
                entries: list[Any] = parsed
                note = f"  <- list, {len(entries)} entries" + ("  (EMPTY)" if not entries else "")
            elif isinstance(parsed, dict):
                mapping: dict[str, Any] = parsed
                note = f"  <- dict, {len(mapping)} keys"
                # * Key case depends on whether the sanitizer ran.
                title = mapping.get("title", mapping.get("Title"))
                if title and ("message" in mapping or "Message" in mapping):
                    note += f"  !! {title}"
            self._learn(endpoint, parsed)
            print(f"  ok {label:24} HTTP {status} {len(body):>8} B -> {name}{note}")

        print(f"\n  {written} written, {skipped} skipped, {failed} failed -> {self.out}")
        if self.resolved:
            print(f"  discovered: {self.resolved}")


def main() -> None:
    """Parse arguments, read local.ini and run the dump."""
    parser = argparse.ArgumentParser(description="Dump AMP API responses from a Controller/Target.")
    parser.add_argument("-section", default="CONTROLLER", help="local.ini section to use, default CONTROLLER.")
    parser.add_argument(
        "-out", default="./_responses/controller_setup",
        help="Output directory, default ./_responses/controller_setup so these stay separate from the ADS dumps.",
    )
    parser.add_argument("-ini", default="./local.ini", help="Path to local.ini, default ./local.ini.")
    parser.add_argument("-raw", action="store_true", help="Keep AMP's PascalCase keys instead of sanitizing to snake_case.")
    args = parser.parse_args()

    ini = Path(args.ini)
    if not ini.is_file():
        print(f"!! No ini file at {ini.resolve()}")
        return

    config = ConfigParser()
    config.read(ini.as_posix())
    if args.section not in config.sections():
        print(f"!! Section [{args.section}] not found. Available: {config.sections()}")
        return

    url = config.get(args.section, "URL")
    print(f"[{args.section}] {url}")

    dumper = Dumper(base_url=url, out_dir=Path(args.out), sanitizer=_get_sanitizer(raw=args.raw))
    try:
        if not dumper.login(
            username=config.get(args.section, "USER"),
            password=config.get(args.section, "PASSWORD"),
            token=config.get(args.section, "TOKEN", fallback=""),
        ):
            return
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        print(f"  !! could not reach {url}: {type(err).__name__}: {err}")
        return

    dumper.run()


if __name__ == "__main__":
    main()
