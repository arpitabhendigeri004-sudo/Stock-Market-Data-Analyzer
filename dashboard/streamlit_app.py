import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
import feedparser
import pyttsx3
import seaborn as sns
import matplotlib.pyplot as plt

from textblob import TextBlob
from sklearn.linear_model import LinearRegression
from streamlit_autorefresh import st_autorefresh

from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

# ==========================================
# AUTO REFRESH
# ==========================================

st_autorefresh(
    interval=5000,
    key="stock_refresh"
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Stock Market Analyzer",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.stMetric {
    background-color: #161A23;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.title("📈 AI Powered Stock Market Analyzer")

st.markdown("""
### 🚀 Advanced FinTech Analytics Dashboard

Features:
- Live Market Analysis
- AI Market Insights
- Candlestick Charts
- Portfolio Simulation
- News Sentiment Analysis
- AI Price Prediction
- Portfolio Tracking
""")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Dashboard Configuration")

ticker = st.sidebar.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

compare_ticker = st.sidebar.text_input(
    "Compare With",
    "MSFT"
)

portfolio = st.sidebar.multiselect(
    "Portfolio Stocks",
    ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "NVDA"],
    default=["AAPL", "MSFT"]
)

start_date = st.sidebar.date_input(
    "Select Start Date",
    pd.to_datetime("2020-01-01")
)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data(stock_ticker, start):

    df = yf.download(
        stock_ticker,
        start=start
    )

    df.reset_index(inplace=True)

    cleaned_columns = []

    for col in df.columns:

        if isinstance(col, tuple):
            cleaned_columns.append(col[0].lower())

        else:
            cleaned_columns.append(col.lower())

    df.columns = cleaned_columns

    return df


df = load_data(ticker, start_date)

compare_df = load_data(compare_ticker, start_date)

# ==========================================
# TECHNICAL INDICATORS
# ==========================================

df['sma20'] = SMAIndicator(
    close=df['close'],
    window=20
).sma_indicator()

df['sma50'] = SMAIndicator(
    close=df['close'],
    window=50
).sma_indicator()

df['rsi'] = RSIIndicator(
    close=df['close'],
    window=14
).rsi()

macd = MACD(close=df['close'])

df['macd'] = macd.macd()

df['macd_signal'] = macd.macd_signal()

bollinger = BollingerBands(
    close=df['close'],
    window=20
)

df['bb_upper'] = bollinger.bollinger_hband()

df['bb_lower'] = bollinger.bollinger_lband()

# ==========================================
# KPI METRICS
# ==========================================

latest_price = round(df['close'].iloc[-1], 2)

highest_price = round(df['high'].max(), 2)

lowest_price = round(df['low'].min(), 2)

volatility = round(
    df['close'].pct_change().std() * 100,
    2
)

avg_return = round(
    df['close'].pct_change().mean() * 100,
    2
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Latest Price",
    f"${latest_price}"
)

col2.metric(
    "📈 Highest Price",
    f"${highest_price}"
)

col3.metric(
    "📉 Lowest Price",
    f"${lowest_price}"
)

col4.metric(
    "⚡ Volatility",
    f"{volatility}%"
)

col5.metric(
    "📊 Avg Return",
    f"{avg_return}%"
)

# ==========================================
# AI INSIGHTS
# ==========================================

st.subheader("🤖 AI Market Insights")

insights = []

if df['sma20'].iloc[-1] > df['sma50'].iloc[-1]:
    insights.append("📈 Bullish Trend Detected")
else:
    insights.append("📉 Bearish Trend Detected")

if df['rsi'].iloc[-1] > 70:
    insights.append("⚠️ Market is Overbought")

elif df['rsi'].iloc[-1] < 30:
    insights.append("🟢 Market is Oversold")

else:
    insights.append("✅ RSI in Normal Range")

if volatility > 3:
    insights.append("⚠️ High Volatility Detected")
else:
    insights.append("✅ Stable Volatility")

for insight in insights:
    st.success(insight)

# ==========================================
# VOICE ASSISTANT
# ==========================================

st.subheader("🎙️ AI Voice Assistant")

if st.button("🔊 Speak Market Insights"):

    engine = pyttsx3.init()

    speech = f"""
    Latest stock price is {latest_price} dollars.
    Volatility is {volatility} percent.
    """

    engine.say(speech)

    engine.runAndWait()

    st.success("Voice Insights Played")

# ==========================================
# CANDLESTICK CHART
# ==========================================

st.subheader("📈 Live Candlestick Chart")

candlestick_fig = go.Figure(
    data=[
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close']
        )
    ]
)

candlestick_fig.update_layout(
    height=600
)

st.plotly_chart(
    candlestick_fig,
    use_container_width=True
)

# ==========================================
# MOVING AVERAGES
# ==========================================

st.subheader("📊 Moving Averages")

ma_fig = go.Figure()

ma_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['close'],
        name="Close"
    )
)

ma_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['sma20'],
        name="SMA20"
    )
)

ma_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['sma50'],
        name="SMA50"
    )
)

st.plotly_chart(
    ma_fig,
    use_container_width=True
)

# ==========================================
# RSI CHART
# ==========================================

st.subheader("📈 RSI Indicator")

rsi_fig = go.Figure()

rsi_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['rsi'],
        name='RSI'
    )
)

rsi_fig.add_hline(y=70)

rsi_fig.add_hline(y=30)

st.plotly_chart(
    rsi_fig,
    use_container_width=True
)

# ==========================================
# MACD CHART
# ==========================================

st.subheader("📉 MACD Indicator")

macd_fig = go.Figure()

macd_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['macd'],
        name='MACD'
    )
)

macd_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['macd_signal'],
        name='Signal'
    )
)

st.plotly_chart(
    macd_fig,
    use_container_width=True
)

# ==========================================
# BOLLINGER BANDS
# ==========================================

st.subheader("📊 Bollinger Bands")

bb_fig = go.Figure()

bb_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['close'],
        name='Close'
    )
)

bb_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['bb_upper'],
        name='Upper Band'
    )
)

bb_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['bb_lower'],
        name='Lower Band'
    )
)

st.plotly_chart(
    bb_fig,
    use_container_width=True
)

# ==========================================
# STOCK COMPARISON
# ==========================================

st.subheader("📊 Stock Comparison")

comparison_fig = go.Figure()

comparison_fig.add_trace(
    go.Scatter(
        x=df['date'],
        y=df['close'],
        name=ticker
    )
)

comparison_fig.add_trace(
    go.Scatter(
        x=compare_df['date'],
        y=compare_df['close'],
        name=compare_ticker
    )
)

st.plotly_chart(
    comparison_fig,
    use_container_width=True
)

# ==========================================
# PORTFOLIO TRACKER
# ==========================================

st.subheader("💼 Portfolio Tracker")

portfolio_data = yf.download(
    portfolio,
    start=start_date
)['Close']

st.line_chart(portfolio_data)

# ==========================================
# INVESTMENT SIMULATOR
# ==========================================

st.subheader("💰 Investment Simulator")

investment = st.number_input(
    "Investment Amount ($)",
    value=1000
)

initial_price = df['close'].iloc[0]

current_price = df['close'].iloc[-1]

shares = investment / initial_price

current_value = shares * current_price

profit = current_value - investment

sim1, sim2 = st.columns(2)

sim1.metric(
    "Portfolio Value",
    f"${round(current_value, 2)}"
)

sim2.metric(
    "Profit / Loss",
    f"${round(profit, 2)}"
)

# ==========================================
# AI PRICE PREDICTION
# ==========================================

st.subheader("🤖 AI Price Prediction")

ml_df = df[['close']].dropna()

ml_df['days'] = np.arange(len(ml_df))

X = ml_df[['days']]

y = ml_df['close']

model = LinearRegression()

model.fit(X, y)

future_day = [[len(ml_df) + 30]]

prediction = model.predict(future_day)

st.metric(
    "Predicted Price (30 Days)",
    f"${round(prediction[0], 2)}"
)

# ==========================================
# NEWS SENTIMENT ANALYSIS
# ==========================================

st.subheader("📰 Live Market News")

feed = feedparser.parse(
    f"https://news.google.com/rss/search?q={ticker}+stock"
)

for entry in feed.entries[:5]:

    sentiment = TextBlob(
        entry.title
    ).sentiment.polarity

    if sentiment > 0:
        st.success(entry.title)

    elif sentiment < 0:
        st.error(entry.title)

    else:
        st.info(entry.title)

# ==========================================
# HEATMAP
# ==========================================

st.subheader("🔥 Correlation Heatmap")

numeric_df = df.select_dtypes(
    include=['float64', 'int64']
)

corr = numeric_df.corr()

fig, ax = plt.subplots(figsize=(10, 6))

sns.heatmap(
    corr,
    annot=True,
    cmap='coolwarm',
    ax=ax
)

st.pyplot(fig)

# ==========================================
# DATA PREVIEW
# ==========================================

st.subheader("📄 Dataset Preview")

st.dataframe(df.tail(20))

# ==========================================
# DOWNLOAD BUTTON
# ==========================================

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name=f"{ticker}_analysis.csv",
    mime='text/csv'
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
### 🚀 Advanced Features Included

✅ AI Insights  
✅ Voice Assistant  
✅ Candlestick Charts  
✅ AI Prediction  
✅ Portfolio Tracking  
✅ News Sentiment Analysis  
✅ Heatmap Analytics  
✅ CSV Export  
✅ Interactive Dashboard  

⚠️ Educational Use Only — Not Financial Advice
""")