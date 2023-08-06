import streamlit as st
import pandas as pd
import yfinance as yf
import utilities as utl

st.title('Test')

# Usage
tickers = utl.scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])
df = utl.compute_svix_for_tickers(tickers)

st.dataframe(df)