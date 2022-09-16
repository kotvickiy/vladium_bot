#!/usr/bin/env python3
# python3 -m venv lin_venv3104 && . lin_venv3104/bin/activate
# pip install aiogram python-crontab
# kill $(pgrep -f .vscode-server/bin/) # убить иксы vscode
# kill $(pgrep -f bot.py) # убить бота
# ssh-keygen
# ssh-copy-id vladium@myselfserver

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from datetime import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, CHAT_ID
from crontab import CronTab
import os
import socket



storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


def edit_phone_list(in_line):
    flag = False
    in_line = in_line.lower().split(" ")
    if in_line[0] == "samsung" or in_line[0] == "s":
        file = "../find_mobile/samsung.csv"
    elif in_line[0] == "xiaomi" or in_line[0] == "x":
        file = "../find_mobile/xiaomi.csv"
    with open(file) as read_file:
        lst_line = [i.strip().split(",") for i in read_file.readlines()]

    if "plus" in in_line[1]:
        line_plus = in_line[1].replace("plus", "+")
    else:
        line_plus = in_line[1]
    
    for line in lst_line:
        if line[0] == in_line[1] or line[0] == line_plus:
            flag = True
            if len(in_line) == 4:
                line[1] = in_line[2]
                line[2] = in_line[3]
            elif len(in_line) == 3:
                line[1] = in_line[2]
                line[2] = int(in_line[2]) // 2
            elif len(in_line) == 2:
                line[1] = 1000
                line[2] = 100000

    if flag:
        with open(file, "w") as write_file:
            for i in lst_line:
                write_file.write(f"{i[0]},{i[1]},{i[2]}\n")
        return "ACCEPT"


class FSMAdmin(StatesGroup):
    name = State()


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
myselfserver = s.getsockname()[0]


def out(project):
    try:
        with open(f"../{project}/out.log") as file:
            return file.read()
    except:
        return "no file"


def rm_out(project):
    if os.path.exists(f"../{project}/out.log"):
        os.system(f"rm ../{project}/out.log")
        return f"out {project} deleted!"
    else:
        return "no file"


def cron():
    return list(CronTab(user="vladium"))


def installation_crontab():
    os.system(f'crontab -l > foocron; echo "@reboot /usr/bin/sleep 15; ssh vladium@{myselfserver} Xvfb &\n@reboot /usr/bin/sleep 20; cd /home/vladium/code/vladium_bot/ && /home/vladium/code/vladium_bot/lin_venv3104/bin/python3 /home/vladium/code/vladium_bot/bot.py >> out.log 2>&1\n# */10 * * * * cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/main.py >> out.log 2>&1\n# */10 * * * * cd /home/vladium/code/find_mobile/ && /home/vladium/code/find_mobile/lin_venv3104/bin/python3 /home/vladium/code/find_mobile/main.py >> out.log 2>&1\n# */5 * * * * cd /home/vladium/code/xypher/ && /home/vladium/code/xypher/env/bin/python3 /home/vladium/code/xypher/main.py >> out.log 2>&1" > foocron; crontab foocron; rm foocron')


try:
    cron()[0]
except:
    installation_crontab()


def kb():
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    return kb_client


b1 = KeyboardButton("Start kwork")
b2 = KeyboardButton("Start find_mobile")
b3 = KeyboardButton("Up kwork cron")
b4 = KeyboardButton("Up find_mobile cron")
b5 = KeyboardButton("Down kwork cron")
b6 = KeyboardButton("Down find_mobile cron")
b7 = KeyboardButton("Verify crontab")
b8 = KeyboardButton("Reboot server")
b9 = KeyboardButton("Menu")
b10 = KeyboardButton("Default cron")
b11 = KeyboardButton("Out kwork")
b12 = KeyboardButton("Out find_mobile")
b13 = KeyboardButton("Edit")
b14 = KeyboardButton("Clear")
b15 = KeyboardButton("Cancel")
b16 = KeyboardButton("Samsung")
b17 = KeyboardButton("Xiaomi")
b18 = KeyboardButton("Rm kwork out")
b19 = KeyboardButton("Rm find_mobile out")
b20 = KeyboardButton("Up xypher cron")
b21 = KeyboardButton("Down xypher cron")
b22 = KeyboardButton("Start xypher")
b23 = KeyboardButton("Out xypher")
b24 = KeyboardButton("Rm xypher out")


acl = (CHAT_ID, 5550131546)
admin_only = lambda message: message.from_user.id not in acl


def verify_cron_and_install_button():
    res = []
    cr = cron()
    if str(cr[2])[0] == "#":
        res.append(b3)
    else:
        res.append(b5)
    if str(cr[3])[0] == "#":
        res.append(b4)
    else:
        res.append(b6)
    if str(cr[4])[0] == "#":
        res.append(b20)
    else:
        res.append(b21)
    return res


async def verify(message):
    if str(cron()[2])[0] == "#":
        kwork = "DISABLE"
    else:
        kwork = "ENABLE"
    if str(cron()[3])[0] == "#":
        find_mobile = "DISABLE"
    else:
        find_mobile = "ENABLE"
    if str(cron()[4])[0] == "#":
        xypher = "DISABLE"
    else:
        xypher = "ENABLE"
    new_btn = verify_cron_and_install_button()
    await bot.send_message(message.from_user.id, f"kwork: {kwork}, find_mobile: {find_mobile}, xypher: {xypher}", reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))


def switch_cron(num_line, switch):
    os.system(f'crontab -l > foocron;')
    with open("./foocron") as file:
        text = file.readlines()
    if switch == "up":
        text[num_line] = text[num_line][2:]
    elif switch == "down":
        text[num_line] = "# " + text[num_line]
    with open("./foocron", "w") as f:
        for i in text:
            f.write(f"{i.strip()}\n")
    os.system(f'crontab foocron; rm foocron')


@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    return


@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await message.delete()
    btn = verify_cron_and_install_button()
    await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(btn[0], btn[1], btn[2]).row(b9))


@dp.message_handler()
async def send(message : types.Message):    
    if message.text == "Start kwork":
        await bot.send_message(message.from_user.id, "kwork is starting...", reply_markup=ReplyKeyboardRemove())
        await message.delete()
        os.system('cd /home/vladium/code/kwork/ && /home/vladium/code/kwork/lin_venv3104/bin/python3 /home/vladium/code/kwork/main.py >> out.log 2>&1')
        await bot.send_message(message.from_user.id, "kwork end!")
        await verify(message)
    elif message.text == "Start find_mobile":
        await bot.send_message(message.from_user.id, "find_mobile is starting...", reply_markup=ReplyKeyboardRemove())
        await message.delete()
        os.system('cd /home/vladium/code/find_mobile/ && /home/vladium/code/find_mobile/lin_venv3104/bin/python3 /home/vladium/code/find_mobile/main.py >> out.log 2>&1')
        await bot.send_message(message.from_user.id, "find_mobile end!")
        await verify(message)

    elif message.text == "Start xypher":
        await bot.send_message(message.from_user.id, "xypher is starting...", reply_markup=ReplyKeyboardRemove())
        await message.delete()
        os.system('cd /home/vladium/code/xypher/ && /home/vladium/code/xypher/env/bin/python3 /home/vladium/code/xypher/main.py >> out.log 2>&1')
        await bot.send_message(message.from_user.id, "xypher end!")
        await verify(message)

    elif message.text == "Verify crontab":
        await message.delete()
        await verify(message)
    elif message.text == "Reboot server":
        await message.delete()
        sudoPassword = '241215'
        command = 'reboot'
        os.system('echo %s|sudo -S %s' % (sudoPassword, command))

    elif message.text == "Menu":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "Menu", reply_markup=kb().row(b1, b2, b22).row(btn[0], btn[1], btn[2]).row(b11, b12, b23).row(b18, b19, b24).row(b7, b8).row(b16, b17).row(b10, b13, b14))
    
    elif message.text == "Up kwork cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb().row(btn[0], btn[1], btn[2]).row(b9))
        switch_cron(2, "up")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "kwork на cron ↑↑↑", reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    elif message.text == "Down kwork cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb().row(btn[0], btn[1], btn[2]).row(b9))
        switch_cron(2, "down")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "Down kwork cron ↓↓↓", reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    
    elif message.text == "Up find_mobile cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb().row(btn[0], btn[1], btn[2]).row(b9))
        switch_cron(3, "up")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "find_mobile на cron ↑↑↑", reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    elif message.text == "Down find_mobile cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb().row(btn[0], btn[1], btn[2]).row(b9))
        switch_cron(3, "down")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "Down find_mobile cron ↓↓↓", reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    
    elif message.text == "Up xypher cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↑↑↑", reply_markup=kb().row(btn[0], btn[1], btn[2]).row(b9))
        switch_cron(4, "up")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "xypher на cron ↑↑↑", reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    elif message.text == "Down xypher cron":
        await message.delete()
        btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "↓↓↓", reply_markup=kb().row(btn[0], btn[1], btn[2]).row(b9))
        switch_cron(4, "down")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "Down find_mobile cron ↓↓↓", reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
        
    elif message.text == "Out kwork":
        await message.delete()
        out_kwork = out("kwork")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, out_kwork, reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    elif message.text == "Rm kwork out":
        await message.delete()
        rm_kwork_out = rm_out("kwork")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, rm_kwork_out, reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))

    elif message.text == "Out find_mobile":
        await message.delete()
        out_find_mobile = out("find_mobile")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, out_find_mobile, reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    elif message.text == "Rm find_mobile out":
        await message.delete()
        rm_find_mobile_out = rm_out("find_mobile")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, rm_find_mobile_out, reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    
    elif message.text == "Out xypher":
        await message.delete()
        out_xypher = out("xypher")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, out_xypher, reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))
    elif message.text == "Rm xypher out":
        await message.delete()
        rm_xypher = rm_out("xypher")
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, rm_xypher, reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))

    elif message.text == "Default cron":
        await message.delete()
        installation_crontab()
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(new_btn[0], new_btn[1], new_btn[2]).row(b9))

    elif message.text == "Samsung":
        with open("../find_mobile/samsung.csv") as file:
            file = file.read()
        await bot.send_message(message.from_user.id, file)
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))
    elif message.text == "Xiaomi":
        with open("../find_mobile/xiaomi.csv") as file:
            file = file.read()
        await bot.send_message(message.from_user.id, file)
        new_btn = verify_cron_and_install_button()
        await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(new_btn[0], new_btn[1]).row(b9))
    elif message.text == "Clear":
        new_message_id = message.message_id
        for i in range(100):
            try:
                await bot.delete_message(chat_id=message.from_user.id, message_id=new_message_id)
            except Exception:
                pass
            new_message_id = new_message_id - 1
    elif message.text == "Edit":
        await FSMAdmin.name.set()
        await message.reply("Enter through the space: name(s or samsung) model max_price min_price", reply_markup=kb().row(b15))


@dp.message_handler(Text(equals="Cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    curent_state = await state.get_state()
    if curent_state is None:
        return
    await state.finish()
    btn = verify_cron_and_install_button()
    await message.reply("OK", reply_markup=kb().row(btn[0], btn[1]).row(b9))


@dp.message_handler(state=FSMAdmin.name)
async def load_model(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    btn = verify_cron_and_install_button()
    try:
        epl = edit_phone_list(data["name"])
        await message.reply(epl, reply_markup=kb().row(btn[0], btn[1]).row(b9))
    except:
        await message.reply("NO RESULT", reply_markup=kb().row(btn[0], btn[1]).row(b9))
        pass
    
    await state.finish()


executor.start_polling(dp, skip_updates=True)
