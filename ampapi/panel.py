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

import logging
from typing import TYPE_CHECKING, Optional, Self

from .accounts import AccountModule
from .analytics import AnalyticsModule
from .credentials import CredentialModule
from .platform import PlatformModule
from .spires import SpireModule
from .tasks import TaskModule

if TYPE_CHECKING:
    from types import TracebackType

__all__ = (
    "Panel",
    "Shard",
)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Panel(AccountModule, AnalyticsModule, CredentialModule, PlatformModule, SpireModule, TaskModule):
    """An AMP 3 panel, with every call this library wraps.

    The calls come from the `...Module` classes it is built from, and each one logs in through the :class:`Session` when
    it needs to.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session to send calls through.
        Leaving an ``async with`` block, or :meth:`clean_up`, logs it out and closes it.

    """

    async def __aenter__(self) -> Self:  # noqa: D105
        return self

    async def __aexit__(  # noqa: D105
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.clean_up()

    async def clean_up(self) -> None:
        """Log out and close the session, the same as :meth:`Session.clean_up`.

        |coro|

        """
        await self.session.clean_up()


class Shard:
    """A shard, AMP 3's name for an Instance, with the calls that act on it.

    .. versionadded:: 6.0.0

    """

    # TODO: Build `Shard` from the shard findings (#47.7).
    # Each method calls the `ShardModule` one with its own ID, eg. `shard.start()` is `panel.start_shard(shard_id)`.
    # It moves to shards.py beside `ShardModule`, as `Spire` sits beside `SpireModule`.
