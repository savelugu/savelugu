forecast customers connected, and grid access: import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pmdarima as pm


# =====================================================
# PRODUCTION FORECASTING HELPERS
# =====================================================

def naive_drift(series, steps):
    drift = (series.iloc[-1] - series.iloc[0]) / (len(series) - 1)
    return np.array([
        series.iloc[-1] + drift * (i + 1)
        for i in range(steps)
    ])


def ets_model(series, steps):
    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal=None
    ).fit()
    return model.forecast(steps)


def auto_arima_model(series, steps):
    model = pm.auto_arima(
        series,
        seasonal=False,
        stepwise=True,
        suppress_warnings=True,
        error_action="ignore"
    )
    return model.predict(n_periods=steps)


def backtest(series, model_fn, min_train=6):
    errors = []

    for i in range(min_train, len(series)):
        train = series[:i]
        test = series[i:i + 1]

        forecast = model_fn(train, 1)
        errors.append(abs(test.values[0] - forecast[0]))

    return np.mean(errors)


def select_best_model(series):
    models = {
        "Naive Drift": naive_drift,
        "ETS (Holt)": ets_model,
        "Auto ARIMA": auto_arima_model
    }

    scores = {}
    for name, fn in models.items():
        scores[name] = backtest(series, fn)

    best_name = min(scores, key=scores.get)
    return best_name, models[best_name], scores


def generate_forecast(series, model_fn, steps):
    forecast = model_fn(series, steps)

    # Empirical CI (robust for small samples)
    sigma = series.diff().dropna().std()
    lower = forecast - 1.96 * sigma
    upper = forecast + 1.96 * sigma

    return forecast, lower, upper


# =====================================================
# STREAMLIT APP
# =====================================================

def app():
    # -----------------------------
    # Page config
    # -----------------------------
    st.set_page_config(
        page_title="Electricity Indicators Dashboard",
        layout="wide",
        page_icon="⚡"
    )

    st.title("⚡ Electricity Indicators Dashboard")
    st.markdown(
        "Production dashboard for electricity access, consumption, "
        "and customer indicators (2015–2024)."
    )

    # -----------------------------
    # Data preparation
    # -----------------------------
    years = list(range(2015, 2025))

    data = [
        ["Customers Connected", "Domestic (Residential)", "Number",
         1006, 1046, 950, 1000, 2003, 9543, 2084, 5559, 6319, 7079],

        ["Customers Connected", "Commercial (Non-residential)", "Number",
         4740, 5836, 6765, 7008, 9187, 1716, 9910, 7836, 8182, 8529],

        ["Customers Connected", "Total Customer Population", "Number",
         5746, 6882, 7715, 8008, 11190, 11259, 11994, 13395, 14501, 15608],

        ["Electricity Consumption", "Consumption", "MWh",
         5459.54, 5607.93, None, None, None, None,
         8681.08, 9205.47, 9767.46, 10329.45],

        ["Grid Access", "Total", "% (0-100)",
         57.30, 59.00, 61.00, 63.50, 64.00,
         83.36, 85.10, 86.91, 91.74, 96.56],

        ["Grid Access", "Urban", "% (0-100)",
         42.00, 41.49, 45.80, 51.19, 51.51,
         65.46, 65.00, 69.30, 73.68, 78.06],

        ["Grid Access", "Rural", "% (0-100)",
         15.30, 17.51, 15.20, 12.31, 12.49,
         17.90, 20.10, 17.61, 18.06, 18.50],
    ]

    columns = ["Indicator", "Disaggregation", "Unit"] + years
    df = pd.DataFrame(data, columns=columns)

    df_long = df.melt(
        id_vars=["Indicator", "Disaggregation", "Unit"],
        var_name="Year",
        value_name="Value"
    )

    df_long["Year"] = df_long["Year"].astype(int)

    # -----------------------------
    # Sidebar filters
    # -----------------------------
    st.sidebar.header("🔎 Filters")

    indicator = st.sidebar.selectbox(
        "Select Indicator",
        df_long["Indicator"].unique()
    )

    disaggregation = st.sidebar.multiselect(
        "Select Disaggregation",
        df_long[df_long["Indicator"] == indicator]["Disaggregation"].unique(),
        default=list(
            df_long[df_long["Indicator"] == indicator]["Disaggregation"].unique()
        )
    )

    filtered_df = df_long[
        (df_long["Indicator"] == indicator) &
        (df_long["Disaggregation"].isin(disaggregation))
    ]

    # -----------------------------
    # KPI metrics
    # -----------------------------
    st.subheader("📊 Key Metrics")

    latest_year = filtered_df["Year"].max()
    latest_data = filtered_df[filtered_df["Year"] == latest_year]

    cols = st.columns(len(latest_data))
    for col, (_, row) in zip(cols, latest_data.iterrows()):
        value = row["Value"]
        if row["Unit"] == "Number":
            value = f"{int(value):,}"
        col.metric(row["Disaggregation"], value)

    # -----------------------------
    # Trend chart
    # -----------------------------
    st.subheader("📈 Trend Over Time")

    fig = px.line(
        filtered_df,
        x="Year",
        y="Value",
        color="Disaggregation",
        markers=True,
        labels={"Value": filtered_df["Unit"].iloc[0]}
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # PRODUCTION FORECAST
    # -----------------------------
    st.subheader("🏭 Production Forecast")

    enable_forecast = st.checkbox("Enable forecast")

    if enable_forecast:
        horizon = st.slider("Forecast horizon (years)", 1, 5, 3)

        forecast_df = filtered_df.dropna()

        if forecast_df["Disaggregation"].nunique() != 1:
            st.warning("Select exactly ONE disaggregation for forecasting.")
        else:
            series = (
                forecast_df
                .sort_values("Year")
                .set_index("Year")["Value"]
            )

            if len(series) < 6:
                st.error("Not enough data for production forecasting.")
            else:
                best_name, best_fn, scores = select_best_model(series)

                st.success(f"Selected model: **{best_name}**")
                st.markdown("### Backtest MAE (lower is better)")
                st.json(scores)

                forecast, lower, upper = generate_forecast(
                    series, best_fn, horizon
                )

                # Convert range to list for Plotly
                future_years = list(range(
                    series.index.max() + 1,
                    series.index.max() + horizon + 1
                ))

                result = pd.DataFrame({
                    "Year": future_years,
                    "Forecast": forecast,
                    "Lower CI": lower,
                    "Upper CI": upper
                })

                st.dataframe(result, use_container_width=True)

                # Plot forecast
                fig_f = px.line(title="Forecast vs Observed")

                fig_f.add_scatter(
                    x=list(series.index),
                    y=series.values,
                    mode="lines+markers",
                    name="Observed"
                )

                fig_f.add_scatter(
                    x=future_years,
                    y=forecast,
                    mode="lines+markers",
                    name="Forecast"
                )

                fig_f.add_scatter(
                    x=future_years,
                    y=lower,
                    mode="lines",
                    name="Lower CI",
                    line=dict(dash="dot")
                )

                fig_f.add_scatter(
                    x=future_years,
                    y=upper,
                    mode="lines",
                    name="Upper CI",
                    line=dict(dash="dot")
                )

                st.plotly_chart(fig_f, use_container_width=True)

                st.info(
                    "⚠️ Forecast is exploratory and intended for planning "
                    "and policy analysis only."
                )

    # -----------------------------
    # Data table
    # -----------------------------
    st.subheader("📋 Data Table")

    table_df = filtered_df.pivot_table(
        index=["Indicator", "Disaggregation", "Unit"],
        columns="Year",
        values="Value"
    ).reset_index()

    st.dataframe(table_df, use_container_width=True)

    # -----------------------------
    # Footer
    # -----------------------------
    st.markdown("---")
    st.caption("⚡ Electricity Indicators Dashboard | Production Version")


# =====================================================
# RUN APP
# =====================================================
if __name__ == "__main__":
    app()
