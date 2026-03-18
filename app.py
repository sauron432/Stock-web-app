import streamlit as st
st.set_page_config(
    page_title = "Trading App",
    page_icon="heavy_dollar_sign:",
    layout="wide" 
)

st.title("Trading Guide App :bar_chart:")

st.header("A platform to collect all information prior to investing")

st.markdown("## We provide following services.")

st.markdown("### :one: Stock Information")
st.write("Through this page, you can see all the information about stock.")
st.markdown("### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models.")
st.markdown("### :three: CAPM return")
st.write("Discover how the Capital Asset Pricing Model calculates the expected return of different stocks asset based on its risk and market performance")
st.markdown("### :four: CAPM Betaf")
st.write("Calculates Beta and Expected return for individual stock.")
