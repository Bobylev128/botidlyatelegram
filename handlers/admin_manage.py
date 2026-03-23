from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from db import ban_user, unban_user, get_bans, add_participant_manual, remove_participant
from handlers.admin import is_admin, battle_data

router = Router()

# 🔒 Баны - просмотр
@router.callback_query(F.data == "admin_bans")
async def view_bans(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return

    bans = get_bans()

    text = "🚫 Список банов:\n\n"
    if bans:
        for user_id, reason in bans:
            text += f"👤 <a href='tg://user?id={user_id}'>Пользователь</a> — {reason}\n"
    else:
        text += "❌ Нет забаненных пользователей"

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup={
            "inline_keyboard": [
                [{"text": "Добавить бан", "callback_data": "admin_ban_add"}],
                [{"text": "Удалить бан", "callback_data": "admin_ban_remove"}],
                [{"text": "🔙 Назад", "callback_data": "admin_back"}]
            ]
        }
    )


# ➕ Добавить бан
@router.callback_query(F.data == "admin_ban_add")
async def ban_add(callback: CallbackQuery, state: "FSMContext"):
    await state.set_state("ban_add_wait")
    await callback.message.edit_text("Введите ID пользователя и причину через пробел:\nПример: 123456 Спам")


@router.message("ban_add_wait")
async def ban_add_message(message: Message, state: "FSMContext"):
    try:
        user_id, reason = message.text.split(" ", 1)
        user_id = int(user_id)
        ban_user(user_id, reason)
        await message.answer("✅ Пользователь забанен")
    except:
        await message.answer("❌ Неверный формат")
    await state.clear()


# ➖ Удалить бан
@router.callback_query(F.data == "admin_ban_remove")
async def ban_remove(callback: CallbackQuery, state: "FSMContext"):
    await state.set_state("ban_remove_wait")
    await callback.message.edit_text("Введите ID пользователя для разбана:")


@router.message("ban_remove_wait")
async def ban_remove_message(message: Message, state: "FSMContext"):
    try:
        user_id = int(message.text)
        unban_user(user_id)
        await message.answer("✅ Пользователь разбанен")
    except:
        await message.answer("❌ Неверный формат")
    await state.clear()


# ➕ Добавление участника вручную
@router.callback_query(F.data == "admin_add_user")
async def add_user(callback: CallbackQuery, state: "FSMContext"):
    await state.set_state("add_user_wait")
    await callback.message.edit_text("Введите ID и username пользователя через пробел\nПример: 123456 @username")


@router.message("add_user_wait")
async def add_user_message(message: Message, state: "FSMContext"):
    try:
        user_id, username = message.text.split()
        add_participant_manual(int(user_id), username)
        await message.answer("✅ Пользователь добавлен")
    except:
        await message.answer("❌ Неверный формат")
    await state.clear()


# ➖ Удаление участника
@router.callback_query(F.data == "admin_remove_user")
async def remove_user(callback: CallbackQuery, state: "FSMContext"):
    await state.set_state("remove_user_wait")
    await callback.message.edit_text("Введите ID пользователя для удаления:")


@router.message("remove_user_wait")
async def remove_user_message(message: Message, state: "FSMContext"):
    try:
        user_id = int(message.text)
        remove_participant(user_id)
        await message.answer("✅ Пользователь удален")
    except:
        await message.answer("❌ Неверный формат")
    await state.clear()