#!/usr/bin/env python3
# python3 -m venv lin_venv3104 && . lin_venv3104/bin/activate
# pip install aiogram python-crontab
# kill $(pgrep -f .vscode-server/bin/) # убить иксы vscode
# kill $(pgrep -f bot.py) # убить бота
# ssh-keygen
# ssh-copy-id vladium@myselfserver

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, CHAT_ID
from crontab import CronTab
import os
import socket


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
myselfserver = s.getsockname()[0]


def cron():
    return list(CronTab(user="vladium"))


def installation_crontab(grid_one="", grid_two="", grid_three="# ", grid_four="# "):
    os.system(f'crontab -l > foocron; echo "{grid_one}@reboot /usr/bin/sleep 15; ssh vladium@{myselfserver} Xvfb &\n{grid_two}@reboot /usr/bin/sleep 20; cd /home/vladium/code/vladium_bot/ && /home/vladium/code/vladium_bot/lin_venv3104/bin/python3 /home/vladium/code/vladium_bot/bot.py >> out.log 2>&1\n{grid_three}*/5 * * * * cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/main.py >> out.log 2>&1\n{grid_four}*/5 * * * * cd /home/vladium/code/find_mobile/ && /home/vladium/code/find_mobile/lin_venv3104/bin/python3 /home/vladium/code/find_mobile/main.py >> out.log 2>&1" > foocron; crontab foocron; rm foocron')


try:
    cron()[0]
except:
    installation_crontab()


def kb():
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    return kb_client


b1 = KeyboardButton("Запустить kwork")
b2 = KeyboardButton("Запустить find_mobile")
b3 = KeyboardButton("Up kwork cron")
b4 = KeyboardButton("Up find_mobile cron")
b5 = KeyboardButton("Down kwork cron")
b6 = KeyboardButton("Down find_mobile cron")
b7 = KeyboardButton("Проверить")
b8 = KeyboardButton("Перезагрузить")
b9 = KeyboardButton("Меню")
b10 = KeyboardButton("Default cron")


acl = (CHAT_ID, )
admin_only = lambda message: message.from_user.id not in acl


@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    return


@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(b9))
    await message.delete()


async def verify(message):
    if str(cron()[2])[0] == "#":
        kwork = "Выключен"
    else:
        kwork = "Включен"
    if str(cron()[3])[0] == "#":
        find_mobile = "Выключен"
    else:
        find_mobile = "Включен"
    await bot.send_message(message.from_user.id, f"kwork: {kwork}, find_mobile: {find_mobile}", reply_markup=kb().row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(b9, b10))


@dp.message_handler()
async def send(message : types.Message):
    
    if message.text == "Запустить kwork":
        await bot.send_message(message.from_user.id, "kwork запущен", reply_markup=ReplyKeyboardRemove())
        await message.delete()
        os.system('cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/main.py >> out.log 2>&1')
        await bot.send_message(message.from_user.id, "kwork завершен")
        await verify(message)
    elif message.text == "Запустить find_mobile":
        await bot.send_message(message.from_user.id, "find_mobile запущен", reply_markup=ReplyKeyboardRemove())
        await message.delete()
        os.system('cd /home/vladium/code/find_mobile/ && /home/vladium/code/find_mobile/lin_venv3104/bin/python3 /home/vladium/code/find_mobile/main.py >> out.log 2>&1')
        await bot.send_message(message.from_user.id, "find_mobile завершен")
        await verify(message)
    elif message.text == "Проверить":
        await message.delete()
        await verify(message)
    elif message.text == "Перезагрузить":
        await message.delete()
        sudoPassword = '241215'
        command = 'reboot'
        os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    elif message.text == "Меню":
        await message.delete()
        await bot.send_message(message.from_user.id, "Меню", reply_markup=kb().row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(b9, b10))
    elif message.text == "Up kwork cron":
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb().row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(b9, b10))
        await message.delete()
        if str(cron()[3])[0] == "#":
            installation_crontab(grid_three="")
        else:
            installation_crontab(grid_three="", grid_four="")
        await bot.send_message(message.from_user.id, "kwork на cron ↑↑↑")
    elif message.text == "Up find_mobile cron": 
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb().row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(b9, b10))
        await message.delete()
        if str(cron()[2])[0] == "#":
            installation_crontab(grid_four="")
        else:
            installation_crontab(grid_three="", grid_four="")
        await bot.send_message(message.from_user.id, "find_mobile на cron ↑↑↑")
    elif message.text == "Down kwork cron":
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb().row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(b9, b10))
        await message.delete()
        if str(cron()[3])[0] == "#":
            installation_crontab(grid_three="#")
        else:
            installation_crontab(grid_three="#", grid_four="")
        await bot.send_message(message.from_user.id, "Down kwork cron ↓↓↓")
    elif message.text == "Down find_mobile cron": 
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb().row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(b9, b10))
        await message.delete()
        if str(cron()[2])[0] == "#":
            installation_crontab(grid_four="#")
        else:
            installation_crontab(grid_three="", grid_four="#")
        await bot.send_message(message.from_user.id, "Down find_mobile cron ↓↓↓")
    elif message.text == "Default cron":
        await message.delete()
        installation_crontab()
        await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(b1, b2).row(b3, b4).row(b5, b6).row(b7, b8).row(b9, b10))



executor.start_polling(dp, skip_updates=True)
