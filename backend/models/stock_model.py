from database.db import get_db_connection
import json

class StockModel:
    @staticmethod
    def get_all_stocks():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stock")
            return cursor.fetchall()

    @staticmethod
    def create_stock(data):
        other_pictures_json = json.dumps(data['other_pictures'])
        annual_demand_json = json.dumps(data['annual_demand'])
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO stock 
                              (url, companyname, description, long_description, picture_url, wallpaper_url, 
                              other_pictures, annual_demand, website, number_of_stock, virtualeth, username, price)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (data['url'], data['companyname'], data['description'], data['long_description'],
                            data['picture_url'], data['wallpaper_url'], other_pictures_json,
                            annual_demand_json, data['website'], data['number_of_stock'],
                            data['virtual_eth'], data['username'], data['virtual_eth']/data['number_of_stock']))
            conn.commit()

    @staticmethod
    def get_stock_by_id(stock_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM stock WHERE id = ?", (stock_id,))
            return cursor.fetchone()
