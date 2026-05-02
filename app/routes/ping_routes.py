from flask import Blueprint
from app.controllers.ping_controller import ping_check

ping_bp = Blueprint("ping", __name__)

ping_bp.route("/ping", methods=["GET"])(ping_check)
