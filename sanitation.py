import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import plotly.graph_objects as go
import networkx as nx
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

def app():
    
    st.title("🧼 Savelugu Municipal Sanitation Insights")

    # Sidebar chart selector
    st.sidebar.markdown("### 📊 Select Chart to Display")
    chart_option = st.sidebar.selectbox(
        "Choose a visualization:",
        (
            "Defecation Points",
            "Water Sources for Other Domestic Use",
            "Toilet Facilities Overview",
            "Main Source of Drinking Water",
            "Improved and Unimproved Water Services",
            "Storage of Solid Waste",
            "Time Taken to Source Drinking Water",
            "Toilet Facility Breakdown",
            "Levels of Toilet Service",
            "Toilet Facility by Type",
            "Solid Waste Storage Methods"
        )
    )

    # Define chart: Defecation Points
    if chart_option == "Defecation Points":
        st.title("🚽 Defecation Points by Locality – Savelugu Municipal")
        data = {
            "Defecation Point": [
                "Defaecation point", "Defaecation point",
                "In the bush/open field/gutter", "In the bush/open field/gutter",
                "At the beach", "At the beach",
                "In a polythene bag", "In a polythene bag",
                "In a chamber pot", "In a chamber pot"
            ],
            "Locality": ["Rural", "Urban"] * 5,
            "Count": [7263, 7154, 7255, 7055, 2, 76, 1, 2, 5, 21]
        }
        df = pd.DataFrame(data)
        fig = px.bar(
            df, x="Count", y="Defecation Point", color="Locality", orientation="h",
            barmode="group", text="Count",
            title="Distribution of Defecation Methods by Locality",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(color="white", title="Population"),
            yaxis=dict(color="white", title="Defecation Method"),
            height=750
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 🧾 Insight Card
        unsafe_methods = [
            "Defaecation point",
            "In the bush/open field/gutter",
            "At the beach",
            "In a polythene bag"
        ]
        total_unsafe = df[df["Defecation Point"].isin(unsafe_methods)]["Count"].sum()

        with st.container():
            st.markdown(
                f"""
                <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:20px;">
                    <h4 style="color:#f5c518;">🧾 Insight</h4>
                    <p style="color:white; font-size:16px;">
                        🔍 Over <strong>{total_unsafe:,} people</strong> across both rural and urban areas practice <strong>unsafe defecation methods</strong> 
                        (e.g., open defecation, defecation in gutters, bags, or beaches).<br>
                        This raises critical <strong>public health and environmental concerns</strong> in the Savelugu Municipality.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Define chart: Storage of Solid Waste
    elif chart_option == "Storage of Solid Waste":
        st.title("🗑️ Storage of Solid Waste by Locality – Savelugu Municipal")
        data = {
            "Waste Storage": [
                "Standard Waste Receptacles", "Standard Waste Receptacles",
                "Covered standard waste bin", "Covered standard waste bin",
                "Uncovered standard waste bin", "Uncovered standard waste bin",
                "Improvised Waste Receptacles", "Improvised Waste Receptacles",
                "Uncovered container", "Uncovered container",
                "Covered container", "Covered container",
                "Covered/uncovered basket", "Covered/uncovered basket",
                "Disposable Waste Receptacles", "Disposable Waste Receptacles",
                "Polythene bag alone", "Polythene bag alone",
                "Sack", "Sack",
                "Other", "Other",
                "None (No receptacle)", "None (No receptacle)"
            ],
            "Locality": ["Rural", "Urban"] * 12,
            "Population": [
                655, 1589,
                31, 527,
                624, 1062,
                5607, 11550,
                4676, 8533,
                165, 1119,
                766, 1898,
                317, 766,
                132, 314,
                181, 419,
                4, 33,
                1839, 759
            ]
        }
        df = pd.DataFrame(data)
        fig = px.bar(
            df, x="Population", y="Waste Storage", color="Locality",
            facet_col="Locality", orientation="h", text="Population",
            title="Storage of Solid Waste by Locality – Faceted View",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(color="white", title="Population"),
            yaxis=dict(color="white", title="Waste Storage Type"),
            height=750
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 🧾 Insight Card for Solid Waste Storage
        unsafe_storage = [
            "Improvised Waste Receptacles",
            "Uncovered container",
            "Covered/uncovered basket",
            "Polythene bag alone",
            "Sack",
            "None (No receptacle)"
        ]
        total_unsafe = df[df["Waste Storage"].isin(unsafe_storage)]["Population"].sum()

        with st.container():
            st.markdown(
                f"""
                <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:20px;">
                    <h4 style="color:#f5c518;">🧾 Insight</h4>
                    <p style="color:white; font-size:16px;">
                        🧹 Over <strong>{total_unsafe:,} people</strong> across Savelugu rely on <strong>unsafe or improvised waste storage methods</strong> 
                        such as polythene bags, sacks, baskets, or having no receptacles at all.<br>
                        This increases the risk of <strong>uncontrolled waste disposal, pests, and disease outbreaks</strong>.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Define chart: Toilet Facilities Overview
    elif chart_option == "Toilet Facilities Overview":
        st.title("🚻 Toilet Facilities by Locality – Savelugu Municipal")
        data = {
            "Toilet Facility": [
                "Household toilet facility", "Household toilet facility",
                "Improved", "Improved",
                "Unimproved", "Unimproved",
                "No Household toilet facility", "No Household toilet facility",
                "None", "None",
                "Public toilet", "Public toilet"
            ],
            "Locality": [
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban"
            ],
            "Population": [
                1012, 2515,
                987, 2499,
                25, 16,
                7406, 12149,
                7263, 7154,
                143, 4995
            ]
        }
        df = pd.DataFrame(data)
        fig = px.bar(
            df,
            x="Population",
            y="Toilet Facility",
            color="Locality",
            orientation="h",
            barmode="group",
            text="Population",
            title="Distribution of Toilet Facilities by Locality",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(title="Population", color="white"),
            yaxis=dict(title="Toilet Facility", color="white"),
            height=750
        )
        st.plotly_chart(fig, use_container_width=True)
        
            # 🧾 Insight Card for Toilet Facilities
        sanitation_challenges = ["No Household toilet facility", "None", "Unimproved"]
        affected_pop = df[df["Toilet Facility"].isin(sanitation_challenges)]["Population"].sum()

        with st.container():
            st.markdown(
                f"""
                <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:20px;">
                    <h4 style="color:#f5c518;">🧾 Insight</h4>
                    <p style="color:white; font-size:16px;">
                        🚻 Over <strong>{affected_pop:,} people</strong> in Savelugu Municipal rely on <strong>unimproved or no household toilet facilities</strong>.<br>
                        This raises serious public health risks including <strong>open defecation, contamination, and disease transmission</strong>.<br>
                        Targeted interventions are needed in rural areas where these challenges are more concentrated.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        
    elif chart_option == "Main Source of Drinking Water":
        st.title("🚰 Main Source of Drinking Water by Locality – Savelugu Municipal")

        data = {
            "Main Water Source": [
                "Improved water sources", "Improved water sources",
                "Public tap/Stand pipe", "Public tap/Stand pipe",
                "Borehole/Tube well", "Borehole/Tube well",
                "Protected spring", "Protected spring",
                "Pipe-borne inside dwelling", "Pipe-borne inside dwelling",
                "Rain water", "Rain water",
                "Protected well", "Protected well",
                "Bottled water", "Bottled water",
                "Sachet water", "Sachet water",
                "Pipe-borne outside dwelling (neighbour)", "Pipe-borne outside dwelling (neighbour)",
                "Pipe-borne outside dwelling (compound)", "Pipe-borne outside dwelling (compound)",
                "Unimproved water sources", "Unimproved water sources",
                "River/Stream", "River/Stream",
                "Unprotected well", "Unprotected well",
                "Unprotected spring", "Unprotected spring",
                "Tanker supplied/Vendor provided", "Tanker supplied/Vendor provided",
                "Other", "Other",
                "Dugout/Pond/Lake/Dam/Canal", "Dugout/Pond/Lake/Dam/Canal"
            ],
            "Locality": ["Rural", "Urban"] * 18,
            "Population": [
                5705, 13181,
                1242, 7350,
                3699, 1271,
                34, 8,
                115, 1902,
                52, 166,
                30, 329,
                3, 5,
                20, 195,
                374, 840,
                136, 1115,
                2713, 1483,
                1735, 383,
                16, 83,
                1, 5,
                1, 495,
                5, 2,
                955, 515
            ]
        }

        # Safety check
        assert len(data["Main Water Source"]) == len(data["Locality"]) == len(data["Population"]), "Data length mismatch"

        df = pd.DataFrame(data)

        # Plot bar chart
        fig = px.bar(
            df,
            x="Population",
            y="Main Water Source",
            color="Locality",
            orientation="h",
            barmode="group",
            text="Population",
            title="Distribution of Main Drinking Water Sources by Locality",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )

        # Apply dark theme
        fig.update_traces(textposition="outside")
        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(title="Population", color="white"),
            yaxis=dict(title="Water Source", color="white"),
            height=950
        )

        st.plotly_chart(fig, use_container_width=True)
        
        # 📊 Insight Card for Water Sources
        unimproved_sources = [
            "Unimproved water sources", "River/Stream", "Unprotected well",
            "Unprotected spring", "Tanker supplied/Vendor provided",
            "Other", "Dugout/Pond/Lake/Dam/Canal"
        ]
        at_risk = df[df["Main Water Source"].isin(unimproved_sources)]["Population"].sum()

        with st.container():
            st.markdown(
                f"""
                <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:20px;">
                    <h4 style="color:#f5c518;">💧 Insight</h4>
                    <p style="color:white; font-size:16px;">
                        ⚠️ An estimated <strong>{at_risk:,} people</strong> in Savelugu Municipal rely on <strong>unimproved or potentially unsafe drinking water sources</strong>.<br>
                        This exposes communities—especially in rural areas—to <strong>waterborne diseases</strong> and sanitation challenges.<br>
                        Prioritizing investments in safe, accessible, and sustainable water infrastructure is critical.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
    elif chart_option == "Levels of Toilet Service":
        st.title("🚻 Levels of Toilet Service – Savelugu Municipal")

        data = {
            "Toilet Service": [
                "Improved Toilet Facilities", "Improved Toilet Facilities",
                "Basic service (Improved and exclusive use)", "Basic service (Improved and exclusive use)",
                "Limited service (Improved and shared)", "Limited service (Improved and shared)",
                "Unimproved", "Unimproved"
            ],
            "Locality": [
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban"
            ],
            "Population": [
                987, 2499,
                351, 1029,
                636, 1470,
                25, 16
            ]
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Create horizontal bar chart
        fig = px.bar(
            df,
            x="Population",
            y="Toilet Service",
            color="Locality",
            orientation="h",
            facet_col="Locality",
            text="Population",
            title="Levels of Toilet Service by Locality – Faceted View",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )

        # Apply dark theme and layout tweaks
        fig.update_traces(textposition="outside")
        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(title="Population", color="white"),
            yaxis=dict(title="Toilet Service", color="white"),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)
        # ✅ Insight Box: Residents without safely managed toilet service
        risky_services = ["Limited service (Improved and shared)", "Unimproved"]
        at_risk_df = df[df["Toilet Service"].isin(risky_services)]
        at_risk_total = at_risk_df["Population"].sum()

        st.markdown(
            f"""
            <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:20px;">
                <h4 style="color:#f5c518;">🔍 Sanitation Insight</h4>
                <p style="color:white; font-size:16px;">
                    🚨 <strong>{at_risk_total:,}</strong> residents are using either unimproved or shared toilet facilities, which do not meet safely managed sanitation standards.
                    <br><br>
                    This highlights the need for targeted investment in private, improved toilet facilities to reduce disease risk and promote dignity.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    elif chart_option == "Improved and Unimproved Water Services":
        st.title("💧 Improved and Unimproved Water Services – Savelugu Municipal")

        # Water service distribution data
        data = {
            "Water Service Type": [
                "Improved Drinking Water Source", "Improved Drinking Water Source",
                "Basic service (within 30 mins round-trip)", "Basic service (within 30 mins round-trip)",
                "Limited service (more than 30 mins round-trip)", "Limited service (more than 30 mins round-trip)",
                "Unimproved Drinking Water Source", "Unimproved Drinking Water Source"
            ],
            "Locality": [
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban"
            ],
            "Population": [
                5705, 13181,
                4190, 11189,
                1515, 1992,
                2713, 1483
            ]
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Plot chart
        fig = px.bar(
            df,
            x="Population",
            y="Water Service Type",
            color="Locality",
            orientation="h",
            barmode="group",
            text="Population",
            title="Distribution of Water Services by Locality",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )

        # Styling (dark theme)
        fig.update_traces(textposition="outside")
        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(title="Population", color="white"),
            yaxis=dict(title="Water Service Type", color="white"),
            height=550
        )

        # Display chart
        st.plotly_chart(fig, use_container_width=True)
        # ✅ Smart Insight Box: Population without safely managed water
        vulnerable_categories = [
            "Limited service (more than 30 mins round-trip)",
            "Unimproved Drinking Water Source"
        ]
        at_risk_df = df[df["Water Service Type"].isin(vulnerable_categories)]
        at_risk_total = at_risk_df["Population"].sum()

        st.markdown(
            f"""
            <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:20px;">
                <h4 style="color:#30c9e8;">🚱 Water Access Insight</h4>
                <p style="color:white; font-size:16px;">
                    ⚠️ <strong>{at_risk_total:,}</strong> residents have limited or unimproved access to drinking water,
                    which does not meet the global standard for safely managed drinking water services.
                    <br><br>
                    💡 This calls for strategic investments in proximity-based water infrastructure and safe source improvement.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    elif chart_option == "Toilet Facility by Type":
        st.title("🚻 Toilet Facilities by Type – Savelugu Municipal")

        data = {
            "Toilet Type": [
                "No private toilet", "No private toilet",
                "No toilet facility", "No toilet facility",
                "Public toilet", "Public toilet",
                "Private toilet", "Private toilet",
                "WC seat", "WC seat",
                "Flush squat bowl", "Flush squat bowl",
                "Pour flush bowl", "Pour flush bowl",
                "Urine-diverting dry toilet (UDDT)", "Urine-diverting dry toilet (UDDT)",
                "Concrete pedestal/slab", "Concrete pedestal/slab",
                "Wooden pedestal/slab", "Wooden pedestal/slab",
                "Satopan/Micro flush", "Satopan/Micro flush",
                "No slab", "No slab",
                "Other", "Other"
            ],
            "Locality": [
                "Rural", "Urban"
            ] * 13,
            "Population": [
                7406, 12149,
                7263, 7154,
                143, 4995,
                1012, 2515,
                297, 676,
                128, 790,
                48, 392,
                31, 94,
                448, 527,
                32, 13,
                1, 10,
                25, 13,
                2, 0
            ]
        }

        # Create DataFrame
        df = pd.DataFrame(data)

        # Create grouped vertical bar chart
        fig = px.bar(
            df,
            x="Toilet Type",
            y="Population",
            color="Locality",
            barmode="group",
            text="Population",
            title="Types of Toilet Facilities by Locality",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )

        # Style enhancements
        fig.update_traces(
            marker_line_width=1.5,
            marker_line_color="black",
            textposition="outside"
        )

        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(
                title="Toilet Type",
                color="white",
                tickangle=45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(title="Population", color="white"),
            height=650
        )

        st.plotly_chart(fig, use_container_width=True)
        # ✅ Smart Insight: Count of population without private toilet
        lacking_private = df[df["Toilet Type"].isin(["No private toilet", "No toilet facility", "Public toilet"])]
        total_without_private = lacking_private["Population"].sum()

        st.markdown(
            f"""
            <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; margin-top:20px;">
                <h4 style="color:#30c9e8;">🚽 Toilet Access Insight</h4>
                <p style="color:white; font-size:16px;">
                    ⚠️ <strong>{total_without_private:,}</strong> residents rely on shared, public, or no toilet facilities,
                    reflecting gaps in private sanitation coverage.
                    <br><br>
                    🧼 Improving access to private and hygienic toilets is critical for reducing disease and improving dignity.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    elif chart_option == "Time Taken to Source Drinking Water":
        st.title("🎻 Violin Plot: Time to Source Drinking Water – Savelugu Municipal")

        data = {
            "Time Taken": [
                "Water on premises", "Water on premises",
                "Within 30 minutes", "Within 30 minutes",
                "31 to 60 minutes", "31 to 60 minutes",
                "61 minutes and above", "61 minutes and above"
            ],
            "Locality": [
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban",
                "Rural", "Urban"
            ],
            "Population": [
                293, 3742,
                5450, 8218,
                2148, 1859,
                527, 845
            ]
        }

        df_agg = pd.DataFrame(data)

        # Simulate raw data by repeating rows
        df_expanded = df_agg.loc[df_agg.index.repeat(df_agg["Population"])].reset_index(drop=True)

        # Plot violin chart
        fig = px.violin(
            df_expanded,
            y="Time Taken",
            x="Locality",
            color="Locality",
            box=True,
            points="all",
            title="Violin Plot of Time Categories by Locality",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )

        # Styling
        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            height=700
        )

        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_option == "Toilet Facility Breakdown":
        st.title("🚽 Toilet Facilities by Locality – Savelugu Municipal")

        data = {
            "Toilet Facility": [
                "No toilet facility", "No toilet facility",
                "Septic tank", "Septic tank",
                "KVIP/VIP", "KVIP/VIP",
                "Pit latrine", "Pit latrine",
                "Enviro Loo", "Enviro Loo",
                "Bio-digester", "Bio-digester",
                "Bio gas", "Bio gas",
                "Bucket/Pan", "Bucket/Pan",
                "Portable toilet", "Portable toilet",
                "Sewer", "Sewer",
                "Public toilet", "Public toilet",
                "Other", "Other"
            ],
            "Locality": ["Rural", "Urban"] * 12,
            "Population": [
                7263, 7154,
                441, 1205,
                346, 1239,
                219, 52,
                1, 0,
                0, 3,
                0, 4,
                0, 3,
                2, 2,
                0, 0,
                143, 4995,
                3, 7
            ]
        }

        # Create DataFrame
        df = pd.DataFrame(data)

        # Horizontal grouped bar chart
        fig = px.bar(
            df,
            x="Population",
            y="Toilet Facility",
            color="Locality",
            orientation="h",
            barmode="group",
            text="Population",
            title="Distribution of Toilet Facilities by Locality",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )

        # Dark styling
        fig.update_traces(textposition="outside")
        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(title="Population", color="white"),
            yaxis=dict(title="Toilet Facility", color="white"),
            height=700
        )

        # Render chart
        st.plotly_chart(fig, use_container_width=True)
        
            # Define unimproved/safe concern facilities
        inadequate_toilet_types = ["No toilet facility", "Bucket/Pan", "Public toilet", "Other"]

        # Calculate total population using inadequate toilet options
        total_inadequate = df[df["Toilet Facility"].isin(inadequate_toilet_types)]["Population"].sum()

        # Card-style Insight Box
        st.markdown(
            f"""
            <div style="
                background-color: #1e1e1e;
                border: 1px solid #444;
                padding: 20px;
                border-radius: 12px;
                margin-top: 20px;
                box-shadow: 0 0 10px rgba(0,0,0,0.6);
            ">
                <h4 style="color: #facc15; margin-bottom: 10px;">🚨 Sanitation Insight</h4>
                <p style="color: white; font-size: 16px; line-height: 1.6;">
                    🚽 <strong>Over {total_inadequate:,} residents</strong> across Savelugu still rely on 
                    <span style="color: #f87171;"><strong>inadequate or unsafe toilet facilities</strong></span> such as public toilets, 
                    bucket/pan systems, or none at all. This reflects urgent <strong>sanitation and dignity gaps</strong> requiring attention.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        
    elif chart_option == "Solid Waste Storage Methods":
        st.title("🗑️ Storage of Solid Waste – Savelugu Municipal")

        # Data
        data = {
            "Solid Waste Storage": [
                "Collected", "Collected",
                "Other vehicles", "Other vehicles",
                "Central container", "Central container",
                "Compaction truck", "Compaction truck",
                "Push carts/Walk-in attendant/Bicycle/Wheelbarrow", "Push carts/Walk-in attendant/Bicycle/Wheelbarrow",
                "Tricycle", "Tricycle",
                "Uncollected", "Uncollected",
                "Burn", "Burn",
                "Bury in the ground", "Bury in the ground",
                "Dumped indiscriminately", "Dumped indiscriminately",
                "Other", "Other",
                "Public dump/open space", "Public dump/open space"
            ],
            "Locality": ["Rural", "Urban"] * 12,
            "Population": [
                30, 3101,
                0, 37,
                12, 2603,
                0, 296,
                17, 64,
                1, 101,
                1962, 2061,
                818, 1617,
                554, 210,
                589, 234,
                1, 0,
                6426, 9502
            ]
        }

        df = pd.DataFrame(data)

        # Calculate total and percent
        total_population = df["Population"].sum()
        df["Percent"] = round(df["Population"] / total_population * 100, 2)

        # Unsafe methods to highlight
        unsafe_methods = [
            "Uncollected", "Burn", "Bury in the ground",
            "Dumped indiscriminately", "Public dump/open space"
        ]
        df["IsUnsafe"] = df["Solid Waste Storage"].isin(unsafe_methods)

        # Bar chart
        fig = px.bar(
            df,
            x="Population",
            y="Solid Waste Storage",
            color="Locality",
            orientation="h",
            barmode="group",
            text="Population",
            hover_data=["Percent"],
            title="Distribution of Solid Waste Storage Methods by Locality",
            color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
        )

        # Style bars
        fig.update_traces(
            textposition="outside",
            marker_line_width=1.5,
            marker_line_color="black"
        )

        fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111",
            font_color="white",
            xaxis=dict(title="Population", color="white"),
            yaxis=dict(title="Storage Method", color="white"),
            height=700
        )

        st.plotly_chart(fig, use_container_width=True)

        # ⏺ Pie chart toggle
        if st.checkbox("🧁 Show Proportion by Locality as Pie Chart"):
            pie_df = df.groupby("Locality")["Population"].sum().reset_index()
            pie_fig = px.pie(
                pie_df,
                names="Locality",
                values="Population",
                title="Proportion of Solid Waste by Locality",
                color="Locality",
                color_discrete_map={"Rural": "#2ca02c", "Urban": "#1f77b4"}
            )
            pie_fig.update_layout(
                plot_bgcolor="#111111",
                paper_bgcolor="#111111",
                font_color="white"
            )
            st.plotly_chart(pie_fig, use_container_width=True)

                # Define unsafe solid waste methods
            unsafe_methods = ["Burn", "Bury in the ground", "Dumped indiscriminately", "Public dump/open space"]

            # Calculate total population using unsafe methods
            total_uncollected = df[df["Solid Waste Storage"].isin(unsafe_methods)]["Population"].sum()

            # Card-style Insight Box with dark theme
            st.markdown(
                f"""
                <div style="
                    background-color: #1e1e1e;
                    border: 1px solid #444;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 20px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.6);
                ">
                    <h4 style="color: #facc15; margin-bottom: 10px;">🧾 Insight</h4>
                    <p style="color: white; font-size: 16px; line-height: 1.6;">
                        🔍 <strong>Over {total_uncollected:,} people</strong> in rural and urban areas still dispose waste using
                        <span style="color: #f87171;"><strong>unsafe methods</strong></span> such as burning, indiscriminate dumping,
                        or public dumps. This poses significant <strong>environmental</strong> and <strong>public health risks</strong>.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # Load and clean the dataset
    watercoverage = pd.read_csv("CoverageStatistics.csv")

    # Rename columns for readability
    watercoverage = watercoverage.rename(columns={
        "No of communities": "No_Comm",
        "Below 75": "Pop_Under_75",
        "75 -\n299": "Pop_75_299",
        "300 -\n1999": "Pop_300_1999",
        "2000 - 4999 \n": "Pop_2000_4999",
        "Over 5000": "Pop_Over_5000",
        "RURAL Population Served\n": "Rural_Served",
        "RURAL Coverage\n": "Rural_Coverage"
    })

    # Ensure numeric types for all analysis columns
    numeric_columns = [
        'Population', 'Rural_Served', 'Rural_Coverage', 'BH', 'HDW', 'SCPS',
        'LMS', 'STPS', 'RHS', 'GWCL', 'Pop_Under_75', 'Pop_75_299',
        'Pop_300_1999', 'Pop_2000_4999', 'Pop_Over_5000'
    ]

    for col in numeric_columns:
        watercoverage[col] = pd.to_numeric(watercoverage[col], errors='coerce')

    # Streamlit Title
    st.title("🚰 Community Water Coverage - Savelugu Constituency (2024)")
    st.dataframe(watercoverage, use_container_width=True)
    
    st.markdown("""
    <style>
    /* General tab container */
    [data-baseweb="tab"] {
        background-color: #1e1e1e;
        padding: 10px 16px;
        margin-right: 8px;
        border-radius: 8px;
        border: 1px solid #333;
        color: #eee;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.2s ease-in-out;
    }

    /* Hover effect */
    [data-baseweb="tab"]:hover {
        background-color: #333;
        color: #00f2ff;
        cursor: pointer;
    }

    /* Selected tab */
    [aria-selected="true"][data-baseweb="tab"] {
        background-color: #00f2ff !important;
        color: #000 !important;
        font-weight: bold;
        box-shadow: 0 0 8px #00f2ff;
    }

    /* Ensure text stays inside */
    [data-baseweb="tab"] > div {
        display: flex;
        align-items: center;
        justify-content: center;
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



    # Tabs 1–10
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "💧 Boreholes",
        "🚰 Water Sources Summary",
        "📊 Population Histogram",
        "👥 Population Size by Category",
        "🏘️ Top 10 Populous",
        "🌊 Top Rural Population Served",
        "📈 Rural Coverage Distribution",
        "🧮 Water Source Usage",
        "🔍 Boreholes vs Coverage",
        "📊 Correlation Heatmap"
    ])

    # --- TAB 1: Boreholes ---
    with tab1:
        st.subheader("💧 Boreholes by Community")
        bh_df = watercoverage[watercoverage['BH'] > 0]
        fig_bh = px.bar(
            bh_df.sort_values('BH', ascending=False),
            x='Communities',
            y='BH',
            labels={'BH': 'Number of Boreholes'},
            color='BH',
            height=500
        )
        st.plotly_chart(fig_bh, use_container_width=True)

    # --- TAB 2: Water Source Pie ---
    with tab2:
        st.subheader("🚰 Proportion of Water Sources (Doughnut Chart)")
        source_columns = ['BH', 'HDW', 'SCPS', 'LMS', 'STPS', 'RHS', 'GWCL']
        source_sums = watercoverage[source_columns].sum().reset_index()
        source_sums.columns = ['Water Source', 'Total']

        fig_doughnut = px.pie(
            source_sums,
            names='Water Source',
            values='Total',
            title='Proportion of Water Sources Used Across Communities',
            hole=0.4  # This makes it a doughnut chart
        )

        fig_doughnut.update_traces(textinfo='percent+label')
        fig_doughnut.update_layout(showlegend=True)

        st.plotly_chart(fig_doughnut, use_container_width=True)


    # --- TAB 3: Population Histogram ---
    with tab3:
        st.subheader("📊 Community Population Distribution")
        fig_hist = px.histogram(
            watercoverage,
            x='Population',
            nbins=30,
            labels={'Population': 'Population'},
            color_discrete_sequence=['#636EFA']
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # --- TAB 4: Population by Size ---
    with tab4:
        st.subheader("👥 Population Size Categories")
        pop_size_df = watercoverage[['Communities', 'Pop_75_299', 'Pop_300_1999', 'Pop_2000_4999', 'Pop_Over_5000']]
        fig_stack = px.bar(
            pop_size_df,
            x='Communities',
            y=['Pop_75_299', 'Pop_300_1999', 'Pop_2000_4999', 'Pop_Over_5000'],
            labels={'value': 'Population', 'variable': 'Size Category'},
            title='Population Size Categories by Community'
        )
        st.plotly_chart(fig_stack, use_container_width=True)

    # --- TAB 5: Top 10 Populous Communities ---
    with tab5:
        st.subheader("🏘️ Top 10 Most Populous Communities")
        top_communities = watercoverage.sort_values(by='Population', ascending=False).head(10)
        st.dataframe(top_communities[['Communities', 'Population']], use_container_width=True)

    # --- TAB 6: Top 10 Communities by Rural Served ---
    with tab6:
        st.subheader("🌊 Top 10 Communities by Rural Population Served")
        top_served = watercoverage.sort_values(by='Rural_Served', ascending=False).head(10)
        fig_top_served = px.bar(
            top_served,
            x='Communities',
            y='Rural_Served',
            title='Top 10 Communities by Rural Population Served',
            labels={'Rural_Served': 'Rural Population Served'},
            color='Rural_Served',
            hover_data=['Population', 'Rural_Coverage']
        )
        st.plotly_chart(fig_top_served, use_container_width=True)

    # --- TAB 7: Rural Coverage Histogram ---
    with tab7:
        st.subheader("📈 Rural Coverage (%) Distribution")
        fig_coverage_dist = px.histogram(
            watercoverage,
            x='Rural_Coverage',
            nbins=20,
            title='Distribution of Rural Coverage Percentages',
            labels={'Rural_Coverage': 'Rural Coverage (%)'},
            color_discrete_sequence=['#00cc96']
        )
        st.plotly_chart(fig_coverage_dist, use_container_width=True)

    # --- TAB 8: Water Source Totals ---
    with tab8:
        st.subheader("🧮 Total Count of Each Water Source Type")
        water_types = ['BH', 'HDW', 'SCPS', 'LMS', 'STPS', 'RHS', 'GWCL']
        totals_df = watercoverage[water_types].sum().reset_index()
        totals_df.columns = ['Source', 'Total']
        fig_sources = px.bar(
            totals_df,
            x='Source',
            y='Total',
            title='Total Count of Each Water Source Type',
            color='Total'
        )
        st.plotly_chart(fig_sources, use_container_width=True)
        
    scatter_df = watercoverage.dropna(subset=['Population', 'BH', 'Rural_Coverage'])

    # --- TAB 9: Boreholes vs Rural Coverage Scatter ---
    with tab9:
        st.subheader("🔍 Boreholes vs Rural Coverage (%)")
        fig_scatter = px.scatter(
        scatter_df,
        x='BH',
        y='Rural_Coverage',
        size='Population',
        hover_name='Communities',
        title='Boreholes vs Rural Coverage (%)',
        labels={'BH': 'Number of Boreholes', 'Rural_Coverage': 'Rural Coverage (%)'},
        color='Rural_Coverage',
        color_continuous_scale='Viridis'
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- TAB 10: Correlation Heatmap ---
    # --- TAB 10: Correlation Heatmap ---
    # --- TAB 10: Correlation Heatmap ---
    with tab10:
        st.subheader("📊 Correlation Heatmap (Dark Theme)")

        import matplotlib.pyplot as plt
        import seaborn as sns

        # Set dark background theme
        plt.style.use('dark_background')
        sns.set_theme(style="darkgrid")

        # Select numeric columns
        numeric_df = watercoverage.select_dtypes(include='number')

        # Create figure and dark theme settings
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('#111')  # Background of the entire figure
        ax.set_facecolor('#111')         # Background of the heatmap itself

        # Draw heatmap
        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap='viridis',        # or 'rocket_r', 'coolwarm', 'plasma', 'magma'
            fmt=".2f",
            ax=ax,
            cbar=True,
            linewidths=0.5,
            linecolor='#333'
        )

        # Optional: Make tick labels bright
        ax.tick_params(axis='both', colors='white')
        st.pyplot(fig)



    st.markdown("""
<style>
    .definitions-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1.5em;
        font-family: 'Segoe UI', sans-serif;
        font-size: 0.95rem;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 8px rgba(255, 255, 255, 0.05);
    }

    .definitions-table thead {
        background-color: #222;
        color: #fff;
    }

    .definitions-table th, .definitions-table td {
        padding: 0.75em 1em;
        text-align: left;
        border-bottom: 1px solid #333;
    }

    .definitions-table tbody tr:nth-child(even) {
        background-color: #111;
    }

    .definitions-table tbody tr:hover {
        background-color: #1a1a1a;
    }

    .definitions-table td {
        color: #eee;
    }

    .definitions-table b {
        color: #fff;
    }
</style>

<table class="definitions-table">
<thead>
<tr>
    <th>Column Name</th>
    <th>Meaning</th>
</tr>
</thead>
<tbody>
<tr><td><b>Community</b></td><td>Name of the locality or town</td></tr>
<tr><td><b>Total Population</b></td><td>Entire population of that community</td></tr>
<tr><td><b>Pop. 75-299</b></td><td>People in settlements with 75–299 people</td></tr>
<tr><td><b>Pop. 300-1999</b></td><td>People in medium-size communities (300–1999)</td></tr>
<tr><td><b>Pop. 2000-4999</b></td><td>People in large communities (2000–4999)</td></tr>
<tr><td><b>Pop. 5000+</b></td><td>People in major towns or urban centers</td></tr>
<tr><td><b>Rural Population</b></td><td>Number of people classified as rural in that community</td></tr>
<tr><td><b>Population Served</b></td><td>Number of rural people with access to potable water</td></tr>
<tr><td><b>Rural Coverage (%)</b></td><td>Percentage of rural population with potable water</td></tr>
<tr><td><b>Population Group Served</b></td><td>Specific group of rural people served</td></tr>
<tr><td><b>No. of Communities</b></td><td>Total communities counted in the dataset</td></tr>
<tr><td><b>BH</b></td><td>Boreholes available in the community</td></tr>
<tr><td><b>HDW</b></td><td>Hand-dug wells count</td></tr>
<tr><td><b>SCPS</b></td><td>Small community piped systems</td></tr>
<tr><td><b>LMS</b></td><td>Limited mechanized systems</td></tr>
<tr><td><b>STPS</b></td><td>Small town piped systems</td></tr>
<tr><td><b>RHS</b></td><td>Rain harvesting systems</td></tr>
<tr><td><b>GWCL</b></td><td>Ghana Water Company Limited connection (urban piped supply)</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)
    with tab2:
        st.subheader("🚰 Proportion of Water Sources")

        source_columns = ['BH', 'HDW', 'SCPS', 'LMS', 'STPS', 'RHS', 'GWCL']
        source_sums = watercoverage[source_columns].sum().reset_index()
        source_sums.columns = ['Water Source', 'Total']

        fig_doughnut = px.pie(
            source_sums,
            names='Water Source',
            values='Total',
            hole=0.5,  # Doughnut style
            title='Water Sources Used Across Communities'
        )

        fig_doughnut.update_traces(
            textinfo='percent+label',
            marker=dict(
                line=dict(color='white', width=2),  # border for "depth" feel
                colors=[
                    '#1f77b4', '#ff7f0e', '#2ca02c',
                    '#d62728', '#9467bd', '#8c564b', '#e377c2'
                ]
            )
        )

        fig_doughnut.update_layout(
            showlegend=True,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white'),
            title_font=dict(size=20)
        )

        st.plotly_chart(fig_doughnut, use_container_width=True)



if __name__ == "__main__":
    app()            
