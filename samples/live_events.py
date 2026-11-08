# Copyright (C) 2021-2026 Katelynn Cadwallader. Part of AMPAPI_Python, under the GPL v3 (see LICENSE).
# ruff: noqa: INP001 # the samples are scripts run directly, not a package
"""Print AMP's live events until Ctrl+C: one shard's console, every shard's state changes and lifecycle, and every task.

It shows both ways to add a listener:
    - class-level, a method marked with `@ShardHub.listener(...)` or `@PanelHub.listener(...)` on a subclass.
    - instance-level, a plain function given to `panel.listen(...)` (or `panel.add_listener(...)`).

Start, stop or update a shard from the web panel while it runs to see the events. With the library installed, set the
panel's URL, a login and the ID of the shard whose console to print, then run it:

    AMP_URL=http://192.168.1.10:8443 AMP_USER=admin AMP_PASSWORD=... AMP_SHARD=<shard ID> python samples/live_events.py
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
from typing import Union

from ampapi import ConsoleLine, LifecycleEvent, Panel, PanelHub, RunningTask, Session, Shard, ShardHub, ShardState, ShardStatus


class MyShard(Shard):
    """Every shard the panel hands out is one of these, as it's the panel's `shard_class`."""

    # AMP's console lines don't say which shard they came from, so a console listener on a shard opens that shard's
    # own hub socket, and hears only that shard.
    @ShardHub.listener(name="console")
    async def on_console(self, data: ConsoleLine) -> None:
        """Print each of this shard's console lines."""
        print(f"[{self.display_name}] {data.text}")


class MyPanel(Panel):
    """The panel's listeners hear the shards and spires it subscribes."""

    def __init__(self, session: Session, *, shard_class: type[Shard] = Shard) -> None:  # noqa: D107
        super().__init__(session=session, shard_class=shard_class)
        # The last status we printed for each shard, as AMP sends the state again when only its heartbeat moved.
        self.printed: dict[str, Union[ShardState, int]] = {}

    @PanelHub.listener(name="state")
    async def on_state(self, data: ShardStatus) -> None:
        """Print a subscribed shard's status when it changes."""
        if self.printed.get(data.shard_id) == data.status:
            return

        self.printed[data.shard_id] = data.status
        status: str = data.status.name if isinstance(data.status, ShardState) else str(data.status)
        print(f"State: {data.shard_id} is now {status}")

    @PanelHub.listener(name="task")
    async def on_task(self, data: RunningTask) -> None:
        """Print each task's progress, eg. a shard's update."""
        # A clone or a move names itself with `name_code` and leaves `name` empty.
        print(f"Task: {data.name or data.name_code} | {data.progress_percent}% | Finished: {data.is_terminal}")


async def main() -> None:
    """Listen until Ctrl+C cancels us, then clean up on the way out."""
    # The hub logs each socket it connects at INFO, which is handy to see here.
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s | %(message)s")
    session = Session(url=os.environ["AMP_URL"], username=os.environ["AMP_USER"], password=os.environ["AMP_PASSWORD"])

    async with MyPanel(session=session, shard_class=MyShard) as panel:
        # The panel only holds its shard objects weakly, so we keep our own reference or the listener goes with it.
        shard: Shard = await panel.get_shard(shard_id=os.environ["AMP_SHARD"])
        print(f"Printing {shard.display_name}'s console.")

        # An instance-level listener is called with the object it was added to, then the event's data.
        @panel.listen("lifecycle")
        async def on_lifecycle(_panel: MyPanel, data: LifecycleEvent) -> None:
            if data.message:
                print(f"Lifecycle: {data.shard_id} | {data.message}")

        # With no list, the panel subscribes every shard and spire it can see, and follows new ones too.
        await panel.add_subscribers()
        # This returns once the hub sockets are up, and they stay up in the background until we clean up.
        await panel.start_listening()
        print("Listening, press Ctrl+C to stop.")
        # Nothing sets this, so we wait here until Ctrl+C.
        await asyncio.Event().wait()


if __name__ == "__main__":
    # Ctrl+C cancels `main`, which logs out as it leaves the `async with`, so the KeyboardInterrupt needs no traceback.
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
