import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

def load_annual_data():
    """Load the annual birth statistics data"""
    data = [
        ["HOSPITAL", "0-14", 1, 1, 0, 2],
        ["CLINIC", "15-19", 12, 9, 0, 21],
        ["HOSPITAL", "15-19", 147, 124, 0, 271],
        ["HOUSE", "15-19", 5, 10, 0, 15],
        ["CLINIC", "20-24", 58, 81, 0, 139],
        ["HOSPITAL", "20-24", 401, 393, 0, 794],
        ["HOUSE", "20-24", 34, 36, 0, 70],
        ["CLINIC", "25-29", 85, 72, 0, 157],
        ["HOSPITAL", "25-29", 454, 448, 0, 902],
        ["HOUSE", "25-29", 62, 55, 0, 117],
        ["CLINIC", "30-34", 78, 70, 0, 148],
        ["HOSPITAL", "30-34", 415, 387, 0, 802],
        ["HOUSE", "30-34", 57, 55, 0, 112],
        ["CLINIC", "35-39", 76, 78, 0, 154],
        ["HOSPITAL", "35-39", 249, 241, 0, 490],
        ["HOUSE", "35-39", 52, 47, 0, 99],
        ["CLINIC", "40-44", 6, 10, 1, 17],
        ["HOSPITAL", "40-44", 75, 59, 0, 134],
        ["HOUSE", "40-44", 5, 10, 0, 15],
        ["HOSPITAL", "45-49", 4, 3, 0, 7],
        ["CLINIC", "45-49", 1, 0, 0, 1],
        ["CLINIC", "50+", 1, 0, 0, 1]
    ]
    
    df = pd.DataFrame(data, columns=["Place of Birth", "Age of Mother", "Male", "Female", "Others", "All Sexes"])
    
    # Calculate percentages
    df["Male %"] = round(df["Male"] / df["All Sexes"] * 100, 1)
    df["Female %"] = round(df["Female"] / df["All Sexes"] * 100, 1)
    df["Others %"] = round(df["Others"] / df["All Sexes"] * 100, 1)
    
    return df

def create_monthly_distribution(df):
    """Create monthly distribution from annual data"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    monthly_data = []
    np.random.seed(42)  # For reproducibility
    
    for _, row in df.iterrows():
        total = row["All Sexes"]
        monthly_counts = np.random.multinomial(total, np.ones(12)/12)  # Equal distribution
        
        for i, count in enumerate(monthly_counts):
            if count > 0:
                # Distribute genders proportionally
                male_count = int(count * (row["Male"] / total))
                female_count = int(count * (row["Female"] / total))
                others_count = count - male_count - female_count
                
                monthly_data.append([
                    row["Place of Birth"],
                    row["Age of Mother"],
                    male_count,
                    female_count,
                    others_count,
                    count,
                    months[i],
                    f"2025-{i+1:02d}",
                    2025
                ])
    
    monthly_df = pd.DataFrame(monthly_data, columns=[
        "Place of Birth", "Age of Mother", "Male", "Female", "Others", 
        "All Sexes", "Month", "Year-Month", "Year"
    ])
    
    return monthly_df

def setup_sidebar(df, monthly_df):
    """Setup sidebar with filters"""
    st.sidebar.header("📅 Data Period")
    st.sidebar.success("**January 2025 - December 2025**")
    st.sidebar.markdown("---")
    
    st.sidebar.header("🔍 Filters")
    
    # Place filter
    places = ["All"] + list(df["Place of Birth"].unique())
    selected_place = st.sidebar.selectbox("Place of Birth:", places)
    
    # Age filter
    ages = ["All"] + list(df["Age of Mother"].unique())
    selected_age = st.sidebar.selectbox("Mother's Age Group:", ages)
    
    # Month filter
    months = ["All"] + sorted(list(monthly_df["Month"].unique()))
    selected_month = st.sidebar.selectbox("Month:", months)
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Select 'All' to view complete 2025 data")
    
    return selected_place, selected_age, selected_month

def filter_data(df, monthly_df, place, age, month):
    """Apply filters to datasets"""
    filtered_df = df.copy()
    filtered_monthly = monthly_df.copy()
    
    if place != "All":
        filtered_df = filtered_df[filtered_df["Place of Birth"] == place]
        filtered_monthly = filtered_monthly[filtered_monthly["Place of Birth"] == place]
    
    if age != "All":
        filtered_df = filtered_df[filtered_df["Age of Mother"] == age]
        filtered_monthly = filtered_monthly[filtered_monthly["Age of Mother"] == age]
    
    if month != "All":
        filtered_monthly = filtered_monthly[filtered_monthly["Month"] == month]
    
    return filtered_df, filtered_monthly

def display_header_metrics(filtered_monthly):
    """Display key metrics at the top"""
    total_births = filtered_monthly["All Sexes"].sum()
    male_births = filtered_monthly["Male"].sum()
    female_births = filtered_monthly["Female"].sum()
    
    # Calculate percentages
    male_percent = round((male_births / total_births * 100), 1) if total_births > 0 else 0
    female_percent = round((female_births / total_births * 100), 1) if total_births > 0 else 0
    
    # Determine period text
    if filtered_monthly["Month"].nunique() == 1:
        month_name = filtered_monthly["Month"].iloc[0]
        period_text = f"{month_name} 2025"
        avg_daily = round(total_births / 30, 1)
    else:
        period_text = "Full Year 2025"
        avg_daily = round(total_births / 365, 1)
    
    st.subheader(f"📊 Analysis Period: {period_text}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Births", f"{total_births:,}")
    
    with col2:
        st.metric("Male Births", f"{male_births:,}", f"{male_percent}%")
    
    with col3:
        st.metric("Female Births", f"{female_births:,}", f"{female_percent}%")
    
    with col4:
        st.metric("Avg Daily", f"{avg_daily}")
    
    return total_births

def create_overview_charts(filtered_df, filtered_monthly):
    """Create charts for overview tab"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Place distribution
        if not filtered_df.empty:
            place_summary = filtered_df.groupby("Place of Birth")["All Sexes"].sum().reset_index()
            fig1 = px.pie(place_summary, values="All Sexes", names="Place of Birth",
                         title="Distribution by Birth Place", hole=0.4)
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Gender distribution
        gender_data = {
            "Gender": ["Male", "Female", "Others"],
            "Count": [
                filtered_df["Male"].sum(),
                filtered_df["Female"].sum(),
                filtered_df["Others"].sum()
            ]
        }
        gender_df = pd.DataFrame(gender_data)
        fig2 = px.bar(gender_df, x="Gender", y="Count", color="Gender",
                     title="Gender Distribution",
                     color_discrete_map={"Male": "#1f77b4", "Female": "#ff7f0e", "Others": "#2ca02c"})
        st.plotly_chart(fig2, use_container_width=True)
    
    # Age distribution
    if not filtered_df.empty:
        age_order = ["0-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50+"]
        age_summary = filtered_df.groupby("Age of Mother")["All Sexes"].sum().reset_index()
        age_summary["Age of Mother"] = pd.Categorical(age_summary["Age of Mother"], categories=age_order, ordered=True)
        age_summary = age_summary.sort_values("Age of Mother")
        
        fig3 = px.bar(age_summary, x="Age of Mother", y="All Sexes",
                     title="Births by Mother's Age Group",
                     color="All Sexes", color_continuous_scale="viridis")
        st.plotly_chart(fig3, use_container_width=True)

def create_monthly_analysis(filtered_monthly):
    """Create monthly analysis charts"""
    st.subheader("📈 Monthly Trends Analysis")
    
    # Monthly trend line chart
    monthly_trend = filtered_monthly.groupby(["Month", "Year-Month"])["All Sexes"].sum().reset_index()
    
    # Sort months in correct order
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_trend["Month"] = pd.Categorical(monthly_trend["Month"], categories=month_order, ordered=True)
    monthly_trend = monthly_trend.sort_values("Month")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(monthly_trend, x="Month", y="All Sexes",
                      title="Monthly Birth Trend", markers=True)
        fig1.update_traces(line=dict(width=3))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(monthly_trend, x="Month", y="All Sexes",
                     title="Monthly Birth Counts",
                     color="All Sexes", color_continuous_scale="blues")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Heatmap by place and month
    if filtered_monthly["Place of Birth"].nunique() > 1:
        st.subheader("🌡️ Births Heatmap by Place and Month")
        heatmap_data = filtered_monthly.pivot_table(
            index="Place of Birth", 
            columns="Month", 
            values="All Sexes", 
            aggfunc="sum"
        ).reindex(columns=month_order)
        
        fig3 = px.imshow(heatmap_data, 
                        title="Births by Place and Month",
                        labels=dict(x="Month", y="Place", color="Births"),
                        color_continuous_scale="YlOrRd")
        st.plotly_chart(fig3, use_container_width=True)

def create_place_analysis(filtered_monthly):
    """Create place-based analysis"""
    st.subheader("🏥 Birth Place Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution by place
        place_gender = filtered_monthly.groupby("Place of Birth")[["Male", "Female", "Others"]].sum()
        fig1 = px.bar(place_gender, barmode="group",
                     title="Gender Distribution by Birth Place")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Scatter plot: Male vs Female by place
        place_stats = filtered_monthly.groupby("Place of Birth").agg({
            "All Sexes": "sum",
            "Male": "sum",
            "Female": "sum"
        }).reset_index()
        
        place_stats["Gender Ratio"] = round(place_stats["Male"] / place_stats["Female"], 2)
        
        fig2 = px.scatter(place_stats, x="Male", y="Female",
                         size="All Sexes", color="Place of Birth",
                         title="Male vs Female Births by Place",
                         hover_name="Place of Birth",
                         hover_data=["Gender Ratio"],
                         size_max=60)
        st.plotly_chart(fig2, use_container_width=True)

def create_age_analysis(filtered_monthly):
    """Create age-based analysis"""
    st.subheader("👩 Age Group Analysis")
    
    # Gender distribution by age
    melted_data = filtered_monthly.melt(
        id_vars=["Age of Mother"],
        value_vars=["Male", "Female", "Others"],
        var_name="Gender",
        value_name="Count"
    )
    
    age_gender_summary = melted_data.groupby(["Age of Mother", "Gender"])["Count"].sum().reset_index()
    
    # Sort age groups
    age_order = ["0-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50+"]
    age_gender_summary["Age of Mother"] = pd.Categorical(
        age_gender_summary["Age of Mother"], 
        categories=age_order, 
        ordered=True
    )
    age_gender_summary = age_gender_summary.sort_values("Age of Mother")
    
    fig1 = px.bar(age_gender_summary, x="Age of Mother", y="Count", color="Gender",
                 barmode="group", title="Gender Distribution by Age Group",
                 color_discrete_map={"Male": "#1f77b4", "Female": "#ff7f0e", "Others": "#2ca02c"})
    st.plotly_chart(fig1, use_container_width=True)
    
    # Age distribution by place
    if filtered_monthly["Place of Birth"].nunique() > 1:
        st.subheader("📊 Age Distribution by Birth Place")
        
        age_place_data = filtered_monthly.groupby(["Age of Mother", "Place of Birth"])["All Sexes"].sum().reset_index()
        age_place_data["Age of Mother"] = pd.Categorical(age_place_data["Age of Mother"], categories=age_order, ordered=True)
        age_place_data = age_place_data.sort_values("Age of Mother")
        
        fig2 = px.bar(age_place_data, x="Age of Mother", y="All Sexes", color="Place of Birth",
                     barmode="group", title="Births by Age Group and Place")
        st.plotly_chart(fig2, use_container_width=True)

def create_data_explorer(filtered_df, filtered_monthly, place, age, month):
    """Create data explorer tab"""
    st.subheader("📋 Data Explorer")
    
    tab1, tab2, tab3 = st.tabs(["📊 Summary Data", "📅 Monthly Details", "📈 Statistics"])
    
    with tab1:
        st.markdown("**Annual Summary Data**")
        display_df = filtered_df.copy()
        display_df["Year"] = 2025
        st.dataframe(
            display_df.style.format({
                "Male %": "{:.1f}%",
                "Female %": "{:.1f}%",
                "Others %": "{:.1f}%"
            }),
            use_container_width=True,
            height=400
        )
        
        # Download button for annual data
        csv_annual = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Annual Data (CSV)",
            data=csv_annual,
            file_name=f"births_annual_{place}_{age}.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.markdown("**Monthly Detailed Data**")
        st.dataframe(filtered_monthly, use_container_width=True, height=400)
        
        # Download button for monthly data
        csv_monthly = filtered_monthly.to_csv(index=False)
        st.download_button(
            label="📥 Download Monthly Data (CSV)",
            data=csv_monthly,
            file_name=f"births_monthly_{place}_{age}_{month}.csv",
            mime="text/csv"
        )
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Summary Statistics**")
            stats_df = filtered_monthly[["Male", "Female", "Others", "All Sexes"]].describe()
            st.dataframe(stats_df, use_container_width=True)
        
        with col2:
            st.markdown("**Key Insights**")
            
            total = filtered_monthly["All Sexes"].sum()
            if total > 0:
                # Most common place
                common_place = filtered_monthly.groupby("Place of Birth")["All Sexes"].sum().idxmax()
                place_percent = round(filtered_monthly.groupby("Place of Birth")["All Sexes"].sum().max() / total * 100, 1)
                
                # Most common age group
                common_age = filtered_monthly.groupby("Age of Mother")["All Sexes"].sum().idxmax()
                age_percent = round(filtered_monthly.groupby("Age of Mother")["All Sexes"].sum().max() / total * 100, 1)
                
                # Peak month
                if filtered_monthly["Month"].nunique() > 1:
                    peak_month = filtered_monthly.groupby("Month")["All Sexes"].sum().idxmax()
                else:
                    peak_month = filtered_monthly["Month"].iloc[0]
                
                st.metric("Most Common Place", f"{common_place}", f"{place_percent}%")
                st.metric("Most Common Age", f"{common_age}", f"{age_percent}%")
                st.metric("Peak Month", peak_month)
                st.metric("Records Count", len(filtered_monthly))

def display_footer():
    """Display app footer"""
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center">
        <p><strong>Births and Deaths Registry - 2025 Annual Report</strong></p>
        <p>Data Period: January 1, 2025 - December 31, 2025</p>
        <p>Generated on: {datetime.now().strftime("%B %d, %Y %H:%M")}</p>
        <p style="color: #666; font-size: 0.9em;">
            Note: Monthly distribution is simulated for demonstration purposes
        </p>
    </div>
    """, unsafe_allow_html=True)

def app():
    """Main Streamlit application function"""
    # Page configuration
    st.set_page_config(
        page_title="Birth Statistics Dashboard 2025",
        page_icon="👶",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # App title
    st.title("👶 Birth Statistics Dashboard")
    st.markdown("### January 2025 - December 2025")
    st.markdown("Analyzing birth records by place of birth, mother's age, and gender")
    
    # Load data
    annual_df = load_annual_data()
    monthly_df = create_monthly_distribution(annual_df)
    
    # Setup sidebar and get filters
    selected_place, selected_age, selected_month = setup_sidebar(annual_df, monthly_df)
    
    # Apply filters
    filtered_annual, filtered_monthly = filter_data(
        annual_df, monthly_df, selected_place, selected_age, selected_month
    )
    
    # Display header metrics
    display_header_metrics(filtered_monthly)
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "📈 Monthly Trends", 
        "🏥 Place Analysis", 
        "👩 Age Analysis", 
        "🔍 Data Explorer"
    ])
    
    # Tab 1: Overview
    with tab1:
        create_overview_charts(filtered_annual, filtered_monthly)
    
    # Tab 2: Monthly Trends
    with tab2:
        create_monthly_analysis(filtered_monthly)
    
    # Tab 3: Place Analysis
    with tab3:
        create_place_analysis(filtered_monthly)
    
    # Tab 4: Age Analysis
    with tab4:
        create_age_analysis(filtered_monthly)
    
    # Tab 5: Data Explorer
    with tab5:
        create_data_explorer(filtered_annual, filtered_monthly, selected_place, selected_age, selected_month)
    
    # Footer
    display_footer()

# Run the app
if __name__ == "__main__":
    app()
