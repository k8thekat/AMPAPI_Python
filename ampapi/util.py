from __future__ import annotations

import ast
import datetime
import json
import logging
import re
import traceback
from datetime import timezone
from json import JSONEncoder
from logging import Logger
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypedDict, Union

from dataclass_wizard import fromdict
from typing_extensions import Unpack

from docs.samples.method_event_usage import example_note

# from .base import Base
from .instance import AMPMinecraftInstance
from .modules import ActionResultError, BuildInfo, Diagnostics, ScheduleData
from .types_ import ScheduleDataData

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from io import TextIOWrapper

    from .controller import AMPADSInstance, AMPControllerInstance, AMPInstance
    from .modules import Diagnostics, Methods, SettingSpec, SettingsSpecParent, Triggers
    from .types_ import APISpec, PermissionNode, ScheduleDataData

LOGGER: logging.Logger = logging.getLogger(__name__)

# static strings for documentation
_instance_id_note = (
    """.. note::\n\tReplace ``instance-id`` with the something like the :py:class:`~Instance.instance_id` value.\n\n"""
)
_parent_node_note: str = (
    '.. note::\n\tAll nodes in this section will be prefixed with "%s.", see examples :ref:`Permission Nodes`\n\n'
)
_wildcard_nodes: str = """.. note::\n\tAny node with a '*' at the end of it is a wild card and using that will make all permissions nodes in that section equal to the value set, treat it like parent inheritance.\n\n"""

_trigger_note: str = """"""

_method_note: str = """"""

# Maps each API spec section name -> (python filename, method name prefix)
_SPEC_MODULE_MAP: dict[str, tuple[str, str]] = {
    "ads_module":               ("adsmodule.py",   ""),
    "analytics_plugin":         ("analytics.py",   ""),
    "core":                     ("core.py",         ""),
    "email_sender_plugin":      ("emailsender.py",  ""),
    "file_manager_plugin":      ("filemanager.py",  ""),
    "local_file_backup_plugin": ("filebackup.py",   ""),
    "minecraft_module":         ("minecraft.py",    "mc_"),
}

_METHOD_RE = re.compile(r"^\s+(?:async )?def (\w+)\s*\(")
_PYTHON_ONLY_PARAMS: frozenset[str] = frozenset({"format_data"})



def _method_event_parse(data: list[Methods], title: str = "", title_body: str = "", path: None | str = None) -> None:
    """Parses method event data and writes it to a .rst file.

    Parameters
    ----------
    data: list[:class:`Methods`]
        The list of dataclass Methods to parse.
    title: :class:`str`, optional
        The Title of the document header; used also as the filename, by default "".
    title_body: :class:`str`, optional
        The body text under the document header, by default "".
    path: :class:`None | str`, optional
        The path to save the .rst file, by default None.

    """
    file_name: str = title.lower().replace(" ", "_")
    _dir: Path = (
        Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
    )
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
            for entry in sorted(method.consumes):
                # print(entry, type(entry.enum_values), entry.enum_values)
                file.write(f"\t* {entry.name}: type({entry.value_type})\n")
                if isinstance(entry.enum_values, dict):
                    for key, value in sorted(entry.enum_values.items()):
                        file.write(f"\t\t* {key} - {value}\n")

    file.close()


async def _parse_get_api_spec_to_file(
    instance: Union[AMPControllerInstance, AMPADSInstance, AMPInstance, AMPMinecraftInstance], sanitize_json: bool,
) -> None:
    """|coro|

    Creates a Markdown file related to the type of :param:`instance` that is passed in to the function.
    .. note::
        See directory ``/docs/{Module_type}_api_spec.md``. where {Module_type} is the class ``.Module`` attribute.

    Parameters
    ----------
    instance : Union[Core, AMPControllerInstance, AMPInstance, AMPMinecraftInstance]
        The class of either :py:class:`Core:, :py:class:'AMPInstance`, :py:class:`AMPControllerInstance` and or :py:class:`AMPMinecraftInstance`.
    sanitize_json : bool
        Sanitize the JSON responses to meet PEP8 compliance. Default is False.

    """
    _logger: Logger = logging.getLogger(__name__)

    data: APISpec | ActionResultError = await instance.get_api_spec(sanitize_json=sanitize_json)
    diag_info: Diagnostics | ActionResultError = await instance.get_diagnostics_info()
    if isinstance(data, ActionResultError) or isinstance(diag_info, ActionResultError):
        _logger.error("Failed to retrieved proper data.| Data: %s | DiagInfo: %s", data, diag_info)
        return
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
    parents: list = []
    mode = "x"
    if _dir.exists():
        mode = "w"
    # TODO - turn these into .rst files instead.
    with Path.open(_dir, mode) as file:
        file.write(f"INSTANCE TYPE: {instance_type}\n")
        file.write(f"APP VERSION: {diag_info.application_version}\n")
        file.write(f"BUILD: {diag_info.build_date}\n\n")

        for parent, parent_value in sorted(data.items()):
            if parent not in parents:
                parents.append(parent)
                file.write("____________________________________________________\n")
                file.write(f"{parent}:\n")
            if isinstance(parent_value, dict):
                for child, child_value in sorted(parent_value.items()):
                    file.write(f"\t{child}:\n")
                    if isinstance(child_value, dict):
                        for key, value in sorted(child_value.items()):
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
        The instance type identifier matching the filename (e.g. ``"ADS"`` or ``"Minecraft"``).
    base_path : Path | None, optional
        Root of the ``api_spec_sheets`` directory. Defaults to ``../docs/api_spec_sheets`` relative to this file.
    output_path : Path | None, optional
        Full path for the output diff file. Defaults to ``{base_path}/diffs/{instance_type}_{version_a}_to_{version_b}.md``.

    """
    _logger: Logger = logging.getLogger(__name__)

    _base: Path = base_path if base_path is not None else Path(__file__).parent.parent.joinpath("docs/api_spec_sheets")

    file_a = _base / version_a / f"{instance_type}_api_spec.md"
    file_b = _base / version_b / f"{instance_type}_api_spec.md"

    print("file_a path", file_a)
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

    _out: Path = (
        output_path
        if output_path is not None
        else _base / "diffs" / f"{instance_type}_{version_a}_to_{version_b}.md"
    )
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
                if val_a != val_b:
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

def _get_implemented_methods(filepath: Path) -> set[str]:
    """Return the set of method names defined in a Python source file.

    Parameters
    ----------
    filepath: :class:`Path`
        The path to the Python source file to parse.

    Returns
    -------
    set[:class:`str`]
        The set of method names found in the file.

    """
    methods: set[str] = set()
    with filepath.open() as file:
        for line in file:
            match = _METHOD_RE.match(line)
            if match:
                methods.add(match.group(1))
    return methods


def _get_function_signatures(filepath: Path) -> dict[str, list[str]]:
    """Return all method signatures from a Python source file.

    Parameters
    ----------
    filepath: :class:`Path`
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
    suffix_aliases: list[str] | None = None,
) -> None:
    """Compare all API spec sheets against their Python implementations and report missing endpoints.

    Merges endpoints across all ``*_api_spec.md`` files found in ``spec_path``, then checks each
    spec section against the corresponding Python module file using :data:`_SPEC_MODULE_MAP`.
    Results are written to a Markdown file and summarised via logging.

    Parameters
    ----------
    spec_path : Path | None, optional
        Directory containing ``*_api_spec.md`` files. Defaults to ``../docs/api_spec_sheets`` relative to this file.
    ampapi_path : Path | None, optional
        Directory containing the Python module files. Defaults to the directory of this file.
    output_path : Path | None, optional
        Path for the output report. Defaults to ``{spec_path}/missing_endpoints.md``.
    suffix_aliases : list[str] | None, optional
        Additional suffixes to try when an exact match is not found. An endpoint is considered
        implemented if ``prefix + endpoint + suffix`` exists for any suffix in the list.
        Defaults to ``["_application"]`` to handle spec names like ``kill`` mapping to ``kill_application``.

    """
    _logger: Logger = logging.getLogger(__name__)
    _spec_dir: Path = spec_path if spec_path is not None else Path(__file__).parent.parent.joinpath("docs/api_spec_sheets")
    _ampapi_dir: Path = ampapi_path if ampapi_path is not None else Path(__file__).parent
    _aliases: list[str] = suffix_aliases if suffix_aliases is not None else ["_application"]

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

    def _is_implemented(ep: str, prefix: str, py_methods: set[str]) -> bool:
        full = prefix + ep
        if full in py_methods:
            return True
        return any((full + alias) in py_methods for alias in _aliases)

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

            py_methods = _get_implemented_methods(py_path)
            missing = sorted(ep for ep in spec_endpoints if not _is_implemented(ep, prefix, py_methods))
            total_missing += len(missing)

            out_file.write(f"## {section} -> [{py_file}](ampapi/{py_file})\n\n")
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
    suffix_aliases: list[str] | None = None,
) -> None:
    """Compare implemented Python method parameters against their API spec definitions and report mismatches.

    For each endpoint that exists in both the spec sheets and the Python implementation, compares
    the parameter names from the spec (converted to snake_case via :meth:`Base.camel_to_snake_re`)
    against the actual Python function signature. Python-only parameters (e.g. ``format_data``)
    defined in :data:`_PYTHON_ONLY_PARAMS` are excluded from the comparison. Results are written
    to a Markdown file and summarised via logging.

    Parameters
    ----------
    spec_path : Path | None, optional
        Directory containing ``*_api_spec.md`` files. Defaults to ``../docs/api_spec_sheets`` relative to this file.
    ampapi_path : Path | None, optional
        Directory containing the Python module files. Defaults to the directory of this file.
    output_path : Path | None, optional
        Path for the output report. Defaults to ``{spec_path}/parameter_mismatches.md``.
    suffix_aliases : list[str] | None, optional
        Additional suffixes to try when resolving a spec endpoint name to a Python method name.
        Defaults to ``["_application"]``.

    """
    _logger: Logger = logging.getLogger(__name__)
    _spec_dir: Path = spec_path if spec_path is not None else Path(__file__).parent.parent.joinpath("docs/api_spec_sheets")
    _ampapi_dir: Path = ampapi_path if ampapi_path is not None else Path(__file__).parent
    _aliases: list[str] = suffix_aliases if suffix_aliases is not None else ["_application"]

    # Merge spec endpoints from all versioned spec files; first file seen wins per key.
    all_spec: dict[str, dict[str, str]] = {}
    for spec_file in sorted(_spec_dir.glob("**/*_api_spec.md")):
        for key, fields in _parse_api_spec_file(spec_file).items():
            all_spec.setdefault(key, fields)

    _out: Path = output_path if output_path is not None else _spec_dir / "parameter_mismatches.md"

    total_mismatches = 0
    with _out.open("w") as out_file:
        out_file.write("# Parameter Mismatches\n\n")

        for section, (py_file, prefix) in sorted(_SPEC_MODULE_MAP.items()):
            py_path = _ampapi_dir / py_file
            if not py_path.exists():
                _logger.warning("Python file not found for section '%s': %s", section, py_path)
                continue

            signatures = _get_function_signatures(py_path)
            section_mismatches: list[str] = []

            for key, fields in sorted(all_spec.items()):
                parent, _, endpoint = key.partition(".")
                if parent != section:
                    continue

                # Resolve the Python method name, accounting for suffix aliases.
                full = prefix + endpoint
                py_method: str | None = None
                if full in signatures:
                    py_method = full
                else:
                    for alias in _aliases:
                        if (full + alias) in signatures:
                            py_method = full + alias
                            break
                if py_method is None:
                    continue  # unimplemented endpoint; covered by find_missing_endpoints

                py_params: set[str] = set(signatures[py_method]) - _PYTHON_ONLY_PARAMS

                raw_params_str = fields.get("parameters", "[]")
                try:
                    spec_param_list: list[dict[str, Any]] = ast.literal_eval(raw_params_str)
                except (ValueError, SyntaxError):
                    _logger.warning("Could not parse parameters for %s: %s", key, raw_params_str)
                    continue

                spec_params: set[str] = {Base.camel_to_snake_re(p["name"]) for p in spec_param_list}

                missing_in_python = sorted(spec_params - py_params)
                extra_in_python = sorted(py_params - spec_params)

                if missing_in_python or extra_in_python:
                    total_mismatches += 1
                    section_mismatches.append(f"### `{key}`\n\n")
                    if missing_in_python:
                        section_mismatches.append("**In spec, missing from Python:**\n")
                        section_mismatches.extend(f"- `{p}`\n" for p in missing_in_python)
                        section_mismatches.append("\n")
                    if extra_in_python:
                        section_mismatches.append("**In Python, not in spec:**\n")
                        section_mismatches.extend(f"- `{p}`\n" for p in extra_in_python)
                        section_mismatches.append("\n")

            out_file.write(f"## {section} -> [{py_file}](ampapi/{py_file})\n\n")
            if section_mismatches:
                out_file.writelines(section_mismatches)
            else:
                out_file.write("_No parameter mismatches._\n")
            out_file.write("\n")

    _logger.info(
        "Parameter mismatch report written to %s | Total endpoints with mismatches: %d", _out, total_mismatches,
    )


def _permission_node_parse(
    data: list[PermissionNode],
    title: str = "",
    title_body: str = "",
    index: int = 0,
    path: str | None = None,
    file: Union[TextIOWrapper, None] = None,
) -> None:
    from docs.samples.permission_node_usage import example_note

    index = index
    used_keys: list[Any] = []

    file_name: str = title.lower().replace(" ", "_")
    _dir: Path = (
        Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
    )
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
        if isinstance(entry, dict) and entry["name"] not in used_keys and index == 0:
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
                        new_child: list[PermissionNode] | PermissionNode = children.get("children", [])
                        if len(new_child) > 0:
                            new_child = new_child[0]
                            for node in sorted(new_child["children"], key=lambda x: x["name"]):
                                # Handles formatting our nodes
                                file.write(f"- Instances.`instance-id`.{node['name']}\n")

                continue
            # Our notes about the prefix characters.
            file.write(_parent_node_note % entry["name"] + "\n")
            # Handles formatting our nodes
            file.write(f"- {temp[-1]}.*\n")
        if isinstance(entry, dict) and entry["name"] not in used_keys and index == 1:
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
                entry["children"], list,
            ):
                file.write(f"- {temp[-1]}.*\n")
                for node in sorted(entry["children"], key=lambda x: x["name"]):
                    file.write(f"- {temp[-1]}.{node['name']}\n")
                continue
            # Our notes about the prefix characters with the passed in var post %.
            file.write(_parent_node_note % entry["name"] + "\n")

            # Handles formatting our nodes
            file.write(f"- {temp[-1]}.*\n")
        if isinstance(entry, dict) and entry["name"] not in used_keys and index == 2:
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
    path: None | str = None,
    file: Union[TextIOWrapper, None] = None,
) -> None:
    from docs.samples.settings_node_usage import example_note

    index = index

    file_name: str = title.lower().replace(" ", "_")
    _dir: Path = (
        Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
    )
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

    for key in sorted(vars(data)):
        # Our second headers.
        header: str = "Settings " + key.title() + " Nodes"
        # file.write("\n:raw-html:`<hr>`\n")
        file.write(f"\n{header}\n")
        file.write(f"{repeat_to_length(string=header, repeat_char='#')}\n")
        file.write(":raw-html:`<hr>`\n\n")

        data_key: list[SettingSpec] = getattr(data, key)
        if isinstance(data_key, list):
            for entry in sorted(data_key):
                file.write(f"\n**Name**: {entry.name}\n")
                if entry.description is not None and len(entry.description) > 0:
                    file.write(f"\t| Description: {str_sanitizer_sphinx(string=entry.description, special_chars=('*',))}\n")
                file.write(f"\t| Node: `{entry.node}`\n")
    file.close()


def _trigger_event_parse(
    data: list[Triggers],
    title: str = "",
    title_body: str = "",
    path: None | str = None,
) -> None:
    """This assumes you have acquired the ScheduleData already and are passing in :attr:`~scheduleData.available_triggers`

    .. note::
        All of these triggers will have a unique ID field that is generated from :meth:`~Core.get_triggers` due to uniqueness.


    Parameters
    ----------
    data: list[:class:`Triggers`]
        The list of dataclass Triggers.
    title: :class:`str`, optional
        The Title of the document header; this is also used to set the filename, by default "".
    title_body: :class:`str`, optional
        The body just under the document header, by default "".
    path: :class:`None | str`, optional
        The path to save the .rst file., by default None.

    """
    from docs.samples.trigger_event_usage import example_note

    file_name: str = title.lower().replace(" ", "_")
    _dir: Path = (
        Path(__file__).parent.joinpath(f"{file_name}.rst") if path is None else Path(path).joinpath(f"{file_name}.rst")
    )
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


async def amp_api_update(instance: AMPControllerInstance, sanitize_json: bool) -> None:
    """|coro|

    Gets the AMP Instance API Endpoints and writes them out to a file. Used for version changes.

    .. note::
        Having a ``Minecraft`` type Instance is beneficial for this call. Otherwise you will only get the ADS/Controller API spec sheet.


    Parameters
    ----------
    instance : AMPControllerInstance
        Must be the Controller instance; as we are looking for the ADS and a Minecraft Instance.
    sanitize_json : bool
        Sanitize the JSON responses to meet PEP8 compliance.

    """
    _logger: Logger = logging.getLogger(__name__)
    # We call get_instances() to force a current listing of instances to be populated.
    await instance.get_instances()
    ADS_diag: Diagnostics | ActionResultError = await instance.get_diagnostics_info()
    if isinstance(ADS_diag, ActionResultError):
        _logger.error("Failed to retrieved proper Diag Info. | DiagInfo: %s", ADS_diag)
        return
    # cur_version: None | AMPMinecraftInstance = None
    for entry in instance.instances:
        # Minecraft instances have their own unique API endpoints; so we need to get those.
        if entry.module == "Minecraft" and isinstance(entry, AMPMinecraftInstance) and entry.running is True:
            instance_diag: Diagnostics | ActionResultError = await entry.get_diagnostics_info()
            if isinstance(instance_diag, ActionResultError):
                _logger.error("Failed to retrieved proper Diag Info. | DiagInfo: %s", ADS_diag)
                return
            if instance_diag.application_version == ADS_diag.application_version:
                _logger.info(
                    "Found %s matching the current ADS version `%s` .", entry.instance_name, ADS_diag.application_version,
                )
                await _parse_get_api_spec_to_file(instance=entry, sanitize_json=sanitize_json)
                break
    # We found our Minecraft Instance, now lets parse our Controller/ADS
    await _parse_get_api_spec_to_file(instance=instance, sanitize_json=sanitize_json)


def dict_merge(dict1: ScheduleDataData, dict2: ScheduleDataData) -> ScheduleDataData:
    """Merges dict2 into dict1 with key overlapp but combining data instead of replacing key data.

    .. note::
        This was made for :class:`ScheduleDataData` specifically to merge the list of :class:`MethodsData` and :class:`TriggersData` under the same key.


    Parameters
    ----------
    dict1: :class:`ScheduleDataData`
        The origin dict.
    dict2: :class:`ScheduleDataData`
        The dict to merge keys from.

    Returns
    -------
    :class:`ScheduleDataData`
        Merged dictionary.

    """
    # _temp: defaultdict[str, list[MethodsData | TriggersData]] = defaultdict(list)
    for key, value in dict2.items():
        dict1[key].extend(value)
    return dict1  # type: ignore



async def generate_docs_rst(instance: AMPControllerInstance) -> None:
    """|coro|

    This will generate the Sphinx ``.rst`` files we use for documentation. The files will be written to ``../docs/nodes/``

    .. warning::
        There may be a few errors due to the formatting of AMPs return information; so it is wrapped in ``try/excepts``


    Parameters
    ----------
    instance: AMPControllerInstance | AMPADSInstance
        Must be of these types as the API endpoint :meth:`get_settingspec` is not available to all.

    """
    logger: Logger = logging.getLogger(__name__)
    spec: SettingsSpecParent | ActionResultError = await instance.get_setting_spec()
    if isinstance(spec, ActionResultError):
        logger.error("Failed to retrieve Spec Data. | Spec: %s", spec)
        return

    _path: Path = Path(__file__).parent.joinpath("../docs/nodes")

    logger.info("Generating Settings Node.rst...")
    # As far as I know settings spec information is the same for all instances
    try:
        _settings_node_parse(data=spec, title="Setting Nodes", title_body="", path=_path.as_posix())
    except Exception:
        logger.error("Ran into a <Exception> when attempting to generate the Setting Nodes.rst.\n %s", traceback.print_exc())
    # As far as I know Permission spec information is the same for all instances
    perms: list[PermissionNode] | ActionResultError = await instance.get_permissions_spec()
    if isinstance(perms, ActionResultError):
        logger.error("Failed to retrieved proper Perms Info. | Perms: %s", perms)
        return
    logger.info("Generating Permission Nodes.rst...")
    try:
        _permission_node_parse(data=perms, title="Permission Nodes", title_body="", path=_path.as_posix())
    except Exception:
        logger.error(
            "Ran into a <Exception> when attempting to generate the Permission Nodes.rst.\n %s", traceback.print_exc(),
        )

    logger.info("Generating Triggers Events.rst and Method Events.rst...")
    await instance.get_instances()
    # data: ScheduleData = await instance.get_schedule_data(format_data=True)
    data: ScheduleDataData | ActionResultError = await instance.get_schedule_data(format_data=False)
    if isinstance(data, ActionResultError):
        logger.error("Failed to retrieved proper Scheduled Data. | Scheduled Data: %s", data)
        return
    mc_: bool = False
    gen_: bool = False
    src_: bool = False
    for entry in instance.instances:
        # print(entry.running, entry.friendly_name, entry.module)
        if mc_ is False and entry.running and entry.module == "Minecraft":
            mc_data: ScheduleDataData | ActionResultError = await entry.get_schedule_data(format_data=False)
            if isinstance(mc_data, ActionResultError):
                logger.error("Failed to retrieved proper Scheduled Data. | Scheduled Data: %s", mc_data)
                return
            data = dict_merge(data, mc_data)
            mc_ = True
        if gen_ is False and entry.running and entry.module == "Generic":
            generic_data: ScheduleDataData | ActionResultError = await entry.get_schedule_data(format_data=False)
            if isinstance(generic_data, ActionResultError):
                logger.error("Failed to retrieved proper Scheduled Data. | Scheduled Data: %s", generic_data)
                return
            data = dict_merge(data, generic_data)
            gen_ = True
        if src_ is False and entry.running and entry.module == "srcds":
            srcds_data: ScheduleDataData | ActionResultError = await entry.get_schedule_data(format_data=False)
            if isinstance(srcds_data, ActionResultError):
                logger.error("Failed to retrieved proper Scheduled Data. | Scheduled Data: %s", srcds_data)
                return
            data = dict_merge(data, srcds_data)
            src_ = True

    _temp: ScheduleData = fromdict(ScheduleData, data)  # type: ignore
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
    string: str
        The string to match the :meth:`len` of.
    repeat_char: str
        The char to repeat to the length of the string or the ``length`` parameter.
    length: int, optional
        The length to repeat the char by, by default 0.

    Returns
    -------
    :class:`str`
        The modified ``repeat_char`` str by the ``length`` provided.

    """
    if length == 0:
        length = len(string) + 1
    return repeat_char * length


def str_sanitizer_sphinx(string: str, special_chars: tuple) -> str:
    """Sanitizes a string to prevent .rst typing errors.

    Parameters
    ----------
    string: :class:`str`
        The string with the special_char.

    Returns
    -------
    :class:`str`
        The converted string for propery Sphinx documentation.

    """
    _temp = ""
    found_special: bool = False
    for char in string:
        if found_special is False and char in special_chars:
            char = "``" + char
            found_special = True
            continue
        if found_special is True and char == " ":
            char = "``" + char
            found_special = False
        _temp += char
    return _temp
