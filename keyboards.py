from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


URL_M325 = r"https://www.dns-shop.ru/product/d7260b9428d73330/mys-besprovodnaa-logitech-wireless-mouse-m325-seryj/"
URL_M535 = r"https://www.dns-shop.ru/product/8899aa97c88f3361/mys-besprovodnaa-logitech-m535-seryj-910-004530/"

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="btn1"),
            KeyboardButton(text="btn2")
        ],
        [
            KeyboardButton(text="btn3")
        ]
    ],
    resize_keyboard=True
)


callback = CallbackData("buy", "id", "name", "price")

keyboard1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Logitech M325", callback_data="buy:8105885:mouse325:2199"),
            InlineKeyboardButton(text="Logitech M535", callback_data="buy:1044631:mouse535:3299")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ]
)

mouse_325 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Купить", url=URL_M325)
        ]
    ]
)

mouse_535 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Купить", url=URL_M535)
        ]
    ]
)

