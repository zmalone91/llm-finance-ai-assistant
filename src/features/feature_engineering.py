# src/features/feature_engineering.py

import pandas as pd
import numpy as np

def create_user_features(tx_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate feature-rich DataFrame from cleaned user transactions data.
    Example features:
      - Monthly net income & expenses
      - Expense category ratios
      - Rolling or cumulative metrics
    Returns a new DataFrame aggregated by date or month.
    """

    # 1. Ensure 'date' column is datetime
    tx_df["date"] = pd.to_datetime(tx_df["date"])

    # 2. (Optional) If you have multiple users, you'd group by 'user_id'
    # Here, we assume a single user.

    # 3. Create a "month" or "year-month" column for monthly aggregation
    tx_df["year_month"] = tx_df["date"].dt.to_period("M")

    # 4. Net daily or monthly amounts
    #    We'll do a monthly aggregation for net flow, also sum up incomes and expenses separately
    monthly_agg = tx_df.groupby("year_month").agg(
        total_income=("amount", lambda x: x[x > 0].sum()),
        total_expenses=("amount", lambda x: x[x < 0].sum()),
        net_flow=("amount", "sum"),
        transaction_count=("transaction_id", "count"),
    ).reset_index()

    # Convert total_expenses to positive values (if you want them as absolute)
    monthly_agg["total_expenses"] = monthly_agg["total_expenses"].abs()

    # 5. Expense category breakdown (e.g., fraction of monthly spending on groceries, housing, etc.)
    #    We'll pivot by category for amounts < 0 (expenses only).
    expense_mask = tx_df["amount"] < 0
    tx_expenses_only = tx_df[expense_mask].copy()
    tx_expenses_only["amount"] = tx_expenses_only["amount"].abs()  # make amounts positive

    monthly_cat = (
        tx_expenses_only.groupby(["year_month", "category"], as_index=False)["amount"]
        .sum()
        .pivot(index="year_month", columns="category", values="amount")
        .fillna(0)
    )

    # Merge the pivoted categories back to monthly_agg
    monthly_features = monthly_agg.merge(
        monthly_cat, on="year_month", how="left"
    )

    # 6. Calculate expense ratios per category
    category_cols = list(monthly_cat.columns)
    # total_expenses is already in monthly_agg, so after merge we name it monthly_features["total_expenses"]
    for cat in category_cols:
        ratio_col = f"{cat.lower()}_ratio"
        monthly_features[ratio_col] = (
            monthly_features[cat] / monthly_features["total_expenses"]
        ).fillna(0)

    # 7. Rolling or lag features (e.g., net_flow in previous month, 3-month average net_flow, etc.)
    monthly_features = monthly_features.sort_values("year_month")
    monthly_features["net_flow_lag1"] = monthly_features["net_flow"].shift(1)
    monthly_features["net_flow_3ma"] = (
        monthly_features["net_flow"].rolling(window=3).mean()
    )

    # 8. Reset or convert year_month to a timestamp (if needed)
    monthly_features["year_month"] = monthly_features["year_month"].astype(str)

    return monthly_features


def create_stock_features(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create time-series features for daily stock prices:
      - Daily returns, log returns
      - Rolling averages / rolling std
      - Example technical indicators (e.g., RSI, simple moving average crossovers)
    Returns a new DataFrame with feature columns.
    """

    # 1. Ensure date is datetime
    prices_df["date"] = pd.to_datetime(prices_df["date"])

    # 2. Sort data by symbol, then date
    prices_df = prices_df.sort_values(["symbol", "date"]).reset_index(drop=True)

    # 3. Daily returns
    #    We can use close price for returns, or an average of (open+close)/2
    prices_df["daily_return"] = prices_df.groupby("symbol")["close"].pct_change()

    # 4. Log returns (sometimes more stable for modeling)
    prices_df["log_return"] = np.log(prices_df["close"]) - np.log(prices_df["close"].shift(1))

    # 5. Rolling statistics (e.g., 5-day moving average of close, 14-day rolling std)
    prices_df["roll_mean_5"] = prices_df.groupby("symbol")["close"].transform(
        lambda x: x.rolling(5).mean()
    )
    prices_df["roll_std_5"] = prices_df.groupby("symbol")["close"].transform(
        lambda x: x.rolling(5).std()
    )

    # 6. Example: RSI, MACD, or other technical indicators
    #    We'll do a small RSI example (14-day period).
    #    RSI formula typically involves average gains/losses over a window.
    #    This is a quick demo, not a perfect implementation.
    window = 14
    delta = prices_df.groupby("symbol")["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.groupby(prices_df["symbol"]).transform(
        lambda x: x.rolling(window).mean()
    )
    avg_loss = loss.groupby(prices_df["symbol"]).transform(
        lambda x: x.rolling(window).mean()
    )
    rs = avg_gain / (avg_loss + 1e-9)
    prices_df["rsi_14"] = 100 - (100 / (1 + rs))

    # 7. Drop rows with NaN from the rolling calculations if you want a clean dataset
    #    or keep them and handle them in modeling
    # prices_df.dropna(inplace=True)

    return prices_df


def combine_user_stock_features(
    user_features: pd.DataFrame, stock_features: pd.DataFrame
) -> pd.DataFrame:
    """
    Optionally combine user finance data with market data.
    Example approach:
      - If you want to merge monthly user stats with monthly or daily stock data,
        you might align by date or by year_month.
      - This is highly project-specific.
    """

    # For demonstration, let’s assume we want to merge on year_month = date's YYYY-MM.
    # 1. Create 'year_month' in the stock df by taking the month-year from 'date'
    stock_features["year_month"] = stock_features["date"].dt.to_period("M").astype(str)

    # 2. Possibly aggregate stock features by 'year_month' if you want monthly-level stats
    #    Example: average daily returns for that month
    monthly_stock = (
        stock_features.groupby(["symbol", "year_month"], as_index=False)
        .agg(
            avg_daily_return=("daily_return", "mean"),
            avg_log_return=("log_return", "mean"),
            avg_rsi_14=("rsi_14", "mean")
            # etc.
        )
    )

    # 3. Merge with user_features (if you want a single symbol, pick it, or do a pivot)
    #    We'll just show how to merge for a single symbol, e.g., "SPY" as a market benchmark
    spy_monthly = monthly_stock[monthly_stock["symbol"] == "SPY"].copy()
    spy_monthly.drop("symbol", axis=1, inplace=True)

    combined_df = user_features.merge(spy_monthly, on="year_month", how="left")

    return combined_df
