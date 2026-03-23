from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import count_votes


def vote_kb(group, round_n, group_n):
    kb = []
    for user in group:
        votes = count_votes(user, round_n, group_n)
        kb.append([
            InlineKeyboardButton(
                text=f"{user} — {votes}",
                callback_data=f"vote_select:{round_n}:{group_n}:{user}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def vote_type_kb(round_n, group_n, user):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Обычный", callback_data=f"vote_free:{round_n}:{group_n}:{user}")],
        [InlineKeyboardButton("Платный (10⭐)", callback_data=f"vote_paid:{round_n}:{group_n}:{user}")]
    ])