CREATE OR REPLACE VIEW vw_top_10_producten AS
SELECT 
    p.product_key AS Product,
    p.description AS Omschrijving,
    SUM(f.total_price) AS Omzet
FROM fact_sales f
LEFT JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY 
    p.product_key,
    p.description
ORDER BY Omzet DESC
LIMIT 10;