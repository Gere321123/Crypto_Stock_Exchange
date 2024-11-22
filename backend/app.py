from flask import Flask
from flask_cors import CORS
from config import Config
from controllers.auth_controller import auth_bp
from controllers.stock_controller import stock_bp
from database.db import init_db

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
init_db()

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(stock_bp)

if __name__ == '__main__':
    app.run(debug=True)
