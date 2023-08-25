import pandas as pd
import yfinance as yf
import streamlit as st
from autoscraper import AutoScraper
from datetime import datetime, timedelta


@st.cache_data(ttl='1d', show_spinner=False)
def scrape(url, wanted_list):
    '''Scrape tickers from the provided URL.'''

    scraper = AutoScraper()
    tickers = scraper.build(url, wanted_list)
    tickers = {ticker.strip() + '.SR' for ticker in tickers}

    return tickers


@st.cache_data(ttl='1d', show_spinner=False)
def download_data(tickers):
    '''Download historical stock data and additional stock information.'''

    start_date = compute_start_date_for_max_data()
    data_dict = {}
    last_date = None  # Initialize last_date

    for ticker in tickers:
        historical_data = yf.download(ticker, interval='1d', start=start_date.strftime('%Y-%m-%d'))
        # Update the last_date
        if not historical_data.empty:
            last_date = historical_data.index[-1].to_pydatetime()

        info = yf.Ticker(ticker).info
        ticker_data = {
            'longName': info.get('longName', None),
            'currentPrice': info.get('currentPrice', None),
            'marketCap': info.get('marketCap', None),
            'historical_data': historical_data}
        data_dict[ticker] = ticker_data

    return data_dict, last_date.date()

def compute_start_date_for_max_data():
    '''Compute the start date for downloading the maximum possible data.'''

    today = datetime.today()
    days_to_last_sunday = today.weekday() + 1
    start_date = today - timedelta(days=days_to_last_sunday + 51*7)  # 51 weeks + current week

    return start_date


def compute_metric_from_data(data_dict, interval, lookback):
    '''Compute the desired metric from the stock data.'''

    metrics = {}

    for ticker, ticker_data in data_dict.items():
        data = ticker_data['historical_data']
        # Handle weekly interval
        if interval == 'Weekly':
            data = data[data.index.weekday == 3][-lookback:]
            if data.empty:
                continue
        else:  # Handle daily interval
            calendar_days = lookback + 2 * (lookback // 5)
            data = data[-calendar_days:]

        latest_close = data['Close'].iloc[-1]
        lowest_low = data['Low'].min()
        highest_high = data['High'].max()
        metric = 1 - (latest_close - lowest_low) / (highest_high - lowest_low)
        metrics[ticker] = {
            'longName': ticker_data['longName'],
            'currentPrice': ticker_data['currentPrice'],
            'marketCap': ticker_data['marketCap'],
            'computed_metric': metric}

    return metrics


def create_dataframe(result, search='', threshold_val=0.0):
    '''Display the computed metrics in a Streamlit dataframe filtered by the SVIX threshold.'''
    
    df = pd.DataFrame(result).T
    df.index = df.index.str.replace('.SR', '')

    # Filter by SVIX threshold
    df = df[df['computed_metric'] >= threshold_val]

    mask = (df.index.str.contains(search, case=False)) | (df['longName'].str.contains(search, case=False, na=False))
    df = df[mask]
    df = df.sort_values(by='marketCap', ascending=False)
    df.drop(columns='marketCap', inplace=True)
    df.columns = ['Name', 'Price', 'SVIX']
    st.dataframe(df, use_container_width=True,
                 column_config={'SVIX': st.column_config.ProgressColumn(format='%.2f')})


st.title('Saudi Market StochasticVIX')

# Fetch and download data
with st.empty():
    with st.spinner('Fetching and downloading data. Please wait...'):
        tickers = scrape('https://www.argaam.com/en/company/companies-prices', ['2222'])
        data_dict, last_date = download_data(tickers)

# User input fields
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
interval = col1.selectbox('Interval', ['Daily', 'Weekly'], index=1)
lookback = col2.selectbox('Lookback', [14, 20, 52], index=1)
threshold = col3.selectbox('SVIX Threshold', [0.0, 0.60, 0.70, 0.80, 0.90], index=3)
search = col4.text_input('Search')

# Display the dataframe with computed metrics
create_dataframe(compute_metric_from_data(data_dict, interval, lookback), search, threshold)
if st.button('Prices updated on {last_date}. Click here to clear Cache and redownload fresh data',
    use_container_width=True):
        st.cache_data.clear()
# st.caption(f'Prices updated on {last_date}')
# with st.expander(f'Prices updated on {last_date}'):
#     if st.button('Clear Cache and Redownload Fresh Data', use_container_width=True):
#         st.cache_data.clear()