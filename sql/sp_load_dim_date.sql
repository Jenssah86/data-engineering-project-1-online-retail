CREATE PROCEDURE sp_load_dim_date() -- Deze procedure laadt de dim_date tabel met unieke datums en hun bijbehorende jaar, maand en dag
BEGIN
    INSERT INTO dim_date (date_key, full_date, year, month, day, weekday, quarter)
    SELECT DISTINCT 
        DATE(InvoiceDate) AS date,
        YEAR(InvoiceDate) AS year,
        MONTH(InvoiceDate) AS month,
        DAY(InvoiceDate) AS day,
        WEEKDAY(InvoiceDate) AS weekday,
        QUARTER(InvoiceDate) AS quarter
    FROM silver_sales s
    LEFT JOIN dim_date d 
    ON d.date_key = DATEFORMAT(s.InvoiceDate, '%Y%m%d') -- Transformeer full_date naar date_key in het formaat YYYYMMDD
    WHERE d.date_key IS NULL; -- Alleen nieuwe datums toevoegen
    GROUP BY DATE(s.InvoiceDate); -- Groeperen op datum om dubbele invoer te voorkomen
END