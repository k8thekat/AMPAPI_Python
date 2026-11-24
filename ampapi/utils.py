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

from typing import Any, TypeGuard

# The helpers here are shared between the library's modules, so `from ampapi import *` doesn't bring them in.
__all__ = ()


def is_dotted_key(value: object) -> bool:
    """If `value` is one of AMP's dotted keys, eg. ``"shards.error.moveNotRunning"``, rather than an English sentence."""
    # A sentence has spaces in it.
    if not isinstance(value, str) or value.split() != [value]:
        return False
    # A key has its dots between words. A one word sentence would only end with a dot.
    return "." in value.rstrip(".")


def is_json_object(value: object) -> TypeGuard[dict[str, Any]]:
    """If `value` is a decoded JSON object, whose keys are always strings."""
    return isinstance(value, dict)
