# Copyright (C) 2021-2026 Katelynn Cadwallader. Part of AMPAPI_Python, under the GPL v3 (see LICENSE).
# ruff: noqa: INP001 # the samples are scripts run directly, not a package
"""Log in, list the spires and shards, read one shard's state, then log out.

With the library installed, set the panel's URL and a login in the environment and run it:

    AMP_URL=http://192.168.1.10:8443 AMP_USER=admin AMP_PASSWORD=... python samples/basic.py
"""

from __future__ import annotations

import asyncio
import os
from typing import Union

from ampapi import Panel, Session, Shard, ShardState, ShardStatus, Spire


async def main() -> None:
    """List what the panel holds and read the first shard's state."""
    # The Session logs in on the first call that needs it, and renews the token on its own.
    session = Session(url=os.environ["AMP_URL"], username=os.environ["AMP_USER"], password=os.environ["AMP_PASSWORD"])

    # Leaving the `async with` block logs out and closes the session, the same as `await panel.clean_up()`.
    async with Panel(session=session) as panel:
        # A spire is AMP 3's name for an ADS or a Target.
        spires: list[Spire] = await panel.get_spires()
        for spire in spires:
            print(f"Spire: {spire.display_name} | ID: {spire.id} | Container Mode: {spire.data['defaultContainerMode']}")

        # A shard is AMP 3's name for an Instance.
        shards: list[Shard] = await panel.get_shards()
        for shard in shards:
            print(f"Shard: {shard.display_name} | ID: {shard.id} | Template: {shard.data['templateSlug']}")

        if not shards:
            print("This panel has no shards yet.")
            return

        # A shard's methods call the panel's with its ID filled in, so this is `panel.get_shard_state(shard_id=...)`.
        state: ShardStatus = await shards[0].get_state()
        # `status` is a `ShardState`, or a plain number for a state this library doesn't know yet.
        status: Union[ShardState, int] = state.status
        status_name: str = status.name if isinstance(status, ShardState) else str(status)
        print(f"{shards[0].display_name} is {status_name} | Running: {state.is_running} | Started At: {state.started_at}")


if __name__ == "__main__":
    asyncio.run(main())
