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
import collections
import json
import logging
import re
import types
import typing
from pathlib import Path
from typing import TYPE_CHECKING, Any, NotRequired, Required, TypeGuard, Union

from . import _types

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from ._types import KeyDrift

__all__ = ("KeyDriftCheck", "declared_keys", "key_drift")

LOGGER: logging.Logger = logging.getLogger(__name__)

# Matches a `url=` literal such as "Core/GetStatus", with or without a leading "API/"
_ENDPOINT_URL_PATTERN = re.compile(r"^(?:API/)?([A-Za-z]+/[A-Za-z0-9]+)$")
# These are what a wrapper narrows its response with, and the second argument is the TypedDict
_NARROWING_CALLS = ("is_response_type", "is_response_list")


def _is_json_object(value: object) -> TypeGuard[Mapping[str, object]]:
    """If `value` is a decoded JSON object."""
    return isinstance(value, dict)


def _is_json_array(value: object) -> TypeGuard[list[object]]:
    """If `value` is a decoded JSON array."""
    return isinstance(value, list)


def _unwrap(hint: Any) -> tuple[Any, Union[bool, None]]:
    """Take `NotRequired` / `Required` off a hint and say which one it was, None for neither."""
    origin = typing.get_origin(hint)
    if origin is NotRequired:
        return typing.get_args(hint)[0], False
    if origin is Required:
        return typing.get_args(hint)[0], True
    return hint, None


def _nested_shape(hint: Any) -> Union[tuple[type, bool], None]:
    """Get the TypedDict a hint holds, directly or in a list, and if it is a list."""
    origin = typing.get_origin(hint)
    # Union[X, None] and X | None
    if origin is Union or origin is types.UnionType:
        for argument in typing.get_args(hint):
            if argument is not type(None):
                return _nested_shape(argument)
        return None

    if origin is list:
        arguments = typing.get_args(hint)
        if arguments and typing.is_typeddict(arguments[0]):
            return arguments[0], True
        return None

    if typing.is_typeddict(hint):
        return hint, False
    return None


def declared_keys(shape: type) -> dict[str, tuple[object, bool]]:
    """Each key a TypedDict declares, with its hint and whether a payload must carry it.

    The annotations are read with `typing.get_type_hints()`, as `__optional_keys__` is empty under
    `from __future__ import annotations`.

    Parameters
    ----------
    shape : :class:`type`
        A TypedDict.

    Returns
    -------
    dict[:class:`str`, tuple[:class:`object`, :class:`bool`]]
        The key, then its hint with any `NotRequired` / `Required` taken off and if the key is required.

    """
    declared: dict[str, tuple[object, bool]] = {}
    for key, hint in typing.get_type_hints(shape, include_extras=True).items():
        inner, is_required = _unwrap(hint)
        declared[key] = (inner, is_required is True or (is_required is None and getattr(shape, "__total__", True) is True))
    return declared


def _count(
    shape: type,
    payloads: Iterable[Mapping[str, object]],
    path: str,
    missing: collections.Counter[str],
    unexpected: collections.Counter[str],
) -> None:
    declared: dict[str, tuple[object, bool]] = declared_keys(shape)
    required: set[str] = {key for key, (_hint, is_required) in declared.items() if is_required}
    nested: dict[str, tuple[type, bool]] = {}
    for key, (hint, _is_required) in declared.items():
        found = _nested_shape(hint)
        if found is not None:
            nested[key] = found

    children: dict[str, list[Mapping[str, object]]] = collections.defaultdict(list)
    for payload in payloads:
        for key in required - payload.keys():
            missing[path + key] += 1
        for key in payload.keys() - declared.keys():
            unexpected[path + key] += 1
        for key, (_child_shape, is_list) in nested.items():
            value = payload.get(key)
            if is_list is True and _is_json_array(value):
                children[key].extend(item for item in value if _is_json_object(item))
            elif is_list is False and _is_json_object(value):
                children[key].append(value)

    for key, (child_shape, _is_list) in nested.items():
        if children[key]:
            _count(child_shape, children[key], f"{path}{key}.", missing, unexpected)


def key_drift(shape: type, payloads: Iterable[Mapping[str, object]]) -> KeyDrift:
    """How `payloads` differ from `shape`: required keys some lack, and keys it does not declare.

    A key typed as another TypedDict, or a list of one, is compared too, under a dotted path (`metrics.tps`).

    Parameters
    ----------
    shape : :class:`type`
        A TypedDict, read with `typing.get_type_hints()`.
    payloads : Iterable[Mapping[:class:`str`, :class:`object`]]
        The captured payloads, each a decoded and sanitized JSON object.

    Returns
    -------
    :class:`KeyDrift`
        Each key and how many payloads it differed in, both empty when the capture matches.

    """
    missing: collections.Counter[str] = collections.Counter()
    unexpected: collections.Counter[str] = collections.Counter()
    _count(shape, [payload for payload in payloads if _is_json_object(payload)], "", missing, unexpected)
    return {"missing": dict(sorted(missing.items())), "unexpected": dict(sorted(unexpected.items()))}


def _annotation_names(node: Union[ast.expr, None]) -> list[str]:
    """Get every plain name in an annotation, eg. `list[Backup]` gives Backup."""
    if node is None:
        return []
    return [child.id for child in ast.walk(node) if isinstance(child, ast.Name)]


class KeyDriftCheck:
    """Compare AMP responses with the TypedDict each endpoint narrows to, to notice AMP changing its keys.

    A dev tool. :meth:`Base._response_handler` uses one when called with ``check_key_drift=True`` and
    ``to_file=True``. :meth:`check_directory` runs over captures already saved to disk.

    .. code-block:: python

        checker = KeyDriftCheck()                     # reads the wrappers once
        checker.shapes["Core/GetStatus"]              # (StatusResponse,)
        checker.check("Core/GetStatus", data)         # (StatusResponse, KeyDrift), or None
        checker.check_directory(Path("_responses"))   # writes _responses/key_drift.md


    Attributes
    ----------
    shapes : dict[:class:`str`, tuple[:class:`type`, ...]]
        Each endpoint URL (eg. `Core/GetStatus`) and the TypedDicts its response is expected to match.

    """

    __slots__ = ("shapes",)

    def __init__(self, package: Union[Path, None] = None) -> None:
        """Read the endpoint shapes from the wrapper source.

        Parameters
        ----------
        package : Union[:class:`Path`, None], optional
            The directory holding the wrapper modules, by default None, which is this package.

        """
        self.shapes: dict[str, tuple[type, ...]] = self._read_shapes(package if package is not None else Path(__file__).parent)

    @staticmethod
    def _read_shapes(package: Path) -> dict[str, tuple[type, ...]]:
        """Read the TypedDicts each endpoint's response should match from the wrapper source.

        A wrapper's shape is the TypedDict it narrows to with `is_response_type()` / `is_response_list()`,
        or the ones named in its return annotation. An endpoint with no TypedDict is left out.

        """
        shapes: dict[str, set[type]] = collections.defaultdict(set)
        for source in sorted(package.glob("*.py")):
            tree = ast.parse(source.read_text())
            for function in ast.walk(tree):
                if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue

                urls: set[str] = set()
                narrowed: list[str] = []
                for node in ast.walk(function):
                    if not isinstance(node, ast.Call):
                        continue
                    for keyword in node.keywords:
                        if keyword.arg == "url" and isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
                            match = _ENDPOINT_URL_PATTERN.match(keyword.value.value)
                            if match:
                                urls.add(match.group(1))

                    if isinstance(node.func, ast.Name) and node.func.id in _NARROWING_CALLS and len(node.args) > 1:
                        narrowed.extend(_annotation_names(node.args[1]))

                # Skip a method with more than one URL, as we can't tell which shape is whose
                if len(urls) != 1:
                    continue

                url: str = next(iter(urls))
                for name in narrowed or _annotation_names(function.returns):
                    shape: object = getattr(_types, name, None)
                    if isinstance(shape, type) and typing.is_typeddict(shape):
                        shapes[url].add(shape)

        return {url: tuple(sorted(found, key=lambda shape: shape.__name__)) for url, found in sorted(shapes.items())}

    def check(self, endpoint: str, data: object) -> Union[tuple[type, KeyDrift], None]:
        """Compare one sanitized endpoint response with the TypedDict it is expected to match.

        Parameters
        ----------
        endpoint : :class:`str`
            The endpoint URL, eg. `Core/GetStatus`.
        data : :class:`object`
            The sanitized JSON response. A list compares each of its objects.

        Returns
        -------
        Union[tuple[:class:`type`, :class:`KeyDrift`], None]
            The TypedDict that matched best and how the response differs from it, or None when the endpoint has
            no known shape or the response holds no JSON object. When an endpoint has several shapes, the one
            with the fewest differing keys is used.

        """
        shapes: tuple[type, ...] = self.shapes.get(endpoint, ())
        if _is_json_array(data):
            payloads: list[Mapping[str, object]] = [item for item in data if _is_json_object(item)]
        else:
            payloads = [data] if _is_json_object(data) else []

        if not shapes or not payloads:
            return None
        results: list[tuple[type, KeyDrift]] = [(shape, key_drift(shape, payloads)) for shape in shapes]
        return min(results, key=lambda result: len(result[1]["missing"]) + len(result[1]["unexpected"]))

    def check_directory(self, path: Path, report: Union[Path, None] = None) -> dict[str, tuple[str, type, KeyDrift]]:
        """Compare every capture under `path` with its endpoint's TypedDict and write a Markdown report.

        A capture is matched to its endpoint by file name, the way `to_file` names it (`getstatus.json` is
        `Core/GetStatus`). Error captures (a JSON object with a `title`) and `*.key_drift.json` files are skipped.
        Empty captures (`[]` or `null`) are listed apart. "No known shape" means the endpoint's wrapper names
        no TypedDict, or the file is not named after an endpoint.

        Parameters
        ----------
        path : :class:`Path`
            The directory of captures, searched recursively.
        report : Union[:class:`Path`, None], optional
            Where to write the report, by default None, which is `key_drift.md` inside `path`.

        Returns
        -------
        dict[:class:`str`, tuple[:class:`str`, :class:`type`, :class:`KeyDrift`]]
            Each drifted capture (relative to `path`), with its endpoint, TypedDict and drift.

        """
        by_name: dict[str, list[str]] = collections.defaultdict(list)
        for endpoint in self.shapes:
            by_name[endpoint.rsplit("/", 1)[1].lower()].append(endpoint)

        drifted: dict[str, tuple[str, type, KeyDrift]] = {}
        unmatched: list[str] = []
        empty: list[str] = []
        checked = 0
        for capture in sorted(path.rglob("*.json")):
            if capture.name.endswith(".key_drift.json"):
                continue
            name: str = capture.relative_to(path).as_posix()
            data: object = json.loads(capture.read_text())
            if _is_json_object(data) and "title" in data:
                continue

            # Empty lists and null have no keys
            if data is None or data == []:
                empty.append(name)
                continue

            # The same endpoint can be in two modules, so we keep the best match
            results = [(endpoint, found) for endpoint in by_name.get(capture.stem.lower(), []) if (found := self.check(endpoint, data))]
            if not results:
                unmatched.append(name)
                continue

            checked += 1
            endpoint, (shape, drift) = min(results, key=lambda result: len(result[1][1]["missing"]) + len(result[1][1]["unexpected"]))
            if drift["missing"] or drift["unexpected"]:
                drifted[name] = (endpoint, shape, drift)

        report_path: Path = report if report is not None else path / "key_drift.md"
        with report_path.open("w") as file:
            file.write("# Key Drift Report\n\n")
            file.write(f"- Captures checked : {checked}\n- Drifted          : {len(drifted)}\n")
            file.write(f"- Empty            : {len(empty)}\n- No known shape   : {len(unmatched)}\n\n")
            for name, (endpoint, shape, drift) in drifted.items():
                file.write(f"## {name} -> `{endpoint}` (`{shape.__name__}`)\n\n")
                for label, keys in (("Missing", drift["missing"]), ("Unexpected", drift["unexpected"])):
                    if keys:
                        file.write(f"- {label}: " + ", ".join(f"`{key}` ({count})" for key, count in keys.items()) + "\n")
                file.write("\n")

            if empty:
                file.write("## Empty\n\n" + "".join(f"- `{name}`\n" for name in empty) + "\n")
            if unmatched:
                file.write("## No known shape\n\n" + "".join(f"- `{name}`\n" for name in unmatched))
        LOGGER.info("Key drift report written to %s | Checked: %d | Drifted: %d", report_path, checked, len(drifted))
        return drifted
