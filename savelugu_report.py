import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64


st.set_page_config(
    page_title="Savelugu Municipal Report",
    page_icon="./Images/cropped2.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Report on Savelugu Municipal Demographics and Development Overview")

def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
# Define your logo and animation paths
logo_path = "./Images/combo.gif"
cropped = "./Images/cropped.png"
animation_home_path = "./Animations/home.json"
animation_employee_path = "./Animations/employee.json"
image_path = "./Images/login.png"
logo_base64 = load_image(logo_path)
cropped_logo =load_image(cropped)
logo_base64 = load_image(logo_path)
# Define a function to create a capacity-building training plan

# Sidebar with custom logo and navigation menu
with st.sidebar:
    # Adding the logo with custom styling
    st.markdown(
        f'''
        <div style="text-align: center; padding: 5px; background-color: black;">
            <img src="data:image/png;base64,{cropped_logo}" alt="Logo" style="width: 100px;">
        </div>
        ''',
        unsafe_allow_html=True,
    )


def create_card(title, value, image_path=None):
    image_base64 = load_image(image_path) if image_path else ""
    style = """
    <style>
        .card-container {
            display: flex;
            justify-content: center;
        }
        .glow {
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 20px #00ff00
            background: #001f3f;
            animation: glow 1.5s infinite alternate;
            width: 300px;
            height: 150px;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            text-align: center;
        }
        @keyframes glow {
            from {
                box-shadow: 0 0 10px #28a745;
            }
            to {
                box-shadow: 0 0 20px #28a745;
            }
        }
        .card-image {
            width: 50px;
            height: 50px;
            margin-left: 10px;
        }
        .card-content {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
    </style>
    """
    card_html = f"""
    <div class="card-container">
        <div class="glow">
            <div class="card-content">
                <h2 class="card-title" style="font-size: 16px;">{title}</h2>
                <p style="font-size: 16px;">{value}</p>
            </div>
            {"<img src='data:image/png;base64," + image_base64 + "' class='card-image'/>" if image_base64 else ""}
        </div>
    </div>
    """
    st.markdown(style, unsafe_allow_html=True)
    st.markdown(card_html, unsafe_allow_html=True)



# 1. Introduction
st.markdown("### 1. Introduction")
st.write("""
Savelugu Municipal is located in the Northern Region of Ghana. 
The municipality covers a total land area of 1,550 square kilometers and had a population 
of 122,888 according to the 2021 Census. This report presents the demographic characteristics, 
population structure, and development indicators of Savelugu Municipal.
""")

# 2. Geographic & Administrative Context
st.markdown("### 2. Geographic & Administrative Context")
st.write("""
Savelugu Municipal lies just north‑west of Tamale, sharing boundaries with Nanton (south‑east), Tolon (west), Karaga (east) and West Mamprusi (north). Created as a separate municipality in 2018, it forms part of Ghana’s Guinea Savannah ecological zone. The terrain is largely flat to gently undulating with vast stretches suited to rain‑fed agriculture as well as seasonal grazing.
""")

st.subheader("📍 Map of Savelugu in Ghana")

# Coordinates of Savelugu
savelugu_coords = {
    "lat": 9.6241,
    "lon": -0.8306
}

# Create map view
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=savelugu_coords["lat"],
        longitude=savelugu_coords["lon"],
        zoom=7,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=[savelugu_coords],
            get_position='[lon, lat]',
            get_color='[255, 0, 0, 160]',
            get_radius=10000,
        )
    ],
))

# 3. Key Development Metrics
st.markdown("### 3. Key Development Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Population", "122,888")
col2.metric("Land Area", "1,550 km²")
col3.metric("Population Density", "79.27/km²")
col4.metric("Annual Growth Rate", "2.6%")

# 4. Demographic Profile
st.markdown("### 4. Demographic Profile")
st.write("""
- **Rapid population growth**: From 92,717 in 2010 to 122,888 in 2021 (≈ 2.6% p.a.)  
- **Youthful population**: 54% are under 20 years  
- **Slightly more females** (50.9%) — sex ratio 96.6  
- **Urbanisation**: 63%, driven by Savelugu township expansion
""")

# 5. Households & Housing
st.markdown("### 5. Households & Housing")
st.write("""
- **Avg. household size**: 5.2 vs 3.6 national  
- **Housing deprivation**: 62.6% in poor housing  
- **Toilets**: 94.3% lack improved toilets  
- **Urban infrastructure**: Slightly better electricity & water access
""")

# 6. Education & Literacy
st.markdown("### 6. Education & Literacy")
st.write("""
- **60,689 persons aged 6+** cannot read or write  
- **57% of the illiterate are female**  
- 5th highest illiteracy count in Northern Region
""")

# 7. Economic Activity
st.markdown("### 7. Economic Activity")
st.write("""
- **Agriculture** employs ≈70% (maize, rice, soy, livestock)  
- **Trade & transport** growing along the N10 corridor  
- **Youth unemployment** is high (16–18%)
""")

# 8. Multidimensional Poverty Index (MPI)
st.markdown("### 8. Multidimensional Poverty Index (MPI)")
col1, col2, col3 = st.columns(3)
col1.metric("MPI Value", "0.187")
col2.metric("Incidence", "41.1%")
col3.metric("Intensity", "45.5%")

st.subheader("🌡️ Heatmap of MPI by Sub-District (Demo)")

# Sample poverty data by zone
poverty_data = pd.DataFrame({
    "Zone": ["Savelugu Central", "Tunaayili", "Kadia", "Yong", "Gushie", "Diare"],
    "Latitude": [9.6241, 9.7001, 9.5202, 9.6500, 9.4800, 9.7400],
    "Longitude": [-0.8306, -0.8500, -0.8000, -0.8100, -0.7800, -0.8700],
    "MPI": [0.19, 0.22, 0.17, 0.15, 0.25, 0.18]
})

# Show as map with color intensity
layer = pdk.Layer(
    "HeatmapLayer",
    data=poverty_data,
    get_position='[Longitude, Latitude]',
    get_weight="MPI",
    radius=30000,
    aggregation=pdk.types.String("MEAN")
)

view_state = pdk.ViewState(
    latitude=9.6,
    longitude=-0.82,
    zoom=9,
    pitch=30,
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))


st.write("""
- **Living standards**: 62.6% deprived (housing material)  
- **Sanitation**: 94.3% lack improved toilets  
- **Health insurance**: 59.3% not insured  
- **Education**: 40%+ adults have no formal schooling
""")
st.success("📌 Over 41% of the population are multidimensionally poor; average deprivation intensity is 45.5%.")

# 9. Population Structure
st.markdown("### 9. Population Structure")

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
st.line_chart(proj_df.set_index("Year"))

with st.expander("📋 View Raw Projection Table"):
    st.dataframe(proj_df, use_container_width=True)

# 14. Planning Implications
st.markdown("### 14. Planning Implications")
st.info("📘 **Expand education, health, and job opportunities** for the growing youth population")
st.success("🚽 **Address water, sanitation, and housing material** deficits")
st.warning("👧 **Promote adult literacy and girl-child school retention** programs")
st.error("🎯 **Target MPI indicators** for focused and measurable poverty reduction")

# 15. Conclusion
st.markdown("### 15. Conclusion")
st.success("""
Savelugu Municipal is experiencing rapid demographic change with strong urban growth, high youth population, 
and persistent poverty challenges. With over 122,000 people and a density of 79.27/km², 
targeted investments in education, sanitation, employment, and infrastructure are essential 
to meet the needs of this growing population and reduce multidimensional poverty.
""")


st.subheader("📊 Poverty vs Key Infrastructure Indicators")

# Sample zone-level data
infra_data = pd.DataFrame({
    "Zone": ["Savelugu Central", "Tunaayili", "Kadia", "Yong", "Gushie", "Diare"],
    "MPI": [0.19, 0.22, 0.17, 0.15, 0.25, 0.18],
    "Improved Toilets (%)": [15, 10, 20, 18, 8, 22],
    "Electricity Access (%)": [65, 45, 55, 60, 40, 70],
    "Literacy Rate (%)": [58, 42, 50, 55, 37, 62],
    "Health Insurance (%)": [45, 30, 35, 40, 25, 50]
})

# Melt dataframe for grouped bar chart
melted = infra_data.melt(id_vars=["Zone", "MPI"], var_name="Indicator", value_name="Percentage")

import altair as alt

chart = alt.Chart(melted).mark_bar().encode(
    x=alt.X("Zone:N", title="Zone"),
    y=alt.Y("Percentage:Q", title="Percentage"),
    color="Indicator:N",
    tooltip=["Zone", "Indicator", "Percentage"]
).properties(
    width=800,
    height=400,
    title="Infrastructure Access vs MPI by Zone"
)

st.altair_chart(chart, use_container_width=True)


st.subheader("🫧 Bubble Chart: MPI vs Improved Toilets")

bubble = alt.Chart(infra_data).mark_circle().encode(
    x="MPI:Q",
    y="Improved Toilets (%):Q",
    size="Electricity Access (%):Q",
    color="Zone:N",
    tooltip=["Zone", "MPI", "Improved Toilets (%)", "Electricity Access (%)"]
).properties(
    width=700,
    height=400
)

st.altair_chart(bubble, use_container_width=True)




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
    </style>
"""
st.markdown(css_animation, unsafe_allow_html=True)
st.markdown("<h1 class='bumping-text'>Savelugu Community Dashboard</h1>", unsafe_allow_html=True)

# --- Metrics ---
total_communities = df['Community_Name'].nunique()
total_population = df['Total_Population'].sum()
total_males = df['Male_Population'].sum()
total_females = df['Female_Population'].sum()
total_households = df['HouseHold'].sum()
head_male = df['Head_Male'].sum()
head_female = df['Head_Female'].sum()

# --- Cards (as Columns) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Communities", total_communities)
col2.metric("Total Population", total_population)
col3.metric("Male Population", total_males)
col4.metric("Female Population", total_females)

col5, col6, col7 = st.columns(3)
col5.metric("Total Households", total_households)
col6.metric("Male Household Heads", head_male)
col7.metric("Female Household Heads", head_female)

# --- Optional: Show full dataset ---
with st.expander("📊 Show Raw Data"):
    st.dataframe(df)


# Compute totals across all communities
total_male = df['Male_Population'].sum()
total_female = df['Female_Population'].sum()

# Gender distribution pie chart
gender_df = pd.DataFrame({
    'Gender': ['Male', 'Female'],
    'Count': [total_male, total_female]
})

# Head of household by gender
head_male = df['Head_Male'].sum()
head_female = df['Head_Female'].sum()

household_head_df = pd.DataFrame({
    'Gender': ['Male Head', 'Female Head'],
    'Count': [head_male, head_female]
})

# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='color: #15FFFF;'>Gender Distribution</h3>", unsafe_allow_html=True)
    
    fig_gender_dist = px.pie(
        gender_df,
        values='Count',
        names='Gender',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu,
    )
    fig_gender_dist.update_traces(textposition='inside', textinfo='percent+label')
    fig_gender_dist.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))
    st.plotly_chart(fig_gender_dist)

with col2:
    st.markdown("<h3 style='color: #15FFFF;'>Household Head by Gender</h3>", unsafe_allow_html=True)
    
    fig_head_dist = px.pie(
        household_head_df,
        values='Count',
        names='Gender',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig_head_dist.update_traces(textposition='inside', textinfo='percent+label')
    fig_head_dist.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))
    st.plotly_chart(fig_head_dist)

st.divider()


<<<<<<< HEAD
# Sidebar Filter for Poverty Breakdown Charts
st.sidebar.markdown("### 📂 Filter Poverty Data")
selected_chart = st.sidebar.selectbox(
    "Select Poverty Breakdown:",
    (
        "By Sex of Head of Household",
        "By Household Size",
        "By Educational Level",
        "By Sector of Employment",
        "By Economic Sector"
    )
)

# Chart: Multidimensional Poverty Breakdown
if selected_chart == "By Sex of Head of Household":
    data = {
        "Sex of Head": ["Savelugu Municipal", "Female", "Male"],
        "Poverty Rate (%)": [41.1, 56.6, 37.7]
    }
    df = pd.DataFrame(data)
    title = "Multidimensional Poverty by Sex of Head of Household - Savelugu Municipal"
    y_col = "Sex of Head"

elif selected_chart == "By Household Size":
    data = {
        "Household Size": [
            "Savelugu Municipal",
            "One to four members",
            "Five to nine members",
            "Ten or more members"
        ],
        "Poverty Rate (%)": [41.1, 38.4, 40.7, 44.3]
    }
    df = pd.DataFrame(data)
    title = "Multidimensional Poverty by Household Size - Savelugu Municipal"
    y_col = "Household Size"

elif selected_chart == "By Educational Level":
    data = {
        "Education Level": [
            "Savelugu Municipal",
            "No education",
            "Basic",
            "Secondary",
            "Post secondary",
            "Tertiary",
            "Other"
        ],
        "Poverty Rate (%)": [41.1, 45.7, 30.9, 29.3, 22.7, 15.3, 16.7]
    }
    df = pd.DataFrame(data)
    title = "Multidimensional Poverty by Educational Level of Head of Household - Savelugu Municipal"
    y_col = "Education Level"

elif selected_chart == "By Sector of Employment":
    data = {
        "Sector of Employment": [
            "Savelugu Municipal",
            "Private Informal",
            "Private Formal",
            "Public",
            "Other",
            "Not Working"
        ],
        "Poverty Rate (%)": [41.1, 34.2, 18.8, 7.6, 3.6, 71.1]
    }
    df = pd.DataFrame(data)
    title = "Multidimensional Poverty by Sector of Employment of Head of Household - Savelugu Municipal"
    y_col = "Sector of Employment"

elif selected_chart == "By Economic Sector":
    data = {
        "Economic Sector": [
            "Savelugu Municipal",
            "Agriculture",
            "Industry",
            "Service"
        ],
        "Poverty Rate (%)": [41.1, 37.0, 17.9, 14.3]
    }
    df = pd.DataFrame(data)
    title = "Multidimensional Poverty by Economic Sector of Employment of Head of Household - Savelugu Municipal"
    y_col = "Economic Sector"

# Plotting the selected chart
fig = px.bar(
    df,
    y=y_col,
    x="Poverty Rate (%)",
    color=y_col,
    text="Poverty Rate (%)",
    orientation="h",
    title=title,
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(
    yaxis_title=None,
    xaxis_title="Poverty Rate (%)",
    showlegend=False,
    height=500
)

st.plotly_chart(fig, use_container_width=True)
=======
>>>>>>> c36dc7ef43d3d45b2ca1509a52ea3449ce8f8cac
