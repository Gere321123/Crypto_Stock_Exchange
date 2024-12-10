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
]
# Database connection
DATABASE = "cryptostock.db"

howManyTimesWeCallTheupdate_stock_prices = 0

def get_bitcoin_value(btc_amount, previous_value, max_retries=5, backoff_factor=2):
    """
    Fetch the current Bitcoin price in USD and calculate the value for the given amount of Bitcoin.
    Includes error handling and retry logic with exponential backoff.
    """
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, timeout=10)  # Added timeout to avoid hanging requests
            response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
            data = response.json()
            btc_price = data['bitcoin']['usd']
            usd_value = btc_amount * btc_price
            return usd_value
        except requests.RequestException as e:
            print(f"Error fetching Bitcoin price: {e}. Retrying in {backoff_factor ** retries} seconds...")
            retries += 1
            time.sleep(backoff_factor ** retries)

    # If all retries fail, return a fallback value or raise an exception
    print("Failed to fetch Bitcoin price after multiple retries.")
    return previous_value

# Function to update stock prices in the database
def update_stock_prices():
    howManyTimesWeCallTheupdate_stock_prices += 1
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Fetch all stocks from the database
        cursor.execute("SELECT id, url, network, price_history_24, index_price_24, max_price_24, min_price_24 FROM stock")
        stocks = cursor.fetchall()

        for stock in stocks:
            stock_id, contract_address, network, price_history_24, index_price_24, max_price_24, min_price_24  = stock
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
                token_value_in_usd = get_bitcoin_value(token_value_in_bitcoin,price_history_24_array[index_price_24 - 1])

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
                    "UPDATE stock SET price = ?, priceinUSD = ?, price_history_24 = ?, index_price_24 = ?, max_price_24 = ?, min_price_24 = ?  WHERE id = ?",
                    (token_value_in_bitcoin, token_value_in_usd, price_history_24, index_price_24, max_price_24, min_price_24, stock_id),
                )
                # if (howManyTimesWeCallTheupdate_stock_prices % 5 == 0):

                # if (howManyTimesWeCallTheupdate_stock_prices % 30):
                # if (howManyTimesWeCallTheupdate_stock_prices % 90):
                # if (howManyTimesWeCallTheupdate_stock_prices % 365):
                # if (howManyTimesWeCallTheupdate_stock_prices % 1825):

            except Exception as e:
                print(f"Error reading contract for stock ID {stock_id}: {e}")

        # Commit changes and close the database connection
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error updating stock prices: {e}")


def start_schedule():
    schedule.every(1).minutes.do(update_stock_prices)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_scheduler, daemon=True).start()
