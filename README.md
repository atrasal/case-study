StockFlow is a conceptual B2B SaaS inventory management platform designed for small and medium-sized businesses.
It allows companies to manage products across multiple warehouses, track inventory changes, work with suppliers, and receive low-stock alerts to prevent stockouts.

This repository contains my solution to the take-home case study, structured into three parts:

Part 1: Code Review & Debugging

Part 2: Database Design

Part 3: Low-Stock Alert API Implementation

The focus is on backend correctness, scalability, and real-world SaaS considerations, rather than a fully runnable application.

🧩 Repository Structure
case-study/
├── Part1/
│   ├── explanation_part1.md
│   ├── fixed_endpoint.py
│   └── issues.md
│
├── Part2/
│   ├── schema.sql
│   ├── explanation.md
│   └── questions.md
│
├── Part3/
│   ├── low_stocks_alert.py
│   ├── explanation_part3.md
│   └── assumptions.md
│
└── README.md

✅ Part 1 — Code Review & Debugging
Objective

Review an existing API endpoint for creating products and:

Identify technical and business logic issues

Explain real-world production impact

Provide a corrected, production-safe version

Key Improvements

Added proper input validation

Enforced SKU uniqueness

Corrected product vs warehouse relationship

Ensured atomic transactions

Improved error handling

Used Decimal for price accuracy

Made inventory creation optional

📄 Files:

issues.md — list of issues and impacts

fixed_endpoint.py — corrected API implementation

explanation_part1.md — reasoning behind changes

🧱 Part 2 — Database Design
Objective

Design a scalable database schema for:

Multi-company, multi-warehouse inventory

Supplier management

Inventory change tracking

Product bundles

Key Design Decisions

Separate products and inventory for multi-warehouse support

Use inventory_log for auditing and forecasting

Enforce SKU uniqueness at company level

Support bundles via self-referencing join table

Use soft deletes to preserve history

Add indexes for SaaS-scale performance

Included

SQL DDL schema

Design explanations

Missing requirement questions for product team

📄 Files:

schema.sql

explanation.md

questions.md

🚨 Part 3 — Low-Stock Alert API
Endpoint
GET /api/companies/{company_id}/alerts/low-stock

Business Rules Implemented

Threshold varies per product

Alerts only for products with recent sales

Inventory evaluated per warehouse

Supplier details included for reordering

Forecast days_until_stockout using recent sales data

Key Concepts

Trailing 30-day sales window

Average daily consumption rate

Warehouse-level alerts

Graceful handling of missing data

Clear assumptions due to incomplete requirements

📄 Files:

low_stocks_alert.py

explanation_part3.md

assumptions.md

🧠 Assumptions & Scope

This is not a fully runnable application

Focus is on design, reasoning, and correctness

Assumptions are explicitly documented in each part

Forecasting logic is intentionally simple due to missing requirements

Bundles are excluded from alerts unless specified otherwise

📈 Scalability & SaaS Considerations

Multi-tenant isolation via company_id

Indexed queries for large datasets

Transaction safety to prevent partial writes

Audit-friendly inventory logs

Extensible schema for future features (variants, batch tracking, bins)

💬 What This Submission Demonstrates

Strong backend fundamentals

Production-oriented thinking

Ability to work with incomplete requirements

Clear communication and documentation

Real-world B2B SaaS design awareness

🏁 Final Notes

This case study was approached as a real production system, not just an academic exercise.
Trade-offs, assumptions, and future extensions are intentionally documented to reflect collaboration with product and engineering teams.

Author: Aaditya Rasal
Purpose: Backend Engineering Case Study
Tech Stack (assumed): Python, Flask, SQLAlchemy, PostgreSQL
