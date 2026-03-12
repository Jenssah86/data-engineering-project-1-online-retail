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
load_dotenv()  # leest .env in

# haalt de database connectie gegevens op uit de omgevingsvariabelen, deze moeten in een .env bestand staan in dezelfde map als dit script
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")


# ---------------------------------------------------------------------------------------
# 2. Instellingen
# ---------------------------------------------------------------------------------------
BRONZE_DIR = Path("bronze")                     # map waar de CSV-bestanden worden geplaatst
PROCESSED_DIR = BRONZE_DIR / "verwerkt"         # map waar de verwerkte bestanden naartoe worden verplaatst
PROCESSED_DIR.mkdir(exist_ok=True)              # zorgt ervoor dat de map 'verwerkt' bestaat, anders wordt deze gemaakt


# ---------------------------------------------------------------------------------------
# 3. Bronze CSV-bestanden zoeken # functie die CSV-files in de bronze map zoekt en een lijst teruggeeft voor in de FOR loop van de main_flow functie
# ---------------------------------------------------------------------------------------
def get_bronze_files():
    return list(BRONZE_DIR.glob("online_retail_*.csv"))


# ---------------------------------------------------------------------------------------
# 4. Data inlezen # functie die een CSV-bestand inleest en teruggeeft als DataFrame
# ---------------------------------------------------------------------------------------
def load_bronze_file(path: Path) -> pd.DataFrame:   # vraagt om een pad naar een CSV-bestand en geeft een DataFrame terug
    print(f"Inlezen: {path.name}")
    return pd.read_csv(path, sep=";")               # leest het CSV-bestand in met een puntkomma als scheidingsteken, en geeft DataFrame terug


# ---------------------------------------------------------------------------------------
# 5. Data opschonen # functie die de data opschoont en teruggeeft als DataFrame
# ---------------------------------------------------------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:                                      # vraagt om een df en geeft een geschoonde df terug
    df.columns = df.columns.str.strip().str.replace(" ", "")                           # verwijdert eventuele spaties in de kolomnamen
    df = df.dropna(subset=["CustomerID", "Invoice", "StockCode"])                      # verwijdert rijen waar deze belangrijke kolommen leeg zijn
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"],                              # kolom om zetten naar datetime, en haalt alleen de datum eruit
    errors="coerce",
    dayfirst=True
    ).dt.date
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")                    # probeert de 'Quantity' kolom om te zetten naar numeriek
    df["Price"] = df["Price"].str.replace(",", ".", regex=False)                       # vervangt komma's door punten in de 'Price' kolom
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")                          # probeert de 'UnitPrice' kolom om te zetten naar numeriek
    df["Total_price"] = (df["Quantity"] * df["Price"]).round(2)                        # voegt een nieuwe kolom 'total_amount' berekening toe

    return df


# ---------------------------------------------------------------------------------------
# 6. MySQL connectie # functie die een SQLAlchemy engine maakt voor de MySQL database
# ---------------------------------------------------------------------------------------
def get_engine():
    url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"   # bouwt de database URL op basis van de omgevingsvariabelen
    return create_engine(url)   # maakt een SQLAlchemy engine aan met de opgegeven URL, voor verbinding met MySQL database


# ---------------------------------------------------------------------------------------
# 7. Wegschrijven naar Silver # functie die de opgeschoonde data wegschrijft naar de MySQL database
# ---------------------------------------------------------------------------------------
def write_to_silver(df: pd.DataFrame):
    engine = get_engine()          # haalt de SQLAlchemy engine op met de get_engine functie

    df.to_sql(                     # gebruikt de to_sql methode van de DataFrame om de data weg te schrijven naar de database
        name="silver_sales",       # geeft de naam van de tabel in de database waar de data naartoe wordt geschreven, in dit geval 'silver_sales'
        con=engine,                # geeft de SQLAlchemy engine door als verbinding voor het wegschrijven van de data naar de database
        if_exists="append",        # zorgt ervoor dat de data wordt toegevoegd aan de bestaande tabel 'silver_sales' ipv deze te overschrijven
        index=False                # zorgt ervoor dat de DataFrame index niet wordt weggeschreven als een aparte kolom in de database
    )

    print("Data toegevoegd aan silver_sales.")


# ---------------------------------------------------------------------------------------
# 8. Verwerkt bestand verplaatsen # functie die het verwerkte bestand verplaatst naar de 'verwerkt' map
# ---------------------------------------------------------------------------------------
def move_to_processed(path: Path):
    destination = PROCESSED_DIR / path.name     # bepaalt de bestemming van het bestand in de 'verwerkt' map, met dezelfde bestandsnaam
    shutil.move(str(path), destination)         # verplaatst het bestand van de bronze map naar de 'verwerkt' map
    print(f"Verplaatst naar: {destination}")


# ---------------------------------------------------------------------------------------
# 9. Main flow # hoofdfunctie dat alle bovenstaande stappen uitvoert
# ---------------------------------------------------------------------------------------
def main_flow():
    print("Zoeken naar nieuwe bronze CSV-bestanden...")

    files = get_bronze_files()              # haalt alle CSV-bestanden op uit de bronze map met def function get_bronze_files()

    if not files:
        print("Geen nieuwe bestanden gevonden.")
        return

    for file in files:
        df_raw = load_bronze_file(file)     # leest het CSV-bestand in als een DataFrame
        df_clean = clean_data(df_raw)       # maakt de data schoon en voegt de 'total_amount' kolom toe
        write_to_silver(df_clean)           # schrijft de opgeschoonde data weg naar de MySQL database
        move_to_processed(file)             # verplaatst het verwerkte bestand naar de 'verwerkt' map

    print("Alle nieuwe bestanden zijn verwerkt en verplaatst.")


# ---------------------------------------------------------------------------------------
# 10. Uitvoeren # zorgt ervoor dat de main_flow alleen wordt uitgevoerd als dit script direct wordt uitgevoerd, dus niet bij een import als module
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":
    main_flow()
