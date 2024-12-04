from flask import Flask
from web3 import Web3
import sqlite3
import schedule
import time
import threading

# Initialize Flask app
app = Flask(__name__)


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

# Function to update stock prices in the database
def update_stock_prices():
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Fetch all stocks from the database
        cursor.execute("SELECT id, url, network FROM stock")
        stocks = cursor.fetchall()

        for stock in stocks:
            stock_id, contract_address, network = stock

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
                token_value_in_bitcoin = Web3.fromWei(token_value_in_wei, "ether")

                # Calculate the token value in USD
                bitcoin_price_usd = get_bitcoin_price()
                token_value_in_usd = token_value_in_bitcoin * bitcoin_price_usd

                # Update price and priceinUSD in the database
                cursor.execute(
                    "UPDATE stock SET price = ?, priceinUSD = ? WHERE id = ?",
                    (token_value_in_bitcoin, token_value_in_usd, stock_id),
                )
                print(f"Updated stock ID {stock_id}: price = {token_value_in_bitcoin}, priceinUSD = {token_value_in_usd}")

            except Exception as e:
                print(f"Error reading contract for stock ID {stock_id}: {e}")

        # Commit changes and close the database connection
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Error updating stock prices: {e}")

# Schedule the task every minute
#schedule.every(1).minute.do(update_stock_prices)

def start_schedule():
    schedule.every(10).seconds.do(update_stock_prices)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_scheduler, daemon=True).start()
