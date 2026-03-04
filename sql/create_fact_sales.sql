-- Create fact table for sales
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id VARCHAR(20),
    customer_key INT,
    product_key INT,
    date_key INT,
    quantity INT,
    price DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

-- Insert data into fact_sales by joining silver_sales with dimension tables to get the corresponding keys
INSERT INTO fact_sales (
    invoice_id, customer_key, product_key, date_key,
    quantity, price, total_price
)
SELECT
    s.Invoice AS invoice_id,
    c.customer_key,
    p.product_key,
    DATE_FORMAT(s.InvoiceDate, '%Y%m%d') AS date_key,
    s.Quantity,
    s.Price,
    s.Total_price
FROM silver_sales s
LEFT JOIN dim_customer c
    ON c.customer_id = s.CustomerID
LEFT JOIN dim_product p
    ON p.stock_code = s.StockCode
LEFT JOIN dim_date d
    ON d.date_key = DATE_FORMAT(s.InvoiceDate, '%Y%m%d');
