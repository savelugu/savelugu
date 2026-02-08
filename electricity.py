import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pmdarima as pm


# =====================================================
# SAFE FORECAST MODELS (NEVER CRASH)
# =====================================================

def naive_drift(series, steps):
    series = series.astype(float)
    drift = (series.iloc[-1] - series.iloc[0]) / max(len(series) - 1, 1)
    return np.array([series.iloc[-1] + drift * (i + 1) for i in range(steps)])

def ets_model(series, steps):
    series = series.astype(float)
    model = ExponentialSmoothing(series, trend="add", seasonal=None)
    fit = model.fit(optimized=True)
    return np.asarray(fit.forecast(steps))

def auto_arima_model(series, steps):
    series = series.astype(float)
    model = pm.auto_arima(
        series,
        seasonal=False,
        suppress_warnings=True,
        error_action="ignore"
    )
    return np.asarray(model.predict(n_periods=steps))


# =====================================================
# ROBUST BACKTESTING
# =====================================================

def backtest(series, model_fn, min_train=6):
    errors = []

    for i in range(min_train, len(series)):
        try:
            train = series.iloc[:i]
            test = series.iloc[i]

            forecast = model_fn(train, 1)
            if forecast is None or len(forecast) == 0:
                continue

            errors.append(abs(test - float(forecast[0])))
        except Exception:
            continue

    return np.mean(errors) if errors else np.inf


def select_best_model(series):
    models = {
        "Naive Drift": naive_drift,
        "ETS (Holt)": ets_model,
        "Auto ARIMA": auto_arima_model
    }

    scores = {}
    for name, fn in models.items():
        score = backtest(series, fn)
        scores[name] = score

    best_name = min(scores, key=scores.get)
    return best_name, models[best_name], scores


# =====================================================
# GUARANTEED FORECAST OUTPUT
# =====================================================

def generate_forecast(series, model_fn, steps):
    try:
        forecast = model_fn(series, steps)
        forecast = np.asarray(forecast, dtype=float)
    except Exception:
        forecast = naive_drift(series, steps)

    sigma = series.diff().dropna().std()
    sigma = 0 if np.isnan(sigma) else sigma

    lower = forecast - 1.96 * sigma
    upper = forecast + 1.96 * sigma

    return forecast, lower, upper


# =====================================================
# STREAMLIT APP
# =====================================================

def app():
    st.set_page_config(page_title="Electricity Indicators Dashboard", layout="wide", page_icon="⚡")
    st.title("⚡ Electricity Indicators Dashboard")

    # -----------------------------
    # DATA
    # -----------------------------
    years = list(range(2015, 2025))
    data = [
        ["Customers Connected", "Domestic", "Number", 1006, 1046, 950, 1000, 2003, 9543, 2084, 5559, 6319, 7079],
        ["Customers Connected", "Commercial", "Number", 4740, 5836, 6765, 7008, 9187, 1716, 9910, 7836, 8182, 8529],
        ["Customers Connected", "Total", "Number", 5746, 6882, 7715, 8008, 11190, 11259, 11994, 13395, 14501, 15608],
        ["Grid Access", "Total", "%", 57.3, 59, 61, 63.5, 64, 83.36, 85.1, 86.91, 91.74, 96.56],
        ["Grid Access", "Urban", "%", 42, 41.49, 45.8, 51.19, 51.51, 65.46, 65, 69.3, 73.68, 78.06],
        ["Grid Access", "Rural", "%", 15.3, 17.51, 15.2, 12.31, 12.49, 17.9, 20.1, 17.61, 18.06, 18.5],
    ]

    df = pd.DataFrame(data, columns=["Indicator", "Disaggregation", "Unit"] + years)
    df_long = df.melt(
        id_vars=["Indicator", "Disaggregation", "Unit"],
        var_name="Year",
        value_name="Value"
    )
    df_long["Year"] = df_long["Year"].astype(int)

    # -----------------------------
    # SIDEBAR
    # -----------------------------
    st.sidebar.header("Filters")
    indicator = st.sidebar.selectbox("Indicator", df_long["Indicator"].unique())
    disagg = st.sidebar.selectbox(
        "Disaggregation",
        df_long[df_long["Indicator"] == indicator]["Disaggregation"].unique()
    )

    df_sel = df_long[
        (df_long["Indicator"] == indicator) &
        (df_long["Disaggregation"] == disagg)
    ].dropna()

    # -----------------------------
    # TREND
    # -----------------------------
    st.subheader("Trend")
    st.plotly_chart(
        px.line(df_sel, x="Year", y="Value", markers=True),
        use_container_width=True
    )

    # -----------------------------
    # FORECAST
    # -----------------------------
    st.subheader("Forecast")

    if len(df_sel) >= 6:
        horizon = st.slider("Forecast years", 1, 5, 3)

        series = df_sel.sort_values("Year").set_index("Year")["Value"]

        best_name, best_fn, scores = select_best_model(series)

        st.success(f"Model used: {best_name}")
        st.json(scores)

        forecast, lower, upper = generate_forecast(series, best_fn, horizon)

        future_years = range(series.index.max() + 1, series.index.max() + horizon + 1)

        fig = px.line(title="Observed vs Forecast")
        fig.add_scatter(x=series.index, y=series.values, mode="lines+markers", name="Observed")
        fig.add_scatter(x=list(future_years), y=forecast, mode="lines+markers", name="Forecast")
        fig.add_scatter(x=list(future_years), y=lower, mode="lines", name="Lower CI", line=dict(dash="dot"))
        fig.add_scatter(x=list(future_years), y=upper, mode="lines", name="Upper CI", line=dict(dash="dot"))

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Not enough data for forecasting (minimum 6 years required).")

    st.caption("⚡ Electricity Indicators Dashboard | Stable Production Build")


if __name__ == "__main__":
    app()
