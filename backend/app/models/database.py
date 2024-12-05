import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()

        # Create the user table
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            who TEXT NOT NULL)''')

        # Insert admin user
        cursor.execute('''INSERT OR IGNORE INTO user (username, password, who)
            VALUES (?, ?, ?)''', ("admin", generate_password_hash("letmein"), "admin"))

        # Create the stock table
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
            virtualBit REAL NOT NULL,
            username TEXT NOT NULL,
            marketcap REAL,
            available_coins INTEGER,
            total_supply INTEGER,
            price REAL,
            priceinUSD REAL,
            start_date TEXT,
            bit_balance REAL,
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
            network TEXT,          
            country TEXT,  
            min_price_24 REAL,  -- Minimum price in the last 24 hours
            max_price_24 REAL,  -- Maximum price in the last 24 hours
            min_price_5d REAL,   -- Minimum price in the last 5 days
            max_price_5d REAL,   -- Maximum price in the last 5 days
            min_price_1m REAL,   -- Minimum price in the last 1 month
            max_price_1m REAL,   -- Maximum price in the last 1 month
            min_price_3m REAL,   -- Minimum price in the last 3 months
            max_price_3m REAL,   -- Maximum price in the last 3 months
            min_price_1y REAL,   -- Minimum price in the last 1 year
            max_price_1y REAL,   -- Maximum price in the last 1 year
            min_price_5y REAL,   -- Minimum price in the last 5 years
            max_price_5y REAL,   -- Maximum price in the last 5 years
            min_price_all REAL,  -- Minimum price for all-time
            max_price_all REAL,  -- Maximum price for all-time
            FOREIGN KEY(username) REFERENCES user(username)
        )''')

        conn.commit()
