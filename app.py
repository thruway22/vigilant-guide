import streamlit as st
import utilities as utl

st.title('Test')

# Usage
tickers = utl.scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])

st.dataframe(tickers)