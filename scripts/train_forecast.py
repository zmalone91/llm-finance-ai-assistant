#!/usr/bin/env python3
"""Script to train time-series forecasting model (e.g., Prophet or ARIMA)."""

import argparse
from src.models.forecasting.train_forecast_model import train_forecast_model

def main(args):
    train_forecast_model()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train forecasting model.")
    # Add any arguments here, e.g.:
    # parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    args = parser.parse_args()
    main(args)
