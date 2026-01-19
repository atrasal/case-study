# StockFlow – Inventory Management System (B2B SaaS)

This repository contains my solution to the **StockFlow take-home assignment**, designed to evaluate backend engineering skills including API design, database modeling, debugging, and working with incomplete requirements in a real-world B2B SaaS context.

The solution is structured into three clearly separated parts to emphasize clarity, reasoning, and maintainability.

---

## Tech Stack (Assumed)

- **Backend**: Python, Flask  
- **ORM**: SQLAlchemy  
- **Database**: PostgreSQL (relational, ACID-compliant)  
- **API Style**: REST  
- **Architecture**: Modular, transaction-safe, scalable for B2B SaaS systems  

---

## Repository Structure

stockflow-backend/
├── README.md
├── Part1/
│ ├── issues.md
│ └── fixed_endpoint.py
├── Part2/
│ ├── schema.sql
│ └── explanation.md
└── Part3/
├── low_stock_alert.py
└── assumptions.md

---

## Part 1 – Code Review & Debugging

**Location:** `Part1/`

This section reviews and fixes an existing API endpoint responsible for product creation.

### Key Topics Covered
- Identification of technical and business-logic issues
- Transaction safety and atomic operations
- SKU uniqueness enforcement
- Precision-safe handling of monetary values
- Support for multi-warehouse inventory workflows

### Files
- `issues.md`  
  Detailed analysis of issues, production impact, fixes, assumptions, and summary.

- `fixed_endpoint.py`  
  Corrected implementation using proper transaction management, validation, and error handling.

---

## Part 2 – Database Design

**Location:** `Part2/`

This section proposes a relational database schema to support a multi-tenant B2B inventory platform.

### Key Topics Covered
- Multi-company and multi-warehouse support
- Product–inventory separation
- Inventory audit trail via movement tracking
- Supplier relationships
- Product bundles
- Constraints, indexes, and scalability considerations

### Files
- `schema.sql`  
  SQL DDL defining tables, relationships, and constraints.

- `explanation.md`  
  Explanation of design decisions, assumptions, and open questions for the product team.

---

## Part 3 – Low Stock Alerts API

**Location:** `Part3/`

This section implements an API endpoint that returns low-stock alerts for a company.

### Endpoint
GET /api/companies/{company_id}/alerts/low-stock

### Key Topics Covered
- Multi-warehouse alert generation
- Product-specific low-stock thresholds
- Filtering based on recent sales activity
- Supplier information for reordering
- Estimation of days until stockout
- Handling of edge cases and missing data

### Files
- `low_stock_alert.py`  
  API implementation with clear separation of concerns.

- `assumptions.md`  
  Business assumptions, edge cases handled, and performance considerations.

---

## Key Assumptions (Summary)

- SKU uniqueness is enforced globally
- Products can exist in multiple warehouses
- Inventory quantities cannot be negative
- Low-stock thresholds are defined per product
- Only products with recent sales activity generate alerts
- Each product has at most one primary supplier

All assumptions are explicitly documented in their respective sections.

---

## Notes for Reviewers

- The solution prioritizes **clarity, correctness, and reasoning** over over-optimization
- Design decisions are documented due to intentionally incomplete requirements
- Code and schema are written with **production readiness** in mind
- Emphasis is placed on **data integrity, scalability, and maintainability**

---

## Author

**Aaditya Rasal**

This repository is submitted as part of the **StockFlow backend selection process**.
