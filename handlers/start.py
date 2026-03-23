from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from handlers.admin import join_battle
from handlers.voting import open_vote_menu
from battle_data import battle_data

router = Router()


@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    args = message.get_args()  # для deeplink

    if args:
        if args.startswith("vote_"):
            _, r, g = args.split("_")
            await open_vote_menu(message, int(r), int(g))
            return

        if args == "join":
            await join_battle(message)
            return

    if battle_data["active"]:
        await message.answer("📃 Перейдите к раунду через кнопку в канале")
    elif battle_data["registration"]:
        await message.answer("🗳 Сейчас идет набор")
    else:
        await message.answer("❌ Батл не идет")