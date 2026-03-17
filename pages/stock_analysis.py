import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
# import ta 

st.set_page_config(
    page_title='Stock Analysis',
    page_icon='page_with_curl',
    layout='wide'
)

st.title("Stock analysis")

col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input('Stock ticker','FUSE')
with col2:
    start_date = st.date_input('Choose start date:',datetime.date(today.year-1, today.month, today.day))
with col3:
    end_date = st.date_input('Choose end date:',datetime.date(today.year, today.month, today.day))

st.subheader(ticker)

stock = yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write("**Sector:**",stock.info['sector'])
st.write("**Employees:**",stock.info['fullTimeEmployees'])
st.write("**Website:**",stock.info['website'])

col1, col2 = st.columns(2)

trailing_pe = stock.info.get("trailingPE")
if trailing_pe is None:
    eps = stock.info.get("trailingEps")
    price = stock.info.get("currentPrice") or stock.info.get("regularMarketPrice")
    trailing_pe = round(price / eps, 2) if eps and price else "N/A"

market_cap = stock.info.get("marketCap")
if not market_cap:
    price = stock.info.get("currentPrice") or stock.info.get("regularMarketPrice")
    shares = stock.info.get("sharesOutstanding")
    market_cap = price * shares if price and shares else "N/A"

# Then format it properly
def format_market_cap(val):
    if isinstance(val, str):
        return val  # "N/A"
    if val >= 1e12:
        return f"${val / 1e12:.2f}T"
    elif val >= 1e9:
        return f"${val / 1e9:.2f}B"
    elif val >= 1e6:
        return f"${val / 1e6:.2f}M"
    else:
        return f"${val:,.0f}"


with col1:
    df = pd.DataFrame(index=['Market Cap','Beta','EPS','PE Ratio'])
    df['Value'] = [
        format_market_cap(market_cap),
        stock.info['beta'],
        stock.info.get('trailingEps'),
        trailing_pe]
    st.table(df)

with col2:
    # Debt to Equity fallback
    debt_to_equity = stock.info.get('debtToEquity')
    if debt_to_equity is None:
        total_debt = stock.info.get('totalDebt')
        equity = stock.info.get('totalStockholderEquity') or stock.info.get('bookValue')
        shares = stock.info.get('sharesOutstanding')
        if total_debt and equity and shares:
            debt_to_equity = round(total_debt / (equity * shares), 2)

    # Return on Equity fallback
    return_on_equity = stock.info.get('returnOnEquity')
    if return_on_equity is None:
        net_income = stock.info.get('netIncomeToCommon')
        equity = stock.info.get('totalStockholderEquity') or stock.info.get('bookValue')
        shares = stock.info.get('sharesOutstanding')
        if net_income and equity and shares:
            return_on_equity = round(net_income / (equity * shares), 2)

    df = pd.DataFrame(index=['Quick Ratio', 'Revenue per share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'])
    df['Value'] = [
        stock.info.get('quickRatio'),
        stock.info.get('revenuePerShare'),
        stock.info.get('profitMargins'),
        debt_to_equity,
        return_on_equity
    ]
    st.table(df)

data = yf.download(ticker, start=start_date, end=end_date)

col1, col2, col3 = st.columns(3)

latest_close = float(data['Close'].iloc[-1])
prev_close = float(data['Close'].iloc[-2])
daily_change = latest_close - prev_close

col1.metric("Daily change", f"${latest_close:.2f}", f"{daily_change:.2f}")
last_10 = data.tail(10).sort_index(ascending = False).round(3)
st.write('### Last 10 days data')
st.table(last_10)