import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from db import init_db

from handlers import user, admin, voting, payments, broadcast

bot = Bot(API_TOKEN)
dp = Dispatcher()

dp.include_router(admin.router)
dp.include_router(user.router)
dp.include_router(voting.router)
dp.include_router(payments.router)
dp.include_router(broadcast.router)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())