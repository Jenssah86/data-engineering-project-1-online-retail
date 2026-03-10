CREATE PROCEDURE sp_load_dim_product() -- Deze procedure laadt de dim_product tabel met unieke producten en hun beschrijving
BEGIN
    INSERT INTO dim_product (stock_code, description)
    SELECT 
        StockCode, 
        MIN(Description) AS description
    FROM silver_sales
    WHERE StockCode IS NOT NULL
    GROUP BY StockCode
    ON DUPLICATE KEY UPDATE 
        description = VALUES(description); -- Update de description als er een nieuwe waarde is
END $$