-- create_dim_product.sql --

-- Insert data into dim_product from silver_sales
INSERT INTO dim_product (stock_code, description)
SELECT
    StockCode AS stock_code,
    MIN(Description) AS description -- Use MIN to get a single description for each stock_code, assuming the description is consistent for each stock_code
FROM silver_sales
WHERE StockCode IS NOT NULL -- Exclude rows with NULL stock_code to maintain data integrity
GROUP BY StockCode;