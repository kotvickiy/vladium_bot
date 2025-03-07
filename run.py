import asyncio

from aiogram import Dispatcher

from app.handlers import router, bot


dp = Dispatcher()


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
