from __future__ import annotations

import logging
import asyncio

from config import ONEC_ENABLED, ONEC_CONNECTION_STRING

logger = logging.getLogger(__name__)

try:
    import pythoncom
    import win32com.client
    _COM_OK = True
except ImportError:
    _COM_OK = False


def _get_codes_sync(product_name, order_id, quantity):
    """Синхронный COM-вызов (выполняется в отдельном потоке через asyncio.to_thread)."""
    pythoncom.CoInitialize()
    try:
        connector = win32com.client.Dispatch("V83.COMConnector")
        ib = connector.Connect(ONEC_CONNECTION_STRING)
        result = ib.bl_BotAPI.GetCodes(str(product_name), str(order_id), int(quantity))
        return [c for c in str(result).split(";") if c]
    finally:
        pythoncom.CoUninitialize()


async def get_activation_code(product_name: str, order_id: str, quantity: int = 1) -> list:
    """
    Запрашивает коды активации из 1С после успешной оплаты.

    Returns:
        Список кодов, например ["1C-XXXX-1", "1C-XXXX-2"]
    """
    if not ONEC_ENABLED:
        logger.warning("1С отключена (ONEC_ENABLED=False) — выдаю тестовые коды")
        return [f"TEST-CODE-{order_id}-{i + 1}" for i in range(quantity)]
    if not _COM_OK:
        raise RuntimeError("pywin32 (COM) недоступен — бот должен работать на сервере с 1С")
    try:
        return await asyncio.to_thread(_get_codes_sync, product_name, order_id, quantity)
    except Exception as e:
        logger.error(f"Ошибка получения кодов из 1С через COM: {e}")
        raise


async def confirm_shipment(order_id: str, codes: list) -> bool:
    """
    Подтверждает в 1С, что коды выданы пользователю.
    ЗАГЛУШКА — добавим вызов 1С-функции подтверждения, когда заведём её в bl_BotAPI.
    """
    if not ONEC_ENABLED:
        return True
    return True


async def check_stock(product_name: str) -> int:
    """
    Проверяет наличие кодов в 1С (опционально, для показа пользователю).
    ЗАГЛУШКА — добавим функцию остатков в bl_BotAPI при необходимости.
    """
    if not ONEC_ENABLED:
        return -1
    return -1
