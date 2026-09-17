from __future__ import annotations
from .common import common_router
from .cabinet import cabinet_router
from .products import products_router
from .payments import payments_router
from .callbacks import callbacks_router

__all__ = [
    "common_router",
    "cabinet_router",
    "products_router",
    "payments_router",
    "callbacks_router",
]
