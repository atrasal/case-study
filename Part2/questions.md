# Part 2 — Questions for the Product Team

1. SKU Scope
- Should SKU be unique globally or only per company?

2. Inventory Granularity
- Do warehouses support bin/shelf/zone storage?
- Do we need lot/batch tracking?

3. Bundles
- Should bundles automatically deduct stock from component products?
- Can bundles be nested (bundle of bundles)?

4. Suppliers
- Can a product have multiple suppliers with different lead times?
- Do we need supplier priority ranking?

5. Forecasting
- What is the default sales window for forecasting?
- Should we calculate moving averages?

6. Inventory Logs
- Do we need fields like user_id for who made the change?
- Should we track reason codes?

7. Product Variants
- Do we need sizes/colors/options?

8. Cost Tracking
- Should we track landed cost, purchase cost, margin?

9. Deletion Behavior
- Hard delete or soft delete for products and warehouses?

10. Multi-tenancy
- Are companies isolated at DB level or row level?
