from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters import Text, Command

from keyboards import keyboard, keyboard1, mouse_325, mouse_535
from main import bot, dp
from config import CHAT_ID


async def send_hello(dp):
    await bot.send_message(chat_id=CHAT_ID, text="Start vladium_bot")


@dp.message_handler(Command("shop"))
async def show_shop(message: Message):
    await message.answer("Shop", reply_markup=keyboard)


@dp.message_handler(Text(equals=["btn1", "btn2", "btn3"]))
async def get_goods(message: Message):
    await message.answer(message.text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Command("tshop"))
async def show(message: Message):
    await message.answer(text="Купить или отенить", reply_markup=keyboard1)


@dp.callback_query_handler(text_contains="mouse325")
async def mouse325(call: CallbackQuery):
    await call.answer(cache_time=60)

    await call.message.answer("Купить", reply_markup=mouse_325)


@dp.callback_query_handler(text_contains="mouse535")
async def mouse535(call: CallbackQuery):
    await call.answer(cache_time=60)

    await call.message.answer("Купить", reply_markup=mouse_535)


@dp.callback_query_handler(text_contains="cancel")
async def cancel(call: CallbackQuery):
    await call.answer("Отмена", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)


