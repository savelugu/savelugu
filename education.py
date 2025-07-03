import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import plotly.graph_objects as go
import networkx as nx
import altair as alt
import plotly.io as pio







# Load data
def app():
    
    # App Heading
    st.markdown("""
    # 🏫 Education Data Dashboard
    ### Analysis of Educational Attainment, Literacy, and School Attendance
    """)
    
    highestleveledu = pd.read_csv("./education/3 years and older by Highestleveledu.csv")  # <-- replace with actual filename
    literacy_status = pd.read_csv("./education/6_years_and_older_by_Literacy_status.csv")
    attending = pd.read_csv("./education/3 years and older currently attending school.csv")  # Replace with your actual CSV path
    attendance = pd.read_csv("./education/attendance.csv")  # Replace with your correct path
    df = pd.read_csv("./education/Literacy_1_20250702-214856.csv")
        

    
    


    
    # Remove unnecessary columns (e.g., 5-Mar, 10-Jun)
    age_columns = [col for col in highestleveledu.columns if col not in ['Highestleveledu', 'Locality', 'Sex']]
    clean_age_cols = [col for col in age_columns if '-' in col or '+' in col]

    # Compute total for each row
    highestleveledu["Total"] = highestleveledu[clean_age_cols].sum(axis=1)
    
        
        # Tabs for sectioning the dashboard
    tab1, tab2, tab3, tab4 = st.tabs([
        "📘 Education Level",
        "📖 Literacy Status",
        "🏫 Currently Attending School",
        "🧾 Attendance by Status"
    ])
    
        # === Tab 1: Education Level ===
    with tab1:
         st.title("📊 Education Level Dashboard by Locality, Sex, and Age Groups")

    # Metric Summary
    total_population = int(highestleveledu["Total"].sum())
    total_males = int(highestleveledu[highestleveledu["Sex"] == "Male"]["Total"].sum())
    total_females = int(highestleveledu[highestleveledu["Sex"] == "Female"]["Total"].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total Population", f"{total_population:,}")
    col2.metric("♂️ Total Males", f"{total_males:,}")
    col3.metric("♀️ Total Females", f"{total_females:,}")

    st.markdown("---")

    # Grouped Bar Chart - by Education Level
    edu_group = highestleveledu.groupby("Highestleveledu")["Total"].sum().reset_index().sort_values("Total", ascending=False)
    fig_edu = px.bar(edu_group, x="Highestleveledu", y="Total", text="Total", color="Highestleveledu",
                    title="Total Population by Education Level")
    st.plotly_chart(fig_edu, use_container_width=True)

    # Filters
    st.header("🔍 Filter Options")
    selected_locality = st.selectbox("Select Locality", ["All"] + sorted(highestleveledu["Locality"].unique().tolist()))
    selected_sex = st.selectbox("Select Sex", ["All", "Male", "Female"])

    filtered_df = highestleveledu.copy()
    if selected_locality != "All":
        filtered_df = filtered_df[filtered_df["Locality"] == selected_locality]
    if selected_sex != "All":
        filtered_df = filtered_df[filtered_df["Sex"] == selected_sex]

    # Chart: Filtered by locality & sex
    edu_filtered = filtered_df.groupby("Highestleveledu")["Total"].sum().reset_index().sort_values("Total", ascending=False)
    fig_filtered = px.bar(edu_filtered, x="Highestleveledu", y="Total", text="Total", color="Highestleveledu",
                        title=f"Filtered: Education Level ({selected_locality}, {selected_sex})")
    st.plotly_chart(fig_filtered, use_container_width=True)

    # Optional Line Chart by Age Groups
    show_age_chart = st.checkbox("📈 Show Age Group Line Chart")
    if show_age_chart:
        st.markdown("### 📈 Age Group Distribution per Education Level")
        long_df = filtered_df.melt(id_vars=["Highestleveledu", "Locality", "Sex"],
                                value_vars=clean_age_cols,
                                var_name="Age Group", value_name="Count")
        age_chart = px.line(long_df.groupby(["Age Group", "Highestleveledu"])["Count"].sum().reset_index(),
                            x="Age Group", y="Count", color="Highestleveledu",
                            markers=True)
        st.plotly_chart(age_chart, use_container_width=True)
        
        # --- AGE GROUP CHARTS ---
    st.markdown("## 👶 Age Group Distribution")

    # Melt age columns for plotting
    long_age_df = filtered_df.melt(id_vars=["Highestleveledu", "Locality", "Sex"],
                                value_vars=age_columns,
                                var_name="Age Group", value_name="Count")

    # Sort age groups correctly
    def sort_age(age_str):
        try:
            return int(age_str.split('-')[0].replace('+', ''))
        except:
            return 999

    long_age_df["Age Sort"] = long_age_df["Age Group"].apply(sort_age)
    long_age_df = long_age_df.sort_values("Age Sort")

    # --- Chart 1: Age Group Totals ---
    age_totals = long_age_df.groupby("Age Group")["Count"].sum().reset_index()
    fig_age_bar = px.bar(age_totals, x="Age Group", y="Count", title="Total Population by Age Group",
                        labels={"Count": "Population"})
    st.plotly_chart(fig_age_bar, use_container_width=True)

    # --- Chart 2: Age Group by Sex ---
    age_by_sex = long_age_df.groupby(["Age Group", "Sex"])["Count"].sum().reset_index()
    fig_age_sex = px.bar(age_by_sex, x="Age Group", y="Count", color="Sex", barmode="group",
                        title="Age Group Distribution by Sex")
    st.plotly_chart(fig_age_sex, use_container_width=True)

    # --- Chart 3: Age Group by Education Level (Optional) ---
    if st.checkbox("📈 Show Line Chart by Education Level and Age Group"):
        age_by_edu = long_age_df.groupby(["Age Group", "Highestleveledu"])["Count"].sum().reset_index()
        fig_age_edu = px.line(age_by_edu, x="Age Group", y="Count", color="Highestleveledu",
                            markers=True, title="Age Group Distribution by Education Level")
        st.plotly_chart(fig_age_edu, use_container_width=True)
        


    # === Tab 2: Literacy Status ===
    with tab2:
            
        st.title("📊 Literacy Status of Population (6 years and older)")
        st.caption("By District, Region, Type of Locality, Age, Sex, and Education")



        # Melt age groups into long format
        age_columns = literacy_status.columns[4:]
        df_melted = literacy_status.melt(
            id_vars=["Literacy_status", "Education", "Locality", "Sex"],
            value_vars=age_columns,
            var_name="Age_Group",
            value_name="Population"
        )

        # Sidebar filters
        st.header("🔎 Filter Data")
        selected_status = st.multiselect("Literacy Status", literacy_status["Literacy_status"].unique(), default=literacy_status["Literacy_status"].unique())
        selected_locality = st.multiselect("Locality", literacy_status["Locality"].unique(), default=literacy_status["Locality"].unique())
        selected_sex = st.multiselect("Sex", literacy_status["Sex"].unique(), default=literacy_status["Sex"].unique())

        filtered_df = df_melted[
            (df_melted["Literacy_status"].isin(selected_status)) &
            (df_melted["Locality"].isin(selected_locality)) &
            (df_melted["Sex"].isin(selected_sex))
        ]

        # === METRICS ===
        st.subheader("📌 Key Metrics")

        total_population = int(filtered_df["Population"].sum())
        total_literate = int(filtered_df[filtered_df["Literacy_status"] == "Literate"]["Population"].sum())
        total_not_literate = int(filtered_df[filtered_df["Literacy_status"] == "Not literate"]["Population"].sum())

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Population", f"{total_population:,}")
        col2.metric("Literate", f"{total_literate:,}")
        col3.metric("Not Literate", f"{total_not_literate:,}")

        # === CHARTS ===
        st.markdown("### 📉 Literacy Status by Age Group")

        fig_line = px.line(
            filtered_df.groupby(["Age_Group", "Literacy_status"])["Population"].sum().reset_index(),
            x="Age_Group", y="Population", color="Literacy_status",
            markers=True, title="Literacy Trend by Age Group"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("### 📊 Literacy Status by Education Level")

        fig_bar = px.bar(
            filtered_df.groupby(["Education", "Literacy_status"])["Population"].sum().reset_index(),
            x="Education", y="Population", color="Literacy_status",
            title="Literacy by Education Level"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("### 🧮 Literacy by Sex")

        fig_pie = px.pie(
            filtered_df.groupby("Sex")["Population"].sum().reset_index(),
            names="Sex", values="Population", title="Population Distribution by Sex",
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # === COMPARISON: Rural vs Urban ===
        # === COMPARISON: Rural vs Urban ===# === COMPARISON: Rural vs Urban ===
        pio.templates.default = "plotly_dark"

    # --- COMPARISON: Rural vs Urban ---
        st.markdown("### 🏘️ Rural vs Urban Comparison")

        df_locality_compare = (
            filtered_df.groupby(["Locality", "Literacy_status"])["Population"]
            .sum()
            .reset_index()
        )

        fig_locality = px.bar(
            df_locality_compare,
            x="Locality",
            y="Population",
            color="Literacy_status",
            barmode="group",
            text="Population",  # 👈 Show values
            color_discrete_map={
                "Literate": "#1f77b4",        # dark blue
                "Not literate": "#7f7f7f"     # dark gray
            },
            title="📌 Literacy Status Comparison: Rural vs Urban"
        )

        # Auto display labels on bars
        fig_locality.update_traces(textposition='outside')

        # Optional: fine-tune layout
        fig_locality.update_layout(
            uniformtext_minsize=8,
            uniformtext_mode='hide'
        )

        st.plotly_chart(fig_locality, use_container_width=True)
    


    # === Tab 3: Currently Attending ===
    with tab3:
            
            # Load and reshape your data
        st.title("📊 Population 3 Years and Older Currently Attending School")
        st.markdown(
        """
        ### by Level, District, Region, Type of Locality, Age, and Sex
        """
        )

        # Sidebar filters
        edu_types = attending["Education_type"].unique()
        localities = attending["Locality"].unique()
        sexes = attending["Sex"].unique()

        selected_edu = st.selectbox("Choose Education Type", edu_types)
        selected_locality = st.selectbox("Choose Locality", localities)
        selected_sex = st.selectbox("Choose Sex", sexes)

        # Filtered Data
        filtered_df = attending[
            (attending["Education_type"] == selected_edu) &
            (attending["Locality"] == selected_locality) &
            (attending["Sex"] == selected_sex)
        ]

        # Melt age columns for plotting
        age_cols = [col for col in attending.columns if col not in ["Education_type", "Locality", "Sex"]]
        melted_df = filtered_df.melt(id_vars=["Education_type", "Locality", "Sex"], 
                                    value_vars=age_cols,
                                    var_name="Age", value_name="Count")

        # Summary Metrics
        total = melted_df["Count"].sum()
        peak_age = melted_df.loc[melted_df["Count"].idxmax()]["Age"]
        peak_value = melted_df["Count"].max()

        st.metric("Total Enrolled", total)
        st.metric("Peak Age Group", peak_age)
        st.metric("Peak Enrollment", peak_value)

        # Line Chart
        st.subheader("Age-wise Enrollment Distribution")
        fig = px.line(melted_df, x="Age", y="Count", markers=True)
        st.plotly_chart(fig, use_container_width=True)

        # Function to show education type comparison
        def show_education_view(edu_type):
            subset = attending[attending["Education_type"] == edu_type]
            rural = subset[subset["Locality"] == "Rural"]
            urban = subset[subset["Locality"] == "Urban"]

            st.subheader(f"{edu_type} - Enrollment Metrics")
            st.metric("Total Rural", rural[age_cols].sum().sum())
            st.metric("Total Urban", urban[age_cols].sum().sum())

            melted = subset.melt(id_vars=["Locality", "Sex"], value_vars=age_cols, 
                                var_name="Age", value_name="Count")

            fig = px.line(melted, x="Age", y="Count", color="Locality", 
                        line_dash="Sex", markers=True, 
                        title=f"{edu_type} Age Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            
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

            
        edu_types = attending["Education_type"].unique().tolist()  # Convert to regular list

        # Dynamic Tabs for top 3 education types
        tab1, tab2, tab3 = st.tabs(edu_types[:3])  # Adjust if fewer than 3 types exist

        with tab1:
            show_education_view(edu_types[0])

        with tab2:
            show_education_view(edu_types[1])

        with tab3:
            show_education_view(edu_types[2])
            
            
        # Define new age group mapping
        # Age group definitions based on actual column names
        age_group_mapping = {
            "3-5 years": ["3", "4", "5"],
            "6-14 years": [str(i) for i in range(6, 15)],
            "15-17 years": ["15", "16", "17"],
            "18-19 years": ["18", "19"],
            "20-24 years": ["20", "21", "22", "23", "24"],
            "25-29 years": ["25", "26", "27", "28", "29"],
            "30 years & older": ["30 years & older"]  # Exact column name
        }

        # Calculate group totals
        grouped_data = {}
        for group, columns in age_group_mapping.items():
            valid_cols = [col for col in columns if col in attending.columns]
            grouped_data[group] = attending[valid_cols].sum().sum()

        # Create DataFrame for chart
        grouped_df = pd.DataFrame({
            "Age Group": list(grouped_data.keys()),
            "Total Enrolled": list(grouped_data.values())
        })

        # Ensure age group order
        ordered_groups = list(age_group_mapping.keys())
        grouped_df["Age Group"] = pd.Categorical(grouped_df["Age Group"], categories=ordered_groups, ordered=True)
        grouped_df.sort_values("Age Group", inplace=True)

        # Plot
        st.subheader("📊 Enrollment by Age Group")
        fig = px.bar(grouped_df, x="Age Group", y="Total Enrolled", text="Total Enrolled",
                    title="Enrollment Distribution by Age Group",
                    labels={"Total Enrolled": "Number of Students"})

        fig.update_traces(marker_color="seagreen", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)


    # === Tab 4: Attendance by Status ===
    with tab4:
            
        # Title
        st.title("📊 Population (3 years and older) by School Attendance")
        st.markdown("### by Schoolattendancestatus, Geographic_Area, Locality, Sex and Age")

        # List of age group columns (adjust if needed)
        age_groups = ["3-5", "6-10", "11-14", "15-19", "20-24", "25-29", "30-34", "35-39",
                    "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", 
                    "75-79", "80-84", "85-89", "90-94", "95-99", "100+"]

        # Sidebar filters
        statuses =  attendance["Schoolattendancestatus"].unique()
        localities =  attendance["Locality"].unique()
        sexes =  attendance["Sex"].unique()

        selected_status = st.selectbox("Select School Attendance Status", statuses)
        selected_locality = st.selectbox("Select Locality", localities)
        selected_sex = st.selectbox("Select Sex", sexes)

        # Filtered data
        filtered_df =  attendance[
            (attendance["Schoolattendancestatus"] == selected_status) &
            (attendance["Locality"] == selected_locality) &
            (attendance["Sex"] == selected_sex)
        ]

        # Calculate total per age group
        age_totals = filtered_df[age_groups].sum().reset_index()
        age_totals.columns = ["Age Group", "Total Enrolled"]

        # Summary metrics
        total_enrolled = age_totals["Total Enrolled"].sum()
        peak_row = age_totals.loc[age_totals["Total Enrolled"].idxmax()]
        peak_age = peak_row["Age Group"]
        peak_value = peak_row["Total Enrolled"]

        # Display metrics
        st.markdown("### 📈 Summary Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Population", f"{total_enrolled:,}")
        col2.metric("Peak Age Group", peak_age)
        col3.metric("Peak Enrollment", f"{peak_value:,}")

        # Bar chart
        st.markdown("### 📊 Age Group Distribution")
        fig = px.bar(age_totals, x="Age Group", y="Total Enrolled", text="Total Enrolled",
                    title=f"Enrollment by Age Group - {selected_status}, {selected_locality}, {selected_sex}",
                    labels={"Total Enrolled": "Number of People", "Age Group": "Age Group"})

        fig.update_traces(marker_color="indianred", textposition="outside")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        

        # Filter for Urban vs Rural comparison
        compare_df = attendance[
            (attendance["Schoolattendancestatus"] == selected_status) &
            (attendance["Sex"] == selected_sex)
        ]

        # Melt for Urban vs Rural comparison
        urban_rural_melted = compare_df.melt(
            id_vars=["Locality"],
            value_vars=age_groups,
            var_name="Age Group",
            value_name="Total Enrolled"
        )

        # Plot grouped bar chart
        st.markdown("### 🏙️ Urban vs Rural: Age Group Comparison")
        fig_compare = px.bar(urban_rural_melted, x="Age Group", y="Total Enrolled",
                            color="Locality", barmode="group", text="Total Enrolled",
                            title=f"Urban vs Rural - {selected_status}, {selected_sex}")

        fig_compare.update_traces(textposition="outside")
        fig_compare.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_compare, use_container_width=True)
        
        col1, col2 = st.columns(2)

        with col1:
            # -------------------------------
            # Pie Chart: Attendance Status Distribution
            # -------------------------------
            st.markdown("### 🥧 School Attendance Status Distribution")

            status_totals = attendance.groupby("Schoolattendancestatus")[age_groups].sum().sum(axis=1).reset_index()
            status_totals.columns = ["Attendance Status", "Total"]

            fig_pie_status = px.pie(
            status_totals,
            values="Total",
            names="Attendance Status",
            title="Distribution by School Attendance Status",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Plasma
            )


            st.plotly_chart(fig_pie_status, use_container_width=True)
            st.markdown("""
            <div style='text-align: justify'>
            🧾 <strong>Insight</strong><br>
            🔍 A significant proportion of children are not currently attending school, with many categorized as "Never attended" or "Dropped out". This suggests barriers such as poverty, long distances to schools, or cultural factors impacting education in Savelugu.
            </div>
            """, unsafe_allow_html=True)
        with col2:
            # -------------------------------
            # Pie Chart: Sex Distribution
            # -------------------------------
            st.markdown("### 👥 School Attendance Sex Distribution")

            sex_totals = attendance.groupby("Sex")[age_groups].sum().sum(axis=1).reset_index()
            sex_totals.columns = ["Sex", "Total"]

            fig_pie_sex = px.pie(
                sex_totals,
                values="Total",
                names="Sex",
                title="Distribution by Sex",
                template="plotly_dark",  # Dark mode applied here too
                color_discrete_sequence=px.colors.sequential.Plasma
            )

            st.plotly_chart(fig_pie_sex, use_container_width=True)
            st.markdown("""
            <div style='text-align: justify'>
            🧾 <strong>Insight</strong><br>
            🔍 While school attendance is similar between sexes, females are slightly underrepresented at higher education levels. Gender-related challenges such as early marriage and domestic responsibilities may be contributing factors.
            </div>
            """, unsafe_allow_html=True)
            
    

        # Define age groups
        age_columns = [col for col in df.columns if col not in ["Language_of_Literacy", "Education", "Locality", "Sex"]]

        # Sidebar filters
        st.header("Filter Options")
        selected_language = st.multiselect("Language of Literacy", df["Language_of_Literacy"].unique())
        selected_education = st.multiselect("Education Level", df["Education"].unique())
        selected_locality = st.multiselect("Locality", df["Locality"].unique())
        selected_sex = st.multiselect("Sex", df["Sex"].unique())

        # Apply filters
        filtered_df = df.copy()
        if selected_language:
            filtered_df = filtered_df[filtered_df["Language_of_Literacy"].isin(selected_language)]
        if selected_education:
            filtered_df = filtered_df[filtered_df["Education"].isin(selected_education)]
        if selected_locality:
            filtered_df = filtered_df[filtered_df["Locality"].isin(selected_locality)]
        if selected_sex:
            filtered_df = filtered_df[filtered_df["Sex"].isin(selected_sex)]

        # Layout
        st.title("Population (6 older) by Language_of_Literacy, Education, Locality, Sex and Age")

        st.subheader("Demographics")
        st.dataframe(filtered_df[["Language_of_Literacy", "Education", "Locality", "Sex",
                                  "6-11", "12-14", "15-19", "20-24", "25-29", "30-34",
                                "35-39", "40-44", "45-49", "50-54", "55-59", "60-64",
                                "65-69", "70-74", "75-79", "80-84", "85-89", "90-94",
                                "95-99", "100+"]])

        st.subheader("Age Distribution")
        st.dataframe(filtered_df[age_columns])

        # Optional: Display summary totals across age groups
        st.subheader("Summary Statistics")
        age_totals = filtered_df[age_columns].sum().reset_index()
        age_totals.columns = ["Age Group", "Total Population"]
        st.bar_chart(age_totals.set_index("Age Group"))

    
    
if __name__ == "__main__":
    app() 
