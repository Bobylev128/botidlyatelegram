from aiogram import Router
from aiogram.types import Message
import aiosqlite

router = Router()

@router.message()
async def start(msg: Message):
    async with aiosqlite.connect("battle.db") as db:
        cur = await db.execute("SELECT 1 FROM blacklist WHERE user_id=?", (msg.from_user.id,))
        if await cur.fetchone():
            await msg.answer("Вы в бане")
            return

    await msg.answer("Добро пожаловать")