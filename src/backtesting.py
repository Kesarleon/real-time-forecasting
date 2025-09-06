import pandas as pd
import numpy as np

def run_sma_crossover_backtest(prices, short_window=40, long_window=100):
    """
    Runs a simple backtest on a Small Moving Average (SMA) crossover strategy.

    Returns a dictionary with KPIs and the signals DataFrame.
    """
    signals = pd.DataFrame(index=prices.index)
    signals['price'] = prices

    # Create short and long simple moving averages
    signals['short_mavg'] = prices.rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = prices.rolling(window=long_window, min_periods=1).mean()

    # Generate signal: 1 when short_mavg > long_mavg, 0 otherwise
    signals['signal'] = 0.0
    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0
    )

    # Generate trading orders (1 for buy, -1 for sell)
    signals['positions'] = signals['signal'].diff()

    # --- Calculate portfolio returns ---
    # Calculate daily returns of the asset
    daily_returns = prices.pct_change()

    # Calculate strategy returns
    # We hold the asset (returns = daily_returns) when signal is 1
    # We hold cash (returns = 0) when signal is 0
    # We shift the signal by 1 to ensure we use the signal from the previous day to calculate today's return
    strategy_returns = daily_returns * signals['signal'].shift(1)

    # --- Calculate KPIs ---
    # 1. Cumulative Returns
    cumulative_returns = (1 + strategy_returns).cumprod()

    # 2. Sharpe Ratio
    # Assume risk-free rate is 0
    # Annualize by multiplying by sqrt of trading days in a year (252)
    sharpe_ratio = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(252) if strategy_returns.std() != 0 else 0

    total_return = (cumulative_returns.iloc[-1] - 1) * 100 if not cumulative_returns.empty else 0

    return {
        'total_return_pct': total_return,
        'sharpe_ratio': sharpe_ratio,
        'cumulative_returns': cumulative_returns,
        'signals': signals
    }
