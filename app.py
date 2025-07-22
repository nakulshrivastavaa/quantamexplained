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

# --- Initialize Session State ---
# For continuous animations
if 'frame' not in st.session_state:
    st.session_state.frame = 0
# For the quiz
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
# For superposition collapse
if 'superposition_state' not in st.session_state:
    st.session_state.superposition_state = "superposition" # 'superposition', '0', or '1'


# --- Asset & Style Loading ---

def load_lottie_from_url(url: str):
    """Loads a Lottie animation from a URL with error handling."""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        return None

def set_background_and_styles():
    """Sets a gradient background and injects custom CSS for particles and other styles."""
    gradient_str = ", ".join(['#000000', '#1a1a2e', '#2c3e50'])
    bg_style = f"""
    <style>
    /* Main background gradient */
    .stApp {{
        background: linear-gradient(135deg, {gradient_str});
        background-attachment: fixed;
    }}

    /* Animated particle background */
    @keyframes move-particles {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-100vh); }}
    }}
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 200vh;
        background-image: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 30px 30px;
        animation: move-particles 50s linear infinite;
        z-index: -1;
    }}

    /* Custom radio buttons */
    div.st-emotion-cache-1t2qdok {{ justify-content: center; gap: 1rem; }}
    div.st-emotion-cache-k7vsyb {{
        border: 1px solid #64FFDA; background-color: transparent;
        padding: 10px 25px; border-radius: 30px; transition: all 0.3s ease;
    }}
    div.st-emotion-cache-k7vsyb:has(input:checked) {{ background-color: #64FFDA; }}
    div.st-emotion-cache-k7vsyb label {{ color: #64FFDA !important; font-weight: bold; font-size: 1.1rem; }}
    div.st-emotion-cache-k7vsyb:has(input:checked) label {{ color: #000000 !important; }}

    /* Sidebar link style */
    .st-emotion-cache-1cypcdb a {{
        color: #b0b0b0;
        text-decoration: none;
    }}
    .st-emotion-cache-1cypcdb a:hover {{
        color: #64FFDA;
        text-decoration: none;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)


# --- UI Section Functions ---

def display_sidebar_nav():
    """CORRECTED: Displays a sticky sidebar for easy navigation using st.markdown."""
    with st.sidebar:
        st.markdown("<h2 style='color: #64FFDA;'>Navigation</h2>", unsafe_allow_html=True)
        st.markdown("[Introduction](#introduction)")
        st.markdown("[Atomic Structure](#atomic-structure)")
        st.markdown("[The Choice: Peace or Destruction](#the-choice)")
        st.markdown("[Superposition & Measurement](#superposition-measurement)")
        st.markdown("[Quantum Entanglement](#quantum-entanglement)")
        st.markdown("[Key Figures](#key-figures)")
        st.markdown("[Quantum Quiz](#quantum-quiz)")
        st.markdown("[Timeline](#timeline)")


def display_header_and_choice():
    """Displays the header and the main path choice radio buttons."""
    # ADDED ID
    st.markdown("<h1 id='introduction' style='text-align: center; color: #64FFDA;'>Quantum Explained Visually</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #b0b0b0;'>Same atom: peaceful energy or devastating weapon?</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ADDED ID
    st.markdown("<h3 id='the-choice' style='text-align: center; color: #e0e0e0;'>Choose the path of humanity:</h3>", unsafe_allow_html=True)
    choice = st.radio("", ["☮ Peace", "💣 Destruction"], horizontal=True, label_visibility="collapsed")
    return choice

def display_atomic_structure():
    """IMPROVED: Continuously animated atomic structure using st.rerun()."""
    # ADDED ID
    st.markdown("<h2 id='atomic-structure'>🔬 Visualizing Atomic Structure (Animated)</h2>", unsafe_allow_html=True)
    animation_speed = st.slider("Electron Orbit Speed", 0.5, 5.0, 1.0, 0.1, key="speed_slider")
    
    t = st.session_state.frame * 0.01 * animation_speed
    
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

def display_peace_path():
    """Content for the 'Peace' path."""
    st.header("🌿 Quantum for Peace: Harnessing Nature's Power")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.success("✅ *Medical Imaging (MRI):* Using nuclear magnetic resonance for diagnostics.")
        st.success("✅ *Clean Energy (Nuclear Reactors):* Controlled fission provides low-carbon power.")
        st.success("✅ *Quantum Computing:* Solving problems impossible for classical computers.")
    with col2:
        lottie = load_lottie_from_url("https://assets1.lottiefiles.com/packages/lf20_e0wU3R.json")
        if lottie: st_lottie(lottie, height=200, key="peace_lottie")

def display_destruction_path():
    """Content for the 'Destruction' path."""
    st.header("💥 The Atomic Bomb: A Terrifying Power")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.warning("☠ *Hiroshima & Nagasaki:* Hundreds of thousands of lives lost instantly.")
        st.warning("⚠ *Long-term Radiation:* Survivors faced severe health issues for decades.")
        st.subheader("Interactive Chain Reaction")
        k = st.slider("Neutron Multiplication Factor (k)", 0.5, 3.0, 1.0, 0.1)
        if k < 1.0:
            st.info(f"**Subcritical (k={k}):** The reaction dies out. (Safe in a reactor)")
        elif k == 1.0:
            st.success(f"**Critical (k={k}):** The reaction is self-sustaining. (Stable reactor power)")
        else:
            st.error(f"**Supercritical (k={k}):** The reaction grows exponentially! (The principle of a bomb)")

    with col2:
        lottie = load_lottie_from_url("https://assets9.lottiefiles.com/packages/lf20_t3o6gq.json")
        if lottie: st_lottie(lottie, height=200, key="destruction_lottie")

def display_superposition_and_entanglement():
    """Section for Superposition and Entanglement visualizations."""
    st.markdown("---")
    st.markdown("<h2 id='superposition-measurement'>🌀 Visualizing Core Quantum Concepts</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Superposition & Measurement")
        
        lottie_superposition_url = "https://assets3.lottiefiles.com/packages/lf20_jG1r46.json"
        lottie_state0_url = "https://assets3.lottiefiles.com/packages/lf20_cUG5w3.json"
        lottie_state1_url = "https://assets4.lottiefiles.com/packages/lf20_awv8l1g9.json"
        
        if st.session_state.superposition_state == "superposition":
            lottie_display = load_lottie_from_url(lottie_superposition_url)
            st.markdown("A qubit can be both 0 and 1 at once. It's in a **superposition**.")
        elif st.session_state.superposition_state == "0":
            lottie_display = load_lottie_from_url(lottie_state0_url)
            st.success("Measured! The qubit collapsed to **State 0**.")
        else: # state '1'
            lottie_display = load_lottie_from_url(lottie_state1_url)
            st.error("Measured! The qubit collapsed to **State 1**.")

        if lottie_display:
            st_lottie(lottie_display, height=200, key="superposition_lottie")

        if st.button("Measure the Qubit!"):
            st.session_state.superposition_state = np.random.choice(['0', '1'])
            st.rerun()
        if st.button("Reset Qubit"):
            st.session_state.superposition_state = "superposition"
            st.rerun()

    with col2:
        # ADDED ID
        st.markdown("<h3 id='quantum-entanglement' style='margin-top:0;'>Quantum Entanglement</h3>", unsafe_allow_html=True)
        st.markdown("Two particles linked instantly. Measure one, and you know the state of the other.")
        
        lottie_entangled_up = "https://assets5.lottiefiles.com/packages/lf20_o25zt6py.json"
        lottie_entangled_down = "https://assets5.lottiefiles.com/packages/lf20_y0i7cp5t.json"

        particle_A, particle_B = st.columns(2)
        with particle_A:
            st.markdown("Particle A")
            lottie_A = load_lottie_from_url(lottie_entangled_up)
            if lottie_A: st_lottie(lottie_A, height=150, key="entangled_A")
        
        with particle_B:
            st.markdown("Particle B")
            lottie_B = load_lottie_from_url(lottie_entangled_down)
            if lottie_B: st_lottie(lottie_B, height=150, key="entangled_B")
        st.info("If Particle A is 'spin up', entangled Particle B must be 'spin down'.")


def display_key_figures():
    """Section for key figures in quantum mechanics."""
    st.markdown("---")
    # ADDED ID
    st.markdown("<h2 id='key-figures'>🧠 Key Figures in Quantum Mechanics</h2>", unsafe_allow_html=True)
    
    figures = {
        "Max Planck": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Max_Planck_%281858-1947%29.jpg",
        "Albert Einstein": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg/800px-Einstein_1921_by_F_Schmutzer_-_restoration.jpg",
        "Niels Bohr": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Niels_Bohr.jpg/800px-Niels_Bohr.jpg",
        "J. R. Oppenheimer": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/JROppenheimer-LosAlamos.jpg/800px-JROppenheimer-LosAlamos.jpg"
    }
    
    descriptions = {
        "Max Planck": "Originated quantum theory in 1900, which revolutionized human understanding of atomic and subatomic processes.",
        "Albert Einstein": "Explained the photoelectric effect, proposing that light energy is carried in discrete quantized packets (photons).",
        "Niels Bohr": "Developed the Bohr model of the atom, in which he proposed that energy levels of electrons are discrete.",
        "J. R. Oppenheimer": "Headed the Manhattan Project, leading to the development of the atomic bomb, and later became a proponent of nuclear control."
    }

    cols = st.columns(len(figures))
    for i, (name, image_url) in enumerate(figures.items()):
        with cols[i]:
            with st.expander(name, expanded=False):
                st.image(image_url)
                st.write(descriptions[name])


def display_quiz():
    """Interactive quantum quiz."""
    st.markdown("---")
    # ADDED ID
    st.markdown("<h2 id='quantum-quiz'>📝 Test Your Knowledge: Quantum Quiz</h2>", unsafe_allow_html=True)

    if st.session_state.quiz_submitted:
        st.success(f"Quiz Complete! Your score: {st.session_state.quiz_score}/2")
        if st.button("Try Again?"):
            st.session_state.quiz_score = 0
            st.session_state.quiz_submitted = False
            st.rerun()
        return

    with st.form("quantum_quiz"):
        st.write("1. Who is credited with originating quantum theory?")
        q1 = st.radio("q1", ["Einstein", "Bohr", "Planck", "Oppenheimer"], label_visibility="collapsed", horizontal=True)

        st.write("2. The principle that a particle can be in multiple states at once is called:")
        q2 = st.radio("q2", ["Entanglement", "Superposition", "Uncertainty", "Fission"], label_visibility="collapsed", horizontal=True)

        submitted = st.form_submit_button("Submit Answers")
        if submitted:
            score = 0
            if q1 == "Planck":
                score += 1
            if q2 == "Superposition":
                score += 1
            st.session_state.quiz_score = score
            st.session_state.quiz_submitted = True
            st.rerun()

def display_timeline():
    """Displays the interactive timeline."""
    st.markdown("---")
    # ADDED ID
    st.markdown("<h2 id='timeline'>📜 Timeline of Quantum Physics</h2>", unsafe_allow_html=True)
    try:
        with open("timeline.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        timeline(data, height=600)
    except FileNotFoundError:
        st.error("❌ timeline.json not found. Please add the file to your project folder.")


# --- Main App Execution ---
set_background_and_styles()
display_sidebar_nav()

# Main content area
choice = display_header_and_choice()
st.markdown("---")

display_atomic_structure()
st.markdown("---")

if choice == "☮ Peace":
    display_peace_path()
else:
    display_destruction_path()

display_superposition_and_entanglement()
display_key_figures()
display_quiz()
display_timeline()

st.markdown("---")
st.caption("Created by Nakul | Enhanced with interactive features by Gemini | Inspired by the profound ethics of scientific discovery.")

# --- Animation Loop Control ---
st.session_state.frame += 1
time.sleep(0.03)
st.rerun()
