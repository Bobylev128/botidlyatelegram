from aiogram import Router, F
from aiogram.types import Message
from db import add_user, is_banned
from battle_data import battle_data

router = Router()


@router.message(F.text.startswith("/start"))
async def start(message: Message):
    add_user(message.from_user.id)

    ban = is_banned(message.from_user.id)
    if ban:
        await message.answer(f"🚫 Вы забанены\nПричина: {ban[0]}")
        return

    args = message.text.split(" ")

    if len(args) > 1:
        arg = args[1]

        if arg == "join":
            if not battle_data["registration"]:
                await message.answer("❌ Набор закрыт")
                return

            if len(battle_data["players"]) >= battle_data["max_players"]:
                await message.answer("⛔️ Лимит достигнут")
                return

            if message.from_user.username:
                battle_data["players"].append(f"@{message.from_user.username}")
                await message.answer("✅ Вы зарегистрированы")
            else:
                await message.answer("❌ Нужен username")

    else:
        await message.answer("👋 Добро пожаловать в батл-бот")