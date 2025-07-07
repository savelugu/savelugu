import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import plotly.graph_objects as go
import networkx as nx
import altair as alt

def app():

    # Load datasets
    fertility_age_group = pd.read_csv("./Fertility/fertility1_age_group-183534.csv")  # Update path if needed
    ever_born = pd.read_csv("./Fertility/ever_born.csv")
    survive = pd.read_csv("./Fertility/children_surviving_12-19.csv")  # Update path as needed
    
    
        # Sidebar filters
    st.sidebar.header("📌 Filter Data")
    locality = st.sidebar.multiselect("Select Locality", fertility_age_group["Locality"].unique(), default=fertility_age_group["Locality"].unique())

    # Filtered Data
    filtered_df = fertility_age_group[fertility_age_group["Locality"].isin(locality)]

    # Compute totals per category (for bar chart and heatmap)
    melted_df = filtered_df.melt(
        id_vars=["Education", "Locality"],
        var_name="Age_Group",
        value_name="Count"
    )

    st.title("👶 Number of Children Born in the Last 12 Months")
    
    st.markdown("""
    <style>
        /* Make buttons dark and clean */
        div.stButton > button {
            background-color: #1f1f2e;
            color: white;
            border: 1px solid #444;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #33334d;
            color: #ffcc00;
            border: 1px solid #666;
        }

        .stDownloadButton, .stFormSubmitButton {
            background-color: #1f1f2e !important;
            color: white !important;
            border-radius: 6px;
            font-size: 15px;
            padding: 0.5em 1em;
        }
        .stDownloadButton:hover, .stFormSubmitButton:hover {
            background-color: #33334d !important;
            color: #ffcc00 !important;
        }

        /* Dark-themed tabs */
        .stTabs [role="tablist"] {
            background-color: #111827;
            border: 1px solid #444;
            border-radius: 8px;
            padding: 5px;
        }
        .stTabs [role="tab"] {
            color: #aaa;
            padding: 10px 20px;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1f1f2e;
            color: #ffffff;
            border-radius: 6px;
            border: 1px solid #555;
        }

        /* Darken the data tables */
        .stDataFrame {
            background-color: #1e1e2f;
            color: white;
        }

        /* Optional: Make the whole page a bit darker and cleaner */
        .block-container {
            padding: 2rem;
            background-color: #0f172a;
        }

        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <style>
        /* Base style for each tab */
        [data-baseweb="tab"] {
            background-color: #1f1f1f;
            padding: 10px 20px;
            margin-right: 10px;
            border-radius: 25px; /* pill shape */
            border: 1px solid #444;
            color: #eee;
            font-weight: 500;
            font-size: 15px;
            transition: all 0.3s ease;
        }

        /* Hover effect */
        [data-baseweb="tab"]:hover {
            background-color: #333;
            color: #00f2ff;
            cursor: pointer;
        }

        /* Active/selected tab */
        [aria-selected="true"][data-baseweb="tab"] {
            background-color: #00f2ff !important;
            color: #000 !important;
            font-weight: 700;
            box-shadow: 0 0 10px #00f2ff;
        }

        /* Ensure the label text stays inside and aligned */
        [data-baseweb="tab"] > div {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Age Group & Locality",
        "📈 Education & Locality",
        "🔥 Heatmap of Rural & Urban",
        "📁 Data Table"
    ])
    
    st.markdown("""
        <style>
        /* Selected multiselect tags */
        [data-baseweb="tag"] {
            background-color: #1f77b4 !important;
            color: white !important;
            font-weight: 600;
            border-radius: 6px !important;
        }

        /* Optional: Multiselect border */
        .stMultiSelect > div {
            border: 2px solid #1f77b4 !important;
            border-radius: 8px !important;
        }

        /* Optional: Selectbox border */
        .stSelectbox > div {
            border: 2px solid #1f77b4 !important;
            border-radius: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)


    with tab1:
        st.subheader("📊 Stacked Bar Chart: Education by Age Group")
        fig_stacked = px.bar(
            melted_df,
            x="Age_Group",
            y="Count",
            color="Education",
            barmode="stack",
            facet_col="Locality",
            color_discrete_sequence=px.colors.sequential.Plasma,
            title="Stacked Bar Chart by Age Group & Locality"
        )
        st.plotly_chart(fig_stacked, use_container_width=True)

    with tab2:
        st.subheader("📈 Grouped Bar Chart: Total Education Counts")
        grouped = melted_df.groupby(["Education", "Locality"])["Count"].sum().reset_index()
        fig_grouped = px.bar(
            grouped,
            x="Education",
            y="Count",
            color="Locality",
            barmode="group",
            title="Grouped Bar Chart of Education by Locality"
        )
        fig_grouped.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_grouped, use_container_width=True)

    with tab3:
        st.subheader("🔥 Heatmap: Education vs Age Group")
        for loc in filtered_df["Locality"].unique():
            st.markdown(f"**Locality: {loc}**")
            heat_df = melted_df[melted_df["Locality"] == loc].pivot(index="Education", columns="Age_Group", values="Count").fillna(0)
            fig_heat = px.imshow(
                heat_df,
                text_auto=True,
                labels={"x": "Age Group", "y": "Education", "color": "Count"},
                title=f"Heatmap for {loc}"
            )
            st.plotly_chart(fig_heat, use_container_width=True)

    with tab4:
        st.subheader("📁 Raw Data Table")
        st.dataframe(filtered_df)

        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="education_by_age.csv", mime="text/csv")
        
        
        st.title("👩‍🍼 Surviving Children (12–19 Year Old Mothers) – Savelugu Municipal")
        survive.rename(columns={"Savelugu Municipal": "Count"}, inplace=True)

        # --- Compute Metrics ---
        total_rural = survive[survive["Locality"] == "Rural"]["Count"].sum()
        total_urban = survive[survive["Locality"] == "Urban"]["Count"].sum()
        top_rural_edu = survive[survive["Locality"] == "Rural"].sort_values("Count", ascending=False).iloc[0]["Education"]
        top_urban_edu = survive[survive["Locality"] == "Urban"].sort_values("Count", ascending=False).iloc[0]["Education"]

        st.markdown("""
        <style>
        .card-container {{
            display: flex;
            gap: 1rem;
            justify-content: space-between;
            margin-bottom: 2rem;
        }}
        .card {{
            flex: 1;
            padding: 1rem;
            background: dark;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .card h3 {{
            color: #007bff;
            margin-bottom: 0.5rem;
        }}
        </style>
        <div class="card-container">
            <div class="card">
                <h3>🌾 Total Rural Births</h3>
                <p><strong>{:,}</strong></p>
            </div>
            <div class="card">
                <h3>🏙️ Total Urban Births</h3>
                <p><strong>{:,}</strong></p>
            </div>
            <div class="card">
                <h3>🥇 Top Rural Education</h3>
                <p><strong>{}</strong></p>
            </div>
            <div class="card">
                <h3>🥇 Top Urban Education</h3>
                <p><strong>{}</strong></p>
            </div>
        </div>
        """.format(total_rural, total_urban, top_rural_edu, top_urban_edu), unsafe_allow_html=True)

        
    

        # --- Bar Chart ---
        st.subheader("📊 Surviving Children by Education and Locality")
        fig_bar = px.bar(
            survive, x="Education", y="Count", color="Locality", barmode="group", text="Count",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )
        fig_bar.update_layout(xaxis_tickangle=-40, height=500)
        st.plotly_chart(fig_bar, use_container_width=True)

        # --- Pie Charts ---
        st.subheader("🥧 Proportion by Locality")
        



        import plotly.io as pio

        # Set default theme to 'plotly_dark' for dark background
        pio.templates.default = "plotly_dark"

        col1, col2 = st.columns(2)

        with col1:
            fig_rural = px.pie(
                survive[survive["Locality"] == "Rural"],
                names="Education",
                values="Count",
                title="🌾 Rural Distribution",
                hole=0.4,
            
                color_discrete_sequence=px.colors.sequential.Plasma # good for dark themes
            )
            fig_rural.update_layout(
                title_font_color="white",
                legend_font_color="white",
                paper_bgcolor="rgba(0,0,0,0)",  # transparent background
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_rural, use_container_width=True)

        with col2:
            fig_urban = px.pie(
                survive[survive["Locality"] == "Urban"],
                names="Education",
                values="Count",
                title="🏙️ Urban Distribution",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            fig_urban.update_layout(
                title_font_color="white",
                legend_font_color="white",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_urban, use_container_width=True)
            
            
        st.title("👶 Children Ever Born by Education, Locality & Age Group")

        # --- Melt the data for visualization ---
        df_long = ever_born.melt(id_vars=["Education", "Locality"], var_name="Age_Group", value_name="Count")

        # --- Metrics Summary ---
        total_rural = ever_born[ever_born["Locality"] == "Rural"].iloc[:, 2:].sum().sum()
        total_urban = ever_born[ever_born["Locality"] == "Urban"].iloc[:, 2:].sum().sum()

        top_rural_edu = ever_born[ever_born["Locality"] == "Rural"].set_index("Education").iloc[:, 1:].sum(axis=1).idxmax()
        top_urban_edu = ever_born[ever_born["Locality"] == "Urban"].set_index("Education").iloc[:, 1:].sum(axis=1).idxmax()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🌾 Total Rural", f"{total_rural:,}")
        col2.metric("🏙️ Total Urban", f"{total_urban:,}")
        col3.metric("🥇 Top Rural Edu.", top_rural_edu)
        col4.metric("🥇 Top Urban Edu.", top_urban_edu)

        # --- Chart Mode Selection ---
        chart_mode = st.radio("Chart Type", ["Grouped", "Stacked"], horizontal=True)
        barmode = "group" if chart_mode == "Grouped" else "stack"

        # --- Bar Chart ---
        # --- Horizontal Bar Chart by Locality ---
        fig = px.bar(
            df_long,
            x="Count",
            y="Age_Group",
            color="Education",
            facet_col="Locality",
            barmode="group",  # or "stack" if you want stacking
            orientation="h",
            color_discrete_sequence=px.colors.sequential.Plasma,
            title="📊 Children Ever Born by Education & Age (Faceted by Locality)"
        )

        # Optional: Improve layout spacing and readability
        fig.update_layout(
            height=600,
            margin=dict(t=60, l=80, r=60),
            font=dict(size=12)
        )

        st.plotly_chart(fig, use_container_width=True)


        # --- Age Slice: Age Group 30–34 ---
        st.markdown("### 🥧 Age Group 30–34 Distribution")

        age_slice = df_long[df_long["Age_Group"] == "30-34"]
        # Get unique education levels and assign consistent colors
        edu_levels = age_slice["Education"].unique()
        color_map = px.colors.sequential.Plasma[:len(edu_levels)]  # Use Plasma scale

        # Map education levels to colors
        color_dict = dict(zip(sorted(edu_levels), color_map))

        col1, col2 = st.columns(2)

        with col1:
            rural_bar = age_slice[age_slice["Locality"] == "Rural"]
            fig_r = px.bar(
                rural_bar,
                x="Count",
                y="Education",
                orientation="h",
                title="🌾 Rural",
                color="Education",
                color_discrete_map=color_dict
            )
            fig_r.update_layout(yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig_r, use_container_width=True)

        with col2:
            urban_bar = age_slice[age_slice["Locality"] == "Urban"]
            fig_u = px.bar(
                urban_bar,
                x="Count",
                y="Education",
                orientation="h",
                title="🏙️ Urban",
                color="Education",
                color_discrete_map=color_dict
            )
            fig_u.update_layout(yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig_u, use_container_width=True)
        
        





if __name__ == "__main__":
    app()  


    



