import streamlit as st
import pandas as pd
import time
from src.dummy_data_generator import generate_dummy_stock_data
from src.modeling import get_arima_forecast, get_garch_volatility_forecast
from src.visualization import plot_advanced_chart
from src.backtesting import run_sma_crossover_backtest
from src.sentiment_analyzer import get_simulated_tweets

st.set_page_config(layout="wide")
st.title('Panel de Análisis de Trading Algorítmico (Modo Demo)')
st.warning("Esta es una versión de demostración que utiliza datos ficticios generados localmente.")

# --- Sidebar for Inputs ---
st.sidebar.header('Configuración de Parámetros')
ticker = st.sidebar.text_input('Ticker de la Acción', 'DEMO_STOCK', disabled=True)

# --- Live Update Controls ---
st.sidebar.subheader('Controles de Ejecución')
run_button = st.sidebar.button('Ejecutar Análisis / Generar Nuevos Datos')

st.sidebar.header('Parámetros de Análisis')
st.sidebar.subheader('Parámetros del Modelo ARIMA')
p_arima = st.sidebar.number_input('Orden p (Auto-Regresivo)', min_value=0, max_value=10, value=5)
d_arima = st.sidebar.number_input('Orden d (Diferenciación)', min_value=0, max_value=5, value=1)
q_arima = st.sidebar.number_input('Orden q (Media Móvil)', min_value=0, max_value=10, value=0)

st.sidebar.subheader('Parámetros del Modelo GARCH')
p_garch = st.sidebar.number_input('Orden p (GARCH)', min_value=1, max_value=5, value=1)
q_garch = st.sidebar.number_input('Orden q (ARCH)', min_value=1, max_value=5, value=1)

st.sidebar.subheader('Parámetros de Backtesting (SMA Crossover)')
short_window = st.sidebar.number_input('Ventana Corta (días)', min_value=5, max_value=100, value=40)
long_window = st.sidebar.number_input('Ventana Larga (días)', min_value=50, max_value=250, value=100)

forecast_steps = st.sidebar.number_input('Días a Pronosticar', min_value=5, max_value=90, value=30)

# --- Main Panel for Outputs ---
if run_button:
    with st.spinner('Generando datos ficticios y realizando análisis...'):
        try:
            # --- 1. Fetch Data ---
            data = generate_dummy_stock_data(days=730) # Generate 2 years of data

            df_close = data['Close']

            # --- 2. Run Models, Backtest & Sentiment Analysis ---
            arima_order = (p_arima, d_arima, q_arima)
            price_forecast = get_arima_forecast(df_close, order=arima_order, steps=forecast_steps)
            volatility_forecast = get_garch_volatility_forecast(df_close, p=p_garch, q=q_garch, steps=forecast_steps)
            backtest_results = run_sma_crossover_backtest(df_close, short_window, long_window)
            tweets = get_simulated_tweets(ticker)
            sentiment_df = pd.DataFrame(tweets)
            avg_sentiment = sentiment_df['polarity'].mean() if not sentiment_df.empty else 0

            # --- 3. Display Results ---
            st.subheader(f'Resultados del Análisis para {ticker}')

            main_chart_fig = plot_advanced_chart(df_close, price_forecast, backtest_results['signals'], ticker)
            st.plotly_chart(main_chart_fig, use_container_width=True)

            st.subheader('Indicadores Clave de Rendimiento y Sentimiento')
            kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
            kpi_col1.metric("Retorno Total (Estrategia)", f"{backtest_results['total_return_pct']:.2f}%")
            kpi_col2.metric("Ratio de Sharpe Anualizado", f"{backtest_results['sharpe_ratio']:.2f}")
            kpi_col3.metric("Sentimiento General (Twitter)", f"{avg_sentiment:.2f}", help="Polaridad promedio de -1 (Neg) a 1 (Pos)")

            perf_col, sent_col = st.columns(2)
            with perf_col:
                st.subheader('Rendimiento de la Estrategia vs. Buy & Hold')
                buy_hold_returns = (1 + df_close.pct_change()).cumprod()
                strategy_cumulative_returns = backtest_results['cumulative_returns']
                performance_df = pd.DataFrame({'Estrategia': strategy_cumulative_returns, 'Buy & Hold': buy_hold_returns})
                st.line_chart(performance_df, use_container_width=True)
            with sent_col:
                st.subheader('Análisis de Sentimiento (Simulado)')
                st.dataframe(sentiment_df)

            st.subheader('Datos de Pronóstico')
            data_col1, data_col2 = st.columns(2)
            with data_col1:
                st.write("Valores de precio pronosticados (ARIMA):")
                st.dataframe(price_forecast)
            with data_col2:
                st.write("Volatilidad diaria pronosticada (GARCH, %):")
                st.dataframe(volatility_forecast)

        except Exception as e:
            st.error(f"Ocurrió un error durante el análisis: {e}")
else:
    st.info('Haga clic en "Ejecutar Análisis" para generar nuevos datos de demostración y ver el panel.')
