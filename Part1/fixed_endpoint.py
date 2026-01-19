from decimal import Decimal
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from app import db
from models import Product, Inventory

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    required_fields = ['name', 'sku', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        with db.session.begin():
            product = Product(
                name=data['name'],
                sku=data['sku'],
                price=Decimal(str(data['price']))
            )
            db.session.add(product)
            db.session.flush()

            if 'warehouse_id' in data and 'initial_quantity' in data:
                inventory = Inventory(
                    product_id=product.id,
                    warehouse_id=data['warehouse_id'],
                    quantity=data['initial_quantity']
                )
                db.session.add(inventory)

        return jsonify({
            "message": "Product created successfully",
            "product_id": product.id
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "SKU must be unique"}), 409
