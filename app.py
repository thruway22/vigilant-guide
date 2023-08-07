import streamlit as st
import pandas as pd
import yfinance as yf
import utilities as utl

st.title('Test')

col1, col2 = st.columns([1,3])

interval = col1.select_slider('Interval', options=('Daily', 'Weekly'))
lookback = col2.slider('Lookback', min_value=1, max_value=52, value=20, step=1)

# Usage
tickers = utl.scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])
# st.write(tickers)
# df = utl.compute_svix_for_tickers(tickers)

st.dataframe(df)