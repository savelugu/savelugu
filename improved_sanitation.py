import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Sanitation Analytics Dashboard",
    page_icon="🚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create the dataset
@st.cache_data
def create_dataset():
    data = {
        'Indicator': [
            'Percentage of households with improved sanitation',
            'Percentage of households with improved sanitation',
            'Percentage of households with improved sanitation',
            'Number of households with latrine',
            'Number of households with latrine',
            'Number of households with latrine',
            'Percentage with refuse collection',
            'Percentage with refuse collection',
            'Percentage with refuse collection',
            'Communities sensitized',
            'Communities sensitized',
            'Communities sensitized',
            'Total waste generated',
            'Total waste generated',
            'Total waste generated',
            'Waste collected from households',
            'Waste collected from households',
            'Waste collected from households',
            'Waste collected from other origins',
            'Waste collected from other origins',
            'Waste collected from other origins',
        ],
        'Level': [
            'Urban', 'Rural', 'Total',
            'Urban', 'Rural', 'Total',
            'Urban', 'Rural', 'Total',
            'Urban', 'Rural', 'Total',
            'Urban', 'Rural', 'Total',
            'Urban', 'Rural', 'Total',
            'Urban', 'Rural', 'Total',
        ],
        'Unit': [
            '% (0-100)', '% (0-100)', '% (0-100)',
            'number', 'number', 'number',
            '% (0-100)', '% (0-100)', '% (0-100)',
            'number', 'number', 'number',
            'tons', 'tons', 'tons',
            'tons', 'tons', 'tons',
            'tons', 'tons', 'tons',
        ]
    }
    
    years = list(range(2015, 2025))
    year_data = {
        2015: [1.0, 1.0, 1.0, 944, 52, 996, None, None, None, 1, 8, 9, 16883.88, 11255.92, 28139.8, 16883.88, 11255.92, 28139.8, None, None, None],
        2016: [7.0, 7.0, 7.0, 1048, 147, 1195, None, None, None, 1, 16, 17, 16883.88, 11255.92, 28139.8, 16883.88, 11255.92, 28139.8, None, None, None],
        2017: [9.0, 9.0, 9.0, 1184, 273, 1457, None, None, None, 1, 32, 33, 16883.88, 11255.92, 28139.8, 16883.88, 11255.92, 28139.8, None, None, None],
        2018: [13.0, 13.0, 13.0, 803, 227, 1030, 2.0, None, 2.0, 1, 26, 27, 16121.1, 10747.4, 26868.5, 16121.1, 10747.4, 26868.5, None, None, None],
        2019: [13.0, 13.0, 13.0, 1922, 415, 2337, 5.0, None, 5.0, 2, 22, 24, 16121.1, 10747.4, 26868.5, 16121.1, 10747.4, 26868.5, None, None, None],
        2020: [5.0, 5.0, 5.0, 2661, 412, 3073, 5.0, None, 5.0, 4, 30, 34, 12273.18, 8182.12, 20455.3, 12273.18, 8182.12, 20455.3, None, None, None],
        2021: [5.0, 5.0, 5.0, 3254, 412, 3666, 8.0, None, 8.0, 4, 44, 48, 12273.18, 8182.12, 20455.3, 12273.18, 8182.12, 20455.3, None, None, None],
        2022: [10.0, 10.0, 10.0, 3644, 412, 4056, 9.0, None, 9.0, 4, 28, 32, 12475.62, 8317.08, 20792.7, 12475.62, 8317.08, 20792.7, None, None, None],
        2023: [10.0, 10.0, 10.0, 4064, 412, 4476, 10.0, None, 10.0, 3, 18, 21, 16896.24, 11264.16, 28160.4, 16896.24, 11264.16, 28160.4, None, None, None],
        2024: [10.0, 10.0, 10.0, 4514, 412, 4926, 10.0, None, 10.0, 2, 16, 18, 17403.0, 11602.0, 29005.0, 17403.0, 11602.0, 29005.0, None, None, None]
    }
    
    df = pd.DataFrame(data)
    for year in years:
        df[year] = year_data[year]
    
    df_melted = df.melt(id_vars=['Indicator', 'Level', 'Unit'], 
                        value_vars=years,
                        var_name='Year', 
                        value_name='Value')
    
    df_melted['Year'] = df_melted['Year'].astype(int)
    
    return df, df_melted

# SARIMA Forecasting Function
def generate_sarima_forecast(series, forecast_years, seasonal_period=4, confidence_level=0.95):
    try:
        series_clean = series.dropna()
        
        if len(series_clean) < 8:
            return None, None, "Insufficient data for SARIMA forecast (need at least 8 data points)"
        
        adf_result = adfuller(series_clean)
        is_stationary = adf_result[1] < 0.05
        
        if is_stationary:
            model = SARIMAX(series_clean, 
                          order=(1, 0, 1), 
                          seasonal_order=(0, 0, 0, seasonal_period),
                          enforce_stationarity=False,
                          enforce_invertibility=False)
        else:
            model = SARIMAX(series_clean, 
                          order=(1, 1, 1), 
                          seasonal_order=(0, 1, 1, seasonal_period),
                          enforce_stationarity=False,
                          enforce_invertibility=False)
        
        model_fit = model.fit(disp=False)
        forecast = model_fit.get_forecast(steps=forecast_years)
        forecast_values = forecast.predicted_mean
        confidence_intervals = forecast.conf_int(alpha=1-confidence_level)
        
        predictions = model_fit.predict(start=1, end=len(series_clean)-1)
        actuals = series_clean.iloc[1:]
        predictions_aligned = predictions.iloc[:len(actuals)]
        
        if len(actuals) > 0 and len(predictions_aligned) > 0:
            mask = actuals != 0
            if mask.any():
                mape = np.mean(np.abs((actuals[mask].values - predictions_aligned[mask].values) / actuals[mask].values)) * 100
            else:
                mape = np.nan
            
            rmse = np.sqrt(np.mean((actuals.values - predictions_aligned.values) ** 2))
        else:
            mape = np.nan
            rmse = np.nan
        
        metrics = {
            'mape': mape,
            'rmse': rmse,
            'aic': model_fit.aic,
            'bic': model_fit.bic,
            'is_stationary': is_stationary,
            'adf_pvalue': adf_result[1]
        }
        
        return forecast_values, confidence_intervals, metrics
        
    except Exception as e:
        return None, None, f"Forecast error: {str(e)}"

def create_forecast_plot(
    historical_data,
    forecast_df,
    selected_indicator,
    selected_level,
    unit,
    confidence_intervals=None
):
    fig = go.Figure()

    # =========================
    # Historical data
    # =========================
    fig.add_trace(go.Scatter(
        x=historical_data['Year'],
        y=historical_data['Value'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#4CC9F0', width=3),
        marker=dict(size=7),
        hovertemplate="Year %{x}<br>Value %{y}<extra></extra>"
    ))

    # =========================
    # Forecast
    # =========================
    fig.add_trace(go.Scatter(
        x=forecast_df['Year'],
        y=forecast_df['Value'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#F72585', width=3, dash='dash'),
        marker=dict(size=7, symbol='diamond'),
        hovertemplate="Year %{x}<br>Forecast %{y}<extra></extra>"
    ))

    # =========================
    # Confidence Interval
    # =========================
    if confidence_intervals is not None:
        fig.add_trace(go.Scatter(
            x=forecast_df['Year'],
            y=forecast_df['Upper_CI'],
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=forecast_df['Year'],
            y=forecast_df['Lower_CI'],
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(247, 37, 133, 0.25)',
            line=dict(width=0),
            name='Confidence Interval',
            hoverinfo='skip'
        ))

    last_year = historical_data['Year'].max()

    # =========================
    # Forecast shading
    # =========================
    fig.add_vrect(
        x0=last_year + 0.5,
        x1=forecast_df['Year'].max() + 0.5,
        fillcolor="rgba(255,255,255,0.04)",
        layer="below",
        line_width=0,
        annotation_text="Forecast Period",
        annotation_position="top left"
    )

    # =========================
    # Layout (DARK THEME)
    # =========================
    fig.update_layout(
        template="plotly_dark",
        height=520,
        title=dict(
            text=f"{selected_indicator}<br><sup>{selected_level} • SARIMA Forecast</sup>",
            x=0.5,
            font=dict(size=20)
        ),
        xaxis=dict(
            title="Year",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)"
        ),
        yaxis=dict(
            title=unit,
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)"
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=50, r=40, t=90, b=50)
    )

    return fig


def setup_sidebar():
    """Setup sidebar"""
    df, df_melted = create_dataset()
    
    st.sidebar.header("📊 Filters & Settings")
    
    # Indicator filter
    indicators = df['Indicator'].unique()
    selected_indicator = st.sidebar.selectbox(
        "Select Indicator",
        options=indicators,
        index=0
    )
    
    # Level filter for the selected indicator
    available_levels = df[df['Indicator'] == selected_indicator]['Level'].unique()
    selected_level = st.sidebar.selectbox(
        "Select Level",
        options=available_levels,
        index=0 if 'Total' in available_levels else 0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Forecast Settings")
    
    forecast_years = st.sidebar.slider(
        "Forecast Years Ahead",
        min_value=1,
        max_value=5,
        value=3
    )
    
    confidence_level = st.sidebar.slider(
        "Confidence Level (%)",
        min_value=80,
        max_value=99,
        value=95
    ) / 100
    
    include_seasonality = st.sidebar.checkbox(
        "Include Seasonality",
        value=True
    )
    
    return {
        'selected_indicator': selected_indicator,
        'selected_level': selected_level,
        'forecast_years': forecast_years,
        'confidence_level': confidence_level,
        'include_seasonality': include_seasonality,
        'df': df,
        'df_melted': df_melted
    }

def display_forecast_tab(settings):
    """Display the forecasting tab"""
    df_melted = settings['df_melted']
    
    st.header("📈 SARIMA Forecasting")
    
    # Get historical data
    historical_data = df_melted[
        (df_melted['Indicator'] == settings['selected_indicator']) &
        (df_melted['Level'] == settings['selected_level'])
    ].sort_values('Year')
    
    if not historical_data.empty and historical_data['Value'].notna().sum() > 0:
        series = historical_data.set_index('Year')['Value']
        
        # Generate forecast
        seasonal_period = 4 if settings['include_seasonality'] else 0
        forecast_values, confidence_intervals, forecast_info = generate_sarima_forecast(
            series, 
            settings['forecast_years'],
            seasonal_period,
            settings['confidence_level']
        )
        
        if forecast_values is not None:
            # Create forecast dataframe
            forecast_years_list = list(range(series.index.max() + 1, series.index.max() + 1 + settings['forecast_years']))
            forecast_df = pd.DataFrame({
                'Year': forecast_years_list,
                'Value': forecast_values.values,
                'Type': 'Forecast'
            })
            
            if confidence_intervals is not None:
                forecast_df['Lower_CI'] = confidence_intervals.iloc[:, 0].values
                forecast_df['Upper_CI'] = confidence_intervals.iloc[:, 1].values
            
            # Create plot
            unit = historical_data['Unit'].iloc[0]
            fig = create_forecast_plot(
                historical_data[['Year', 'Value']], 
                forecast_df,
                settings['selected_indicator'],
                settings['selected_level'],
                unit,
                confidence_intervals
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display forecast metrics
            if isinstance(forecast_info, dict):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if not np.isnan(forecast_info['mape']):
                        st.metric(
                            label="MAPE",
                            value=f"{forecast_info['mape']:.1f}%",
                            help="Mean Absolute Percentage Error"
                        )
                
                with col2:
                    if not np.isnan(forecast_info['rmse']):
                        st.metric(
                            label="RMSE",
                            value=f"{forecast_info['rmse']:.1f}",
                            help="Root Mean Square Error"
                        )
                
                with col3:
                    st.metric(
                        label="AIC",
                        value=f"{forecast_info['aic']:.1f}",
                        help="Akaike Information Criterion"
                    )
                
                with col4:
                    st.metric(
                        label="BIC",
                        value=f"{forecast_info['bic']:.1f}",
                        help="Bayesian Information Criterion"
                    )
            
            # Forecast summary
            st.subheader("Forecast Summary")
            col_sum1, col_sum2, col_sum3 = st.columns(3)
            
            with col_sum1:
                avg_growth = ((forecast_df['Value'].iloc[-1] / forecast_df['Value'].iloc[0]) ** (1/settings['forecast_years']) - 1) * 100
                st.metric(
                    label="Avg Annual Growth",
                    value=f"{avg_growth:+.1f}%"
                )
            
            with col_sum2:
                total_growth = ((forecast_df['Value'].iloc[-1] / series.iloc[-1]) - 1) * 100
                st.metric(
                    label="Total Growth",
                    value=f"{total_growth:+.1f}%",
                    delta=f"By {forecast_years_list[-1]}"
                )
            
            with col_sum3:
                if 'Upper_CI' in forecast_df.columns:
                    uncertainty = ((forecast_df['Upper_CI'].iloc[-1] - forecast_df['Lower_CI'].iloc[-1]) / forecast_df['Value'].iloc[-1]) * 100
                    st.metric(
                        label="Uncertainty Range",
                        value=f"±{uncertainty/2:.1f}%",
                        delta=f"{int(settings['confidence_level']*100)}% confidence"
                    )
            
            # Detailed forecast table
            st.subheader("Detailed Forecast")
            forecast_display_df = forecast_df[['Year', 'Value']].copy()
            forecast_display_df['Value'] = forecast_display_df['Value'].round(2)
            forecast_display_df.rename(columns={'Value': 'Forecast'}, inplace=True)
            
            if 'Lower_CI' in forecast_df.columns and 'Upper_CI' in forecast_df.columns:
                forecast_display_df['Lower Bound'] = forecast_df['Lower_CI'].round(2)
                forecast_display_df['Upper Bound'] = forecast_df['Upper_CI'].round(2)
            
            st.dataframe(
                forecast_display_df,
                use_container_width=True
            )
            
        else:
            st.error(f"Could not generate forecast: {forecast_info}")
            st.info("Try adjusting the forecast settings or select a different indicator/level with more historical data.")
    
    else:
        st.warning("Insufficient historical data available for forecasting. Please select a different indicator or level.")

def display_historical_trends_tab(settings):
    """Display historical trends tab"""
    st.header("📊 Historical Trends")
    
    df_melted = settings['df_melted']
    indicators = df_melted['Indicator'].unique()
    
    # Allow multiple indicators and levels for comparison
    selected_indicators_hist = st.multiselect(
        "Select Indicators for Comparison",
        options=indicators,
        default=[settings['selected_indicator']],
        key="hist_indicators"
    )
    
    if selected_indicators_hist:
        hist_data = df_melted[df_melted['Indicator'].isin(selected_indicators_hist)]
        
        if not hist_data.empty:
            # Create faceted plot
            fig = px.line(
                hist_data,
                x='Year',
                y='Value',
                color='Level',
                facet_col='Indicator',
                facet_col_wrap=2,
                title='Historical Trends Comparison',
                markers=True,
                height=500
            )
            
            fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            fig.update_xaxes(tickangle=45)
            fig.update_layout(
                hovermode='x unified',
                legend_title="Geographic Level"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Year-over-year growth analysis
            st.subheader("Year-over-Year Growth Analysis")
            
            for indicator in selected_indicators_hist:
                st.write(f"**{indicator}**")
                indicator_data = hist_data[hist_data['Indicator'] == indicator]
                
                # Calculate YoY growth for each level
                growth_data = []
                for level in indicator_data['Level'].unique():
                    level_data = indicator_data[indicator_data['Level'] == level].sort_values('Year')
                    level_data = level_data.dropna(subset=['Value'])
                    
                    if len(level_data) > 1:
                        level_data['YoY_Growth'] = level_data['Value'].pct_change() * 100
                        level_data['Level'] = level
                        growth_data.append(level_data[['Year', 'Level', 'YoY_Growth']])
                
                if growth_data:
                    growth_df = pd.concat(growth_data, ignore_index=True)
                    
                    # Create heatmap of YoY growth
                    pivot_df = growth_df.pivot(index='Level', columns='Year', values='YoY_Growth')
                    
                    fig_heatmap = px.imshow(
                        pivot_df,
                        labels=dict(x="Year", y="Level", color="Growth %"),
                        title=f"Year-over-Year Growth - {indicator}",
                        aspect="auto",
                        color_continuous_scale="RdYlGn"
                    )
                    
                    st.plotly_chart(fig_heatmap, use_container_width=True)

def display_data_analysis_tab(settings):
    """Display data analysis tab"""
    st.header("📋 Data Analysis")
    
    df_melted = settings['df_melted']
    
    # Interactive data explorer
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_indicator_exp = st.selectbox(
            "Select Indicator",
            options=df_melted['Indicator'].unique(),
            key="exp_indicator"
        )
    
    with col2:
        selected_level_exp = st.selectbox(
            "Select Level",
            options=df_melted[df_melted['Indicator'] == selected_indicator_exp]['Level'].unique(),
            key="exp_level"
        )
    
    with col3:
        chart_type = st.selectbox(
            "Chart Type",
            options=["Line Chart", "Area Chart", "Bar Chart"],
            key="chart_type"
        )
    
    # Display selected data
    exp_data = df_melted[
        (df_melted['Indicator'] == selected_indicator_exp) &
        (df_melted['Level'] == selected_level_exp)
    ].sort_values('Year')
    
    if not exp_data.empty:
        # Create chart based on selection
        if chart_type == "Line Chart":
            fig = px.line(
                exp_data, x='Year', y='Value',
                title=f'{selected_indicator_exp} - {selected_level_exp}',
                markers=True
            )
        elif chart_type == "Area Chart":
            fig = px.area(
                exp_data, x='Year', y='Value',
                title=f'{selected_indicator_exp} - {selected_level_exp}'
            )
        else:  # Bar Chart
            fig = px.bar(
                exp_data, x='Year', y='Value',
                title=f'{selected_indicator_exp} - {selected_level_exp}'
            )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        stats_df = exp_data['Value'].describe().round(2)
        st.dataframe(stats_df, use_container_width=True)
        
        # Data table
        st.subheader("Raw Data")
        st.dataframe(
            exp_data[['Year', 'Value']].rename(columns={'Value': 'Value (' + exp_data['Unit'].iloc[0] + ')'}),
            use_container_width=True,
            height=300
        )

st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

def app():
    """Main Streamlit application function"""
    # Title
    st.title("🚽 Sanitation Indicators Dashboard")
    
    # Setup sidebar and get settings
    settings = setup_sidebar()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Forecasting", "Historical Trends", "Data Analysis"])
    
    with tab1:
        display_forecast_tab(settings)
    
    with tab2:
        display_historical_trends_tab(settings)
    
    with tab3:
        display_data_analysis_tab(settings)
    
    # Simple footer
    st.markdown("---")
    st.caption("Sanitation Indicators Dashboard • Data: 2015-2024 • Powered by Streamlit")

# Run the app
if __name__ == "__main__":
    app()
