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
# PEP 440 form of 6.0.0-beta; pip treats it as a pre-release, so a plain install never picks it up.
__version__ = "6.0.0b0"
__credits__ = "AMP by CubeCoders and associates."

from typing import Literal, NamedTuple

from ._enums import *
from ._types import *
from .accounts import *
from .analytics import *
from .base import *
from .credentials import *
from .errors import *
from .panel import *
from .platform import *
from .session import *
from .shards import *
from .spires import *
from .tasks import *
from .templates import *


class VersionInfo(NamedTuple):
    Major: int
    Minor: int
    Revision: int
    releaseLevel: Literal["alpha", "beta", "pre-release", "release", "development"]


version_info: VersionInfo = VersionInfo(Major=6, Minor=0, Revision=0, releaseLevel="beta")

del NamedTuple, Literal, VersionInfo
