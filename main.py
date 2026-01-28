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
# Enhanced Professional Sidebar with Modern Design
with st.sidebar:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Base styles */
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* Logo Container with Enhanced Glow */
        .logo-container {{
            background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
            padding: 25px 20px;
            border-radius: 20px;
            text-align: center;
            border: 1px solid rgba(21, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
            margin-bottom: 30px;
            box-shadow: 
                0 10px 30px rgba(0, 0, 0, 0.5),
                0 0 20px rgba(21, 255, 255, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1);
        }}
        
        .logo-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(21, 255, 255, 0.1),
                transparent
            );
            transition: left 0.7s ease;
        }}
        
        .logo-container:hover {{
            transform: translateY(-2px);
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.6),
                0 0 30px rgba(21, 255, 255, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }}
        
        .logo-container:hover::before {{
            left: 100%;
        }}
        
        /* Logo Image */
        .logo-img {{
            width: 160px;
            height: 160px;
            object-fit: contain;
            margin: 0 auto 15px;
            display: block;
            filter: drop-shadow(0 0 10px rgba(21, 255, 255, 0.3));
            transition: transform 0.4s ease;
        }}
        
        .logo-container:hover .logo-img {{
            transform: scale(1.05);
        }}
        
        /* Title Styling */
        .logo-title {{
            margin: 10px 0 5px;
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, #15ffff 0%, #00b4b4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 0.5px;
        }}
        
        .logo-subtitle {{
            font-size: 13px;
            color: #94a3b8;
            font-weight: 400;
            letter-spacing: 0.3px;
            opacity: 0.9;
        }}
        
        /* Spacer */
        .sidebar-spacer {{
            height: 1px;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(21, 255, 255, 0.2), 
                transparent);
            margin: 25px 0;
        }}
        
        /* Glow Animation */
        @keyframes gentle-glow {{
            0% {{
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.5),
                    0 0 20px rgba(21, 255, 255, 0.15);
            }}
            100% {{
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.5),
                    0 0 25px rgba(21, 255, 255, 0.25);
            }}
        }}
        
        .logo-container {{
            animation: gentle-glow 3s ease-in-out infinite alternate;
        }}
        </style>

        <!-- Logo Section -->
        <div class="logo-container">
            <img src="data:image/png;base64,{cropped_logo}" 
                 alt="Savelugu Logo" 
                 class="logo-img" />
            <h2 class="logo-title">Savelugu Report</h2>
            <p class="logo-subtitle">Municipal Data Analytics Dashboard</p>
        </div>
        
        <!-- Spacer -->
        <div class="sidebar-spacer"></div>
        """,
        unsafe_allow_html=True
    )
    
    # Enhanced Navigation Menu
    app = option_menu(
        menu_title="",
        options=[
            "Savelugu Municipal", "Structures", "Savelugu MPI",
            "Water & Sanitation", "Economic Activities", "Population",
            "Housing", "Fertility", "Education", 
            "Difficulties in Performing Activities"
        ],
        icons=[
            "building", "columns-gap", "graph-up-arrow",
            "droplet-half", "bar-chart-steps", "people",
            "house-door", "heart-pulse", "book",
            "activity"
        ],
        menu_icon="",
        default_index=0,
        styles={
            "container": {
                "padding": "8px",
                "background-color": "#0f172a",
                "border-radius": "12px",
                "border": "1px solid rgba(21, 255, 255, 0.1)",
                "box-shadow": "0 4px 20px rgba(0, 0, 0, 0.3)"
            },
            "icon": {
                "color": "#15ffff",
                "font-size": "20px",
                "margin-right": "12px",
                "transition": "all 0.3s ease"
            },
            "nav-link": {
                "color": "#cbd5e1",
                "font-size": "15px",
                "font-weight": "500",
                "padding": "14px 16px",
                "margin": "3px 0",
                "border-radius": "8px",
                "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                "display": "flex",
                "align-items": "center",
                "gap": "10px"
            },
            "nav-link:hover": {
                "color": "#ffffff",
                "background": "rgba(21, 255, 255, 0.1)",
                "transform": "translateX(5px)",
                "border-left": "3px solid #15ffff"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #0f4c75 0%, #15a3a3 100%)",
                "color": "#ffffff",
                "font-weight": "600",
                "box-shadow": "0 4px 15px rgba(21, 255, 255, 0.25)",
                "border-left": "3px solid #15ffff",
                "transform": "translateX(5px)"
            },
            "menu-title": {
                "display": "none"
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
