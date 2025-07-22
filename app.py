import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import requests
import plotly.graph_objects as go
import time
import base64

# --- Page Configuration ---
st.set_page_config(page_title="Quantum Explained", layout="wide")

# --- Background Setting Function ---
def set_background(image_file=None, gradient_colors=None):
    """
    Sets a background for the Streamlit app.
    Args:
        image_file (str, optional): The path to the background image file. Defaults to None.
        gradient_colors (list, optional): A list of two or more hex color codes for a gradient background. E.g., ['#000000', '#2C3E50']. Defaults to None.
    """
    if image_file:
        with open(image_file, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        bg_style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64}");
            background-repeat: no-repeat;
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """
    elif gradient_colors and len(gradient_colors) >= 2:
        gradient_str = ", ".join(gradient_colors)
        bg_style = f"""
        <style>
        .stApp {{
            background: linear-gradient(to bottom right, {gradient_str});
            background-attachment: fixed;
        }}
        </style>
        """
    else:
        bg_style = f"""
        <style>
        .stApp {{
            background-color: #f0f2f6;
            background-attachment: fixed;
        }}
        </style>
        """
    st.markdown(bg_style, unsafe_allow_html=True)

# --- Apply Background ---
set_background(gradient_colors=['#000000', '#2C3E50'])

# --- Helper Functions for Lottie Animations ---
def load_lottie_from_local(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ Lottie file not found at {filepath}. Please ensure the JSON file is in the same directory.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading Lottie file from {filepath}: {e}")
        return None

def load_lottie_from_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.RequestException:
        return None
    return None

# --- UI Elements ---

# Title
st.markdown("<h1 style='text-align: center; color: #64FFDA;'> Quantum Explained Visually</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Same atom: peaceful energy or devastating weapon? A journey through quantum possibilities.</h4>", unsafe_allow_html=True)
st.markdown("---")

# Choice
st.markdown("<h3><p style='text-align: center;'>Choose the path of humanity:</p></h3>", unsafe_allow_html=True)
choice = st.radio("", ["☮ Peace", "💣 Destruction"], horizontal=True, label_visibility="collapsed")
st.markdown("---")

# Animated Atomic Structure
st.header("🔬 Visualizing Atomic Structure (Animated)")
st.markdown("<p style='color: gray;'>Witness the dance of electrons around the nucleus.</p>", unsafe_allow_html=True)
animation_speed = st.slider("Electron Orbit Speed", 0.1, 2.0, 1.0, 0.1)
atomic_structure_placeholder = st.empty()

# Animation loop for electrons
for i in range(100):
    t = i * 0.05 * animation_speed
    nucleus_x, nucleus_y = [0], [0]
    electron1_radius = 1
    electron1_x = [electron1_radius * np.cos(t)]
    electron1_y = [electron1_radius * np.sin(t)]
    electron2_radius = 1.2
    electron2_x = [electron2_radius * np.cos(t + np.pi)]
    electron2_y = [electron2_radius * np.sin(t + np.pi)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nucleus_x, y=nucleus_y, mode='markers', marker=dict(size=40, color='red', symbol='circle'), name='Nucleus'))
    fig.add_trace(go.Scatter(x=electron1_x, y=electron1_y, mode='markers', marker=dict(size=15, color='blue', symbol='circle'), name='Electron 1'))
    fig.add_trace(go.Scatter(x=electron2_x, y=electron2_y, mode='markers', marker=dict(size=15, color='green', symbol='circle'), name='Electron 2'))

    orbit_t = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(go.Scatter(x=electron1_radius * np.cos(orbit_t), y=electron1_radius * np.sin(orbit_t), mode='lines', line=dict(color='blue', dash='dot', width=1), showlegend=False))
    fig.add_trace(go.Scatter(x=electron2_radius * np.cos(orbit_t), y=electron2_radius * np.sin(orbit_t), mode='lines', line=dict(color='green', dash='dot', width=1), showlegend=False))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-1.5, 1.5]),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1, range=[-1.5, 1.5]),
        showlegend=False,
        width=700,
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="black",
        margin=dict(l=0, r=0, t=0, b=0)
    )
    with atomic_structure_placeholder:
        st.plotly_chart(fig, use_container_width=True)
    time.sleep(0.05)

st.markdown("---")

# Einstein's Quote and Animation
st.header("🎲 Einstein's Dilemma: God Doesn't Play Dice")
st.markdown("<p style='color: gray;'>Albert Einstein's famous resistance to the probabilistic nature of quantum mechanics.</p>", unsafe_allow_html=True)
col_quote, col_animation = st.columns([2, 1])
with col_quote:
    st.markdown("<h3 style='text-align: center; color: #BB86FC;'>\"God does not play dice with the universe.\"</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>- Albert Einstein</p>", unsafe_allow_html=True)
with col_animation:
    lottie_dice = load_lottie_from_url("https://assets10.lottiefiles.com/packages/lf20_mxgd762x.json")
    if lottie_dice:
        st_lottie(lottie_dice, speed=1, reverse=False, loop=True, quality="high", height=200)

st.markdown("---")

# Conditional Content Paths
if choice == "☮ Peace":
    st.header("🌿 Quantum for Peace: Harnessing Nature's Power")
    st.markdown("<p style='color: gray;'>Discover how quantum principles are used to heal, power, and secure our world.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.success("✅ *Medical Imaging (MRI):* Powerful magnetic fields and radio waves interact with atomic nuclei to create detailed images of the human body, revolutionizing diagnostics.")
        st.success("✅ *Cancer Radiotherapy:* Precisely targeted radiation from isotopes destroys cancer cells while minimizing damage to healthy tissue.")
        st.success("✅ *Clean Energy (Nuclear Reactors):* Controlled nuclear fission releases vast amounts of energy from a small mass, providing a low-carbon power source for millions.")
    with col2:
        lottie_clean_energy = load_lottie_from_url("https://assets1.lottiefiles.com/packages/lf20_e0wU3R.json")
        if lottie_clean_energy:
            st_lottie(lottie_clean_energy, speed=1, reverse=False, loop=True, quality="high", height=300)

    st.subheader("📖 Fundamental Scientific Principles")
    st.code("E = mc² # Einstein's Energy-Mass Equivalence", language="python")
    st.code("Ψ(x,t) # Wave Function (Schrödinger Equation)", language="python")
    st.markdown("> *\"He who sees all beings in the self and the self in all beings does not hate...\"* — Bhagavad Gita")
else:
    st.header("💥 The Atomic Bomb: Power Misused, Humanity's Warning")
    st.markdown("<p style='color: gray;'>A stark reminder of the devastating consequences when quantum power is unleashed for destruction.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.warning("☠ *Hiroshima (August 6, 1945):* An estimated 140,000 lives lost, a city vaporized in an instant.")
        st.warning("☠ *Nagasaki (August 9, 1945):* Another 74,000 lives extinguished, demonstrating the horrifying scale of atomic warfare.")
        st.warning("⚠ *Long-term Radiation Effects:* Survivors faced severe health issues like cancers and genetic mutations for decades.")
    with col2:
        lottie_explosion = load_lottie_from_url("https://assets9.lottiefiles.com/packages/lf20_t3o6gq.json")
        if lottie_explosion:
            st_lottie(lottie_explosion, speed=1, reverse=False, loop=False, quality="high", height=300)

    st.subheader("📊 Impact Data: The Human Cost")
    data = pd.DataFrame({
        "City": ["Hiroshima", "Nagasaki"],
        "Initial Deaths": [140000, 74000],
        "Estimated Radiation Affected": [200000, 120000]
    })
    st.bar_chart(data.set_index("City"))
    st.markdown("> *\"Now I am become Death, the Destroyer of Worlds.\"* — J. Robert Oppenheimer")

    st.image("./oppenheimer_test_image.jpg", caption="Trinity Test, the first atomic bomb detonation (Conceptual)", use_container_width=True)
    try:
        with open("oppenheimer_theme.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3", start_time=0)
    except FileNotFoundError:
        st.info("🎵 To enhance the experience, place an audio file named 'oppenheimer_theme.mp3' in the same folder.")

st.markdown("---")

# Timeline
st.header("📜 Timeline of Quantum Physics: A Journey of Discovery")
st.markdown("<p style='color: gray;'>Explore key milestones in the development of quantum mechanics and its applications.</p>", unsafe_allow_html=True)
try:
    with open("timeline.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    timeline(data, height=600)
except FileNotFoundError:
    st.error("❌ timeline.json not found. Please ensure the file is in the same directory as your script.")

st.markdown("---")

# Quantum Vibe Animation
st.header("🌌 Animated Quantum Vibe: The Fabric of Reality")
lottie_q = load_lottie_from_local("./quantum_vibe.json")
if lottie_q:
    st_lottie(lottie_q, speed=1, reverse=False, loop=True, quality="high", height=300)

st.markdown("---")

# Centered Videos
st.header("🎥 Quantum Reality in Motion: Visualizing the Impact")
col1, col2 = st.columns(2)
with col1:
    try:
        with open("oppenheimer_intro.mp4", "rb") as f:
            st.video(f.read(), format="video/mp4", start_time=0)
        st.caption("A glimpse into the historical context.")
    except FileNotFoundError:
        st.warning("Video 'oppenheimer_intro.mp4' not found.")
with col2:
    try:
        with open("atomic_blast.mp4", "rb") as f:
            st.video(f.read(), format="video/mp4", start_time=0)
        st.caption("The raw power of an atomic explosion.")
    except FileNotFoundError:
        st.warning("Video 'atomic_blast.mp4' not found.")

st.markdown("---")

# Footer
st.caption("Created by Nakul | Powered by Streamlit & Quantum Insights | Inspired by the profound ethics of scientific discovery.")
