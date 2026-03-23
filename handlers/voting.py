from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from db import add_vote, has_voted
from keyboards.vote_kb import vote_kb, vote_type_kb
from handlers.payments import send_invoice
from battle_data import battle_data

router = Router()


async def open_vote_menu(message: Message, round_n, group_n):
    group = battle_data["rounds"][round_n][group_n]

    text = "💬 Голосование\n\n" + "\n".join(group)

    await message.answer(
        text,
        reply_markup=vote_kb(group, round_n, group_n)
    )


@router.callback_query(F.data.startswith("vote_select"))
async def vote_select(callback: CallbackQuery):
    _, r, g, user = callback.data.split(":")
    await callback.message.edit_reply_markup(
        reply_markup=vote_type_kb(r, g, user)
    )


@router.callback_query(F.data.startswith("vote_free"))
async def vote_free(callback: CallbackQuery):
    _, r, g, user = callback.data.split(":")

    if has_voted(callback.from_user.id, r, g):
        await callback.answer("❌ Уже голосовали", show_alert=True)
        return

    add_vote(callback.from_user.id, user, int(r), int(g), "free")
    await callback.answer("✅ Голос засчитан")


@router.callback_query(F.data.startswith("vote_paid"))
async def vote_paid(callback: CallbackQuery):
    _, r, g, user = callback.data.split(":")
    await send_invoice(callback.bot, callback.from_user.id, r, g, user)