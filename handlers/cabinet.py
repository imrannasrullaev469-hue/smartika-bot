from __future__ import annotations
# handlers/cabinet.py
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import user_history, user_purchases, user_balance, user_referral_codes, user_referrals, save_user_data
from keyboards.reply import cabinet_keyboard
from utils import show_main_menu

cabinet_router = Router()

@cabinet_router.message(F.text == '👤 ЛИЧНЫЙ КАБИНЕТ')
async def personal_cabinet(message: types.Message):
    await message.answer(
        '**👤 Личный кабинет**\n\n'
        'Добро пожаловать! Здесь вы можете просмотреть свои покупки, баланс и рефералов.',
        parse_mode='Markdown',
        reply_markup=cabinet_keyboard()
    )

@cabinet_router.message(F.text == '📜 История заказов')
async def history_orders(message: types.Message):
    user_id = message.chat.id
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад в кабинет', callback_data='back_cabinet')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(2)

    if user_id in user_history and user_history[user_id]:
        response_text = '**📜 История заказов**\n\n'
        for i, order in enumerate(user_history[user_id], 1):
            response_text += f"{i}. {order['product']} × {order['quantity']} | {order['total']} руб. | {order['payment_method']} | {order['date']}\n"
        response_text += '\nВернуться в личный кабинет — используйте меню ниже.'
    else:
        response_text = '📭 У вас пока нет заказов.'

    await message.answer(response_text, parse_mode='Markdown', reply_markup=builder.as_markup())


@cabinet_router.message(F.text == '🎁 Мои лицензии и коды')
async def my_licenses(message: types.Message):
    user_id = message.chat.id
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад в кабинет', callback_data='back_cabinet')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(2)

    if user_id in user_purchases and user_purchases[user_id]:
        response_text = '**🎁 Мои лицензии и коды**\n\n'
        for i, item in enumerate(user_purchases[user_id], 1):
            response_text += f"{i}. {item['product']}\nКод: `{item['code']}`\nДата покупки: {item['date']}\n\n"
        response_text += 'Коды отправляются автоматически после оплаты.'
    else:
        response_text = '🎁 У вас пока нет купленных лицензий.'

    await message.answer(response_text, parse_mode='Markdown', reply_markup=builder.as_markup())


@cabinet_router.message(F.text == '💰 Баланс и пополнение')
async def balance(message: types.Message):
    user_id = message.chat.id
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад в кабинет', callback_data='back_cabinet')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(2)

    balance_val = user_balance.get(user_id, 0)
    response_text = f'**💰 Ваш баланс:** {balance_val} руб.\n\n' \
                    f'Пополнить баланс можно через оплату картой или другими способами в процессе покупки.\n' \
                    f'(В будущем добавим прямое пополнение)'

    await message.answer(response_text, parse_mode='Markdown', reply_markup=builder.as_markup())


@cabinet_router.message(F.text == '🤝 Реферальная система')
async def referral_system(message: types.Message):
    user_id = message.chat.id
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад в кабинет', callback_data='back_cabinet')
    builder.button(text='Назад в главное меню', callback_data='back_main')
    builder.adjust(2)

    if user_id not in user_referral_codes:
        user_referral_codes[user_id] = f"ref_{user_id}"
        save_user_data(user_id)
    ref_code = user_referral_codes[user_id]
    bot_username = (await message.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    referrals_count = len(user_referrals.get(user_id, []))
    response_text = f'**🤝 Реферальная система**\n\n' \
                    f'Ваша реферальная ссылка:\n{ref_link}\n\n' \
                    f'Приглашено рефералов: {referrals_count}\n' \
                    f'За каждого реферала, который совершит покупку, вы получите бонус на баланс (в разработке).'

    await message.answer(response_text, parse_mode='Markdown', reply_markup=builder.as_markup())