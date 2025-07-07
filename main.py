import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import streamlit.components.v1 as components
import structures, mpi, sanitation, economic, population, savelugu, housing, fertility, education, difficulties

# Page configuration
st.set_page_config(
    page_title="Savelugu Municipal Report",
    page_icon="./Images/cropped2.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load and encode image
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Image paths
logo_path = "./Images/coat.png"
cropped_logo = load_image(logo_path)

   # --- CSS Animation for the Header and Glowing Cards ---
css_animation = """
<style>
@keyframes bump {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* Bouncing, glowing heading */
.bumping-text {
    display: inline-block;
    animation: bump 1s infinite;
    font-size: 2.5rem;
    font-weight: bold;
    color: #00ccff;
    text-align: center;
    width: 100%;
    margin-bottom: 2rem;
    white-space: nowrap;
}

/* Glow effect for metric cards */
.metric-glow {
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 12px;
    background: #111;
    color: white;
    box-shadow: 0 0 15px rgba(0, 153, 255, 0.6);
    transition: 0.3s ease-in-out;
}

.metric-glow:hover {
    box-shadow: 0 0 25px rgba(0, 153, 255, 1);
    transform: scale(1.02);
}
</style>
"""

# Inject CSS
st.markdown(css_animation, unsafe_allow_html=True)
# Savelugu coordinates
# Savelugu coordinates# Savelugu coordinates
# Savelugu coordinates
savelugu_coords = {"lat": 9.6245, "lng": -0.8305}

# CSS for column layout and animation
st.markdown(f"""
<style>
@keyframes bump {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-10px); }}
}}

.header-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
    gap: 1rem;
}}

.bumping-text {{
    animation: bump 1.5s infinite;
    font-size: 2.3rem;
    font-weight: bold;
    color: #00ccff;
    margin: 0;
    text-align: center;
}}

.globe-box {{
    width: 200px;
    height: 200px;
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 0 15px rgba(0, 204, 255, 0.4);
}}
</style>
""", unsafe_allow_html=True)

# HTML structure with globe above text
st.markdown(f"""
<div class="header-container">
    <div class="globe-box">
        <iframe srcdoc="
        <html>
          <head>
            <script src='https://unpkg.com/three@0.139.2/build/three.min.js'></script>
            <script src='https://unpkg.com/globe.gl'></script>
            <style>
              html, body {{ margin: 0; padding: 0; overflow: hidden; width: 100%; height: 100%; }}
              #globeViz {{ width: 100%; height: 100%; }}
            </style>
          </head>
          <body>
            <div id='globeViz'></div>
            <script>
              const world = Globe()
                (document.getElementById('globeViz'))
                .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
                .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
                .showAtmosphere(true)
                .atmosphereColor('lightskyblue')
                .atmosphereAltitude(0.5)
                .pointOfView({{ lat: {savelugu_coords['lat']}, lng: {savelugu_coords['lng']}, altitude: 1 }}, 0);
              world.controls().autoRotate = true;
              world.controls().autoRotateSpeed = 1.5;
              world
                .pointsData([{{ lat: {savelugu_coords['lat']}, lng: {savelugu_coords['lng']}, size: 0.25 }}])
                .pointColor(() => 'red')
                .pointAltitude(() => 0.05)
                .pointLabel(() => 'Savelugu');
            </script>
          </body>
        </html>" width="100%" height="100%" style="border:none;"></iframe>
    </div>
    <div class="bumping-text">Savelugu Municipal Demographic Dashboard</div>
</div>
""", unsafe_allow_html=True)




# Sidebar with glowing logo and styled nav
with st.sidebar:
    st.markdown(
    f"""
    <style>
    
    .custom-box {{
        background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        animation: glow 2s ease-in-out infinite alternate;
        color: #ffffff;
        box-shadow: 0 0 12px rgba(21, 255, 255, 0.3);
        transition: all 0.3s ease-in-out;
        margin-bottom: 25px;  /* 👈 This adds space below the logo box */
    }}
    .custom-box h2 {{
        margin: 10px 0;
        font-size: 22px;
        color: #15ffff;
        font-weight: bold;
    }}
    .custom-box p {{
        font-size: 14px;
        margin: 0;
        color: #ccc;
    }}
    </style>

    <div class="custom-box">
        <img src="data:image/png;base64,{cropped_logo}" alt="Logo" style="width: 90px; margin-bottom: 10px;" />
        <h2>Savelugu Report</h2>
        <p>Municipal Dashboard</p>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)


    app = option_menu(
        menu_title="Navigation",
        options=[
            "Savelugu Municipal", "Structures", "Savelugu MPI",
            "Water & Sanitation", "Economic Activities", "Population","Housing","Fertility","Education","Difficulties in Performing Activities"
        ],
        icons=[
            "building", "columns-gap", "graph-up-arrow",
            "droplet-half", "bar-chart-steps", "people-fill","people-fill","people-fill","people-fill"
        ],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {
                "padding": "5px",
                "background-color": "#111111",
                "border-radius": "10px",
            },
            "icon": {
                "color": "#15ffff",
                "font-size": "22px",
                "animation": "glow 2s ease-in-out infinite alternate"
            },
            "nav-link": {
                "color": "#cccccc",
                "font-size": "18px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#15ffff",
                "transition": "0.3s"
            },
            "nav-link-selected": {
                "background-color": "#0f4c75",
                "color": "#ffffff",
                "font-weight": "bold",
                "box-shadow": "0 0 10px #15ffff",
                "border-radius": "8px",
            }
        }
    )

# Google Analytics (optional)
st.markdown(
    f"""
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={os.getenv('analytics_tag')}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{ dataLayer.push(arguments); }}
        gtag('js', new Date());
        gtag('config', '{os.getenv('analytics_tag')}');
    </script>
    """, unsafe_allow_html=True
)

# Debug print
print(os.getenv('analytics_tag'))

# Navigation controller
if app == "Structures":
    structures.app()
elif app == "Savelugu MPI":
    mpi.app()
elif app == "Water & Sanitation":
    sanitation.app()
elif app == "Economic Activities":
    economic.app()
elif app == "Population":
    population.app()
elif app == "Savelugu Municipal":
    savelugu.app()
    
elif app == "Housing":
    housing.app()
elif app == "Fertility":
    fertility.app()
elif app == "Education":
    education.app()
elif app == "Difficulties in Performing Activities":
    difficulties.app()