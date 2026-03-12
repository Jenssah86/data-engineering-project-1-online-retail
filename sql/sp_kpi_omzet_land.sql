CREATE PROCEDURE kpi_omzet_land(
    IN p_land VARCHAR(255)) -- Deze procedure berekent de omzet per land voor een gegeven land
BEGIN
    SELECT 
        d.full_date AS Datum,
        SUM(f.total_price) AS Omzet,
        c.country AS Land
    FROM fact_sales f
    LEFT JOIN dim_date d 
        ON f.date_key = d.date_key
    LEFT JOIN dim_customer c 
        ON c.customer_key = f.customer_key
    WHERE c.country = p_land
    GROUP BY 
        d.full_date,
        c.country;
END