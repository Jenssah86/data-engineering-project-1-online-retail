-- Create dimension table for customers
CREATE TABLE IF NOT EXISTS dim_customer ( 
    customer_key INT AUTO_INCREMENT PRIMARY KEY, -- Surrogate key for customers
    customer_id INT NOT NULL,
    country VARCHAR(100),
    UNIQUE (customer_id) -- Ensure customer_id is unique to prevent duplicates
);

-- CTE to clean and deduplicate customer data
WITH cleaned AS ( 
    SELECT DISTINCT
        CustomerID AS customer_id,
        Country AS country
    FROM silver_sales
    WHERE CustomerID IS NOT NULL
)

-- Inser data in to dim_customer from cleaned CTE, ensuring only unique customers are added
INSERT INTO dim_customer (customer_id, country)
SELECT customer_id, country
FROM cleaned;