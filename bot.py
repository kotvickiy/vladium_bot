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


def out(project):
    try:
        with open(f"../{project}/out.log") as file:
            return file.readlines()[-1].strip()
    except:
        return "no file"


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
b11 = KeyboardButton("Out kwork")
b12 = KeyboardButton("Out find_mobile")


acl = (CHAT_ID, )
admin_only = lambda message: message.from_user.id not in acl


def verify_cron_and_install_button():
    if str(cron()[2])[0] == "#" and str(cron()[3])[0] == "#":
        return [b3, b4]
    elif str(cron()[2])[0] == "*" and str(cron()[3])[0] == "*":
        return [b5, b6]
    elif str(cron()[2])[0] == "#" and str(cron()[3])[0] == "*":
        return [b3, b6]
    elif str(cron()[2])[0] == "*" and str(cron()[3])[0] == "#":
        return [b5, b4]


@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    return


@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await message.delete()
    btn = verify_cron_and_install_button()
    await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(btn[0], btn[1]).row(b9))


async def verify(message):
    if str(cron()[2])[0] == "#":
        kwork = "Выключен"
    else:
        kwork = "Включен"
    if str(cron()[3])[0] == "#":
        find_mobile = "Выключен"
    else:
        find_mobile = "Включен"
    new_btn = verify_cron_and_install_button()
    await bot.send_message(message.from_user.id, f"kwork: {kwork}, find_mobile: {find_mobile}", reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))


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
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "Меню", reply_markup=kb().row(b1, b2).row(btn[0], btn[1]).row(b7, b8).row(b11, b12).row(b10))
    elif message.text == "Up kwork cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb().row(btn[0], btn[1]).row(b9))
        if str(cron()[3])[0] == "#":
            installation_crontab(grid_three="")
        else:
            installation_crontab(grid_three="", grid_four="")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "kwork на cron ↑↑↑", reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))
    elif message.text == "Up find_mobile cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb().row(btn[0], btn[1]).row(b9))
        if str(cron()[2])[0] == "#":
            installation_crontab(grid_four="")
        else:
            installation_crontab(grid_three="", grid_four="")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "find_mobile на cron ↑↑↑", reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))
    elif message.text == "Down kwork cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb().row(btn[0], btn[1]).row(b9))
        if str(cron()[3])[0] == "#":
            installation_crontab(grid_three="#")
        else:
            installation_crontab(grid_three="#", grid_four="")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "Down kwork cron ↓↓↓", reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))
    elif message.text == "Down find_mobile cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb().row(btn[0], btn[1]).row(b9))
        if str(cron()[2])[0] == "#":
            installation_crontab(grid_four="#")
        else:
            installation_crontab(grid_three="", grid_four="#")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "Down find_mobile cron ↓↓↓", reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))
    elif message.text == "Out kwork":
        await message.delete()
        out_find_mobile = out("kwork")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, out_find_mobile, reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))
    elif message.text == "Out find_mobile":
        await message.delete()
        out_find_mobile = out("find_mobile")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, out_find_mobile, reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))
    elif message.text == "Default cron":
        await message.delete()
        installation_crontab()
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))


executor.start_polling(dp, skip_updates=True)
