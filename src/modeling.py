import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from arch import arch_model
import numpy as np

def get_arima_forecast(data, order=(5,1,0), steps=30):
    """
    Generates a forecast using an ARIMA model.
    """
    model = ARIMA(data, order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast

def get_garch_volatility_forecast(data_close, p=1, q=1, steps=30):
    """
    Generates a volatility forecast using a GARCH model.
    """
    # Calculate percentage returns
    returns = 100 * data_close.pct_change().dropna()

    # Fit GARCH model
    model = arch_model(returns, vol='Garch', p=p, q=q)
    model_fit = model.fit(disp='off')

    # Forecast volatility
    forecast = model_fit.forecast(horizon=steps)

    # Get the variance and convert to volatility (std dev)
    # The forecast object gives us the h.1, h.2, ... variances
    # We take the values and compute the square root to get the volatility
    forecasted_variance = forecast.variance.iloc[-1]
    forecasted_volatility = np.sqrt(forecasted_variance)

    return forecasted_volatility
