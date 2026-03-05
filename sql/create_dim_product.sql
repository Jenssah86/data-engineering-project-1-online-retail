-- create_dim_product.sql --

-- Create dimension table for products
CREATE TABLE IF NOT EXISTS dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    UNIQUE (stock_code)
);
