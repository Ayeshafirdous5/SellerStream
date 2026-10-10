-- =========================================
-- SellerStream Data Warehouse Schema
-- =========================================


-- =========================================
-- 1. Customer Dimension
-- =========================================

CREATE TABLE dim_customer (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(50) DEFAULT 'India',
    signup_date DATE,
    customer_segment VARCHAR(30)
);


-- =========================================
-- 2. Seller Dimension
-- =========================================

CREATE TABLE dim_seller (
    seller_id VARCHAR(20) PRIMARY KEY,
    seller_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    seller_category VARCHAR(50),
    join_date DATE,
    seller_rating DECIMAL(3,2),
    seller_status VARCHAR(20)
);


-- =========================================
-- 3. Product Dimension
-- =========================================

CREATE TABLE dim_product (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    brand VARCHAR(100),
    seller_id VARCHAR(20),
    unit_price DECIMAL(10,2),
    cost_price DECIMAL(10,2),
    launch_date DATE,
    product_status VARCHAR(20),

    FOREIGN KEY (seller_id)
        REFERENCES dim_seller(seller_id)
);


-- =========================================
-- 4. Order Header Fact Table
-- =========================================

CREATE TABLE fact_order_header (
    order_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    order_status VARCHAR(30),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id)
);


-- =========================================
-- 5. Order Lines Fact Table
-- =========================================

CREATE TABLE fact_orders (
    order_line_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    seller_id VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    order_status VARCHAR(30),

    FOREIGN KEY (order_id)
        REFERENCES fact_order_header(order_id),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    FOREIGN KEY (seller_id)
        REFERENCES dim_seller(seller_id)
);


-- =========================================
-- 6. Payments Fact Table
-- =========================================

CREATE TABLE fact_payments (
    payment_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(30),
    payment_status VARCHAR(30),
    payment_amount DECIMAL(12,2) NOT NULL,
    refund_amount DECIMAL(12,2) DEFAULT 0,

    FOREIGN KEY (order_id)
        REFERENCES fact_order_header(order_id)
);


-- =========================================
-- 7. Shipments Fact Table
-- =========================================

CREATE TABLE fact_shipments (
    shipment_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    seller_id VARCHAR(20) NOT NULL,
    shipment_date DATE,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    shipping_provider VARCHAR(50),
    shipping_status VARCHAR(30),
    delivery_days INT,

    FOREIGN KEY (order_id)
        REFERENCES fact_order_header(order_id),

    FOREIGN KEY (seller_id)
        REFERENCES dim_seller(seller_id)
);


-- =========================================
-- 8. Returns Fact Table
-- =========================================

CREATE TABLE fact_returns (
    return_id VARCHAR(30) PRIMARY KEY,
    order_line_id VARCHAR(30) NOT NULL,
    return_date DATE NOT NULL,
    return_reason VARCHAR(100),
    return_status VARCHAR(30),
    refund_amount DECIMAL(12,2) DEFAULT 0,

    FOREIGN KEY (order_line_id)
        REFERENCES fact_orders(order_line_id)
);

-- =========================================
-- 9. Inventory Fact Table
-- =========================================

CREATE TABLE fact_inventory (
    inventory_id VARCHAR(30) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    seller_id VARCHAR(20) NOT NULL,
    inventory_date DATE NOT NULL,
    location VARCHAR(100),
    available_quantity INT NOT NULL,
    reserved_quantity INT DEFAULT 0,
    reorder_level INT DEFAULT 0,
    stock_status VARCHAR(30),

    FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    FOREIGN KEY (seller_id)
        REFERENCES dim_seller(seller_id)
);

-- =========================================
-- 10. Reviews Fact Table
-- =========================================

CREATE TABLE fact_reviews (
    review_id VARCHAR(30) PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    seller_id VARCHAR(20) NOT NULL,
    review_date DATE NOT NULL,
    rating INT NOT NULL,
    review_text TEXT,
    review_status VARCHAR(30),

    FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    FOREIGN KEY (seller_id)
        REFERENCES dim_seller(seller_id)
);