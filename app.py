import streamlit as st
import numpy as np
import pandas as pd
import json
import requests
import plotly.graph_objects as go
import time
import base64
from streamlit_lottie import st_lottie
from streamlit_timeline import timeline # From the second script

# --- Page Configuration ---
st.set_page_config(page_title="Quantum Explained Visually", layout="wide")

# --- Asset Loading ---
def load_lottie_from_url(url: str):
    """Loads a Lottie animation from a URL."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None

def load_lottie_from_local(filepath: str):
    """Loads a Lottie from a local file, with error handling."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ Lottie file not found: {filepath}. Make sure it's in the same folder.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading Lottie file: {e}")
        return None

# --- Background Styling (from second script) ---
def set_background(gradient_colors=['#000000', '#1a1a2e', '#2c3e50']):
    """Sets a dark gradient background for the app."""
    gradient_str = ", ".join(gradient_colors)
    bg_style = f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, {gradient_str});
        background-attachment: fixed;
    }}
    /* Style for metric labels */
    .st-emotion-cache-1g6gooi {{ /* This class might change */
        color: #a0a0a0;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# --- Initialize Session State for Animations (CRUCIAL for animations from first script) ---
if 'frame' not in st.session_state:
    st.session_state.frame = 0
if 'tunneling_pos' not in st.session_state:
    st.session_state.tunneling_pos = -5.0

# --- UI Sections as Functions ---

def display_header():
    """Displays the main title and introduction."""
    st.markdown("<h1 style='text-align: center; color: #64FFDA; text-shadow: 0 0 10px #64FFDA;'>Quantum Explained Visually</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #b0b0b0;'>Same atom: peaceful energy or devastating weapon? A journey through quantum possibilities.</h4>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)

def display_path_choice():
    """Displays the custom-styled radio buttons for path selection (from first script)."""
    st.markdown("<h3 style='text-align: center; color: #e0e0e0;'>Choose the path of humanity:</h3>", unsafe_allow_html=True)
    
    # Custom styled radio buttons CSS
    st.markdown("""
    <style>
        div.st-emotion-cache-1t2qdok { /* container */
            display: flex;
            justify-content: center;
            gap: 1rem;
        }
        div.st-emotion-cache-k7vsyb { /* individual radio */
            border: 1px solid #64FFDA;
            background-color: transparent;
            padding: 10px 25px;
            border-radius: 30px;
            transition: all 0.3s ease;
        }
        div.st-emotion-cache-k7vsyb:has(input:checked) {
            background-color: #64FFDA;
        }
        div.st-emotion-cache-k7vsyb label {
            color: #64FFDA !important;
            font-weight: bold;
            font-size: 1.1rem;
        }
        div.st-emotion-cache-k7vsyb:has(input:checked) label {
            color: #000000 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    choice = st.radio("", ["☮ Peace", "💣 Destruction"], horizontal=True, label_visibility="collapsed")
    st.markdown("---", unsafe_allow_html=True)
    return choice

def display_peace_path():
    """Content for the 'Peace' path, including the E=mc^2 calculator."""
    st.header("🌿 Quantum for Peace: Harnessing Nature's Power")
    st.markdown("<p style='color: #b0b0b0;'>Discover how quantum principles are used to heal, power, and secure our world.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.success("✅ *Medical Imaging (MRI):* Using nuclear magnetic resonance to create detailed images of the human body.")
        st.success("✅ *Clean Energy (Nuclear Reactors):* Controlled fission provides vast low-carbon power.")
        st.success("✅ *Quantum Computing:* Exploiting superposition and entanglement to solve problems impossible for classical computers.")
        st.success("✅ *GPS & Atomic Clocks:* Ultra-precise timekeeping based on atomic vibrations, essential for global navigation.")

    with col2:
        lottie_q_computer = load_lottie_from_url("https://assets4.lottiefiles.com/packages/lf20_cUG5w3.json")
        if lottie_q_computer:
            st_lottie(lottie_q_computer, speed=1, height=250, key="peace_lottie")

    # Interactive E=mc^2 Calculator (from first script)
    st.subheader("Interactive E = mc²")
    st.markdown("See the immense energy locked within a tiny amount of mass.")
    mass_grams = st.number_input("Enter mass in grams (g):", min_value=0.0, value=1.0, step=0.1, format="%.2f")
    
    C = 299792458  # Speed of light in m/s
    mass_kg = mass_grams / 1000
    energy_joules = mass_kg * (C ** 2)
    
    st.metric(label="Equivalent Energy in Joules", value=f"{energy_joules:,.2e}")
    st.info(f"Just {mass_grams}g of mass, if fully converted, could power an average US household for over {int(energy_joules / (3.6e6 * 8760))} years!")

def display_destruction_path():
    """Content for the 'Destruction' path, including Plotly chart and audio."""
    st.header("💥 The Atomic Bomb: A Terrifying Power")
    st.markdown("<p style='color: #b0b0b0;'>A stark reminder of the devastating consequences when quantum power is unleashed for destruction.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.warning("☠ *Hiroshima & Nagasaki:* Hundreds of thousands of lives lost instantly, cities vaporized, and the horrifying dawn of the nuclear age.")
        st.warning("⚠ *Long-term Radiation:* Survivors faced severe health issues like cancers for decades due to lingering radioactive fallout.")
        lottie_radiation = load_lottie_from_url("https://assets3.lottiefiles.com/packages/lf20_3rqwsqb2.json")
        if lottie_radiation:
            st_lottie(lottie_radiation, speed=1, height=150, key="radiation_lottie")

    with col2:
        lottie_explosion = load_lottie_from_url("https://assets9.lottiefiles.com/packages/lf20_t3o6gq.json")
        if lottie_explosion:
            st_lottie(lottie_explosion, speed=1, height=250, key="destruction_lottie")

    # Plotly Impact Data Chart (from first script for better styling)
    st.subheader("📊 Impact Data: The Human Cost")
    data = pd.DataFrame({"City": ["Hiroshima", "Nagasaki"], "Initial Fatalities": [140000, 74000]})
    fig = go.Figure(data=[go.Bar(
        x=data['City'], y=data['Initial Fatalities'],
        marker_color=['#ff6b6b', '#ff8e8e'], text=data['Initial Fatalities'], textposition='auto',
    )])
    fig.update_layout(
        title_text='Estimated Immediate Deaths', xaxis_title="City", yaxis_title="Number of People",
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#e0e0e0'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("> *\"Now I am become Death, the Destroyer of Worlds.\"* — J. Robert Oppenheimer")
    
    # Audio Player (from second script)
    try:
        with open("oppenheimer_theme.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3", start_time=0)
    except FileNotFoundError:
        st.info("🎵 To enhance the experience, add 'oppenheimer_theme.mp3' to the folder.")


def display_quantum_concepts():
    """Core quantum concepts and animations from the first script."""
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #e0e0e0;'>The Weird & Wonderful World of Quantum</h2>", unsafe_allow_html=True)
    
    # --- Animated Atomic Structure ---
    st.subheader("🔬 Visualizing Atomic Structure (Continuous Animation)")
    t = st.session_state.frame * 0.02
    
    nucleus = go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=40, color='#ff6b6b'), name='Nucleus')
    electron1 = go.Scatter(x=[np.cos(t)], y=[np.sin(t)], mode='markers', marker=dict(size=15, color='#4d96ff'), name='Electron 1')
    electron2 = go.Scatter(x=[1.2 * np.cos(-0.8 * t)], y=[1.2 * np.sin(-0.8 * t)], mode='markers', marker=dict(size=15, color='#6bcB77'), name='Electron 2')
    
    orbit_t = np.linspace(0, 2 * np.pi, 100)
    orbit1 = go.Scatter(x=np.cos(orbit_t), y=np.sin(orbit_t), mode='lines', line=dict(color='rgba(77, 150, 255, 0.3)', dash='dot'), showlegend=False)
    orbit2 = go.Scatter(x=1.2*np.cos(orbit_t), y=1.2*np.sin(orbit_t), mode='lines', line=dict(color='rgba(107, 203, 119, 0.3)', dash='dot'), showlegend=False)

    fig = go.Figure(data=[nucleus, electron1, electron2, orbit1, orbit2])
    fig.update_layout(
        xaxis=dict(visible=False, range=[-1.5, 1.5]), yaxis=dict(visible=False, scaleanchor="x", scaleratio=1, range=[-1.5, 1.5]),
        showlegend=False, plot_bgcolor="rgba(255, 255, 255, 0.05)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0), height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # --- Wave-Particle Duality ---
    st.subheader("🎭 Wave-Particle Duality")
    st.markdown("A quantum object can behave as a wave or a particle. The act of observation determines its nature.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("*As a Wave (Unobserved)*")
        lottie_wave = load_lottie_from_url("https://assets8.lottiefiles.com/packages/lf20_bwni5s5t.json")
        if lottie_wave: st_lottie(lottie_wave, height=200, key="wave")
        
    with col2:
        st.markdown("*As a Particle (Observed)*")
        lottie_particle = load_lottie_from_url("https://assets8.lottiefiles.com/packages/lf20_acm4h8kx.json")
        if lottie_particle: st_lottie(lottie_particle, height=200, key="particle")
        
    # --- Quantum Tunneling ---
    st.subheader("👻 Quantum Tunneling")
    st.markdown("Particles can pass through energy barriers they classically shouldn't be able to overcome.")
    
    x = np.linspace(-5, 5, 400)
    barrier_height, barrier_width = 10, 0.5
    barrier = np.where((x > -barrier_width/2) & (x < barrier_width/2), barrier_height, 0)
    
    pos = st.session_state.tunneling_pos
    wave_packet = np.exp(-((x - pos)**2)) * np.sin(10 * (x-pos))
    
    fig_tunnel = go.Figure()
    fig_tunnel.add_trace(go.Scatter(x=x, y=barrier, fill='tozeroy', name='Energy Barrier', line=dict(color='rgba(255, 107, 107, 0.5)')))
    fig_tunnel.add_trace(go.Scatter(x=x, y=wave_packet + barrier_height/2, name='Wave Packet', line=dict(color='#64FFDA')))
    
    fig_tunnel.update_layout(
        yaxis=dict(visible=False, range=[-2, barrier_height + 2]), xaxis=dict(visible=False),
        showlegend=False, plot_bgcolor="rgba(255, 255, 255, 0.05)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0), height=250
    )
    st.plotly_chart(fig_tunnel, use_container_width=True)

def display_timeline():
    """Displays the interactive timeline from the second script."""
    st.markdown("---", unsafe_allow_html=True)
    st.header("📜 Timeline of Quantum Physics")
    st.markdown("<p style='color: #b0b0b0;'>Explore key milestones in the development of quantum mechanics.</p>", unsafe_allow_html=True)
    try:
        with open("timeline.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        timeline(data, height=600)
    except FileNotFoundError:
        st.error("❌ timeline.json not found. Please add the file to your project folder.")
    except Exception as e:
        st.error(f"❌ Timeline failed to load: {e}.")

# --- Main App Logic ---
set_background()
display_header()
choice = display_path_choice()

if choice == "☮ Peace":
    display_peace_path()
else:
    display_destruction_path()

# Display the core concepts regardless of the choice
display_quantum_concepts()

# Display the timeline
display_timeline()

# --- Footer ---
st.markdown("---", unsafe_allow_html=True)
st.caption("Created by Nakul | Enhanced with combined features | Inspired by the profound ethics of scientific discovery.")

# --- Animation Loop Control (The engine from the first script) ---
st.session_state.frame += 1
st.session_state.tunneling_pos += 0.05
if st.session_state.tunneling_pos > 5:
    st.session_state.tunneling_pos = -5.0

# This will cause the script to rerun, creating the animation effect
time.sleep(0.03)
st.rerun()
