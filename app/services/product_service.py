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

    return Product.query.paginated(page=page, per_page=per_page, error_out=False)
