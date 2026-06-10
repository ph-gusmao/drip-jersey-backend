from flask import Blueprint
from app.controllers.auth_controller import register, login, profile, refresh

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(register)
auth_bp.route("/login", methods=["POST"])(login)
auth_bp.route("/profile", methods=["GET"])(profile)
auth_bp.route("/refresh", methods=["POST"])(refresh)
