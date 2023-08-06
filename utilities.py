import pandas as pd
import yfinance as yf
from autoscraper import AutoScraper

def scrape(url, wanted_list):
    """Scrape and retrieve tickers from the provided URL."""
    scraper = AutoScraper()
    tickers = scraper.build(url, wanted_list)
    tickers = {ticker.strip() + '.SR' for ticker in tickers}
    tickers = pd.DataFrame(tickers)
    return tickers

def svix(ticker, lookback, period, interval, buy_threshold):
    """Compute svix and buy signals for a given ticker."""
    ticker_data = yf.Ticker(ticker)
    df = ticker_data.history(period=period, interval=interval).ffill()[['High', 'Low', 'Close']]
    
    df['HHigh'] = df['High'].rolling(lookback).max()
    df['LLow'] = df['Low'].rolling(lookback).min()
    df['svix'] = (1 - (df['Close'] - df['LLow']) / (df['HHigh'] - df['LLow'])) * 100
    df['buy'] = (df['svix'] > buy_threshold).astype(int)
    df['bought'] = df['buy'] * df['Close']
    
    return df
