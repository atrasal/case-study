# Part 1 — Issues Identified in Original Code

## 1. No Input Validation
- Code assumes all fields exist in request JSON.
- Missing validation for formats, nulls, negative values.

**Impact:** Random 500 errors, broken API reliability.

---

## 2. SKU Uniqueness Not Enforced
- Backend does not check if SKU already exists.
- DB may accept duplicates if constraint missing.

**Impact:** Search, analytics, and inventory accuracy break.

---

## 3. Incorrect Product–Warehouse Relationship
- Product model incorrectly stores warehouse_id.
- Products should exist globally; inventory is warehouse-specific.

**Impact:** Cannot manage multi-warehouse inventory correctly.

---

## 4. Two Separate Commits → Partial Writes
- product commit happens before inventory commit.

**Impact:** If inventory insert fails, product is created without stock entry.

---

## 5. Not Using a Database Transaction Block
- Each commit is handled individually.

**Impact:** Data inconsistency & rollback issues.

---

## 6. Price Type Not Validated
- Floats used instead of Decimal/Numeric.

**Impact:** Rounding errors in billing & reporting.

---

## 7. Missing Optional Field Handling
- initial_quantity and warehouse_id are required implicitly.

**Impact:** API breaks for optional cases.

---

## 8. No Error Handling
- Exceptions from SQLAlchemy leak into client.

**Impact:** Poor user experience & confusing behavior.

---

## 9. Inventory Created Even If Warehouse Not Provided
- Does not check for warehouse existence.

**Impact:** Invalid inventory rows; FK violation.
