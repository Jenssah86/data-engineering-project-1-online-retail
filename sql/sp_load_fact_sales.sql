CREATE PROCEDURE sp_load_fact_sales() -- Deze procedure laadt de fact_sales tabel met verkoopgegevens en koppelt deze aan de dimensietabellen
BEGIN
    INSERT INTO fact_sales (
        invoice_id,
        customer_key,
        product_key,
        date_key,
        quantity,
        price,
        total_price
        )
    SELECT 
        s.Invocie,
        c.customer_key,
        p.product_key,
        s.StockCode,
        ROUND(SUM(s.Quantity), 2) AS quantity, -- Totaal aantal verkochte eenheden
        ROUND(SUM(s.Price * s.Quantity) / NULLIF(SUM(s.Quantity), 0), 2) AS price, -- Gemiddelde prijs per eenheid
        ROUND(SUM(s.Price * s.Quantity), 2) AS total_price -- Totale omzet
    FROM silver_sales s 
    LEFT JOIN dim_customer c 
        ON s.CustomerID = c.customer_id
    LEFT JOIN dim_product p 
        ON s.StockCode = p.stock_code   
    LEFT JOIN dim_date d 
        ON d.datekey = DATEFORMAT(s.InvoiceDate, '%Y%m%d') -- Transformeer full_date naar date_key in het formaat YYYYMMDD
    GROUP BY 
    s.Invoice, 
    c.customer_key, 
    p.product_key, 
    d.date_key
    ON DUPLICATE KEY UPDATE 
        quantity = VALUES(quantity), -- Update de quantity als er een nieuwe waarde is
        price = VALUES(price), -- Update de price als er een nieuwe waarde is
        total_price = VALUES(total_price); -- Update de total_price als er een nieuwe waarde is
END $$
