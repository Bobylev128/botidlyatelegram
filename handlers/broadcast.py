from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto, InputMediaDocument, InputMediaAnimation
from handlers.admin import is_admin
from db import cursor

router = Router()


# 🔹 Начало рассылки
@router.message(F.text == "/broadcast")
async def start_broadcast(message: Message, state: "FSMContext"):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещен")
        return

    await state.set_state("broadcast_wait")
    await message.answer(
        "✉️ Введите сообщение для рассылки.\n"
        "Можно отправить текст, фото, гиф или документ."
    )


# 🔹 Получение контента для рассылки
@router.message("broadcast_wait")
async def process_broadcast(message: Message, state: "FSMContext"):
    bot = message.bot
    await state.clear()

    media = None
    text = message.text

    # проверка типа сообщения
    if message.photo:
        media = InputMediaPhoto(media=message.photo[-1].file_id, caption=message.caption or "")
    elif message.document:
        media = InputMediaDocument(media=message.document.file_id, caption=message.caption or "")
    elif message.animation:
        media = InputMediaAnimation(media=message.animation.file_id, caption=message.caption or "")

    # подтверждение
    await message.answer("✅ Проверка готова. Начать рассылку? (да/нет)")

    await state.update_data(broadcast_text=text, broadcast_media=media)


# 🔹 Подтверждение
@router.message()
async def confirm_broadcast(message: Message, state: "FSMContext"):
    answer = message.text.lower()
    if answer not in ["да", "yes"]:
        await message.answer("❌ Рассылка отменена")
        await state.clear()
        return

    data = await state.get_data()
    text = data.get("broadcast_text")
    media = data.get("broadcast_media")

    # получаем всех участников
    cursor.execute("SELECT user_id FROM battle_participants")
    users = [row[0] for row in cursor.fetchall()]

    sent = 0
    failed = 0

    for user_id in users:
        try:
            if media:
                await bot.send_media_group(chat_id=user_id, media=[media])
            else:
                await bot.send_message(chat_id=user_id, text=text)
            sent += 1
        except:
            failed += 1

    await message.answer(f"✅ Рассылка завершена!\n📨 Отправлено: {sent}\n❌ Ошибки: {failed}")
    await state.clear()