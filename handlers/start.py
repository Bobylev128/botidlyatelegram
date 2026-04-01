from aiogram import Router, F
from aiogram.types import Message
from db import add_user, is_banned
from battle_data import battle_data

router = Router()


@router.message(F.text.startswith("/start"))
async def start_handler(message: Message):
    add_user(message.from_user.id)

    # проверка бана
    ban = is_banned(message.from_user.id)
    if ban:
        await message.answer(f"🚫 Вы забанены\nПричина: {ban[0]}")
        return

    # ✅ ПРАВИЛЬНЫЙ DEEPLINK
    parts = message.text.split(" ")

    if len(parts) > 1:
        arg = parts[1]

        # регистрация
        if arg == "join":
            if not battle_data["registration"]:
                await message.answer("❌ Набор закрыт")
                return

            if len(battle_data["players"]) >= battle_data["max_players"]:
                await message.answer("⛔️ Лимит достигнут")
                return

            if not message.from_user.username:
                await message.answer("❌ У вас нет username")
                return

            username = f"@{message.from_user.username}"

            if username in battle_data["players"]:
                await message.answer("⚠️ Вы уже зарегистрированы")
                return

            battle_data["players"].append(username)
            await message.answer("✅ Вы зарегистрированы")
            return

        # голосование
        if arg.startswith("vote_"):
            try:
                _, r, g = arg.split("_")

                await message.answer(
                    f"🗳 Голосование\nРаунд: {int(r)+1}\nГруппа: {int(g)+1}"
                )
            except:
                await message.answer("❌ Ошибка deeplink")

            return

    await message.answer("👋 Добро пожаловать")
