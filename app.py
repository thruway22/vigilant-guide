import streamlit as st
import utilities as utl

st.title('Test')

# Usage
df = utl.scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])
df.columns = ['ticker']

# df['name'] = df.apply(lambda x: yf.Ticker(x), axis=1)

st.dataframe(df)