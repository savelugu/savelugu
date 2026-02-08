import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import pmdarima as pm

# =====================================================
# FORECASTING HELPERS
# =====================================================

def naive_drift(series, steps):
    drift = (series.iloc[-1] - series.iloc[0]) / (len(series) - 1)
    return np.array([series.iloc[-1] + drift * (i + 1) for i in range(steps)])

def ets_model(series, steps):
    model = ExponentialSmoothing(series, trend="add", seasonal=None).fit()
    return model.forecast(steps)

def auto_arima_model(series, steps):
    model = pm.auto_arima(series, seasonal=False, stepwise=True,
                          suppress_warnings=True, error_action="ignore")
    return model.predict(n_periods=steps)

def backtest(series, model_fn, min_train=6):
    errors = []
    for i in range(min_train, len(series)):
        train = series.iloc[:i]
        test = series.iloc[i:i + 1]
        forecast = model_fn(train, 1)
        forecast = np.array(forecast)
        if len(forecast) == 0 or len(test) == 0:
            continue
        errors.append(abs(test.values[0] - forecast[0]))
    return np.mean(errors) if errors else np.nan

def select_best_model(series):
    models = {
        "Naive Drift": naive_drift,
        "ETS (Holt)": ets_model,
        "Auto ARIMA": auto_arima_model
    }
    scores = {name: backtest(series, fn) for name, fn in models.items()}
    scores = {k: v for k, v in scores.items() if not np.isnan(v)}
    if not scores:
        return None, None, {}
    best_name = min(scores, key=scores.get)
    return best_name, models[best_name], scores

def generate_forecast(series, model_fn, steps):
    forecast = np.array(model_fn(series, steps))
    sigma = series.diff().dropna().std()
    lower = forecast - 1.96 * sigma
    upper = forecast + 1.96 * sigma
    return forecast, lower, upper

# =====================================================
# STREAMLIT APP
# =====================================================

def app():
    st.set_page_config(
        page_title="Agriculture Indicators Dashboard",
        layout="wide",
        page_icon="🌾"
    )

    st.title("🌾 Agriculture Indicators Dashboard")
    st.markdown(
        "Production dashboard for agriculture participation, farmers, "
        "livestock, and climate-smart practices (2015–2024)."
    )

    # -----------------------------
    # DATA
    # -----------------------------
    years = list(range(2015, 2025))
    data = [
        ["Population in Agriculture", "Female", "% (0-100)", 18, 20, 21, 22, 25, 25, 23, 21, 25, 27],
        ["Population in Agriculture", "Male", "% (0-100)", 62, 63, 63, 64, 62, 62, 62, 64, 61, 60],
        ["Population in Agriculture", "Total", "% (0-100)", 80, 83, 84, 86, 87, 87, 85, 85, 86, 87],
        ["Number of Farmers", "Female", "Number", 14986, 15037, 15268, 16102, 16946, 18216, 19476, 19930, 35572, 35850],
        ["Number of Farmers", "Male", "Number", 49603, 51812, 52384, 52645, 53372, 54357, 54865, 52840, 50450, 50683],
        ["Number of Farmers", "Total", "Number", 64589, 66849, 67652, 68747, 70318, 72573, 74341, 72770, 86022, 86533],
        ["Livestock Reared", "Goats", "Number", 68975, 71653, 74689, 77052, 81228, 91371, 98499, 98871, 104130, 107320],
        ["Livestock Reared", "Cattle", "Number", 2985, 30975, 33581, 36872, 39046, 41226, 42052, 43356, 46230, 48120],
        ["Livestock Reared", "Poultry", "Number", 91986, 93985, 95894, 98987, 106695, 112391, 115785, 116425, 120322, 125654],
        ["CSA Adoption Rate", "Total", "% (0-100)", 11, 13, 23, 35, 40, 43, 45, 51, 53, 55],
    ]
    columns = ["Indicator", "Disaggregation", "Unit"] + years
    df = pd.DataFrame(data, columns=columns)

    df_long = df.melt(id_vars=["Indicator", "Disaggregation", "Unit"],
                      var_name="Year", value_name="Value")
    df_long["Year"] = df_long["Year"].astype(int)

    # -----------------------------
    # SIDEBAR
    # -----------------------------
    st.sidebar.header("🔎 Filters")
    indicator = st.sidebar.selectbox("Select Indicator", df_long["Indicator"].unique())
    disaggregation = st.sidebar.multiselect(
        "Select Disaggregation",
        df_long[df_long["Indicator"] == indicator]["Disaggregation"].unique(),
        default=list(df_long[df_long["Indicator"] == indicator]["Disaggregation"].unique())
    )
    filtered_df = df_long[
        (df_long["Indicator"] == indicator) &
        (df_long["Disaggregation"].isin(disaggregation))
    ]

    # -----------------------------
    # KPIs
    # -----------------------------
    st.subheader("📊 Key Metrics")
    latest_year = filtered_df["Year"].max()
    latest_data = filtered_df[filtered_df["Year"] == latest_year]
    cols = st.columns(len(latest_data))
    for col, (_, row) in zip(cols, latest_data.iterrows()):
        value = row["Value"]
        if row["Unit"] == "Number" and pd.notna(value):
            value = f"{int(value):,}"
        col.metric(row["Disaggregation"], value)

    # -----------------------------
    # TREND
    # -----------------------------
    st.subheader("📈 Trend Over Time")
    fig = px.line(filtered_df, x="Year", y="Value", color="Disaggregation", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # FORECAST
    # -----------------------------
    st.subheader("🔮 Forecast")
    enable_forecast = st.checkbox("Enable forecasting")

    if enable_forecast:
        horizon = st.slider("Forecast horizon (years)", 1, 5, 3)
        forecast_df = filtered_df.dropna()
        auto_forecast_indicators = ["Population in Agriculture", "Number of Farmers", "Livestock Reared"]

        if indicator in auto_forecast_indicators:
            # Forecast all disaggregations separately
            for disagg in forecast_df["Disaggregation"].unique():
                series = forecast_df[forecast_df["Disaggregation"] == disagg].sort_values("Year").set_index("Year")["Value"]

                if len(series) < 6:
                    st.error(f"Not enough data to forecast {disagg}.")
                    continue

                best_name, best_fn, scores = select_best_model(series)
                if best_name is None:
                    st.warning(f"Unable to select a model for {disagg}.")
                    continue

                st.success(f"Forecast for **{disagg}** (Model: {best_name})")
                st.markdown("**Backtest MAE:**")
                st.json(scores)

                forecast, lower, upper = generate_forecast(series, best_fn, horizon)
                future_years = list(range(series.index.max() + 1, series.index.max() + horizon + 1))
                result = pd.DataFrame({
                    "Year": future_years,
                    "Forecast": forecast,
                    "Lower CI": lower,
                    "Upper CI": upper
                })
                st.dataframe(result, use_container_width=True)

                fig_f = px.line(title=f"{disagg}: Observed vs Forecast")
                fig_f.add_scatter(x=list(series.index), y=series.values, mode="lines+markers", name="Observed")
                fig_f.add_scatter(x=future_years, y=forecast, mode="lines+markers", name="Forecast")
                fig_f.add_scatter(x=future_years, y=lower, mode="lines", name="Lower CI", line=dict(dash="dot"))
                fig_f.add_scatter(x=future_years, y=upper, mode="lines", name="Upper CI", line=dict(dash="dot"))
                st.plotly_chart(fig_f, use_container_width=True)

                st.info("⚠️ Forecasts are exploratory and intended for planning and policy analysis.")

        else:
            # Other indicators: single disaggregation only
            if forecast_df["Disaggregation"].nunique() != 1:
                st.warning("Select exactly ONE disaggregation to forecast.")
            else:
                series = forecast_df.sort_values("Year").set_index("Year")["Value"]

                if len(series) < 6:
                    st.error("Not enough data for forecasting.")
                else:
                    best_name, best_fn, scores = select_best_model(series)
                    if best_name is None:
                        st.warning("Unable to select a forecasting model (insufficient data).")
                    else:
                        st.success(f"Selected model: **{best_name}**")
                        st.markdown("### Backtest MAE")
                        st.json(scores)

                        forecast, lower, upper = generate_forecast(series, best_fn, horizon)
                        future_years = list(range(series.index.max() + 1, series.index.max() + horizon + 1))
                        result = pd.DataFrame({
                            "Year": future_years,
                            "Forecast": forecast,
                            "Lower CI": lower,
                            "Upper CI": upper
                        })
                        st.dataframe(result, use_container_width=True)

                        fig_f = px.line(title="Observed vs Forecast")
                        fig_f.add_scatter(x=list(series.index), y=series.values, mode="lines+markers", name="Observed")
                        fig_f.add_scatter(x=future_years, y=forecast, mode="lines+markers", name="Forecast")
                        fig_f.add_scatter(x=future_years, y=lower, mode="lines", name="Lower CI", line=dict(dash="dot"))
                        fig_f.add_scatter(x=future_years, y=upper, mode="lines", name="Upper CI", line=dict(dash="dot"))
                        st.plotly_chart(fig_f, use_container_width=True)

                        st.info("⚠️ Forecasts are exploratory and intended for planning and policy analysis.")

    # -----------------------------
    # DATA TABLE
    # -----------------------------
    st.subheader("📋 Data Table")
    table_df = filtered_df.pivot_table(
        index=["Indicator", "Disaggregation", "Unit"],
        columns="Year",
        values="Value"
    ).reset_index()
    st.dataframe(table_df, use_container_width=True)

    st.markdown("---")
    st.caption("🌾 Agriculture Indicators Dashboard | Production Version")

# =====================================================
# RUN APP
# =====================================================
if __name__ == "__main__":
    app()
