"""
Entry point for the Discord Economy Bot.

Loads config, sets up the bot, connects to the database, loads all
cogs in ./cogs, and syncs the slash command tree on startup.
"""

import asyncio
import logging

import discord
from discord.ext import commands

from config import DISCORD_TOKEN, COMMAND_PREFIX
from utils.database import Database

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("economy-bot")

INITIAL_COGS = [
    "cogs.economy",
]


class EconomyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # only needed if you add prefix commands
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents)
        self.db = Database("economy.db")

    async def setup_hook(self):
        await self.db.connect()
        for cog in INITIAL_COGS:
            await self.load_extension(cog)
            log.info("Loaded cog: %s", cog)

        # Sync slash commands globally. For faster iteration during
        # development, sync to a single guild instead:
        # self.tree.copy_global_to(guild=discord.Object(id=YOUR_GUILD_ID))
        # await self.tree.sync(guild=discord.Object(id=YOUR_GUILD_ID))
        synced = await self.tree.sync()
        log.info("Synced %d slash command(s)", len(synced))

    async def close(self):
        await self.db.close()
        await super().close()


bot = EconomyBot()


@bot.event
async def on_ready():
    log.info("Logged in as %s (ID: %s)", bot.user, bot.user.id)


def main():
    if not DISCORD_TOKEN:
        raise SystemExit(
            "DISCORD_TOKEN is not set. Copy .env.example to .env and add your bot token."
        )
    asyncio.run(bot.start(DISCORD_TOKEN))


if __name__ == "__main__":
    main()
