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
    """The calls for joining a new spire to the panel: the message bus a spire joins over, and the join files (enrolments).

    An enrolment is a machine that isn't a spire yet. Open the message bus with :meth:`expand_message_bus`, make a join
    file with :meth:`create_spire_enrollment`, then :meth:`approve_spire_enrollment` once the machine has used the join
    file.

    A fresh panel's first-run setup, its network step included, is :class:`SetupModule`.

    .. versionadded:: 6.0.0

    """

    async def approve_spire_enrollment(self, enrollment_id: str) -> SpireEnrollmentResponse:
        """Let the machine that used the enrolment's join file become a spire.

        |coro|

        Endpoint: ``POST /api/spires/enrollments/{enrollment_id}/approve``

        Check the enrolment's `admission` first: its `fingerprint` should match the fingerprint the joining machine
        shows in its `HealthStatusResponse.messageParams`. The machine collects its credential the next time the machine
        asks the panel, and joins within seconds. The enrolment's `status` then goes from ``"approved"`` to
        ``"redeemed"``.

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

        The new machine takes the join file's `joinBlob` in its own first-run setup, then waits for
        :meth:`approve_spire_enrollment`. This library doesn't wrap the new machine's first-run setup, so the join file
        goes into the new machine's setup page. :meth:`PlatformModule.get_health_status` on the new machine shows the
        wait.

        A public entry node is a relay and a front door for the panel that hosts no shards. Its enrolment reads `role`
        ``"publicentrynode"``.

        - The panel dials the entry node at `public_host` over a WireGuard tunnel.
        - An entry node needs AMP's own message bus, and WireGuard on the panel's machine.
        - The logged in user needs the network-manage capability as well as spire-create.
        - AMP only checks the host's form. A host nothing answers on is accepted, and the enrolment's `entryNodeState`
          stays ``"waiting"``.

        Parameters
        ----------
        label : :class:`str`
            A name for the enrolment. The spire the machine becomes takes the label as its `displayName`.
        expires_in_hours : Union[:class:`int`, None], optional
            How long the join file works for, 1 to 720, by default None for AMP's 72.
        hosts : Union[list[:class:`str`], None], optional
            The addresses the new machine should reach the panel on, by default None for the network address the
            message bus is bound to. The machine uses the first address it can reach, so a network address and a public
            address together cover a machine on the panel's network and a machine outside it. See
            :meth:`get_spire_enrollment_hosts`.
        entry_node : :class:`bool`, optional
            If the machine joins as a public entry node rather than a spire or not, by default False.
        public_host : Union[:class:`str`, None], optional
            The entry node's public address, eg. ``"203.0.113.10"``, by default None. An entry node needs a public
            address. A standard enrolment ignores `public_host`.

        Returns
        -------
        :class:`SpireEnrollmentCreatedResponse`
            The enrolment (201), with `status` ``"pending"``, and the join file, which AMP sends only in this reply.

        Raises
        ------
        AMPAPIRequestError
            **400** - If `label` is empty, or the message bus can't issue credentials, from AMP's docs and not seen
            live.\n
            **400** - If an entry node has no `public_host` `spire.enroll.error.entryNodeHostRequired`.\n
            **400** - If `public_host` isn't a host name or an IP address `spire.enroll.error.entryNodeHostInvalid`.\n
            **400** - If an entry node is asked for and no tunnel slot is left, from AMP's docs and not seen live.\n
            **400** - If an entry node is asked for and the panel's machine has no WireGuard, from AMP's docs and not seen
            live.\n
            **403** - If the logged in user lacks the spire-create capability, or network-manage for an entry node, from
            AMP's docs and not seen live.\n
            **409** - If another entry node is being made at the same moment, from AMP's docs and not seen live.

        """
        data: SpireEnrollmentRequest = {"label": label, "hosts": hosts if hosts is not None else []}

        if expires_in_hours is not None:
            data["expiresInHours"] = expires_in_hours

        # `entryNode` and `publicHost` matter only for an entry node. AMP ignores the host on a standard enrolment.
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
        fine too. Revoking doesn't remove a machine that already joined, as the machine has its own credential. Delete
        that spire instead, see :meth:`SpireModule.delete_spire`.

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

        This call does the same as :meth:`SetupModule.expand_setup_network`, through the system route. Use this call
        once the panel is set up, and :meth:`SetupModule.expand_setup_network` during the first-run setup.

        - AMP opens the message bus's port (TCP 4222 unless the spire's `busPort` says otherwise) on the host's
          firewall. Nothing restarts.
        - The message bus's `servers` move from ``127.0.0.1`` to the machine's network address.
        - Calling :meth:`expand_message_bus` again on an open message bus answers the same.

        .. warning::
            There's no call to close the message bus again. To close the message bus by hand on the panel's machine:

            - Set `ManagedNats.MultiMachine` and `IsPublic` back to `false` in
              ``/opt/cubecoders/amp3/data/bootstrap.local.json``. Keep the file owned by ``amp:amp`` with mode 600.
            - Run ``systemctl restart amp3``. The health `phase` reads ``"starting"`` for under a minute, then the
              firewall closes the port again. The logged in user's session survives the restart.

        Returns
        -------
        :class:`BusExpandResponse`
            How to reach the message bus now, and what became of the port's firewall rule. A firewall `outcome` other
            than ``"Open"`` is information to act on, not a failed call.

            - ``"Open"``: AMP opened the port.
            - ``"NotManaged"``, ``"Pending"`` or ``"WriteFailed"``: AMP's docs name these outcomes without saying what
              each means, and no capture shows them yet. Check the port on the host by hand.
            - When `agentRunning` is `False`, the port has to be opened by hand.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the logged in user lacks the spire-create capability, from AMP's docs and not seen live.\n
            **409** - If the panel uses an external message bus that AMP doesn't manage, from AMP's docs and not seen
            live.

        """
        return await self._request(method="POST", path="/api/system/bus/expand")

    async def get_message_bus(self) -> SystemBusResponse:
        """Get the state of the message bus spires talk to the panel over.

        |coro|

        Endpoint: ``GET /api/system/bus``

        Returns
        -------
        :class:`SystemBusResponse`
            If AMP runs the message bus, if the message bus is open to other machines, and how to join the message bus.

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
            The enrolments, newest first. Revoked and redeemed enrolments stay in the list.

        """
        return await self._request(method="GET", path="/api/spires/enrollments")
