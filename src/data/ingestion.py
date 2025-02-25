# src/data/ingestion.py
import pandas as pd
from pathlib import Path

def load_user_transactions(path: str = "data/raw/user_transactions.csv") -> pd.DataFrame:
    df = pd.read_csv(Path(path))
    return df

def load_stock_prices(path: str = "data/raw/stock_prices.csv") -> pd.DataFrame:
    df = pd.read_csv(Path(path))
    return df
