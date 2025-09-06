import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_advanced_chart(historical_data, forecast_data, backtest_signals, ticker):
    """
    Creates an advanced, interactive chart with price, forecast, moving averages, and trading signals.
    """
    fig = go.Figure()

    # 1. Add historical price
    fig.add_trace(
        go.Scatter(x=historical_data.index, y=historical_data, name='Precio Histórico', line=dict(color='#636EFA'))
    )

    # 2. Add forecast data
    last_date = historical_data.index[-1]
    forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=len(forecast_data))
    fig.add_trace(
        go.Scatter(x=forecast_index, y=forecast_data, name='Pronóstico (ARIMA)', line=dict(color='#FFA15A', dash='dash'))
    )

    # 3. Add moving averages from the backtest signals
    fig.add_trace(
        go.Scatter(x=backtest_signals.index, y=backtest_signals['short_mavg'], name='SMA Corta', line=dict(color='#00CC96', width=1.5), opacity=0.7)
    )
    fig.add_trace(
        go.Scatter(x=backtest_signals.index, y=backtest_signals['long_mavg'], name='SMA Larga', line=dict(color='#EF553B', width=1.5), opacity=0.7)
    )

    # 4. Add Buy/Sell signals
    buy_signals = backtest_signals[backtest_signals['positions'] == 1.0]
    sell_signals = backtest_signals[backtest_signals['positions'] == -1.0]

    fig.add_trace(
        go.Scatter(
            x=buy_signals.index, y=buy_signals['price'],
            name='Señal de Compra', mode='markers',
            marker=dict(symbol='triangle-up', color='#00CC96', size=10, line=dict(width=1, color='DarkSlateGrey'))
        )
    )
    fig.add_trace(
        go.Scatter(
            x=sell_signals.index, y=sell_signals['price'],
            name='Señal de Venta', mode='markers',
            marker=dict(symbol='triangle-down', color='#EF553B', size=10, line=dict(width=1, color='DarkSlateGrey'))
        )
    )

    # --- Update layout ---
    fig.update_layout(
        title=f'Análisis Técnico y Pronóstico para {ticker}',
        xaxis_title='Fecha',
        yaxis_title='Precio (USD)',
        legend_title='Leyenda',
        template='plotly_white',
        xaxis_rangeslider_visible=True # Add a rangeslider for better navigation
    )

    return fig
