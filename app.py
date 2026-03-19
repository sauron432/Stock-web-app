import streamlit as st

st.set_page_config(
    page_title="Trading App",
    page_icon="💲",
    layout="wide"
)

pg = st.navigation([
    st.Page("pages/home.py", title="Home"),
    st.Page("pages/stock_analysis.py", title="Stock Analysis"),
    st.Page("pages/stock_prediction.py", title="Stock Prediction"),
])

pg.run()