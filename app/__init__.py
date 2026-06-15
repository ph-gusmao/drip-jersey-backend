from flask import Flask, request, g
from app.extensions import db, jwt, migrate
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from datetime import datetime
from dotenv import load_dotenv
import time
from app.errors.handlers import register_error_handlers
from app.config import DevelopmentConfig

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(product_bp)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    register_error_handlers(app)

    @app.before_request
    def log_request():

        g.start_time = time.time()

        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        print(f"[{current_time}] {request.method} {request.path}")

    @app.after_request
    def log_response(response):

        execution_time = time.time() - g.start_time

        print(f"[RESPONSE] Status: " f"{response.status_code}")

        print(f"[TIME] {execution_time:.4f} segundos")

        return response

    return app
