from aiogram import Router, F
from aiogram.types import *
from db import get_all_users

router = Router()

cache = {}


@router.message(F.text == "/broadcast")
async def start(message: Message):
    await message.answer("Отправь сообщение для рассылки")


@router.message()
async def preview(message: Message):
    cache["msg"] = message

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Отправить", callback_data="send")]
    ])

    await message.answer("Отправить это сообщение?", reply_markup=kb)


@router.callback_query(F.data == "send")
async def send(callback: CallbackQuery):
    for uid in get_all_users():
        try:
            await cache["msg"].copy_to(uid)
        except:
            pass

    await callback.answer("📢 Рассылка завершена")