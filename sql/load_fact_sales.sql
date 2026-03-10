INSERT INTO fact_sales (
    invoice_id, customer_key, product_key, date_key,
    quantity, price, total_price
)
SELECT
    s.Invoice AS invoice_id,
    c.customer_key,
    p.product_key,
    d.date_key,
    ROUND(SUM(s.Quantity), 2) AS quantity,
    ROUND(SUM(s.Price * s.Quantity) / SUM(s.Quantity), 2) AS price,
    ROUND(SUM(s.Price * s.Quantity), 2) AS total_price
FROM silver_sales s
LEFT JOIN dim_customer c
    ON c.customer_id = s.CustomerID
LEFT JOIN dim_product p
    ON p.stock_code = s.StockCode
LEFT JOIN dim_date d
    ON d.date_key = DATE_FORMAT(s.InvoiceDate, '%Y%m%d')
GROUP BY
    s.Invoice,
    c.customer_key,
    p.product_key,
    d.date_key;