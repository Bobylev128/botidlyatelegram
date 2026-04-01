from aiogram import Router, F
from aiogram.types import *
from db import ban_user

router = Router()


@router.message(F.text.startswith("/ban"))
async def ban(message: Message):
    args = message.text.split()

    uid = int(args[1])
    reason = " ".join(args[2:])

    ban_user(uid, reason)
    await message.answer("🚫 Пользователь забанен")