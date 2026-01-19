Part 1: Code Review & Debugging

StockFlow – Product Creation API

1. Original Code Under Review
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    
    # Create new product
    product = Product(
        name=data['name'],
        sku=data['sku'],
        price=data['price'],
        warehouse_id=data['warehouse_id']
    )
    
    db.session.add(product)
    db.session.commit()
    
    # Update inventory count
    inventory = Inventory(
        product_id=product.id,
        warehouse_id=data['warehouse_id'],
        quantity=data['initial_quantity']
    )
    
    db.session.add(inventory)
    db.session.commit()
    
    return {"message": "Product created", "product_id": product.id}


The code compiles and works in simple cases, but fails under real production conditions.

2. Issues Identified
2.1 Technical Issues

No input validation

Direct access to data['field'] can raise KeyError

No type validation for numeric fields

Multiple database commits

Product and inventory are committed in separate transactions

No transaction management

Partial writes are possible if inventory creation fails

SKU uniqueness not enforced

Duplicate SKUs can be created concurrently

Price precision not handled

Price is likely stored as a floating-point number

No exception handling

Database errors surface as generic 500 responses

Race condition risk

Two parallel requests can insert the same SKU

2.2 Business Logic Issues

Product incorrectly coupled to warehouse

Products should exist independently of warehouses

Does not support multi-warehouse inventory

A product can exist in multiple warehouses

Inventory creation assumed mandatory

Some workflows create products before stocking

Initial quantity assumed always present

Breaks cases where inventory is added later

3. Production Impact
Issue	Impact
No validation	API crashes on malformed requests
No transaction	Orphan products or missing inventory
Duplicate SKUs	Ordering, reporting, billing failures
Float pricing	Financial inaccuracies
Single-warehouse design	Limits platform scalability
No error handling	Poor client experience
4. Explanation of Fixes
Transaction Safety

with db.session.begin() ensures all-or-nothing behavior

Prevents orphaned records

Precision Handling

Decimal ensures accurate financial calculations

Decoupled Product Model

Product is no longer tied directly to a warehouse

Supports multi-warehouse inventory

Optional Inventory

Enables product-first workflows

More flexible for B2B use cases

Explicit Error Handling

Prevents silent failures

Returns meaningful HTTP status codes

5. Assumptions Made

SKU uniqueness is enforced globally

Inventory creation is optional at product creation

One inventory record per (product_id, warehouse_id)

Price values require financial precision

Product creation should not fail due to missing inventory

6. Summary

This refactor:

Improves data integrity

Aligns with real-world B2B inventory workflows

Supports multi-warehouse scalability

Prevents financial and operational errors

Provides a clean, maintainable API contract