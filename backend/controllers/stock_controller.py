from flask import Blueprint, request, jsonify
from models.stock_model import StockModel

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/stocks', methods=['GET', 'POST'])
def stocks():
    if request.method == 'GET':
        stocks = StockModel.get_all_stocks()
        return jsonify({"stocks": stocks}), 200

    if request.method == 'POST':
        data = request.json
        try:
            StockModel.create_stock(data)
        except Exception as e:
            return jsonify({"message": "An error occurred while creating the stock.", "error": str(e)}), 500

        return jsonify({"message": "Stock created successfully."}), 201

@stock_bp.route('/stocks/<int:id>', methods=['GET'])
def get_stock_details(id):
    stock = StockModel.get_stock_by_id(id)
    return jsonify({"company": stock}), 200
