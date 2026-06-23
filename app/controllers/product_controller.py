from flask import request, jsonify
from app.services.product_service import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
    get_paginated_products,
)
from flask_jwt_extended import jwt_required
from app.decorators.admin_required import admin_required
from app.errors.exceptions import NotFoundError, UnauthorizedError, BadRequestError
from app.schemas.product_schema import ProductSchema


@jwt_required()
@admin_required()
def create():

    schema = ProductSchema()

    data = schema.load(request.json)

    product = create_product(data["name"], data["price"], data["stock"])

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

    page = request.args.get("page", default=1, type=int)

    per_page = request.args.get("per_page", default=10, type=int)
    per_page = min(per_page, 50)

    pagination = get_paginated_products(page, per_page)

    return jsonify(
        {
            "items": [
                {"id": p.id, "name": p.name, "price": p.price, "stock": p.stock}
                for p in pagination.items
            ],
            "page": pagination.page,
            "pages": pagination.pages,
            "per_page": pagination.per_page,
            "total": pagination.total,
        }
    )

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
        raise NotFoundError("Produto não encontrado")

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
@admin_required()
def update(product_id):
    product = get_product_by_id(product_id)

    if not product:
        raise NotFoundError("Produto não encontrado")

    updated = update_product(product, request.json)

    return jsonify({"id": updated.id, "name": updated.name}), 200


@jwt_required()
@admin_required()
def delete(product_id):
    product = get_product_by_id(product_id)

    if not product:
        raise NotFoundError("Produto não encontrado")

    delete_product(product)

    return {"msg": "Produto deletado"}
