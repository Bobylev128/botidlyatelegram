from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_panel():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Начать батл", callback_data="admin_start_battle")],
            [InlineKeyboardButton("Отменить батл‼️", callback_data="admin_cancel_battle")],
            [InlineKeyboardButton("Батл📃", callback_data="admin_battle")],
            [InlineKeyboardButton("Баны 🚫", callback_data="admin_bans")],
            [InlineKeyboardButton("Добавить участника ➕", callback_data="admin_add_user")],
            [InlineKeyboardButton("Удалить участника ➖", callback_data="admin_remove_user")],
            [InlineKeyboardButton("Редактировать батл ✏️", callback_data="admin_edit_battle")],
        ]
    )