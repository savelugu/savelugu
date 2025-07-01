import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import plotly.graph_objects as go
import networkx as nx
import altair as alt



def app():
    
    st.title("Savelugu Municipal Housing Insights")
    st.markdown("Explore housing completion and structural types across rural and urban communities.")

    # --- Residential Completion Data ---
    res_completion = {
        "Level_of_Completion": [
            "Fully Completed", "Completely roofed but uncompleted", "Partially roofed",
            "Roofing level (with improvised roof)", "Lintel Level (with improvised roof)"
        ],
        "Rural": [4647, 311, 19, 31, 8],
        "Urban": [6278, 730, 115, 70, 11]
    }
    res_df = pd.DataFrame(res_completion)
    res_melted = res_df.melt("Level_of_Completion", var_name="Locality", value_name="Count")

    # --- Structure Completion Data ---
    structure_completion = {
        "Level_of_Completion": [
            "Fully Completed", "Completely roofed but uncompleted", "Partially roofed",
            "Roofing level (with improvised roof)", "Lintel Level (with improvised roof)",
            "Roofing level (without roof)", "Lintel Level (without roof)",
            "Windows Level", "Concrete/Metal Pillar level"
        ],
        "Rural": [6965, 486, 31, 64, 31, 165, 62, 40, 5],
        "Urban": [9138, 999, 130, 99, 28, 1105, 219, 44, 8]
    }
    struct_df = pd.DataFrame(structure_completion)
    struct_melted = struct_df.melt("Level_of_Completion", var_name="Locality", value_name="Count")

    # --- Structure Types Data ---
    structure_types = {
        "Type_of_Structure": [
            "Conventional Structures", "Single Building (Detached)", "One-Storey (Detached)",
            "Single Building (Semi-Detached)", "Two-storey (Semi-Detached)",
            "Multiple-storey (Semi-Detached)", "One-storey (Semi-Detached)",
            "Two Storey (Detached)", "Multiple-storey (Detached)", "Terrace",
            "Wooden Structures", "Kiosks", "Metal Containers", "Others"
        ],
        "Rural": [7452, 7181, 17, 247, 0, 0, 5, 2, 0, 0, 47, 33, 44, 1],
        "Urban": [9268, 9143, 29, 74, 3, 4, 2, 7, 6, 0, 185, 158, 782, 1]
    }
    type_df = pd.DataFrame(structure_types)
    type_melted = type_df.melt("Type_of_Structure", var_name="Locality", value_name="Count")
    
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


    # --- Tabs Without Education ---
    tab1, tab2, tab3 = st.tabs([
        "Residential Completion", 
        "Structure Completion", 
        "Structure Types"
    ])

    with tab1:
        st.subheader("Residential Structure Completion by Locality")
        st.dataframe(res_df)
        chart = alt.Chart(res_melted).mark_bar().encode(
            x=alt.X("Level_of_Completion:N", sort="-y"),
            y=alt.Y("Count:Q"),
            color="Locality:N",
            column=alt.Column("Locality:N"),
            tooltip=["Level_of_Completion", "Count"]
        ).properties(width=350)
        st.altair_chart(chart)

    with tab2:
        st.subheader("Full Structure Completion Status by Locality")
        st.dataframe(struct_df)
        chart = alt.Chart(struct_melted).mark_bar().encode(
            x=alt.X("Level_of_Completion:N", sort="-y"),
            y=alt.Y("Count:Q"),
            color="Locality:N",
            column=alt.Column("Locality:N"),
            tooltip=["Level_of_Completion", "Count"]
        ).properties(width=350)
        st.altair_chart(chart)

    with tab3:
        st.subheader("Types of Residential Structures by Locality")
        st.dataframe(type_df)
        chart = alt.Chart(type_melted).mark_bar().encode(
            x=alt.X("Type_of_Structure:N", sort="-y"),
            y=alt.Y("Count:Q"),
            color="Locality:N",
            column=alt.Column("Locality:N"),
            tooltip=["Type_of_Structure", "Count"]
        ).properties(width=350)
        st.altair_chart(chart)

if __name__ == "__main__":
    app()



