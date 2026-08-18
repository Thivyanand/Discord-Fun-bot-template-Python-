import html
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

import config


class TriviaView(discord.ui.View):
    def __init__(self, correct_answer: str, author_id: int):
        super().__init__(timeout=30)
        self.correct_answer = correct_answer
        self.author_id = author_id
        self.answered = False

    async def disable_all(self):
        for item in self.children:
            item.disabled = True

    async def handle_answer(self, interaction: discord.Interaction, choice: str, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("This isn't your trivia question.", ephemeral=True)
            return

        if self.answered:
            await interaction.response.send_message("You already answered this question.", ephemeral=True)
            return

        self.answered = True
        await self.disable_all()

        for item in self.children:
            if item.label == self.correct_answer:
                item.style = discord.ButtonStyle.success
            elif item == button and choice != self.correct_answer:
                item.style = discord.ButtonStyle.danger

        if choice == self.correct_answer:
            result_text = "✅ Correct!"
        else:
            result_text = f"❌ Wrong! The correct answer was **{self.correct_answer}**."

        await interaction.response.edit_message(content=result_text, view=self)
        self.stop()

    async def on_timeout(self):
        await self.disable_all()


class Trivia(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    @app_commands.command(name="trivia", description="Answer a random trivia question.")
    async def trivia(self, interaction: discord.Interaction):
        await interaction.response.defer()

        params = {"amount": 1, "type": "multiple"}
        try:
            async with self.session.get(config.TRIVIA_API_URL, params=params) as resp:
                data = await resp.json()
        except Exception:
            await interaction.followup.send("Couldn't fetch a trivia question right now, try again later.")
            return

        results = data.get("results")
        if not results:
            await interaction.followup.send("Couldn't fetch a trivia question right now, try again later.")
            return

        question_data = results[0]
        question = html.unescape(question_data["question"])
        correct = html.unescape(question_data["correct_answer"])
        incorrect = [html.unescape(a) for a in question_data["incorrect_answers"]]

        choices = incorrect + [correct]
        random.shuffle(choices)

        view = TriviaView(correct_answer=correct, author_id=interaction.user.id)
        for choice in choices:
            button = discord.ui.Button(label=choice, style=discord.ButtonStyle.primary)

            async def button_callback(inter: discord.Interaction, b=button, c=choice):
                await view.handle_answer(inter, c, b)

            button.callback = button_callback
            view.add_item(button)

        category = html.unescape(question_data.get("category", "Trivia"))
        difficulty = question_data.get("difficulty", "medium").capitalize()

        embed = discord.Embed(
            title=f"🧠 {category}",
            description=question,
            color=discord.Color.purple(),
        )
        embed.set_footer(text=f"Difficulty: {difficulty}")

        await interaction.followup.send(embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Trivia(bot))
