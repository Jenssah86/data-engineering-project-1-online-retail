-- Create dimension table for products
CREATE TABLE IF NOT EXISTS dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    UNIQUE (stock_code)
);

-- CTE to extract unique products from silver_sales
WITH cleaned AS (
    SELECT DISTINCT
        StockCode AS stock_code,
        Description AS description
    FROM silver_sales
)

-- Insert data into dim_product, ensuring only unique products are added
INSERT INTO dim_product (stock_code, description)
SELECT stock_code, description
FROM cleaned;