# src/data/preprocess.py
import pandas as pd

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    # Convert dateg
    df["date"] = pd.to_datetime(df["date"])
    # drop duplicates or fill missing categories
    df.drop_duplicates(inplace=True)
    return df

def clean_stock_prices(df: pd.DataFrame) -> pd.DataFrame:
    # Convert date
    df["date"] = pd.to_datetime(df["date"])
    # Ensure numeric columns are properly typed
    df["open"] = pd.to_numeric(df["open"], errors="coerce")
    return df
