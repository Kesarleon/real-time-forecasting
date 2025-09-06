import streamlit as st
import pandas as pd
from src.data_fetcher import fetch_data
from src.modeling import get_arima_forecast, get_garch_volatility_forecast
from src.visualization import plot_advanced_chart
from src.backtesting import run_sma_crossover_backtest

st.set_page_config(layout="wide")
st.title('Panel de Análisis de Trading Algorítmico')

# --- Sidebar for Inputs ---
st.sidebar.header('Configuración de Parámetros')
ticker = st.sidebar.text_input('Ticker de la Acción', 'AAPL')

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

run_button = st.sidebar.button('Ejecutar Análisis')

# --- Main Panel for Outputs ---
if run_button and ticker:
    with st.spinner('Realizando análisis... Esto puede tardar un momento.'):
        try:
            # --- 1. Fetch Data ---
            start_date = '2020-01-01'
            end_date = pd.to_datetime('today').strftime('%Y-%m-%d')
            data = fetch_data(ticker, start_date, end_date)

            if data is None:
                st.error(f"No se encontraron datos para el ticker '{ticker}'. Por favor, verifica el símbolo.")
            else:
                df_close = data['Close']

                # --- 2. Run Models & Backtest ---
                arima_order = (p_arima, d_arima, q_arima)
                price_forecast = get_arima_forecast(df_close, order=arima_order, steps=forecast_steps)
                volatility_forecast = get_garch_volatility_forecast(df_close, p=p_garch, q=q_garch, steps=forecast_steps)
                backtest_results = run_sma_crossover_backtest(df_close, short_window, long_window)

                # --- 3. Display Results ---
                st.subheader(f'Resultados del Análisis para {ticker}')

                # Main Chart
                main_chart_fig = plot_advanced_chart(df_close, price_forecast, backtest_results['signals'], ticker)
                st.plotly_chart(main_chart_fig, use_container_width=True)

                # KPIs
                st.subheader('Resultados del Backtesting (Estrategia SMA Crossover)')
                kpi_col1, kpi_col2 = st.columns(2)
                kpi_col1.metric("Retorno Total de la Estrategia", f"{backtest_results['total_return_pct']:.2f}%")
                kpi_col2.metric("Ratio de Sharpe Anualizado", f"{backtest_results['sharpe_ratio']:.2f}")

                # Performance Chart
                st.write("Rendimiento de la Estrategia vs. Comprar y Mantener (Buy & Hold)")
                buy_hold_returns = (1 + df_close.pct_change()).cumprod()
                strategy_cumulative_returns = backtest_results['cumulative_returns']

                performance_df = pd.DataFrame({
                    'Estrategia': strategy_cumulative_returns,
                    'Buy & Hold': buy_hold_returns
                })
                st.line_chart(performance_df, use_container_width=True)

                # Data Tables
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
    st.info('Por favor, configure los parámetros en la barra lateral y haga clic en "Ejecutar Análisis".')
