from __future__ import annotations
# services/yukassa.py
# ============================================================
# МОДУЛЬ ЮКАССА
# Установка: pip install yookassa
# Документация: https://yookassa.ru/developers/api
# ============================================================

import uuid
import logging
from config import YUKASSA_SHOP_ID, YUKASSA_SECRET_KEY, WEBHOOK_HOST

logger = logging.getLogger(__name__)

# TODO: Раскомментировать после установки библиотеки и заполнения config.py
# from yookassa import Configuration, Payment
# Configuration.account_id = YUKASSA_SHOP_ID
# Configuration.secret_key = YUKASSA_SECRET_KEY


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
            "payment_id": "...",    # ID платежа в ЮКассе
            "payment_url": "...",   # Ссылка для оплаты
            "status": "pending"
        }
    """

    # ============================================================
    # TODO: ВСТАВИТЬ РЕАЛЬНЫЙ КОД ПОСЛЕ ПОЛУЧЕНИЯ КЛЮЧЕЙ
    # ============================================================
    # payment = Payment.create({
    #     "amount": {
    #         "value": f"{amount:.2f}",
    #         "currency": "RUB"
    #     },
    #     "confirmation": {
    #         "type": "redirect",
    #         "return_url": f"{WEBHOOK_HOST}/payment/success"
    #     },
    #     "capture": True,
    #     "description": description,
    #     "metadata": {
    #         "user_id": str(user_id),
    #         "order_id": order_id
    #     }
    # }, uuid.uuid4())
    #
    # return {
    #     "payment_id": payment.id,
    #     "payment_url": payment.confirmation.confirmation_url,
    #     "status": payment.status
    # }
    # ============================================================

    # ЗАГЛУШКА (удалить после подключения ЮКассы)
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

    # ============================================================
    # TODO: ВСТАВИТЬ РЕАЛЬНЫЙ КОД
    # ============================================================
    # payment = Payment.find_one(payment_id)
    # return payment.status
    # ============================================================

    logger.warning("ЮКасса не подключена — возвращается заглушка статуса")
    return "pending"


def verify_webhook_signature(body: bytes, signature: str) -> bool:
    """
    Проверяет подпись входящего webhook от ЮКассы.
    Вызывается в обработчике webhook перед обработкой события.
    """

    # ============================================================
    # TODO: ВСТАВИТЬ РЕАЛЬНУЮ ПРОВЕРКУ ПОДПИСИ
    # ============================================================
    # import hmac, hashlib
    # expected = hmac.new(
    #     YUKASSA_SECRET_KEY.encode(),
    #     body,
    #     hashlib.sha256
    # ).hexdigest()
    # return hmac.compare_digest(expected, signature)
    # ============================================================

    logger.warning("Проверка подписи webhook отключена — только для разработки!")
    return True
