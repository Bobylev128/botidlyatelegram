import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN_API
from handlers import start, admin, voting, payments, broadcast, bans
from utils.updater import updater
from utils.storage import load, save


async def main():
    bot = Bot(TOKEN_API)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(voting.router)
    dp.include_router(payments.router)
    dp.include_router(broadcast.router)
    dp.include_router(bans.router)

    load()

    asyncio.create_task(updater(bot))

    try:
        await dp.start_polling(bot)
    finally:
        save()


if __name__ == "__main__":
    asyncio.run(main())