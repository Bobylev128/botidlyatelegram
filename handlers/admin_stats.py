from aiogram import Router, F
from aiogram.types import CallbackQuery

from handlers.admin import battle_data, is_admin
from db import get_group_votes, get_voters

router = Router()


# 📃 открыть список раундов
@router.callback_query(F.data == "admin_battle")
async def open_battle(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    if not battle_data.get("active"):
        await callback.answer("❌ Батл не идёт", show_alert=True)
        return

    buttons = []

    for i in range(len(battle_data["rounds"])):
        buttons.append([{
            "text": f"Раунд {i+1}",
            "callback_data": f"admin_round:{i}"
        }])

    buttons.append([{"text": "🔙 Назад", "callback_data": "admin_back"}])

    await callback.message.edit_text(
        "📊 Выберите раунд:",
        reply_markup={"inline_keyboard": buttons}
    )


# 📊 группы внутри раунда
@router.callback_query(F.data.startswith("admin_round"))
async def open_round(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    _, round_n = callback.data.split(":")
    round_n = int(round_n)

    groups = battle_data["rounds"][round_n]

    buttons = []

    for i in range(len(groups)):
        buttons.append([{
            "text": f"Группа {i+1}",
            "callback_data": f"admin_group:{round_n}:{i}"
        }])

    buttons.append([{"text": "🔙 Назад", "callback_data": "admin_battle"}])

    await callback.message.edit_text(
        f"📊 Раунд {round_n+1}",
        reply_markup={"inline_keyboard": buttons}
    )


# 👥 просмотр группы
@router.callback_query(F.data.startswith("admin_group"))
async def open_group(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    _, round_n, group_n = callback.data.split(":")
    round_n, group_n = int(round_n), int(group_n)

    group = battle_data["rounds"][round_n][group_n]
    votes = get_group_votes(round_n, group_n)

    text = f"📊 Раунд {round_n+1} | Группа {group_n+1}\n\n"

    buttons = []

    for user in group:
        user_votes = votes.get(user, {"free": 0, "paid": 0})
        total = user_votes["free"] + user_votes["paid"]

        text += (
            f"{user}\n"
            f"🆓 {user_votes['free']} | 💰 {user_votes['paid']} | 📊 {total}\n\n"
        )

        buttons.append([{
            "text": f"👁 {user}",
            "callback_data": f"admin_user_votes:{round_n}:{group_n}:{user}"
        }])

    buttons.append([{"text": "🔙 Назад", "callback_data": f"admin_round:{round_n}"}])

    await callback.message.edit_text(
        text,
        reply_markup={"inline_keyboard": buttons}
    )


# 🧾 кто голосовал
@router.callback_query(F.data.startswith("admin_user_votes"))
async def show_voters(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    _, round_n, group_n, user = callback.data.split(":")
    round_n, group_n = int(round_n), int(group_n)

    voters = get_voters(user, round_n, group_n)

    if not voters:
        text = "❌ Нет голосов"
    else:
        text = f"🧾 Голоса за {user}:\n\n"

        for voter_id, vote_type in voters:
            text += f"👤 <a href='tg://user?id={voter_id}'>Пользователь</a>"
            if vote_type == "paid":
                text += " 💰"
            text += "\n"

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup={
            "inline_keyboard": [[
                {
                    "text": "🔙 Назад",
                    "callback_data": f"admin_group:{round_n}:{group_n}"
                }
            ]]
        }
    )