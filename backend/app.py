from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for production use
CORS(app)

# Initialize Database (as shown in your example)
def init_db():
    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT UNIQUE NOT NULL,
                         password TEXT NOT NULL,
                         isadmin BOOLEAN NOT NULL CHECK (isadmin IN (0, 1)))''')
        cursor.execute('''
        INSERT OR IGNORE INTO user (username, password, isadmin)
        VALUES (?, ?, ?)
        ''', ("admin", "letmein", 1))  # 1 for admin

        cursor.execute('''CREATE TABLE IF NOT EXISTS stock (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         url TEXT NOT NULL,
                         companyname TEXT NOT NULL,
                         description TEXT,
                         long_description TEXT,
                         picture_url TEXT,
                         wallpaper_url TEXT,
                         other_pictures TEXT,               -- JSON encoded array of URLs
                         annual_demand TEXT,                -- JSON encoded array of demand values
                         website TEXT,
                         number_of_stock INTEGER NOT NULL,
                         virtualeth REAL NOT NULL,
                         username TEXT NOT NULL,
                         
                         -- New fields as requested
                         marketcap REAL,
                         available_coins INTEGER,
                         total_supply INTEGER,
                         price REAL,
                         start_date TEXT,                   -- Store as a date string in ISO format
                         eth_balance REAL,

                         -- Price history arrays (JSON encoded arrays of integers, max 1440 items)
                         price_history_24 TEXT,             -- JSON array for 24-hour price history
                         price_history_5d TEXT,             -- JSON array for 5-day price history
                         price_history_1m TEXT,             -- JSON array for 1-month price history
                         price_history_3m TEXT,             -- JSON array for 3-month price history
                         price_history_1y TEXT,             -- JSON array for 1-year price history
                         price_history_5y TEXT,             -- JSON array for 5-year price history
                         price_history_all TEXT,            -- JSON array for all-time price history
                         
                         -- Profit fields (can be negative values)
                         profit_24 INTEGER,
                         profit_5d INTEGER,
                         profit_1m INTEGER,
                         profit_3m INTEGER,
                         profit_1y INTEGER,
                         profit_5y INTEGER,
                         profit_all INTEGER,
                         
                         FOREIGN KEY(username) REFERENCES user(username))''')
        
        conn.commit()


init_db()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    is_admin = data.get("is_admin", False)

    # Check if username or password is missing
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()
        try:
            # Insert the new user into the database
            cursor.execute("INSERT INTO user (username, password, isadmin) VALUES (?, ?, ?)", 
                           (username, generate_password_hash(password), is_admin))
            conn.commit()
        except sqlite3.IntegrityError:
            # Return error if the username already exists
            return jsonify({"message": "Username already exists."}), 400
        except Exception as e:
            # Catch any other errors and return a 500 status
            return jsonify({"message": "An error occurred during registration.", "error": str(e)}), 500

    return jsonify({"message": "User registered successfully."}), 201



# Login route to set session
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, isadmin FROM user WHERE username = ?", (username,))
        record = cursor.fetchone()
        if record and check_password_hash(record[0], password):
            session['user'] = username
            session['isadmin'] = bool(record[1])
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"message": "Invalid credentials"}), 401

# Logout route to clear session
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

# Helper function to check if a user is logged in
def is_logged_in():
    return 'user' in session

@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    if request.method == 'GET':
        # Fetch all stocks from the database
        with sqlite3.connect("cryptostock.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stock")
            stocks = cursor.fetchall()
            return jsonify({"stocks": stocks}), 200

    if request.method == 'POST':
        data = request.json
        # Serialize the lists into JSON strings
        other_pictures_json = json.dumps(data['other_pictures'])
        annual_demand_json = json.dumps(data['annual_demand'])
        print (data['url'], data['companyname'], data['description'], data['long_description'],
                                data['picture_url'], data['wallpaper_url'], other_pictures_json,
                                annual_demand_json, data['website'], data['number_of_stock'],
                                data['virtual_eth'], data['username'])
        try:
            with sqlite3.connect("cryptostock.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO stock 
                                  (url, companyname, description, long_description, picture_url, wallpaper_url, 
                                  other_pictures, annual_demand, website, number_of_stock, virtualeth, username, price)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                               (data['url'], data['companyname'], data['description'], data['long_description'],
                                data['picture_url'], data['wallpaper_url'], other_pictures_json,
                                annual_demand_json, data['website'], data['number_of_stock'],
                                data['virtual_eth'], data['username'],  data['virtual_eth']/data['number_of_stock']))
                conn.commit()
        except Exception as e:
            print(e)
            return jsonify({"message": "An error occurred while creating the stock.", "error": str(e)}), 500

        return jsonify({"message": "Stock created successfully."}), 201

@app.route('/stocks/<int:id>', methods=['GET'])
def get_stock_details(id):
    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE id = ?", (id,))
        stock = cursor.fetchone()

        # Return the stock directly
        return jsonify({"company": stock}), 200



if __name__ == '__main__':
    app.run(debug=True)
