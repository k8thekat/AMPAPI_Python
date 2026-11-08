# Copyright (C) 2021-2026 Katelynn Cadwallader. Part of AMPAPI_Python, under the GPL v3 (see LICENSE).
# ruff: noqa: INP001 # the samples are scripts run directly, not a package
"""Start a shard, wait for it to run, send a console command, read the console back, then stop it.

The shard's game has to be installed first (`panel.update_shard(shard_id=...)`), as a shard that was never updated
fails its start. With the library installed, set the panel's URL, a login and the shard's ID, then run it:

    AMP_URL=http://192.168.1.10:8443 AMP_USER=admin AMP_PASSWORD=... AMP_SHARD=<shard ID> python samples/shard_control.py
"""

from __future__ import annotations

import asyncio
import os

from ampapi import ConsoleHistory, Panel, Session, Shard, ShardState, ShardStatus

# Most games take `say`, so change it to suit yours.
COMMAND: str = "say Hello from AMPAPI_Python"


async def wait_for_status(shard: Shard, statuses: tuple[ShardState, ...]) -> ShardStatus:
    """Check the shard's state every 2 seconds until it reads one of `statuses`.

    AMP answers a start or a stop before the game has done it, so we follow it with the shard's state. We ask AMP each
    time, which works on any shard object. A shard got with `auto_state=True` keeps `shard.state` current from AMP's live
    events instead, at the cost of a hub socket.

    Raises
    ------
    TimeoutError
        If the shard doesn't get there within 5 minutes.

    """
    async with asyncio.timeout(300):
        while True:
            state: ShardStatus = await shard.get_state()
            if state.status in statuses:
                return state
            await asyncio.sleep(2)


async def main() -> None:
    """Run the shard through a start, a console command and a stop."""
    session = Session(url=os.environ["AMP_URL"], username=os.environ["AMP_USER"], password=os.environ["AMP_PASSWORD"])

    async with Panel(session=session) as panel:
        shard: Shard = await panel.get_shard(shard_id=os.environ["AMP_SHARD"])
        state: ShardStatus = await shard.get_state()
        if state.is_running is True:
            print(f"{shard.display_name} is already running.")
        else:
            print(f"Starting {shard.display_name}...")
            await shard.start()
            state = await wait_for_status(shard=shard, statuses=(ShardState.running_ready, ShardState.failed_startup))

        if state.status == ShardState.failed_startup:
            print(f"{shard.display_name} failed to start: {state.last_error_message}")
            return

        print(f"{shard.display_name} is running. Sending: {COMMAND}")
        await shard.send_console(command=COMMAND)
        # The game answers in its own time, so we give it a moment before reading the console.
        await asyncio.sleep(3)

        # The newest lines, oldest first. `before_seq` pages further back.
        history: ConsoleHistory = await shard.get_console_history(limit=15)
        for line in history.lines:
            print(f"[{line.stream_id}] {line.text}")

        print(f"Stopping {shard.display_name}...")
        await shard.stop()
        await wait_for_status(shard=shard, statuses=(ShardState.stopped,))
        print(f"{shard.display_name} has stopped.")


if __name__ == "__main__":
    asyncio.run(main())
