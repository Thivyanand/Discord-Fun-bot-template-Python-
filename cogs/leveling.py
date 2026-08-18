import random
from datetime import datetime, timedelta, timezone

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.database import xp_for_level


class Leveling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cooldowns = {}

    @property
    def db(self):
        return self.bot.db

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        now = datetime.now(timezone.utc)
        last = self.cooldowns.get(message.author.id)
        if last and now - last < timedelta(seconds=config.XP_COOLDOWN_SECONDS):
            return

        self.cooldowns[message.author.id] = now
        amount = random.randint(config.XP_MIN, config.XP_MAX)
        new_level, leveled_up = await self.db.add_xp(message.author.id, amount)

        if leveled_up:
            await message.channel.send(
                f"🎉 {message.author.mention} leveled up to **Level {new_level}**!"
            )

    @app_commands.command(name="rank", description="Check your (or someone else's) level and XP.")
    @app_commands.describe(member="The user to check. Defaults to yourself.")
    async def rank(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        row = await self.db.get_user(member.id)
        needed = xp_for_level(row["level"])

        embed = discord.Embed(
            title=f"{member.display_name}'s Rank",
            color=discord.Color.blue(),
        )
        embed.add_field(name="Level", value=str(row["level"]), inline=True)
        embed.add_field(name="XP", value=f"{row['xp']} / {needed}", inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="See the top-ranked users in the server.")
    async def leaderboard(self, interaction: discord.Interaction):
        rows = await self.db.get_leaderboard(limit=10)

        if not rows:
            await interaction.response.send_message("No one has earned any XP yet!")
            return

        lines = []
        for i, row in enumerate(rows, start=1):
            user = interaction.guild.get_member(row["user_id"]) if interaction.guild else None
            name = user.display_name if user else f"User {row['user_id']}"
            lines.append(f"**{i}.** {name} — Level {row['level']} ({row['xp']} XP)")

        embed = discord.Embed(
            title="🏆 XP Leaderboard",
            description="\n".join(lines),
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Leveling(bot))
