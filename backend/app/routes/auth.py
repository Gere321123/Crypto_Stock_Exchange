from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    who = data.get("who", "company")

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT username FROM user WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"message": "Username already exists."}), 400

        try:
            # Insert new user
            cursor.execute("INSERT INTO user (username, password, who) VALUES (?, ?, ?)", 
                           (username, generate_password_hash(password), who))
            conn.commit()
        except Exception as e:
            return jsonify({"message": "An error occurred during registration.", "error": str(e)}), 500

    return jsonify({"message": "User registered successfully."}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, who FROM user WHERE username = ?", (username,))
        record = cursor.fetchone()
        if record and check_password_hash(record[0], password):
            session['user'] = username
            session['who'] = record[1]

            # Return the appropriate role
            role = record[1]
            return jsonify({"message": "Login successful", "role": role}), 200
        return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/users', methods=['GET'])
def get_users():
    with sqlite3.connect("cryptostock.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT username, who FROM user")
            users = cursor.fetchall()
            return jsonify({"users": users}), 200
        except Exception as e:
            return jsonify({"message": "An error occurred while retrieving users.", "error": str(e)}), 500

@auth_bp.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username):
    try:
        with sqlite3.connect("cryptostock.db") as conn:
            cursor = conn.cursor()

            # Check if the user exists
            cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
            user = cursor.fetchone()
            if not user:
                return jsonify({"message": "User not found"}), 404

            # Delete the user
            cursor.execute("DELETE FROM user WHERE username = ?", (username,))
            conn.commit()

            return jsonify({"message": f"User '{username}' deleted successfully."}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"message": "An error occurred while deleting the user.", "error": str(e)}), 500
