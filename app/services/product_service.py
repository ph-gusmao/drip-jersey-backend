from app.models.product_model import Product
from app.extensions import db


def create_product(name, price, stock):
    product = Product(name=name, price=price, stock=stock)
    db.session.add(product)
    db.session.commit()
    return product


def get_all_products():
    return Product.query.all()


def get_product_by_id(product_id):
    return db.session.get(Product, product_id)


def update_product(product, data):
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.stock = data.get("stock", product.stock)

    db.session.commit()
    return product


def delete_product(product):
    db.session.delete(product)
    db.session.commit()


def get_paginated_products(page, per_page):

    pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "items": pagination.items,
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total,
        "per_page": pagination.per_page,
    }


def get_filtered_products(
    page, per_page, name=None, price=None, min_price=None, max_price=None, in_stock=None
):

    query = Product.query

    # Filtro por nome
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if in_stock is not None:
        if in_stock:
            query = query.filter(Product.stock > 0)
        else:
            query = query.filter(Product.stock == 0)

    # Paginação no final
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return pagination
