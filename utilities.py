import pandas as pd
import yfinance as yf
from autoscraper import AutoScraper

def scrape(url, wanted_list):
    """Scrape and retrieve tickers from the provided URL."""
    scraper = AutoScraper()
    tickers = scraper.build(url, wanted_list)
    tickers = {ticker.strip() + '.SR' for ticker in tickers}
    return tickers

# def svix2(tickers, lookback, period, interval, buy_threshold):
#     for ticker in tickers:
#         engine = yf.Ticker(ticker)
#         name = engine.info['longName']
#         df = engine.history(period=period, interval=interval).ffill()[['High', 'Low', 'Close']]
#         df = df.tail(lookback)
#         HHigh = df['High'].max()
#         LLow = df['Low'].min()
#         close = df['Close'].tail(1)
#         svix = (1 - (close - LLow) / (HHigh - LLow)) * 100

# def svix(ticker, lookback, period, interval, buy_threshold):
#     """Compute svix and buy signals for a given ticker."""
#     ticker_data = yf.Ticker(ticker)
#     df = ticker_data.history(period=period, interval=interval).ffill()[['High', 'Low', 'Close']]
    
#     df['HHigh'] = df['High'].rolling(lookback).max()
#     df['LLow'] = df['Low'].rolling(lookback).min()
#     df['svix'] = (1 - (df['Close'] - df['LLow']) / (df['HHigh'] - df['LLow'])) * 100
#     df['buy'] = (df['svix'] > buy_threshold).astype(int)
#     df['bought'] = df['buy'] * df['Close']
    
#     return df

def compute_svix_for_tickers(tickers):
    """Compute svix for a list of tickers."""
    data = []
    
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            svix = (1 - (info['previousClose'] - info['fiftyTwoWeekLow']) / (info['fiftyTwoWeekHigh'] - info['fiftyTwoWeekLow'])) * 100
            data.append([ticker, info['longName'], svix])
        except:
            pass
        
    return pd.DataFrame(data, columns=['ticker', 'name', 'svix'])



#########

import yfinance as yf
from datetime import datetime, timedelta

def compute_start_date(interval: str, lookback: int) -> datetime:
    today = datetime.today()
    
    if interval == "Daily":
        # Convert business days to calendar days (excluding Fridays and Saturdays)
        calendar_days = lookback + 2 * (lookback // 5)
        start_date = today - timedelta(days=calendar_days)
    elif interval == "Weekly":
        # Calculate how many days to go back to the previous Sunday
        days_to_last_sunday = today.weekday() + 1
        start_date = today - timedelta(days=days_to_last_sunday + (lookback-1)*7)
    else:
        raise ValueError("Invalid interval. Please choose 'Daily' or 'Weekly'.")
    
    return start_date

def get_metric(tickers, interval, lookback):
    start_date = compute_start_date(interval, lookback)
    
    metrics = {}
    
    for ticker in tickers:
        # Fetch the daily data
        data = yf.download(ticker, interval="1d", start=start_date.strftime('%Y-%m-%d'), progress=False)
        
        if interval == "Weekly":
            # Filter only the Thursdays' data
            data = data[data.index.weekday == 3]
        
        # Extract required data
        latest_close = data['Close'].iloc[-1]
        lowest_low = data['Low'].min()
        highest_high = data['High'].max()
        
        # Compute the metric
        metric = 1 - (latest_close - lowest_low) / (highest_high - lowest_low)
        metrics[ticker] = metric

    return metrics

