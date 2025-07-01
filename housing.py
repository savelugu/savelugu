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
    df = pd.read_csv("./Housing/Bathing2021_20250629-075522.csv")  # Update path if needed
    df_coking = pd.read_csv("./Housing/Cooking_Space_20250629-075747.csv")
    df_fuel = pd.read_csv("./Housing/Fuel_Source_20250629-075637.csv")  # Update path as needed
    df_light = pd.read_csv("./Housing/Light_Source_20250629-080905.csv")  # Adjust path as needed
    df_restype = pd.read_csv("./Housing/Restype_20250629-083234.csv")  # Replace with your actual path if needed
    df_tenure = pd.read_csv("./Housing/Tenure2021_20250629-083015.csv")
    df_dwelling = pd.read_csv("./Housing/Rooms1_20250629-081846.csv")
    sleeping_df = pd.read_csv("./Housing/Rooms2_20250629-082913.csv")
    type_dwelling=pd.read_csv("./Housing/Household_Structures_by_Typeofdwelling,_Locality and Geographic_Area.csv")
    floor_material=pd.read_csv("./Housing/Households_by_Floor_Material_Locality_and_Geographic_Area.csv")
    wall_material=pd.read_csv("./Housing/Households_by_Wall_Material_Locality_and_Geographic_Area.csv")
    roof_material=pd.read_csv("./Housing/Households_by_Roof_Material_Locality_and_Geographic_Area.csv")
    source_water=pd.read_csv("./Housing/Household_Water_Source.csv")



    # --- CSS Animation for the Header ---
    css_animation = """
        <style>
        @keyframes bump {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .bumping-text {
            display: inline-block;
            animation: bump 1s infinite;
            font-size: 42px;
            color: #15FFFF;
            text-align: center;
            width: 100%;
        }
        
        /* Glow effect for metric cards */
    .metric-glow {
        padding: 1rem;
        margin: 0.5rem;
        border-radius: 12px;
        background: #111;
        box-shadow: 0 0 15px rgba(0, 153, 255, 0.6);
        transition: 0.3s ease-in-out;
    }

    .metric-glow:hover {
        box-shadow: 0 0 25px rgba(0, 153, 255, 1);
        transform: scale(1.02);
    }

    /* Center and style headings */
    .bumping-text {
        color: #00ccff;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
        </style>
    """
    st.markdown(css_animation, unsafe_allow_html=True)
    st.markdown("<h1 class='bumping-text'>🏠 Housing Facilities Analysis - Savelugu Municipal</h1>", unsafe_allow_html=True)
    
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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🛁 Bathing Facilities", "🍳 Cooking Spaces","🔥 Cooking Fuel","💡 Lighting Sources","🏠 Housing Unit Types", "🛖Tenure","🏠Room Dwelling"])

    with tab1:
        st.header("🛁 Bathing Facilities")

        tab_b1, tab_b2, tab_b3, tab_b4, tab_b5, tab_b6, tab_b7 = st.tabs([
            "📊 Bar Chart", "📥 Download + Table", "📊 Grouped Bar",
            "🌞 Sunburst", "🥧 Pie Charts", "🌳 Treemap", "🔥 Heatmap"
        ])

        with tab_b1:
            fig = px.bar(
                df,
                x="Bathing_Facility",
                y="Savelugu Municipal",
                color="Locality",
                barmode="group",
                title="Bathing Facilities by Locality",
                text="Savelugu Municipal"
            )
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

        with tab_b2:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", data=csv, file_name="savelugu_bathing_facilities.csv", mime='text/csv')
            st.dataframe(df)

        with tab_b3:
            fig_grouped = px.bar(
                df,
                x="Bathing_Facility",
                y="Savelugu Municipal",
                color="Locality",
                barmode="group",
                title="Grouped Comparison of Bathing Facilities (Urban vs Rural)",
                text="Savelugu Municipal"
            )
            fig_grouped.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_grouped, use_container_width=True)

        with tab_b4:
            fig_sunburst = px.sunburst(
                df,
                path=["Locality", "Bathing_Facility"],
                values="Savelugu Municipal",
                title="Sunburst of Bathing Facilities by Locality"
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)

        with tab_b5:
            col1, col2 = st.columns(2)
            with col1:
                fig_rural_pie = px.pie(
                    df[df["Locality"] == "Rural"],
                    names="Bathing_Facility",
                    values="Savelugu Municipal",
                    title="Rural Facility Distribution"
                )
                st.plotly_chart(fig_rural_pie, use_container_width=True)

            with col2:
                fig_urban_pie = px.pie(
                    df[df["Locality"] == "Urban"],
                    names="Bathing_Facility",
                    values="Savelugu Municipal",
                    title="Urban Facility Distribution"
                )
                st.plotly_chart(fig_urban_pie, use_container_width=True)

        with tab_b6:
            fig_tree = px.treemap(
                df,
                path=["Locality", "Bathing_Facility"],
                values="Savelugu Municipal",
                title="Treemap of Bathing Facility Usage"
            )
            st.plotly_chart(fig_tree, use_container_width=True)

        with tab_b7:
            pivot_df = df.pivot(index="Bathing_Facility", columns="Locality", values="Savelugu Municipal").fillna(0)
            fig_heatmap = px.imshow(
                pivot_df,
                labels=dict(x="Locality", y="Facility", color="Savelugu Municipal"),
                title="Heatmap of Bathing Facility Usage",
                text_auto=True
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

    with tab2:
        st.header("🍳 Cooking Spaces")

        tab_c1, tab_c2, tab_c3, tab_c4, tab_c5, tab_c6 = st.tabs([
            "📊 Grouped Bar", "🥧 Pie Charts", "🌳 Treemap",
            "🌞 Sunburst", "🔥 Heatmap", "📥 Table + Download"
        ])

        with tab_c1:
            fig_grouped = px.bar(
                df_coking,
                x="Cooking_Space",
                y="Savelugu Municipal",
                color="Locality",
                barmode="group",
                text="Savelugu Municipal",
                title="Grouped Comparison of Cooking Spaces (Urban vs Rural)"
            )
            fig_grouped.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_grouped, use_container_width=True)

        with tab_c2:
            col1, col2 = st.columns(2)
            with col1:
                fig_rural_pie = px.pie(
                    df_coking[df_coking["Locality"] == "Rural"],
                    names="Cooking_Space",
                    values="Savelugu Municipal",
                    title="Rural Cooking Spaces"
                )
                st.plotly_chart(fig_rural_pie, use_container_width=True)

            with col2:
                fig_urban_pie = px.pie(
                    df_coking[df_coking["Locality"] == "Urban"],
                    names="Cooking_Space",
                    values="Savelugu Municipal",
                    title="Urban Cooking Spaces"
                )
                st.plotly_chart(fig_urban_pie, use_container_width=True)

        with tab_c3:
            fig_treemap = px.treemap(
                df_coking,
                path=["Locality", "Cooking_Space"],
                values="Savelugu Municipal",
                title="Treemap of Cooking Space Usage"
            )
            st.plotly_chart(fig_treemap, use_container_width=True)

        with tab_c4:
            fig_sunburst = px.sunburst(
                df_coking,
                path=["Locality", "Cooking_Space"],
                values="Savelugu Municipal",
                title="Sunburst of Cooking Space Usage by Locality"
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)

        with tab_c5:
            pivot_df = df_coking.pivot(index="Cooking_Space", columns="Locality", values="Savelugu Municipal").fillna(0)
            fig_heatmap = px.imshow(
                pivot_df,
                labels=dict(x="Locality", y="Cooking_Space", color="Savelugu Municipal"),
                title="Heatmap of Cooking Space Distribution",
                text_auto=True
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

        with tab_c6:
            csv = df_coking.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Cooking Data", data=csv, file_name="savelugu_cooking_spaces.csv", mime='text/csv')
            st.dataframe(df_coking)
            
                # Add this inside tab3
    with tab3:
        st.header("🔥 Cooking Fuel")

        tab_f1, tab_f2, tab_f3, tab_f4, tab_f5, tab_f6 = st.tabs([
            "📊 Grouped Bar", "🥧 Pie Charts", "🌳 Treemap",
            "🌞 Sunburst", "🔥 Heatmap", "📥 Table + Download"
        ])

        with tab_f1:
            fig_fuel = px.bar(
                df_fuel,
                x="Fuel",
                y="Savelugu Municipal",
                color="Locality",
                barmode="group",
                title="Grouped Comparison of Cooking Fuels (Urban vs Rural)",
                text="Savelugu Municipal"
            )
            fig_fuel.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_fuel, use_container_width=True)

        with tab_f2:
            col1, col2 = st.columns(2)
            with col1:
                fig_rural = px.pie(
                    df_fuel[df_fuel["Locality"] == "Rural"],
                    names="Fuel",
                    values="Savelugu Municipal",
                    title="Rural Cooking Fuel Usage"
                )
                st.plotly_chart(fig_rural, use_container_width=True)
            with col2:
                fig_urban = px.pie(
                    df_fuel[df_fuel["Locality"] == "Urban"],
                    names="Fuel",
                    values="Savelugu Municipal",
                    title="Urban Cooking Fuel Usage"
                )
                st.plotly_chart(fig_urban, use_container_width=True)

        with tab_f3:
            fig_tree = px.treemap(
                df_fuel,
                path=["Locality", "Fuel"],
                values="Savelugu Municipal",
                title="Treemap of Cooking Fuel Usage"
            )
            st.plotly_chart(fig_tree, use_container_width=True)

        with tab_f4:
            fig_sunburst = px.sunburst(
                df_fuel,
                path=["Locality", "Fuel"],
                values="Savelugu Municipal",
                title="Sunburst of Cooking Fuel by Locality"
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)

        with tab_f5:
            pivot_df = df_fuel.pivot(index="Fuel", columns="Locality", values="Savelugu Municipal").fillna(0)
            fig_heatmap = px.imshow(
                pivot_df,
                labels=dict(x="Locality", y="Fuel", color="Savelugu Municipal"),
                title="Heatmap of Cooking Fuel Usage",
                text_auto=True
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

        with tab_f6:
            csv = df_fuel.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Cooking Fuel CSV", data=csv, file_name="savelugu_cooking_fuel.csv", mime='text/csv')
            st.dataframe(df_fuel)
            
    with tab4:
        st.header("💡 Lighting Sources")

        tab_l1, tab_l2, tab_l3, tab_l4, tab_l5, tab_l6 = st.tabs([
            "📊 Grouped Bar", "🥧 Pie Charts", "🌳 Treemap",
            "🌞 Sunburst", "🔥 Heatmap", "📥 Table + Download"
        ])

        with tab_l1:
            fig_light = px.bar(
                df_light,
                x="Light",
                y="Savelugu Municipal",
                color="Locality",
                barmode="group",
                title="Grouped Comparison of Lighting Sources (Urban vs Rural)",
                text="Savelugu Municipal"
            )
            fig_light.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_light, use_container_width=True)

        with tab_l2:
            col1, col2 = st.columns(2)
            with col1:
                fig_rural = px.pie(
                    df_light[df_light["Locality"] == "Rural"],
                    names="Light",
                    values="Savelugu Municipal",
                    title="Rural Lighting Sources"
                )
                st.plotly_chart(fig_rural, use_container_width=True)
            with col2:
                fig_urban = px.pie(
                    df_light[df_light["Locality"] == "Urban"],
                    names="Light",
                    values="Savelugu Municipal",
                    title="Urban Lighting Sources"
                )
                st.plotly_chart(fig_urban, use_container_width=True)
                
        df_light = df_light.dropna(subset=["Light"])
        df_light = df_light[df_light["Light"].str.strip() != ""]


        with tab_l3:
            fig_tree = px.treemap(
            df_light.dropna(subset=["Light"]),
            path=["Locality", "Light"],
            values="Savelugu Municipal",
            title="Treemap of Lighting Sources"
            )

            st.plotly_chart(fig_tree, use_container_width=True)

        with tab_l4:
            fig_sunburst = px.sunburst(
                df_light,
                path=["Locality", "Light"],
                values="Savelugu Municipal",
                title="Sunburst of Lighting Sources by Locality"
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)

        with tab_l5:
            pivot_df = df_light.pivot(index="Light", columns="Locality", values="Savelugu Municipal").fillna(0)
            fig_heatmap = px.imshow(
                pivot_df,
                labels=dict(x="Locality", y="Savelugu Municipal", color="Savelugu Municipal"),
                title="Heatmap of Lighting Usage",
                text_auto=True
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

        with tab_l6:
            csv = df_light.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Lighting Data CSV", data=csv, file_name="savelugu_lighting.csv", mime='text/csv')
            st.dataframe(df_light)
            
            
            
    with tab5:
        st.subheader("🏠 Housing Unit Types in Savelugu Municipal") 
        
        # Compute totals for Restype across Rural and Urban
        rural_restype = df_restype[df_restype["Locality"] == "Rural"][["Restype", "Savelugu Municipal"]]
        urban_restype = df_restype[df_restype["Locality"] == "Urban"][["Restype", "Savelugu Municipal"]]

        # Layout with two columns
        tab1, tab2 = st.columns(2)

        with tab1:
            st.markdown("<h3 style='color: #20C997;'>🏡 Rural Housing Unit Types</h3>", unsafe_allow_html=True)
    
            fig_rural = px.pie(
            rural_restype,
            values="Savelugu Municipal",
            names="Restype",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
            )

            fig_rural.update_traces(textposition='inside', textinfo='percent+label', pull=[0.02]*len(rural_restype))
            fig_rural.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#FFFFFF"
            )
            st.plotly_chart(fig_rural, use_container_width=True)

        with tab2:
            st.markdown("<h3 style='color: #F39C12;'>🏙️ Urban Housing Unit Types</h3>", unsafe_allow_html=True)

            fig_urban = px.pie(
            urban_restype,
            values="Savelugu Municipal",
            names="Restype",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Turbo
            )

                
            fig_urban.update_traces(textposition='inside', textinfo='percent+label', pull=[0.02]*len(urban_restype))
            fig_urban.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#FFFFFF"
                )
            st.plotly_chart(fig_urban, use_container_width=True)

        st.divider()
        
        
        
    with tab6:    

        st.markdown("## 🏘️ Tenure Arrangement in Savelugu Municipal")

        # --- TABS ---
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Tenure By Locality ", "🥧 Tenure Arrangement", "🌳 Tenure Type", "🌞 Tenure By Locality", "🔥 Heatmap of Tenure Types by Locality"
        ])

        with tab1:
            fig = px.bar(
                df_tenure,
                x="Tenure_Arrangement",
                y="Savelugu Municipal",
                color="Locality",
                barmode="group",
                text="Savelugu Municipal",
                title="Grouped Bar: Tenure by Locality",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            tab1, tab2 = st.columns(2)
            with tab1:
                st.markdown("### 🌾 Rural")
                rural_df = df_tenure[df_tenure["Locality"] == "Rural"].sort_values(by="Savelugu Municipal")
                fig_rural_bar = px.bar(
                    rural_df,
                    x="Savelugu Municipal",
                    y="Tenure_Arrangement",
                    orientation='h',
                    title="Tenure by Locality - Rural",
                    color="Tenure_Arrangement",
                    text="Savelugu Municipal",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_rural_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_rural_bar, use_container_width=True)

            with tab2:
                st.markdown("### 🏙️ Urban")
                urban_df = df_tenure[df_tenure["Locality"] == "Urban"].sort_values(by="Savelugu Municipal")
                fig_urban_bar = px.bar(
                    urban_df,
                    x="Savelugu Municipal",
                    y="Tenure_Arrangement",
                    orientation='h',
                    title="Tenure by Locality - Urban",
                    color="Tenure_Arrangement",
                    text="Savelugu Municipal",
                    color_discrete_sequence=px.colors.qualitative.Vivid
                )
                fig_urban_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_urban_bar, use_container_width=True)

        with tab3:
            fig_tree = px.treemap(
                df_tenure,
                path=["Locality", "Tenure_Arrangement"],
                values="Savelugu Municipal",
                title="Treemap of Tenure Types",
                color_discrete_sequence=px.colors.sequential.Tealgrn
            )
            st.plotly_chart(fig_tree, use_container_width=True)

        with tab4:
            fig_sunburst = px.sunburst(
                df_tenure,
                path=["Locality", "Tenure_Arrangement"],
                values="Savelugu Municipal",
                title="Sunburst of Tenure Types by Locality",
                color_discrete_sequence=px.colors.sequential.Mint
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)

        with tab5:
            pivot_df = df_tenure.pivot(index="Tenure_Arrangement", columns="Locality", values="Savelugu Municipal").fillna(0)
            fig_heatmap = px.imshow(
                pivot_df,
                labels=dict(x="Locality", y="Tenure Arrangement", color="Residents"),
                title="Heatmap of Tenure Types by Locality",
                text_auto=True,
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            
            # Create DataFrame
    with tab7:
        st.title("🏘️ Rooms in Dwelling and Sleeping by Locality - Savelugu Municipal")
        tab1, tab2=st.columns(2)
        with tab1:
            st.subheader("🏘️ Rooms in Dwelling by Locality - Savelugu Municipal")
            # Horizontal grouped bar chart
            fig = px.bar(
                df_dwelling,
                x="Savelugu Municipal",
                y="Rooms",
                color="Locality",
                barmode="group",
                orientation='h',
                title="Distribution of Rooms by Locality in Savelugu Municipal",
                text="Savelugu Municipal",
                labels={"Savelugu Municipal": "Number of Dwellings"}
            )

            fig.update_layout(yaxis={'categoryorder': 'total ascending'})

            # Display chart
            st.plotly_chart(fig)
            
        with tab2:
            st.subheader("🛏️ Sleeping Rooms in Dwelling by Locality - Savelugu Municipal")
            # Plot horizontal grouped bar chart
            fig_sleeping = px.bar(
                sleeping_df,
                x="Savelugu Municipal",
                y="Rooms",
                color="Locality",
                barmode="group",
                orientation='h',
                title="Sleeping Rooms in Dwelling by Rooms and Locality (Savelugu Municipal)",
                text="Savelugu Municipal",
                labels={"Savelugu Municipal": "Number of Sleeping Rooms"}
            )

            fig_sleeping.update_layout(yaxis={'categoryorder': 'total ascending'})

            # Display chart
            st.plotly_chart(fig_sleeping)
            


        # Floor material data
        # Data: Floor Material by Locality
        # Data
    



    

        # --- Create Tabs ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🛖 Floor Material", 
        "🏠 Roof Material", 
        "🧱 Wall Material", 
        "🏡 Type of Dwelling",
        "🏡 Water Source"
    ])

    # === TAB 1: Floor Material Radar ===
    with tab1:
        st.subheader("🪵 Floor Materials Metrics – ")
        # Pivot to wide format
        floor_material_wide = floor_material.pivot(
            index="Floor_Material",
            columns="Locality",
            values="Savelugu Municipal"
        ).reset_index()
        floor_material_wide.columns.name = None
        floor_material_wide.columns = ["Floor_Material", "Rural", "Urban"]

        # Prepare radar data
        categories = floor_material_wide["Floor_Material"].tolist()
        rural = floor_material_wide["Rural"].tolist()
        urban = floor_material_wide["Urban"].tolist()
        categories += [categories[0]]
        rural += [rural[0]]
        urban += [urban[0]]

        # === METRICS ===
        total_rural = floor_material_wide["Rural"].sum()
        total_urban = floor_material_wide["Urban"].sum()
        total = total_rural + total_urban

        # Most common floor material
        floor_material_wide["Total"] = floor_material_wide["Rural"] + floor_material_wide["Urban"]
        most_common = floor_material_wide.loc[floor_material_wide["Total"].idxmax()]["Floor_Material"]
        most_common_count = floor_material_wide["Total"].max()

        # Percentage using Cement/Concrete
        cement_row = floor_material_wide[floor_material_wide["Floor_Material"].str.contains("Cement|Concrete", case=False)]
        cement_pct = (cement_row["Total"].values[0] / total * 100) if not cement_row.empty else 0

        # Percentage using Earth/Mud
        mud_row = floor_material_wide[floor_material_wide["Floor_Material"].str.contains("Earth|Mud", case=False)]
        mud_pct = (mud_row["Total"].values[0] / total * 100) if not mud_row.empty else 0

        # === DISPLAY METRIC CARDS ===
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏡 Rural Floor Dwellings", f"{total_rural:,}")
        with col2:
            st.metric("🏙️ Urban Floor Dwellings", f"{total_urban:,}")
        with col3:
            st.metric("🏆 Most Common Floor", most_common)

        col4, col5 = st.columns(2)
        with col4:
            st.metric("🧱 Cement/Concrete", f"{cement_pct:.1f}%", help="Usage across all dwellings")
        with col5:
            st.metric("🪨 Earth/Mud", f"{mud_pct:.1f}%", help="Usage across all dwellings")

        st.markdown("---")

        # === CHART ===
        st.title("🪵 Floor Materials by Locality – Radar View")
        st.markdown("Visual comparison of rural and urban housing floor types in Savelugu Municipal.")

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=rural,
            theta=categories,
            mode='lines+markers',
            name='Rural',
            line=dict(color='lime', width=3),
            marker=dict(color='lime', size=6)
        ))
        fig.add_trace(go.Scatterpolar(
            r=urban,
            theta=categories,
            mode='lines+markers',
            name='Urban',
            line=dict(color='cyan', width=3),
            marker=dict(color='cyan', size=6)
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='black',
                radialaxis=dict(visible=True, gridcolor='gray', linecolor='white',
                                tickfont=dict(color='white', size=11)),
                angularaxis=dict(tickfont=dict(color='white', size=11), gridcolor='gray', linecolor='white')
            ),
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white', size=13),
            legend=dict(orientation="h", y=-0.15, font=dict(color='white')),
            margin=dict(l=40, r=40, t=40, b=80),
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)


    # === TAB 2: Roof Material Horizontal Grouped Bar ===
    with tab2:
        st.subheader("🏚️ Roof Material Metrics – ")
                # --- Metrics ---
        # --- Pivot first ---
        roof_material_wide = roof_material.pivot(
            index="Roof_Material",
            columns="Locality",
            values="Savelugu Municipal"
        ).reset_index()
        roof_material_wide.columns.name = None
        roof_material_wide.columns = ["Roof_Material", "Rural", "Urban"]

        # --- Metrics ---
        total_rural = roof_material_wide["Rural"].sum()
        total_urban = roof_material_wide["Urban"].sum()
        total = total_rural + total_urban

        roof_material_wide["Total"] = roof_material_wide["Rural"] + roof_material_wide["Urban"]

        # Most common roof material
        most_common = roof_material_wide.loc[roof_material_wide["Total"].idxmax()]["Roof_Material"]
        most_common_count = roof_material_wide["Total"].max()

        # % using Metal Sheet/Slate/Asbestos
        metal_row = roof_material_wide[roof_material_wide["Roof_Material"].str.contains("Metal", case=False)]
        metal_pct = (metal_row["Total"].values[0] / total * 100) if not metal_row.empty else 0

        # % using Palm Leaves/Thatch/Raffia
        thatch_row = roof_material_wide[roof_material_wide["Roof_Material"].str.contains("Thatch|Palm", case=False)]
        thatch_pct = (thatch_row["Total"].values[0] / total * 100) if not thatch_row.empty else 0

        # --- Display Metrics as Cards ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏚️ Rural Roof Dwellings", f"{total_rural:,}")
        with col2:
            st.metric("🏙️ Urban Roof Dwellings", f"{total_urban:,}")
        with col3:
            st.metric("🏆 Most Common Roof", most_common)

        col4, col5 = st.columns(2)
        with col4:
            st.metric("🧱 Metal Sheet/Slate", f"{metal_pct:.1f}%", help="Usage across all dwellings")
        with col5:
            st.metric("🌴 Thatch/Palm/Raffia", f"{thatch_pct:.1f}%", help="Usage across all dwellings")

        st.markdown("---")

        # --- Melt for chart
        df_melted = roof_material_wide.melt(id_vars="Roof_Material", value_vars=["Rural", "Urban"],
                                            var_name="Locality", value_name="Count")

        # --- Plot
        st.title("🏠 Roof Material by Locality – Savelugu Municipal")
        st.markdown("### Comparison of Urban and Rural Roof Types")

        fig = px.bar(
            df_melted,
            x="Count",
            y="Roof_Material",
            color="Locality",
            orientation="h",
            barmode="group",
            text="Count",
            color_discrete_map={"Rural": "green", "Urban": "blue"},
            labels={"Roof_Material": "Roof Type"}
        )
        fig.update_layout(
            yaxis=dict(title="", tickfont=dict(size=12)),
            xaxis=dict(title="Number of Dwellings", tickfont=dict(size=12)),
            legend=dict(title="Locality", orientation="h", y=-0.2),
            margin=dict(l=40, r=40, t=40, b=60),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        # === TAB 3: Wall Material Stacked Bar ===
    with tab3:
        wall_material_wide = wall_material.pivot(
            index="Wall_Material",
            columns="Locality",
            values="Savelugu Municipal"
        ).reset_index()
        wall_material_wide.columns.name = None
        wall_material_wide.columns = ["Wall_Material", "Rural", "Urban"]

        df_melted = wall_material_wide.melt(id_vars="Wall_Material", value_vars=["Rural", "Urban"],
                                            var_name="Locality", value_name="Count")

        st.title("🧱 Wall Material by Locality – Savelugu Municipal")
        st.markdown("### Stacked Bar Chart of Urban vs Rural Distribution")
        fig = px.bar(df_melted, x="Wall_Material", y="Count", color="Locality", text="Count",
                    barmode="stack", color_discrete_map={"Rural": "#00cc96", "Urban": "#636efa"},
                    labels={"Wall_Material": "Wall Type", "Count": "Number of Dwellings"})
        fig.update_layout(
            xaxis_tickangle=-30,
            yaxis=dict(title="Total Dwellings"),
            xaxis=dict(title="Wall Material", tickfont=dict(size=11)),
            legend=dict(title="Locality", orientation="h", y=-0.2),
            margin=dict(l=30, r=30, t=40, b=80),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
                # --- Metrics ---
        total_rural = wall_material_wide["Rural"].sum()
        total_urban = wall_material_wide["Urban"].sum()
        total = total_rural + total_urban

        # Add total column
        wall_material_wide["Total"] = wall_material_wide["Rural"] + wall_material_wide["Urban"]

        # Most common wall material
        most_common = wall_material_wide.loc[wall_material_wide["Total"].idxmax()]["Wall_Material"]
        most_common_count = wall_material_wide["Total"].max()

        # Percentage using mud bricks/earth
        mud_row = wall_material_wide[wall_material_wide["Wall_Material"].str.contains("Mud bricks", case=False)]
        if not mud_row.empty:
            mud_total = mud_row["Total"].values[0]
            mud_pct = (mud_total / total) * 100
        else:
            mud_total = 0
            mud_pct = 0

        # Percentage using cement blocks/concrete
        cement_row = wall_material_wide[wall_material_wide["Wall_Material"].str.contains("Cement", case=False)]
        if not cement_row.empty:
            cement_total = cement_row["Total"].values[0]
            cement_pct = (cement_total / total) * 100
        else:
            cement_total = 0
            cement_pct = 0

        # --- Display Metrics as Cards ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏡 Rural Dwellings", f"{total_rural:,}")
        with col2:
            st.metric("🏙️ Urban Dwellings", f"{total_urban:,}")
        with col3:
            st.metric("🏆 Most Common Material", most_common)

        col4, col5 = st.columns(2)
        with col4:
            st.metric("🧱 Mud Bricks/Earth", f"{mud_pct:.1f}%", help="Usage across all dwellings")
        with col5:
            st.metric("🏗️ Cement Blocks/Concrete", f"{cement_pct:.1f}%", help="Usage across all dwellings")

        st.markdown("---")  # separator before chart


    # === TAB 4: Type of Dwelling 100% Stacked Bar ===
    with tab4:
        type_dwelling_wide = type_dwelling.pivot(
            index="Typeofdwelling",
            columns="Locality",
            values="Savelugu Municipal"
        ).reset_index()
        type_dwelling_wide.columns.name = None
        type_dwelling_wide.columns = ["Typeofdwelling", "Rural", "Urban"]

        type_dwelling_wide["Total"] = type_dwelling_wide["Rural"] + type_dwelling_wide["Urban"]
        type_dwelling_wide["Rural %"] = (type_dwelling_wide["Rural"] / type_dwelling_wide["Total"] * 100).fillna(0)
        type_dwelling_wide["Urban %"] = (type_dwelling_wide["Urban"] / type_dwelling_wide["Total"] * 100).fillna(0)

        df_melted = type_dwelling_wide.melt(id_vars="Typeofdwelling", value_vars=["Rural %", "Urban %"],
                                            var_name="Locality", value_name="Percentage")
        df_melted["Locality"] = df_melted["Locality"].str.replace(" %", "")

        st.title("🏡 Type of Dwelling – Proportional Chart by Locality")
        st.markdown("### 100% Stacked Bar Chart for Rural vs Urban Distribution")
        fig = px.bar(df_melted, x="Typeofdwelling", y="Percentage", color="Locality",
                    text=df_melted["Percentage"].round(1).astype(str) + "%",
                    color_discrete_map={"Rural": "#00cc96", "Urban": "#636efa"})
        fig.update_layout(
            barmode="stack",
            yaxis=dict(title="Percentage", range=[0, 100]),
            xaxis=dict(title="", tickangle=-30, tickfont=dict(size=11)),
            legend=dict(orientation="h", y=-0.2),
            margin=dict(l=30, r=30, t=40, b=100),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_traces(textposition='inside', insidetextanchor='middle')
        st.plotly_chart(fig, use_container_width=True)
        
                # --- Metrics ---
        total_rural = type_dwelling_wide["Rural"].sum()
        total_urban = type_dwelling_wide["Urban"].sum()
        total = total_rural + total_urban

        # Most common type overall
        type_dwelling_wide["Total"] = type_dwelling_wide["Rural"] + type_dwelling_wide["Urban"]
        most_common = type_dwelling_wide.loc[type_dwelling_wide["Total"].idxmax()]["Typeofdwelling"]
        most_common_count = type_dwelling_wide["Total"].max()

        # Percentage using compound houses
        compound_row = type_dwelling_wide[type_dwelling_wide["Typeofdwelling"].str.contains("Compound house", case=False)]
        if not compound_row.empty:
            compound_total = compound_row["Total"].values[0]
            compound_pct = (compound_total / total) * 100
        else:
            compound_total = 0
            compound_pct = 0

        # Percentage of urban dwellings that are flats/apartments
        flat_row = type_dwelling_wide[type_dwelling_wide["Typeofdwelling"].str.contains("Flat", case=False)]
        if not flat_row.empty:
            flat_urban = flat_row["Urban"].values[0]
            flat_urban_pct = (flat_urban / total_urban) * 100
        else:
            flat_urban = 0
            flat_urban_pct = 0

        # --- Display Metrics as Cards ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏡 Rural Dwellings", f"{total_rural:,}")
        with col2:
            st.metric("🏙️ Urban Dwellings", f"{total_urban:,}")
        with col3:
            st.metric("🏘️ Most Common Type", most_common)

        col4, col5 = st.columns(2)
        with col4:
            st.metric("🧱 Compound House Usage", f"{compound_pct:.1f}%", help="Across both urban and rural")
        with col5:
            st.metric("🏢 Urban Flats/Apartment", f"{flat_urban_pct:.1f}%", help="Urban dwellings that are flats")
        
        st.markdown("---")  # separator before chart

    with tab5:
        # Pivot to wide format
        df_wide = source_water.pivot(index="Domesticwater", columns="Locality", values="Savelugu Municipal").reset_index()
        df_wide.columns.name = None
        df_wide.columns = ["Water_Source", "Rural", "Urban"]

        # Melt for plotting
        df_melted = df_wide.melt(id_vars="Water_Source", value_vars=["Rural", "Urban"],
                                var_name="Locality", value_name="Count")

        # Plot in Streamlit
        st.title("🚰 Domestic Water Sources by Locality – Savelugu Municipal")
        st.markdown("### Horizontal Grouped Bar Chart")

        fig = px.bar(
            df_melted,
            x="Count",
            y="Water_Source",
            color="Locality",
            orientation="h",
            text="Count",
            barmode="group",
            color_discrete_map={"Rural": "#00cc96", "Urban": "#636efa"},
            labels={"Water_Source": "Water Source Type"}
        )

        fig.update_layout(
            yaxis=dict(title="", tickfont=dict(size=11)),
            xaxis=dict(title="Number of Dwellings"),
            legend=dict(title="Locality", orientation="h", y=-0.2),
            margin=dict(l=40, r=40, t=40, b=60),
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)
        
        
        
        st.markdown("### 📊 Water Source Metrics Overview")

        # Pivot to wide format
        df_wide = source_water.pivot(index="Domesticwater", columns="Locality", values="Savelugu Municipal").reset_index()
        df_wide.columns.name = None
        df_wide.columns = ["Water_Source", "Rural", "Urban"]

        # Metric Calculations
        total_rural = df_wide["Rural"].sum()
        total_urban = df_wide["Urban"].sum()
        total_households = total_rural + total_urban

        # Define source types
        improved_sources = [
            "Pipe-borne inside dwelling",
            "Pipe-borne outside dwelling but on compound",
            "Pipe-borne outside dwelling but in neighbour's house/compound",
            "Public tap/Stand pipe",
            "Borehole/Tube well",
            "Protected well",
            "Protected spring",
            "Rain water"
        ]

        unprotected_sources = [
            "Unprotected well",
            "Unprotected spring",
            "River/Stream",
            "Dugout/Pond/Lake/Dam/Canal"
        ]

        pipe_access = [
            "Pipe-borne inside dwelling",
            "Pipe-borne outside dwelling but on compound",
            "Pipe-borne outside dwelling but in neighbour's house/compound"
        ]

        total_improved = df_wide[df_wide["Water_Source"].isin(improved_sources)][["Rural", "Urban"]].sum().sum()
        total_unprotected = df_wide[df_wide["Water_Source"].isin(unprotected_sources)][["Rural", "Urban"]].sum().sum()

        pipe_df = df_wide[df_wide["Water_Source"].isin(pipe_access)]
        pipe_rural = pipe_df["Rural"].sum()
        pipe_urban = pipe_df["Urban"].sum()

        # Display Metric Cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏡 Rural Households", f"{total_rural:,}")
        with col2:
            st.metric("🏙️ Urban Households", f"{total_urban:,}")
        with col3:
            st.metric("👥 Total Households", f"{total_households:,}")

        col4, col5 = st.columns(2)
        with col4:
            st.metric("💧 Improved Access", f"{(total_improved / total_households * 100):.1f}%", help="Pipe, Borehole, Protected, Rain")
        with col5:
            st.metric("⚠️ Unsafe Sources", f"{(total_unprotected / total_households * 100):.1f}%", help="River, Dugout, Unprotected")

        col6, col7 = st.columns(2)
        with col6:
            st.metric("🔌 Pipe Access – Rural", f"{pipe_rural:,}")
        with col7:
            st.metric("🔌 Pipe Access – Urban", f"{pipe_urban:,}")

        st.markdown("---")  # separator line
        
        
if __name__ == "__main__":
    app()