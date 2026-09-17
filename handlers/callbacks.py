from __future__ import annotations
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from database import user_cart, save_user_data
from keyboards.inline import quantity_inline, payment_inline, ofd_taxcom_inline, ofd_platform_inline, ofd_ofdru_inline
from states import CallbackRequestStates
from utils import show_main_menu, edit_message_smart
from handlers.payments import handle_payment_selection
from config import GROUP_ID
from .cabinet import personal_cabinet

callbacks_router = Router()

@callbacks_router.callback_query()
async def callback_handler(query: types.CallbackQuery, state: FSMContext):
    data = query.data
    user_id = query.message.chat.id

    if data == 'back_main':
        await show_main_menu(query.message)
        return

    if data == 'back_cabinet':
        await query.message.delete()
        await personal_cabinet(query.message)
        return

    sigma_products = {
        'sigma_start': {'name': 'SIGMA СТАРТ 1 год', 'price': 5900},
        'sigma_razvitie': {'name': 'SIGMA РАЗВИТИЕ 1 год', 'price': 7900},
        'sigma_business': {'name': 'SIGMA БИЗНЕС 1 год', 'price': 15900},
        'sigma_marking': {'name': 'SIGMA модуль "Маркировка" 1 год', 'price': 6900}
    }
    if data in sigma_products:
        await handle_product_selection(query, sigma_products[data])
        return

    frontol_products = {
        'frontol_basic': {'name': 'ПО Frontol - Тариф "Базовый" на 1 год', 'price': 7000},
        'frontol_full': {'name': 'ПО Frontol - Тариф "Полный" на 1 год', 'price': 14000},
        'frontol_selfie': {'name': 'Модуль Frontol 6 Selfie на 1 год', 'price': 15000},
        'frontol_driver': {'name': 'ПО Frontol Driver Unit', 'price': 5000},
        'frontol_terminal': {'name': 'ПО Frontol Driver Unit для терминальных сессий', 'price': 15000}
    }
    if data in frontol_products:
        await handle_product_selection(query, frontol_products[data])
        return

    ofd_categories = {
        'ofd_category_taxcom': {
            'name': 'ТАКСКОМ',
            'description': 'Коды ОФД на подключение новых и продления текущих тарифов ОФД на каждую кассу.',
            'markup': ofd_taxcom_inline()
        },
        'ofd_category_platform': {
            'name': 'ПЛАТФОРМА ОФД',
            'description': 'Коды ОФД на подключение новых и продления текущих тарифов ОФД на каждую кассу.',
            'markup': ofd_platform_inline()
        },
        'ofd_category_ofdru': {
            'name': 'OFD.ru',
            'description': 'Коды ОФД на подключение новых и продления текущих тарифов ОФД на каждую кассу.',
            'markup': ofd_ofdru_inline()
        }
    }
    if data in ofd_categories:
        category = ofd_categories[data]
        text = f'**{category["name"]}**\n\n{category["description"]}'
        await edit_message_smart(query.message, text, 'Markdown', category['markup'])
        return

    ofd_products = {
        'ofd_taxcom_15': {'name': 'ОФД Такском на 15 мес.', 'price': 3000},
        'ofd_taxcom_36': {'name': 'ОФД Такском на 36 мес.', 'price': 7000},
        'ofd_platform_13': {'name': 'Платформа ОФД на 13 мес.', 'price': 3000},
        'ofd_platform_15': {'name': 'Платформа ОФД на 15 мес.', 'price': 3500},
        'ofd_platform_36': {'name': 'Платформа ОФД на 36 мес.', 'price': 7000},
        'ofd_ofdru_12': {'name': 'OFD.ru на 12 мес.', 'price': 3000},
        'ofd_ofdru_15': {'name': 'OFD.ru на 15 мес.', 'price': 3500},
        'ofd_ofdru_36': {'name': 'OFD.ru на 36 мес.', 'price': 7000}
    }
    if data in ofd_products:
        await handle_product_selection(query, ofd_products[data])
        return

    if data == 'crypto_pro':
        product = {'name': 'КриптоПро бессрочная на 1 рабочее место', 'price': 4000}
        await handle_product_selection(query, product)
        return

    quantity_map = {
        'quantity_1': 1,
        'quantity_2': 2,
        'quantity_3': 3,
        'quantity_5': 5,
        'quantity_10': 10
    }
    if data in quantity_map and user_id in user_cart:
        await handle_quantity_selection(query, quantity_map[data])
        return

    if data.startswith('payment_') and user_id in user_cart:
        await handle_payment_selection(query, state, data)
        return

    if data == 'callback_request':
        await query.message.answer(
            '**Заказать звонок**\n\n'
            'Менеджер свяжется с Вами в рабочие дни по МСК с 10:00 до 20:00\n\n'
            'Введите ваше имя:',
            parse_mode='Markdown'
        )
        await state.set_state(CallbackRequestStates.name)
        return

@callbacks_router.message(StateFilter(CallbackRequestStates.name))
async def ask_phone_for_callback(message: types.Message, state: FSMContext):
    user_name = message.text
    await state.update_data(user_name=user_name)
    await message.answer(f'Спасибо, {user_name}! Теперь введите ваш номер телефона:')
    await state.set_state(CallbackRequestStates.phone)

@callbacks_router.message(StateFilter(CallbackRequestStates.phone))
async def save_callback_request(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_name = data['user_name']
    user_phone = message.text
    await message.answer(
        f'✅ Заявка на звонок принята!\n\n'
        f'Имя: {user_name}\n'
        f'Телефон: {user_phone}\n\n'
        f'Менеджер свяжется с вами в рабочие дни с 10:00 до 20:00 по МСК.'
    )
    await message.bot.send_message(
        GROUP_ID,
        f'Новая заявка на звонок:\n'
        f'Имя: {user_name}\n'
        f'Телефон: {user_phone}\n'
        f'Пользователь ID: {message.chat.id}'
    )
    await state.clear()

async def handle_product_selection(query: types.CallbackQuery, product: dict):
    user_id = query.message.chat.id
    user_cart[user_id] = {
        'product': product['name'],
        'price': product['price'],
        'quantity': 1
    }
    save_user_data(user_id)
    text = f'**Лицензия: {product["name"]}**\n\n' \
           f'**Цена: {product["price"]} руб.**\n\n' \
           f'Выберите количество лицензий, которые хотите купить:'
    await edit_message_smart(query.message, text, 'Markdown', quantity_inline())

async def handle_quantity_selection(query: types.CallbackQuery, quantity: int):
    user_id = query.message.chat.id
    user_cart[user_id]['quantity'] = quantity
    save_user_data(user_id)
    product = user_cart[user_id]['product']
    price = user_cart[user_id]['price']
    total_price = price * quantity
    text = f'**Вы выбрали:**\n' \
           f'Товар: {product}\n' \
           f'Количество: {quantity}\n' \
           f'Цена за единицу: {price} руб.\n' \
           f'**Итого к оплате: {total_price} руб.**\n\n' \
           f'Выберите способ оплаты:'
    await edit_message_smart(query.message, text, 'Markdown', payment_inline())
