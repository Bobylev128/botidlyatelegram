import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(API_TOKEN)
dp = Dispatcher()

@dp.message()
async def start(msg: Message):
    if msg.text == "/start":
        await msg.answer("✅ Бот работает")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
