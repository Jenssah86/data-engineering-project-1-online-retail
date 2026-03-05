-- load_dim_customer.sql --

-- Inser data in to dim_customer from silver_sales
INSERT INTO dim_customer (customer_id, country)
SELECT DISTINCT CustomerID, Country
FROM silver_sales
WHERE CustomerID IS NOT NULL; -- Exclude rows with NULL customer_id to maintain data integrity
