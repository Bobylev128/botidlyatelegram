from aiogram import Router, F
from aiogram.types import *

router = Router()


@router.message(F.text == "/admin")
async def admin(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Батл", callback_data="battle")],
        [InlineKeyboardButton(text="📢 Рассылка", callback_data="broadcast")],
        [InlineKeyboardButton(text="🚫 Баны", callback_data="bans")]
    ])

    await message.answer("👑 Админка", reply_markup=kb)