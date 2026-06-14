from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.models.user_model import User


def admin_required():

    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):

            user_id = int(get_jwt_identity())

            user = User.query.get(user_id)

            if not user:

                return {"msg": "Usuário não encontrado"}, 404

            if user.role != "ADMIN":
                return {"msg": "Acesso negado"}, 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper
