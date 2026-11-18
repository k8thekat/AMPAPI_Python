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
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from ._types import BusExpandResponse, SetupAdminRequest, SetupNetworkResponse, SetupProvisionStatusResponse, TokenResponse

__all__ = ("SetupModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class SetupModule(Base):
    """The calls for a fresh panel's first-run setup, which turn a new AMP install into a panel with an admin.

    The setup's calls run in this order:

    - :meth:`check_setup_code`, so a wrong setup code is caught before the first real step.
    - :meth:`provision_message_bus`, then :meth:`get_provision_status` until `step` reads ``"done"``.
    - :meth:`PlatformModule.get_health_status` until `phase` reads ``"setup-admin"``. The health reads ``"starting"``
      for a few seconds first.
    - :meth:`create_admin`, which logs the `Session` in as the admin and deletes the setup code.
    - Optionally, :meth:`get_setup_network`, then :meth:`expand_setup_network` when other machines will join the panel.

    The setup code comes from ``setup-token.txt`` in AMP's data folder (``/opt/cubecoders/amp3/data``), or from the
    installer's output. The calls before the admin exists need no login, so the module works on a `Session` alone,
    eg. ``SetupModule(session=session)``, before there's an account to log in as.

    .. warning::
        AMP locks the caller's IP address out after 10 wrong setup codes. During the lockout AMP refuses every setup
        code from that IP address for about 15 minutes, the right setup code included. The library never sends a
        refused setup code again. Don't retry a refused setup code in a loop either.

    .. versionadded:: 6.0.0

    """

    async def check_setup_code(self, code: str) -> None:
        """Check the setup code a fresh panel's first-run setup needs.

        |coro|

        Endpoint: ``GET /api/auth/setup/code``

        This call needs no login. See :class:`SetupModule` for the order of the first-run setup's calls.

        .. warning::
            AMP locks the caller's IP address out after 10 wrong setup codes.

            - Each wrong setup code counts toward the lockout.
            - During the lockout AMP refuses every setup code from the caller's IP address for about 15 minutes, the right
              setup code included.
            - The library never sends a refused setup code again. Don't retry a refused setup code in a loop either.

        Parameters
        ----------
        code : :class:`str`
            The setup code from ``setup-token.txt`` in AMP's data folder (``/opt/cubecoders/amp3/data``), or from the
            installer's output. Whitespace around the code, eg. the file's trailing newline, is dropped.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the setup code is wrong `auth.setup.code.invalid`. The wrong code counts toward the lockout.\n
            **429** - If AMP locked the caller's IP address out after 10 wrong setup codes `auth.setup.code.throttled`.
            AMP sends no ``Retry-After`` header. The lockout lifts after about 15 minutes.\n
            **503** - If setup has finished `auth.setup.code.unavailable`. :meth:`create_admin` deletes the setup code,
            so this 503 isn't an outage and the library doesn't send the call again. Running ``amp3-host reset-setup`` on
            the panel's machine makes a new setup code.
        ValueError
            If `code` is empty or only whitespace. Nothing is sent.

        """
        await self._request(method="GET", path="/api/auth/setup/code", use_token=False, setup_code=code)

    async def create_admin(self, code: str, email: str) -> TokenResponse:
        """Make the panel's first admin, which logs the `Session` in as the admin.

        |coro|

        Endpoint: ``POST /api/auth/setup/admin``

        This call needs no login. See :class:`SetupModule` for the order of the first-run setup's calls.

        - The admin gets the `Session`'s `username` and password.
        - The `Session` keeps the admin's token, so a :class:`Panel` made on the `Session` works at once.
        - Creating the admin deletes the setup code. Every call that needs the setup code raises a 503
          `auth.setup.code.unavailable` from then on.
        - The health `phase` then reads ``"preview-licence"`` on a preview build, or ``"ready"`` on a release build.

        .. warning::
            Call :meth:`create_admin` once :meth:`PlatformModule.get_health_status` reads ``"setup-admin"``. Right after
            :meth:`get_provision_status` reads ``"done"``, the health reads ``"starting"`` for a few seconds.

        .. warning::
            AMP locks the caller's IP address out after 10 wrong setup codes.

            - Each wrong setup code counts toward the lockout.
            - During the lockout AMP refuses every setup code from the caller's IP address for about 15 minutes, the right
              setup code included.
            - The library never sends a refused setup code again. Don't retry a refused setup code in a loop either.

        Parameters
        ----------
        code : :class:`str`
            The setup code from ``setup-token.txt`` in AMP's data folder (``/opt/cubecoders/amp3/data``), or from the
            installer's output. Whitespace around the code, eg. the file's trailing newline, is dropped.
        email : :class:`str`
            The admin's email address.

        Returns
        -------
        :class:`TokenResponse`
            The admin's session token, which the `Session` keeps.

        Raises
        ------
        AMPAPIRequestError
            **400** - If the `Session`'s password doesn't pass :meth:`Session.get_password_policy`. The error's `errors`
            lists each rule the password breaks. AMP undoes the step, so the same setup code works again with a
            :class:`Session` made with a stronger password.\n
            **403** - If the setup code is wrong `auth.setup.code.invalid`. The wrong code counts toward the lockout.\n
            **409** - If the panel has an admin already and ``amp3-host reset-setup`` made a new setup code. AMP makes
            no second admin.\n
            **429** - If AMP locked the caller's IP address out after 10 wrong setup codes `auth.setup.code.throttled`.\n
            **503** - If AMP's message bus isn't set up yet, see :meth:`provision_message_bus`.\n
            **503** - If AMP can't reach the message bus, or the message bus has no storage for the account, from AMP's
            docs and not seen live.\n
            **503** - If the panel has an admin already `auth.setup.code.unavailable`. Creating the admin deleted the
            setup code, so this 503 isn't an outage and the library doesn't send the call again.
        ValueError
            If `code` is empty or only whitespace. Nothing is sent.

        """
        data: SetupAdminRequest = {
            "username": self.session.username,
            "email": email,
            "password": self.session._password,  # pyright: ignore[reportPrivateUsage]
        }
        body: TokenResponse = await self._request(method="POST", path="/api/auth/setup/admin", data=data, use_token=False, setup_code=code)
        LOGGER.debug("<%s.%s> | Username: %s", __class__.__name__, "create_admin", self.session.username)

        # The admin's token is a login, so the `Session` keeps it as one and needs no second login
        return await self.session._login_result(data=body)  # pyright: ignore[reportPrivateUsage]

    async def expand_setup_network(self) -> BusExpandResponse:
        """Open the message bus to other machines, as the first-run setup's network step does.

        |coro|

        Endpoint: ``POST /api/auth/setup/network/expand``

        This call does the same as :meth:`EnrollmentModule.expand_message_bus`, through the first-run setup's route. Use
        this call during the first-run setup, and :meth:`EnrollmentModule.expand_message_bus` once the panel is set up.
        The setup code isn't needed: the call uses the `Session`'s login, eg. the admin's from :meth:`create_admin`. The
        web panel only calls this route when the admin says other machines will join the panel.

        - AMP opens the message bus's port (TCP 4222 unless the spire's `busPort` says otherwise) on the host's
          firewall. Nothing restarts.
        - The message bus's `servers` move from ``127.0.0.1`` to the machine's network address.
        - Calling :meth:`expand_setup_network` again on an open message bus answers the same.

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
        return await self._request(method="POST", path="/api/auth/setup/network/expand")

    async def get_provision_status(self, code: str) -> SetupProvisionStatusResponse:
        """Get how far :meth:`provision_message_bus` has got.

        |coro|

        Endpoint: ``GET /api/auth/setup/database/provision/status``

        This call needs no login. See :class:`SetupModule` for the order of the first-run setup's calls.

        - The web panel polls the provision status every half second.
        - Once `step` reads ``"done"``, :meth:`PlatformModule.get_health_status` reads ``"starting"`` for a few seconds,
          then ``"setup-admin"``. Wait for ``"setup-admin"`` before :meth:`create_admin`.
        - If AMP restarts while it sets up the message bus, `step` reads ``"idle"`` again. A health `phase` of
          ``"setup-admin"`` then means the message bus is set up all the same.

        .. warning::
            AMP locks the caller's IP address out after 10 wrong setup codes.

            - Each wrong setup code counts toward the lockout.
            - During the lockout AMP refuses every setup code from the caller's IP address for about 15 minutes, the right
              setup code included.
            - The library never sends a refused setup code again. Don't retry a refused setup code in a loop either.

        Parameters
        ----------
        code : :class:`str`
            The setup code from ``setup-token.txt`` in AMP's data folder (``/opt/cubecoders/amp3/data``), or from the
            installer's output. Whitespace around the code, eg. the file's trailing newline, is dropped.

        Returns
        -------
        :class:`SetupProvisionStatusResponse`
            The step AMP is on, and how far through the step AMP is.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the setup code is wrong `auth.setup.code.invalid`. The wrong code counts toward the lockout.\n
            **409** - If setup has finished and ``amp3-host reset-setup`` made a new setup code.\n
            **429** - If AMP locked the caller's IP address out after 10 wrong setup codes `auth.setup.code.throttled`.\n
            **503** - If setup has finished `auth.setup.code.unavailable`. :meth:`create_admin` deletes the setup code,
            so this 503 isn't an outage and the library doesn't send the call again.
        ValueError
            If `code` is empty or only whitespace. Nothing is sent.

        """
        return await self._request(method="GET", path="/api/auth/setup/database/provision/status", use_token=False, setup_code=code)

    async def get_setup_network(self) -> SetupNetworkResponse:
        """Get how the panel's machine reaches the internet, and if other machines can join the message bus.

        |coro|

        Endpoint: ``GET /api/auth/setup/network``

        The first-run setup's network step calls this route once the admin exists, and the call works any time after
        that too. The setup code isn't needed: the call uses the `Session`'s login, eg. the admin's from
        :meth:`create_admin`.

        - The call changes nothing.
        - AMP runs a traceroute and looks up the public address, so the call takes a few seconds.
        - AMP keeps the result for a short while, from AMP's docs.

        Returns
        -------
        :class:`SetupNetworkResponse`
            How the machine reaches the internet, if AMP runs the message bus, and if the message bus is open already.
            :meth:`expand_setup_network` opens the message bus.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the logged in user lacks the spire-create capability, from AMP's docs and not seen live.

        """
        return await self._request(method="GET", path="/api/auth/setup/network")

    async def provision_message_bus(self, code: str) -> None:
        """Have AMP set up its own message bus, the first-run setup's database step.

        |coro|

        Endpoint: ``POST /api/auth/setup/database/provision``

        This call needs no login. See :class:`SetupModule` for the order of the first-run setup's calls.

        - AMP sets up the message bus in the background and answers at once. Poll :meth:`get_provision_status` until
          `step` reads ``"done"``.
        - Calling :meth:`provision_message_bus` again while AMP sets up the message bus answers the same, and starts
          nothing new.
        - After a provisioning that failed (`step` reads ``"error"``), :meth:`provision_message_bus` can be called again.
        - The message bus starts open to the panel's machine only. :meth:`expand_setup_network` opens the message bus
          to other machines once the admin exists.

        .. warning::
            AMP locks the caller's IP address out after 10 wrong setup codes.

            - Each wrong setup code counts toward the lockout.
            - During the lockout AMP refuses every setup code from the caller's IP address for about 15 minutes, the right
              setup code included.
            - The library never sends a refused setup code again. Don't retry a refused setup code in a loop either.

        Parameters
        ----------
        code : :class:`str`
            The setup code from ``setup-token.txt`` in AMP's data folder (``/opt/cubecoders/amp3/data``), or from the
            installer's output. Whitespace around the code, eg. the file's trailing newline, is dropped.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the setup code is wrong `auth.setup.code.invalid`. The wrong code counts toward the lockout.\n
            **409** - If AMP's message bus is already set up.\n
            **429** - If AMP locked the caller's IP address out after 10 wrong setup codes `auth.setup.code.throttled`.\n
            **503** - If setup has finished `auth.setup.code.unavailable`. :meth:`create_admin` deletes the setup code,
            so this 503 isn't an outage and the library doesn't send the call again. A new setup code from
            ``amp3-host reset-setup`` gets the 409 instead.
        ValueError
            If `code` is empty or only whitespace. Nothing is sent.

        """
        await self._request(method="POST", path="/api/auth/setup/database/provision", use_token=False, setup_code=code)
