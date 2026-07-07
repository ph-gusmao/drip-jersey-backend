from flask import request, jsonify
from app.services.product_service import (
    create_product,
    get_product_by_id,
    update_product,
    delete_product,
    get_filtered_products,
)
from flask_jwt_extended import jwt_required
from app.decorators.admin_required import admin_required
from app.errors.exceptions import NotFoundError, UnauthorizedError, BadRequestError
from app.schemas.product_schema import product_schema, products_schema
from app.utils.response import success_response
from marshmallow import ValidationError


@jwt_required()
@admin_required()
def create():

    data = product_schema.load(request.json)

    product = create_product(data["name"], data["price"], data["stock"])

    return (
        jsonify(
            success_response(
                data=products_schema.dump(product),
                message="Product created successfully",
            )
        ),
        201,
    )


def list_products():

    sort = request.args.get("sort", default="id", type=str)
    order = request.args.get("order", default="asc", type=str)

    page = request.args.get("page", default=1, type=int)

    per_page = request.args.get("per_page", default=10, type=int)

    # filtros
    name = request.args.get("name", type=str)
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    in_stock = request.args.get("in_stock", type=str)

    # converter in_stock (string --> bool)
    if in_stock is not None:
        in_stock = in_stock.lower() == "true"

    # segurança
    page = max(page, 1)
    per_page = min(max(per_page, 1), 50)

    pagination = get_filtered_products(
        page=page,
        name=name,
        per_page=per_page,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        sort=sort,
        order=order,
    )

    data = [...]

    data = product_schema.dump(pagination.items)

    meta = {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total_pages": pagination.pages,
        "total_items": pagination.total,
    }

    return (
        jsonify(
            success_response(
                data=data, meta=meta, message="filtered products retrieved successfuly"
            )
        ),
        200,
    )


def list_product_by_id(product_id):

    product = get_product_by_id(product_id)

    if not product:
        raise NotFoundError("Produto não encontrado")

    return jsonify((success_response(data=product_schema.dump(product)))), 200


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

    return jsonify(success_response(message="Product deleted successfully"))
