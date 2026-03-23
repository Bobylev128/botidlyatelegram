from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import ADMIN_ID, MAIN_CHANNEL_ID, BOT_USERNAME
from db import get_all_users, add_participant_manual
from battle_data import battle_data
from utils.brackets import generate_brackets
from utils.deeplink import create_vote_link, create_join_link
from keyboards.user_kb import join_kb

router = Router()


def is_admin(user_id):
    return user_id == ADMIN_ID


@router.message(Command(commands=["admin"]))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Админ панель")


async def join_battle(message: Message):
    if not battle_data["registration"]:
        await message.answer("❌ Набор закрыт")
        return

    if not message.from_user.username:
        await message.answer("❌ У вас нет username")
        return

    add_participant_manual(message.from_user.id, "@" + message.from_user.username)
    await message.answer("✅ Вы зарегистрированы!")


async def start_battle(bot):
    users = get_all_users()
    users = [u[1] for u in users]

    battle_data["rounds"] = [generate_brackets(users)]
    battle_data["current_round"] = 0
    battle_data["active"] = True

    await send_round(bot, 0)


async def send_round(bot, round_index):
    groups = battle_data["rounds"][round_index]

    for i, group in enumerate(groups):
        link = create_vote_link(BOT_USERNAME, round_index, i)

        text = (
            f"💬 Раунд {round_index+1}\n\n"
            + "\n".join(group)
            + f"\n\n🗳 <a href='{link}'>Голосовать</a>"
        )

        await bot.send_message(
            MAIN_CHANNEL_ID,
            text,
            parse_mode="HTML"
        )