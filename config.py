from __future__ import annotations

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


BOT_TOKEN = _required("BOT_TOKEN")
GROUP_ID = int(_required("GROUP_ID"))

YUKASSA_SHOP_ID = os.getenv("YUKASSA_SHOP_ID", "")
YUKASSA_SECRET_KEY = os.getenv("YUKASSA_SECRET_KEY", "")

WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook/yukassa")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8080"))

ONEC_ENABLED = os.getenv("ONEC_ENABLED", "false").strip().lower() in ("1", "true", "yes")

ONEC_BASE_PATH = os.getenv("ONEC_BASE_PATH", "")
ONEC_USERNAME = os.getenv("ONEC_USERNAME", "")
ONEC_PASSWORD = os.getenv("ONEC_PASSWORD", "")

if ONEC_ENABLED and not ONEC_BASE_PATH:
    raise RuntimeError("ONEC_ENABLED=true, но не задан ONEC_BASE_PATH")

ONEC_CONNECTION_STRING = 'File="%s";Usr="%s";Pwd="%s";' % (
    ONEC_BASE_PATH,
    ONEC_USERNAME,
    ONEC_PASSWORD,
)
