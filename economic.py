import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import plotly.graph_objects as go
import networkx as nx
import altair as alt

def app():
    
    st.title("Educational Attainment Breakdown (Age 5-14) – Savelugu Municipal")

    # ------------------------------
    # Raw Data
    data = [
        # Not economically active
        {"Econ": "Not economically active", "Area": "Rural", "Gender": "Male", "Age": "5-9", "Never attended": 1072, "Nursery": 133, "Kindergarten": 564, "Primary": 2006, "JSS/JHS": 0, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Not economically active", "Area": "Rural", "Gender": "Male", "Age": "10-14", "Never attended": 564, "Nursery": 1, "Kindergarten": 2, "Primary": 1799, "JSS/JHS": 322, "SSS/SHS": 4, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Not economically active", "Area": "Rural", "Gender": "Female", "Age": "5-9", "Never attended": 1224, "Nursery": 115, "Kindergarten": 500, "Primary": 1681, "JSS/JHS": 0, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Not economically active", "Area": "Rural", "Gender": "Female", "Age": "10-14", "Never attended": 769, "Nursery": 1, "Kindergarten": 1, "Primary": 1394, "JSS/JHS": 229, "SSS/SHS": 3, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Not economically active", "Area": "Urban", "Gender": "Male", "Age": "5-9", "Never attended": 751, "Nursery": 261, "Kindergarten": 1174, "Primary": 3794, "JSS/JHS": 0, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Not economically active", "Area": "Urban", "Gender": "Male", "Age": "10-14", "Never attended": 321, "Nursery": 1, "Kindergarten": 1, "Primary": 3220, "JSS/JHS": 727, "SSS/SHS": 9, "Secondary": 3, "Voc/technical/commercial": 0},
        {"Econ": "Not economically active", "Area": "Urban", "Gender": "Female", "Age": "5-9", "Never attended": 962, "Nursery": 248, "Kindergarten": 1061, "Primary": 3506, "JSS/JHS": 0, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Not economically active", "Area": "Urban", "Gender": "Female", "Age": "10-14", "Never attended": 488, "Nursery": 1, "Kindergarten": 0, "Primary": 2829, "JSS/JHS": 668, "SSS/SHS": 5, "Secondary": 0, "Voc/technical/commercial": 0},
        # Economically active
        {"Econ": "Economically active", "Area": "Rural", "Gender": "Male", "Age": "5-9", "Never attended": 56, "Nursery": 1, "Kindergarten": 4, "Primary": 28, "JSS/JHS": 0, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Economically active", "Area": "Rural", "Gender": "Male", "Age": "10-14", "Never attended": 126, "Nursery": 0, "Kindergarten": 0, "Primary": 76, "JSS/JHS": 16, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Economically active", "Area": "Rural", "Gender": "Female", "Age": "5-9", "Never attended": 21, "Nursery": 0, "Kindergarten": 2, "Primary": 8, "JSS/JHS": 0, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Economically active", "Area": "Rural", "Gender": "Female", "Age": "10-14", "Never attended": 58, "Nursery": 0, "Kindergarten": 0, "Primary": 36, "JSS/JHS": 7, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Economically active", "Area": "Urban", "Gender": "Male", "Age": "5-9", "Never attended": 29, "Nursery": 1, "Kindergarten": 9, "Primary": 14, "JSS/JHS": 0, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Economically active", "Area": "Urban", "Gender": "Male", "Age": "10-14", "Never attended": 55, "Nursery": 0, "Kindergarten": 0, "Primary": 82, "JSS/JHS": 15, "SSS/SHS": 1, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Economically active", "Area": "Urban", "Gender": "Female", "Age": "5-9", "Never attended": 18, "Nursery": 0, "Kindergarten": 3, "Primary": 9, "JSS/JHS": 0, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
        {"Econ": "Economically active", "Area": "Urban", "Gender": "Female", "Age": "10-14", "Never attended": 40, "Nursery": 0, "Kindergarten": 0, "Primary": 37, "JSS/JHS": 9, "SSS/SHS": 0, "Secondary": 0, "Voc/technical/commercial": 0},
    ]

    # ------------------------------
    # Raw Data
    df = pd.DataFrame(data)  # Assuming `data` is defined as you've posted

    # ------------------------------
    # Sidebar Filters
    st.sidebar.header("📊 Filter Options")
    econ_filter = st.sidebar.multiselect("Economic Status", df["Econ"].unique(), default=df["Econ"].unique())
    area_filter = st.sidebar.multiselect("Area", df["Area"].unique(), default=df["Area"].unique())
    gender_filter = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
    age_filter = st.sidebar.multiselect("Age Group", df["Age"].unique(), default=df["Age"].unique())

    # ------------------------------
    # Filtered Data
    filtered_df = df[
        (df["Econ"].isin(econ_filter)) &
        (df["Area"].isin(area_filter)) &
        (df["Gender"].isin(gender_filter)) &
        (df["Age"].isin(age_filter))
    ]

    # ------------------------------
    # Melt the data for animation (retain Age)
    edu_cols = ["Never attended", "Nursery", "Kindergarten", "Primary", "JSS/JHS", "SSS/SHS", "Secondary", "Voc/technical/commercial"]
    df_melted = filtered_df.melt(
        id_vars=["Age", "Gender", "Area"], 
        value_vars=edu_cols,
        var_name="Education Level",
        value_name="Population"
    )

    # ------------------------------
    # Animated Horizontal Bar Chart by Age
    fig = px.bar(
        df_melted,
        x="Population",
        y="Education Level",
        orientation='h',
        title="Animated Educational Levels by Age Group",
        color="Population",
        color_continuous_scale="Viridis",
        animation_frame="Age",
        animation_group="Education Level"
    )

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
        xaxis=dict(title="Number of People", color="white", gridcolor="gray"),
        yaxis=dict(color="white"),
        height=550,
        margin=dict(l=80, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.title("Educational Attainment by Industry (Age 5-14) – Savelugu Municipal")

    # Sample cleaned dataset
    data = [
        {"Industry": "Agriculture", "Education": "Never attended", "Area": "Rural", "Gender": "Male", "Age": "5-9", "Count": 54},
        {"Industry": "Agriculture", "Education": "Never attended", "Area": "Rural", "Gender": "Male", "Age": "10-14", "Count": 123},
        {"Industry": "Agriculture", "Education": "Never attended", "Area": "Rural", "Gender": "Female", "Age": "5-9", "Count": 17},
        {"Industry": "Agriculture", "Education": "Never attended", "Area": "Rural", "Gender": "Female", "Age": "10-14", "Count": 50},
        {"Industry": "Manufacturing", "Education": "Primary", "Area": "Urban", "Gender": "Male", "Age": "10-14", "Count": 6},
        {"Industry": "Wholesale", "Education": "Primary", "Area": "Urban", "Gender": "Female", "Age": "10-14", "Count": 3},
        {"Industry": "Construction", "Education": "Primary", "Area": "Urban", "Gender": "Male", "Age": "10-14", "Count": 7},
        {"Industry": "Accommodation", "Education": "JSS/JHS", "Area": "Urban", "Gender": "Female", "Age": "10-14", "Count": 2},
        {"Industry": "Other services", "Education": "Primary", "Area": "Urban", "Gender": "Male", "Age": "10-14", "Count": 8},
    ]

    df = pd.DataFrame(data)

    # Sidebar filters
    st.sidebar.header("🔎 Filter Options")
    industry = st.sidebar.multiselect("Select Industry", df["Industry"].unique(), default=df["Industry"].unique(), key="industry_filter")
    education = st.sidebar.multiselect("Select Education Level", df["Education"].unique(), default=df["Education"].unique(), key="education_filter")
    area = st.sidebar.multiselect("Select Area", df["Area"].unique(), default=df["Area"].unique(), key="area_filter")
    gender = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique(), key="gender_filter")
    age = st.sidebar.multiselect("Select Age Group", df["Age"].unique(), default=df["Age"].unique(), key="age_filter")


    # Filter data
    filtered_df = df[
        (df["Industry"].isin(industry)) &
        (df["Education"].isin(education)) &
        (df["Area"].isin(area)) &
        (df["Gender"].isin(gender)) &
        (df["Age"].isin(age))
    ]

    # Summarize for chart
    summary = filtered_df.groupby("Education")["Count"].sum().reset_index().sort_values("Count")

    # Plot
    fig = px.bar(
        summary,
        x="Count",
        y="Education",
        orientation="h",
        title="Filtered Educational Distribution by Industry",
        color="Count",
        color_continuous_scale="Inferno"
    )

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
        xaxis=dict(title="Number of People", color="white", gridcolor="gray"),
        yaxis=dict(title="Education Level", color="white"),
        height=550
    )

    st.plotly_chart(fig, use_container_width=True)
    
if __name__ == "__main__":
    app()
