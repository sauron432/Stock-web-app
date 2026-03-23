import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.plotly_fig import *

st.set_page_config(
    page_title='Stock Analysis',
    page_icon='📄',
    layout='wide'
)

@st.cache_data(ttl=300)
def get_stock_info(ticker):
    return yf.Ticker(ticker).info

@st.cache_data(ttl=300)
def get_stock_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

@st.cache_data(ttl=300)
def get_ticker_history(ticker):
    return yf.Ticker(ticker).history(period='max')

st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input('Stock ticker', 'TTWO')
with col2:
    start_date = st.date_input('Choose start date:', datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input('Choose end date:', datetime.date(today.year, today.month, today.day))

st.subheader(ticker)

try:
    info = get_stock_info(ticker)
except Exception as e:
    st.error(f"Unable to fetch data for {ticker}. Please try again in a moment.")
    st.stop()

st.write(info.get('longBusinessSummary', 'N/A'))
st.write("**Sector:**", info.get('sector', 'N/A'))
st.write("**Employees:**", info.get('fullTimeEmployees', 'N/A'))
st.write("**Website:**", info.get('website', 'N/A'))

# ── Metrics ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

trailing_pe = info.get("trailingPE")
if trailing_pe is None:
    eps = info.get("trailingEps")
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    trailing_pe = round(price / eps, 2) if eps and price else "N/A"

market_cap = info.get("marketCap")
if not market_cap:
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    shares = info.get("sharesOutstanding")
    market_cap = price * shares if price and shares else "N/A"

def format_market_cap(val):
    if isinstance(val, str):
        return val
    if val >= 1e12:
        return f"${val / 1e12:.2f}T"
    elif val >= 1e9:
        return f"${val / 1e9:.2f}B"
    elif val >= 1e6:
        return f"${val / 1e6:.2f}M"
    else:
        return f"${val:,.0f}"

with col1:
    df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
    df['Value'] = [
        format_market_cap(market_cap),
        info.get('beta'),
        info.get('trailingEps'),
        trailing_pe
    ]
    st.plotly_chart(plotly_table(df), use_container_width=True)

with col2:
    debt_to_equity = info.get('debtToEquity')
    if debt_to_equity is None:
        total_debt = info.get('totalDebt')
        equity = info.get('totalStockholderEquity') or info.get('bookValue')
        shares = info.get('sharesOutstanding')
        if total_debt and equity and shares:
            debt_to_equity = round(total_debt / (equity * shares), 2)

    return_on_equity = info.get('returnOnEquity')
    if return_on_equity is None:
        net_income = info.get('netIncomeToCommon')
        equity = info.get('totalStockholderEquity') or info.get('bookValue')
        shares = info.get('sharesOutstanding')
        if net_income and equity and shares:
            return_on_equity = round(net_income / (equity * shares), 2)

    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'])
    df['Value'] = [
        info.get('quickRatio'),
        info.get('revenuePerShare'),
        info.get('profitMargins'),
        debt_to_equity,
        return_on_equity
    ]
    st.plotly_chart(plotly_table(df), use_container_width=True)

try:
    data = get_stock_data(ticker, start_date, end_date)
except Exception as e:
    st.error(f"Unable to fetch historical data. Please try again in a moment.")
    st.stop()

col1, col2, col3 = st.columns(3)

latest_close = float(data['Close'].iloc[-1])
prev_close = float(data['Close'].iloc[-2])
daily_change = latest_close - prev_close

col1.metric("Daily change", f"${latest_close:.2f}", f"{daily_change:.2f}")

last_10 = data.tail(10).sort_index(ascending=False).round(3)
st.write('### Last 10 days data')
st.plotly_chart(plotly_table(last_10), use_container_width=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

num_period = '1y'
with col1:
    if st.button('5D'):
        num_period = '5d'
with col2:
    if st.button('1M'):
        num_period = '1mo'
with col3:
    if st.button('6M'):
        num_period = '6mo'
with col4:
    if st.button('1Y'):
        num_period = '1y'
with col5:
    if st.button('5Y'):
        num_period = '5y'
with col6:
    if st.button('MAX'):
        num_period = 'max'

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    chart_type = st.selectbox('', ('Candle', 'Line'))
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('', ('RSI', 'MACD'))
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))

try:
    data1 = get_ticker_history(ticker)
except Exception as e:
    st.error(f"Unable to fetch chart data. Please try again in a moment.")
    st.stop()

if chart_type == 'Candle' and indicators == "RSI":
    st.plotly_chart(candle_stick(data1, num_period), use_container_width=True)
    st.plotly_chart(RSI(data1, num_period), use_container_width=True)

elif chart_type == 'Candle' and indicators == "MACD":
    st.plotly_chart(candle_stick(data1, num_period), use_container_width=True)
    st.plotly_chart(MACD(data1, num_period), use_container_width=True)

elif chart_type == 'Line' and indicators == "RSI":
    st.plotly_chart(close_chart(data1, num_period), use_container_width=True)
    st.plotly_chart(RSI(data1, num_period), use_container_width=True)

elif chart_type == 'Line' and indicators == "MACD":
    st.plotly_chart(close_chart(data1, num_period), use_container_width=True)
    st.plotly_chart(MACD(data1, num_period), use_container_width=True)

elif chart_type == 'Line' and indicators == "Moving Average":
    st.plotly_chart(Moving_average(data1, num_period), use_container_width=True)