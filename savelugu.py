import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import base64
import plotly.graph_objects as go
import networkx as nx


def app():

    st.header("📊 Savelugu Municipal Demographics and Development Overview")
    
   

    def load_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    # Define your logo and animation paths
    logo_path = "./Images/combo.gif"
    cropped = "./Images/coat.png"
    # Define a function to create a capacity-building training plan

    
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

    st.markdown("""
        <div style='text-align: justify;'>
        Savelugu Municipal is located in the Northern Region of Ghana. 
        The municipality covers a total land area of 1,550 square kilometers and had a population 
        of 122,888 according to the 2021 Census. This report presents the demographic characteristics, 
        population structure, and development indicators of Savelugu Municipal.
        The Savelugu Municipal Assembly, which until 15th March 2017 when Nanton District was created was called Savelugu-Nanton Municipal Assembly. It was carved out of the then Western Dagomba District in 1988 under PNDC Law 207. In March 2012, the Assembly was upgraded to a Municipal status under L.I 2071.
        </div>
        """, unsafe_allow_html=True)


        # 2. Geographic & Administrative Context
    st.markdown("### 2. Geographic & Administrative Context")
    st.write("""
        Savelugu Municipal lies just north‑west of Tamale, sharing boundaries with Nanton (south‑east), Tolon (west), Karaga (east) and West Mamprusi (north). Created as a separate municipality in 2018, it forms part of Ghana’s Guinea Savannah ecological zone. The terrain is largely flat to gently undulating with vast stretches suited to rain‑fed agriculture as well as seasonal grazing.
        """)

        # Inject custom CSS styles
    st.markdown("""
        <style>
        .section-title {
            font-size: 28px;
            font-weight: bold;
            color: #30c9e8;
            margin-top: 30px;
            text-align: center;
        }

        /* Flip-card container */
        .flip-card {
            background-color: transparent;
            width: 100%;
            height: 220px;
            perspective: 1000px;
            margin-bottom: 30px;
        }

        /* Inner content of flip-card */
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
            transform-style: preserve-3d;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            border-radius: 10px;
        }

        /* Flip on hover */
        .flip-card:hover .flip-card-inner {
            transform: rotateY(180deg);
        }

        /* Front and back side */
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 10px;
            padding: 20px;
            box-sizing: border-box;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Front side */
        .flip-card-front {
            background-color: #1a1a1a;
            font-size: 20px;
            font-weight: bold;
        }

        /* Back side */
        .flip-card-back {
            background-color: #333;
            transform: rotateY(180deg);
            font-size: 16px;
            line-height: 1.6;
            text-align: left;
        }
        </style>
        """, unsafe_allow_html=True)


    st.markdown('<div class="section-title">🎯 Mission, Vision & Core Values</div>', unsafe_allow_html=True)

        # Mission
    st.markdown("""
        <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
            🖋️ Mission
            </div>
            <div class="flip-card-back">
            <ul>
            <div class="section-title">🖋️ Mission</div>
            The Savelugu Municipal Assembly exists to promote grassroots participatory democracy and development, 
            provide effective administrative and technical services to the populace, 
            and create a conducive atmosphere for socio-economic development.
            </ul>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        # Vision
    st.markdown("""
        <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
            🌌 Vision
            </div>
            <div class="flip-card-back">
            <ul>
            <div class="section-title">🌌 Vision</div>
            A population with a high quality of life in a well-managed environment where children, women, and men 
            have equal opportunity, participate in decision-making, and have access to quality and sustained health services, 
            education, and economic resources.
            </ul>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        # Core Values
    st.markdown("""
        <div class="flip-card">
        <div class="flip-card-inner">
            <div class="flip-card-front">
            ⚙️ Core Values
            </div>
            <div class="flip-card-back">
            <ul>
            <div class="section-title">⚙️ Core Values</div>
                <li>🧑‍💼 <b>Professionalism</b></li>
                <li>🧭 <b>Integrity</b></li>
                <li>📊 <b>Accountability</b></li>
                <li>🤝 <b>Client-Oriented Service Delivery</b></li>
            </ul>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)


    # Section: Political Administration
    st.markdown('<div class="section-title">🏛️ Political Administration</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card body-text">
    The Savelugu Assembly is the highest authority for initiating and coordinating development.
    <br><br>
    The <b>MCE</b> oversees day-to-day operations and represents Central Government. The <b>Municipal Coordinating Director</b> supports as head of bureaucracy and Assembly secretary.
    <br><br>
    <b>Zonal Councils (4):</b>
    <ul>
    <li>🏘️ Savelugu Zonal Council</li>
    <li>🏘️ Pong Tamale Zonal Council</li>
    <li>🏘️ Diare Zonal Council</li>
    <li>🏘️ Moglaa Zonal Council</li>
    </ul>
    <br>
    <b>Assembly Members (39):</b>
    <ul>
    <li>🗳️ 25 Elected</li>
    <li>🧾 12 Appointed</li>
    <li>👤 1 Member of Parliament</li>
    <li>🏛️ Municipal Chief Executive</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


    # Section: Location and Size
    st.markdown('<div class="section-title">📍 Location and Size</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card body-text">
    Created in 1988 from Western Dagomba and elevated to Municipal status in 2012.
    <br><br>
    Located in the northern part of the Northern Region:
    <ul>
    <li>⬆️ North: West Mamprusi</li>
    <li>➡️ East: Karaga & Nanton</li>
    <li>⬅️ West: Kumbungu</li>
    <li>⬇️ South: Sagnerigu</li>
    </ul>
    <br>
    <b>Coverage:</b> 81 communities | Land area: <b>2,022.6 sq. km</b>
    </div>
    """, unsafe_allow_html=True)


    # Section: Topography and Geology
    st.markdown('<div class="section-title">⛰️ Topography and Geology</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card body-text">
    Mostly flat with slight undulations (400–800 ft). Southern part slightly hilly.
    <br><br>
    <b>Geology:</b><br>
    <ul>
    <li>🪨 Middle Voltaian (North): Sandstone, shale, siltstone</li>
    <li>🪨 Upper Voltaian (South): Shale, mudstone</li>
    </ul>
    <br>
    💧 Borehole success is higher in the northern zone due to favorable geology.
    </div>
    """, unsafe_allow_html=True)


    # Section: Climate and Rainfall
    st.markdown('<div class="section-title">🌧️ Climate and Rainfall</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card body-text">
    Annual rainfall: <b>600–1000mm</b> (one farming season, starts April)
    <br><br>
    Temperature range: <b>16°C – 42°C</b>
    <br><br>
    🌀 Harmattan season (Dec–Feb) brings low humidity and high evaporation.
    </div>
    """, unsafe_allow_html=True)


    # Section: Drainage and Vegetation
    st.markdown('<div class="section-title">🌿 Drainage and Vegetation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card body-text">
    Drained by the <b>White Volta River</b> and tributaries like <i>Kuldalnali</i> (boundary with Kumbungu).
    <br><br>
    🏞️ Flood-prone northern zones support rice farming.
    <br><br>
    <b>Ecology:</b> Guinea Savannah Woodland
    <ul>
    <li>🌾 Crops: rice, yam, maize, cassava</li>
    <li>🐄 Livestock farming</li>
    <li>🌰 Trees: Shea, Dawadawa (economic trees)</li>
    </ul>
    <br>
    Northern zone: Denser vegetation<br>
    Southern zone: Human degradation (tree felling, bush burning)
    </div>
    """, unsafe_allow_html=True)

   
    st.markdown("### 3. Key Development Metrics")

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
    
    
    .circle {
        display: inline-block;
        width: 48px;
        height: 48px;
        line-height: 48px;
        margin-right: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0d0887, #f0f921);
        color: #000;
        font-weight: bold;
        text-align: center;
        font-size: 14px;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
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
    .circle {
        display: inline-block;
        width: 48px;
        height: 48px;
        line-height: 48px;
        margin-right: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0d0887, #f0f921);
        color: #000;
        font-weight: bold;
        text-align: center;
        font-size: 14px;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    </style>

    <div class="card-grid">

    <div class="card">
        <div class="card-title">4. Demographic Profile</div>
        <div class="card-body">
        • <b>Rapid growth</b>: <span class="circle">2.6%</span> p.a. (2010: 92,717 → 2021: 122,888)<br>
        • <b>Youthful</b>: <span class="circle">54%</span> under age 20<br>
        • <b>Females</b>: <span class="circle">50.9%</span> (sex ratio: 96.6)<br>
        • <b>Urban</b>: <span class="circle">63%</span> urbanized (Savelugu expansion)
        </div>
    </div>

    <div class="card">
        <div class="card-title">5. Households & Housing</div>
        <div class="card-body">
        • Avg. household size: <span class="circle">5.2</span> vs <span class="circle">3.6</span> national<br>
        • Poor housing: <span class="circle">62.6%</span><br>
        • No toilets: <span class="circle">94.3%</span> without improved facilities<br>
        • Electricity & water: Moderate coverage
        </div>
    </div>

    <div class="card">
        <div class="card-title">6. Education & Literacy</div>
        <div class="card-body">
        • Illiterate (6+ yrs): <span class="circle">60K+</span><br>
        • Female illiterate share: <span class="circle">57%</span><br>
        • Region rank: <b>5th</b> highest illiteracy in Northern Region
        </div>
    </div>

    <div class="card">
        <div class="card-title">7. Economic Activity</div>
        <div class="card-body">
        • Agriculture: <span class="circle">70%</span> engaged<br>
        • Youth unemployment: <span class="circle">16%</span>–<span class="circle">18%</span><br>
        • Growth in trade & transport (N10 corridor)
        </div>
    </div>

    </div>
    """, unsafe_allow_html=True)

    
    
if __name__ == "__main__":
    app()
