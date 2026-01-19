# Part 3 – Assumptions & Edge Cases

## Assumptions
- Low stock threshold is stored per product
- Recent sales means activity within the last 30 days
- Sales velocity is calculated as average daily sales
- Each product has at most one primary supplier
- Inventory quantities are non-negative
- Products with no recent sales are excluded from alerts

## Edge Cases Handled
- Multiple warehouses per company
- Products without suppliers
- Products without thresholds
- Division by zero prevention
- Zero or stale sales data

## Performance Considerations
- Indexed foreign keys for joins
- Business logic kept out of controllers where possible
- Can be optimized using cached sales metrics or background jobs
