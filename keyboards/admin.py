from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def admin_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    keyboard = [
        "Статистика 📊",
        "Розсилка 📢",
        "Всі Користувачі 👥",
        "Всі Кориистувачі 👑",
        "Користувачі що не мали 👑",
    ]

    for button in keyboard:
        builder.add(KeyboardButton(text=button, callback_data=button))

    return builder.adjust(2).as_markup(resize_keyboard=True)


def send_alarm() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    keyboard = ["Всім 👥", "Особисто 👤", "Преміум 👑"]

    for button in keyboard:
        builder.add(InlineKeyboardButton(text=button, callback_data=button))

    return builder.adjust(1).as_markup(resize_keyboard=True)
