from flask import jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from app import app, db
from models import (
    Product,
    Warehouse,
    Inventory,
    InventoryLog,
    Supplier,
    SupplierProduct
)


@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    """
    Low Stock Alerts API
    Business Rules Implemented:
    - Threshold varies per product
    - Only include products with recent sales activity
    - Works across multiple warehouses
    - Include supplier info for reordering
    - Forecast days until stockout using trailing sales window
    """

    try:
        # Configuration
        SALES_WINDOW_DAYS = 30
        cutoff_date = datetime.utcnow() - timedelta(days=SALES_WINDOW_DAYS)

        
        # 1. Find products with recent sales
        
        recent_sales_query = (
            db.session.query(InventoryLog.product_id)
            .join(Product, Product.id == InventoryLog.product_id)
            .filter(Product.company_id == company_id)
            .filter(InventoryLog.change_type == "sale")
            .filter(InventoryLog.created_at >= cutoff_date)
            .distinct()
        )

        recent_product_ids = [row.product_id for row in recent_sales_query]

        if not recent_product_ids:
            return jsonify({"alerts": [], "total_alerts": 0}), 200

        
        # 2. Fetch inventory + suppliers per warehouse
        
        inventory_records = (
            db.session.query(
                Inventory,
                Product,
                Warehouse,
                Supplier,
                SupplierProduct.lead_time_days
            )
            .join(Product, Product.id == Inventory.product_id)
            .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
            .outerjoin(SupplierProduct, SupplierProduct.product_id == Product.id)
            .outerjoin(Supplier, Supplier.id == SupplierProduct.supplier_id)
            .filter(Product.company_id == company_id)
            .filter(Product.id.in_(recent_product_ids))
            .all()
        )

       
        # 3. Compute average daily sales (consumption rate)
        
        sales_rates = (
            db.session.query(
                InventoryLog.product_id,
                func.sum(InventoryLog.quantity_change).label("total_sold")
            )
            .filter(InventoryLog.product_id.in_(recent_product_ids))
            .filter(InventoryLog.change_type == "sale")
            .filter(InventoryLog.created_at >= cutoff_date)
            .group_by(InventoryLog.product_id)
            .all()
        )

        # Convert negative sale logs into positive daily numbers
        daily_sales_map = {}
        for product_id, total_sold in sales_rates:
            avg_daily_sales = abs(total_sold) / SALES_WINDOW_DAYS
            daily_sales_map[product_id] = max(avg_daily_sales, 0.01)   # avoid divide-by-zero

        
        # 4. Generate Alerts
        
        alerts = []

        for inv, product, wh, supplier, lead_time in inventory_records:

            threshold = product.threshold or 20

            if inv.quantity >= threshold:
                continue  # not low stock

            # Forecast stockout time
            daily_sales = daily_sales_map.get(product.id, 0.01)
            days_until_stockout = int(inv.quantity / daily_sales)

            alerts.append({
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_id": wh.id,
                "warehouse_name": wh.name,
                "current_stock": inv.quantity,
                "threshold": threshold,
                "days_until_stockout": days_until_stockout,
                "supplier": {
                    "id": supplier.id if supplier else None,
                    "name": supplier.name if supplier else None,
                    "contact_email": supplier.contact_email if supplier else None
                }
            })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        }), 200

    except Exception as e:
        print("Low stock alert error:", e)
        return jsonify({"error": "Internal server error"}), 500
