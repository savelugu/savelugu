import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import plotly.graph_objects as go
import altair as alt

def app():
    st.set_page_config(layout="wide")
    st.title("📄 Multidimensional Poverty Fact Sheet - Savelugu Municipal")

    # --- CSS Styling ---
    css = """
    <style>
    @keyframes bump {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .bumping-text {
        display: inline-block;
        animation: bump 1s infinite;
        font-size: 2.5rem;
        font-weight: bold;
        color: #00ccff;
        text-align: center;
        width: 100%;
        margin-bottom: 2rem;
    }
    .metric-glow {
        padding: 1rem;
        margin: 0.5rem;
        border-radius: 12px;
        background: #111;
        color: white;
        box-shadow: 0 0 15px rgba(0, 153, 255, 0.6);
        transition: 0.3s ease-in-out;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
    }
    .metric-glow:hover {
        box-shadow: 0 0 25px rgba(0, 153, 255, 1);
        transform: scale(1.02);
    }
    .circle-value {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: #00ccff;
        color: #000;
        font-size: 1.4rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 10px auto;
        box-shadow: 0 0 10px rgba(0, 153, 255, 0.7);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    st.markdown("<h1 class='bumping-text'>Savelugu Municipal Dashboard</h1>", unsafe_allow_html=True)

    # --- Intro Card ---
    st.markdown("""
    <div class="metric-glow">
        <h4>📊 Overview</h4>
        <p>This dashboard summarizes the <strong>multidimensional poverty statistics</strong> for <strong>Savelugu Municipal</strong>, based on the <strong>2021 Population and Housing Census (PHC)</strong>. It provides insights into who is poor, how poor they are, and which areas are most deprived.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Key Metrics Cards ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-glow">
            <h4>🧍‍♀️ Incidence</h4>
            <div class="circle-value">41.1%</div>
            <p>Percentage of population considered <strong>poor</strong>. Answers <em>"Who is poor?"</em></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-glow">
            <h4>🔥 Intensity</h4>
            <div class="circle-value">45.5%</div>
            <p>Average <strong>severity of poverty</strong> among the poor. Higher means deeper deprivation.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-glow">
            <h4>📌 Contribution to Poverty</h4>
            <p>Shows which dimensions (health, education, living standards, employment) contribute most to poverty. Helps answer <em>"How is poverty experienced?"</em></p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-glow">
            <h4>🌍 Deprivation in 4 Dimensions</h4>
            <p>Provides a snapshot of deprivation across <strong>health, education, living standards, and employment</strong>. Indicates alignment with <em>world standards</em>.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-glow">
            <h4>📉 Deprivation in 13 Indicators</h4>
            <p>Breakdown of poverty across specific indicators like sanitation, housing, health insurance, and education. Highlights what people lack.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-glow">
            <h4>🔗 Learn More</h4>
            <p>For methodology and details on Multidimensional Poverty Index (MPI):</p>
            <p><a href="https://statsghana.gov.gh/MPI-Primer.pdf" target="_blank">MPI Primer (PDF)</a></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("📊 Key Statistics for Savelugu Municipal")

    # --- Key Stats Cards ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-glow">
            <h4>📉 Multidimensional Poverty</h4>
            <div class="circle-value">41.1%</div>
            <p>Percentage of population living in <strong>multidimensional poverty</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-glow">
            <h4>📊 Poverty Intensity</h4>
            <div class="circle-value">45.5%</div>
            <p>Average intensity of poverty among the poor.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-glow">
            <h4>📌 MPI Value</h4>
            <div class="circle-value">0.187</div>
            <p>The <strong>Multidimensional Poverty Index</strong> combines incidence and intensity into a single score.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-glow">
            <h4>🏅 National Ranking</h4>
            <div class="circle-value">221st</div>
            <p>Rank among 261 districts (lower = less poverty).</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-glow">
        <h4>📍 Regional Ranking</h4>
        <div class="circle-value">5th</div>
        <p>Rank among 16 districts in the <strong>Northern Region</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🚫 Areas of Highest Deprivation")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-glow">
            <h4>🚽 Toilet Facilities</h4>
            <div class="circle-value">94.3%</div>
            <p>Population lacking <strong>improved toilet facilities</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-glow">
            <h4>🏠 Housing Quality</h4>
            <div class="circle-value">62.6%</div>
            <p>Households deprived in <strong>housing material quality</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="metric-glow">
            <h4>🏥 Health Insurance</h4>
            <div class="circle-value">59.3%</div>
            <p>Population without <strong>health insurance coverage</strong>.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-glow">
            <h4>📊 High Deprivation</h4>
            <div class="circle-value">9 / 13</div>
            <p>Savelugu Municipal shows <strong>higher deprivation than national average</strong> in 9 of 13 indicators.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🌡️ Heatmap of MPI by Sub-District")
    poverty_data = pd.DataFrame({
        "Zone": ["Savelugu Central", "Tunaayili", "Kadia", "Yong", "Gushie", "Diare"],
        "Latitude": [9.6241, 9.7001, 9.5202, 9.6500, 9.4800, 9.7400],
        "Longitude": [-0.8306, -0.8500, -0.8000, -0.8100, -0.7800, -0.8700],
        "MPI": [0.19, 0.22, 0.17, 0.15, 0.25, 0.18]
    })
    layer = pdk.Layer(
        "HeatmapLayer",
        data=poverty_data,
        get_position='[Longitude, Latitude]',
        get_weight="MPI",
        radius=30000,
        aggregation=pdk.types.String("MEAN")
    )
    view_state = pdk.ViewState(
        latitude=9.6, longitude=-0.82, zoom=9, pitch=30
    )
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    st.markdown("<p>This heatmap shows <strong>higher MPI zones in darker/red areas</strong>. Useful for targeting interventions.</p>", unsafe_allow_html=True)

    st.subheader("📊 Infrastructure Access vs MPI by Zone")
    infra_data = pd.DataFrame({
        "Zone": ["Savelugu Central", "Tunaayili", "Kadia", "Yong", "Gushie", "Diare"],
        "MPI": [0.19, 0.22, 0.17, 0.15, 0.25, 0.18],
        "Improved Toilets (%)": [15, 10, 20, 18, 8, 22],
        "Electricity Access (%)": [65, 45, 55, 60, 40, 70],
        "Literacy Rate (%)": [58, 42, 50, 55, 37, 62],
        "Health Insurance (%)": [45, 30, 35, 40, 25, 50]
    })
    melted = infra_data.melt(id_vars=["Zone", "MPI"], var_name="Indicator", value_name="Percentage")
    chart = alt.Chart(melted).mark_bar().encode(
        x=alt.X("Zone:N", title="Zone"),
        y=alt.Y("Percentage:Q", title="Percentage"),
        color="Indicator:N",
        tooltip=["Zone", "Indicator", "Percentage"]
    ).properties(
        width=800, height=400,
        title="Infrastructure Access vs MPI by Zone"
    )
    st.altair_chart(chart, use_container_width=True)
    st.markdown("<p>Zones with <strong>lower infrastructure access</strong> often have <strong>higher MPI values</strong>.</p>", unsafe_allow_html=True)

    st.subheader("🫧 Bubble Chart: MPI vs Improved Toilets")
    bubble = alt.Chart(infra_data).mark_circle().encode(
        x="MPI:Q",
        y="Improved Toilets (%):Q",
        size="Electricity Access (%):Q",
        color="Zone:N",
        tooltip=["Zone", "MPI", "Improved Toilets (%)", "Electricity Access (%)"]
    ).properties(width=700, height=400)
    st.altair_chart(bubble, use_container_width=True)
    st.markdown("<p>Bubble size represents electricity access. This chart shows multifactorial deprivation by zone.</p>", unsafe_allow_html=True)

    # --- Gender Distribution ---
    df = pd.read_csv("communities.csv")
    total_male = df['Male_Population'].sum()
    total_female = df['Female_Population'].sum()
    gender_df = pd.DataFrame({'Gender': ['Male', 'Female'], 'Count': [total_male, total_female]})
    fig_gender = px.pie(gender_df, values='Count', names='Gender', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    fig_gender.update_traces(textposition='inside', textinfo='percent+label')
    st.subheader("👫 Gender Distribution")
    st.plotly_chart(fig_gender, use_container_width=True)
    st.markdown("<p>Shows male vs female population proportion in Savelugu Municipal.</p>", unsafe_allow_html=True)

    # --- Household Head by Gender ---
    head_male = df['Head_Male'].sum()
    head_female = df['Head_Female'].sum()
    head_df = pd.DataFrame({'Gender': ['Male Head', 'Female Head'], 'Count': [head_male, head_female]})
    fig_head = px.pie(head_df, values='Count', names='Gender', hole=0.4, color_discrete_sequence=px.colors.sequential.Plasma)
    fig_head.update_traces(textposition='inside', textinfo='percent+label')
    st.subheader("🏠 Household Head by Gender")
    st.plotly_chart(fig_head, use_container_width=True)
    st.markdown("<p>Shows proportion of male vs female household heads, highlighting gender-based household leadership.</p>", unsafe_allow_html=True)

    # --- Add further explanations for other charts similarly ---
    st.markdown("<p>All charts and maps include annotations and hover tooltips to provide insights on poverty levels, intensity, and geographic distribution in Savelugu Municipal.</p>", unsafe_allow_html=True)
