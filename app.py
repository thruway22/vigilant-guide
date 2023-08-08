import streamlit as st
import pandas as pd
import yfinance as yf
import utilities as utl

st.title('Test')

col1, col2 = st.columns([1,3])
interval = col1.selectbox('Interval', ['Daily', 'Weekly'])
lookback = col2.slider('Lookback', min_value=1, max_value=52, value=20, step=1)

# # Sample usage:

# # Download the maximum possible data once
# tickers = ["2222.SR", "4002.SR"]  # Replace with your Saudi tickers
# data_dict = download_data(tickers)

# # Compute the metric based on user input
# interval = "Weekly"  # Example interval
# lookback = 10  # Example lookback
# result = compute_metric_from_data(data_dict, interval, lookback)
# print(result)

tickers = utl.scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])
data_dict = utl.download_data(tickers)

result = utl.compute_metric_from_data(data_dict, interval, lookback)
st.dataframe(result.T)