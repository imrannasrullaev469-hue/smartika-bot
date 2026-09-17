from __future__ import annotations
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Главное меню бота
    """
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text='АТОЛ SIGMA'),
        KeyboardButton(text='FRONTOL')
    )
    builder.row(
        KeyboardButton(text='ОФД'),
        KeyboardButton(text='КриптоПро')
    )
    builder.row(
        KeyboardButton(text='ОФЕРТА'),
        KeyboardButton(text='О НАС')
    )
    builder.row(
        KeyboardButton(text='👤 ЛИЧНЫЙ КАБИНЕТ')
    )

    builder.resize_keyboard = True

    return builder.as_markup()


def cabinet_keyboard() -> ReplyKeyboardMarkup:
    """
    Меню личного кабинета
    """
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text='📜 История заказов'),
        KeyboardButton(text='🎁 Мои лицензии и коды')
    )
    builder.row(
        KeyboardButton(text='💰 Баланс и пополнение'),
        KeyboardButton(text='🤝 Реферальная система')
    )
    builder.row(
        KeyboardButton(text='🔙 Назад в главное меню')
    )

    builder.resize_keyboard = True

    return builder.as_markup()
