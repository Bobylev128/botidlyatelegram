# FULL TELEGRAM BATTLE BOT (ALL-IN-ONE)
# NOTE: This is a merged version of all stages. Some parts may require environment setup.

import os
import asyncio
import time
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ================= CONFIG =================
API_TOKEN = os.getenv("API_TOKEN")
MAIN_CHANNEL_ID = int(os.getenv("mainch", "0"))
ANNOUNCE_CHANNEL_ID = int(os.getenv("annch", "0"))
ADMIN_ID = int(os.getenv("admid", "0"))
CHANNEL_LINK = os.getenv("clink")

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# ================= DATABASE =================
conn = sqlite3.connect("bot.db")
cursor = conn.cursor()


def init_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS participants(user_id INTEGER, username TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS votes(id INTEGER PRIMARY KEY AUTOINCREMENT, round_id INTEGER, voter_id INTEGER, username TEXT, paid INTEGER)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS rounds(id INTEGER PRIMARY KEY AUTOINCREMENT, round_number INTEGER, users TEXT)""")
    conn.commit()


# ================= HELPERS =================

def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users VALUES(?)", (user_id,))
    conn.commit()


def add_participant(user_id, username):
    cursor.execute("INSERT INTO participants VALUES(?,?)", (user_id, username))
    conn.commit()


def get_participants():
    cursor.execute("SELECT username FROM participants")
    return [x[0] for x in cursor.fetchall()]


def add_vote(round_id, voter_id, username, paid=0):
    cursor.execute("INSERT INTO votes(round_id,voter_id,username,paid) VALUES(?,?,?,?)",
                   (round_id, voter_id, username, paid))
    conn.commit()


def get_votes(round_id):
    cursor.execute("SELECT username, COUNT(*) FROM votes WHERE round_id=? GROUP BY username", (round_id,))
    return dict(cursor.fetchall())


# ================= START =================
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    add_user(msg.from_user.id)
    await msg.answer("🔥 Добро пожаловать в батл-бот!")


# ================= REGISTRATION =================
@dp.message_handler(commands=['join'])
async def join(msg: types.Message):
    if not msg.from_user.username:
        return await msg.answer("❌ У вас нет username")

    add_participant(msg.from_user.id, msg.from_user.username)
    await msg.answer("✅ Вы зарегистрированы")


# ================= CREATE ROUND =================
@dp.message_handler(commands=['startbattle'])
async def start_battle(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    users = get_participants()

    if len(users) < 2:
        return await msg.answer("❌ Недостаточно игроков")

    cursor.execute("DELETE FROM rounds")

    groups = [users[i:i+4] for i in range(0, len(users), 4)]

    for i, g in enumerate(groups):
        cursor.execute("INSERT INTO rounds(round_number, users) VALUES(?,?)",
                       (1, "|".join(g)))

    conn.commit()

    await send_rounds(1)


# ================= SEND ROUNDS =================
async def send_rounds(round_number):
    cursor.execute("SELECT * FROM rounds WHERE round_number=?", (round_number,))
    data = cursor.fetchall()

    for r in data:
        round_id = r[0]
        users = r[2].split("|")

        kb = InlineKeyboardMarkup()

        text = f"🔥 Раунд {round_number}\n\n"

        for u in users:
            kb.add(InlineKeyboardButton(f"Голос за @{u}", callback_data=f"vote_{round_id}_{u}"))
            text += f"@{u}\n"

        await bot.send_message(MAIN_CHANNEL_ID, text, reply_markup=kb)


# ================= VOTE =================
@dp.callback_query_handler(lambda c: c.data.startswith("vote_"))
async def vote(call: types.CallbackQuery):
    _, round_id, username = call.data.split("_")

    add_vote(int(round_id), call.from_user.id, username)

    await call.answer("✅ Голос засчитан")


# ================= TIMER =================
async def round_timer():
    while True:
        await asyncio.sleep(60)
        # simplified auto finish logic


# ================= ADMIN =================
@dp.message_handler(commands=['admin'])
async def admin(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🚀 Старт батла", callback_data="admin_start"))

    await msg.answer("Админ панель", reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == "admin_start")
async def admin_start(call: types.CallbackQuery):
    await start_battle(call.message)


# ================= RUN =================
async def main():
    init_db()
    asyncio.create_task(round_timer())
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
