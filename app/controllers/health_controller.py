from flask import jsonify
from app.services.health_service import get_health_status


def health_check():
    status = get_health_status()
    return jsonify(status)
