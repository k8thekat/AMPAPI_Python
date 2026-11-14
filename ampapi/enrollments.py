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
from typing import TYPE_CHECKING, Optional

from .base import Base

if TYPE_CHECKING:
    from ._types import (
        BusExpandResponse,
        SpireEnrollmentCreatedResponse,
        SpireEnrollmentHostResponse,
        SpireEnrollmentRequest,
        SpireEnrollmentResponse,
        SpireEnrollmentRevokeRequest,
        SystemBusResponse,
    )

__all__ = ("EnrollmentModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class EnrollmentModule(Base):
    """The calls for joining a new spire to the panel: the message bus it joins over, and the join files (enrolments).

    An enrolment is a machine that isn't a spire yet. Open the bus with :meth:`expand_message_bus`, make a join file
    with :meth:`create_spire_enrollment`, then :meth:`approve_spire_enrollment` once the machine has used the join file.

    .. versionadded:: 6.0.0

    """

    async def approve_spire_enrollment(self, enrollment_id: str) -> SpireEnrollmentResponse:
        """Let the machine that used the enrolment's join file become a spire.

        |coro|

        Endpoint: ``POST /api/spires/enrollments/{enrollment_id}/approve``

        Check the enrolment's `admission` first: its `fingerprint` should match the fingerprint the joining machine
        shows in its `HealthStatusResponse.messageParams`. The machine collects its credential the next time it asks
        and joins within seconds, and the enrolment's `status` goes from ``"approved"`` to ``"redeemed"``.

        Parameters
        ----------
        enrollment_id : :class:`str`
            The enrolment's ID, once the enrolment's `status` is ``"awaitingapproval"``.

        Returns
        -------
        :class:`SpireEnrollmentResponse`
            The enrolment, with `status` ``"approved"``.

        Raises
        ------
        AMPAPIRequestError
            **409** - If no machine is waiting on the enrolment `spire.enroll.error.nothingToApprove`.

        """
        return await self._request(method="POST", path=f"/api/spires/enrollments/{enrollment_id}/approve")

    async def create_spire_enrollment(
        self,
        label: str,
        *,
        expires_in_hours: Optional[int] = None,
        hosts: Optional[list[str]] = None,
        entry_node: bool = False,
        public_host: Optional[str] = None,
    ) -> SpireEnrollmentCreatedResponse:
        """Make a join file, so another machine can join the panel as a spire, or as a public entry node.

        |coro|

        Endpoint: ``POST /api/spires/enrollments``

        .. warning::
            AMP refuses the enrolment with ``"spire.enroll.error.busNotPublic"`` until the message bus is opened to
            other machines (:meth:`expand_message_bus`).

        The new machine's first-run setup takes the `joinBlob`, then waits in :meth:`PlatformModule.get_health_status`
        until :meth:`approve_spire_enrollment`.

        A public entry node is a relay and a front door for the panel that hosts no shards; its enrolment reads `role`
        ``"publicentrynode"``. The panel dials the entry node at `public_host` over a WireGuard tunnel, so an entry node
        needs the panel's own message bus and WireGuard on the panel's machine, and the logged in user needs the network
        manage permission too. AMP only checks the host's form: a host nothing answers on is accepted, and the
        enrolment's `entryNodeState` stays ``"waiting"``.

        Parameters
        ----------
        label : :class:`str`
            A name for the enrolment; the spire the machine becomes takes the label as its `displayName`.
        expires_in_hours : Union[:class:`int`, None], optional
            How long the join file works for, 1 to 720, by default None for AMP's 72.
        hosts : Union[list[:class:`str`], None], optional
            The addresses the new machine should reach the panel on, by default None for the network address the
            message bus is bound to. The machine uses the first address it can reach, so a network address and a public
            address together cover both cases. See :meth:`get_spire_enrollment_hosts`.
        entry_node : :class:`bool`, optional
            If the machine joins as a public entry node rather than a spire or not, by default False.
        public_host : Union[:class:`str`, None], optional
            The entry node's public address, eg. ``"203.0.113.10"``, by default None. An entry node needs a public
            address, and a standard enrolment ignores it.

        Returns
        -------
        :class:`SpireEnrollmentCreatedResponse`
            The enrolment (201), with `status` ``"pending"``, and the join file, which AMP sends only in this reply.

        Raises
        ------
        AMPAPIRequestError
            **400** - If an entry node has no `public_host` `spire.enroll.error.entryNodeHostRequired`.\n
            **400** - If `public_host` isn't a host `spire.enroll.error.entryNodeHostInvalid`.\n
            **400** - If an entry node is asked for and no tunnel slot is left, from AMP's docs and not seen live.\n
            **400** - If an entry node is asked for and the panel's machine has no WireGuard, from AMP's docs and not seen
            live.\n
            **409** - If another entry node is being made at the same moment, from AMP's docs and not seen live.

        """
        data: SpireEnrollmentRequest = {"label": label, "hosts": hosts if hosts is not None else []}

        if expires_in_hours is not None:
            data["expiresInHours"] = expires_in_hours

        # Only an entry node takes the two; AMP ignores the host on a standard enrolment
        if entry_node is True:
            data["entryNode"] = True

        if public_host is not None:
            data["publicHost"] = public_host

        return await self._request(method="POST", path="/api/spires/enrollments", data=data)

    async def delete_spire_enrollment(self, enrollment_id: str, *, reason: Optional[str] = None) -> None:
        """Revoke a join file.

        |coro|

        Endpoint: ``DELETE /api/spires/enrollments/{enrollment_id}``

        The enrolment stays in :meth:`get_spire_enrollments` with `status` ``"revoked"``. Revoking the enrolment again is
        fine too. Revoking doesn't remove a machine that already joined, which has its own credential; delete that spire
        instead, see :meth:`SpireModule.delete_spire`.

        Parameters
        ----------
        enrollment_id : :class:`str`
            The enrolment's ID.
        reason : Union[:class:`str`, None], optional
            Why the enrolment was revoked, by default None. AMP keeps the reason as the enrolment's `revokedReason`.

        """
        data: Optional[SpireEnrollmentRevokeRequest] = {"reason": reason} if reason is not None else None
        await self._request(method="DELETE", path=f"/api/spires/enrollments/{enrollment_id}", data=data)

    async def deny_spire_enrollment(self, enrollment_id: str) -> None:
        """Refuse the machine that used the enrolment's join file.

        |coro|

        Endpoint: ``POST /api/spires/enrollments/{enrollment_id}/deny``

        The enrolment then reads ``"denied"``, with `deniedAt` and `deniedByName` in its `admission`. Within a few
        seconds the machine's health reads ``"auth.setup.joining.refused"``, and the machine can take a new join file
        without reinstalling AMP.

        Parameters
        ----------
        enrollment_id : :class:`str`
            The enrolment's ID.

        Raises
        ------
        AMPAPIRequestError
            **404** - If there's no enrolment with that ID.\n
            **409** - If no machine is waiting on the enrolment, eg. the enrolment is pending, revoked or already
            denied `spire.enroll.error.nothingToApprove`.

        """
        await self._request(method="POST", path=f"/api/spires/enrollments/{enrollment_id}/deny")

    async def expand_message_bus(self) -> BusExpandResponse:
        """Open the message bus to other machines, which a new spire needs to join.

        |coro|

        Endpoint: ``POST /api/system/bus/expand``

        .. warning::
            Opening the bus changes how the panel is reached, and there's no call to close the bus again.

        AMP opens the bus's port on the host's firewall. Calling this again on an open bus answers the same.

        Returns
        -------
        :class:`BusExpandResponse`
            How to reach the bus now, and the port AMP opened.

        """
        return await self._request(method="POST", path="/api/system/bus/expand")

    async def get_message_bus(self) -> SystemBusResponse:
        """Get the state of the message bus spires talk to the panel over.

        |coro|

        Endpoint: ``GET /api/system/bus``

        Returns
        -------
        :class:`SystemBusResponse`
            If AMP runs the bus, if the bus is public and how to join the bus.

        """
        return await self._request(method="GET", path="/api/system/bus")

    async def get_spire_enrollment_hosts(self) -> list[SpireEnrollmentHostResponse]:
        """Get the addresses a new spire could reach the panel on.

        |coro|

        Endpoint: ``GET /api/spires/enrollments/hosts``

        Returns
        -------
        list[:class:`SpireEnrollmentHostResponse`]
            The addresses, the panel's public address included.

        """
        return await self._request(method="GET", path="/api/spires/enrollments/hosts")

    async def get_spire_enrollments(self) -> list[SpireEnrollmentResponse]:
        """Get the join files that were made, and their state.

        |coro|

        Endpoint: ``GET /api/spires/enrollments``

        Returns
        -------
        list[:class:`SpireEnrollmentResponse`]
            The enrolments, newest first. Revoked and redeemed ones stay in the list.

        """
        return await self._request(method="GET", path="/api/spires/enrollments")
