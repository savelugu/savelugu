import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import plotly.graph_objects as go
import networkx as nx
import altair as alt

def app():
    
    # 9. Population Structure
    st.markdown("### 9. Population Structure")
    st.markdown("### Key Development Metrics")

    st.markdown("""
    <style>
    .card-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: nowrap;
        gap: 20px;
        margin-top: 10px;
    }
    .card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        flex: 1;
        min-width: 200px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        text-align: center;
        color: white;
        font-family: "Segoe UI", sans-serif;
    }
    .card-title {
        font-size: 14px;
        color: #bbbbbb;
    }
    .card-value {
        font-size: 28px;
        font-weight: bold;
        color: #f1f1f1;
    }
    </style>

    <div class="card-container">
    <div class="card">
        <div class="card-title">Total Population</div>
        <div class="card-value">122,888</div>
    </div>
    <div class="card">
        <div class="card-title">Land Area</div>
        <div class="card-value">1,550 km²</div>
    </div>
    <div class="card">
        <div class="card-title">Population Density</div>
        <div class="card-value">79.27/km²</div>
    </div>
    <div class="card">
        <div class="card-title">Annual Growth Rate</div>
        <div class="card-value">2.6%</div>
    </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("### 📊 Demographic & Socioeconomic Snapshot")

    st.markdown("""
    <style>
    .card-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-top: 20px;
    }
    .card {
        background-color: #1e1e1e;
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        font-family: "Segoe UI", sans-serif;
    }
    .card-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
        color: #1E90FF;
    }
    .card-body {
        font-size: 15px;
        line-height: 1.6;
        text-align: justify;
    }
    </style>

    <div class="card-grid">

    <div class="card">
        <div class="card-title">4. Demographic Profile</div>
        <div class="card-body">
        • <b>Rapid population growth</b>: From 92,717 in 2010 to 122,888 in 2021 (≈ 2.6% p.a.)<br>
        • <b>Youthful population</b>: 54% are under 20 years<br>
        • <b>Slightly more females</b> (50.9%) — sex ratio 96.6<br>
        • <b>Urbanisation</b>: 63%, driven by Savelugu township expansion
        </div>
    </div>

    <div class="card">
        <div class="card-title">5. Households & Housing</div>
        <div class="card-body">
        • <b>Avg. household size</b>: 5.2 vs 3.6 national<br>
        • <b>Housing deprivation</b>: 62.6% in poor housing<br>
        • <b>Toilets</b>: 94.3% lack improved toilets<br>
        • <b>Urban infrastructure</b>: Slightly better electricity & water access
        </div>
    </div>

    <div class="card">
        <div class="card-title">6. Education & Literacy</div>
        <div class="card-body">
        • <b>60,689 persons aged 6+</b> cannot read or write<br>
        • <b>57% of the illiterate are female</b><br>
        • 5th highest illiteracy count in Northern Region
        </div>
    </div>

    <div class="card">
        <div class="card-title">7. Economic Activity</div>
        <div class="card-body">
        • <b>Agriculture</b> employs ≈70% (maize, rice, soy, livestock)<br>
        • <b>Trade & transport</b> growing along the N10 corridor<br>
        • <b>Youth unemployment</b> is high (16–18%)
        </div>
    </div>

    </div>
    """, unsafe_allow_html=True)



    st.subheader("9.1 Gender Distribution")
    gender_df = pd.DataFrame({
        "Gender": ["Males", "Females"],
        "Number of Persons": [60390, 62498]
    })
    st.dataframe(gender_df, use_container_width=True)

    st.subheader("9.2 Age Group Distribution")
    age_group_df = pd.DataFrame({
        "Age Group": ["0-14 years", "15-64 years", "65+ years"],
        "Number of Persons": [53963, 64484, 4441]
    })
    st.dataframe(age_group_df, use_container_width=True)

    st.subheader("9.3 Age Distribution by Gender")
    age_gender_df = pd.DataFrame({
        "Age Group": ["80+ years", "70-79", "60-69", "50-59", "40-49", 
                    "30-39", "20-29", "10-19", "0-9"],
        "Males": [503, 917, 1453, 2333, 4661, 6747, 9767, 13756, 20253],
        "Females": [788, 1179, 1513, 2361, 5164, 8434, 11197, 12076, 19786]
    })
    st.dataframe(age_gender_df, use_container_width=True)

    # 10. Urbanization
    st.markdown("### 10. Urbanization")
    urban_df = pd.DataFrame({
        "Category": ["Rural", "Urban"],
        "Number of Persons": [45567, 77321]
    })
    st.dataframe(urban_df, use_container_width=True)

    # Urbanization Pie Chart
    st.subheader("🧭 Urban vs Rural Population Share")
    urban_pie = px.pie(
        urban_df,
        names="Category",
        values="Number of Persons",
        title="Urbanization Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.4
    )
    st.plotly_chart(urban_pie, use_container_width=True)


    # 11. Literacy Levels
    st.markdown("### 11. Literacy (Aged 11+)")
    literacy_df = pd.DataFrame({
        "Literacy Status": ["Literate", "Illiterate"],
        "Number of Persons": [31961, 47451]
    })
    st.dataframe(literacy_df, use_container_width=True)

    # 12. Ethnic Composition
    st.markdown("### 12. Ethnic Composition")
    ethnic_df = pd.DataFrame({
        "Ethnic Group": [
            "Akan", "Ga-Dangme", "Ewe", "Guan", "Gurma", 
            "Mole-Dagbani", "Grusi", "Mandé", "Other Ethnic Groups"
        ],
        "Number of Persons": [1365, 65, 799, 207, 565, 114076, 1102, 3330, 621]
    })
    st.dataframe(ethnic_df, use_container_width=True)

    # Ethnic Group Pie Chart
    st.subheader("🌍 Ethnic Composition of Savelugu Municipal")
    ethnic_pie = px.pie(
        ethnic_df,
        names="Ethnic Group",
        values="Number of Persons",
        title="Ethnic Group Share",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole =0.4
    )
    st.plotly_chart(ethnic_pie, use_container_width=True)


    # 13. Population Projections
    st.markdown("### 13. Population Projections (2021–2032)")
    years = list(range(2021, 2033))
    total_pop = [122888, 127613, 132413, 137243, 142091, 146290, 150984, 155697, 160422, 165152, 169902, 174667]
    male_pop =  [60390,  63051,  65422,  67804,  70192,  72256,  74561,  76874,  79189,  81505,  83828,  86157]
    female_pop = [62498, 64562, 66991, 69439, 71899, 74034, 76423, 78823, 81233, 83647, 86074, 88510]

    proj_df = pd.DataFrame({
        "Year": [str(y) for y in years],
        "Total Population": total_pop,
        "Male Population": male_pop,
        "Female Population": female_pop
    })
    # Create frames for each year
    frames = []
    for i in range(len(proj_df)):
        year = proj_df.loc[i, "Year"]
        frame_data = [
            go.Scatter(x=proj_df["Year"][:i+1], y=proj_df["Total Population"][:i+1], mode='lines+markers', name="Total Population"),
            go.Scatter(x=proj_df["Year"][:i+1], y=proj_df["Male Population"][:i+1], mode='lines+markers', name="Male Population"),
            go.Scatter(x=proj_df["Year"][:i+1], y=proj_df["Female Population"][:i+1], mode='lines+markers', name="Female Population"),
        ]
        frames.append(go.Frame(data=frame_data, name=year))

    # Initial figure
    fig_proj = go.Figure(
        data=[
            go.Scatter(x=[proj_df["Year"][0]], y=[proj_df["Total Population"][0]], mode='lines+markers', name="Total Population"),
            go.Scatter(x=[proj_df["Year"][0]], y=[proj_df["Male Population"][0]], mode='lines+markers', name="Male Population"),
            go.Scatter(x=[proj_df["Year"][0]], y=[proj_df["Female Population"][0]], mode='lines+markers', name="Female Population"),
        ],
        layout=go.Layout(
            title="Population Projections (2021–2032)",
            xaxis=dict(tickmode='linear'),
            yaxis=dict(title="Population"),
            updatemenus=[{
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }],
            sliders=[{
                "active": 0,
                "steps": [
                    {
                        "method": "animate",
                        "label": str(year),
                        "args": [[str(year)], {"frame": {"duration": 300, "redraw": True}, "mode": "immediate"}]
                    }
                    for year in proj_df["Year"]
                ]
            }]
        ),
        frames=frames
    )

    # Display in Streamlit
    st.plotly_chart(fig_proj, use_container_width=True)

    with st.expander("📋 View Raw Projection Table"):
        st.dataframe(proj_df, use_container_width=True)

    st.markdown("""
    <style>
    .dark-card {
        background-color: #1e1e1e;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-left: 6px solid;
        border-radius: 10px;
        font-size: 1.05rem;
        color: #f1f1f1;
        box-shadow: 0 0 10px rgba(0, 150, 255, 0.2);
    }

    .dark-info { border-color: #00bfff; }
    .dark-success { border-color: #28a745; }
    .dark-warning { border-color: #ffc107; }
    .dark-error { border-color: #dc3545; }

    .dark-card span.emoji {
        font-size: 1.3rem;
        margin-right: 0.4rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- DATA ---
    data = [
        ["Total", "Rural", "Male", 22593],
        ["Total", "Rural", "Female", 22970],
        ["Total", "Urban", "Male", 37749],
        ["Total", "Urban", "Female", 39444],
        ["Not Covered", "Rural", "Male", 11701],
        ["Not Covered", "Rural", "Female", 10688],
        ["Not Covered", "Urban", "Male", 11511],
        ["Not Covered", "Urban", "Female", 10128],
        ["Covered", "Rural", "Male", 10892],
        ["Covered", "Rural", "Female", 12282],
        ["Covered", "Urban", "Male", 26238],
        ["Covered", "Urban", "Female", 29316],
    ]

    df = pd.DataFrame(data, columns=["Coverage", "Area", "Gender", "Count"])

    # --- SIDEBAR FILTERS ---
    # Custom CSS for blue multiselects
    st.markdown("""
        <style>
        section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
            background-color: #003366;
            color: white;
            border-radius: 5px;
            border: 1px solid #3399ff;
        }

        section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
            background-color: #3399ff;
            color: white;
            border-radius: 5px;
        }

        section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"]:hover {
            border-color: #66ccff;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR FILTERS ---
    st.title("🧭 Filter Data")
    # Inject custom CSS for filter container
    st.markdown("""
        <style>
        .filter-container {
            background-color: #007BFF !important;  /* force Bootstrap blue */
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 1rem;
        }
        .filter-container label, .filter-container .stMultiSelect label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Open the filter container
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    gender_filter = st.multiselect("Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
    area_filter = st.multiselect("Select Area", options=df["Area"].unique(), default=df["Area"].unique())

    # --- FILTERED DATA ---
    filtered_df = df[df["Gender"].isin(gender_filter) & df["Area"].isin(area_filter)]

    # --- MAIN TITLE ---
    st.title("🏥 Health Insurance Coverage - Savelugu Municipal")

    # --- FUNNEL CHART ---
    st.subheader("🔻 Funnel Chart: Overall Health Insurance Coverage")
    funnel_df = filtered_df[filtered_df["Coverage"] != "Total"].groupby("Coverage")["Count"].sum().reset_index()
    funnel_df = funnel_df.sort_values(by="Count", ascending=False)

    fig_funnel = px.funnel(
        funnel_df,
        y="Coverage",
        x="Count",
        title="Health Insurance Funnel (Filtered)",
        color="Coverage",
        color_discrete_sequence=px.colors.sequential.Burg
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    # --- GROUPED BAR CHART ---
    st.subheader("📊 Grouped Bar Chart: Area & Coverage by Gender")

    fig_grouped = px.bar(
        filtered_df[filtered_df["Coverage"] != "Total"],
        x="Area",
        y="Count",
        color="Coverage",
        barmode="group",
        facet_col="Gender",
        title="Coverage Breakdown (Filtered)",
        text="Count"
    )
    st.plotly_chart(fig_grouped, use_container_width=True)

    st.subheader("🌞 Savelugu: Health Insurance Coverage by Gender and Area")

    fig_sunburst = px.sunburst(
        filtered_df[filtered_df["Coverage"] != "Total"],
        path=["Gender", "Area", "Coverage"],
        values="Count",
        title="Sunburst of Health Insurance Coverage",
    )

    fig_sunburst.update_layout(
        margin=dict(t=50, l=0, r=0, b=0),
        paper_bgcolor="#1f1f2e",
        plot_bgcolor="#1f1f2e",
        font_color="white",
    )

    st.plotly_chart(fig_sunburst, use_container_width=True)


    # --- RAW DATA VIEW ---
    with st.expander("📄 View Raw Data"):
        st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)


    
    # Load your data
    df = pd.read_csv("communities.csv")  # Replace with actual path

    # Bar Chart: Top 15 Communities by Total Population
    top_communities = df.sort_values("Total_Population", ascending=False).head(15)
    fig_pop = px.bar(top_communities, 
                    x="Community_Name", 
                    y="Total_Population", 
                    title="Top 15 Most Populous Communities in Savelugu",
                    labels={"Total_Population": "Population"},
                    color="Total_Population")

    st.plotly_chart(fig_pop)
        # Title
    st.title("📊 Population by Religious Affiliation, Locality, Geographic Area, Sex and Age")

    # Load the data (replace with your actual file)
    @st.cache_data
    def load_data():
        return pd.read_csv("./Population/religious_affiliation.csv")  # Replace with your CSV or Excel

    df = load_data()
    


# Inject custom CSS for filter container
    st.markdown("""
        <style>
        .filter-container {
            background-color: #007BFF !important;  /* force Bootstrap blue */
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 1rem;
        }
        .filter-container label, .filter-container .stMultiSelect label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Open the filter container
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)

    # ---- FILTERS ----
    st.title("🔎 Filter Data")

    
    # Filters inside styled block with unique keys
    religions = st.multiselect(
        "Select Religious Affiliation",
        options=df['Religious_Affiliation'].unique(),
        default=df['Religious_Affiliation'].unique(),
        key="religion_filter_main"
    )

    localities = st.multiselect(
        "Select Locality",
        options=df['Locality'].unique(),
        default=df['Locality'].unique(),
        key="locality_filter_main"
    )

    sexes = st.multiselect(
        "Select Sex",
        options=df['Sex'].unique(),
        default=df['Sex'].unique(),
        key="sex_filter_main"
    )

    # Close the div
    st.markdown('</div>', unsafe_allow_html=True)



    # Apply filters
    filtered_df = df[
        df["Religious_Affiliation"].isin(religions) &
        df["Locality"].isin(localities) &
        df["Sex"].isin(sexes)
    ]

    # ---- TABLE DISPLAY ----
    st.subheader("📋 Filtered Data Table")
    st.dataframe(df, use_container_width=True)

    # ---- EXPORT ----
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_population_data.csv",
        mime='text/csv'
    )
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


        # ---- CHARTS TABBED ----
    tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs([
        "📊 Age Group Distribution",
        "🛐 Total by Religious Affiliation",
        "🧭 By Religious Affiliation & Locality",
        "🚻 By Religious Affiliation & Sex",
        "📉 Religion vs Age Trends",
        "🏙️ Locality vs Sex"
    ])

    # --- TAB 1 ---# --- TAB 1 ---
    with tab1:
        st.subheader("📈 Population Chart by Age Groups")

        age_columns = df.columns[4:]  # First 4 columns assumed to be metadata

        long_df = filtered_df.melt(
            id_vars=["Religious_Affiliation", "Locality", "Sex"],
            value_vars=age_columns,
            var_name="Age_Group",
            value_name="Population",
        )

        # Calculate total population between age groups
        total_by_age_group = long_df.groupby("Age_Group")["Population"].sum().reset_index()
        total_population_all = total_by_age_group["Population"].sum()
        dominant_age_group = total_by_age_group.loc[total_by_age_group["Population"].idxmax()]

        # Insight Card with dynamic numbers
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
                    🔍 The total population analyzed across all age groups is 
                    <strong>{int(total_population_all):,}</strong> individuals.
                    The <span style="color:#facc15;"><strong>{dominant_age_group['Age_Group']}</strong></span> group has the highest population,
                    accounting for <strong>{int(dominant_age_group['Population']):,} people</strong>.
                    This indicates a <strong>youthful population structure</strong> that will require strong investment in 
                    education, employment, and health services in the coming years.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Bar chart by Age Group and Sex
        fig = px.bar(
            long_df,
            x="Age_Group",
            y="Population",
            color="Sex",
            barmode="group",
            title="Population Distribution by Age Group",
            labels={"Age_Group": "Age Group", "Population": "Number of People"},
            height=500
        )

        # Apply dark layout
        fig.update_layout(
            plot_bgcolor="#1f1f2e",
            paper_bgcolor="#1f1f2e",
            font_color="#ffffff",
            legend_bgcolor="#1f1f2e",
            legend_bordercolor="#444",
            legend_borderwidth=1
        )

        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2 ---
    with tab2:
        st.subheader("📊 Total Population by Religious Affiliation")

        # Group and calculate total population per Religious Affiliation
        pop_by_religion = df.groupby("Religious_Affiliation")[age_columns].sum()
        pop_by_religion["Total_Population"] = pop_by_religion.sum(axis=1)
        pop_by_religion = pop_by_religion[["Total_Population"]].reset_index()

        # Display insight box
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
                    🔍 <strong>Islam</strong> is the most widely practiced religion in the Savelugu Municipality,
                    with a substantial margin over all other affiliations. Christianity follows,
                    with <em>Pentecostal/Charismatic</em> and <em>Catholic</em> groups forming notable subgroups.
                    This population distribution has implications for <strong>community outreach, education, and health programming</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Plot bar chart
        fig_religion = px.bar(
            pop_by_religion,
            x="Religious_Affiliation",
            y="Total_Population",
            color="Religious_Affiliation",
            title="Total Population by Religious Affiliation",
            labels={"Total_Population": "Population"},
            height=500
        )

        # Apply dark theme
        fig_religion.update_layout(
            plot_bgcolor="#1f1f2e",
            paper_bgcolor="#1f1f2e",
            font_color="#ffffff",
            legend_bgcolor="#1f1f2e",
            legend_bordercolor="#444",
            legend_borderwidth=1
        )

        st.plotly_chart(fig_religion, use_container_width=True)


    # --- TAB 3 ---
    with tab3:
        st.subheader("📊 Population by Religious Affiliation and Locality")

        # Group and calculate total population
        pop_religion_locality = df.groupby(["Religious_Affiliation", "Locality"])[age_columns].sum()
        pop_religion_locality["Total_Population"] = pop_religion_locality.sum(axis=1)
        pop_religion_locality = pop_religion_locality[["Total_Population"]].reset_index()

        # Display the table
        st.dataframe(pop_religion_locality, use_container_width=True)

        # --- Insight Box ---
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
                    🔍 <strong>Islam is the dominant religion</strong> in both urban and rural parts of Savelugu Municipality,
                    with significantly higher populations across both settings.
                    <strong>Christian populations</strong> tend to be more evenly split between urban and rural,
                    with urban areas slightly favoring Pentecostal and Catholic groups.
                    This reveals key patterns for <strong>faith-based outreach, urban planning, and service delivery</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Plot the chart
        fig = px.bar(
            pop_religion_locality,
            x="Religious_Affiliation",
            y="Total_Population",
            color="Locality",
            barmode="group",
            title="Population by Religious Affiliation and Locality",
            height=600
        )

        # Dark theme for the chart
        fig.update_layout(
            plot_bgcolor="#1f1f2e",
            paper_bgcolor="#1f1f2e",
            font_color="#ffffff",
            legend_bgcolor="#1f1f2e",
            legend_bordercolor="#444",
            legend_borderwidth=1
        )

        st.plotly_chart(fig, use_container_width=True)


    # --- TAB 4 ---
    with tab4:
        st.subheader("📊 Population by Religious Affiliation and Sex (with Percentages)")

        pop_religion_sex = df.groupby(["Religious_Affiliation", "Sex"])[age_columns].sum()
        pop_religion_sex["Total_Population"] = pop_religion_sex.sum(axis=1)
        pop_religion_sex = pop_religion_sex.reset_index()

        total_pop_all = pop_religion_sex["Total_Population"].sum()
        pop_religion_sex["Percentage"] = (pop_religion_sex["Total_Population"] / total_pop_all) * 100

        st.dataframe(
            pop_religion_sex[["Religious_Affiliation", "Sex", "Total_Population", "Percentage"]],
            use_container_width=True
        )

        # --- Insight Box ---
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
                    🔍 <strong>Islam remains the dominant religion</strong> across both sexes, with notable female-majority populations
                    in urban Muslim communities. <strong>Christian denominations</strong> show relatively balanced distributions,
                    but some (e.g., Pentecostal/Charismatic) have slightly more females.
                    These patterns offer key insights for tailoring <strong>gender-sensitive programs</strong>
                    in education, healthcare, and community outreach.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Chart ---
        fig = px.bar(
            pop_religion_sex,
            x="Religious_Affiliation",
            y="Total_Population",
            color="Sex",
            barmode="group",
            text=pop_religion_sex["Percentage"].apply(lambda x: f"{x:.1f}%"),
            title="Population by Religious Affiliation and Sex (with Percentages)",
            labels={"Total_Population": "Population"},
            height=600
        )

        fig.update_traces(textposition="outside")

        fig.update_layout(
            plot_bgcolor="#1f1f2e",
            paper_bgcolor="#1f1f2e",
            font_color="#ffffff",
            legend_bgcolor="#1f1f2e",
            legend_bordercolor="#444",
            legend_borderwidth=1
        )

        st.plotly_chart(fig, use_container_width=True)


    # --- TAB 5 ---
    with tab5:
        st.subheader("📊 Population by Religious Affiliation and Age Group (with Percentages)")

        long_df = df.melt(
            id_vars=["Religious_Affiliation"],
            value_vars=age_columns,
            var_name="Age_Group",
            value_name="Population"
        )

        pop_by_religion_age = long_df.groupby(["Religious_Affiliation", "Age_Group"], as_index=False).sum()

        total_per_religion = pop_by_religion_age.groupby("Religious_Affiliation")["Population"].transform("sum")
        pop_by_religion_age["Percentage"] = (pop_by_religion_age["Population"] / total_per_religion) * 100

        st.dataframe(pop_by_religion_age, use_container_width=True)

        # --- Insight Box ---
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
                    🔍 The age group analysis reveals that <strong>Islamic adherents</strong> form the largest population across
                    nearly all age bands, especially within the <strong>0–14 and 15–64 year ranges</strong>. This suggests that public
                    policy, education, and healthcare targeting younger and working-age groups should be <strong>culturally inclusive</strong>
                    and sensitive to <strong>religious diversity</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Chart ---
        fig = px.line(
            pop_by_religion_age,
            x="Age_Group",
            y="Population",
            color="Religious_Affiliation",
            markers=True,
            title="📉 Population Trends by Religious Affiliation and Age Group",
            labels={"Population": "Population"},
            height=600
        )

        fig.update_layout(
            plot_bgcolor="#1f1f2e",
            paper_bgcolor="#1f1f2e",
            font_color="#ffffff",
            legend_bgcolor="#1f1f2e",
            legend_bordercolor="#444",
            legend_borderwidth=1
        )

        st.plotly_chart(fig, use_container_width=True)

        
        # --- TAB 6 ---
    with tab6:
        st.subheader("🏙️ Population by Locality and Sex")

        # Group by Locality and Sex
        locality_sex_df = df.groupby(["Locality", "Sex"])[age_columns].sum()
        locality_sex_df["Total_Population"] = locality_sex_df.sum(axis=1)
        locality_sex_df = locality_sex_df.reset_index()

        # Display the table
        st.dataframe(locality_sex_df, use_container_width=True)

        # Plot
        fig = px.bar(
            locality_sex_df,
            x="Locality",
            y="Total_Population",
            color="Sex",
            barmode="group",
            text=locality_sex_df["Total_Population"],
            title="Population by Locality and Sex",
            labels={"Total_Population": "Population"},
            height=600
        )
        
        fig.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
        )
        
        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, use_container_width=True)
        
        # --- INSIGHTS: Population Demographics ---

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
                    🔍 <strong>Over 10,675 females</strong> aged <strong>0–14 years</strong> are located in <strong>rural areas</strong> of Savelugu Municipal.
                    This highlights a pressing need for improved <strong>early education</strong>, <strong>maternal health services</strong>,
                    and <strong>gender-sensitive community development</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

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
                    🔍 <strong>Over 10,291 males</strong> aged <strong>0–14 years</strong> live in <strong>rural areas</strong>.
                    This large young male population underscores the need for increased investment in <strong>primary schools</strong>,
                    <strong>youth development programs</strong>, and <strong>healthcare outreach</strong> in rural zones.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

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
                    🔍 In <strong>urban areas</strong>, there are approximately <strong>6,866 females</strong> aged <strong>0–14 years</strong>.
                    This suggests the need for sustained investment in <strong>girls’ education</strong>, <strong>safe urban spaces</strong>,
                    and <strong>inclusive school feeding programs</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

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
                    🔍 The <strong>urban male</strong> population aged <strong>0–14 years</strong> is around <strong>7,207</strong>, slightly
                    higher than their female counterparts. Urban youth services should prioritize <strong>gender-equitable access</strong>
                    to education, sports, and child protection.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

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
                    🔍 Over <strong>1,000 elderly individuals (65+ years)</strong> live across both urban and rural localities,
                    with a slightly higher number of <strong>elderly women</strong>. This signals a need for improved <strong>eldercare services</strong>,
                    <strong>social protection policies</strong>, and <strong>age-friendly infrastructure</strong> in the municipality.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.title("📊 Marital Status & Demographic Explorer – Savelugu Municipal")


    df = pd.read_csv("./Population/maritalstatus.csv")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert age group columns to numeric
    age_cols = df.columns[5:]
    df[age_cols] = df[age_cols].apply(pd.to_numeric, errors="coerce")

    # Total column
    df["Total"] = df[age_cols].sum(axis=1)
    
    # Inject custom CSS for filter container
    st.markdown("""
        <style>
        .filter-container {
            background-color: #007BFF !important;  /* force Bootstrap blue */
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 1rem;
        }
        .filter-container label, .filter-container .stMultiSelect label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Open the filter container
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)


    st.subheader("✅ Filters")
    sex_filter = st.selectbox("Filter by Sex", options=["All"] + sorted(df["Sex"].unique().tolist()))
    locality_filter = st.selectbox("Filter by Locality", options=["All"] + sorted(df["Locality"].unique().tolist()))
    edu_filter = st.selectbox("Filter by Education", options=["All"] + sorted(df["Education"].unique().tolist()))
    
    show_pct = st.sidebar.checkbox("Show Percentages Instead of Counts", value=False)
    
    


    filtered_df = df.copy()
    if sex_filter != "All":
        filtered_df = filtered_df[filtered_df["Sex"] == sex_filter]
    if locality_filter != "All":
        filtered_df = filtered_df[filtered_df["Locality"] == locality_filter]
    if edu_filter != "All":
        filtered_df = filtered_df[filtered_df["Education"] == edu_filter]

    st.write("### 📋 Summary Table")
    st.dataframe(filtered_df)

    total_pop = filtered_df["Total"].sum()
    st.metric("Total People in Selection", f"{int(total_pop):,}")

    # Pie chart by Sex
    pie_data = filtered_df.groupby("Sex")["Total"].sum().reset_index()
    fig_pie = px.pie(pie_data, names="Sex", values="Total", title="Population Distribution by Sex")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Bar chart by Education
    edu_data = filtered_df.groupby("Education")["Total"].sum().reset_index()
    fig_edu = px.bar(edu_data, x="Education", y="Total", title="Population by Education Level")
    st.plotly_chart(fig_edu, use_container_width=True)

    # Age distribution
    st.write("### 📈 Age Group Distribution")
    age_sums = filtered_df[age_cols].sum().reset_index()
    age_sums.columns = ["Age Group", "Count"]
    fig_age = px.bar(age_sums, x="Age Group", y="Count", title="Age Group Distribution")
    st.plotly_chart(fig_age, use_container_width=True)
    
        # Stacked bar: Age group by Sex
    st.subheader("🧑‍🤝‍🧑 Age Group Distribution by Sex")
    stacked_sex = filtered_df.groupby("Sex")[age_cols].sum().T
    stacked_sex = stacked_sex.reset_index().rename(columns={"index": "Age Group"})
    stacked_sex = pd.melt(stacked_sex, id_vars=["Age Group"], var_name="Sex", value_name="Count")
    fig_stack = px.bar(stacked_sex, x="Age Group", y="Count", color="Sex", title="Stacked Age Group by Sex")
    st.plotly_chart(fig_stack, use_container_width=True)

    # Grouped bar: Age group by Locality
    st.subheader("🏙️ Age Group Distribution by Locality")
    locality_age = filtered_df.groupby("Locality")[age_cols].sum().T
    locality_age = locality_age.reset_index().rename(columns={"index": "Age Group"})
    locality_age = pd.melt(locality_age, id_vars=["Age Group"], var_name="Locality", value_name="Count")
    fig_loc = px.bar(locality_age, x="Age Group", y="Count", color="Locality", barmode="group", title="Age Group by Locality")
    st.plotly_chart(fig_loc, use_container_width=True)

    # Heatmap: Age group vs Education
    st.subheader("🔥 Heatmap: Age Group vs Education")
    edu_age = filtered_df.groupby("Education")[age_cols].sum()
    fig_heat = px.imshow(edu_age, labels=dict(x="Age Group", y="Education", color="Count"),
                         x=edu_age.columns, y=edu_age.index,
                         title="Heatmap: Age Group Distribution by Education")
    st.plotly_chart(fig_heat, use_container_width=True)
    
    
    # Marital Status Comparison
    st.subheader("💍 Marital Status Comparison")
    mar_stat = filtered_df.groupby("Marital_Status")["Total"].sum().reset_index().sort_values("Total", ascending=False)

    if show_pct:
        mar_stat["Percentage"] = (mar_stat["Total"] / mar_stat["Total"].sum()) * 100
        mar_stat["Label"] = mar_stat["Percentage"].round(1).astype(str) + '%'
        fig_marital = px.bar(
            mar_stat,
            x="Marital_Status",
            y="Percentage",
            text="Label",
            title="Marital Status Distribution (%)"
        )
    else:
        mar_stat["Label"] = mar_stat["Total"].astype(int).astype(str)
        fig_marital = px.bar(
            mar_stat,
            x="Marital_Status",
            y="Total",
            text="Label",
            title="Marital Status Distribution"
        )

    fig_marital.update_traces(textposition="outside")
    fig_marital.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_marital, use_container_width=True)
    
    
# Load your dataset safely
    @st.cache_data
    def load_data():
        df = pd.read_csv("./Population/population_20250624-234400.csv")

        # Clean and normalize column names
        df.columns = df.columns.str.strip().str.replace('\ufeff', '').str.replace('\xa0', '')

        # Show cleaned columns
        

        # Check if required columns exist
        required_cols = ["Male", "Female", "Age", "Locality", "Education"]
        for col in required_cols:
            if col not in df.columns:
                st.error(f"❌ Required column missing: {col}")
                st.stop()

        # Create total population column
        df["Total"] = df["Male"] + df["Female"]
        return df

    # Load data
    df = load_data()

    # App title
    st.title("📊 Education & Demographic Analysis Dashboard")

    # Sidebar filters with unique keys
    st.header("🔍 Filter Data")

    selected_locality = st.multiselect(
        "Select Locality", df["Locality"].unique(), default=df["Locality"].unique(), key="locality_filter"
    )
    selected_education = st.multiselect(
        "Select Education Level", df["Education"].unique(), default=df["Education"].unique(), key="education_filter"
    )
    

    # Apply filters
    filtered_df = df[
        (df["Locality"].isin(selected_locality)) &
        (df["Education"].isin(selected_education)) 
        
    ]

    # Show filtered data
    st.subheader("📋 Filtered Data Preview")
    st.dataframe(filtered_df)
        # === Tabs for Visualizations ===
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧑‍🤝‍🧑 Gender Distribution",
        "🎓 Education Level Totals",
        "🌍 Locality Heatmap",
        "🧮 Gender Ratio Pie Chart"
    ])

    # === Tab 1: Gender Distribution Bar Chart ===
    with tab1:
        st.subheader("🧑‍🤝‍🧑 Gender Distribution by Education")
        gender_fig = px.bar(
            filtered_df, x="Education", y=["Male", "Female"],
            barmode="group", title="Male vs Female by Education Level"
        )
        st.plotly_chart(gender_fig, use_container_width=True)

    # === Tab 2: Total by Education ===
    with tab2:
        st.subheader("🎓 Total Population by Education Level")
        edu_summary = filtered_df.groupby("Education")["Total"].sum().reset_index()
        edu_fig = px.bar(
            edu_summary, x="Education", y="Total", text_auto=True,
            color="Total", title="Total by Education Level"
        )
        st.plotly_chart(edu_fig, use_container_width=True)

    # === Tab 3: Heatmap ===
    with tab3:
        st.subheader("🌍 Education Levels by Locality (Heatmap)")
        heatmap_df = filtered_df.pivot_table(
            values="Total", index="Locality", columns="Education", aggfunc="sum"
        ).fillna(0)
        heatmap_fig = px.imshow(
            heatmap_df,
            labels=dict(x="Education", y="Locality", color="Population"),
            title="Heatmap of Education Level by Locality"
        )
        st.plotly_chart(heatmap_fig, use_container_width=True)

    # === Tab 4: Gender Ratio Pie Chart ===
    with tab4:
        st.subheader("🧮 Overall Gender Ratio (Doughnut Chart)")

        # Prepare gender totals
        gender_total = filtered_df[["Male", "Female"]].sum().reset_index()
        gender_total.columns = ["Gender", "Count"]

        # Define a professional color palette
        custom_colors = ["#0D1C8D", "#a92b98"]  # Deep blue & warm coral

        # Create doughnut chart
        fig_gender_dist = px.pie(
            gender_total,
            names="Gender",
            values="Count",
            hole=0.5,
            title="Gender Composition (Doughnut)",
            color_discrete_sequence=custom_colors
        )

        # Customize layout: modern, minimal look
        fig_gender_dist.update_traces(
            textinfo="percent+label",
            marker=dict(line=dict(color="#FFFFFF", width=2))
        )

        fig_gender_dist.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            showlegend=True,
            title_font=dict(size=18, color="#264653"),
            legend_title_text='Gender',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig_gender_dist, use_container_width=True)
        
        
            # ---------- LOAD & PREP ---------- #
    @st.cache_data
    def load_health_data():
        df = pd.read_csv("./Population/health_20250624-164053.csv")
        #st.write("🔍 Raw Columns:", df.columns.tolist())

        # tidy up column names
        df.columns = (
            df.columns.str.strip()
            .str.replace("\ufeff", "", regex=True)
            .str.replace("\xa0", "", regex=True)
        )

        static_cols = ["Health_Insurance", "Education", "Locality", "Sex"]
        age_cols   = [c for c in df.columns if c not in static_cols]

        # wide ➜ long
        df_long = df.melt(
            id_vars=static_cols,
            value_vars=age_cols,
            var_name="Age_Group",
            value_name="Population",
        )
        # drop 0 / NaN
        df_long = df_long[df_long["Population"] > 0]
        return df_long


    df_long = load_health_data()

    st.title("🏥 Health‑Insurance Demographics Dashboard")

    # ---------- FILTERS ---------- #
    with st.sidebar:
        st.header("🔍 Filters")
        st.caption("Use the selectors to filter the visuals in real‑time")

        ins_filter = st.multiselect(
            "Health Insurance status",
            df_long["Health_Insurance"].unique(),
            default=df_long["Health_Insurance"].unique(),
            key="ins_filter",
        )
        edu_filter = st.multiselect(
            "Education level",
            df_long["Education"].unique(),
            default=df_long["Education"].unique(),
            key="edu_filter",
        )
        loc_filter = st.multiselect(
            "Locality",
            df_long["Locality"].unique(),
            default=df_long["Locality"].unique(),
            key="loc_filter",
        )
        sex_filter = st.multiselect(
            "Sex",
            df_long["Sex"].unique(),
            default=df_long["Sex"].unique(),
            key="sex_filter",
        )

    # apply filters
    filt = df_long[
        df_long["Health_Insurance"].isin(ins_filter)
        & df_long["Education"].isin(edu_filter)
        & df_long["Locality"].isin(loc_filter)
        & df_long["Sex"].isin(sex_filter)
    ]

    # ---------- TABS & CHARTS ---------- #
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🟢 Covered vs Not Covered",
            "🌞 Sunburst",
            "📊 Age Breakdown",
            "📈  (Age × Locality)",
            "🗂️  (Education share)",
        ]
    )

   # ---- 1. Doughnut: Covered vs Not Covered ---- #
    with tab1:
        st.subheader("🩺 Health‑Insurance Coverage")

        # Summarize population by insurance coverage
        coverage_tot = filt.groupby("Health_Insurance")["Population"].sum().reset_index()

        # Create doughnut chart
        pie_cov = px.pie(
            coverage_tot,
            names="Health_Insurance",
            values="Population",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Set2,
            template='plotly_dark'
        )

        # Apply dark layout settings
        pie_cov.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=30, r=10, l=10, b=30)
        )

        # Add percent + label to each wedge
        pie_cov.update_traces(textinfo="percent+label")

        # Display chart
        st.plotly_chart(pie_cov, use_container_width=True)

    # ---- 2. Sunburst: Insurance → Education → Sex ---- #
    with tab2:
        st.subheader("Population Pyramid: Insurance ➜ Education ➜ Sex")
        sb = px.sunburst(
            filt,
            path=["Health_Insurance", "Education", "Sex"],
            values="Population",
            color="Education",
            color_discrete_sequence=px.colors.qualitative.Prism,
        )
        sb.update_layout(margin=dict(t=30, r=0, l=0, b=0))
        st.plotly_chart(sb, use_container_width=True)

    # ---- 3. Age Distribution (grouped bar) ---- #
    with tab3:
        st.subheader("Age‑Group Distribution (all filters applied)")
        age_tot = filt.groupby("Age_Group")["Population"].sum().reset_index()
        bar_age = px.bar(
            age_tot,
            x="Age_Group",
            y="Population",
            title="Population by Age Group",
            labels={"Age_Group": "Age Group"},
            color_discrete_sequence=["#1f77b4"],
        )
        bar_age.update_layout(xaxis_tickangle=-45, margin=dict(t=40, b=80))
        st.plotly_chart(bar_age, use_container_width=True)

    with tab4:
        st.subheader("📊 Grouped Bar Chart: Age Group by Locality")

        bar_df = (
            filt.groupby(["Locality", "Age_Group"])["Population"]
            .sum()
            .reset_index()
        )

        fig_grouped = px.bar(
            bar_df,
            x="Age_Group",
            y="Population",
            color="Locality",
            barmode="group",
            text="Population",
            title="Population Distribution by Age Group & Locality",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Plasma_r
        )

        fig_grouped.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis_title="Age Group",
            yaxis_title="Total Population",
            xaxis_tickangle=-35,
            margin=dict(t=60, l=40, r=10, b=80),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )

        fig_grouped.update_traces(textposition='outside', cliponaxis=False)

        st.plotly_chart(fig_grouped, use_container_width=True)



    with tab5:
        st.subheader("📚 Education Composition inside Insurance Status (Bar Chart)")

        bar_df = (
            filt.groupby(["Health_Insurance", "Education"])["Population"]
            .sum()
            .reset_index()
        )

        bar_chart = px.bar(
            bar_df,
            x="Education",
            y="Population",
            color="Health_Insurance",
            barmode="group",  # side-by-side bars
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Set3,
            title="Education Composition by Insurance Status"
        )

        bar_chart.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=40, l=20, r=20, b=80),
            xaxis_tickangle=-45,
            xaxis_title="Education Level",
            yaxis_title="Population"
        )

        st.plotly_chart(bar_chart, use_container_width=True)


            
        

    # Footer
    st.markdown("---")
    st.markdown("Developed by **Zakari Moro** | Data powered by Savelugu Municipal Demographics")
if __name__ == "__main__":
    app()
