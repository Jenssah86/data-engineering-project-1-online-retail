import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime

# Load .env from project root
load_dotenv()  # leest .env in

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

# Functie om verbinding te maken met MySQL database
def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# Functie om een stored procedure uit te voeren
def run_procedure(conn, procedure_name):
    cursor = conn.cursor()
    print(f"[{datetime.now()}] Running: {procedure_name}")
    cursor.callproc(procedure_name)
    conn.commit()
    cursor.close()
    print(f"[{datetime.now()}] Completed: {procedure_name}")

# Main functie om het ETL proces te starten
def main():
    print("=== Starting Incremental ETL Load ===")
    conn = get_connection()

    # 1. Load dimensions
    run_procedure(conn, "sp_load_dim_customer")
    run_procedure(conn, "sp_load_dim_product")
    run_procedure(conn, "sp_load_dim_date")

    # 2. Load fact table
    run_procedure(conn, "sp_load_fact_sales")

    conn.close()
    print("=== Incremental ETL Load Finished ===")

# Entry point van het script
if __name__ == "__main__":
    main()
