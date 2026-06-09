from flask import request, jsonify
from app.services.product_service import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
)
from flask_jwt_extended import jwt_required


@jwt_required()
def create():
    data = request.json

    product = create_product(data["name"], data["price"], data["stock"])

    if not data:
        return jsonify({"error": "Dados obrigatórios"}), 400

    return (
        jsonify(
            {
                "id": product.id,
                "name": product.name,
            }
        ),
        201,
    )


def list_products():

    products = get_all_products()

    return jsonify(
        [
            {"id": p.id, "name": p.name, "price": p.price, "stock": p.stock}
            for p in products
        ]
    )


def list_product_by_id(product_id):

    product = get_product_by_id(product_id)

    if not product:
        return jsonify({"error": "Este produto não existe"}), 404

    return (
        jsonify(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
            }
        ),
        200,
    )


def create_protected():
    return create()


@jwt_required()
def update(product_id):
    product = get_product_by_id(product_id)

    if not product:
        return {"msg": "Produto não encontrado"}, 404

    updated = update_product(product, request.json)

    return jsonify({"id": updated.id, "name": updated.name}), 200


@jwt_required()
def delete(product_id):
    product = get_product_by_id(product_id)

    if not product:
        return {"mesg": "Produto não encontrado"}, 404

    delete_product(product)

    return {"msg": "Produto deletado"}
