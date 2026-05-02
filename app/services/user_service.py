from app.models.user_model import User
from app.extensions import db
import bcrypt


def create_user(username, password):
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        raise Exception("Usuário já existe")

    # garante que é bcrypt antes de  converter
    password_bytes = str(password).encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    user = User(username=username, password=hashed.decode("utf-8"))

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
