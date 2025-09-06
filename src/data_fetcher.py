import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    """
    Fetches historical stock data from Yahoo Finance.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        return None
    return data
