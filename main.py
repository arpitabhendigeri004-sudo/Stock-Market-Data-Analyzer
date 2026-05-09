from src.utils import create_database
from src.ingest import fetch_stock_data, save_to_database
from src.indicators import calculate_indicators, save_indicators
from src.visualization import generate_all_charts

# ==========================================
# CREATE DATABASE
# ==========================================

create_database()

# ==========================================
# FETCH STOCK DATA
# ==========================================

ticker = "AAPL"

df = fetch_stock_data(
    ticker=ticker,
    start="2020-01-01"
)

# ==========================================
# PROCESS DATA
# ==========================================

if df is not None:

    # Save Raw Data
    save_to_database(df, ticker)

    # Calculate Indicators
    df = calculate_indicators(df)

    # Save Indicators
    save_indicators(df, ticker)

    # Generate Charts
    generate_all_charts(df, ticker)

print("Stock Market Analytics System Completed 🚀")