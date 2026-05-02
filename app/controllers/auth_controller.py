from flask import request, jsonify
from app.services.user_service import create_user, authenticate_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user_model import User


def register():
    data = request.json

    try:
        user = create_user(data["username"], data["password"])
        return jsonify({"msg:": "Usuário criado", "id": user.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def login():
    data = request.json

    user = authenticate_user(data["username"], data["password"])

    if not user:
        return jsonify({"msg": "Credenciais inválidas"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": token})


@jwt_required()
def profile():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return {"msg": "Usuário não encontrado"}, 404

    return {
        "id": user.id,
        "username": user.username,
        "message": "Usuário autenticado com sucesso",
    }
