from app.models.user_model import User
from app.extensions import db
import bcrypt
from app.errors.exceptions import NotFoundError


def create_user(username, password, role="USER"):
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        raise Exception("Usuário já existe")

    # garante que é bcrypt antes de  converter
    password_bytes = str(password).encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    user = User(username=username, password=hashed.decode("utf-8"), role=role)

    db.session.add(user)
    db.session.commit()

    return user


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()

    if not user:
        return None

    password_bytes = str(password).encode("utf-8")
    stored_password_bytes = user.password.encode("utf-8")

    if bcrypt.checkpw(password_bytes, stored_password_bytes):
        return user

    return None


def get_all_users():
    return User.query, all()


def get_user_by_id(user_id):

    user = db.session.get(User, user_id)

    if not user:
        raise NotFoundError("Usuário não encontrado")

    return user


def update_user_role(user_id, role):

    user = get_user_by_id(user_id)

    user.role = role

    db.session.commit()

    return user


def delete_user(user_id):

    user = get_user_by_id(user_id)

    db.session.delete(user)

    db.session.commit()
