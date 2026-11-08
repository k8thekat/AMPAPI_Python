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
from .hubs import PanelHub
from .platform import PlatformModule
from .shards import Shard, ShardModule
from .spires import Spire, SpireModule
from .tasks import TaskModule
from .templates import TemplateModule

if TYPE_CHECKING:
    from types import TracebackType

    from ._types import ShardResponse, SpireResponse
    from .session import Session

__all__ = ("Panel",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class Panel(
    PanelHub,
    AccountModule,
    AnalyticsModule,
    CredentialModule,
    PlatformModule,
    ShardModule,
    SpireModule,
    TaskModule,
    TemplateModule,
):
    """An AMP 3 panel, with every call this library wraps, and the panel level of the hubs.

    The calls come from the `...Module` classes it is built from, and each one logs in through the :class:`Session` when
    it needs to. A subclass can declare listeners, eg. ``@PanelHub.listener(name="console")``; see :class:`PanelHub`.

    .. versionadded:: 6.0.0

    Parameters
    ----------
    session : :class:`Session`
        The session to send calls through.
        Leaving an ``async with`` block, or :meth:`clean_up`, logs it out and closes it.
    shard_class : type[:class:`Shard`], optional
        The class `get_shard` and `get_shards` make, eg. a subclass with listeners, by default :class:`Shard`.
    spire_class : type[:class:`Spire`], optional
        The class `get_spire` and `get_spires` make, by default :class:`Spire`.

    """

    def __init__(self, session: Session, *, shard_class: type[Shard] = Shard, spire_class: type[Spire] = Spire) -> None:  # noqa: D107
        super().__init__(session=session)
        self.shard_class = shard_class
        self.spire_class = spire_class

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
        """Stop listening to the hubs, then log out and close the session, as :meth:`Session.clean_up` does.

        |coro|

        Endpoint: ``POST /api/auth/logout``

        """
        await self.stop_listening()
        await self.session.clean_up()

    def _make_shard(self, data: ShardResponse) -> Shard:
        """The shard object we already keep for `data`, brought up to date, so a shard listens through one object only."""
        for existing in self._shard_objects.get(data["id"], ()):
            if isinstance(existing, self.shard_class):
                existing.data = data
                existing.display_name = data["displayName"]
                return existing
        return super()._make_shard(data=data)

    def _make_spire(self, data: SpireResponse) -> Spire:
        """The spire object we already keep for `data`, brought up to date, so a spire listens through one object only."""
        for existing in self._spire_objects.get(data["id"], ()):
            if isinstance(existing, self.spire_class):
                existing.data = data
                existing.display_name = data["displayName"]
                return existing
        return super()._make_spire(data=data)

    async def _list_records(self) -> tuple[list[ShardResponse], list[SpireResponse]]:
        """The shard and spire lists the hub routing works from, as dicts, so no listener objects are made for them."""
        shards: list[ShardResponse] = await self._request(method="GET", path="/api/shards")
        spires: list[SpireResponse] = await self._request(method="GET", path="/api/spires")
        return shards, spires
