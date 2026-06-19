from flask import Blueprint

from app.controllers.user_controller import (
    list_users,
    get_user,
    update_role,
    delete_user_controller,
)

user_bp = Blueprint("users", __name__)

user_bp.route("/users", methods=["GET"])(list_users)
user_bp.route("/users/<int:user_id>", methods=["GET"])(get_user)
user_bp.route("/users/<int:user_id>/role", methods=["PUT"])(update_role)
user_bp.route("/users/<int:user_id>", methods=["DELETE"])(delete_user_controller)
