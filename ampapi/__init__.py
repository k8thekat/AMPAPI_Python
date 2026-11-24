# ruff: noqa: N815, F821, UP037 # version_info is deleted after use
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

__title__ = "AMPAPI Python"
__author__ = "k8thekat"
__license__ = "GNU"
# PEP 440 form of 6.0.0-beta.5; pip treats it as a pre-release, so a plain install never picks it up.
__version__ = "6.0.0b5"
__credits__ = "AMP by CubeCoders and associates."

from typing import Literal, NamedTuple

from . import (
    _enums,
    _types,
    accounts,
    analytics,
    audit,
    base,
    credentials,
    enrollments,
    errors,
    https,
    licence,
    networking,
    objects,
    panel,
    platform,
    session,
    setup,
    shards,
    spires,
    tasks,
    templates,
)
from ._enums import *
from ._types import *
from .accounts import *
from .analytics import *
from .audit import *
from .base import *
from .credentials import *
from .enrollments import *
from .errors import *
from .https import *

# from .hubs import *
from .licence import *
from .networking import *
from .objects import *
from .panel import *
from .platform import *
from .session import *
from .setup import *
from .shards import *
from .spires import *
from .tasks import *
from .templates import *

# Each module's own `__all__`, so `from ampapi import *` brings in the public names and not the modules or `typing`.
__all__ = ["version_info"]
__all__ += _enums.__all__
__all__ += _types.__all__
__all__ += accounts.__all__
__all__ += analytics.__all__
__all__ += audit.__all__
__all__ += base.__all__
__all__ += credentials.__all__
__all__ += enrollments.__all__
__all__ += errors.__all__
__all__ += https.__all__
# __all__ += hubs.__all__
__all__ += licence.__all__
__all__ += networking.__all__
__all__ += objects.__all__
__all__ += panel.__all__
__all__ += platform.__all__
__all__ += session.__all__
__all__ += setup.__all__
__all__ += shards.__all__
__all__ += spires.__all__
__all__ += tasks.__all__
__all__ += templates.__all__


class VersionInfo(NamedTuple):
    Major: int
    Minor: int
    Revision: int
    releaseLevel: Literal["alpha", "beta", "pre-release", "release", "development"]
    # Which alpha, beta or pre-release of this version it is, as `sys.version_info` counts them; 0 for a release.
    serial: int


version_info: VersionInfo = VersionInfo(Major=6, Minor=0, Revision=0, releaseLevel="beta", serial=5)

del NamedTuple, Literal, VersionInfo
