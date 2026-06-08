from flask import Flask
from app.extensions import db, jwt
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super_secret_key"
    app.register_blueprint(auth_bp, url_prefix="/auth")

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(product_bp)

    return app
