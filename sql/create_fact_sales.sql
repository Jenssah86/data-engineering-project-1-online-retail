-- create_fact_sales.sql --

-- Create fact table for sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id VARCHAR(20),
    customer_key INT,
    product_key INT,
    date_key INT,
    quantity INT,
    price DECIMAL(18, 2),
    total_price DECIMAL(18, 2),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key), -- Establish foreign key relationship with dim_customer
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key), -- Establish foreign key relationship with dim_product
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key) -- Establish foreign key relationship with dim_date
);