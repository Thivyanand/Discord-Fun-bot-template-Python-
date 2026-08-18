import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

XP_MIN = 10
XP_MAX = 25
XP_COOLDOWN_SECONDS = 60

MEME_API_URL = "https://meme-api.com/gimme"
TRIVIA_API_URL = "https://opentdb.com/api.php"
JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"
