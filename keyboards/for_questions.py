from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types, F


def login() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Отправить мой контакт', request_contact=True, reresize_keyboard=True)
    return kb.as_markup(reresize_keyboard=True)

