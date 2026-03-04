# flake8: noqa

import sys
from pathlib import Path
import pandas as pd
from datetime import date
# sys.path aanpassen NA alle imports, maar vóór je eigen imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from python.bronze_to_silver import clean_data


def test_clean_data_removes_invalid_rows():  # testfunctie die controleert of clean_data functie correct werkt
    df = pd.DataFrame({                      # maakt een test DataFrame
        "CustomerID": [12345, None],
        "Invoice": ["A001", "A002"],
        "StockCode": ["10001", "10002"],
        "InvoiceDate": ["1-12-2009 07:45:00", "1-12-2009 07:45:00"],
        "Quantity": [1, 2],
        "Price": ["2,50", "3,00"]
    })

    cleaned = clean_data(df)

    # assert - controleert of er nog maar één rij over is na het opschonen van de data, en of die rij de juiste CustomerID heeft
    assert len(cleaned) == 1                                    # controleert of er nog maar één rij over is na het opschonen van de data
    assert cleaned.iloc[0]["CustomerID"] == 12345               # controleert of de overgebleven rij de juiste CustomerID heeft, namelijk 12345
    assert cleaned.iloc[0]["Price"] == 2.50                     # controleert of de prijs correct is omgezet en dat de komma is vervangen door een punt
    assert cleaned.iloc[0]["InvoiceDate"] == date(2009, 12, 1)  # controleert of de InvoiceDate correct is omgezet naar datetime en dat alleen de datum overblijft
