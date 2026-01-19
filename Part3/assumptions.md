# Part 3 — Assumptions

1. Recent Sales Window
- We use a 30-day window to determine "recent sales".

2. Sales Logs
- Negative quantity_change represents sales.
- All sales are recorded in inventory_log.

3. Forecasting
- Based on moving average of last 30 days' sales.
- Minimum consumption rate = 0.01 units/day.

4. Thresholds
- If threshold field is NULL → default to 20.

5. Multiple Suppliers
- Only primary supplier is shown.
  (Assumption: whichever matches supplier_products row)

6. Bundles
- Bundles are ignored for low-stock alerts.
- Only physical products generate alerts.

7. Deletions
- Products with is_deleted = TRUE are ignored.

8. Concurrency
- Inventory rows are assumed updated atomically by other endpoints.

9. Multi-Tenancy
- Company_id filtering ensures isolation.

10. Zero Inventory Logs
- If no sales exist for a product → no alert generated.
