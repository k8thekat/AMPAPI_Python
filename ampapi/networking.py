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

from ._enums import GatewayState, PublicationState
from .base import Base

if TYPE_CHECKING:
    from ._types import (
        FirewallResponse,
        GatewayEligibilityResponse,
        GatewayPreflightResponse,
        GatewayRequest,
        GatewayResponse,
        PublicationRequest,
        PublicationResponse,
        PublicationUpdateRequest,
        TunnelFrontResponse,
        TunnelResponse,
    )

__all__ = ("NetworkModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class NetworkModule(Base):
    """The calls for the panel's networking: the host firewall, gateways, public port forwards and the tunnels between
    spires.

    The port claims of one spire are :meth:`SpireModule.get_spire_port_claims`.

    .. versionadded:: 6.0.0

    """

    # TODO: Trim the note once AMP fixes the gateway status gaps (U26b, U26e).
    # AMP 3.0.0.6 routes a running shard only after it restarts, and reads `Fault` while a new tunnel connects.
    async def create_gateway(self, shard_id: str, front_spire_id: str) -> GatewayResponse:
        """Route a shard through a front spire, so players reach it at that spire's address.

        |coro|

        Endpoint: ``POST /api/networking/gateways``

        A gateway is the shard's route over a WireGuard tunnel between its spire and the front spire, which AMP sets up
        itself (see :meth:`get_tunnels`). The shard gets an `address` on that tunnel, eg. ``"10.83.0.10"``, and an
        `egressAllowList`. Once it routes, the shard answers on the front spire's address at its own port. Follow it
        with :meth:`get_gateways`.

        .. note::
            A shard that was running before the gateway only routes once it restarts. Until then the gateway reads
            `GatewayState.awaiting_shard` with `runningWithoutRoute`, though the shard's endpoint already lists the
            front's address. A new gateway also reads `GatewayState.fault` while its tunnel connects.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        front_spire_id : :class:`str`
            The front spire's ID. It needs its ``"spire.publicHost"`` setting set, see
            :meth:`SpireModule.set_spire_settings`.

        Returns
        -------
        :class:`GatewayResponse`
            The gateway AMP made (201), its `status` `None` until AMP has set the route up.

        Raises
        ------
        AMPAPIRequestError
            If the front spire doesn't exist or has no public host (400, ``"networking.error.frontNotRoutable"``), or
            the shard already runs on it (400, ``"networking.error.gatewaySameSpire"``). :meth:`preflight_gateway`
            catches neither.

        """
        data: GatewayRequest = {"shardId": shard_id, "frontSpireId": front_spire_id}
        result: GatewayResponse = await self._request(method="POST", path="/api/networking/gateways", data=data)
        return self._gateway_enums(gateway=result)

    # TODO: Drop the note once AMP stops reading `TunnelFault` while a first tunnel is set up (U26a).
    # AMP 3.0.0.6 reads it for about a minute, then the publication turns active by itself.
    async def create_publication(self, front_spire_id: str, public_port: int, shard_id: str, port_reference: str) -> PublicationResponse:
        """Forward a public port on a front spire to a shard's port.

        |coro|

        Endpoint: ``POST /api/networking/publications``

        Through another spire, AMP sets up a WireGuard tunnel between the two spires (see :meth:`get_tunnels`), and the
        forward works once :meth:`get_publications` reads it `PublicationState.active`.

        .. note::
            A first publication through another spire can read `PublicationState.tunnel_fault` with
            ``"The file does not exist."`` for about a minute, while the tunnel's agent is put in place, then turns
            active by itself.

        Parameters
        ----------
        front_spire_id : :class:`str`
            The front spire's ID. The shard's own spire works as it is; another spire needs its ``"spire.publicHost"``
            setting set first, see :meth:`SpireModule.set_spire_settings`.
        public_port : :class:`int`
            The port players connect to.
        shard_id : :class:`str`
            The shard's ID.
        port_reference : :class:`str`
            The shard port's `ref`, eg. ``"ServerPort"``, see :meth:`ShardModule.get_shard_ports`.

        Returns
        -------
        :class:`PublicationResponse`
            The publication AMP made (201), turned on, with the `protocol` of the shard's port and `status` `None`.

        Raises
        ------
        AMPAPIRequestError
            If the front is another spire with no public host (400, ``"networking.error.frontNoPublicHost"``), which
            AMP checks before the port. Else if `public_port` isn't a port number (400, ``"networking.error.invalidPort"``),
            or the shard has no port named `port_reference` (400, ``"networking.error.portRefMissing"``).

        """
        data: PublicationRequest = {
            "frontSpireId": front_spire_id,
            "publicPort": public_port,
            "shardId": shard_id,
            "portRef": port_reference,
        }

        result: PublicationResponse = await self._request(method="POST", path="/api/networking/publications", data=data)
        return self._publication_enums(publication=result)

    async def delete_gateway(self, gateway_id: str) -> None:
        """Remove a gateway.

        |coro|

        Endpoint: ``DELETE /api/networking/gateways/{gateway_id}``

        Its tunnel goes some seconds after.

        Parameters
        ----------
        gateway_id : :class:`str`
            The gateway's ID.

        Raises
        ------
        AMPAPIRequestError
            If there's no such gateway, eg. it was removed already (404).

        """
        await self._request(method="DELETE", path=f"/api/networking/gateways/{gateway_id}")

    async def delete_publication(self, publication_id: str) -> None:
        """Remove a public port forward.

        |coro|

        Endpoint: ``DELETE /api/networking/publications/{publication_id}``

        Parameters
        ----------
        publication_id : :class:`str`
            The publication's ID.

        Raises
        ------
        AMPAPIRequestError
            If there's no such publication, eg. it was removed already (404).

        """
        await self._request(method="DELETE", path=f"/api/networking/publications/{publication_id}")

    async def get_firewall(self) -> FirewallResponse:
        """Get the firewall rules AMP keeps on the host.

        |coro|

        Endpoint: ``GET /api/networking/firewall``

        Returns
        -------
        :class:`FirewallResponse`
            The rules applied and anything held back.

        """
        return await self._request(method="GET", path="/api/networking/firewall")

    async def get_gateway_eligibility(self) -> GatewayEligibilityResponse:
        """Get the shards and front spires that can take part in a gateway.

        |coro|

        Endpoint: ``GET /api/networking/gateway-eligibility``

        Returns
        -------
        :class:`GatewayEligibilityResponse`
            The shard and front spire IDs.

        """
        return await self._request(method="GET", path="/api/networking/gateway-eligibility")

    def _gateway_enums(self, gateway: GatewayResponse) -> GatewayResponse:
        if gateway["status"] is not None:
            gateway["status"]["state"] = self._to_enum(GatewayState, gateway["status"]["state"])
        return gateway

    async def get_gateways(self) -> list[GatewayResponse]:
        """Get the gateways, each a shard's route through a front spire, see :meth:`create_gateway`.

        |coro|

        Endpoint: ``GET /api/networking/gateways``

        Returns
        -------
        list[:class:`GatewayResponse`]
            The gateways, each `status.state` a :class:`GatewayState`.

        """
        result: list[GatewayResponse] = await self._request(method="GET", path="/api/networking/gateways")
        return [self._gateway_enums(gateway=gateway) for gateway in result]

    def _publication_enums(self, publication: PublicationResponse) -> PublicationResponse:
        if publication["status"] is not None:
            publication["status"]["state"] = self._to_enum(PublicationState, publication["status"]["state"])
        return publication

    async def get_publications(self) -> list[PublicationResponse]:
        """Get the public port forwards from front spires to shards.

        |coro|

        Endpoint: ``GET /api/networking/publications``

        Returns
        -------
        list[:class:`PublicationResponse`]
            The publications, each `status.state` a :class:`PublicationState`.

        """
        result: list[PublicationResponse] = await self._request(method="GET", path="/api/networking/publications")
        return [self._publication_enums(publication=publication) for publication in result]

    async def get_tunnel_fronts(self) -> list[TunnelFrontResponse]:
        """Get the spires that can front a tunnel, for a publication or a gateway through them.

        |coro|

        Endpoint: ``GET /api/networking/tunnel-fronts``

        Returns
        -------
        list[:class:`TunnelFrontResponse`]
            The tunnel fronts, empty until a spire has its ``"spire.publicHost"`` setting set.

        """
        return await self._request(method="GET", path="/api/networking/tunnel-fronts")

    async def get_tunnels(self) -> list[TunnelResponse]:
        """Get the WireGuard tunnels between spires.

        |coro|

        Endpoint: ``GET /api/networking/tunnels``

        AMP makes one on demand for a publication or a gateway through another spire, with addresses such as
        ``"10.83.0.1"`` (the front) and ``"10.83.0.2"`` (the back), and removes it some seconds after it's no longer
        needed.

        Returns
        -------
        list[:class:`TunnelResponse`]
            The tunnels.

        """
        return await self._request(method="GET", path="/api/networking/tunnels")

    # TODO: Trim the warning once AMP's preflight checks what the create checks (U20b, U20c).
    # AMP 3.0.0.6 passes an empty body, a gateway on the shard's own spire and a front spire with no public host.
    async def preflight_gateway(self, shard_id: str, front_spire_id: str) -> GatewayPreflightResponse:
        """Check a gateway can be made, before :meth:`create_gateway`.

        |coro|

        Endpoint: ``POST /api/networking/gateways/preflight``

        .. warning::
            AMP checks little here: an empty body and a gateway on the shard's own spire pass with no conflicts, and
            so does a front spire with no public host, though :meth:`create_gateway` refuses the last two.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        front_spire_id : :class:`str`
            The front spire's ID.

        Returns
        -------
        :class:`GatewayPreflightResponse`
            What stands in the way of the gateway.

        """
        data: GatewayRequest = {"shardId": shard_id, "frontSpireId": front_spire_id}
        return await self._request(method="POST", path="/api/networking/gateways/preflight", data=data)

    # TODO: Drop the old status sentence once AMP answers with the new one (U26c).
    # AMP 3.0.0.6 answers a publication turned off with its old `Active` status.
    async def update_publication(
        self,
        publication_id: str,
        *,
        enabled: Optional[bool] = None,
        public_port: Optional[int] = None,
    ) -> PublicationResponse:
        """Turn a public port forward on or off, or move it to another port.

        |coro|

        Endpoint: ``PUT /api/networking/publications/{publication_id}``

        The two changes are separate: moving the port leaves `enabled` as it was. With neither, AMP changes nothing.

        Parameters
        ----------
        publication_id : :class:`str`
            The publication's ID.
        enabled : Union[:class:`bool`, None], optional
            If the forward is on or not, by default None.
        public_port : Union[:class:`int`, None], optional
            The new public port, by default None.

        Returns
        -------
        :class:`PublicationResponse`
            The publication after the change. Its `status` can still be the old one, eg. active after turning it off,
            so read :meth:`get_publications` for the new state.

        Raises
        ------
        AMPAPIRequestError
            If there's no such publication (404).

        """
        data: PublicationUpdateRequest = {"enabled": enabled, "publicPort": public_port}
        # We only send what changes, as the web panel does.
        result: PublicationResponse = await self._request(
            method="PUT",
            path=f"/api/networking/publications/{publication_id}",
            data=self._without_none(mapping=data),
        )
        return self._publication_enums(publication=result)
