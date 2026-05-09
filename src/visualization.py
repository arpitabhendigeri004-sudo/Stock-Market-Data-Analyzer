import os
import matplotlib.pyplot as plt


def create_output_folder():

    os.makedirs("images/charts", exist_ok=True)


# ==========================================
# STOCK PRICE CHART
# ==========================================

def plot_stock_price(df, ticker):

    plt.figure(figsize=(14, 6))

    plt.plot(
        df['date'],
        df['close'],
        label='Closing Price'
    )

    plt.title(f'{ticker} Stock Closing Price')

    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.legend()

    plt.tight_layout()

    path = f"images/charts/{ticker}_closing_price.png"

    plt.savefig(path)

    plt.close()

    print(f"Saved: {path}")


# ==========================================
# MOVING AVERAGE CHART
# ==========================================

def plot_moving_averages(df, ticker):

    plt.figure(figsize=(14, 6))

    plt.plot(df['date'], df['close'], label='Close')

    plt.plot(df['date'], df['sma20'], label='SMA20')

    plt.plot(df['date'], df['sma50'], label='SMA50')

    plt.title(f'{ticker} Moving Averages')

    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.legend()

    plt.tight_layout()

    path = f"images/charts/{ticker}_moving_averages.png"

    plt.savefig(path)

    plt.close()

    print(f"Saved: {path}")


# ==========================================
# RSI CHART
# ==========================================

def plot_rsi(df, ticker):

    plt.figure(figsize=(14, 5))

    plt.plot(df['date'], df['rsi'], label='RSI')

    plt.axhline(70, linestyle='--')

    plt.axhline(30, linestyle='--')

    plt.title(f'{ticker} RSI Indicator')

    plt.xlabel("Date")
    plt.ylabel("RSI")

    plt.legend()

    plt.tight_layout()

    path = f"images/charts/{ticker}_rsi.png"

    plt.savefig(path)

    plt.close()

    print(f"Saved: {path}")


# ==========================================
# MACD CHART
# ==========================================

def plot_macd(df, ticker):

    plt.figure(figsize=(14, 5))

    plt.plot(df['date'], df['macd'], label='MACD')

    plt.plot(df['date'], df['macd_signal'], label='Signal')

    plt.title(f'{ticker} MACD Indicator')

    plt.xlabel("Date")
    plt.ylabel("MACD")

    plt.legend()

    plt.tight_layout()

    path = f"images/charts/{ticker}_macd.png"

    plt.savefig(path)

    plt.close()

    print(f"Saved: {path}")


# ==========================================
# BOLLINGER BANDS
# ==========================================

def plot_bollinger_bands(df, ticker):

    plt.figure(figsize=(14, 6))

    plt.plot(df['date'], df['close'], label='Close')

    plt.plot(df['date'], df['bollinger_upper'], label='Upper Band')

    plt.plot(df['date'], df['bollinger_lower'], label='Lower Band')

    plt.title(f'{ticker} Bollinger Bands')

    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.legend()

    plt.tight_layout()

    path = f"images/charts/{ticker}_bollinger_bands.png"

    plt.savefig(path)

    plt.close()

    print(f"Saved: {path}")


# ==========================================
# BUY SELL SIGNALS
# ==========================================

def plot_signals(df, ticker):

    plt.figure(figsize=(14, 6))

    plt.plot(df['date'], df['close'], label='Close Price')

    buy_signals = df[df['signal'] == 'BUY']

    sell_signals = df[df['signal'] == 'SELL']

    plt.scatter(
        buy_signals['date'],
        buy_signals['close'],
        marker='^',
        label='BUY'
    )

    plt.scatter(
        sell_signals['date'],
        sell_signals['close'],
        marker='v',
        label='SELL'
    )

    plt.title(f'{ticker} BUY/SELL Signals')

    plt.xlabel("Date")
    plt.ylabel("Price")

    plt.legend()

    plt.tight_layout()

    path = f"images/charts/{ticker}_signals.png"

    plt.savefig(path)

    plt.close()

    print(f"Saved: {path}")


# ==========================================
# GENERATE ALL CHARTS
# ==========================================

def generate_all_charts(df, ticker):

    create_output_folder()

    plot_stock_price(df, ticker)

    plot_moving_averages(df, ticker)

    plot_rsi(df, ticker)

    plot_macd(df, ticker)

    plot_bollinger_bands(df, ticker)

    plot_signals(df, ticker)

    print("All charts generated successfully.")