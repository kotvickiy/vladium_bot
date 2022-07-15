#!/usr/bin/python3
import asyncio
from aiogram import Bot, Dispatcher, executor
from config import TOKEN, CHAT_ID


loop = asyncio.new_event_loop()
bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop)


if __name__ == '__main__':
    from handlers import dp, send_hello
    executor.start_polling(dp, on_startup=send_hello)
