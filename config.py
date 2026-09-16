from __future__ import annotations
# config.py
# ============================================================
# Все секреты читаются из переменных окружения (файл .env рядом с main.py).
# Шаблон со списком переменных — .env.example.
# Сам .env в репозиторий не попадает (см. .gitignore).
# ============================================================

import os

from dotenv import load_dotenv

load_dotenv()


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Не задана переменная окружения {name}. "
            f"Скопируй .env.example в .env и заполни значения."
        )
    return value


# ============================================================
# TELEGRAM
# Токен выдаёт @BotFather. GROUP_ID — чат менеджеров, куда падают
# уведомления о заказах (у групп id отрицательный).
# ============================================================
BOT_TOKEN = _required("BOT_TOKEN")
GROUP_ID = int(_required("GROUP_ID"))

# ============================================================
# ЮКАССА
# Получить в личном кабинете: yookassa.ru → Настройки → API
# ============================================================
YUKASSA_SHOP_ID = os.getenv("YUKASSA_SHOP_ID", "")
YUKASSA_SECRET_KEY = os.getenv("YUKASSA_SECRET_KEY", "")

# ============================================================
# WEBHOOK — публичный URL сервера.
# Нужен для получения уведомлений об оплате от ЮКассы.
# ============================================================
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook/yukassa")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Порт, на котором слушает webhook-сервер
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8080"))

# ============================================================
# 1С УНФ — подключение через COM (прямое соединение к файловой базе,
# в обход веб-сервиса/лицензии). Бот вызывает функцию 1С bl_BotAPI.GetCodes(...).
# РАБОТАЕТ ТОЛЬКО НА СЕРВЕРЕ, где лежит файловая база 1С.
# ============================================================
# ГЛАВНЫЙ ПЕРЕКЛЮЧАТЕЛЬ:
#   false — бот выдаёт ТЕСТОВЫЕ коды (TEST-CODE-...), 1С не нужна.
#   true  — бот берёт коды из 1С через COM-соединение.
ONEC_ENABLED = os.getenv("ONEC_ENABLED", "false").strip().lower() in ("1", "true", "yes")

# Путь к файловой базе 1С на сервере + пользователь 1С (НЕ Windows-учётка!).
ONEC_BASE_PATH = os.getenv("ONEC_BASE_PATH", "")
ONEC_USERNAME = os.getenv("ONEC_USERNAME", "")
ONEC_PASSWORD = os.getenv("ONEC_PASSWORD", "")

if ONEC_ENABLED and not ONEC_BASE_PATH:
    raise RuntimeError("ONEC_ENABLED=true, но не задан ONEC_BASE_PATH")

# Строка COM-соединения (собирается автоматически из настроек выше).
ONEC_CONNECTION_STRING = 'File="%s";Usr="%s";Pwd="%s";' % (
    ONEC_BASE_PATH,
    ONEC_USERNAME,
    ONEC_PASSWORD,
)
