import pandas as pd
import numpy as np

def generate_dummy_stock_data(days=500):
    """
    Generates a DataFrame with dummy stock data that looks realistic.

    Args:
        days (int): The number of days of data to generate.

    Returns:
        pd.DataFrame: A DataFrame with Open, High, Low, Close, and Volume columns.
    """
    start_date = pd.to_datetime('today') - pd.DateOffset(days=days)
    date_range = pd.date_range(start=start_date, periods=days, freq='D')

    # Generate a random walk for the close price
    price_changes = 1 + np.random.randn(days) * 0.02
    close_price = 100 * price_changes.cumprod()

    # Create other columns based on the close price to make them look realistic
    high_price = close_price * (1 + np.random.uniform(0, 0.02, size=days))
    low_price = close_price * (1 - np.random.uniform(0, 0.02, size=days))

    # Ensure Open is somewhere between High and Low of the previous day
    open_price = (high_price + low_price) / 2 - np.random.uniform(-0.01, 0.01, size=days) * close_price
    open_price[0] = close_price[0] * (1 + np.random.uniform(-0.01, 0.01))

    # Ensure high is the max and low is the min of O, H, L, C
    open_close = np.vstack([open_price, close_price])
    high_price = np.maximum(high_price, open_close.max(axis=0))
    low_price = np.minimum(low_price, open_close.min(axis=0))

    volume = np.random.randint(1_000_000, 10_000_000, size=days)

    data = pd.DataFrame({
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Close': close_price,
        'Volume': volume
    }, index=date_range)

    data.index.name = 'Date'

    return data
