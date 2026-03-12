import pandas as pd
from datetime import date
from pathlib import Path
from sqlalchemy import create_engine
import shutil
import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------------------------------------
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

# ---------------------------------------------------------------------------------------
# 2. Absolute project directory (BELANGRIJK VOOR TAAKPLANNER)
# ---------------------------------------------------------------------------------------
BASE_DIR = Path(r"D:\Studie\GitHub portfolio\data-engineering-project-1-online-retail")

BRONZE_DIR = BASE_DIR / "bronze"
PROCESSED_DIR = BRONZE_DIR / "verwerkt"

# Zorg dat de mappen bestaan
BRONZE_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------------------
# 3. Bronze CSV-bestanden zoeken
# ---------------------------------------------------------------------------------------
def get_bronze_files():
    return list(BRONZE_DIR.glob("online_retail_*.csv"))

# ---------------------------------------------------------------------------------------
# 4. Data inlezen
# ---------------------------------------------------------------------------------------
def load_bronze_file(path: Path) -> pd.DataFrame:
    print(f"Inlezen: {path.name}")
    return pd.read_csv(path, sep=";")

# ---------------------------------------------------------------------------------------
# 5. Data opschonen
# ---------------------------------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.replace(" ", "")
    df = df.dropna(subset=["CustomerID", "Invoice", "StockCode"])
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce",
        dayfirst=True
    ).dt.date
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = df["Price"].str.replace(",", ".", regex=False)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Total_price"] = (df["Quantity"] * df["Price"]).round(2)
    return df

# ---------------------------------------------------------------------------------------
# 6. MySQL connectie
# ---------------------------------------------------------------------------------------
def get_engine():
    url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    return create_engine(url)

# ---------------------------------------------------------------------------------------
# 7. Wegschrijven naar Silver
# ---------------------------------------------------------------------------------------
def write_to_silver(df: pd.DataFrame):
    engine = get_engine()
    df.to_sql(
        name="silver_sales",
        con=engine,
        if_exists="append",
        index=False
    )
    print("Data toegevoegd aan silver_sales.")

# ---------------------------------------------------------------------------------------
# 8. Verwerkt bestand verplaatsen
# ---------------------------------------------------------------------------------------
def move_to_processed(path: Path):
    destination = PROCESSED_DIR / path.name
    shutil.move(str(path), destination)
    print(f"Verplaatst naar: {destination}")

# ---------------------------------------------------------------------------------------
# 9. Main flow
# ---------------------------------------------------------------------------------------
def main_flow():
    print("Zoeken naar nieuwe bronze CSV-bestanden...")

    files = get_bronze_files()

    if not files:
        print("Geen nieuwe bestanden gevonden.")
        return

    for file in files:
        df_raw = load_bronze_file(file)
        df_clean = clean_data(df_raw)
        write_to_silver(df_clean)
        move_to_processed(file)

    print("Alle nieuwe bestanden zijn verwerkt en verplaatst.")

# ---------------------------------------------------------------------------------------
# 10. Uitvoeren
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":
    main_flow()