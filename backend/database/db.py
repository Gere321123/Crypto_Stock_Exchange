import sqlite3

def get_db_connection():
    return sqlite3.connect("cryptostock.db")

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT UNIQUE NOT NULL,
                         password TEXT NOT NULL,
                         isadmin BOOLEAN NOT NULL CHECK (isadmin IN (0, 1)))''')
        cursor.execute('''
        INSERT OR IGNORE INTO user (username, password, isadmin)
        VALUES (?, ?, ?)
        ''', ("admin", "letmein", 1))

        cursor.execute('''CREATE TABLE IF NOT EXISTS stock (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         url TEXT NOT NULL,
                         companyname TEXT NOT NULL,
                         description TEXT,
                         long_description TEXT,
                         picture_url TEXT,
                         wallpaper_url TEXT,
                         other_pictures TEXT,
                         annual_demand TEXT,
                         website TEXT,
                         number_of_stock INTEGER NOT NULL,
                         virtualeth REAL NOT NULL,
                         username TEXT NOT NULL,
                         marketcap REAL,
                         available_coins INTEGER,
                         total_supply INTEGER,
                         price REAL,
                         start_date TEXT,
                         eth_balance REAL,
                         price_history_24 TEXT,
                         price_history_5d TEXT,
                         price_history_1m TEXT,
                         price_history_3m TEXT,
                         price_history_1y TEXT,
                         price_history_5y TEXT,
                         price_history_all TEXT,
                         profit_24 INTEGER,
                         profit_5d INTEGER,
                         profit_1m INTEGER,
                         profit_3m INTEGER,
                         profit_1y INTEGER,
                         profit_5y INTEGER,
                         profit_all INTEGER,
                         FOREIGN KEY(username) REFERENCES user(username))''')
        conn.commit()
