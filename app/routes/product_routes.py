from flask import Blueprint
from app.controllers.product_controller import (
    create,
    list_products,
    delete,
    update,
    list_product_by_id,
)

product_bp = Blueprint("products", __name__)

product_bp.route("/products", methods=["POST"])(create)
product_bp.route("/products", methods=["GET"])(list_products)
product_bp.route("/products/<int:product_id>", methods=["GET"])(list_product_by_id)
product_bp.route("/products/<int:product_id>", methods=["PUT"])(update)
product_bp.route("/products/<int:product_id>", methods=["DELETE"])(delete)
