from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def join_kb(link):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Участвовать", url=link)]
    ])