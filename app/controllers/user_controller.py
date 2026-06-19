from flask import jsonify, request

from flask_jwt_extended import jwt_required

from app.decorators.admin_required import admin_required

from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    update_user_role,
    delete_user,
)

from app.schemas.admin_user_schema import AdminUserSchema


@jwt_required()
@admin_required()
def list_users():

    users = get_all_users()

    return jsonify(
        [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
            for user in users
        ]
    )


@jwt_required()
@admin_required()
def get_user(user_id):

    user = get_user_by_id(user_id)

    return jsonify(
        [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        ]
    )


@jwt_required()
@admin_required()
def update_role(user_id):

    schema = AdminUserSchema()

    data = schema.load(request.json)

    user = update_user_role(user_id, data["role"])

    return jsonify([{"id": user.id, "username": user.username, "role": user.role}])


@jwt_required()
@admin_required()
def delete_user_controller(user_id):

    delete_user(user_id)

    return jsonify({"msg": "Usuário removido"})
