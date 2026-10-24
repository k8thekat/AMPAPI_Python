"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMPAPI_Python.

AMPAPI_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMPAPI_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMPAPI_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

from __future__ import annotations

import ast
import logging
import os
import re
from dataclasses import asdict, fields
from logging import Logger
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

from ._types import ScheduleDataResponse
from .base import Base
from .errors import AMPAPITypeError
from .instance import MinecraftInstance
from .modules import Diagnostics, ScheduleData, SettingsSpecParent

if TYPE_CHECKING:
    from collections.abc import Mapping
    from io import TextIOWrapper

    from ._types import DiagnosticsResponse, PermissionNodeResponse, ScheduleDataResponse, SettingsSpecParentResponse
    from .instance import Controller, Instance, InstanceTypeAliases
    from .modules import Methods, SettingSpec, Triggers

LOGGER: logging.Logger = logging.getLogger(__name__)

# static strings for documentation
_instance_id_note = """.. note::\n\tReplace ``instance-id`` with the something like the :py:class:`~Instance.instance_id` value.\n\n"""
_parent_node_note: str = '.. note::\n\tAll nodes in this section will be prefixed with "%s.", see examples :ref:`Permission Nodes`\n\n'
_wildcard_nodes: str = (
    """.. note::\n\tAny node with a '*' at the end of it is a wild card and using that will make all permissions nodes """
    """in that section equal to the value set, treat it like parent inheritance.\n\n"""
)

_trigger_note: str = """"""

_method_note: str = """"""

# Maps each API spec section name -> (python filename, method name prefix)
_SPEC_MODULE_MAP: dict[str, tuple[str, str]] = {
    "ads_module": ("adsmodule.py", ""),
    "analytics_plugin": ("analytics.py", ""),
    "core": ("core.py", ""),
    "email_sender_plugin": ("emailsender.py", ""),
    "file_manager_plugin": ("filemanager.py", ""),
    "generic_module": ("generic.py", ""),
    "local_file_backup_plugin": ("filebackup.py", ""),
    "minecraft_module": ("minecraft.py", "mc_"),
    "steamcmdplugin": ("steamcmd.py", ""),
}

# Matches "Core/CreateTestTask" and "API/Core/CreateTestTask" style endpoint URLs.
_ENDPOINT_URL_RE = re.compile(r"^(?:API/)?([A-Za-z]+)/([A-Za-z0-9]+)$")
_PYTHON_ONLY_PARAMS: frozenset[str] = frozenset({"format_data", "request_params"})


def _method_event_parse(data: list[Methods], title: str = "", title_body: str = "", path: str | None = None) -> None:
    """Parses method event data and writes it to a .rst file.

    Parameters
    ----------
    data : list[:class:`Methods`]
        The list of dataclass Methods to parse.
    title : :class:`str`, optional
        The Title of the document header; used also as the filename, by default "".
    title_body : :class:`str`, optional
        The body text under the document header, by default "".
    path : :class:`None | str`, optional
        The path to save the .rst file, by default None.

    """
    from docs.samples.method_event_usage import example_note  # noqa: PLC0415

    file_name: str = title.lower().replace(" ", "_")
    _dir: Path = Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
    mode = "x"
    if _dir.exists():
        mode = "w"
    used_ids: list[str] = []
    used_names: list[str] = []
    file = Path.open(_dir, mode)

    # First through iteration, we write our header and title.
    file.write(".. role:: raw-html(raw)\n\t:format: html\n")
    file.write(f"\n{title}\n")
    file.write(f"{repeat_to_length(string=title, repeat_char='=')}\n")
    file.write(":raw-html:`<hr>`\n")
    file.write(title_body + "\n")

    # make a sub heading with "Event Method Names:"
    sub_header: str = "\nMethod Information\n"
    file.write(sub_header)
    file.write(f"{repeat_to_length(string=sub_header, repeat_char='#')}\n")
    file.write(":raw-html:`<hr>`\n")
    file.write("\n" + _method_note)
    file.write(f"\n{example_note}\n")

    for method in sorted(data):
        name = method.name

        if method.id in used_ids:
            continue
        if method.name in used_names:
            name = f"{method.name} - {method.id.split('.')[1]}"
        file.write(f"\n{name}\n")
        used_names.append(method.name)
        file.write(f"{repeat_to_length(string=name, repeat_char='~')}\n")
        file.write(":raw-html:`<hr>`\n")
        file.write(f"{method.description}\n\n")
        file.write(f"- ``{method.id}``\n\n")
        used_ids.append(method.id)
        if len(method.consumes) > 0:
            file.write("Consumes these values:\n")
            # Methods.consumes holds the raw ConsumesResponse dicts unless a Consumes was handed in.
            consumes: list[Mapping[str, Any]] = [consume if isinstance(consume, dict) else asdict(consume) for consume in method.consumes]
            for entry in sorted(consumes, key=lambda x: x["name"]):
                # print(entry, type(entry.enum_values), entry.enum_values)
                file.write(f"\t* {entry['name']}: type({entry['value_type']})\n")
                enum_values: str | dict[str, str] | None = entry.get("enum_values")
                if isinstance(enum_values, dict):
                    for key, value in sorted(enum_values.items()):
                        file.write(f"\t\t* {key} - {value}\n")

    file.close()


async def _parse_get_api_spec_to_file(
    instance: Union[Controller, Instance, MinecraftInstance],
    sanitize_json: bool,
) -> None:
    """|coro|

    Creates a Markdown file related to the type of :param:`instance` that is passed in to the function.
    .. note::
        See directory ``/docs/{Module_type}_api_spec.md``. where {Module_type} is the class ``.Module`` attribute.

    Parameters
    ----------
    instance : Union[Controller, Instance, MinecraftInstance]
        The class of either :py:class:`Controller`, :py:class:`Instance` or :py:class:`MinecraftInstance`.
    sanitize_json : bool
        Sanitize the JSON responses to meet PEP8 compliance. Default is False.

    """
    _logger: Logger = logging.getLogger(__name__)

    data: Mapping[str, Any] = await instance.get_api_spec(sanitize_json=sanitize_json)
    diag_info: Diagnostics | DiagnosticsResponse = await instance.get_diagnostics_info()
    if not isinstance(diag_info, Diagnostics):
        raise AMPAPITypeError(end_point="Core/GetDiagnosticsInfo", cur_type=diag_info, expec_type=Diagnostics)
    instance_type = instance.module

    _dir: Path = Path(__file__).parent.joinpath(f"../docs/api_spec_sheets/{diag_info.application_version}/{instance_type}_api_spec.md")
    _dir.parent.mkdir(parents=True, exist_ok=True)
    _logger.info(
        "Instance Type: %s\nApplication Version: %s\nTools Version: %s\nBuild Date: %s\nPath: %s",
        instance_type,
        diag_info.application_version,
        diag_info.tools_version,
        diag_info.build_date,
        _dir,
    )
    parents: list[str] = []
    mode = "x"
    if _dir.exists():
        mode = "w"
    # TODO: turn these into .rst files instead.
    with Path.open(_dir, mode) as file:
        file.write(f"INSTANCE TYPE: {instance_type}\n")
        file.write(f"APP VERSION: {diag_info.application_version}\n")
        file.write(f"BUILD: {diag_info.build_date}\n\n")

        for parent, parent_value in sorted(data.items()):
            if parent not in parents:
                parents.append(parent)
                file.write("____________________________________________________\n")
                file.write(f"{parent}:\n")
            if isinstance(parent_value, dict):  # pyright: ignore[reportUnnecessaryIsInstance]
                children: dict[str, Any] = parent_value
                for child, child_value in sorted(children.items()):
                    file.write(f"\t{child}:\n")
                    if isinstance(child_value, dict):
                        child_fields: dict[str, Any] = child_value  # pyright: ignore[reportUnknownVariableType]
                        for key, value in sorted(child_fields.items()):
                            if key == "Parameters":
                                file.write(f"\t\t{key}:\n")
                                for entry in sorted(value):
                                    file.write(f"\t\t\t{entry}\n")
                            else:
                                file.write(f"\t\t{key}: {value}\n")

                    else:
                        file.write(f"\t\t({child_value})\n")

        file.close()


def _parse_api_spec_file(path: Path) -> dict[str, dict[str, str]]:
    """Parse an API spec .md file into a flat dict of ``{module.endpoint: {field: value}}``."""
    endpoints: dict[str, dict[str, str]] = {}
    current_parent = ""
    current_child = ""

    with path.open() as file:
        for line in file:
            raw = line.rstrip("\n")
            if not raw.strip() or raw.startswith(("INSTANCE TYPE:", "APP VERSION:", "BUILD:", "____")):
                continue
            stripped = raw.lstrip("\t")
            depth = len(raw) - len(stripped)
            stripped = stripped.rstrip()
            if depth == 0 and stripped.endswith(":"):
                current_parent = stripped[:-1]
            elif depth == 1 and stripped.endswith(":"):
                current_child = stripped[:-1]
                endpoints[f"{current_parent}.{current_child}"] = {}
            elif depth == 2 and ": " in stripped:
                field, _, value = stripped.partition(": ")
                endpoints[f"{current_parent}.{current_child}"][field] = value

    return endpoints


def _write_parameter_diff(file: TextIOWrapper, raw_a: str | None, raw_b: str | None) -> None:
    """Write a human-readable diff of two parameter lists to `file`.

    Parses the raw stringified parameter lists from the spec files and compares them
    by parameter name, reporting which parameters were added, removed, or modified
    between the two versions.

    Parameters
    ----------
    file : :class:`TextIOWrapper`
        The open file handle to write the diff output to.
    raw_a : Union[:class:`str`, None]
        The raw parameter string from the older spec version.
    raw_b : Union[:class:`str`, None]
        The raw parameter string from the newer spec version.

    """
    try:
        params_a: list[dict[str, Any]] = ast.literal_eval(raw_a) if raw_a else []
        params_b: list[dict[str, Any]] = ast.literal_eval(raw_b) if raw_b else []
    except (ValueError, SyntaxError):
        # Fallback to the raw dump when the parameter string is not parseable.
        file.write("**parameters**:\n")
        file.write(f"- `{raw_a}`\n")
        file.write(f"+ `{raw_b}`\n\n")
        return

    by_name_a: dict[str, dict[str, Any]] = {p["name"]: p for p in params_a}
    by_name_b: dict[str, dict[str, Any]] = {p["name"]: p for p in params_b}
    names_a = set(by_name_a)
    names_b = set(by_name_b)

    added_params = sorted(names_b - names_a)
    removed_params = sorted(names_a - names_b)

    # Fields worth showing when they change between versions.
    _compare_fields = ("type_name", "optional", "description", "param_enum_values")
    modified_params: list[tuple[str, list[str]]] = []
    for name in sorted(names_a & names_b):
        diffs: list[str] = []
        for field in _compare_fields:
            old_val = by_name_a[name].get(field)
            new_val = by_name_b[name].get(field)
            if old_val != new_val:
                diffs.append(f"{field}: `{old_val}` -> `{new_val}`")
        if diffs:
            modified_params.append((name, diffs))

    if not added_params and not removed_params and not modified_params:
        return

    file.write("**parameters**:\n\n")

    if added_params:
        for name in added_params:
            param = by_name_b[name]
            optional_tag = ", optional" if param.get("optional") else ""
            file.write(f"- Added: `{name}` ({param.get('type_name', '?')}{optional_tag})\n")
        file.write("\n")

    if removed_params:
        for name in removed_params:
            param = by_name_a[name]
            file.write(f"- Removed: `{name}` ({param.get('type_name', '?')})\n")
        file.write("\n")

    if modified_params:
        for name, diffs in modified_params:
            file.write(f"- Changed: `{name}`\n")
            for diff_line in diffs:
                file.write(f"  - {diff_line}\n")
        file.write("\n")


def _write_permissions_diff(file: TextIOWrapper, raw_a: str | None, raw_b: str | None) -> None:
    """Write a human-readable diff of two permission lists to `file`.

    Parses the raw stringified permission lists from the spec files and compares them
    as sets, reporting which permissions were added or removed between the two versions.

    Parameters
    ----------
    file : :class:`TextIOWrapper`
        The open file handle to write the diff output to.
    raw_a : Union[:class:`str`, None]
        The raw permissions string from the older spec version.
    raw_b : Union[:class:`str`, None]
        The raw permissions string from the newer spec version.

    """
    try:
        perms_a: set[str] = set(ast.literal_eval(raw_a)) if raw_a and raw_a != "None" else set()
        perms_b: set[str] = set(ast.literal_eval(raw_b)) if raw_b and raw_b != "None" else set()
    except (ValueError, SyntaxError):
        file.write("**required_permissions**:\n")
        file.write(f"- `{raw_a}`\n")
        file.write(f"+ `{raw_b}`\n\n")
        return

    # When the old value was literally None (not tracked), label it as newly defined.
    was_none = raw_a is None or raw_a == "None"

    added_perms = sorted(perms_b - perms_a)
    removed_perms = sorted(perms_a - perms_b)

    if not added_perms and not removed_perms and not was_none:
        return

    file.write("**required_permissions**:\n\n")

    if was_none and added_perms:
        file.write("- Previously: *not defined*\n")
        for perm in added_perms:
            file.write(f"- Added: `{perm}`\n")
    elif was_none:
        file.write("- Previously: *not defined*\n")
        file.write("- Now: *none required*\n")
    else:
        for perm in added_perms:
            file.write(f"- Added: `{perm}`\n")
        for perm in removed_perms:
            file.write(f"- Removed: `{perm}`\n")

    file.write("\n")


def compare_api_spec_versions(
    version_a: str,
    version_b: str,
    instance_type: str,
    base_path: Path | None = None,
    output_path: Path | None = None,
) -> None:
    """Compare two versions of an API spec sheet and write a diff summary to a Markdown file.

    Parameters
    ----------
    version_a : str
        The older/base version string (e.g. ``"2.6.0.0"``).
    version_b : str
        The newer version string to compare against (e.g. ``"2.6.5.0"``).
    instance_type : str
        The Instance type identifier matching the filename (e.g. ``"ADS"`` or ``"Minecraft"``).
    base_path : Path | None, optional
        Root of the ``api_spec_sheets`` directory. Defaults to ``../docs/api_spec_sheets`` relative to this file.
    output_path : Path | None, optional
        Full path for the output diff file. Defaults to ``{base_path}/diffs/{instance_type}_{version_a}_to_{version_b}.md``.

    """
    _logger: Logger = logging.getLogger(__name__)

    _base: Path = base_path if base_path is not None else Path(__file__).parent.parent.joinpath("docs/api_spec_sheets")

    file_a = _base / version_a / f"{instance_type}_api_spec.md"
    file_b = _base / version_b / f"{instance_type}_api_spec.md"

    for _file in (file_a, file_b):
        if not _file.exists():
            _logger.error("API spec file not found: %s", _file)
            return

    spec_a = _parse_api_spec_file(file_a)
    spec_b = _parse_api_spec_file(file_b)

    keys_a = set(spec_a)
    keys_b = set(spec_b)
    added = sorted(keys_b - keys_a)
    removed = sorted(keys_a - keys_b)
    changed = sorted(k for k in keys_a & keys_b if spec_a[k] != spec_b[k])

    _out: Path = output_path if output_path is not None else _base / "diffs" / f"{instance_type}_{version_a}_to_{version_b}.md"
    _out.parent.mkdir(parents=True, exist_ok=True)

    with _out.open("w") as file:
        file.write(f"# API Spec Diff: {instance_type}\n\n")
        file.write(f"FROM: `{version_a}`  \nTO: `{version_b}`\n\n")

        file.write(f"## Added Endpoints ({len(added)})\n\n")
        for key in added:
            file.write(f"### + `{key}`\n\n")
            for field, value in spec_b[key].items():
                file.write(f"- **{field}**: {value}\n")
            file.write("\n")

        file.write(f"## Removed Endpoints ({len(removed)})\n\n")
        for key in removed:
            file.write(f"### - `{key}`\n\n")
            for field, value in spec_a[key].items():
                file.write(f"- **{field}**: {value}\n")
            file.write("\n")

        file.write(f"## Changed Endpoints ({len(changed)})\n\n")
        for key in changed:
            file.write(f"### ~ `{key}`\n\n")
            for field in sorted(spec_a[key].keys() | spec_b[key].keys()):
                val_a = spec_a[key].get(field)
                val_b = spec_b[key].get(field)
                if val_a == val_b:
                    continue

                if field == "parameters":
                    _write_parameter_diff(file, val_a, val_b)
                elif field == "required_permissions":
                    _write_permissions_diff(file, val_a, val_b)
                else:
                    file.write(f"**{field}**:\n")
                    file.write(f"- `{val_a}`\n")
                    file.write(f"+ `{val_b}`\n\n")

    _logger.info(
        "Diff written to %s | Added: %d | Removed: %d | Changed: %d",
        _out,
        len(added),
        len(removed),
        len(changed),
    )


def _get_endpoint_urls(filepath: Path) -> set[str]:
    """Return the normalized endpoint URLs a Python source file posts to.

    Collects every string literal passed as a ``url=`` or ``endpoint=`` keyword argument whose
    value looks like ``Module/EndpointName`` (an optional leading ``API/`` is ignored).

    Parameters
    ----------
    filepath : :class:`Path`
        The path to the Python source file to parse.

    Returns
    -------
    set[:class:`str`]
        The URLs in :func:`_normalize_endpoint` form, eg. ``core/createtesttask``.

    """
    urls: set[str] = set()
    tree = ast.parse(filepath.read_text())
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg not in ("url", "endpoint"):
                continue
            if not isinstance(keyword.value, ast.Constant) or not isinstance(keyword.value.value, str):
                continue
            match = _ENDPOINT_URL_RE.match(keyword.value.value)
            if match:
                urls.add(f"{_normalize_endpoint(match.group(1))}/{_normalize_endpoint(match.group(2))}")
    return urls


def _normalize_endpoint(name: str) -> str:
    """Lowercase a name and drop its underscores so ``snake_case`` and ``PascalCase`` names compare equal.

    Parameters
    ----------
    name : :class:`str`
        A spec section, a spec endpoint or a URL part, eg. ``get_webauthn_credential_i_ds``.

    Returns
    -------
    :class:`str`
        The normalized name, eg. ``getwebauthncredentialids``.

    """
    return name.replace("_", "").lower()


def _get_function_signatures(filepath: Path) -> dict[str, list[str]]:
    """Return all method signatures from a Python source file.

    Parameters
    ----------
    filepath : :class:`Path`
        The path to the Python source file to parse.

    Returns
    -------
    dict[:class:`str`, list[:class:`str`]]
        A mapping of ``{method_name: [param_names]}``, excluding ``self``.

    """
    result: dict[str, list[str]] = {}
    tree = ast.parse(filepath.read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params = [arg.arg for arg in node.args.args if arg.arg != "self"]
            params += [arg.arg for arg in node.args.kwonlyargs]
            result[node.name] = params
    return result


def find_missing_endpoints(
    spec_path: Path | None = None,
    ampapi_path: Path | None = None,
    output_path: Path | None = None,
    suffix_aliases: list[str] | None = None,  # noqa: ARG001 # kept so existing callers still work, see the docstring
) -> None:
    """Compare all API spec sheets against their Python implementations and report missing endpoints.

    Merges endpoints across all ``*_api_spec.md`` files found in ``spec_path``, then checks each
    spec section against the corresponding Python module file using :data:`_SPEC_MODULE_MAP`.
    Results are written to a Markdown file and summarised via logging.

    .. note::
        An endpoint counts as implemented when any module in ``ampapi_path`` posts to its URL (eg.
        ``url="Core/CreateTestTask"``), whatever the wrapper method is named. This covers renamed wrappers,
        private ``DEV:`` wrappers and endpoints folded into another method. Spec and URL names are compared
        lowercased with underscores removed, and the spec section must match the URL's module part
        (``ads_module`` -> ``ADSModule/``).

    Parameters
    ----------
    spec_path : Path | None, optional
        Directory containing ``*_api_spec.md`` files. Defaults to ``../docs/api_spec_sheets`` relative to this file.
    ampapi_path : Path | None, optional
        Directory containing the Python module files. Defaults to the directory of this file.
    output_path : Path | None, optional
        Path for the output report. Defaults to ``{spec_path}/missing_endpoints.md``.
    suffix_aliases : list[str] | None, optional
        Unused here since endpoints are matched on their URL rather than the method name; still accepted so
        existing calls keep working, by default None.

    """
    _logger: Logger = logging.getLogger(__name__)
    _spec_dir: Path = spec_path if spec_path is not None else Path(__file__).parent.parent.joinpath("docs/api_spec_sheets")
    _ampapi_dir: Path = ampapi_path if ampapi_path is not None else Path(__file__).parent

    # Merge endpoints from all spec files, keyed by section
    all_spec: dict[str, set[str]] = {}
    for spec_file in sorted(_spec_dir.glob("**/*_api_spec.md")):
        current_parent: str = ""
        with spec_file.open() as file:
            for line in file:
                raw = line.rstrip("\n")
                if not raw.strip() or raw.startswith(("INSTANCE TYPE:", "APP VERSION:", "BUILD:", "____")):
                    continue
                stripped = raw.lstrip("\t")
                depth = len(raw) - len(stripped)
                stripped = stripped.rstrip()
                if depth == 0 and stripped.endswith(":"):
                    current_parent = stripped[:-1]
                    all_spec.setdefault(current_parent, set())
                elif depth == 1 and stripped.endswith(":") and current_parent:
                    all_spec[current_parent].add(stripped[:-1])

    _out: Path = output_path if output_path is not None else _spec_dir / "missing_endpoints.md"

    # Every endpoint URL any module posts to; "Core/Login" lives in base.py, so all of the modules are read.
    implemented_urls: set[str] = set()
    for module_path in sorted(_ampapi_dir.glob("*.py")):
        implemented_urls |= _get_endpoint_urls(module_path)

    total_missing = 0
    with _out.open("w") as out_file:
        out_file.write("# Missing Endpoint Implementations\n\n")

        for section, (py_file, prefix) in sorted(_SPEC_MODULE_MAP.items()):
            spec_endpoints = all_spec.get(section, set())
            py_path = _ampapi_dir / py_file

            if not py_path.exists():
                _logger.warning("Python file not found for section '%s': %s", section, py_path)
                out_file.write(f"## {section} -> `{py_file}` NOT FOUND\n\n")
                continue

            section_key: str = _normalize_endpoint(section)
            missing = sorted(ep for ep in spec_endpoints if f"{section_key}/{_normalize_endpoint(ep)}" not in implemented_urls)
            total_missing += len(missing)

            # The link is relative to the report, wherever it is written to.
            py_link: str = Path(os.path.relpath(py_path, _out.parent)).as_posix()
            out_file.write(f"## {section} -> [{py_file}]({py_link})\n\n")
            out_file.write(f"- Spec endpoints : {len(spec_endpoints)}\n")
            out_file.write(f"- Implemented    : {len(spec_endpoints) - len(missing)}\n")
            out_file.write(f"- Missing        : {len(missing)}\n\n")
            if missing:
                for ep in missing:
                    out_file.write(f"- `{prefix}{ep}`\n")
            else:
                out_file.write("_All endpoints implemented._\n")
            out_file.write("\n")

    _logger.info("Missing endpoint report written to %s | Total missing: %d", _out, total_missing)


def find_parameter_mismatches(
    spec_path: Path | None = None,
    ampapi_path: Path | None = None,
    output_path: Path | None = None,
    suffix_aliases: list[str] | None = None,  # noqa: ARG001 # kept so existing callers still work, see the docstring
) -> None:
    """Compare implemented Python method parameters against their API spec definitions and report mismatches.

    For each endpoint that exists in both the spec sheets and the Python implementation, compares
    the parameter names from the spec (converted to snake_case via :meth:`Base.camel_to_snake_re`)
    against the actual Python function signature. Python-only parameters (e.g. ``format_data``)
    defined in :data:`_PYTHON_ONLY_PARAMS` are excluded from the comparison. Results are written
    to a Markdown file and summarised via logging.

    .. note::
        A spec endpoint is matched to the Python methods that post to its URL (eg. ``url="Core/CreateTestTask"``),
        whatever the method is named, the same matching :func:`find_missing_endpoints` uses.


    .. note::
        Only the newest spec version directory under `spec_path` is compared (versions compare as numbers, so
        `2.10.0.0` is newer than `2.8.0.8`). When `spec_path` holds no version directories, every
        ``*_api_spec.md`` file under it is merged instead.


    Parameters
    ----------
    spec_path : Path | None, optional
        Directory containing the versioned spec directories, or the ``*_api_spec.md`` files themselves.
        Defaults to ``../docs/api_spec_sheets`` relative to this file.
    ampapi_path : Path | None, optional
        Directory containing the Python module files. Defaults to the directory of this file.
    output_path : Path | None, optional
        Path for the output report. Defaults to ``{spec_path}/parameter_mismatches.md``.
    suffix_aliases : list[str] | None, optional
        Unused here since endpoints are matched on their URL rather than the method name; still accepted so
        existing calls keep working, by default None.

    """
    _logger: Logger = logging.getLogger(__name__)
    _spec_dir: Path = spec_path if spec_path is not None else Path(__file__).parent.parent.joinpath("docs/api_spec_sheets")
    _ampapi_dir: Path = ampapi_path if ampapi_path is not None else Path(__file__).parent

    # Versions compare as int tuples, so 2.10.0.0 sorts after 2.8.0.8.
    version_dirs: dict[tuple[int, ...], Path] = {
        tuple(int(part) for part in child.name.split(".")): child
        for child in _spec_dir.iterdir()
        if child.is_dir() and re.fullmatch(r"\d+(\.\d+)*", child.name)
    }
    spec_root: Path = _spec_dir
    if version_dirs:
        spec_root = version_dirs[max(version_dirs)]
        _logger.info("Comparing against the newest spec version: %s", spec_root.name)

    all_spec: dict[str, dict[str, str]] = {}
    for spec_file in sorted(spec_root.glob("**/*_api_spec.md")):
        for key, fields in _parse_api_spec_file(spec_file).items():
            all_spec.setdefault(key, fields)

    # Every method that posts to a URL, keyed by the URL in `_normalize_endpoint` form.
    methods_by_url: dict[str, list[tuple[str, str, list[str]]]] = {}
    for module_path in sorted(_ampapi_dir.glob("*.py")):
        signatures = _get_function_signatures(module_path)
        for node in ast.walk(ast.parse(module_path.read_text())):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for call in ast.walk(node):
                if not isinstance(call, ast.Call):
                    continue
                for keyword in call.keywords:
                    if keyword.arg not in ("url", "endpoint"):
                        continue
                    if not isinstance(keyword.value, ast.Constant) or not isinstance(keyword.value.value, str):
                        continue
                    match = _ENDPOINT_URL_RE.match(keyword.value.value)
                    if match is None:
                        continue
                    url_key = f"{_normalize_endpoint(match.group(1))}/{_normalize_endpoint(match.group(2))}"
                    entry = (module_path.name, node.name, signatures[node.name])
                    if entry not in methods_by_url.setdefault(url_key, []):
                        methods_by_url[url_key].append(entry)

    _out: Path = output_path if output_path is not None else _spec_dir / "parameter_mismatches.md"

    total_mismatches = 0
    with _out.open("w") as out_file:
        out_file.write("# Parameter Mismatches\n\n")

        for section, (py_file, _prefix) in sorted(_SPEC_MODULE_MAP.items()):
            py_path = _ampapi_dir / py_file
            if not py_path.exists():
                _logger.warning("Python file not found for section '%s': %s", section, py_path)
                continue

            section_mismatches: list[str] = []

            for key, fields in sorted(all_spec.items()):
                parent, _, endpoint = key.partition(".")
                if parent != section:
                    continue

                # # Resolve the Python method name, accounting for suffix aliases.
                # full = prefix + endpoint
                # py_method: str | None = None
                # if full in signatures:
                #     py_method = full
                # else:
                #     for alias in _aliases:
                #         if (full + alias) in signatures:
                #             py_method = full + alias
                #             break
                # if py_method is None:
                #     continue  # unimplemented endpoint; covered by find_missing_endpoints

                # py_params: set[str] = set(signatures[py_method]) - _PYTHON_ONLY_PARAMS

                url_key = f"{_normalize_endpoint(section)}/{_normalize_endpoint(endpoint)}"
                if url_key not in methods_by_url:
                    continue  # unimplemented endpoint; covered by find_missing_endpoints

                raw_params_str = fields.get("parameters", "[]")
                try:
                    spec_param_list: list[dict[str, Any]] = ast.literal_eval(raw_params_str)
                except (ValueError, SyntaxError):
                    _logger.warning("Could not parse parameters for %s: %s", key, raw_params_str)
                    continue

                spec_params: set[str] = {Base.camel_to_snake_re(p["name"]) for p in spec_param_list}

                # missing_in_python = sorted(spec_params - py_params)
                # extra_in_python = sorted(py_params - spec_params)

                # if missing_in_python or extra_in_python:
                #     total_mismatches += 1
                #     section_mismatches.append(f"### `{key}`\n\n")
                #     if missing_in_python:
                #         section_mismatches.append("**In spec, missing from Python:**\n")
                #         section_mismatches.extend(f"- `{p}`\n" for p in missing_in_python)
                #         section_mismatches.append("\n")
                #     if extra_in_python:
                #         section_mismatches.append("**In Python, not in spec:**\n")
                #         section_mismatches.extend(f"- `{p}`\n" for p in extra_in_python)
                #         section_mismatches.append("\n")

                for method_file, method_name, method_params in methods_by_url[url_key]:
                    py_params: set[str] = set(method_params) - _PYTHON_ONLY_PARAMS
                    missing_in_python = sorted(spec_params - py_params)
                    extra_in_python = sorted(py_params - spec_params)

                    if missing_in_python or extra_in_python:
                        total_mismatches += 1
                        section_mismatches.append(f"### `{key}` -> `{method_file}::{method_name}`\n\n")
                        if missing_in_python:
                            section_mismatches.append("**In spec, missing from Python:**\n")
                            section_mismatches.extend(f"- `{p}`\n" for p in missing_in_python)
                            section_mismatches.append("\n")
                        if extra_in_python:
                            section_mismatches.append("**In Python, not in spec:**\n")
                            section_mismatches.extend(f"- `{p}`\n" for p in extra_in_python)
                            section_mismatches.append("\n")

            # The link is relative to the report, wherever it is written to.
            py_link: str = Path(os.path.relpath(py_path, _out.parent)).as_posix()
            out_file.write(f"## {section} -> [{py_file}]({py_link})\n\n")
            if section_mismatches:
                out_file.writelines(section_mismatches)
            else:
                out_file.write("_No parameter mismatches._\n")
            out_file.write("\n")

    _logger.info(
        "Parameter mismatch report written to %s | Total endpoints with mismatches: %d",
        _out,
        total_mismatches,
    )


def _permission_node_parse(
    data: list[PermissionNodeResponse],
    title: str = "",
    title_body: str = "",
    index: int = 0,
    path: str | None = None,
    file: Union[TextIOWrapper, None] = None,
) -> None:
    from docs.samples.permission_node_usage import example_note  # noqa: PLC0415

    used_keys: list[Any] = []

    file_name: str = title.lower().replace(" ", "_")
    _dir: Path = Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
    mode = "x"
    if _dir.exists():
        mode = "w"

    if file is None:
        file = Path.open(_dir, mode)

    if index == 0:
        # First through iteration, we write our header and title.
        file.write(".. role:: raw-html(raw)\n\t:format: html\n")
        file.write(f"\n{title}\n")
        file.write(f"{repeat_to_length(string=title, repeat_char='=')}\n")
        file.write(":raw-html:`<hr>`\n\n")
        file.write(title_body + "\n")
        file.write("\n" + _wildcard_nodes)
        file.write(f"\n{example_note}\n")

    for entry in sorted(data, key=lambda x: x["name"]):
        # print(f"Currently on {index} -- checking {entry['name']} | not used?: {entry['name'] not in used_keys}")
        if entry["name"] not in used_keys and index == 0:
            used_keys.append(entry["name"])

            # Our first headers.
            header = entry["name"] + " Permission Nodes"
            file.write(f"\n{header}\n")
            file.write(f"{repeat_to_length(string=header, repeat_char='#')}\n")
            file.write(":raw-html:`<hr>`\n\n")

            # Our node description handler.
            _temp: str | None = entry.get("description")
            if _temp is not None and len(_temp) > 0:
                file.write(f"Description: {entry['description']}\n\n")

            temp: list[str] = entry["node"].split(".")
            # This is to handle Instances having their Instance ID as the value.
            if entry["node"].startswith("Instances") and isinstance(entry["children"], list):
                file.write(_instance_id_note)

                # Handles formatting our nodes
                file.write(f"- {temp[-1]}.*\n")

                for children in entry["children"]:
                    # We cheaply ignore them since they always have a "-" in them.
                    if "-" in children["name"]:
                        new_child: list[PermissionNodeResponse] = children.get("children") or []
                        if len(new_child) > 0:
                            for node in sorted(new_child[0]["children"] or [], key=lambda x: x["name"]):
                                # Handles formatting our nodes
                                file.write(f"- Instances.`instance-id`.{node['name']}\n")

                continue
            # Our notes about the prefix characters.
            file.write(_parent_node_note % entry["name"] + "\n")
            # Handles formatting our nodes
            file.write(f"- {temp[-1]}.*\n")
        if entry["name"] not in used_keys and index == 1:
            used_keys.append(entry["name"])

            # Our second headers.
            header = entry["name"] + " Nodes"
            # file.write("\n:raw-html:`<hr>`\n")
            file.write(f"\n{header}\n")
            file.write(f"{repeat_to_length(string=header, repeat_char='~')}\n")
            file.write(":raw-html:`<hr>`\n\n")

            # Our node description handler.
            _temp: str | None = entry.get("description")
            if _temp is not None and len(_temp) > 0:
                file.write(f"Description: {entry['description']}\n\n")

            # Handles formatting our nodes
            temp = entry["node"].split(".")

            # These 4 modules DO NOT have 2 layers of parents to get through. So we need to cut them shorter.
            if entry["node"].startswith(("ADS", "FileManager", "LocalFileBackup", "Core")) and isinstance(
                entry["children"],
                list,
            ):
                file.write(f"- {temp[-1]}.*\n")
                for node in sorted(entry["children"], key=lambda x: x["name"]):
                    file.write(f"- {temp[-1]}.{node['name']}\n")
                continue
            # Our notes about the prefix characters with the passed in var post %.
            file.write(_parent_node_note % entry["name"] + "\n")

            # Handles formatting our nodes
            file.write(f"- {temp[-1]}.*\n")
        if entry["name"] not in used_keys and index == 2:
            used_keys.append(entry["name"])
            header: str | Any = entry["name"] + " Nodes"
            if entry["node"].startswith("Settings.FileManagerPlugin."):
                header = "FMP " + header

            # Handles the Header for the rst to break up sections. This is our second subsection.
            file.write(f"\n{header}\n")
            file.write(f"{repeat_to_length(string=header, repeat_char='^')}\n")
            file.write(":raw-html:`<hr>`\n\n")

            # Handles formatting our nodes
            temp = entry["node"].split(".")
            file.write(f"- {temp[-1]}.*\n")

            # handles the remaining entries of our nodes.
            if isinstance(entry["children"], list):
                for node in sorted(entry["children"], key=lambda x: x["name"]):
                    # Handles formatting our nodes
                    file.write(f"- {temp[-1]}.{node['name']}\n")

        if isinstance(entry["children"], list):
            _permission_node_parse(data=entry["children"], index=index + 1, file=file)

    if index == 0:
        file.close()


def _settings_node_parse(
    data: SettingsSpecParent,
    title: str = "",
    title_body: str = "",
    index: int = 0,
    path: str | None = None,
    file: Union[TextIOWrapper, None] = None,
) -> None:
    from docs.samples.settings_node_usage import example_note  # noqa: PLC0415

    file_name: str = title.lower().replace(" ", "_")
    _dir: Path = Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
    mode = "x"
    if _dir.exists():
        mode = "w"

    if file is None:
        file = Path.open(_dir, mode)

    if index == 0:
        # First through iteration, we write our header and title.
        file.write(".. role:: raw-html(raw)\n\t:format: html\n")
        file.write(f"\n{title}\n")
        file.write(f"{repeat_to_length(string=title, repeat_char='=')}\n")
        file.write(":raw-html:`<hr>`\n\n")
        file.write(title_body + "\n")
        file.write("\n" + _wildcard_nodes)
        file.write(f"\n{example_note}\n")

    # for key in sorted(vars(data)):
    # SettingsSpecParent is slotted and has no __dict__. Its fields hold the same names.
    for key in sorted(field.name for field in fields(data)):
        # Our second headers.
        header: str = "Settings " + key.title() + " Nodes"
        # file.write("\n:raw-html:`<hr>`\n")
        file.write(f"\n{header}\n")
        file.write(f"{repeat_to_length(string=header, repeat_char='#')}\n")
        file.write(":raw-html:`<hr>`\n\n")

        data_key: list[SettingSpec] = getattr(data, key)
        if isinstance(data_key, list):  # pyright: ignore[reportUnnecessaryIsInstance]
            for entry in sorted(data_key):
                file.write(f"\n**Name**: {entry.name}\n")
                if len(entry.description) > 0:
                    file.write(f"\t| Description: {str_sanitizer_sphinx(string=entry.description, special_chars=('*',))}\n")
                file.write(f"\t| Node: `{entry.node}`\n")
    file.close()


def _trigger_event_parse(
    data: list[Triggers],
    title: str = "",
    title_body: str = "",
    path: str | None = None,
) -> None:
    """Assumes you have acquired the ScheduleData already and are passing in :attr:`~scheduleData.available_triggers`

    .. note::
        All of these triggers will have a unique ID field that is generated from :meth:`~Core.get_triggers` due to uniqueness.


    Parameters
    ----------
    data : list[:class:`Triggers`]
        The list of dataclass Triggers.
    title : :class:`str`, optional
        The Title of the document header; this is also used to set the filename, by default "".
    title_body : :class:`str`, optional
        The body just under the document header, by default "".
    path : :class:`None | str`, optional
        The path to save the .rst file., by default None.

    """
    from docs.samples.trigger_event_usage import example_note  # noqa: PLC0415

    file_name: str = title.lower().replace(" ", "_")
    _dir: Path = Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
    mode = "x"
    if _dir.exists():
        mode = "w"

    file = Path.open(_dir, mode)

    # First through iteration, we write our header and title.
    file.write(".. role:: raw-html(raw)\n\t:format: html\n")
    file.write(f"\n{title}\n")
    file.write(f"{repeat_to_length(string=title, repeat_char='=')}\n")
    file.write(":raw-html:`<hr>`\n\n")
    file.write(title_body + "\n")

    sub_header: str = "\nEvents Information\n"
    file.write(sub_header)
    file.write(f"{repeat_to_length(string=sub_header, repeat_char='#')}\n")
    file.write(":raw-html:`<hr>`\n")
    file.write("\n" + _trigger_note)
    file.write(f"\n{example_note}\n")
    for trigger in sorted(data):
        _temp: str = " | "
        file.write("\n:raw-html:`<hr>`\n")
        file.write(f"**Trigger Description**: {trigger.description}\n\n")
        if len(trigger.emits) > 0:
            file.write(f"- Emits: {_temp.join(trigger.emits)}\n")
    file.close()


async def amp_api_update(instance: Controller, sanitize_json: bool) -> None:
    """|coro|

    Gets the AMP Instance API Endpoints and writes them out to a file. Used for version changes.

    .. note::
        Having a ``Minecraft`` type Instance is beneficial for this call. Otherwise you will only get the ADS/Controller API spec sheet.


    Parameters
    ----------
    instance : :class:`Controller`
        Must be the Controller Instance; as we are looking for the ADS and a Minecraft Instance.
    sanitize_json : bool
        Sanitize the JSON responses to meet PEP8 compliance.

    """
    _logger: Logger = logging.getLogger(__name__)
    # We call get_instances() to force a current listing of Instances to be populated.
    await instance.get_instances()
    ads_diag: Diagnostics | DiagnosticsResponse = await instance.get_diagnostics_info()
    # cur_version: None | AMPMinecraftInstance = None
    # A remote Target's Instances live on its TargetADS, so we look through those too.
    every_instance: set[InstanceTypeAliases] = set(instance.instances)
    for target_ads in instance.targets.values():
        every_instance.update(target_ads.instances)
    for entry in every_instance:
        # Minecraft Instances have their own unique API endpoints; so we need to get those.
        if entry.module == "Minecraft" and isinstance(entry, MinecraftInstance) and entry.running is True:
            instance_diag: Diagnostics | DiagnosticsResponse = await entry.get_diagnostics_info()
            # if isinstance(ads_diag, Diagnostics) and isinstance(instance_diag, Diagnostics):
            #     if instance_diag.application_version == ads_diag.application_version:
            #         _logger.info(
            #             "Found %s matching the current ADS version `%s` .",
            #             entry.instance_name,
            #             ads_diag.application_version,
            #         )
            #         await _parse_get_api_spec_to_file(instance=entry, sanitize_json=sanitize_json)
            #         break
            #     _logger.warning(
            #         "<%s.%s> | Version mismatch between the Instance and the ADS. ADS: %s | Instance: %s",
            #         "util",
            #         "amp_api_update",
            #         instance_diag.application_version,
            #         ads_diag.application_version,
            #     )
            # err = "Responses are of the wrong type. ADS: %s | Instance: %s"
            # raise TypeError(err, type(ads_diag), type(instance_diag))

            if not isinstance(ads_diag, Diagnostics) or not isinstance(instance_diag, Diagnostics):
                msg = f"Responses are of the wrong type. ADS: {type(ads_diag)} | Instance: {type(instance_diag)}"
                raise TypeError(msg)
            if instance_diag.application_version == ads_diag.application_version:
                _logger.info(
                    "Found %s matching the current ADS version `%s` .",
                    entry.instance_name,
                    ads_diag.application_version,
                )
                await _parse_get_api_spec_to_file(instance=entry, sanitize_json=sanitize_json)
                break
            # A mismatched Instance isn't fatal, we just move on and try the next one.
            _logger.warning(
                "<%s.%s> | Version mismatch between the Instance and the ADS. ADS: %s | Instance: %s",
                "util",
                "amp_api_update",
                ads_diag.application_version,
                instance_diag.application_version,
            )
    # We found our Minecraft Instance, now lets parse our Controller/ADS
    await _parse_get_api_spec_to_file(instance=instance, sanitize_json=sanitize_json)


def dict_merge(dict1: ScheduleDataResponse, dict2: ScheduleDataResponse) -> ScheduleDataResponse:
    """Merges dict2 into dict1 with key overlapp but combining data instead of replacing key data.

    .. note::
        This was made for `ScheduleDataResponse` specifically to merge the lists of available methods and triggers under the same key.


    Parameters
    ----------
    dict1 : :class:`ScheduleDataResponse`
        The origin dict.
    dict2 : :class:`ScheduleDataResponse`
        The dict to merge keys from.

    Returns
    -------
    :class:`ScheduleDataResponse`
        Merged dictionary.

    """
    # _temp: defaultdict[str, list[MethodsData | TriggersData]] = defaultdict(list)
    dict1["available_methods"].extend(dict2["available_methods"])
    dict1["available_triggers"].extend(dict2["available_triggers"])
    dict1["populated_triggers"].extend(dict2["populated_triggers"])
    return dict1


async def generate_docs_rst(instance: Controller) -> None:
    """|coro|

    This will generate the Sphinx ``.rst`` files we use for documentation. The files will be written to ``../docs/nodes/``

    .. warning::
        There may be a few errors due to the formatting of AMPs return information; so it is wrapped in ``try/excepts``


    Parameters
    ----------
    instance : :class:`Controller`
        Must be the Controller Instance, as the API endpoint :meth:`get_setting_spec` is not available to all.

    """
    logger: Logger = logging.getLogger(__name__)
    spec: SettingsSpecParent | SettingsSpecParentResponse = await instance.get_setting_spec()
    if not isinstance(spec, SettingsSpecParent):
        raise AMPAPITypeError(end_point="Core/GetSettingSpec", cur_type=spec, expec_type=SettingsSpecParent)

    _path: Path = Path(__file__).parent.joinpath("../docs/nodes")

    logger.info("Generating Settings Node.rst...")
    # As far as I know settings spec information is the same for all Instances
    try:
        _settings_node_parse(data=spec, title="Setting Nodes", title_body="", path=_path.as_posix())
    except Exception:
        # logger.error("Ran into a <Exception> when attempting to generate the Setting Nodes.rst.\n %s", traceback.print_exc())
        logger.exception("Ran into a <Exception> when attempting to generate the Setting Nodes.rst.")
    # As far as I know Permission spec information is the same for all Instances
    permission_nodes = await instance.get_permissions_spec(format_data=False)
    perms: list[PermissionNodeResponse] = [node for node in permission_nodes if isinstance(node, dict)]
    logger.info("Generating Permission Nodes.rst...")
    try:
        _permission_node_parse(data=perms, title="Permission Nodes", title_body="", path=_path.as_posix())
    except Exception:
        # logger.error(
        #     "Ran into a <Exception> when attempting to generate the Permission Nodes.rst.\n %s",
        #     traceback.print_exc(),
        # )
        logger.exception("Ran into a <Exception> when attempting to generate the Permission Nodes.rst.")

    logger.info("Generating Triggers Events.rst and Method Events.rst...")
    await instance.get_instances()
    # data: ScheduleData = await instance.get_schedule_data(format_data=True)
    data: ScheduleData | ScheduleDataResponse = await instance.get_schedule_data(format_data=False)
    if not isinstance(data, dict):
        raise AMPAPITypeError(end_point="Core/GetScheduleData", cur_type=data, expec_type=dict)
    mc_: bool = False
    gen_: bool = False
    src_: bool = False
    # A remote Target's Instances live on its TargetADS, so we look through those too.
    every_instance: set[InstanceTypeAliases] = set(instance.instances)
    for target_ads in instance.targets.values():
        every_instance.update(target_ads.instances)
    for entry in every_instance:
        # print(entry.running, entry.friendly_name, entry.module)
        if mc_ is False and entry.running and entry.module == "Minecraft":
            mc_data: ScheduleData | ScheduleDataResponse = await entry.get_schedule_data(format_data=False)
            if not isinstance(mc_data, dict):
                raise AMPAPITypeError(end_point="Core/GetScheduleData", cur_type=mc_data, expec_type=dict)
            data = dict_merge(data, mc_data)
            mc_ = True
        # AMP 2.8 reports Generic Instances as "GenericModule", Source (srcds) games included.
        if gen_ is False and entry.running and entry.module in ("Generic", "GenericModule"):
            generic_data: ScheduleData | ScheduleDataResponse = await entry.get_schedule_data(format_data=False)
            if not isinstance(generic_data, dict):
                raise AMPAPITypeError(end_point="Core/GetScheduleData", cur_type=generic_data, expec_type=dict)
            data = dict_merge(data, generic_data)
            gen_ = True
        # TODO: AMP 2.8 has no "srcds" module, so this never matches there.
        #       Drop it once we know no supported AMP version still sends it.
        if src_ is False and entry.running and entry.module == "srcds":
            srcds_data: ScheduleData | ScheduleDataResponse = await entry.get_schedule_data(format_data=False)
            if not isinstance(srcds_data, dict):
                raise AMPAPITypeError(end_point="Core/GetScheduleData", cur_type=srcds_data, expec_type=dict)
            data = dict_merge(data, srcds_data)
            src_ = True

    _temp: ScheduleData = ScheduleData(data=data)
    _trigger_event_parse(
        data=_temp.available_triggers,
        title="Trigger Events",
        title_body="",
        path="./docs/events/",
    )
    _method_event_parse(
        data=_temp.available_methods,
        title="Method Events",
        title_body="",
        path="./docs/events/",
    )


def repeat_to_length(string: str, repeat_char: str, length: int = 0) -> str:
    """Will repeat the passed in ``repeat_char`` by the ``len(string)`` provided or by the ``length`` parameter.

    .. note::
        By default the ``repeat_char`` will be one longer than the provided string unless you specify the ``length`` parameter.


    Parameters
    ----------
    string : str
        The string to match the :meth:`len` of.
    repeat_char : str
        The char to repeat to the length of the string or the ``length`` parameter.
    length : int, optional
        The length to repeat the char by, by default 0.

    Returns
    -------
    :class:`str`
        The modified ``repeat_char`` str by the ``length`` provided.

    """
    if length == 0:
        length = len(string) + 1
    return repeat_char * length


def str_sanitizer_sphinx(string: str, special_chars: tuple[str, ...]) -> str:
    """Sanitizes a string to prevent .rst typing errors.

    Parameters
    ----------
    string : :class:`str`
        The string with the special_char.
    special_chars : tuple[:class:`str`, ...]
        The characters that open a literal, which the next space closes.

    Returns
    -------
    :class:`str`
        The converted string for propery Sphinx documentation.

    """
    _temp = ""
    found_special: bool = False
    # for char in string:
    #     if found_special is False and char in special_chars:
    #         char = "``" + char
    #         found_special = True
    #         continue
    #     if found_special is True and char == " ":
    #         char = "``" + char
    #         found_special = False
    #     _temp += char
    for char in string:
        piece: str = char
        if found_special is False and char in special_chars:
            piece = "``" + char
            found_special = True
        elif found_special is True and char == " ":
            piece = "``" + char
            found_special = False
        _temp += piece
    # A literal still open at the end of the string gets closed, or Sphinx warns about it.
    if found_special is True:
        _temp += "``"
    return _temp
