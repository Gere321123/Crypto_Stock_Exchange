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

def get_bitcoin_value(btc_amount):
    # Fetch the current Bitcoin price in USD
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    data = response.json()
    btc_price = data['bitcoin']['usd']
    
    # Calculate the USD value of the given Bitcoin amount
    usd_value = btc_amount * btc_price
    return usd_value

# Function to update stock prices in the database
def update_stock_prices():
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Fetch all stocks from the database
        cursor.execute("SELECT id, url, network, price_history_24, index_price_24 FROM stock")
        stocks = cursor.fetchall()

        for stock in stocks:
            stock_id, contract_address, network, price_history_24, index_price_24 = stock
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
                token_value_in_usd = get_bitcoin_value(token_value_in_bitcoin)

                price_history_24_array[index_price_24] = token_value_in_usd

                index_price_24 += 1

                price_history_24 = json.dumps(price_history_24_array)
                # Update price and priceinUSD in the database
                cursor.execute(
                    "UPDATE stock SET price = ?, priceinUSD = ?, price_history_24 = ?, index_price_24 = ? WHERE id = ?",
                    (token_value_in_bitcoin, token_value_in_usd, price_history_24, index_price_24, stock_id),
                )
                #print(f"Updated stock ID {stock_id}: price = {token_value_in_bitcoin}, priceinUSD = {token_value_in_usd}")

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
