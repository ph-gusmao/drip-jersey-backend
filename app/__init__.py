from flask import Flask, request, g
from app.extensions import db, jwt
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from datetime import timedelta, datetime
import time, os


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(product_bp)

    db.init_app(app)
    jwt.init_app(app)

    @app.before_request
    def log_request():

        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        print(f"[{current_time}] {request.method} {request.path}")

    @app.after_request
    def log_response(response):

        print(f"[RESPONSE] Status: {response.status_code}")

        return response

    return app
