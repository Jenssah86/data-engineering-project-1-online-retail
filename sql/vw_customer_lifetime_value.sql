CREATE OR REPLACE VIEW vw_customer_lifetime_value AS
SELECT
    c.customer_key,
    SUM(f.total_price) AS lifetime_value,
    COUNT(DISTINCT f.invoice_id) AS aantal_orders,
    SUM(f.quantity) AS totaal_items
FROM fact_sales f
INNER JOIN dim_customer c 
    ON c.customer_key = f.customer_key
GROUP BY c.customer_key;