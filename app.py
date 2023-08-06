import streamlit as st
import pandas as pd
import yfinance as yf
import utilities as utl

st.title('Test')

# Usage
df = utl.scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])
df.columns = ['ticker']

df['name'] = df.apply(lambda x: yf.Ticker(x['ticker']).info['longName'], axis=1)

st.dataframe(df)