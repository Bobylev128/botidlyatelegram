from aiogram import Router, F
from aiogram.types import CallbackQuery
import aiosqlite

router = Router()

@router.callback_query(F.data.startswith("vote"))
async def vote(call: CallbackQuery):
    _, gid, user = call.data.split(":")

    async with aiosqlite.connect("battle.db") as db:
        await db.execute(
            "INSERT INTO votes VALUES (?, ?, ?, ?)",
            (call.from_user.id, gid, user, "normal")
        )
        await db.commit()

    await call.answer("Голос принят")