from flask import request, jsonify
from app.services.user_service import create_user, authenticate_user
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
)
from app.models.user_model import User
from app.errors.exceptions import UnauthorizedError
from app.extensions import db
from app.schemas.register_schema import RegisterSchema
from app.schemas.login_schema import LoginSchema
from app.errors.exceptions import NotFoundError


def register():

    schema = RegisterSchema()

    data = schema.load(request.json)

    user = create_user(data["username"], data["password"], data["email"])

    return jsonify({"msg": "Usuário criado", "id": user.id}), 201


def login():

    schema = LoginSchema()

    data = schema.load(request.json)

    user = authenticate_user(data["username"], data["password"])

    if not user:
        raise UnauthorizedError("Credenciais inválidas")

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({"access_token": access_token, "refresh_token": refresh_token})


@jwt_required()
def profile():
    user_id = int(get_jwt_identity())

    user = db.session.get(User, user_id)

    if not user:
        raise NotFoundError("Usuário não encontrado")

    return {
        "id": user.id,
        "username": user.username,
        "message": "Usuário autenticado com sucesso",
        "role": user.role,
    }


@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()

    new_access_token = create_access_token(identity=user_id)

    return jsonify({"access_token": new_access_token})
