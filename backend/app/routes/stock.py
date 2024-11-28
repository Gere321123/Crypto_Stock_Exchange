from flask import Blueprint, request, jsonify
import sqlite3
import json

stock_bp = Blueprint('stock', __name__)

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
      
      # Debug: Print incoming data
      print("Incoming data:", data)
      
      try:
          # Ensure required keys exist
          required_keys = ['url', 'companyname', 'description', 'long_description', 'picture_url',
                          'wallpaper_url', 'other_pictures', 'annual_demand', 'website', 
                          'number_of_stock', 'virtual_Bit', 'username', 'network']
          for key in required_keys:
              if key not in data:
                  return jsonify({"message": f"Missing key: {key}"}), 400
          
          # Convert JSON fields
          other_pictures_json = json.dumps(data['other_pictures'])
          annual_demand_json = json.dumps(data['annual_demand'])
          
          # Debug: Check for zero stock
          if data['number_of_stock'] == 0:
              return jsonify({"message": "Number of stock cannot be zero."}), 400
          
          price = data['virtual_Bit'] / data['number_of_stock']
          
          with sqlite3.connect("cryptostock.db") as conn:
              cursor = conn.cursor()
              cursor.execute('''INSERT INTO stock 
                  (url, companyname, description, long_description, picture_url, wallpaper_url, 
                  other_pictures, annual_demand, website, number_of_stock, virtualBit, username, price, network)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (data['url'], data['companyname'], data['description'], data['long_description'],
                  data['picture_url'], data['wallpaper_url'], other_pictures_json,
                  annual_demand_json, data['website'], data['number_of_stock'],
                  data['virtual_Bit'], data['username'], price, data['network']))
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
