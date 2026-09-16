from __future__ import annotations
# main.py
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import load_all_user_data
from handlers import (
    common_router,
    cabinet_router,
    products_router,
    payments_router,
    callbacks_router,
)
from webhook_handler import start_webhook_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(common_router)
dp.include_router(cabinet_router)
dp.include_router(products_router)
dp.include_router(payments_router)
dp.include_router(callbacks_router)


async def main():
    load_all_user_data()

    # Запускаем webhook-сервер и бота параллельно
    webhook_runner = await start_webhook_server(bot)

    logging.info("Бот запущен. Начало поллинга...")
    try:
        await dp.start_polling(bot)
    finally:
        await webhook_runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
    except Exception as e:
        logging.exception(f"Критическая ошибка: {e}")
