# Part 2: Database Design – StockFlow

## Design Goals
- Support multiple companies and warehouses
- Allow products in multiple warehouses
- Track inventory changes over time
- Support suppliers and product bundles

## Key Design Decisions

### Product vs Inventory Separation
Products are warehouse-agnostic. Inventory is warehouse-specific, enabling multi-warehouse scalability.

### Inventory Movements
An append-only inventory_movements table enables auditing, analytics, and debugging stock discrepancies.

### Supplier Relationships
Many-to-many relationship allows multiple suppliers per product and future expansion.

### Bundles
Product bundles are modeled relationally to preserve referential integrity and queryability.

## Indexing & Constraints
- Unique SKU constraint
- Unique (product_id, warehouse_id) inventory constraint
- Non-negative inventory quantities

## Missing Requirements / Questions
1. Is SKU uniqueness global or company-specific?
2. Can products belong to multiple companies?
3. Are negative inventories allowed?
4. Can bundles contain other bundles?
5. Are suppliers warehouse-specific?

## Assumptions
- SKU uniqueness is global
- Inventory quantities cannot be negative
- Bundles contain only standard products
- Products may have multiple suppliers

## Summary
This schema balances scalability, data integrity, and real-world B2B inventory requirements.
