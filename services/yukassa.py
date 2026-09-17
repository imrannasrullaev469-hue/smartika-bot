from __future__ import annotations

import uuid
import logging
from config import YUKASSA_SHOP_ID, YUKASSA_SECRET_KEY, WEBHOOK_HOST

logger = logging.getLogger(__name__)


async def create_payment(amount: float, description: str, user_id: int, order_id: str) -> dict:
    """
    Создаёт платёж в ЮКассе и возвращает ссылку на оплату.

    Args:
        amount: Сумма в рублях (например 5900.0)
        description: Описание товара
        user_id: Telegram ID пользователя
        order_id: Уникальный ID заказа

    Returns:
        {
            "payment_id": "...",
            "payment_url": "...",
            "status": "pending"
        }
    """
    logger.warning("ЮКасса не подключена — используется заглушка!")
    return {
        "payment_id": f"fake_{order_id}",
        "payment_url": "https://yookassa.ru/ЗАГЛУШКА",
        "status": "pending"
    }


async def check_payment_status(payment_id: str) -> str:
    """
    Проверяет статус платежа.

    Returns:
        "succeeded" | "pending" | "canceled"
    """
    logger.warning("ЮКасса не подключена — возвращается заглушка статуса")
    return "pending"


def verify_webhook_signature(body: bytes, signature: str) -> bool:
    """
    Проверяет подпись входящего webhook от ЮКассы.
    Вызывается в обработчике webhook перед обработкой события.
    """
    logger.warning("Проверка подписи webhook отключена — только для разработки!")
    return True
