-- Create dimension table for dates
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT,
    day INT,
    weekday INT,
    quarter INT
);

-- CTE to extract unique dates from silver_sales
WITH dates AS (
    SELECT DISTINCT
        DATE(InvoiceDate) AS full_date
    FROM silver_sales
)

-- Insert data into dim_date, transforming full_date into date_key and extracting date components
INSERT INTO dim_date (
    date_key, full_date, year, month, day, weekday, quarter
)
SELECT
    DATE_FORMAT(full_date, '%Y%m%d') AS date_key,
    full_date,
    YEAR(full_date),
    MONTH(full_date),
    DAY(full_date),
    WEEKDAY(full_date),
    QUARTER(full_date)
FROM dates;