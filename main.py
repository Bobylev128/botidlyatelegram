import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN_API

from handlers import start, admin, voting, payments

bot = Bot(TOKEN_API)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(admin.router)
dp.include_router(voting.router)
dp.include_router(payments.router)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))