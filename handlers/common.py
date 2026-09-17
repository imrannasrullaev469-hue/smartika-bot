from __future__ import annotations
from aiogram import Router, types, F
from aiogram.filters import Command

from config import GROUP_ID
from database import user_balance, user_cart, user_history, user_referrals, user_purchases, save_user_data
from keyboards.reply import cabinet_keyboard
from utils import show_main_menu

common_router = Router()

@common_router.message(Command(commands=['start']))
async def start(message: types.Message):
    user_id = message.chat.id
    args = message.text.split()
    if len(args) > 1 and args[1].startswith('ref_'):
        referrer_id = int(args[1][4:])
        if referrer_id != user_id:
            if referrer_id not in user_referrals:
                user_referrals[referrer_id] = []
            if user_id not in user_referrals[referrer_id]:
                user_referrals[referrer_id].append(user_id)
                save_user_data(referrer_id)
                await message.bot.send_message(referrer_id, f"🎉 Новый реферал! Пользователь {message.from_user.username or user_id} зарегистрировался по вашей ссылке.")

    if user_id not in user_balance:
        user_balance[user_id] = 0
        user_cart[user_id] = {}
        user_history[user_id] = []
        user_referrals[user_id] = []
        user_purchases[user_id] = []
        save_user_data(user_id)

    await show_main_menu(message, delete_previous=False)

@common_router.message(Command(commands=['testgroup']))
async def test_group(message: types.Message):
    try:
        await message.bot.send_message(GROUP_ID, "Тестовое сообщение из бота. Если видишь — всё работает!")
        await message.reply("Тест отправлен в группу")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

@common_router.message(F.text == '🔙 Назад в главное меню')
async def back_to_main(message: types.Message):
    await show_main_menu(message)
