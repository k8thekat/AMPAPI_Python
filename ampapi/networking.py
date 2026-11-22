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
        FirewallResponse,
        GatewayEgressRequest,
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

    # TODO: Trim the note and the warning once AMP fixes the gateway status gaps and keeps the publications (U26b, U26e, U31).
    # As of AMP 3.0.2 a running shard still routes only after it restarts, and a new tunnel reads `Fault` while it connects.
    # As of AMP 3.0.2 making the gateway still deletes the shard's publications.
    async def create_gateway(self, shard_id: str, front_spire_id: str) -> GatewayResponse:
        """Route a shard through a front spire, so players reach it at that spire's address.

        |coro|

        Endpoint: ``POST /api/networking/gateways``

        A gateway is the shard's route over a WireGuard tunnel between its spire and the front spire, which AMP sets up
        itself (see :meth:`get_tunnels`). The shard gets an `address` on that tunnel, eg. ``"10.83.0.10"``, and an
        `egressAllowList` (see :meth:`set_gateway_egress`). Once the gateway routes, the shard answers on the front
        spire's address at the shard's own port. Follow the gateway with :meth:`get_gateways`.

        .. warning::
            AMP deletes the shard's publications (:meth:`create_publication`) when it makes the gateway, as the gateway
            carries all of the shard's ports, and the reply doesn't say so.

        .. note::
            - A shard that was running before the gateway only routes once the shard restarts. Until then the gateway
              reads `GatewayState.awaiting_shard` with `runningWithoutRoute`, though the shard's endpoint already lists
              the front spire's address.
            - A new gateway also reads `GatewayState.fault` while its tunnel connects.
            - A start or restart of the shard with the gateway in place waits for the route. Meanwhile the shard's
              `ShardStatus.status` reads `ShardState.pre_start` and its `ShardStatus.status_code` reads
              ``"agent.msg.gatewayConnecting"``. The shard then runs with the gateway `GatewayState.active`.

        Parameters
        ----------
        shard_id : :class:`str`
            The shard's ID.
        front_spire_id : :class:`str`
            The front spire's ID. The front spire needs its ``"spire.publicHost"`` setting set, see
            :meth:`SpireModule.set_spire_settings`.

        Returns
        -------
        :class:`GatewayResponse`
            The gateway AMP made (201), its `status` `None` until AMP has set the route up.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the front spire doesn't exist or has no public host `networking.error.frontNotRoutable`.\n
            **400** - If the shard already runs on the front spire `networking.error.gatewaySameSpire`.\n
            **409** - If the shard already has a gateway. A shard has one gateway at most.\n
            :meth:`preflight_gateway` catches none of these.

        """
        data: GatewayRequest = {"shardId": shard_id, "frontSpireId": front_spire_id}
        return await self._request(method="POST", path="/api/networking/gateways", data=data)

    # TODO: Drop the note once AMP stops reading `TunnelFault` while a first tunnel is set up (U26a).
    # As of AMP 3.0.1 it still reads `TunnelFault` for about a minute.
    # Then the publication's `state` reads `Active` by itself.
    async def create_publication(
        self,
        front_spire_id: str,
        public_port: int,
        shard_id: str,
        port_reference: str,
        *,
        front_public_host: Optional[str] = None,
    ) -> PublicationResponse:
        """Forward a public port on a front spire to a shard's port.

        |coro|

        Endpoint: ``POST /api/networking/publications``

        Through another spire, AMP sets up a WireGuard tunnel between the two spires (see :meth:`get_tunnels`), and the
        forward works once :meth:`get_publications` reads the publication as `PublicationState.active`. The protocol is
        always the shard port's own protocol.

        .. note::
            A first publication's `state` through another spire can read `PublicationState.tunnel_fault` with
            ``"The file does not exist."`` for about a minute, while the tunnel's agent is put in place. The `state`
            then reads `PublicationState.active` by itself.

        Parameters
        ----------
        front_spire_id : :class:`str`
            The front spire's ID. The shard's own spire works as it is; another spire needs a public host, either its
            ``"spire.publicHost"`` setting (see :meth:`SpireModule.set_spire_settings`) or `front_public_host`.
        public_port : :class:`int`
            The port players connect to, 1 to 65535. A front spire forwards each port once, and ``"Both"`` counts as
            TCP and UDP.
        shard_id : :class:`str`
            The shard's ID. A shard routed through a gateway can't have publications, see :meth:`create_gateway`.
        port_reference : :class:`str`
            The shard port's `ref`, eg. ``"ServerPort"``, see :meth:`ShardModule.get_shard_ports`. The port has to be
            marked publicly reachable in the shard's ports.
        front_public_host : Union[:class:`str`, None], optional
            A public host for the front spire, eg. ``"amp.example.com"``, by default None. A front spire without a
            public host keeps this host as its ``"spire.publicHost"`` setting; a front spire that already has a public
            host ignores it.

        Returns
        -------
        :class:`PublicationResponse`
            The publication AMP made (201), turned on, with the `protocol` of the shard's port and `status` `None`.

        Raises
        ------
        AMPAPIRequestError
            AMP checks the front spire first, then the port and the shard, in this order.\n
            **400** - If the front is another spire with no public host and no `front_public_host`
            `networking.error.frontNoPublicHost`.\n
            **400** - If `front_public_host` isn't a bare host `spire.error.invalidPublicHost`.\n
            **400** - If `public_port` isn't a port number `networking.error.invalidPort`.\n
            **400** - If the shard has no port named `port_reference` `networking.error.portRefMissing`.\n
            **409** - If the shard is routed through a gateway.\n
            **409** - If the front spire already forwards `public_port`.

        """
        data: PublicationRequest = {
            "frontSpireId": front_spire_id,
            "publicPort": public_port,
            "shardId": shard_id,
            "portRef": port_reference,
        }

        # Left out, AMP uses the front spire's own public host
        if front_public_host is not None:
            data["frontPublicHost"] = front_public_host

        return await self._request(method="POST", path="/api/networking/publications", data=data)

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
            **404** - If there's no gateway with that ID, eg. the gateway was removed already.

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
            **404** - If there's no publication with that ID, eg. the publication was removed already.

        """
        await self._request(method="DELETE", path=f"/api/networking/publications/{publication_id}")

    async def get_firewall(self) -> FirewallResponse:
        """Get the firewall rules AMP keeps on the host.

        |coro|

        Endpoint: ``GET /api/networking/firewall``

        It is the panel's own spire's firewall, as AMP's system agent last applied it; another spire's can't be read.

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

    async def get_gateways(self) -> list[GatewayResponse]:
        """Get the gateways, each a shard's route through a front spire, see :meth:`create_gateway`.

        |coro|

        Endpoint: ``GET /api/networking/gateways``

        Returns
        -------
        list[:class:`GatewayResponse`]
            The gateways, each `status.state` a :class:`GatewayState` value as AMP sends it.

        """
        return await self._request(method="GET", path="/api/networking/gateways")

    async def get_publications(self) -> list[PublicationResponse]:
        """Get the public port forwards from front spires to shards.

        |coro|

        Endpoint: ``GET /api/networking/publications``

        Returns
        -------
        list[:class:`PublicationResponse`]
            The publications, each `status.state` a :class:`PublicationState` value as AMP sends it.

        """
        return await self._request(method="GET", path="/api/networking/publications")

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

        AMP makes a tunnel on demand for a publication or a gateway through another spire, with addresses such as
        ``"10.83.0.1"`` (the front) and ``"10.83.0.2"`` (the back), and removes the tunnel some seconds after it's no
        longer needed.

        Returns
        -------
        list[:class:`TunnelResponse`]
            The tunnels.

        """
        return await self._request(method="GET", path="/api/networking/tunnels")

    # TODO: Trim the warning once AMP's preflight checks what the create checks (U20b, U20c).
    # As of AMP 3.0.1 it still passes an empty body, a gateway on the shard's own spire and a front spire with no public host.
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

    async def set_gateway_egress(self, gateway_id: str, allow_list: list[str]) -> GatewayResponse:
        """Set which private networks a shard routed through a gateway may reach.

        |coro|

        Endpoint: ``PUT /api/networking/gateways/{gateway_id}/egress``

        A gateway sends all of the shard's traffic through the front spire, and the front spire drops anything bound for
        a private network by default (10/8, 172.16/12, 192.168/16, 100.64/10, 169.254/16 and loopback). This allow list
        is the exception. The front spire's own services aren't covered by the list: a service the front spire serves
        on its network address stays reachable unless the front spire's firewall says otherwise.

        Parameters
        ----------
        gateway_id : :class:`str`
            The gateway's ID, see :meth:`get_gateways`.
        allow_list : list[:class:`str`]
            IPv4 networks in CIDR form, no wider than a /8, eg. ``["192.168.4.0/24"]``, at most 32 networks. The list
            replaces the gateway's old list, and an empty list leaves the shard the internet only.

        Returns
        -------
        :class:`GatewayResponse`
            The gateway, with its new `egressAllowList`.

        Raises
        ------
        AMPAPIRequestError
            **400** - If a network is wider than a /8 `networking.error.egressTooWide`. AMP also audits the attempt as
            a security event.\n
            **400** - If an entry isn't an IPv4 network in CIDR form, eg. an IPv6 network or a bare address
            `networking.error.egressNotCidr`.\n
            **404** - If there's no gateway with that ID.

        """
        data: GatewayEgressRequest = {"egressAllowList": allow_list}
        return await self._request(method="PUT", path=f"/api/networking/gateways/{gateway_id}/egress", data=data)

    # TODO: Drop the old status sentence once AMP answers with the new one (U26c).
    # As of AMP 3.0.1 a publication turned off is still answered with its old `Active` status.
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
            **404** - If there's no publication with that ID.

        """
        data: PublicationUpdateRequest = {"enabled": enabled, "publicPort": public_port}
        # We only send what changes, as the web panel does.
        return await self._request(
            method="PUT",
            path=f"/api/networking/publications/{publication_id}",
            data=self._without_none(mapping=data),
        )
