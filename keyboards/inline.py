from __future__ import annotations
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def atol_sigma_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='SIGMA СТАРТ 1 год, 5900 руб.', callback_data='sigma_start')
    builder.button(text='SIGMA РАЗВИТИЕ 1 год, 7900 руб.', callback_data='sigma_razvitie')
    builder.button(text='SIGMA БИЗНЕС 1 год, 15 900 руб.', callback_data='sigma_business')
    builder.button(text='SIGMA модуль "Маркировка" 1 год, 6900 руб.', callback_data='sigma_marking')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def frontol_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='ПО Frontol - Тариф "Базовый" на 1 год - 7 000 руб.', callback_data='frontol_basic')
    builder.button(text='ПО Frontol - Тариф "Полный" на 1 год - 14 000 руб.', callback_data='frontol_full')
    builder.button(text='Модуль Frontol 6 Selfie на 1 год - 15 000 руб.', callback_data='frontol_selfie')
    builder.button(text='ПО Frontol Driver Unit - 5 000 руб.', callback_data='frontol_driver')
    builder.button(text='ПО Frontol Driver Unit для терминальных сессий - 15 000 руб.', callback_data='frontol_terminal')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def ofd_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='ТАКСКОМ', callback_data='ofd_category_taxcom')
    builder.button(text='ПЛАТФОРМА ОФД', callback_data='ofd_category_platform')
    builder.button(text='OFD.ru', callback_data='ofd_category_ofdru')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def cryptopro_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='КриптоПро бессрочная на 1 рабочее место - 4 000 руб.', callback_data='crypto_pro')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def oferta_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def about_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='📞 Заказать звонок', callback_data='callback_request')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def ofd_taxcom_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='ОФД Такском на 15 мес. - 3000 руб.', callback_data='ofd_taxcom_15')
    builder.button(text='ОФД Такском на 36 мес. - 7000 руб.', callback_data='ofd_taxcom_36')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def ofd_platform_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Платформа ОФД на 13 мес. - 3000 руб.', callback_data='ofd_platform_13')
    builder.button(text='Платформа ОФД на 15 мес. - 3500 руб.', callback_data='ofd_platform_15')
    builder.button(text='Платформа ОФД на 36 мес. - 7000 руб.', callback_data='ofd_platform_36')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def ofd_ofdru_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='OFD.ru на 12 мес. - 3000 руб.', callback_data='ofd_ofdru_12')
    builder.button(text='OFD.ru на 15 мес. - 3500 руб.', callback_data='ofd_ofdru_15')
    builder.button(text='OFD.ru на 36 мес. - 7000 руб.', callback_data='ofd_ofdru_36')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()


def quantity_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='1', callback_data='quantity_1')
    builder.button(text='2', callback_data='quantity_2')
    builder.button(text='3', callback_data='quantity_3')
    builder.button(text='5', callback_data='quantity_5')
    builder.button(text='10', callback_data='quantity_10')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(5, 1)
    return builder.as_markup()


def payment_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='💳 Оплата картой', callback_data='payment_card')
    builder.button(text='📱 СБП (Сбер)', callback_data='payment_sbp')
    builder.button(text='🏢 По счету B2B', callback_data='payment_invoice')
    builder.button(text='💎 Другие способы', callback_data='payment_other')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(1)
    return builder.as_markup()
