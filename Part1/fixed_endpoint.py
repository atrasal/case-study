from flask import request, jsonify
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from app import app, db
from models import Product, Inventory


@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}

    
    # 1. Basic Validation
    
    required_fields = ["name", "sku", "price"]
    missing = [f for f in required_fields if f not in data]

    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Validate price
    try:
        price = Decimal(str(data["price"]))
        if price < 0:
            return jsonify({"error": "Price must be positive"}), 400
    except:
        return jsonify({"error": "Invalid price format"}), 400

    initial_qty = data.get("initial_quantity", 0)
    warehouse_id = data.get("warehouse_id")

    # Negative quantity edge-case
    if initial_qty < 0:
        return jsonify({"error": "Initial quantity cannot be negative"}), 400

    try:
        
        # 2. Transaction Block
        
        with db.session.begin():

            product = Product(
                name=data["name"],
                sku=data["sku"],
                price=price
            )
            db.session.add(product)
            db.session.flush()

            # Optional inventory creation
            if warehouse_id:
                inventory = Inventory(
                    product_id=product.id,
                    warehouse_id=warehouse_id,
                    quantity=initial_qty
                )
                db.session.add(inventory)

        
        # Success Response
        
        return jsonify({
            "message": "Product created",
            "product_id": product.id
        }), 201

    
    # 3. Error Handling
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "SKU already exists"}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500
