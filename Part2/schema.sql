-- STOCKFLOW — Database Schema


-- Companies

CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);


-- Warehouses

CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_warehouses_company ON warehouses(company_id);


-- Products

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    is_bundle BOOLEAN DEFAULT FALSE,
    threshold INT DEFAULT 20,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(company_id, sku)
);

CREATE INDEX idx_products_company ON products(company_id);


-- Bundle Components (Many-to-Many)

CREATE TABLE product_components (
    bundle_id INT REFERENCES products(id),
    component_id INT REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY(bundle_id, component_id)
);


-- Inventory (Per-Warehouse Stock)

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(id),
    warehouse_id INT NOT NULL REFERENCES warehouses(id),
    quantity INT DEFAULT 0 CHECK (quantity >= 0),
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(product_id, warehouse_id)
);

CREATE INDEX idx_inventory_product_warehouse
    ON inventory(product_id, warehouse_id);


-- Inventory Log (Audit + Forecasting)

CREATE TABLE inventory_log (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(id),
    warehouse_id INT NOT NULL REFERENCES warehouses(id),
    change_type VARCHAR(20) NOT NULL CHECK (
        change_type IN ('sale', 'restock', 'adjustment')
    ),
    quantity_change INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_inventorylog_product_date
    ON inventory_log(product_id, created_at);


-- Suppliers

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    company_id INT NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255)
);


-- Supplier - Product Mapping

CREATE TABLE supplier_products (
    supplier_id INT REFERENCES suppliers(id),
    product_id INT REFERENCES products(id),
    lead_time_days INT DEFAULT 7,
    PRIMARY KEY(supplier_id, product_id)
);

CREATE INDEX idx_supplier_products_supplier
    ON supplier_products(supplier_id);
