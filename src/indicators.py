import pandas as pd
import sqlite3

from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

DB_PATH = "db/market.db"


def calculate_indicators(df):

    print("Calculating Technical Indicators...")

    # =========================
    # MOVING AVERAGES
    # =========================

    df['sma20'] = SMAIndicator(
        close=df['close'],
        window=20
    ).sma_indicator()

    df['sma50'] = SMAIndicator(
        close=df['close'],
        window=50
    ).sma_indicator()

    # =========================
    # RSI
    # =========================

    df['rsi'] = RSIIndicator(
        close=df['close'],
        window=14
    ).rsi()

    # =========================
    # MACD
    # =========================

    macd = MACD(close=df['close'])

    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()

    # =========================
    # BOLLINGER BANDS
    # =========================

    bollinger = BollingerBands(
        close=df['close'],
        window=20
    )

    df['bollinger_upper'] = bollinger.bollinger_hband()
    df['bollinger_lower'] = bollinger.bollinger_lband()

    # =========================
    # BUY / SELL SIGNALS
    # =========================

    df['signal'] = "HOLD"

    df.loc[
        df['sma20'] > df['sma50'],
        'signal'
    ] = "BUY"

    df.loc[
        df['sma20'] < df['sma50'],
        'signal'
    ] = "SELL"

    print("Indicators calculated successfully.")

    return df


def save_indicators(df, ticker):

    connection = sqlite3.connect(DB_PATH)

    indicator_columns = [
        'date',
        'sma20',
        'sma50',
        'rsi',
        'macd',
        'macd_signal',
        'bollinger_upper',
        'bollinger_lower',
        'signal'
    ]

    indicator_df = df[indicator_columns].copy()

    indicator_df['ticker'] = ticker

    indicator_df.to_sql(
        "indicators",
        connection,
        if_exists="append",
        index=False
    )

    connection.close()

    print("Indicators saved to database.")