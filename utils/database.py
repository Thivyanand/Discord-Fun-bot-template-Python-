from datetime import datetime, timezone
from typing import Optional

import aiosqlite


def xp_for_level(level: int) -> int:
    return 5 * (level ** 2) + 50 * level + 100


class Database:
    def __init__(self, path: str = "fun.db"):
        self.path = path
        self._conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        self._conn = await aiosqlite.connect(self.path)
        self._conn.row_factory = aiosqlite.Row
        await self._create_tables()

    async def close(self):
        if self._conn:
            await self._conn.close()

    async def _create_tables(self):
        await self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS levels (
                user_id     INTEGER PRIMARY KEY,
                xp          INTEGER NOT NULL DEFAULT 0,
                level       INTEGER NOT NULL DEFAULT 0,
                last_xp_at  TEXT
            )
            """
        )
        await self._conn.commit()

    async def _ensure_user(self, user_id: int):
        await self._conn.execute(
            "INSERT OR IGNORE INTO levels (user_id) VALUES (?)", (user_id,)
        )
        await self._conn.commit()

    async def get_user(self, user_id: int) -> aiosqlite.Row:
        await self._ensure_user(user_id)
        cursor = await self._conn.execute(
            "SELECT * FROM levels WHERE user_id = ?", (user_id,)
        )
        return await cursor.fetchone()

    async def add_xp(self, user_id: int, amount: int):
        await self._ensure_user(user_id)
        row = await self.get_user(user_id)
        new_xp = row["xp"] + amount
        new_level = row["level"]
        leveled_up = False

        while new_xp >= xp_for_level(new_level):
            new_xp -= xp_for_level(new_level)
            new_level += 1
            leveled_up = True

        await self._conn.execute(
            "UPDATE levels SET xp = ?, level = ?, last_xp_at = ? WHERE user_id = ?",
            (new_xp, new_level, datetime.now(timezone.utc).isoformat(), user_id),
        )
        await self._conn.commit()
        return new_level, leveled_up

    async def get_leaderboard(self, limit: int = 10):
        cursor = await self._conn.execute(
            """
            SELECT user_id, xp, level
            FROM levels
            ORDER BY level DESC, xp DESC
            LIMIT ?
            """,
            (limit,),
        )
        return await cursor.fetchall()
