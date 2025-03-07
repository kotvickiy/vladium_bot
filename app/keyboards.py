from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]], resize_keyboard=True)

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Новости', url='https://dzen.ru')],
    [InlineKeyboardButton(text='E1', url='https://e1.ru')],
    [InlineKeyboardButton(text='4pda', url='https://4pda.to')]
    ])
