import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

DB_PATH = "db/market.db"


def fetch_stock_data(ticker="AAPL", start="2020-01-01", end=None):

    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    print(f"Fetching data for {ticker}...")

    # Download stock data
    df = yf.download(ticker, start=start, end=end)

    # Check if empty
    if df.empty:
        print("No data found.")
        return None

    # Reset index
    df.reset_index(inplace=True)

    # Handle multi-index columns safely
    cleaned_columns = []

    for col in df.columns:

        # If column is tuple
        if isinstance(col, tuple):
            cleaned_columns.append(col[0].lower().replace(" ", "_"))

        else:
            cleaned_columns.append(col.lower().replace(" ", "_"))

    df.columns = cleaned_columns

    print("Columns Found:")
    print(df.columns)

    # Rename adjusted close column if needed
    if "adj_close" not in df.columns:

        if "adj close" in df.columns:
            df.rename(columns={"adj close": "adj_close"}, inplace=True)

        elif "close" in df.columns:
            df["adj_close"] = df["close"]

    # Save CSV
    csv_path = f"data/{ticker}_stock_data.csv"

    df.to_csv(csv_path, index=False)

    print(f"CSV saved at: {csv_path}")

    return df


def save_to_database(df, ticker):

    connection = sqlite3.connect(DB_PATH)

    # Add ticker column
    df["ticker"] = ticker

    required_columns = [
        "ticker",
        "date",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume"
    ]

    # Keep only required columns
    df = df[required_columns]

    # Save to SQLite
    df.to_sql(
        "stock_data",
        connection,
        if_exists="append",
        index=False
    )

    connection.close()

    print("Data stored in SQLite database.")