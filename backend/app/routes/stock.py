from flask import Blueprint, request, jsonify
import sqlite3
import json
import datetime
import requests

stock_bp = Blueprint('stock', __name__)

def get_bitcoin_value(btc_amount):
    # Fetch the current Bitcoin price in USD
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    data = response.json()
    btc_price = data['bitcoin']['usd']
    
    # Calculate the USD value of the given Bitcoin amount
    usd_value = btc_amount * btc_price
    return usd_value

@stock_bp.route('/stocks', methods=['GET', 'POST'])
def stocks():
    if request.method == 'GET':
        with sqlite3.connect("cryptostock.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stock")
            stocks = cursor.fetchall()
            return jsonify({"stocks": stocks}), 200

    if request.method == 'POST':
        data = request.json
        
        try:
            
            # Convert JSON fields
            other_pictures_json = json.dumps(data['other_pictures'])
            annual_demand_json = json.dumps(data['annual_demand'])
            
            # Calculated fields
            price = data['virtual_Bit'] / data['number_of_stock']
            total_supply = data['number_of_stock']
            available_coins = total_supply  # Available coins same as total supply initially
            marketcap = 0
            priceinUSD = get_bitcoin_value(price)  # Assuming price is already in USD
            start_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Today's date
            
            # Initialize price history and profit fields
            price_history_empty = "[]"
            profit_zero = 0
            
            # Initialize min and max price fields
            min_price = priceinUSD
            max_price = priceinUSD * 2
            
            with sqlite3.connect("cryptostock.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO stock 
                (url, companyname, description, long_description, picture_url, wallpaper_url, 
                other_pictures, annual_demand, website, number_of_stock, virtualBit, username, 
                marketcap, available_coins, total_supply, price, priceinUSD, start_date, bit_balance,
                price_history_24, price_history_5d, price_history_1m, price_history_3m, 
                price_history_1y, price_history_5y, price_history_all, profit_24, profit_5d, 
                profit_1m, profit_3m, profit_1y, profit_5y, profit_all, network, country, 
                min_price_24, max_price_24, min_price_5d, max_price_5d, min_price_1m, max_price_1m,
                min_price_3m, max_price_3m, min_price_1y, max_price_1y, min_price_5y, max_price_5y,
                min_price_all, max_price_all)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (data['url'], data['companyname'], data['description'], data['long_description'],
                data['picture_url'], data['wallpaper_url'], other_pictures_json, annual_demand_json,
                data['website'], data['number_of_stock'], data['virtual_Bit'], data['username'], 
                marketcap, available_coins, total_supply, price, priceinUSD, start_date, 0,
                price_history_empty, price_history_empty, price_history_empty, price_history_empty,
                price_history_empty, price_history_empty, price_history_empty, profit_zero, profit_zero,
                profit_zero, profit_zero, profit_zero, profit_zero, profit_zero, data['network'], 
                data['country'], min_price, max_price, min_price, max_price, min_price, max_price, 
                min_price, max_price, min_price, max_price, min_price, max_price, min_price, max_price))

                conn.commit()
        except Exception as e:
            # Debug: Print exception details
            print("Error:", str(e))
            return jsonify({"message": "An error occurred while creating the stock.", "error": str(e)}), 500

        return jsonify({"message": "Stock created successfully."}), 201


@stock_bp.route('/stocks/<int:id>', methods=['GET'])
def get_stock_details(id):
    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock WHERE id = ?", (id,))
        stock = cursor.fetchone()
        return jsonify({"stock": stock}), 200

@stock_bp.route('/stocks/<int:id>', methods=['PUT'])
def update_stock(id):
    data = request.json
    print(data[8])
    try:
        with sqlite3.connect("cryptostock.db") as conn:
            cursor = conn.cursor()

            # Check if stock exists
            cursor.execute("SELECT * FROM stock WHERE id = ?", (id,))
            stock = cursor.fetchone()
            if not stock:
                return jsonify({"message": "Stock not found"}), 404

            # Update the stock
            query = '''UPDATE stock SET 
                       url = ?, companyname = ?, description = ?, long_description = ?, 
                       picture_url = ?, wallpaper_url = ?, other_pictures = ?, annual_demand = ?, 
                       website = ?, number_of_stock = ?, virtualBit = ?, username = ?, network = ?
                       WHERE id = ?'''
            cursor.execute(query, (
                data[1], data[2], data[3], data[4], 
                data[5], data[6], data[7], 
                data[8], data[9], data[10], 
                data[11], data[12], data[34], id))
            conn.commit()

            return jsonify({"message": "Stock updated successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while updating the stock.", "error": str(e)}), 500
    
@stock_bp.route('/stocks/<int:id>', methods=['DELETE'])
def delete_stock(id):
    try:
        with sqlite3.connect("cryptostock.db") as conn:
            cursor = conn.cursor()

            # Check if the stock exists
            cursor.execute("SELECT * FROM stock WHERE id = ?", (id,))
            stock = cursor.fetchone()
            if not stock:
                return jsonify({"message": "Stock not found"}), 404

            # Delete the stock
            cursor.execute("DELETE FROM stock WHERE id = ?", (id,))
            conn.commit()

            return jsonify({"message": "Stock deleted successfully."}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "An error occurred while deleting the stock.", "error": str(e)}), 500

@stock_bp.route('/stock-by-username/<string:username>', methods=['GET'])
def get_stock_by_username(username):
    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM stock WHERE username = ?", (username,))
        stock = cursor.fetchone()
        if stock:
            return jsonify({"stockId": stock[0]}), 200
        print("itt")
        return jsonify({"message": "No stock found for this username"}), 404

