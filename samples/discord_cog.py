# Copyright (C) 2021-2026 Katelynn Cadwallader. Part of AMPAPI_Python, under the GPL v3 (see LICENSE).
# ruff: noqa: INP001 # the samples are scripts run directly, not a package
# pyright: basic
# pyright: reportMissingImports=false
# discord.py isn't one of this library's dependencies, so pyright can't see it, hence basic mode.
"""A sketch of a discord.py cog that posts each shard's state changes to a channel.

It needs discord.py, which this library doesn't depend on: `pip install discord.py`.

The bot holds the one `Panel`, so the panel outlives the cog. The cog adds its listener in `cog_load` and removes it in
`cog_unload`, so reloading the cog doesn't leave its old listener behind. Set the panel's URL, a login, the bot's token
and the channel to post in, then run it:

    AMP_URL=... AMP_USER=... AMP_PASSWORD=... DISCORD_TOKEN=... DISCORD_CHANNEL=<channel ID> python samples/discord_cog.py
"""

from __future__ import annotations

import os
from typing import Union

import discord
from discord.ext import commands

from ampapi import Panel, Session, Shard, ShardState, ShardStatus


class AMPBot(commands.Bot):
    """A bot holding one AMP panel for its cogs."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
        session = Session(url=os.environ["AMP_URL"], username=os.environ["AMP_USER"], password=os.environ["AMP_PASSWORD"])
        self.panel: Panel = Panel(session=session)

    async def setup_hook(self) -> None:
        """Start listening to AMP, then load the cog."""
        # With no list, the panel subscribes every shard and spire it can see, and follows new ones too.
        await self.panel.add_subscribers()
        await self.panel.start_listening()
        await self.add_cog(ShardStates(bot=self))

    async def close(self) -> None:
        """Stop the hubs and log out of AMP, then close the bot."""
        await self.panel.clean_up()
        await super().close()


class ShardStates(commands.Cog):
    """Posts each shard's state changes to one channel."""

    def __init__(self, bot: AMPBot) -> None:  # noqa: D107
        self.bot: AMPBot = bot
        self.channel_id: int = int(os.environ["DISCORD_CHANNEL"])
        # The last status we posted for each shard, as AMP sends the state again when only its heartbeat moved.
        self.posted: dict[str, Union[ShardState, int]] = {}
        # `remove_listener` needs the same object `add_listener` was given, and each `self.on_shard_state` is a new one.
        self.listener = self.on_shard_state

    async def cog_load(self) -> None:
        """Add our listener to the bot's panel."""
        self.bot.panel.add_listener(self.listener, "state")

    async def cog_unload(self) -> None:
        """Take our listener off the bot's panel, which carries on for the rest of the bot."""
        self.bot.panel.remove_listener(self.listener, "state")

    async def on_shard_state(self, panel: Panel, data: ShardStatus) -> None:
        """Post a shard's new status. Like any listener added to the panel, it gets the panel first, then the state."""
        previous: Union[ShardState, int, None] = self.posted.get(data.shard_id)
        self.posted[data.shard_id] = data.status
        # The first state we see for a shard is where it already was, so only the ones after it are changes.
        if previous is None or previous == data.status:
            return

        channel = self.bot.get_channel(self.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        shard: Shard = await panel.get_shard(shard_id=data.shard_id)
        status: str = data.status.name if isinstance(data.status, ShardState) else str(data.status)
        # A state change isn't worth a notification, so we post it silently.
        await channel.send(content=f"**{shard.display_name}** is now `{status}`.", silent=True)


if __name__ == "__main__":
    AMPBot().run(os.environ["DISCORD_TOKEN"])
