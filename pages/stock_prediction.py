import streamlit as st
import pandas as pd

from pages.utils.model_train import *
from pages.utils.plotly_fig import *

st.set_page_config(
    page_title="Stock Prediction", page_icon="chart_with_downwards_trend", layout="wide"
)

st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input("Stock Ticker", "AAPL")
rmse = 0
st.subheader("Predicting next 30 days close price for " + ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)
differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write("**Model RMSE Score:**", rmse)

forecast = get_forecast(scaled_data, differencing_order)
forecast["Close"] = inverse_scaling(scaler, forecast["Close"])
st.write("### Forecast Data")

fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

if isinstance(rolling_price.columns, pd.MultiIndex):
    rolling_price.columns = rolling_price.columns.get_level_values(0)

rolling_price_close = rolling_price[["Close"]]
forecast_combined = pd.concat([rolling_price_close, forecast])

st.plotly_chart(
    moving_average_forecast(forecast_combined.iloc[150:]), use_container_width=True
)
