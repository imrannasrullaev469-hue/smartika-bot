from __future__ import annotations
import sqlite3
import json
from threading import Lock

conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()
lock = Lock()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    cart TEXT,
    history TEXT,
    referral_code TEXT,
    referrals TEXT,
    balance INTEGER,
    purchases TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS pending_orders (
    order_id TEXT PRIMARY KEY,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

conn.commit()

user_cart = {}
user_history = {}
user_referral_codes = {}
user_referrals = {}
user_balance = {}
user_purchases = {}


def load_all_user_data():
    with lock:
        cursor.execute('SELECT * FROM users')
        for row in cursor.fetchall():
            user_id = row[0]
            user_cart[user_id] = json.loads(row[1]) if row[1] else {}
            user_history[user_id] = json.loads(row[2]) if row[2] else []
            user_referral_codes[user_id] = row[3]
            user_referrals[user_id] = json.loads(row[4]) if row[4] else []
            user_balance[user_id] = row[5] if row[5] is not None else 0
            user_purchases[user_id] = json.loads(row[6]) if row[6] else []


def save_user_data(user_id):
    with lock:
        cart_json = json.dumps(user_cart.get(user_id, {}))
        history_json = json.dumps(user_history.get(user_id, []))
        ref_code = user_referral_codes.get(user_id)
        referrals_json = json.dumps(user_referrals.get(user_id, []))
        balance = user_balance.get(user_id, 0)
        purchases_json = json.dumps(user_purchases.get(user_id, []))
        cursor.execute(
            '''INSERT OR REPLACE INTO users 
               (user_id, cart, history, referral_code, referrals, balance, purchases)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (user_id, cart_json, history_json, ref_code, referrals_json, balance, purchases_json)
        )
        conn.commit()


def save_pending_order(order_id: str, data: dict):
    with lock:
        cursor.execute(
            'INSERT OR REPLACE INTO pending_orders (order_id, data) VALUES (?, ?)',
            (order_id, json.dumps(data))
        )
        conn.commit()


def get_pending_order(order_id: str) -> dict | None:
    with lock:
        cursor.execute('SELECT data FROM pending_orders WHERE order_id = ?', (order_id,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None


def delete_pending_order(order_id: str):
    with lock:
        cursor.execute('DELETE FROM pending_orders WHERE order_id = ?', (order_id,))
        conn.commit()
