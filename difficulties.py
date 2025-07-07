import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import plotly.graph_objects as go
import networkx as nx
import altair as alt

def app():
    
    # App Heading
    st.markdown("""
    # 🏫 Disability
    ### Analysis of Speech, Hearing, Seeing,Physical,Selfcare,Remembering and Severity of Disability
    """)
    
    speech = pd.read_csv("./difficulties/speech disability_20250703-185627.csv")  # <-- replace with actual filename
    hearing = pd.read_csv("./difficulties/hearingdisability_20250703-182902.csv")
    seeing = pd.read_csv("./difficulties/seeing_disability_20250703-180817.csv")  # Replace with your actual CSV path
    physical = pd.read_csv("./difficulties/physicaldisability_20250703-183809.csv")  # Replace with your correct path
    selfcare = pd.read_csv("./difficulties/selfcaredisability_20250703-184432.csv")
    remembering = pd.read_csv("./difficulties/rememberingdisability_20250703-183318.csv")
    severity = pd.read_csv("./difficulties/severity_20250703-185233.csv")
    
    
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
    # Tabs for sectioning the dashboard
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📘 Speech Disability",
        "📖 Hearing Disability",
        "🧾 SelfCare Disability",
        "🏫 Seeing Disability",
        "🧾 Physical Challenge",
        "🧾 Remembering Disability",
        "🧾 Severity of Disability"
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
        st.markdown("""
            <div style='text-align: center;'>
                <h2>📊 Population Analysis Dashboard</h2>
                <>Population (5 years and older) by Speech, Education, Locality,Sex<br>
            </div>
            """, unsafe_allow_html=True)
        
        # Sidebar filters
        st.header("Filter Options")
        speech_options = speech["Speech"].unique().tolist()
        education_options = speech["Education"].unique().tolist()
        locality_options = speech["Locality"].unique().tolist()
        sex_options = speech["Sex"].unique().tolist()

        selected_speech = st.selectbox("Speech Difficulty", speech_options)
        selected_education = st.multiselect("Education Level", education_options, default=education_options)
        selected_locality = st.selectbox("Locality", locality_options)
        selected_sex = st.selectbox("Sex", sex_options)

        # Apply filters
        f = (
            (speech["Speech"] == selected_speech) &
            (speech["Education"].isin(selected_education)) &
            (speech["Locality"] == selected_locality) &
            (speech["Sex"] == selected_sex)
        )
        filtered = speech[f]

        # Display metrics
        st.title("📊 Community Overview")
        total_people = filtered.iloc[:, 4:].sum().sum()
        st.metric("🧍 Total Individuals", f"{int(total_people):,}")

        # Pie charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🌍 Distribution by Locality")
            pie_loc = speech.groupby("Locality").sum().iloc[:, 4:].sum(axis=1).reset_index()
            pie_loc.columns = ["Locality", "Count"]
            fig_loc = px.pie(pie_loc, names="Locality", values="Count",
                            template="plotly_dark",
                            title="All Speech+Education Groups",
                            color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig_loc, use_container_width=True)
            st.markdown("""
            <div style='text-align: justify'>
            🧾 **Insight**<br>
            🔍 Urban areas contribute a larger share of the population under reported speech categories. This may reflect urban concentration and/or better detection/reporting infrastructure.
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("### 🚻 Distribution by Sex")
            pie_sex = speech.groupby("Sex").sum().iloc[:, 4:].sum(axis=1).reset_index()
            pie_sex.columns = ["Sex", "Count"]
            fig_sex = px.pie(pie_sex, names="Sex", values="Count",
                            template="plotly_dark",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            title="All Speech+Education Groups")
            st.plotly_chart(fig_sex, use_container_width=True)
            st.markdown("""
            <div style='text-align: justify'>
            🧾 **Insight**<br>
            🔍 Males and females appear nearly equal in representation. If differences emerge in specific categories on breakdown, further investigation is warranted.
            </div>
            """, unsafe_allow_html=True)

        # Speech difficulty distribution
        st.markdown("### 🗣 Speech Difficulty Overview")
        pie_speech = speech.groupby("Speech").sum().iloc[:, 4:].sum(axis=1).reset_index()
        pie_speech.columns = ["Speech", "Count"]
        fig_speech = px.pie(pie_speech, names="Speech", values="Count",
                            template="plotly_dark",
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            title="Distribution by Speech Difficulty")
        st.plotly_chart(fig_speech, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify'>
        🧾 **Insight**<br>
        🔍 Most individuals report **no difficulty** in speech. However, non-trivial proportions with *some* or *a lot of difficulty* exist – these signal areas where supportive communication services may be essential.
        </div>
        """, unsafe_allow_html=True)

        # Age distribution bar chart
        st.markdown("### 📈 Age Group Distribution")
        age_cols = speech.columns[4:]
        age_sums = filtered[age_cols].sum().rename_axis("Age Group").reset_index(name="Count")
        fig_age = px.bar(age_sums, x="Age Group", y="Count",
                        template="plotly_dark",
                        color="Count", color_continuous_scale="Plasma",
                        title=f"Age Breakdown — Filtered ({selected_speech}, {selected_education}, {selected_locality}, {selected_sex})")
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify'>
        🧾 **Insight**<br>
        🔍 The population is skewed towards younger age brackets, notably 5–9 through 20–24. If policy aims to support early intervention or schooling, this demographic trend is key.
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        st.markdown("""
            <div style='text-align: center;'>
                <h2>📊 Population Analysis Dashboard</h2>
                <h4>Population (5 years and older) by Hearing, Education, Locality,<br>
                Sex, and Age</h4>
            </div>
            """, unsafe_allow_html=True)

        st.header("🔍 Filter Options")

        # Add "All" to options
        hearing_options = ["All"] + hearing["Hearing"].dropna().unique().tolist()
        education_options = ["All"] + hearing["Education"].dropna().unique().tolist()
        locality_options = ["All"] + hearing["Locality"].dropna().unique().tolist()
        sex_options = ["All"] + hearing["Sex"].dropna().unique().tolist()

        # Create 4 columns for filters
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            selected_hearing = st.radio("Hearing", hearing_options, key="hearing_radio_tab2", horizontal=True)

        with col2:
            selected_education = st.radio("Education", education_options, key="education_radio_tab2", horizontal=True)

        with col3:
            selected_locality = st.radio("Locality", locality_options, key="locality_radio_tab2", horizontal=True)

        with col4:
            selected_sex = st.radio("Sex", sex_options, key="sex_radio_tab2", horizontal=True)

        # Apply filters
        filtered = hearing.copy()
        if selected_hearing != "All":
            filtered = filtered[filtered["Hearing"] == selected_hearing]
        if selected_education != "All":
            filtered = filtered[filtered["Education"] == selected_education]
        if selected_locality != "All":
            filtered = filtered[filtered["Locality"] == selected_locality]
        if selected_sex != "All":
            filtered = filtered[filtered["Sex"] == selected_sex]

        # Display metrics
        st.title("🦻 Hearing Difficulty - Community Overview")
        total_people = filtered.iloc[:, 4:].sum().sum()
        st.metric("🧍 Total Individuals", f"{int(total_people):,}")

        # Pie charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🌍 Distribution by Locality")
            pie_loc = hearing.groupby("Locality").sum().iloc[:, 4:].sum(axis=1).reset_index()
            pie_loc.columns = ["Locality", "Count"]
            fig_loc = px.pie(
                pie_loc, names="Locality", values="Count",
                template="plotly_dark", title="All Hearing+Education Groups",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig_loc, use_container_width=True)
            st.markdown("""
            <div style='text-align: justify'>
            🧾 **Insight**<br>
            🔍 Urban areas may report more hearing difficulty cases — potentially due to better diagnostic access or population size. Rural discrepancies may reflect underreporting or access barriers.
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("### 🚻 Distribution by Sex")
            pie_sex = hearing.groupby("Sex").sum().iloc[:, 4:].sum(axis=1).reset_index()
            pie_sex.columns = ["Sex", "Count"]
            fig_sex = px.pie(
                pie_sex, names="Sex", values="Count",
                template="plotly_dark", title="All Hearing+Education Groups",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig_sex, use_container_width=True)
            st.markdown("""
            <div style='text-align: justify'>
            🧾 **Insight**<br>
            🔍 Male and female distributions are relatively balanced. Deeper analysis might explore age-adjusted hearing trends by gender.
            </div>
            """, unsafe_allow_html=True)

        # Hearing difficulty distribution
        st.markdown("### 👂 Hearing Difficulty Overview")
        pie_hearing = hearing.groupby("Hearing").sum().iloc[:, 4:].sum(axis=1).reset_index()
        pie_hearing.columns = ["Hearing", "Count"]
        fig_hearing = px.pie(
            pie_hearing, names="Hearing", values="Count",
            template="plotly_dark", title="Distribution by Hearing Difficulty",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_hearing, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify'>
        🧾 **Insight**<br>
        🔍 Most individuals report **no difficulty** hearing. However, individuals with *some* or *a lot* of hearing difficulty still represent a meaningful share, which could impact education and communication.
        </div>
        """, unsafe_allow_html=True)

        # Age distribution bar chart
        st.markdown("### 📈 Age Group Distribution")
        age_cols = hearing.columns[4:]
        age_sums = filtered[age_cols].sum().rename_axis("Age Group").reset_index(name="Count")
        fig_age = px.bar(
            age_sums, x="Age Group", y="Count",
            template="plotly_dark", color="Count", color_continuous_scale="Plasma",
            title=f"Age Breakdown — Filtered ({selected_hearing}, {selected_education}, {selected_locality}, {selected_sex})"
        )
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown("""
        <div style='text-align: justify'>
        🧾 **Insight**<br>
        🔍 Hearing challenges may be more prevalent among older individuals, though early-onset cases exist. Age-specific support strategies are vital.
        </div>
        """, unsafe_allow_html=True)
        
    

    with tab3:
        st.markdown("""
            <div style='text-align: center;'>
                <h2>👁️ Selfcare Difficulty Dashboard</h2>
                <h4>Population (5 years and older) by Selfcare, Education, Locality,<br>
                Geographic Area, Sex, and Age</h4>
            </div>
            """, unsafe_allow_html=True)

        # Sidebar Filters with unique keys
        st.title("🔍 Filter Options")
        selfcare_options = selfcare["Selfcare"].unique()
        edu_options = selfcare["Education"].unique()
        locality_options = selfcare["Locality"].unique()
        sex_options = selfcare["Sex"].unique()

        selected_selfcare = st.multiselect(
            "Selfcare Difficulty", 
            options=selfcare_options, 
            default=selfcare_options, 
            key="selfcare_select"
        )

        selected_edu = st.multiselect(
            "Education Level", 
            options=edu_options, 
            default=edu_options, 
            key="edu_select"
        )

        selected_locality = st.multiselect(
            "Locality", 
            options=locality_options, 
            default=locality_options, 
            key="locality_select"
        )

        selected_sex = st.multiselect(
            "Sex", 
            options=sex_options, 
            default=sex_options, 
            key="sex_select"
        )

        # Filter Data
        filtered_df = selfcare[
            (selfcare["Selfcare"].isin(selected_selfcare)) &
            (selfcare["Education"].isin(selected_edu)) &
            (selfcare["Locality"].isin(selected_locality)) &
            (selfcare["Sex"].isin(selected_sex))
        ]

        # Sum population across all age groups
        age_columns = selfcare.columns[4:]  # Skips 'Selfcare', 'Education', 'Locality', 'Sex'
        filtered_df["Total"] = filtered_df[age_columns].sum(axis=1)

        # Metrics Display
        total_population = int(filtered_df["Total"].sum())
        st.metric("👥 Total Population (Filtered)", f"{total_population:,}")

        if not filtered_df.empty:
            # Bar Chart for Age Distribution
            age_data = filtered_df[age_columns].sum().reset_index()
            age_data.columns = ["Age Group", "Population"]

            fig_bar = px.bar(age_data, x="Age Group", y="Population", title="📊 Age Distribution",color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig_bar, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                # ---------------- PIE CHART: Sex Distribution ----------------
                sex_grouped = selfcare[
                    (selfcare["Selfcare"].isin(selected_selfcare)) &
                    (selfcare["Education"].isin(selected_edu)) &
                    (selfcare["Locality"].isin(selected_locality))
                ].copy()
                sex_grouped["Total"] = sex_grouped[age_columns].sum(axis=1)
                sex_data = sex_grouped.groupby("Sex")["Total"].sum().reset_index()

                fig_sex = px.pie(sex_data, names="Sex", values="Total", title="🧑🏽‍🤝‍🧑🏼 Sex Distribution",
                                color_discrete_sequence=px.colors.sequential.Plasma)
                st.plotly_chart(fig_sex, use_container_width=True)

            with col2:    
                # ---------------- PIE CHART: Locality Distribution ----------------
                locality_grouped = selfcare[
                    (selfcare["Selfcare"].isin(selected_selfcare)) &
                    (selfcare["Education"].isin(selected_edu)) &
                    (selfcare["Sex"].isin(selected_sex))
                ].copy()
                locality_grouped["Total"] = locality_grouped[age_columns].sum(axis=1)
                locality_data = locality_grouped.groupby("Locality")["Total"].sum().reset_index()

                fig_locality = px.pie(locality_data, names="Locality", values="Total", title="📍 Locality Distribution",
                                    color_discrete_sequence=px.colors.sequential.Plasma)
                st.plotly_chart(fig_locality, use_container_width=True)

            # ---------------- FUNNEL CHART: Education Level Funnel ----------------
            edu_funnel = selfcare[
                (selfcare["Selfcare"].isin(selected_selfcare)) &
                (selfcare["Locality"].isin(selected_locality)) &
                (selfcare["Sex"].isin(selected_sex))
            ].copy()

            edu_funnel["Total"] = edu_funnel[age_columns].sum(axis=1)
            funnel_data = edu_funnel.groupby("Education")["Total"].sum().reset_index()
            funnel_data = funnel_data.sort_values("Total", ascending=False)

            fig_funnel = px.funnel(
                funnel_data,
                x="Total",
                y="Education",
                color_discrete_sequence=px.colors.sequential.Plasma,
                title="🔻 Education Funnel Chart (Population by Education Level)",
                color="Education"
            )

            fig_funnel.update_layout(
                height=600,
                funnelmode="stack",
                margin=dict(t=60, b=60, l=60, r=60),
                font=dict(size=14)
            )

            fig_funnel.update_traces(marker=dict(opacity=0.9, line=dict(width=1, color='black')))

            st.plotly_chart(fig_funnel, use_container_width=True)
        else:
            st.warning("⚠️ No data available for the selected filters.")

        
    with tab6:
        
        # Melt the dataframe into long format
        age_cols = remembering.columns[4:]  # all age group columns
        df_long = remembering.melt(id_vars=["Intellectual", "Education", "Locality", "Sex"],
                        value_vars=age_cols,
                        var_name="Age_Group",
                        value_name="Population")

        # Sidebar filters
        st.header("Filter Options")
        intellectual_filter = st.multiselect("Select Intellectual Difficulty", remembering["Intellectual"].unique(), default=remembering["Intellectual"].unique())
        edu_filter = st.multiselect("Select Education Level", remembering["Education"].unique(), default=remembering["Education"].unique())
        locality_filter = st.multiselect("Select Locality", remembering["Locality"].unique(), default=remembering["Locality"].unique())
        sex_filter = st.multiselect("Select Sex", remembering["Sex"].unique(), default=remembering["Sex"].unique())

        # Apply filters
        filtered_df = df_long[
            (df_long["Intellectual"].isin(intellectual_filter)) &
            (df_long["Education"].isin(edu_filter)) &
            (df_long["Locality"].isin(locality_filter)) &
            (df_long["Sex"].isin(sex_filter))
        ]

        st.title("📊 Intellectual Difficulty Dashboard")
        st.subheader("Population Distribution by Age Groups")

        # Line Chart
        st.plotly_chart(
            px.line(filtered_df, x="Age_Group", y="Population",
                    color="Education", line_dash="Sex", markers=True,
                    title="Population Trends by Age Group"),
            use_container_width=True
        )

        # Bar Chart
        st.plotly_chart(
            px.bar(filtered_df, x="Age_Group", y="Population",
                color="Sex", barmode="group",
                facet_col="Locality", facet_row="Intellectual",
                title="Population Breakdown by Age, Sex, and Locality"),
            use_container_width=True
        )

        # Optional: Data Table
        st.dataframe(filtered_df)
        
    with tab5:
        
        st.title("Population (5 years and older) by Physical, Education, Locality, Geographic_Area, Sex and Age")
        # Melt the age columns into a long format for easier filtering/plotting
        age_columns = physical.columns[4:]  # Assuming first 4 are: Physical, Education, Locality, Sex
        df_melted = physical.melt(id_vars=["Physical", "Education", "Locality", "Sex"],
                            value_vars=age_columns,
                            var_name="Age Group",
                            value_name="Population")

        # === Sidebar Filters ===
        st.header("💪 Physical Difficulty Filter Options")
        physical_options = df_melted["Physical"].unique()
        education_options = df_melted["Education"].unique()
        locality_options = df_melted["Locality"].unique()
        sex_options = df_melted["Sex"].unique()

        selected_physical = st.selectbox("Select Physical Difficulty", physical_options)
        selected_education = st.selectbox("Select Education Level", education_options)
        selected_locality = st.selectbox("Select Locality", locality_options)
        selected_sex = st.selectbox("Select Sex", sex_options)

        # Filter data
        filtered_df = df_melted[
            (df_melted["Physical"] == selected_physical) &
            (df_melted["Education"] == selected_education) &
            (df_melted["Locality"] == selected_locality) &
            (df_melted["Sex"] == selected_sex)
        ]

        # === Visualization ===
        st.markdown("### 📊 Age Distribution for Selected Filters")
        fig = px.bar(filtered_df, x="Age Group", y="Population", color="Age Group", text="Population",color_discrete_sequence=px.colors.sequential.Plasma)
        fig.update_layout(xaxis_title="Age Group", yaxis_title="Population", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # === Display Data ===
        st.markdown("### 📄 Filtered Data Table")
        st.dataframe(filtered_df)
        
                # Section: Pie Charts for Categorical Variables
        st.header("📊 Pie Charts for Categorical Variables")

        # Create two rows with two columns each
        col1, col2 = st.columns(2)

        with col1:
            physical_counts = physical['Physical'].value_counts().reset_index()
            physical_counts.columns = ['Physical', 'Count']
            fig1 = px.pie(physical_counts, names='Physical', values='Count', title='Distribution of Physical Difficulty')
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            edu_counts = physical['Education'].value_counts().reset_index()
            edu_counts.columns = ['Education', 'Count']
            fig2 = px.pie(edu_counts, names='Education', values='Count',
                          title='Distribution of Education Levels',color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            locality_counts = physical['Locality'].value_counts().reset_index()
            locality_counts.columns = ['Locality', 'Count']
            fig3 = px.pie(locality_counts, names='Locality', values='Count', title='Distribution of Localities')
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            sex_counts = physical['Sex'].value_counts().reset_index()
            sex_counts.columns = ['Sex', 'Count']
            fig4 = px.pie(sex_counts, names='Sex', values='Count', title='Distribution by Sex',color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig4, use_container_width=True)
   

    
    
    
    
    
if __name__ == "__main__":
    app()  
    





