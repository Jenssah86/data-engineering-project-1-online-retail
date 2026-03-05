-- load_fact_sales.sql --

-- Insert data into fact_sales by joining silver_sales with dimension tables to get the corresponding keys
INSERT INTO fact_sales (
    invoice_id, customer_key, product_key, date_key,
    quantity, price, total_price
)
SELECT
    s.Invoice AS invoice_id,
    c.customer_key,
    p.product_key,
    d.date_key,
    s.Quantity,
    s.Price,
    s.Total_price
FROM silver_sales s
LEFT JOIN dim_customer c -- Join with dim_customer to get customer_key
    ON c.customer_id = s.CustomerID
LEFT JOIN dim_product p -- Join with dim_product to get product_key
    ON p.stock_code = s.StockCode
LEFT JOIN dim_date d -- Join with dim_date to get date_key
    ON d.date_key = DATE_FORMAT(s.InvoiceDate, '%Y%m%d'); -- Assuming date_key in dim_date is in 'YYYYMMDD' format
