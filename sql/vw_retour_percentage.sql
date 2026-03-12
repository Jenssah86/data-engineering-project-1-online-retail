CREATE OR REPLACE VIEW vw_retour_percentage AS
SELECT
    SUM(CASE WHEN quantity < 0 THEN ABS(total_price) ELSE 0 END) AS Retour_aantal,
    SUM(CASE WHEN quantity >= 0 THEN total_price ELSE 0 END) AS Verkoop_aantal,
    ROUND(
        (
            SUM(CASE WHEN quantity < 0 THEN ABS(total_price) ELSE 0 END) /
            SUM(CASE WHEN quantity >= 0 THEN total_price ELSE 0 END)
        ) * 100,
        2
    ) AS Retour_percentage
FROM fact_sales;