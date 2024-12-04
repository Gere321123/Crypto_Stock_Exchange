from flask import Flask
from flask_cors import CORS

from app.models.database import init_db
from app.smartContracts.readprice import start_schedule

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Change this for production use
    CORS(app)

    # Initialize database
    init_db()
    start_schedule()
    # Register routes
    from app.routes.auth import auth_bp
    from app.routes.stock import stock_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_bp)

    return app
