from flask import Flask
from app.extensions import db, jwt
from app.routes.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super_secret_key"
    app.register_blueprint(auth_bp, url_prefix="/auth")

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.health_routes import health_bp
    from app.routes.ping_routes import ping_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(ping_bp)

    return app
