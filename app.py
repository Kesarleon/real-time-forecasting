import streamlit as st
import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

st.title('Pronóstico de Precios de Acciones en Tiempo Real')

# Input for stock ticker
ticker = st.text_input('Introduce el Ticker de la Acción (ej: AAPL, GOOG)', 'AAPL')

if ticker:
    try:
        # Download data
        data = yf.download(ticker, start='2020-01-01', end=pd.to_datetime('today').strftime('%Y-%m-%d'))
        if data.empty:
            st.error(f"No se encontraron datos para el ticker '{ticker}'. Por favor, verifica el símbolo.")
        else:
            st.subheader(f'Datos brutos para {ticker}')
            st.write(data.tail())

            # Forecasting
            st.subheader('Pronóstico con ARIMA')
            df_close = data['Close']

            # Fit ARIMA model
            # A simple ARIMA(5,1,0) model
            model = ARIMA(df_close, order=(5,1,0))
            model_fit = model.fit()

            # Forecast
            forecast = model_fit.forecast(steps=30)

            # Plotting
            st.subheader('Datos Pronosticados')
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df_close.index, df_close, label='Datos Históricos')
            # Create a correct index for the forecast
            last_date = df_close.index[-1]
            forecast_index = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30, freq='D')
            ax.plot(forecast_index, forecast, label='Pronóstico', color='red')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Precio de la Acción (USD)')
            ax.set_title(f'Pronóstico del Precio de la Acción para {ticker}')
            ax.legend()
            st.pyplot(fig)

            st.write("Valores pronosticados para los próximos 30 días:")
            st.write(forecast)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
