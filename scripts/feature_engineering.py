# scripts/feature_engineering.py
import pandas as pd
from src.data.ingestion import load_user_transactions, load_stock_prices
from src.data.preprocess import clean_transactions, clean_stock_prices
from src.features.feature_engineering import (
    create_user_features, create_stock_features, combine_user_stock_features
)

def main():
    # Load & clean data
    tx_df = load_user_transactions("data/processed/user_transactions_clean.csv")
    stocks_df = load_stock_prices("data/processed/stock_prices_clean.csv")

    # Create features
    user_feats = create_user_features(tx_df)
    stock_feats = create_stock_features(stocks_df)

    # Optionally combine user + stock data
    combined_df = combine_user_stock_features(user_feats, stock_feats)

    # Save
    user_feats.to_csv("data/processed/user_features.csv", index=False)
    stock_feats.to_csv("data/processed/stock_features.csv", index=False)
    combined_df.to_csv("data/processed/combined_features.csv", index=False)

    print("Feature engineering complete. Files saved to data/processed/.")

if __name__ == "__main__":
    main()
