from aiogram import Router
from aiogram.types import Message
import aiosqlite

router = Router()

@router.message()
async def broadcast(msg: Message):
    async with aiosqlite.connect("battle.db") as db:
        cur = await db.execute("SELECT user_id FROM users")
        users = await cur.fetchall()

    for u in users:
        try:
            await msg.copy_to(u[0])
        except:
            pass