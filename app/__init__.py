from flask import Flask
from app.extensions import db, jwt
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from datetime import timedelta


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super_secret_key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(product_bp)

    db.init_app(app)
    jwt.init_app(app)

    return app
