from __future__ import annotations
from pathlib import Path

from aiogram import types
from aiogram.types import BufferedInputFile

from keyboards.reply import main_menu_keyboard


BASE_DIR = Path("/Users/smira/PycharmProjects/smartika")
ASSETS_DIR = BASE_DIR / "assets"


async def show_main_menu(message: types.Message, delete_previous: bool = True):

    if delete_previous:
        try:
            await message.delete()
        except:
            pass

    user_id = message.chat.id
    photo_path = ASSETS_DIR / "photo_5977733193811471396_x.jpg"

    try:
        with open(photo_path, "rb") as f:
            photo_bytes = f.read()

        photo = BufferedInputFile(
            file=photo_bytes,
            filename="main_menu.jpg"
        )

        await message.bot.send_photo(
            chat_id=user_id,
            photo=photo,
            caption=(
                "Привет! Я бот компании Smartika.\n"
                "Мы занимаемся продажей электронных лицензий 24/7.\n"
                "Чем могу помочь?"
            ),
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Ошибка при отправке главного фото: {e}")
        await message.answer(
            "Привет! Я бот компании Smartika.\n"
            "Мы занимаемся продажей электронных лицензий 24/7.\n"
            "Чем могу помочь?",
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown",
        )


async def edit_message_smart(
    message: types.Message,
    text: str,
    parse_mode: str = "Markdown",
    reply_markup: types.InlineKeyboardMarkup = None,
):
    try:
        await message.edit_caption(
            caption=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )
    except Exception:
        try:
            await message.edit_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
        except Exception as e:
            print(f"Не удалось отредактировать сообщение: {e}")
