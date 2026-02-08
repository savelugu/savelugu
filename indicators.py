import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from math import ceil

def app():
    """Multidimensional Poverty Index (MPI) Calculator"""
    
    st.set_page_config(
        page_title="MPI Calculator",
        page_icon="📊",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .dimension-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
    }
    .indicator-row {
        padding: 10px;
        margin: 5px 0;
        background-color: white;
        border-radius: 5px;
        border-left: 3px solid #2196F3;
    }
    .weight-badge {
        background-color: #FF9800;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
        margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.title("📊 Multidimensional Poverty Index (MPI) Calculator")
    st.markdown("### Ghana Deprivation Indicators and Weights")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Indicators", "🧮 Calculator", "📈 Visualization", "📊 About MPI"])
    
    # Tab 1: Indicators Table
    with tab1:
        st.header("MPI Dimensions and Indicators")
        
        # Data for the table
        mpi_data = [
            ["Living Standards", "Cooking fuel", "Deprived if household uses solid fuels and cooking is not done outside the house or in the open/ or cooking is undertaken in enclosed spaces", "1/28", "1/4"],
            ["Living Standards", "Water", "Deprived if a household's drinking water is from an unclean source (tanker supply/vendor provided; unprotected well; unprotected spring; river/stream; dugout/pond/lake/dam/canal; other) or a round trip distance to collect water takes 30 minutes or more", "1/28", "1/4"],
            ["Living Standards", "Assets", "Deprived if household does not have more than one small asset (radio, TV, telephone, bike, motorbike, refrigerator, or computer) and does not own a car", "1/28", "1/4"],
            ["Living Standards", "Housing", "Deprived if household uses inadequate flooring (earth/mud, other) or walls (earth/mud, palm leaves/thatch (grass/raffia), other)", "1/28", "1/4"],
            ["Living Standards", "Overcrowding", "Deprived if household has more than 3 people per sleeping room, on average", "1/28", "1/4"],
            ["Living Standards", "Electricity", "Deprived if household does not have electric power", "1/28", "1/4"],
            ["Living Standards", "Toilet", "Deprived if household has no toilet facilities, uses bucket/pan, public toilet, shared toilet outside the house, other", "1/28", "1/4"],
            ["Education", "School attendance", "Deprived if any school-age child (4-15 years) in the household is not attending school", "1/12", "1/4"],
            ["Education", "School attainment", "Deprived if no household member has received at least 9 years of schooling", "1/12", "1/4"],
            ["Education", "School lag", "Deprived if household has any member who is 2 or more years behind in school", "1/12", "1/4"],
            ["Health", "Mortality", "A household is deprived if either a child (<5 years) or a pregnant mother died in the household", "1/8", "1/4"],
            ["Health", "Health insurance", "Deprived if anyone in the household is not covered by the national health insurance scheme", "1/8", "1/4"],
            ["Wage Employment", "Employment", "Deprived if no member 15 years and older in the household is employed", "1/4", "1/4"],
        ]
        
        # Create DataFrame
        df = pd.DataFrame(mpi_data, columns=["Dimension", "Indicator", "Deprivation Cut-off Definition", "Indicator Weight", "Dimension Weight"])
        
        # Convert weights to numeric
        df["Indicator Weight Value"] = df["Indicator Weight"].apply(lambda x: eval(x))
        df["Dimension Weight Value"] = df["Dimension Weight"].apply(lambda x: eval(x))
        
        # Display data
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.dataframe(df[["Dimension", "Indicator", "Deprivation Cut-off Definition", "Indicator Weight"]], 
                        use_container_width=True,
                        height=600)
        
        with col2:
            # Summary statistics
            st.subheader("Summary")
            
            # Counts
            dimensions = df["Dimension"].unique()
            st.metric("Total Dimensions", len(dimensions))
            st.metric("Total Indicators", len(df))
            
            # Weight distribution
            weight_df = df.groupby("Dimension")["Indicator Weight Value"].sum().reset_index()
            weight_df.columns = ["Dimension", "Total Weight"]
            weight_df["Percentage"] = (weight_df["Total Weight"] * 100).round(1)
            
            fig = px.pie(weight_df, values="Total Weight", names="Dimension",
                        title="Weight Distribution by Dimension",
                        hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: Calculator
    with tab2:
        st.header("🏠 Household Poverty Assessment Calculator")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Household Information
            st.subheader("Household Information")
            household_size = st.number_input("Household Size", min_value=1, max_value=20, value=5)
            
            # Create expanders for each dimension
            deprivation_scores = {}
            
            with st.expander("🏠 Living Standards (7 indicators)", expanded=True):
                cooking_fuel = st.selectbox("Cooking Fuel", 
                                           ["Clean fuel with proper ventilation", "Solid fuel in enclosed space", "Solid fuel in open space"],
                                           help="Select based on cooking fuel type and location")
                deprivation_scores["cooking_fuel"] = 1 if cooking_fuel == "Solid fuel in enclosed space" else 0
                
                water_source = st.selectbox("Drinking Water Source",
                                          ["Piped water into dwelling", "Protected well/spring", "Unclean source or >30min walk"],
                                          help="Consider source quality and collection time")
                deprivation_scores["water"] = 1 if water_source == "Unclean source or >30min walk" else 0
                
                assets = st.multiselect("Household Assets",
                                       ["Radio", "TV", "Telephone", "Bicycle", "Motorbike", "Refrigerator", "Computer", "Car"],
                                       default=["Radio", "TV"],
                                       help="Select all assets owned")
                deprivation_scores["assets"] = 1 if (len(assets) <= 1 and "Car" not in assets) else 0
                
                housing_material = st.selectbox("Flooring and Walls",
                                               ["Adequate (cement/bricks)", "Inadequate (earth/mud, thatch)"],
                                               help="Consider both flooring and wall materials")
                deprivation_scores["housing"] = 1 if housing_material == "Inadequate (earth/mud, thatch)" else 0
                
                overcrowding = st.number_input("Persons per sleeping room", min_value=0.5, max_value=10.0, value=2.5, step=0.5)
                deprivation_scores["overcrowding"] = 1 if overcrowding > 3 else 0
                
                electricity = st.radio("Electricity Access", ["Has electricity", "No electricity"])
                deprivation_scores["electricity"] = 1 if electricity == "No electricity" else 0
                
                toilet = st.selectbox("Toilet Facilities",
                                     ["Private flush toilet", "Shared flush toilet", "Public toilet", "Bucket/pan", "No toilet"],
                                     help="Type of toilet facility used")
                deprivation_scores["toilet"] = 1 if toilet in ["Public toilet", "Bucket/pan", "No toilet"] else 0
            
            with st.expander("🎓 Education (3 indicators)"):
                school_attendance = st.radio("School Attendance (children 4-15)",
                                            ["All attending", "Some not attending"],
                                            help="Are all school-age children attending school?")
                deprivation_scores["school_attendance"] = 1 if school_attendance == "Some not attending" else 0
                
                school_attainment = st.radio("Highest Education Level",
                                            ["At least one member completed 9+ years", "No member completed 9+ years"],
                                            help="Highest education level in household")
                deprivation_scores["school_attainment"] = 1 if school_attainment == "No member completed 9+ years" else 0
                
                school_lag = st.radio("School Lag",
                                     ["No members behind in school", "Some members 2+ years behind"],
                                     help="Are any members significantly behind in school?")
                deprivation_scores["school_lag"] = 1 if school_lag == "Some members 2+ years behind" else 0
            
            with st.expander("🏥 Health (2 indicators)"):
                mortality = st.radio("Child/Pregnancy Mortality (last 5 years)",
                                   ["No deaths", "Child (<5) or pregnant mother died"],
                                   help="Any child or maternal deaths in last 5 years")
                deprivation_scores["mortality"] = 1 if mortality == "Child (<5) or pregnant mother died" else 0
                
                health_insurance = st.radio("Health Insurance Coverage",
                                          ["All members covered", "Some members not covered"],
                                          help="National Health Insurance Scheme coverage")
                deprivation_scores["health_insurance"] = 1 if health_insurance == "Some members not covered" else 0
            
            with st.expander("💼 Employment (1 indicator)"):
                employment = st.radio("Employment Status (members 15+)",
                                     ["At least one employed", "No one employed"],
                                     help="Employment status of household members 15+")
                deprivation_scores["employment"] = 1 if employment == "No one employed" else 0
        
        with col2:
            # Calculate MPI Score
            st.subheader("MPI Calculation")
            
            # Define weights
            weights = {
                "cooking_fuel": 1/28,
                "water": 1/28,
                "assets": 1/28,
                "housing": 1/28,
                "overcrowding": 1/28,
                "electricity": 1/28,
                "toilet": 1/28,
                "school_attendance": 1/12,
                "school_attainment": 1/12,
                "school_lag": 1/12,
                "mortality": 1/8,
                "health_insurance": 1/8,
                "employment": 1/4
            }
            
            # Calculate weighted deprivation score
            if deprivation_scores:
                weighted_deprivations = {}
                total_score = 0
                
                for indicator, score in deprivation_scores.items():
                    weighted_score = score * weights.get(indicator, 0)
                    weighted_deprivations[indicator] = weighted_score
                    total_score += weighted_score
                
                # Display results
                st.markdown("### 📊 Results")
                
                # MPI Score
                st.metric("MPI Score", f"{total_score:.3f}")
                
                # Interpretation
                if total_score >= 0.33:
                    st.error("🏚️ **Multidimensionally Poor**")
                    st.info("Household is deprived in at least 33% of weighted indicators")
                elif total_score >= 0.20:
                    st.warning("⚠️ **Vulnerable to Poverty**")
                    st.info("Household is deprived in 20-33% of weighted indicators")
                else:
                    st.success("✅ **Not Multidimensionally Poor**")
                    st.info("Household is deprived in less than 20% of weighted indicators")
                
                # Deprivation count
                deprivation_count = sum(deprivation_scores.values())
                st.metric("Indicators Deprived", f"{deprivation_count}/13")
                
                # Visualize deprivation by dimension
                dimension_deprivations = {
                    "Living Standards": sum([deprivation_scores.get(k, 0) for k in ["cooking_fuel", "water", "assets", "housing", "overcrowding", "electricity", "toilet"]]),
                    "Education": sum([deprivation_scores.get(k, 0) for k in ["school_attendance", "school_attainment", "school_lag"]]),
                    "Health": sum([deprivation_scores.get(k, 0) for k in ["mortality", "health_insurance"]]),
                    "Employment": deprivation_scores.get("employment", 0)
                }
                
                # Create bar chart
                fig = go.Figure(data=[
                    go.Bar(x=list(dimension_deprivations.keys()),
                          y=list(dimension_deprivations.values()),
                          marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
                ])
                fig.update_layout(title="Deprivations by Dimension",
                                 xaxis_title="Dimension",
                                 yaxis_title="Number of Indicators Deprived",
                                 height=300)
                st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Visualization
    with tab3:
        st.header("📈 MPI Visualizations")
        
        # Create sample data for visualization - FIXED: Using np.random
        sample_households = pd.DataFrame({
            'Household': [f'HH{i:02d}' for i in range(1, 21)],
            'MPI_Score': np.random.uniform(0, 0.5, 20),
            'Region': np.random.choice(['Greater Accra', 'Ashanti', 'Northern', 'Eastern', 'Western'], 20),
            'Urban_Rural': np.random.choice(['Urban', 'Rural'], 20, p=[0.4, 0.6]),
            'Household_Size': np.random.randint(3, 12, 20)
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # MPI Distribution
            fig1 = px.histogram(sample_households, x='MPI_Score',
                               title='Distribution of MPI Scores',
                               nbins=20,
                               color_discrete_sequence=['#4CAF50'])
            st.plotly_chart(fig1, use_container_width=True)
            
            # Urban vs Rural comparison
            fig2 = px.box(sample_households, x='Urban_Rural', y='MPI_Score',
                         title='MPI Scores: Urban vs Rural',
                         color='Urban_Rural',
                         color_discrete_map={'Urban': '#2196F3', 'Rural': '#FF9800'})
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Regional comparison
            fig3 = px.bar(sample_households.groupby('Region')['MPI_Score'].mean().reset_index(),
                         x='Region', y='MPI_Score',
                         title='Average MPI Score by Region',
                         color='MPI_Score',
                         color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig3, use_container_width=True)
            
            # Correlation with household size
            fig4 = px.scatter(sample_households, x='Household_Size', y='MPI_Score',
                             title='MPI Score vs Household Size',
                             trendline='ols',
                             color='Urban_Rural')
            st.plotly_chart(fig4, use_container_width=True)
    
    # Tab 4: About MPI
    with tab4:
        st.header("📚 About Multidimensional Poverty Index")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### What is MPI?
            
            The **Multidimensional Poverty Index (MPI)** measures acute poverty 
            across three dimensions and 13 indicators:
            
            **1. Living Standards (1/4 weight)**
            - Cooking fuel
            - Water
            - Assets
            - Housing
            - Overcrowding
            - Electricity
            - Toilet
            
            **2. Education (1/4 weight)**
            - School attendance
            - School attainment
            - School lag
            
            **3. Health (1/4 weight)**
            - Mortality
            - Health insurance
            
            **4. Wage Employment (1/4 weight)**
            - Employment
            """)
        
        with col2:
            st.markdown("""
            ### How is MPI Calculated?
            
            **Formula:**
            ```
            MPI = (∑ Weight_i × Deprivation_i) / N
            ```
            
            Where:
            - **Weight_i** = Indicator weight (sums to 1)
            - **Deprivation_i** = 1 if deprived, 0 if not
            - **N** = Number of indicators (13)
            
            **Poverty Thresholds:**
            - **MPI ≥ 0.33**: Multidimensionally poor
            - **MPI 0.20-0.33**: Vulnerable to poverty
            - **MPI < 0.20**: Not multidimensionally poor
            
            ### Uses of MPI
            
            1. **Policy targeting** - Identify poorest households
            2. **Program monitoring** - Track poverty reduction
            3. **Resource allocation** - Guide government spending
            4. **International comparisons** - Compare with other countries
            """)
        
        # Add download button for MPI guide
        st.download_button(
            label="📥 Download MPI Methodology Guide",
            data=open("mpi_methodology.txt", "w").write("Multidimensional Poverty Index Methodology\n" + "="*50 + "\n\n"),
            file_name="mpi_guide.txt",
            mime="text/plain"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p><strong>Multidimensional Poverty Index Calculator</strong></p>
            <p>Based on Ghana Statistical Service MPI Methodology | Developed for Policy Analysis</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    app()
