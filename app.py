import streamlit as st
import numpy as np
import pandas as pd
import json
import requests
import plotly.graph_objects as go
import time
import base64
from streamlit_lottie import st_lottie
from streamlit_timeline import timeline

# --- Page Configuration ---
st.set_page_config(page_title="Quantum Explained Visually", layout="wide")

# --- Initialize Session State (CRUCIAL for new animations) ---
if 'frame' not in st.session_state:
    st.session_state.frame = 0
if 'tunneling_pos' not in st.session_state:
    st.session_state.tunneling_pos = -5.0

# --- Asset Loading & Styling ---
def load_lottie_from_url(url: str):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.RequestException:
        return None
    return None

def set_background_and_styles():
    """Sets a gradient background and injects custom CSS."""
    bg_style = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #2c3e50 100%);
        background-attachment: fixed;
    }
    /* Sidebar link style */
    .st-emotion-cache-1cypcdb a {
        color: #b0b0b0;
        text-decoration: none;
    }
    .st-emotion-cache-1cypcdb a:hover {
        color: #64FFDA;
        text-decoration: none;
    }
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# --- UI Section Functions ---

def display_sidebar():
    """NEW: Displays a sticky sidebar for easy navigation."""
    with st.sidebar:
        st.markdown("<h2 style='color: #64FFDA;'>Navigation</h2>", unsafe_allow_html=True)
        st.markdown("[Introduction](#introduction)")
        st.markdown("[Atomic Structure](#atomic-structure)")
        st.markdown("[Core Concepts](#core-concepts)")
        st.markdown("[The Choice: Peace or Destruction](#the-choice)")
        st.markdown("[Timeline](#timeline)")
        st.markdown("[Key Figures & Videos](#key-figures-videos)")
        st.markdown("[Further Learning](#further-learning)")

def display_header():
    """Displays the main title and introduction."""
    st.markdown("<h1 id='introduction' style='text-align: center; color: #64FFDA;'>Quantum Explained Visually</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #b0b0b0;'>Same atom: peaceful energy or devastating weapon? A journey through quantum possibilities.</h4>", unsafe_allow_html=True)
    st.markdown("---")

def display_atomic_structure_improved():
    """IMPROVED: Continuously animated atomic structure using st.rerun()."""
    st.markdown("<h2 id='atomic-structure'>🔬 Visualizing Atomic Structure (Continuous Animation)</h2>", unsafe_allow_html=True)
    animation_speed = st.slider("Electron Orbit Speed", 0.5, 5.0, 1.5, 0.1, key="speed_slider")

    # Use session_state for continuous animation
    t = st.session_state.frame * 0.01 * animation_speed

    fig = go.Figure()
    # Nucleus
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=40, color='#ff6b6b'), name='Nucleus'))
    # Electrons
    fig.add_trace(go.Scatter(x=[np.cos(t)], y=[np.sin(t)], mode='markers', marker=dict(size=15, color='#4d96ff'), name='Electron 1'))
    fig.add_trace(go.Scatter(x=[1.2 * np.cos(-0.8 * t)], y=[1.2 * np.sin(-0.8 * t)], mode='markers', marker=dict(size=15, color='#6bcB77'), name='Electron 2'))
    # Orbits
    orbit_t = np.linspace(0, 2 * np.pi, 100)
    fig.add_trace(go.Scatter(x=np.cos(orbit_t), y=np.sin(orbit_t), mode='lines', line=dict(color='rgba(77, 150, 255, 0.3)', dash='dot'), showlegend=False))
    fig.add_trace(go.Scatter(x=1.2*np.cos(orbit_t), y=1.2*np.sin(orbit_t), mode='lines', line=dict(color='rgba(107, 203, 119, 0.3)', dash='dot'), showlegend=False))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-1.5, 1.5]), yaxis=dict(visible=False, scaleanchor="x", scaleratio=1, range=[-1.5, 1.5]),
        showlegend=False, plot_bgcolor="rgba(255, 255, 255, 0.05)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0), height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

def display_core_concepts():
    """NEW: Displays visualizations for core quantum concepts."""
    st.markdown("<h2 id='core-concepts'>🌀 The Weird & Wonderful World of Quantum</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎭 Wave-Particle Duality")
        st.markdown("A quantum object can be a wave or a particle. Observation forces a choice.")
        lottie_wave = load_lottie_from_url("https://assets8.lottiefiles.com/packages/lf20_bwni5s5t.json")
        if lottie_wave:
            st_lottie(lottie_wave, height=200, key="wave")

    with col2:
        st.subheader("👻 Quantum Tunneling")
        st.markdown("Particles can 'tunnel' through barriers they shouldn't be able to cross.")
        x = np.linspace(-5, 5, 400)
        barrier = np.where((x > -0.5) & (x < 0.5), 10, 0)
        pos = st.session_state.tunneling_pos
        wave_packet = np.exp(-((x - pos)**2)) * np.sin(10 * (x - pos))

        fig_tunnel = go.Figure()
        fig_tunnel.add_trace(go.Scatter(x=x, y=barrier, fill='tozeroy', name='Barrier', line=dict(color='rgba(255, 107, 107, 0.5)')))
        fig_tunnel.add_trace(go.Scatter(x=x, y=wave_packet + 5, name='Wave Packet', line=dict(color='#64FFDA')))
        fig_tunnel.update_layout(
            yaxis=dict(visible=False, range=[-2, 12]), xaxis=dict(visible=False),
            showlegend=False, plot_bgcolor="rgba(255, 255, 255, 0.05)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0), height=200
        )
        st.plotly_chart(fig_tunnel, use_container_width=True)
    st.markdown("---")

def display_path_choice_and_sections():
    """Handles the user's choice and displays the relevant peace/destruction path."""
    st.markdown("<h2 id='the-choice' style='text-align: center;'>Choose the Path of Humanity</h2>", unsafe_allow_html=True)
    choice = st.radio("", ["☮ Peace", "💣 Destruction"], horizontal=True, label_visibility="collapsed")
    st.markdown("---")

    if choice == "☮ Peace":
        st.header("🌿 Quantum for Peace: Harnessing Nature's Power")
        st.success("✅ *Medical Imaging (MRI):* Using nuclear magnetic resonance for diagnostics.")
        st.success("✅ *Clean Energy (Nuclear Reactors):* Controlled fission provides low-carbon power.")
        st.success("✅ *Quantum Computing:* Solving problems impossible for classical computers.")
    else:
        st.header("💥 The Atomic Bomb: A Terrifying Power")
        st.warning("☠ *Uncontrolled Fission:* The principle behind the atomic bomb, leading to catastrophic destruction.")
        st.warning("⚠ *Long-term Fallout:* Lingering radiation causes environmental damage and health crises for generations.")

        st.subheader("📊 Impact Data: The Human Cost")
        data = pd.DataFrame({
            "City": ["Hiroshima", "Nagasaki"],
            "Initial Deaths": [140000, 74000],
        })
        st.bar_chart(data.set_index("City"))
    st.markdown("---")

def display_timeline():
    """Displays the interactive timeline by loading from timeline.json."""
    st.markdown("<h2 id='timeline'>📜 Timeline of Quantum Physics</h2>", unsafe_allow_html=True)
    try:
        with open("timeline.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        timeline(data, height=600)
    except FileNotFoundError:
        st.error("❌ timeline.json not found. Please ensure the file is in the same directory as your script.")
    except Exception as e:
        st.error(f"❌ Timeline failed to load: {e}. Check the format of your timeline.json file.")
    st.markdown("---")

def display_figures_and_videos():
    """Displays key figures and multimedia content."""
    st.markdown("<h2 id='key-figures-videos'>Key Figures & Videos</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("J. Robert Oppenheimer")
        st.markdown("> *\"Now I am become Death, the Destroyer of Worlds.\"*")
        try:
            st.image("./oppenheimer_test_image.jpg", caption="Trinity Test, July 1945")
        except FileNotFoundError:
            st.warning("Image 'oppenheimer_test_image.jpg' not found.")
        try:
            with open("oppenheimer_theme.mp3", "rb") as f:
                st.audio(f.read(), format="audio/mp3")
        except FileNotFoundError:
            st.warning("Audio 'oppenheimer_theme.mp3' not found.")

    with col2:
        st.subheader("Visualizing the Impact")
        try:
            with open("atomic_blast.mp4", "rb") as f:
                st.video(f.read(), format="video/mp4")
        except FileNotFoundError:
            st.warning("Video 'atomic_blast.mp4' not found.")
    st.markdown("---")

def display_further_learning():
    """NEW: Displays links for further learning."""
    st.markdown("<h2 id='further-learning'>📚 Further Learning</h2>", unsafe_allow_html=True)
    st.info("Dive deeper into the fascinating world of quantum mechanics with these resources.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 📖 Reading")
        st.markdown("- [Quantum Mechanics on Wikipedia](https://en.wikipedia.org/wiki/Quantum_mechanics)\n- [The Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/)")
    with col2:
        st.markdown("#### 🎥 Video")
        st.markdown("- [PBS Space Time](https://www.youtube.com/c/pbsspacetime)\n- [Veritasium on Quantum Physics](https://www.youtube.com/watch?v=z1_zNquY1_I)")
    with col3:
        st.markdown("#### 🎓 Courses")
        st.markdown("- [Coursera: Quantum Mechanics](https://www.coursera.org/learn/quantum-mechanics)\n- [edX: Quantum Mechanics for Everyone](https://www.edx.org/learn/quantum-mechanics)")

# --- Main App Execution ---

set_background_and_styles()
display_sidebar()

# Main content area
display_header()
display_atomic_structure_improved()
display_core_concepts()
display_path_choice_and_sections()
display_timeline()
display_figures_and_videos()
display_further_learning()

st.markdown("---")
st.caption("Created by Nakul | Enhanced with interactive features by Gemini")

# --- Animation Loop Control ---
st.session_state.frame += 1
if st.session_state.tunneling_pos > 5:
    st.session_state.tunneling_pos = -5.0
else:
    st.session_state.tunneling_pos += 0.05

time.sleep(0.03)
st.rerun()
