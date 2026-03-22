import asyncio
import os
import aiosqlite

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# ---------- LOAD ENV ----------
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("❌ API_TOKEN не найден в переменных окружения")

# ---------- CONFIG ----------
ADMIN_ID = int(os.getenv("admid"))
MAIN_CHANNEL_ID = int(os.getenv("mchid"))
# ---------- INIT ----------
bot = Bot(API_TOKEN)
dp = Dispatcher()

DB = "db.sqlite"

# ---------- DB ----------
async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, username TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS votes(voter_id INTEGER, target TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS blacklist(user_id INTEGER)")
        await db.commit()

# ---------- START ----------
@dp.message()
async def test(msg: Message):
    await msg.answer("Я живой ✅")
async def start(msg: Message):

    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT 1 FROM blacklist WHERE user_id=?", (msg.from_user.id,))
        if await cur.fetchone():
            await msg.answer("🚫 Вы в ЧС")
            return

    if not msg.from_user.username:
        await msg.answer("❌ У вас нет username")
        return

    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT INTO users VALUES (?,?)",
                         (msg.from_user.id, "@"+msg.from_user.username))
        await db.commit()

    await msg.answer("✅ Вы зарегистрированы")

# ---------- ADMIN ----------
def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Создать батл", callback_data="create")]
    ])

@dp.message(F.text == "/admin")
async def admin(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer("⚙️ Админ панель", reply_markup=admin_kb())

# ---------- CREATE BATTLE ----------
players = []

@dp.callback_query(F.data == "create")
async def create(call: CallbackQuery):
    players.clear()
    await call.message.answer("Введите участников:\nпример:\n@user1 @user2 @user3")

@dp.message()
async def add_players(msg: Message):
    global players

    if msg.from_user.id != ADMIN_ID:
        return

    if "@" in msg.text:
        players = msg.text.split()

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"🗳 Голос за {u}", callback_data=f"vote:{u}")]
            for u in players
        ])

        await bot.send_message(
            MAIN_CHANNEL_ID,
            "🔥 <b>БАТЛ НАЧАЛСЯ</b>\n\n👇 Голосуй 👇",
            reply_markup=kb
        )

        await msg.answer("✅ Батл запущен")

# ---------- VOTE ----------
@dp.callback_query(F.data.startswith("vote"))
async def vote(call: CallbackQuery):

    user = call.data.split(":")[1]

    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT 1 FROM votes WHERE voter_id=?",
            (call.from_user.id,))
        if await cur.fetchone():
            await call.answer("❌ Вы уже голосовали")
            return

        await db.execute(
            "INSERT INTO votes VALUES (?,?)",
            (call.from_user.id, user))
        await db.commit()

    await call.answer("✅ Голос принят")

# ---------- STATS ----------
@dp.message(F.text == "/stats")
async def stats(msg: Message):

    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT target, COUNT(*) FROM votes GROUP BY target")
        data = await cur.fetchall()

    text = "📊 <b>Результаты</b>\n\n"

    for u, c in data:
        text += f"{u} — {c}\n"

    await msg.answer(text)

# ---------- RUN ----------
async def main():
    await init_db()
    print("🔥 BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
