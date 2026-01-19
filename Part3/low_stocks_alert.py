from flask import jsonify
from app import db
from models import Inventory, Warehouse, Product, Supplier
from datetime import datetime, timedelta

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    alerts = []

    inventories = (
        db.session.query(Inventory)
        .join(Warehouse)
        .join(Product)
        .filter(Warehouse.company_id == company_id)
        .all()
    )

    for inventory in inventories:
        product = inventory.product
        warehouse = inventory.warehouse

        threshold = product.low_stock_threshold
        if threshold is None or inventory.quantity >= threshold:
            continue

        # Fetch recent sales (assumed helper method)
        avg_daily_sales = product.get_avg_daily_sales(days=30)

        if avg_daily_sales <= 0:
            continue  # Ignore products without recent sales

        days_until_stockout = int(inventory.quantity / avg_daily_sales)

        supplier = product.get_primary_supplier()

        alerts.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "current_stock": inventory.quantity,
            "threshold": threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": {
                "id": supplier.id,
                "name": supplier.name,
                "contact_email": supplier.contact_email
            } if supplier else None
        })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    }), 200
