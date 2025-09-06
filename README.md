# Panel de Análisis Cuantitativo para Trading Algorítmico

Este es un panel de control avanzado construido con Streamlit para realizar análisis cuantitativos en activos financieros. La herramienta permite a los usuarios analizar tendencias de precios, predecir la volatilidad del mercado y realizar backtesting de estrategias de trading simples, todo a través de una interfaz interactiva.

![App Screenshot](assets/screenshot.png)
*(Nota: Se recomienda añadir una captura de pantalla de la aplicación aquí.)*

---

## Características Principales

- **Análisis de Series Temporales:** Utiliza el modelo **ARIMA** (Autoregressive Integrated Moving Average) para pronosticar los precios futuros de los activos.
- **Predicción de Volatilidad:** Implementa un modelo **GARCH** (Generalized Autoregressive Conditional Heteroskedasticity) para analizar y predecir la volatilidad, un factor clave en la gestión de riesgos.
- **Backtesting de Estrategias:** Incluye un motor de backtesting para evaluar el rendimiento histórico de una estrategia de trading basada en el **cruce de medias móviles (SMA Crossover)**.
- **Métricas de Rendimiento (KPIs):** Calcula y muestra métricas clave como el **Retorno Total** y el **Ratio de Sharpe Anualizado** para evaluar la efectividad de la estrategia.
- **Visualizaciones Interactivas:** Gráficos dinámicos construidos con **Plotly** que muestran precios históricos, pronósticos, medias móviles y señales de compra/venta en un solo lugar.
- **Interfaz Configurable:** Todos los parámetros de los modelos y del backtesting son completamente configurables a través de una barra lateral intuitiva.

---

## Metodología

### 1. Pronóstico de Precios (ARIMA)
El modelo ARIMA se utiliza para capturar patrones en los datos históricos de precios (tendencias, estacionalidad) y proyectarlos hacia el futuro. El modelo se define por tres parámetros `(p, d, q)` que el usuario puede ajustar para optimizar el pronóstico.

### 2. Pronóstico de Volatilidad (GARCH)
La volatilidad (el grado de variación de los precios) no es constante. El modelo GARCH se utiliza para modelar estos cambios en la volatilidad a lo largo del tiempo. Esto es fundamental para la gestión de riesgos y para entender las condiciones del mercado.

### 3. Estrategia de Backtesting (SMA Crossover)
Para evaluar una estrategia de trading, utilizamos el método de cruce de medias móviles:
- **Señal de Compra:** Se genera cuando la media móvil de corto plazo cruza por encima de la media móvil de largo plazo. Esto sugiere un impulso alcista.
- **Señal de Venta:** (En esta implementación, se vuelve a efectivo). Se genera cuando la media móvil corta cruza por debajo de la larga.
El rendimiento de esta estrategia se compara con una estrategia pasiva de "Comprar y Mantener" (Buy & Hold).

---

## Tech Stack

- **Python 3.10+**
- **Streamlit:** Para la interfaz web interactiva.
- **Pandas:** Para la manipulación de datos.
- **yfinance:** Para la obtención de datos financieros.
- **statsmodels:** Para el modelo ARIMA.
- **arch:** Para el modelo GARCH.
- **plotly:** Para las visualizaciones interactivas.
- **scikit-learn:** (Incluido para futuras ampliaciones).

---

## Cómo Ejecutar el Proyecto

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/Kesarleon/real-time-forecasting.git
    cd real-time-forecasting
    ```

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación de Streamlit:**
    ```bash
    streamlit run app.py
    ```

La aplicación se abrirá en tu navegador web.
