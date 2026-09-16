from __future__ import annotations
# handlers/products.py
from pathlib import Path
from aiogram import Router, types, F
from aiogram.types import BufferedInputFile

from keyboards.inline import atol_sigma_inline, frontol_inline, ofd_inline, cryptopro_inline, oferta_inline, about_inline
from utils import ASSETS_DIR

products_router = Router()

@products_router.message(F.text == 'АТОЛ SIGMA')
async def atol_sigma(message: types.Message):
    caption = '**АТОЛ SIGMA**\n\n' \
              'Покупайте лицензии на программное обеспечение АТОЛ Sigma ежегодно у нас.\n\n' \
              '✅ Быстрая отгрузка 24/7\n\n' \
              'Описание и сравнение тарифов: https://sigma.ru/tarify'

    photo_path = ASSETS_DIR / 'photo_2025-12-17 10.23.39.jpg'
    try:
        with open(photo_path, "rb") as f:
            photo_bytes = f.read()
        photo = BufferedInputFile(photo_bytes, filename="sigma.jpg")
        await message.answer_photo(photo=photo, caption=caption, parse_mode='Markdown', reply_markup=atol_sigma_inline())
    except Exception as e:
        print(f"Ошибка отправки фото SIGMA: {e}")
        await message.answer(caption, parse_mode='Markdown', reply_markup=atol_sigma_inline())

@products_router.message(F.text == 'FRONTOL')
async def frontol(message: types.Message):
    caption = '**FRONTOL**\n\n' \
              'Покупайте лицензии на программное обеспечение FRONTOL ежегодно у нас.\n\n' \
              '✅ Быстрая отгрузка 24/7\n\n' \
              'Описание лицензий и сравнение тарифов: https://frontol.ru/catalog/frontol-6/'

    photo_path = ASSETS_DIR / '2025-12-17 10.56.31.jpg'
    try:
        with open(photo_path, "rb") as f:
            photo_bytes = f.read()
        photo = BufferedInputFile(photo_bytes, filename="frontol.jpg")
        await message.answer_photo(photo=photo, caption=caption, parse_mode='Markdown', reply_markup=frontol_inline())
    except Exception as e:
        print(f"Ошибка отправки фото FRONTOL: {e}")
        await message.answer(caption, parse_mode='Markdown', reply_markup=frontol_inline())

@products_router.message(F.text == 'ОФД')
async def ofd(message: types.Message):
    caption = '**ОФД**\n\n' \
              'Коды ОФД на подключение новых и продления текущих тарифов ОФД на каждую кассу.'

    photo_path = ASSETS_DIR / '2025-12-17 10.57.57.jpg'
    try:
        with open(photo_path, "rb") as f:
            photo_bytes = f.read()
        photo = BufferedInputFile(photo_bytes, filename="ofd.jpg")
        await message.answer_photo(photo=photo, caption=caption, parse_mode='Markdown', reply_markup=ofd_inline())
    except Exception as e:
        print(f"Ошибка отправки фото OFD: {e}")
        await message.answer(caption, parse_mode='Markdown', reply_markup=ofd_inline())

@products_router.message(F.text == 'КриптоПро')
async def cryptopro(message: types.Message):
    await message.answer(
        '**КриптоПро**\n\n'
        'Лицензия на право использования СКЗИ КриптоПро CSP версии 5.0 '
        '(БЕССРОЧНАЯ ЛИЦЕНЗИЯ на 1 рабочее место)',
        parse_mode='Markdown',
        reply_markup=cryptopro_inline()
    )

@products_router.message(F.text == 'ОФЕРТА')
async def oferta(message: types.Message):
    await message.answer(
        '**ОФЕРТА**\n\n'
        '1. Покупатель вправе отказаться от заказа ПО до момента его оплаты.\n\n'
        '2. Отказ от ПО после оплаты невозможен, т.к. лицензии и коды активации '
        'имеют индивидуальные характеристики и не могут быть использованы '
        'повторно после отгрузки в телеграмм покупателю.\n\n'
        '3. Оплата происходит через интернет-эквайринг, чек об оплате высылается '
        'на E-mail, указанный покупателем при оплате.\n\n'
        '4. Коды активации, номера лицензий ПО отгружаются 24/7 непосредственно '
        'в телеграмм в окне бота.\n\n'
        '5. Телеграмм-бот работает автоматически в режиме 24/7.',
        parse_mode='Markdown',
        reply_markup=oferta_inline()
    )

@products_router.message(F.text == 'О НАС')
async def about_us(message: types.Message):
    await message.answer(
        '**О НАС**\n\n'
        'Команда энтузиастов, которая живет целью сделать отгрузки электронных '
        'лицензий, кодов активаций - моментальными, 24/7, а мир - интеллектуальным и удобным.\n\n'
        '**Также, к нам можно обращаться по следующим вопросам:**\n\n'
        '✅ NEW! Все виды страхования: коммерческое и личное\n'
        '✅ NEW! Продвижение личного бренда собственника в СМИ\n'
        '✅ Открытие ИП и ООО\n'
        '✅ 1С: любые лицензии, дополнительные лицензии на РМ\n'
        '✅ Онлайн-кассы\n'
        '✅ Весовое оборудование\n'
        '✅ Принтеры печати этикеток\n'
        '✅ Сканеры ШК\n'
        '✅ Терминалы сбора данных\n'
        '✅ Программное обеспечение для ТСД (Склад 15, DataMobile, Курьер, Клеверенс и др.)\n'
        '✅ POS-системы, сенсорные моноблоки\n'
        '✅ Кассы самообслуживания\n'
        '✅ Счетчики и детекторы банкнот\n'
        '✅ ЭЦП, ЭДО, отчетность, маркировка, честный знак\n'
        '✅ Гарантийный и постгарантийный ремонт оборудования АТОЛ, Эвотор\n'
        '✅ Бухгалтерские услуги (акцент на розничной торговле)',
        parse_mode='Markdown',
        reply_markup=about_inline()
    )