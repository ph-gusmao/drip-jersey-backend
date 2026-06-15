from flask import jsonify

from app.errors.exceptions import (
    NotFoundError,
    BadRequestError,
    ForbiddenError,
    UnauthorizedError,
)


def register_error_handlers(app):

    @app.errorhandler(NotFoundError)
    def handle_not_found(error):

        return jsonify({"error": str(error)}), 404

    @app.errorhandler(BadRequestError)
    def handle_bad_request(error):

        return jsonify({"error": str(error)}), 400

    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(error):

        return jsonify({"error": str(error)}), 401

    @app.errorhandler(ForbiddenError)
    def handle_forbidden(error):

        return jsonify({"error": str(error)}), 403

    @app.errorhandler(Exception)
    def handle_internal_error(error):

        print(f"[ERROR] {error}")

        return jsonify({"error": "Erro interno do servidor"}), 500
