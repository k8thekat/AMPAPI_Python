# ruff: noqa
"""
Copyright (C) 2021-2022 Katelynn Cadwallader.

This file is part of Gatekeeper, the AMP API.

Gatekeeper is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

Gatekeeper is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with Gatekeeper; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

from __future__ import annotations

__title__ = "CubeCoders AMP API"
__author__ = "k8thekat"
__license__ = "GNU"
__version__ = "1.1.0"
__credits__ = "AMP by CubeCoders and associates."

from typing import Literal, NamedTuple

from . import dataclass as dataclass
from . import enums as enums
from . import modules as modules
from . import types_ as types
from . import util as util
from .adsmodule import *
from .analytics import *
from .base import *
from .bridge import *
from .controller import *
from .core import *
from .emailsender import *
from .filebackup import *
from .filemanager import *
from .instance import *
from .minecraft import *


class VersionInfo(NamedTuple):
    Major: int
    Minor: int
    Revision: int
    releaseLevel: Literal["alpha", "beta", "pre-release", "release", "development"]


version_info: VersionInfo = VersionInfo(Major=1, Minor=1, Revision=0, releaseLevel="release")

del NamedTuple, Literal, VersionInfo
