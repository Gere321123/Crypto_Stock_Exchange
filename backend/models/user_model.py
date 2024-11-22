from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db_connection

class UserModel:
    @staticmethod
    def register_user(username, password, is_admin):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (username, password, isadmin) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), is_admin)
            )
            conn.commit()

    @staticmethod
    def get_user_by_username(username):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password, isadmin FROM user WHERE username = ?", (username,))
            return cursor.fetchone()
