# Part 3 — Low Stock Alert API: Design Explanation

## 1. High-Level Logic
The endpoint returns products that:
1. Belong to the company
2. Had recent sales activity (last 30 days)
3. Are below their configured threshold
4. Must include supplier details for replenishment

Each warehouse is evaluated independently.

---

## 2. Recent Sales Filtering
Low-stock alerts are only meaningful when stock is actually moving.
So we filter using inventory_log:

change_type = 'sale'

This avoids alerting stale or discontinued products.

---

## 3. Forecasting Logic
To estimate `days_until_stockout`:

1. Sum all sales in the last 30 days
2. Derive average daily sales rate
3. Apply:

days = current_stock / avg_daily_sales

Even if sales are low, we enforce a minimum daily sales of 0.01 to avoid division errors.

---

## 4. Supplier Information
If SupplierProduct has a supplier entry, we include:
- supplier id
- name
- contact email
- lead time

This helps users reorder quickly.

---

## 5. Warehouse-Level Evaluation
Each warehouse has independent inventory rows.
Alerts are generated per warehouse.

---

## 6. SQL / ORM Query Optimization
- `distinct()` used to avoid duplicated product IDs
- Aggregation only done for products with recent sales
- Joined queries reduce N+1 issues

---

## 7. Error Handling
All unexpected issues return a clean 500 response.

---

## 8. Business Logic Compliance
- Threshold read from products table
- Bundles excluded by default (assumption)
- Soft-deleted products ignored

---

## 9. Pagination (Optional Extension)
Can be implemented with:

?limit=50&offset=0

But not required for this assignment.
