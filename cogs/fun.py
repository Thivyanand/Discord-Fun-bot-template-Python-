import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

import config

EIGHTBALL_RESPONSES = [
    "It is certain.",
    "Without a doubt.",
    "You may rely on it.",
    "Yes, definitely.",
    "It is decidedly so.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful.",
]


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question.")
    @app_commands.describe(question="Your question for the 8-ball.")
    async def eightball(self, interaction: discord.Interaction, question: str):
        answer = random.choice(EIGHTBALL_RESPONSES)
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=answer, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="meme", description="Get a random meme.")
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            async with self.session.get(config.MEME_API_URL) as resp:
                data = await resp.json()
        except Exception:
            await interaction.followup.send("Couldn't fetch a meme right now, try again later.")
            return

        embed = discord.Embed(
            title=data.get("title", "Meme"),
            url=data.get("postLink"),
            color=discord.Color.orange(),
        )
        embed.set_image(url=data.get("url"))
        embed.set_footer(text=f"👍 {data.get('ups', 0)} · r/{data.get('subreddit', 'memes')}")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="joke", description="Get a random joke.")
    async def joke(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            async with self.session.get(config.JOKE_API_URL) as resp:
                data = await resp.json()
        except Exception:
            await interaction.followup.send("Couldn't fetch a joke right now, try again later.")
            return

        setup = data.get("setup", "Why did the chicken cross the road?")
        punchline = data.get("punchline", "To get to the other side.")
        embed = discord.Embed(
            title=setup,
            description=punchline,
            color=discord.Color.green(),
        )
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="coinflip", description="Flip a coin.")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        await interaction.response.send_message(f"🪙 The coin landed on **{result}**!")

    @app_commands.command(name="roll", description="Roll a dice.")
    @app_commands.describe(sides="Number of sides on the dice. Defaults to 6.")
    async def roll(self, interaction: discord.Interaction, sides: int = 6):
        if sides < 2:
            await interaction.response.send_message("A dice needs at least 2 sides.", ephemeral=True)
            return
        result = random.randint(1, sides)
        await interaction.response.send_message(f"🎲 You rolled a **{result}** (1-{sides}).")


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
