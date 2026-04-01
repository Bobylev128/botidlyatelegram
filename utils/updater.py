import asyncio
from datetime import datetime
from battle_data import battle_data
from db import count_votes
from utils.formatter import format_round
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb(group, r, g):
    rows = []
    for u in group:
        votes = count_votes(u, r, g)
        total = votes["free"] + votes["paid"]

        rows.append([
            InlineKeyboardButton(
                text=f"{u} — {total}",
                url=f"https://t.me/YOUR_BOT?start=vote_{r}_{g}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def updater(bot):
    while True:
        if battle_data["active"]:
            for chat_id, msg_id, r, g in battle_data["vote_messages"]:
                try:
                    group = battle_data["rounds"][r][g]

                    rem = int((battle_data["round_end_time"] - datetime.now()).total_seconds())
                    m, s = rem // 60, rem % 60

                    text = format_round(r, group, f"{m:02}:{s:02}")

                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=msg_id,
                        text=text,
                        reply_markup=kb(group, r, g)
                    )
                except:
                    pass

        await asyncio.sleep(10)