#!/usr/bin/env python3
"""Scan Python classes for attributes and insert a NumPy-style Attributes section.

Usage:
    docstring_attrs.py file.py                 # preview a unified diff
    docstring_attrs.py file.py --write          # apply in place
    docstring_attrs.py file.py --class Foo      # only touch class Foo
    docstring_attrs.py file.py --line 42 --write  # only touch the class enclosing line 42
    docstring_attrs.py file.py --include-private  # also list _private attributes
"""

from __future__ import annotations

import argparse
import ast
import difflib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

NUMPY_SECTION_ORDER = [
    "Parameters",
    "Attributes",
    "Methods",
    "Returns",
    "Yields",
    "Raises",
    "See Also",
    "Notes",
    "References",
    "Examples",
]
SECTIONS_AFTER_ATTRIBUTES = set(
    NUMPY_SECTION_ORDER[NUMPY_SECTION_ORDER.index("Attributes") + 1 :]
)
UNDERLINE_RE = re.compile(r"^-{3,}\s*$")


@dataclass
class Attribute:
    name: str
    type_hint: str | None


def infer_type(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant):
        if node.value is None:
            return None
        return type(node.value).__name__
    if isinstance(node, (ast.List, ast.ListComp)):
        return "list"
    if isinstance(node, (ast.Dict, ast.DictComp)):
        return "dict"
    if isinstance(node, (ast.Set, ast.SetComp)):
        return "set"
    if isinstance(node, ast.Tuple):
        return "tuple"
    if isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            return func.attr
    return None


def collect_attributes(cls: ast.ClassDef, include_private: bool = False) -> list[Attribute]:
    attrs: dict[str, Attribute] = {}

    for stmt in cls.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            attrs[stmt.target.id] = Attribute(stmt.target.id, ast.unparse(stmt.annotation))
        elif isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    attrs.setdefault(target.id, Attribute(target.id, infer_type(stmt.value)))

    for stmt in cls.body:
        if not isinstance(stmt, ast.FunctionDef):
            continue
        for node in ast.walk(stmt):
            target = None
            annotation = None
            value = None
            if isinstance(node, ast.AnnAssign):
                target, annotation = node.target, node.annotation
            elif isinstance(node, ast.Assign) and len(node.targets) == 1:
                target, value = node.targets[0], node.value

            if not (
                isinstance(target, ast.Attribute)
                and isinstance(target.value, ast.Name)
                and target.value.id == "self"
            ):
                continue

            if annotation is not None:
                attrs[target.attr] = Attribute(target.attr, ast.unparse(annotation))
            else:
                existing = attrs.get(target.attr)
                inferred = infer_type(value) if value is not None else None
                if existing is None or (existing.type_hint is None and inferred):
                    attrs[target.attr] = Attribute(target.attr, inferred)

    if not include_private:
        attrs = {name: attr for name, attr in attrs.items() if not name.startswith("_")}

    return sorted(attrs.values(), key=lambda a: a.name)


def build_attributes_block(attrs: list[Attribute], indent: str) -> list[str]:
    lines = [f"{indent}Attributes", f"{indent}----------"]
    for attr in attrs:
        lines.append(f"{indent}{attr.name} : {attr.type_hint or 'TYPE'}")
        lines.append(f"{indent}    DESCRIPTION.")
    return lines


def find_section_headers(lines: list[str]) -> list[tuple[int, str]]:
    """Return (line_index, header_name) for each numpydoc section header."""
    headers = []
    for i in range(len(lines) - 1):
        line, underline = lines[i], lines[i + 1]
        stripped = line.strip()
        if stripped and UNDERLINE_RE.match(underline.strip()):
            headers.append((i, stripped))
    return headers


def replace_or_insert_section(body: str, indent: str, new_block: list[str]) -> str:
    lines = body.splitlines()
    headers = find_section_headers(lines)

    attr_span = None
    insert_before = None
    for idx, (line_idx, name) in enumerate(headers):
        if name == "Attributes":
            end = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
            while end > line_idx and not lines[end - 1].strip():
                end -= 1
            attr_span = (line_idx, end)
        elif insert_before is None and name in SECTIONS_AFTER_ATTRIBUTES:
            insert_before = line_idx

    if attr_span is not None:
        start, end = attr_span
        lines[start:end] = new_block
    else:
        pos = insert_before if insert_before is not None else len(lines)
        while pos > 0 and not lines[pos - 1].strip():
            pos -= 1
        prefix_needs_blank = pos > 0 and lines[pos - 1].strip() != ""
        suffix_needs_blank = pos >= len(lines) or lines[pos].strip() != ""
        insertion = (
            ([""] if prefix_needs_blank else [])
            + new_block
            + ([""] if suffix_needs_blank else [])
        )
        lines[pos:pos] = insertion

    return "\n".join(lines)


def process_class(source: str, cls: ast.ClassDef, include_private: bool = False) -> str | None:
    attrs = collect_attributes(cls, include_private=include_private)
    if not attrs:
        return None

    indent = " " * (cls.body[0].col_offset if cls.body else cls.col_offset + 4)
    new_block = build_attributes_block(attrs, indent)

    first_stmt = cls.body[0]
    has_docstring = (
        isinstance(first_stmt, ast.Expr)
        and isinstance(getattr(first_stmt, "value", None), ast.Constant)
        and isinstance(first_stmt.value.value, str)
    )

    lines = source.splitlines(keepends=True)

    if has_docstring:
        doc_node = first_stmt.value
        old_text = ast.get_source_segment(source, doc_node)
        quote = old_text[:3] if old_text[:3] in ('"""', "'''") else old_text[0]
        body = old_text[len(quote): -len(quote)]
        new_body = replace_or_insert_section(body, indent, new_block)
        new_text = f"{quote}{new_body}{quote}"

        start_line, start_col = doc_node.lineno - 1, doc_node.col_offset
        end_line, end_col = doc_node.end_lineno - 1, doc_node.end_col_offset

        before = "".join(lines[:start_line]) + lines[start_line][:start_col]
        after = lines[end_line][end_col:] + "".join(lines[end_line + 1 :])
        return before + new_text + after

    body_indent = indent
    doc_lines = [
        f'{body_indent}"""Summary line.\n\n',
        *(f"{body_indent}{l}\n" for l in build_attributes_block(attrs, "")),
        f'{body_indent}"""\n\n',
    ]
    insert_at = first_stmt.lineno - 1
    return "".join(lines[:insert_at]) + "".join(doc_lines) + "".join(lines[insert_at:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--write", action="store_true", help="modify the file in place")
    parser.add_argument("--class", dest="class_name", help="only process this class name")
    parser.add_argument(
        "--line",
        type=int,
        help="1-indexed line number (e.g. the editor cursor); targets the innermost enclosing class",
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="include attributes whose name starts with '_' (excluded by default)",
    )
    args = parser.parse_args()

    source = args.path.read_text()
    tree = ast.parse(source)

    if args.line is not None:
        candidates = [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.ClassDef) and n.lineno <= args.line <= n.end_lineno
        ]
        classes = [min(candidates, key=lambda c: c.end_lineno - c.lineno)] if candidates else []
    else:
        classes = [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.ClassDef) and (args.class_name is None or n.name == args.class_name)
        ]
    if not classes:
        print("No matching classes found.", file=sys.stderr)
        return 1

    # Process bottom-up so earlier edits don't shift later line numbers.
    classes.sort(key=lambda c: c.lineno, reverse=True)

    result = source
    for cls in classes:
        tree = ast.parse(result)
        target = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == cls.name)
        updated = process_class(result, target, include_private=args.include_private)
        if updated is not None:
            result = updated

    if result == source:
        print("No attributes found / nothing to change.", file=sys.stderr)
        return 0

    if args.write:
        args.path.write_text(result)
        print(f"Updated {args.path}")
    else:
        diff = difflib.unified_diff(
            source.splitlines(keepends=True),
            result.splitlines(keepends=True),
            fromfile=str(args.path),
            tofile=str(args.path),
        )
        sys.stdout.writelines(diff)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
