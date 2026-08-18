# Discord Fun & Engagement Bot (Template)

A small, hackable Discord bot built with [discord.py](https://discordpy.readthedocs.io/), focused on fun commands and server engagement (leveling, trivia, memes). Meant as a starting point for open-source contributions.

## Features

- 🧠 Trivia with interactive buttons (`/trivia`)
- 📈 XP/leveling system from chatting, with level-up announcements
- 🏆 Rank card and leaderboard (`/rank`, `/leaderboard`)
- 😂 Random memes (`/meme`)
- 🃏 Random jokes (`/joke`)
- 🎱 Magic 8-ball (`/8ball`)
- 🪙 Coinflip and dice roll (`/coinflip`, `/roll`)

## Setup

1. **Clone the repo and install dependencies**

   ```bash
   git clone <your-fork-url>
   cd fun-bot
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create a bot application**

   - Go to the [Discord Developer Portal](https://discord.com/developers/applications), create an application, and add a bot user.
   - Under **Bot**, enable the **Message Content Intent** and **Server Members Intent**.
   - Copy the bot token.
   - Under **OAuth2 > URL Generator**, select the `bot` and `applications.commands` scopes, and invite the bot to your server.

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and paste in your bot token.

4. **Run the bot**

   ```bash
   python bot.py
   ```

   On first run, the bot creates `fun.db` automatically and syncs its slash commands.

## Project structure

```
fun-bot/
├── bot.py               # Entry point — loads cogs, syncs commands
├── config.py             # Env vars + tuning constants (XP rates, API URLs)
├── cogs/
│   ├── fun.py            # 8ball, meme, joke, coinflip, roll
│   ├── leveling.py       # XP gain, rank, leaderboard
│   └── trivia.py         # Interactive trivia questions
├── utils/
│   └── database.py       # Async SQLite wrapper
├── requirements.txt
├── .env.example
└── .gitignore
```

## External APIs used

- [Open Trivia Database](https://opentdb.com/) — trivia questions (no key required)
- [meme-api.com](https://meme-api.com/) — random memes from Reddit (no key required)
- [Official Joke API](https://official-joke-api.appspot.com/) — random jokes (no key required)

## Contributing

Some good first issues for contributors:

- Add a `/poll` command with reaction or button voting
- Add reaction-role support for self-assignable roles
- Add a rank card image generator (using Pillow) instead of a plain embed
- Add per-guild XP settings (rate, cooldown) stored in the DB
- Add a `/giveaway` command with a timed entry window and random winner
- Add unit tests for `utils/database.py`

**Workflow:**

1. Fork the repo and create a branch: `git checkout -b feature/my-feature`
2. Make your changes (keep commands in `cogs/`, DB logic in `utils/database.py`)
3. Test locally against a dev server
4. Open a pull request describing what you changed and why

## License

MIT — do whatever you'd like with this template.
