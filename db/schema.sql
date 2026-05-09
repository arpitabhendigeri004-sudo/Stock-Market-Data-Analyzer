CREATE TABLE IF NOT EXISTS stock_data (
    ticker TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adj_close REAL,
    volume INTEGER,
    PRIMARY KEY (ticker, date)
);
CREATE TABLE IF NOT EXISTS indicators (
    ticker TEXT,
    date TEXT,
    sma20 REAL,
    sma50 REAL,
    rsi REAL,
    macd REAL,
    macd_signal REAL,
    bollinger_upper REAL,
    bollinger_lower REAL,
    signal TEXT,
    PRIMARY KEY (ticker, date)
);