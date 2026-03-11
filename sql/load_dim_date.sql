-- create_dim_date.sql --

-- Insert data into dim_date, transforming full_date into date_key and extracting date components
INSERT INTO dim_date (
    date_key, full_date, year, month, day, quarter
)
SELECT DISTINCT
    DATE_FORMAT(InvoiceDate, '%Y%m%d') AS date_key, -- Transform full_date into an integer in the format YYYYMMDD for date_key
    InvoiceDate,
    YEAR(InvoiceDate),
    MONTH(InvoiceDate),
    DAY(InvoiceDate),
    QUARTER(InvoiceDate)
FROM silver_sales;