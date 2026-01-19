# Part 2 — Database Design Notes

## 1. Companies → Warehouses (One-to-Many)
A company can operate multiple warehouses.

## 2. Products
Products belong to a company.
SKU is unique per company (not globally).

Fields:
- threshold: used for low-stock alerts
- is_deleted: soft delete for audit & referential integrity

## 3. Inventory (product + warehouse)
This table tracks stock levels per warehouse.
The UNIQUE(product_id, warehouse_id) constraint ensures exactly one row per warehouse.

## 4. Inventory Log
Tracks all stock changes over time.
Useful for:
- audit trails
- forecasting
- low-stock prediction

## 5. Suppliers
Suppliers mapped per company.

## 6. supplier_products (many-to-many)
A supplier may supply many products; a product may have multiple suppliers.

Lead time is stored here since it varies per supplier.

## 7. Bundles (product_components)
A bundle is a product composed of other products.

- Uses a self join via product_components
- Allows flexible kit definitions

## 8. Indexing Choices
- SKU index → fast lookup
- inventory(product_id, warehouse_id) → fast joins for alerts
- inventory_log(product_id, created_at) → fast forecasting
- warehouse/company indexes → multi-tenant SaaS performance

## 9. Soft Deletes
Products have an `is_deleted` flag to avoid breaking FK constraints.
Keeps historical logs intact.

## 10. Constraints for Data Quality
- Positive quantity in bundle components
- Non-negative inventory
- ENUM-like checks for change_type
