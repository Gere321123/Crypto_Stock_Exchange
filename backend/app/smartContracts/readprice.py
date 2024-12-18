from flask import Flask
from web3 import Web3
import sqlite3
import schedule
import time
import threading
import json
# Initialize Flask app
app = Flask(__name__)

import requests

CONTRACT_ABI = [
    {
        "type": "function",
        "name": "getValueOfOneTokenInWei",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256"}],
    },
    {
    "inputs": [],
    "name": "getMarketCap",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "geNumberOfTokensInTheMarcetCapp",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
]
# Database connection
DATABASE = "cryptostock.db"

howManyTimesWeCallTheupdate_stock_prices = 0

def get_bitcoin_value():
    """
    Fetch the current Bitcoin price in USD and calculate the value for the given amount of Bitcoin.
    Includes error handling and retry logic with exponential backoff.
    """
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'

    response = requests.get(url, timeout=10)  # Added timeout to avoid hanging requests
    response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
    data = response.json()
    btc_price = data['bitcoin']['usd']
            
    return btc_price

# Function to update stock prices in the database
def update_stock_prices():
    global howManyTimesWeCallTheupdate_stock_prices
    howManyTimesWeCallTheupdate_stock_prices += 1
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()

        # Fetch all stocks from the database
        cursor.execute("SELECT id, url, network, price_history_24, index_price_24, max_price_24, min_price_24, total_supply FROM stock")
        stocks = cursor.fetchall()

        bitValue = get_bitcoin_value()

        for stock in stocks:
            stock_id, contract_address, network, price_history_24, index_price_24, max_price_24, min_price_24, total_supply  = stock
            price_history_24_array = json.loads(price_history_24)
            # Skip if necessary fields are missing
            if not contract_address or not network:
                print(f"Skipping stock ID {stock_id}: Missing contract address or network.")
                continue

            # Set up Web3 connection for the stock's network
            web3 = Web3(Web3.HTTPProvider(network))

            # Create contract instance
            contract = web3.eth.contract(address=contract_address, abi=CONTRACT_ABI)

            try:
                # Call the contract function
                token_value_in_wei = contract.functions.getValueOfOneTokenInWei().call()
                # Convert Wei to Bitcoin (1 Bitcoin = 10**18 Wei)
                token_value_in_bitcoin = token_value_in_wei / (10 **18)
                # Calculate the token value in USD
                
                token_value_in_usd = token_value_in_bitcoin * bitValue

                tokensInTheMarcetCapp = contract.functions.geNumberOfTokensInTheMarcetCapp().call()
                available_coins = total_supply - (tokensInTheMarcetCapp / (10**18))
                marketcap = (tokensInTheMarcetCapp * token_value_in_usd) / (10**18)

                price_history_24_array[index_price_24] = token_value_in_usd

                index_price_24 += 1

                if index_price_24 >= 1440:
                    for i in range(len(price_history_24_array)):
                        if i == 0:
                            price_history_24_array[0] = price_history_24_array[1439]
                        else:
                            price_history_24_array[i] = -1
                    index_price_24 = 1

                price_history_24 = json.dumps(price_history_24_array)

                while (token_value_in_usd < min_price_24 * 1.001):
                    min_price_24 *= 0.999

                while (token_value_in_usd > max_price_24 * 0.999):
                    max_price_24 *= 1.001
                # Update price and priceinUSD in the database
                cursor.execute(
                    "UPDATE stock SET price = ?, priceinUSD = ?, price_history_24 = ?, index_price_24 = ?, max_price_24 = ?, min_price_24 = ?, marketcap = ?, available_coins = ?  WHERE id = ?",
                    (token_value_in_bitcoin, token_value_in_usd, price_history_24, index_price_24, max_price_24, min_price_24, marketcap, available_coins, stock_id),
                )

            except Exception as e:
                print(f"Error reading contract for stock ID {stock_id}: {e}")

        # Commit changes and close the database connection
        conn.commit()
        conn.close()

        if howManyTimesWeCallTheupdate_stock_prices % 5 == 0:
            updateStockhistory("price_history_5d", "max_price_5d", "min_price_5d", "index_price_5d")
        if howManyTimesWeCallTheupdate_stock_prices % 30 == 0:
            updateStockhistory("price_history_1m", "max_price_1m", "min_price_1m", "index_price_1m")
        if howManyTimesWeCallTheupdate_stock_prices % 90 == 0:
            updateStockhistory("price_history_3m", "max_price_3m", "min_price_3m", "index_price_3m")
        if howManyTimesWeCallTheupdate_stock_prices % 365 == 0:
            updateStockhistory("price_history_1y", "max_price_1y", "min_price_1y", "index_price_1y")
        if howManyTimesWeCallTheupdate_stock_prices % 1825 == 0:
            updateStockhistory("price_history_5y", "max_price_5y", "min_price_5y", "index_price_5y")

    except Exception as e:
        print(f"Error updating stock prices: {e}")

def updateStockhistory(history, max_price, min_price, index):
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        cursor = conn.cursor()

        # Get data for all stocks
        cursor.execute(f"""
            SELECT id, {history}, {max_price}, {min_price}, {index}, max_price_24, min_price_24, priceinUSD
            FROM stock
        """)
        all_stocks = cursor.fetchall()

        for stock in all_stocks:
            stock_id = stock[0]
            price_history = json.loads(stock[1])  # Assuming it's stored as a JSON string
            max_price_history = stock[2]
            min_price_history = stock[3]
            index_price = stock[4]
            max_price_24 = stock[5]
            min_price_24 = stock[5]
            price = stock[7]  # Current price in USD

            # Update the price history array based on the index and new price
            if index_price < 1440:
                price_history[index_price] = price
                index_price += 1
            else:
                for i in range(1, len(price_history)):
                    price_history[i - 1] = price_history[i]
                price_history[-1] = price

            # Update the max and min prices
            if max_price_24 > max_price_history:
                max_price_history = max_price_24
            if min_price_24 < min_price_history:
                min_price_history = min_price_24

            # Update the database for this stock
            cursor.execute(f"""
                UPDATE stock
                SET {history} = ?, {max_price} = ?, {min_price} = ?, {index} = ?
                WHERE id = ?
            """, (json.dumps(price_history), max_price_history, min_price_history, index_price, stock_id))

        # Commit all updates
        conn.commit()

    except Exception as e:
        print(f"Error updating stock history: {e}")
    finally:
        conn.close()

def start_schedule():
    schedule.every(1).minutes.do(update_stock_prices)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_scheduler, daemon=True).start()
