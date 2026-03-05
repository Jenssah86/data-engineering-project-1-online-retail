-- create_dim_customer.sql --

-- Create dimension table for customers
CREATE TABLE IF NOT EXISTS dim_customer ( 
    customer_key INT AUTO_INCREMENT PRIMARY KEY, -- Surrogate key for customers
    customer_id INT NOT NULL,
    country VARCHAR(100),
    UNIQUE (customer_id) -- Ensure customer_id is unique to prevent duplicates
);