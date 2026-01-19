# Part 1 — Explanation of Changes

## 1. Validation Layer Added
Ensures required fields exist and validates formats for price and quantity.

## 2. Decimal Used for Price
Avoids floating-point rounding errors.

## 3. Removed warehouse_id from Product
Product is a global entity. Inventory varies per warehouse.

## 4. Atomic Transaction (db.session.begin)
Product + inventory creation is now atomic.
Prevents partial writes.

## 5. Proper Error Handling
User-friendly responses for:
- missing fields
- bad formats
- SKU duplicates
- server errors

## 6. Optional Inventory Creation
Supports product creation without assigning to a warehouse initially.

## 7. Clean Return Format
REST-friendly JSON responses.
