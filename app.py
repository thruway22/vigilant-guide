import pandas as pd
import yfinance as yf
import streamlit as st
from autoscraper import AutoScraper
from datetime import datetime, timedelta

@st.cache_data(show_spinner=False)
def scrape(url, wanted_list):
    scraper = AutoScraper()
    tickers = scraper.build(url, wanted_list)
    tickers = {ticker.strip() + '.SR' for ticker in tickers}
    return tickers

@st.cache_data(show_spinner=False)
def download_data(tickers):
    start_date = compute_start_date_for_max_data()
    data_dict = {}
    for ticker in tickers:
        historical_data = yf.download(ticker, interval="1d", start=start_date.strftime('%Y-%m-%d'))
        info = yf.Ticker(ticker).info
        ticker_data = {
            "longName": info.get("longName", None),
            "currentPrice": info.get("currentPrice", None),
            "marketCap": info.get("marketCap", None),
            "historical_data": historical_data}
        data_dict[ticker] = ticker_data
    return data_dict

def compute_start_date_for_max_data() -> datetime:
    today = datetime.today()
    days_to_last_sunday = today.weekday() + 1
    start_date = today - timedelta(days=days_to_last_sunday + 51*7)  # 51 weeks + current week
    return start_date

def compute_metric_from_data(data_dict, interval, lookback):
    metrics = {}
    for ticker, ticker_data in data_dict.items():
        data = ticker_data["historical_data"]
        if interval == "Weekly":
            data = data[data.index.weekday == 3][-lookback:]
            if data.empty:
                continue
        else:
            calendar_days = lookback + 2 * (lookback // 5)
            data = data[-calendar_days:]
        latest_close = data['Close'].iloc[-1]
        lowest_low = data['Low'].min()
        highest_high = data['High'].max()
        metric = 1 - (latest_close - lowest_low) / (highest_high - lowest_low)
        metrics[ticker] = {
            "longName": ticker_data["longName"],
            "currentPrice": ticker_data["currentPrice"],
            "marketCap": ticker_data["marketCap"],
            "computed_metric": metric}
    return metrics

# def create_dataframe(result, ticker=None):
#     df = pd.DataFrame(result).T.sort_values('marketCap', ascending=False)
#     df.index = df.index.str.replace('.SR', '')
#     df.columns = ['Company', 'Price', 'Market Cap', 'SVIX']

#     st.dataframe(df, use_container_width=True, column_config={
#         "SVIX": st.column_config.ProgressColumn(),
#     },)

def create_dataframe(result, sortby, search=""):
    df = pd.DataFrame(result).T

    df.index = df.index.str.replace('.SR', '')
    df.columns = ['Company', 'Price', 'Market Cap', 'SVIX']

    # Filter based on search input
    mask = (df.index.str.contains(search, case=False)) | (df['Company'].str.contains(search, case=False, na=False))
    df = df[mask]

    # Sort the dataframe
    df = df.sort_values(by=sortby, ascending=False)

    # Drop the Market Cap column
    df.drop(columns='Market Cap', inplace=True)

    
    

    st.dataframe(df, use_container_width=True, column_config={
        "SVIX": st.column_config.ProgressColumn(),
    },)


######################


st.title('Saudi Market StochasticVIX')

with st.empty():
    with st.spinner("Fetching and downloading data. Please wait..."):
        tickers = scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])
        data_dict = download_data(tickers)

col1, col2, col3, col4 = st.columns(4)
interval = col1.selectbox('Interval', ['Daily', 'Weekly'])
lookback = col2.selectbox('Lookback', [14, 20, 52], index=1)
sortby = col3.selectbox('Sort by', ['Market Cap', 'SVIX'])
search = col4.text_input('Search')

# result = compute_metric_from_data(data_dict, interval, lookback)
# create_dataframe(result)

result = compute_metric_from_data(data_dict, interval, lookback)
create_dataframe(result, sortby, search)

