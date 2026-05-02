from flask import jsonify
from app.services.ping_service import get_ping_status


def ping_check():
    status = get_ping_status()
    return jsonify(status)
