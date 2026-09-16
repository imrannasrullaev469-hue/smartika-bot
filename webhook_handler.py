from __future__ import annotations
# webhook_handler.py
# ============================================================
# Сервер для приёма webhook-уведомлений от ЮКассы
# Запускается параллельно с ботом
# Установка: pip install aiohttp
# ============================================================

import json
import logging
from aiohttp import web
from aiogram import Bot

from config import WEBHOOK_PATH, WEBHOOK_PORT
from services.yukassa import verify_webhook_signature
from handlers.payments import process_yukassa_webhook

logger = logging.getLogger(__name__)


async def yukassa_webhook_handler(request: web.Request) -> web.Response:
    """Принимает POST-запросы от ЮКассы"""

    # Проверяем подпись (раскомментировать после подключения ЮКассы)
    # signature = request.headers.get("X-Request-Signature", "")
    # body = await request.read()
    # if not verify_webhook_signature(body, signature):
    #     logger.warning("Неверная подпись webhook от ЮКассы!")
    #     return web.Response(status=400, text="Invalid signature")

    try:
        body = await request.read()
        event = json.loads(body)
        logger.info(f"Получен webhook от ЮКассы: {event.get('event')}")

        bot: Bot = request.app["bot"]
        await process_yukassa_webhook(event, bot)

        return web.Response(status=200, text="OK")

    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return web.Response(status=500, text="Internal error")


def create_webhook_app(bot: Bot) -> web.Application:
    """Создаёт aiohttp приложение с маршрутом webhook"""
    app = web.Application()
    app["bot"] = bot
    app.router.add_post(WEBHOOK_PATH, yukassa_webhook_handler)
    return app


async def start_webhook_server(bot: Bot):
    """Запускает webhook-сервер"""
    app = create_webhook_app(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=WEBHOOK_PORT)
    await site.start()
    logger.info(f"Webhook-сервер запущен на порту {WEBHOOK_PORT}")
    logger.info(f"Путь: {WEBHOOK_PATH}")
    return runner
