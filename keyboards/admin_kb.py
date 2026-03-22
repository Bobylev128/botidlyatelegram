from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать батл", callback_data="create")],
        [InlineKeyboardButton(text="Участники", callback_data="users")],
        [InlineKeyboardButton(text="Рассылка", callback_data="broadcast")]
    ])