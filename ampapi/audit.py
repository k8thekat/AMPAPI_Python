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
from typing import TYPE_CHECKING, Optional, Union

from .base import Base

if TYPE_CHECKING:
    from ._enums import AuditOrigin, AuditSeverity, AuditSort
    from ._types import AuditFacetsResponse, AuditPageResponse, AuditRootsPageResponse, AuditTreeResponse

__all__ = ("AuditModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class AuditModule(Base):
    """The calls for the audit log: who did what on the panel, as single events or grouped into flows.

    .. versionadded:: 6.0.0

    """

    async def get_audit_events(
        self,
        *,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        origin: Optional[AuditOrigin] = None,
        min_severity: Optional[AuditSeverity] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        search: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[AuditSort] = None,
    ) -> AuditPageResponse:
        """Get one page of the audit log.

        |coro|

        Endpoint: ``GET /api/audit``

        Parameters
        ----------
        user_id : Union[:class:`str`, None], optional
            Only events by this user's ID, and the events inside a flow the user started, by default None.
        action : Union[:class:`str`, None], optional
            Only this action, eg. ``"ShardCreated"`` (any case), by default None.
            - See :meth:`get_audit_facets` for the actions logged so far.
            - An action AMP doesn't know, eg. a misspelt action, gives no events rather than an error.
        origin : Union[:class:`AuditOrigin`, None], optional
            Only events with this origin, by default None.
        min_severity : Union[:class:`AuditSeverity`, None], optional
            Only events of this severity or higher, by default None.
        target_type : Union[:class:`str`, None], optional
            Only events about this kind of target, eg. ``"Shard"``, by default None.
        target_id : Union[:class:`str`, None], optional
            Only events about the target with this ID, by default None.
        correlation_id : Union[:class:`str`, None], optional
            Only the events of one flow, by default None. Use the flow's `correlationId` from :meth:`get_audit_roots`,
            or an event's `correlationId["value"]`, as an event wraps the ID. The same events as
            :meth:`get_audit_tree`, as a flat page.
        search : Union[:class:`str`, None], optional
            Text to look for, by default None.
        from_time : Union[:class:`str`, None], optional
            The earliest time, ISO 8601 like ``"2026-11-01T00:00:00Z"``, by default None.
        to_time : Union[:class:`str`, None], optional
            The latest time, ISO 8601, by default None.
        page : Union[:class:`int`, None], optional
            The page, from 1, by default None.
            - AMP reads page 0 as page 1.
        page_size : Union[:class:`int`, None], optional
            Events a page, by default None. AMP gives 50 unless asked.
            - AMP reads a size below 1 as 1, and a size above 200 as 200.
        sort : Union[:class:`AuditSort`, None], optional
            The order of the events, by default None for newest first.

        Returns
        -------
        :class:`AuditPageResponse`
            The page of events and the total that match.

        Raises
        ------
        AMPAPIRequestError
            AMP's 400 for a filter AMP can't read carries no `code`.\n
            **400** - If `origin` is a number no `AuditOrigin` member has. The error's `errors` is keyed by ``"origin"``.\n
            **400** - If `min_severity` is a number no `AuditSeverity` member has. The error's `errors` is keyed by
            ``"minSeverity"``.\n
            **400** - If AMP can't read `from_time`. The error's `errors` is keyed by ``"from"``.\n
            **400** - If AMP can't read `to_time`. The error's `errors` is keyed by ``"to"``.

        """
        filters: dict[str, Optional[Union[str, int]]] = {
            "userId": user_id,
            "action": action,
            "origin": origin,
            "minSeverity": min_severity,
            "targetType": target_type,
            "targetId": target_id,
            "correlationId": correlation_id,
            "search": search,
            "from": from_time,
            "to": to_time,
            "page": page,
            "pageSize": page_size,
            "sort": sort,
        }

        # We only send the filters that are set, as the web panel does.
        parameters: dict[str, Union[str, int]] = self._without_none(mapping=filters)

        return await self._request(method="GET", path="/api/audit", parameters=parameters)

    async def get_audit_facets(self) -> AuditFacetsResponse:
        """Get what the audit log's filters can choose from, with how often each was logged.

        |coro|

        Endpoint: ``GET /api/audit/facets``

        Returns
        -------
        :class:`AuditFacetsResponse`
            The actions, users, target types and origins seen so far.

        """
        return await self._request(method="GET", path="/api/audit/facets")

    async def get_audit_roots(
        self,
        *,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        origin: Optional[AuditOrigin] = None,
        min_severity: Optional[AuditSeverity] = None,
        target_type: Optional[str] = None,
        target_id: Optional[str] = None,
        search: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[AuditSort] = None,
    ) -> AuditRootsPageResponse:
        """Get one page of the audit log grouped into flows, each led by the event that started it.

        |coro|

        Endpoint: ``GET /api/audit/roots``

        The filters are :meth:`get_audit_events`' filters without `correlation_id`. Each filter but `min_severity` is
        matched against the flow's first event.

        Parameters
        ----------
        user_id : Union[:class:`str`, None], optional
            Only flows this user's ID started, by default None.
        action : Union[:class:`str`, None], optional
            Only this action, eg. ``"ShardCreated"`` (any case), by default None.
            - See :meth:`get_audit_facets` for the actions logged so far.
            - An action AMP doesn't know, eg. a misspelt action, gives no flows rather than an error.
        origin : Union[:class:`AuditOrigin`, None], optional
            Only flows started with this origin, by default None.
            - A flow never starts with an `AuditOrigin.user_flow` event, so `AuditOrigin.user_flow` finds no flows.
        min_severity : Union[:class:`AuditSeverity`, None], optional
            Only flows with an event of this severity or higher, by default None.
        target_type : Union[:class:`str`, None], optional
            Only events about this kind of target, eg. ``"Shard"``, by default None.
        target_id : Union[:class:`str`, None], optional
            Only events about the target with this ID, by default None.
        search : Union[:class:`str`, None], optional
            Text to look for, by default None.
        from_time : Union[:class:`str`, None], optional
            The earliest time, ISO 8601 like ``"2026-11-01T00:00:00Z"``, by default None.
        to_time : Union[:class:`str`, None], optional
            The latest time, ISO 8601, by default None.
        page : Union[:class:`int`, None], optional
            The page, from 1, by default None.
            - AMP reads page 0 as page 1.
        page_size : Union[:class:`int`, None], optional
            Flows a page, by default None.
            - AMP reads a size below 1 as 1, and a size above 200 as 200.
        sort : Union[:class:`AuditSort`, None], optional
            The order of the flows, by default None for newest first.

        Returns
        -------
        :class:`AuditRootsPageResponse`
            The page of flows and the total that match.

        Raises
        ------
        AMPAPIRequestError
            AMP's 400 for a filter AMP can't read carries no `code`.\n
            **400** - If `origin` is a number no `AuditOrigin` member has. The error's `errors` is keyed by ``"origin"``.\n
            **400** - If `min_severity` is a number no `AuditSeverity` member has. The error's `errors` is keyed by
            ``"minSeverity"``.\n
            **400** - If AMP can't read `from_time`. The error's `errors` is keyed by ``"from"``.\n
            **400** - If AMP can't read `to_time`. The error's `errors` is keyed by ``"to"``.

        """
        filters: dict[str, Optional[Union[str, int]]] = {
            "userId": user_id,
            "action": action,
            "origin": origin,
            "minSeverity": min_severity,
            "targetType": target_type,
            "targetId": target_id,
            "search": search,
            "from": from_time,
            "to": to_time,
            "page": page,
            "pageSize": page_size,
            "sort": sort,
        }

        # We only send the filters that are set, as the web panel does.
        parameters: dict[str, Union[str, int]] = self._without_none(mapping=filters)

        return await self._request(method="GET", path="/api/audit/roots", parameters=parameters)

    async def get_audit_tree(self, correlation_id: str) -> AuditTreeResponse:
        """Get every event in one flow, as a tree.

        |coro|

        Endpoint: ``GET /api/audit/tree/{correlation_id}``

        Parameters
        ----------
        correlation_id : :class:`str`
            The flow's `correlationId` from :meth:`get_audit_roots`; the root event's own `id` gives 404.

        Returns
        -------
        :class:`AuditTreeResponse`
            The flow, from its first event down.

        Raises
        ------
        AMPAPIRequestError
            **404** - If no events carry that ID `audit.error.flowNotFound`.

        """
        return await self._request(method="GET", path=f"/api/audit/tree/{correlation_id}")
