from __future__ import annotations

import uuid
import logging
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config import GROUP_ID
from database import user_cart, user_history, user_purchases, save_user_data, save_pending_order, get_pending_order, delete_pending_order
from datetime import datetime
from states import PaymentStates
from utils import edit_message_smart
from services.yukassa import create_payment
from services.onec import get_activation_code, confirm_shipment

payments_router = Router()
logger = logging.getLogger(__name__)


async def handle_payment_selection(query: types.CallbackQuery, state: FSMContext, data: str):
    user_id = query.message.chat.id
    product = user_cart[user_id]['product']
    quantity = user_cart[user_id]['quantity']
    price = user_cart[user_id]['price']
    total_price = price * quantity
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    payment_methods = {
        'payment_card': '💳 Оплата банковской картой (ЮКасса)',
        'payment_sbp': '📱 СБП (ЮКасса)',
        'payment_invoice': '🏢 По счету для юридических лиц',
        'payment_other': '💎 Другие способы оплаты'
    }
    payment_method = payment_methods.get(data, data)

    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].append({
        'product': product,
        'quantity': quantity,
        'total': total_price,
        'payment_method': payment_method,
        'date': current_date
    })
    save_user_data(user_id)

    if data in ('payment_card', 'payment_sbp'):
        await handle_yukassa_payment(query, product, quantity, price, total_price)

    elif data == 'payment_invoice':
        text = (
            f'**Оплата по счету B2B**\n\n'
            f'Товар: {product}\n'
            f'Количество: {quantity}\n'
            f'Сумма: {total_price} руб.\n\n'
            f'Для выставления счета отправьте реквизиты вашей компании\n'
            f'(ИНН, КПП, название организации, адрес):'
        )
        await edit_message_smart(query.message, text, 'Markdown', None)
        await state.set_state(PaymentStates.requisites)
        await state.update_data(product=product, quantity=quantity, total_price=total_price)

    elif data == 'payment_other':
        text = (
            f'**Другие способы оплаты**\n\n'
            f'Товар: {product}\n'
            f'Количество: {quantity}\n'
            f'Сумма: {total_price} руб.\n\n'
            f'Напишите предпочтительный способ оплаты и мы свяжемся с вами:'
        )
        await edit_message_smart(query.message, text, 'Markdown', None)
        await state.set_state(PaymentStates.payment_details)
        await state.update_data(product=product, quantity=quantity, total_price=total_price)

    if user_id in user_cart:
        del user_cart[user_id]
    save_user_data(user_id)


async def handle_yukassa_payment(
    query: types.CallbackQuery,
    product: str,
    quantity: int,
    price: int,
    total_price: int
):
    user_id = query.message.chat.id
    order_id = str(uuid.uuid4())

    try:
        payment = await create_payment(
            amount=float(total_price),
            description=f"{product} × {quantity}",
            user_id=user_id,
            order_id=order_id
        )

        save_pending_order(order_id, {
            "user_id": user_id,
            "product": product,
            "quantity": quantity,
            "total_price": total_price,
            "payment_id": payment["payment_id"]
        })

        text = (
            f'**Оплата через ЮКассу**\n\n'
            f'Товар: {product}\n'
            f'Количество: {quantity}\n'
            f'Сумма: {total_price} руб.\n\n'
            f'Нажмите кнопку для оплаты. После подтверждения платежа '
            f'коды активации будут отправлены автоматически.\n\n'
            f'🔗 [Перейти к оплате]({payment["payment_url"]})'
        )
        await edit_message_smart(query.message, text, 'Markdown', None)

    except Exception as e:
        logger.error(f"Ошибка создания платежа ЮКасса: {e}")
        await query.message.answer(
            '❌ Ошибка при создании платежа. Попробуйте позже или свяжитесь с поддержкой.'
        )


async def process_yukassa_webhook(event: dict, bot: Bot):
    """
    Вызывается когда ЮКасса присылает уведомление об оплате.
    Подключить в webhook_handler.py
    """

    event_type = event.get("event")

    if event_type != "payment.succeeded":
        return

    payment_obj = event.get("object", {})
    payment_id = payment_obj.get("id")
    metadata = payment_obj.get("metadata", {})
    order_id = metadata.get("order_id")

    if not order_id:
        logger.error(f"Webhook: нет order_id в metadata платежа {payment_id}")
        return

    order = get_pending_order(order_id)
    if not order:
        logger.error(f"Webhook: заказ {order_id} не найден в БД")
        return

    user_id = order["user_id"]
    product = order["product"]
    quantity = order["quantity"]

    try:
        codes = await get_activation_code(
            product_name=product,
            order_id=order_id,
            quantity=quantity
        )

        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if user_id not in user_purchases:
            user_purchases[user_id] = []

        for code in codes:
            user_purchases[user_id].append({
                'product': product,
                'code': code,
                'date': current_date
            })
        save_user_data(user_id)

        codes_text = '\n'.join([f'`{code}`' for code in codes])
        await bot.send_message(
            user_id,
            f'✅ **Оплата получена!**\n\n'
            f'Товар: {product}\n'
            f'Количество: {quantity}\n\n'
            f'**Ваши коды активации:**\n{codes_text}\n\n'
            f'Коды также сохранены в разделе "🎁 Мои лицензии и коды".',
            parse_mode='Markdown'
        )

        await confirm_shipment(order_id=order_id, codes=codes)

        await bot.send_message(
            GROUP_ID,
            f'✅ Заказ выполнен!\n'
            f'Пользователь: {user_id}\n'
            f'Товар: {product} × {quantity}\n'
            f'Сумма: {order["total_price"]} руб.\n'
            f'Order ID: {order_id}\n'
            f'Коды выданы: {len(codes)} шт.'
        )

        delete_pending_order(order_id)

    except Exception as e:
        logger.error(f"Ошибка обработки webhook для заказа {order_id}: {e}")
        await bot.send_message(
            GROUP_ID,
            f'❌ ОШИБКА выдачи кодов!\n'
            f'Order ID: {order_id}\n'
            f'Пользователь: {user_id}\n'
            f'Товар: {product}\n'
            f'Ошибка: {e}\n\n'
            f'Требуется ручная обработка!'
        )
        await bot.send_message(
            user_id,
            '⚠️ Оплата получена, но возникла техническая ошибка при выдаче кодов. '
            'Менеджер свяжется с вами в ближайшее время.'
        )


@payments_router.message(StateFilter(PaymentStates.requisites))
async def handle_invoice_requisites(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product = data['product']
    quantity = data['quantity']
    total_price = data['total_price']
    requisites = message.text

    await message.answer(
        f'✅ Реквизиты получены!\n\n'
        f'Счет на {total_price} руб. за {product} × {quantity} будет '
        f'подготовлен и отправлен в течение рабочего дня.'
    )
    await message.bot.send_message(
        GROUP_ID,
        f'📄 Новый запрос счёта B2B\n'
        f'Пользователь: {message.chat.id}\n'
        f'Товар: {product} × {quantity}\n'
        f'Сумма: {total_price} руб.\n'
        f'Реквизиты:\n{requisites}'
    )
    await state.clear()


@payments_router.message(StateFilter(PaymentStates.payment_details))
async def handle_other_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product = data['product']
    quantity = data['quantity']
    total_price = data['total_price']
    details = message.text

    await message.answer('✅ Запрос принят! Менеджер свяжется с вами.')
    await message.bot.send_message(
        GROUP_ID,
        f'💎 Нестандартный способ оплаты\n'
        f'Пользователь: {message.chat.id}\n'
        f'Товар: {product} × {quantity}\n'
        f'Сумма: {total_price} руб.\n'
        f'Детали: {details}'
    )
    await state.clear()
