# scripts/ingest_data.py
import argparse
from src.data.ingestion import load_user_transactions, load_stock_prices
from src.data.preprocess import clean_transactions, clean_stock_prices
import pandas as pd

def main():
    # Ingest
    tx_df = load_user_transactions()
    stocks_df = load_stock_prices()

    # Clean
    tx_df = clean_transactions(tx_df)
    stocks_df = clean_stock_prices(stocks_df)

    # Example: Save to data/processed
    tx_df.to_csv("data/processed/user_transactions_clean.csv", index=False)
    stocks_df.to_csv("data/processed/stock_prices_clean.csv", index=False)

    print("Data ingested and cleaned, files saved to data/processed/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest and clean financial data.")
    # Optionally add arguments like --input-path, etc.
    args = parser.parse_args()
    main()
