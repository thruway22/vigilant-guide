import streamlit as st
import pandas as pd
import yfinance as yf
import utilities as utl

st.title('Test')

interval = st.select_slider('Interval', options=('Daily', 'Weekly'))
lookback = st.slider('Lookback', min_value=1, max_value=52, value=20, step=1)

# Usage
tickers = utl.scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])
# st.write(tickers)
# df = utl.compute_svix_for_tickers(tickers)

st.dataframe(df)