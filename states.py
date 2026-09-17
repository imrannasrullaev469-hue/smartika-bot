from __future__ import annotations
from aiogram.fsm.state import StatesGroup, State

class CallbackRequestStates(StatesGroup):
    name = State()
    phone = State()

class PaymentStates(StatesGroup):
    requisites = State()
    payment_details = State()
