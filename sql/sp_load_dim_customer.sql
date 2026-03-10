CREATE PROCEDURE sp_load_dim_customer() -- Deze procedure laadt de dim_customer tabel met unieke klanten en hun land
BEGIN
    INSERT INTO dim_customer (customer_id, country)
    SELECT DISTINCT 
        Customer_id, 
        Country
    FROM silver_sales
    WHERE CustomerID IS NOT NULL
    ON DUPLICATE KEY UPDATE 
        country = VALUES(country); -- Update het land als er een nieuwe waarde is
END