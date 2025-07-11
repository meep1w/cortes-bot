import sqlite3

conn = sqlite3.connect("../bot_database.db")
cursor = conn.cursor()

# Таблица пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    language TEXT DEFAULT 'ru',
    registered INTEGER DEFAULT 0,
    deposited INTEGER DEFAULT 0,
    blocked INTEGER DEFAULT 0
)
""")
conn.commit()

# Таблица рефссылки и промокода
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    ref_link TEXT,
    promo_code TEXT
)
""")
conn.commit()

# Если ещё нет настроек, добавляем
cursor.execute("SELECT COUNT(*) FROM settings")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO settings (id, ref_link, promo_code) VALUES (1, ?, ?)", (
        "https://1wcjlr.com/casino/list?open=register&p=rvcf",
        "C0RTES"
    ))
    conn.commit()


def add_user(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()


def get_user(user_id):
    cursor.execute("select * from users where user_id = ?", (user_id,))
    user = cursor.fetchone()
    return user if user is not None else None


def update_language(user_id, lang):
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
    conn.commit()


def get_language(user_id):
    cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else "ru"


def set_registered(user_id):
    cursor.execute("UPDATE users SET registered = 1 WHERE user_id = ?", (user_id,))
    conn.commit()


def is_registered(user_id):
    cursor.execute("SELECT registered FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return bool(row and row[0])


def update_deposited(user_id):
    cursor.execute("UPDATE users SET deposited = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    cursor.close()


def get_deposit(user_id):
    cursor.execute("SELECT deposited FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row if row is not None else None


def get_stats():
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE registered = 1")
    registered = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE blocked = 1")
    blocked = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE deposited = 1")
    deposited = cursor.fetchone()[0]
    return total, registered, deposited, blocked


def set_blocked(user_id):
    cursor.execute("UPDATE users SET blocked = 1 WHERE user_id = ?", (user_id,))
    conn.commit()


def update_settings(ref_link, promo_code):
    cursor.execute("UPDATE settings SET ref_link = ?, promo_code = ? WHERE id = 1", (ref_link, promo_code))
    conn.commit()


def get_settings():
    cursor.execute("SELECT ref_link, promo_code FROM settings WHERE id = 1")
    return cursor.fetchone()

def update(param, value):
    try:
        cursor.execute(f"update settings set {param} = ? where id = 1", (value, ))
        conn.commit()
        return True
    except Exception as e:
        return False
