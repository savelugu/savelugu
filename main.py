import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import streamlit.components.v1 as components
import requests
from datetime import datetime
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
logo_path = "./Images/ai.png"
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


st.title("🤖 Savelugu Municipal Assembly Dashboard")

st.markdown("""
<style>
body {
  background-color: #0a0a0a;
  margin: 0;
}

/* Center the content horizontally */
.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
}

.circular-frame {
  width: 350px;
  height: 350px;
  border-radius: 50%;
  overflow: hidden;
  border: 6px solid #00FFFF;
  box-shadow: 0 0 30px #00FFFF, 0 0 60px #0ff;
  background: #000;
}
.circular-frame iframe {
  width: 100%;
  height: 100%;
  border: none;
}
</style>

<div class="center-container">
  <div class="circular-frame">
    <iframe title="Wireframe Human Head"
      src="https://sketchfab.com/models/6bb795e00ba34bfe9eb27bc7517019de/embed?autostart=1&autospin=0.8&ui_theme=dark"
      allowfullscreen mozallowfullscreen webkitallowfullscreen>
    </iframe>
  </div>
</div>
""", unsafe_allow_html=True)
        # Define CSS for the continuous sliding animation with 3D text effect
css_animation = """
    <style>
    @keyframes slide {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .sliding-text-container {
        text-align: center;
        font-weight: bold;
        margin-top: 20px;
        overflow: hidden; /* Ensures the text is hidden before it slides in */
        white-space: nowrap; /* Prevents text from wrapping to the next line */
    }

    .sliding-text {
        display: inline-block;
        animation: slide 20s linear infinite;
        font-size: 36px;
        text-align: center;
        color: #00FFFF;
        text-shadow: 1px 1px 0 #000, 2px 2px 0 #000, 3px 3px 0 #000,
                    4px 4px 0 #000, 5px 5px 0 #000, 6px 6px 0 #000,
                    7px 7px 0 #000, 8px 8px 0 #000, 9px 9px 0 #000;
    }
    </style>
    """

    # Insert the CSS into the Streamlit app
st.markdown(css_animation, unsafe_allow_html=True)

    # Insert the HTML for the animated text
html_content = """
    <div class='sliding-text-container'>
        <div class='sliding-text'>Visit Savelugu Municipal</div>
    </div>
    """

st.markdown(html_content, unsafe_allow_html=True)







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
        <img src="data:image/png;base64,{cropped_logo}" alt="Logo" style="width: 170px; margin-bottom: 10px;" />
        <h2>Savelugu Report</h2>
        <p></p>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
    
    # SVG content for the flowing water effect
    svg_content = """
        <svg viewBox="0 0 500 100" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 50 Q 50 90 100 50 T 200 50 T 300 50 T 400 50 T 500 50 V 100 H 0 Z" fill="#00FFFF">
            <animate
            repeatCount="indefinite"
            attributeName="d"
            dur="5s"
            values="M0 50 Q 50 90 100 50 T 200 50 T 300 50 T 400 50 T 500 50 V 100 H 0 Z;
                    M0 50 Q 50 10 100 50 T 200 50 T 300 50 T 400 50 T 500 50 V 100 H 0 Z;
                    M0 50 Q 50 90 100 50 T 200 50 T 300 50 T 400 50 T 500 50 V 100 H 0 Z" />
        </path>
        </svg>
        """

    # Combine CSS and HTML content
    html_content = f"""
        <div class='bumping-text-container'>
            <div class='bumping-text'></div>
        </div>
        <div style="position: absolute; top: 60%; left: 50%; transform: translate(-50%, -50%); width: 100%;">
            {svg_content}
        </div>
        """

        # Add the CSS and HTML to the sidebar
    st.markdown(css_animation, unsafe_allow_html=True)
    st.markdown(html_content, unsafe_allow_html=True)


    app = option_menu(
        menu_title="Navigation",
        options=[
            "Savelugu Municipal", "Structures", "Savelugu MPI",
            "Water & Sanitation", "Economic Activities", "Population","Housing","Fertility","Education","Difficulties in Performing Activities"
        ],
        icons=[
            "building", "columns-gap", "graph-up-arrow",
            "droplet-half", "bar-chart-steps", "people-fill","people-fill","people-fill","people-fill", "speedometer2"
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
    
st.markdown("<h5 style='text-align: center; color: #15FFFF'>Created with ❤️ by Shaz Data Consult</h5>", unsafe_allow_html=True)