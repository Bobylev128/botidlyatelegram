from aiogram import Router
from aiogram.types import Message

from handlers.voting import open_vote_menu
from handlers.admin import join_battle
from battle_data import battle_data

router = Router()


@router.message()
async def start_handler(message: Message):
    args = message.text.split()

    if len(args) > 1:
        param = args[1]

        if param.startswith("vote_"):
            _, r, g = param.split("_")
            await open_vote_menu(message, int(r), int(g))
            return

        if param == "join":
            await join_battle(message)
            return

    if battle_data["active"]:
        await message.answer("📃 Перейдите к раунду через кнопку в канале")
    elif battle_data["registration"]:
        await message.answer("🗳 Сейчас идет набор")
    else:
        await message.answer("❌ Батл не идет")