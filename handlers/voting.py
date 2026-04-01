from aiogram import Router, F
from aiogram.types import *
from db import add_vote, has_voted_free

router = Router()


@router.callback_query(F.data.startswith("vote:"))
async def vote(callback: CallbackQuery):
    _, r, g, user = callback.data.split(":")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обычный", callback_data=f"free:{r}:{g}:{user}")],
        [InlineKeyboardButton(text="Платный (10⭐)", callback_data=f"pay:{r}:{g}:{user}")]
    ])

    await callback.message.answer("Выберите тип голоса", reply_markup=kb)


@router.callback_query(F.data.startswith("free:"))
async def free(callback: CallbackQuery):
    _, r, g, user = callback.data.split(":")

    if has_voted_free(callback.from_user.id, r, g):
        await callback.answer("❌ Уже голосовал", show_alert=True)
        return

    add_vote(callback.from_user.id, user, int(r), int(g), "free")
    await callback.answer("✅ Голос принят")