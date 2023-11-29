from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Інформація 🧾",
        "Преміум 👑",
        "Посилання 🔗",
        "FAQ 👤"
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)
