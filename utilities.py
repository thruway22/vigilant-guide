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
        info = yf.Ticker(ticker).info
        svix = (1 - (info['previousClose'] - info['fiftyTwoWeekLow']) / (info['fiftyTwoWeekHigh'] - info['fiftyTwoWeekLow'])) * 100
        data.append([ticker, info['longName'], svix])
        
    return pd.DataFrame(data, columns=['ticker', 'name', 'svix'])

