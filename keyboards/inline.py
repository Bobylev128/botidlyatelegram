from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def vote_kb(gid, users):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=u, callback_data=f"vote:{gid}:{u}")]
        for u in users
    ])