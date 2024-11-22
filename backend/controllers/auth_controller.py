from flask import Blueprint, request, jsonify, session
from models.user_model import UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    is_admin = data.get("is_admin", False)

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    try:
        UserModel.register_user(username, password, is_admin)
    except Exception as e:
        return jsonify({"message": "Username already exists.", "error": str(e)}), 400

    return jsonify({"message": "User registered successfully."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = UserModel.get_user_by_username(username)

    if user and UserModel.check_password(password, user[0]):
        session['user'] = username
        session['isadmin'] = bool(user[1])
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid credentials"}), 401
