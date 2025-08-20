import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from streamlit_timeline import timeline
from streamlit_lottie import st_lottie
import requests
import plotly.graph_objects as go
import time
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Quantum Explained",
    page_icon="⚛️", # Added an icon for the browser tab
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar open by default
)

# --- Custom Styling (Centralized CSS) ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# You would create a file named 'style.css' and add CSS code.
# For simplicity here, I'll embed the CSS directly.
st.markdown("""
<style>
/* Main font and text color */
html, body, [class*="st-"] {
    font-family: 'Verdana', 'Geneva', sans-serif;
    color: #EAEAEA; /* Light gray text for dark background */
}

/* Header styles */
h1 {
    color: #64FFDA; /* Mint green for main title */
}
h2, h3 {
    color: #BB86FC; /* Light purple for subtitles */
}

/* Style for st.success */
.st-success {
    background-color: rgba(0, 255, 127, 0.1);
    border-left: 5px solid #00FF7F;
}

/* Style for st.warning */
.st-warning {
    background-color: rgba(255, 165, 0, 0.1);
    border-left: 5px solid #FFA500;
}

/* Style for st.info */
.st-info {
    background-color: rgba(0, 191, 255, 0.1);
    border-left: 5px solid #00BFFF;
}

/* Custom horizontal rule */
hr {
    margin-top: 20px !important;
    margin-bottom: 20px !important;
    border-top: 2px solid #64FFDA;
}
</style>
""", unsafe_allow_html=True)


# --- Background Setting Function (Unchanged) ---
def set_background(image_file=new_background.png, gradient_colors=None):
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
            background-color: #0E1117; /* Default Streamlit dark */
            background-attachment: fixed;
        }}
        </style>
        """
    st.markdown(bg_style, unsafe_allow_html=True)

# --- Apply Background ---
set_background(gradient_colors=['#000000', '#1E1E1E', '#2C3E50'])


# --- Helper Functions for Lottie Animations (with caching) ---
@st.cache_data # Cache the data to avoid re-loading on every interaction
def load_lottie_from_local(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ Lottie file not found at {filepath}. Please ensure it's in your repository.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading Lottie file from {filepath}: {e}")
        return None

@st.cache_data # Cache the data to avoid re-fetching
def load_lottie_from_url(url: str):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status() # Raise an exception for bad status codes
        return r.json()
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not load Lottie animation from URL: {e}")
        return None


# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h1 style='color: #64FFDA;'>Navigation</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3><p>Choose the path of humanity:</p></h3>", unsafe_allow_html=True)
    choice = st.radio("", ["🕊️ Peace", "💥 Destruction"], label_visibility="collapsed")
    st.markdown("---")
    with st.expander("ℹ️ About This App"):
        st.info(
            "This interactive application explores the dual nature of quantum physics—its capacity "
            "for profound creation and immense destruction. Journey through the fundamental principles "
            "and their real-world consequences."
        )

# --- Main App ---

# 🕱 Title
st.markdown("<h1 style='text-align: center; color: #64FFDA;'> Quantum Explained Visually</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Same atom: peaceful energy or devastating weapon? A journey through quantum possibilities.</h4>", unsafe_allow_html=True)
st.markdown("---")


# 🔬 NEW: Interactive Atomic Structure
st.header("⚛️ Interactive Atomic Model (Bohr Model)")
st.markdown("<p style='color: gray;'>Select an element to see a simplified model of its electrons orbiting the nucleus.</p>", unsafe_allow_html=True)

element_config = {
    'Hydrogen': {'electrons': 1, 'neutrons': 0, 'protons': 1},
    'Helium': {'electrons': 2, 'neutrons': 2, 'protons': 2},
    'Lithium': {'electrons': 3, 'neutrons': 4, 'protons': 3},
    'Beryllium': {'electrons': 4, 'neutrons': 5, 'protons': 4}
}

selected_element = st.selectbox("Choose an Element", options=list(element_config.keys()))

def plot_bohr_model(element_name):
    config = element_config[element_name]
    num_electrons = config['electrons']
    fig = go.Figure()

    # Nucleus
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode='markers',
        marker=dict(size=20 + config['protons']*2, color='#FF4B4B', symbol='circle'),
        name=f"Nucleus ({config['protons']}p, {config['neutrons']}n)"
    ))

    # Electrons and Orbits
    electrons_placed = 0
    shell_capacity = [2, 8, 18] # Max electrons per shell (simplified)
    shell_radii = [0.8, 1.2, 1.6]

    for i, capacity in enumerate(shell_capacity):
        if electrons_placed < num_electrons:
            radius = shell_radii[i]
            electrons_in_shell = min(num_electrons - electrons_placed, capacity)
            angles = np.linspace(0, 2 * np.pi, electrons_in_shell + 1)[:-1]

            # Orbit path
            orbit_t = np.linspace(0, 2*np.pi, 100)
            fig.add_trace(go.Scatter(
                x=radius * np.cos(orbit_t), y=radius * np.sin(orbit_t),
                mode='lines', line=dict(color='#00BFFF', dash='dot', width=1),
                showlegend=False
            ))

            # Electrons
            fig.add_trace(go.Scatter(
                x=radius * np.cos(angles), y=radius * np.sin(angles),
                mode='markers', marker=dict(size=12, color='#00BFFF'), name=f"Shell {i+1} Electrons"
            ))
            electrons_placed += electrons_in_shell

    fig.update_layout(
        xaxis=dict(visible=False, range=[-2, 2]),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1, range=[-2, 2]),
        showlegend=True,
        legend=dict(font=dict(color="white")),
        width=700,
        height=500,
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

plot_bohr_model(selected_element)
st.markdown("---")

# ☮ Peace or 💣 Destruction Path
if choice == "🕊️ Peace":
    st.header("🕊️ Quantum for Peace: Harnessing Nature's Power")
    st.markdown("<p style='color: gray;'>Discover how quantum principles are used to heal, power, and secure our world.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])

    with col1:
        with st.expander("🩺 Medical Applications"):
            st.success("✅ *Medical Imaging (MRI):* Powerful magnetic fields and radio waves interact with atomic nuclei to create detailed images of the human body, revolutionizing diagnostics.")
            st.success("✅ *Cancer Radiotherapy:* Precisely targeted radiation from isotopes destroys cancer cells while minimizing damage to healthy tissue.")
        with st.expander("⚡ Clean Energy"):
            st.success("✅ *Clean Energy (Nuclear Reactors):* Controlled nuclear fission releases vast amounts of energy from a small mass, providing a low-carbon power source for millions.")
        with st.expander("🔒 Quantum Technology"):
            st.success("✅ *Quantum Encryption:* Leveraging principles like superposition and entanglement to create unhackable communication channels, vital for cybersecurity.")
            st.success("✅ *Atomic Clocks:* Unimaginably precise timekeeping devices based on atomic vibrations, essential for GPS and global communication networks.")
            st.success("✅ *Quantum Computing:* Using qubits to perform complex calculations impossible for classical computers, promising breakthroughs in medicine, materials science, and AI.")


    with col2:
        lottie_clean_energy = load_lottie_from_url("https://assets1.lottiefiles.com/packages/lf20_e0wU3R.json")
        if lottie_clean_energy:
            st_lottie(lottie_clean_energy, speed=1, loop=True, quality="high", height=300)
        else:
            st.image("https://cdn.britannica.com/37/123637-050-1B14113C/nuclear-power-plant-Cattenom-France.jpg", caption="Nuclear Power Plant", use_container_width=True)

    st.subheader("📖 Fundamental Scientific Principles")
    st.code("E = mc² # Einstein's Energy-Mass Equivalence: The foundational principle behind nuclear energy.", language="python")
    st.code("Ψ(x,t) # Wave Function (Schrödinger Equation): Describes the probability amplitude of a quantum particle's state.", language="python")
    st.markdown("> *\"He who sees all beings in the self and the self in all beings does not hate...\"* — Bhagavad Gita")

else: # Destruction Path
    st.header("💥 The Atomic Bomb: Power Misused, Humanity's Warning")
    st.markdown("<p style='color: gray;'>A stark reminder of the devastating consequences when quantum power is unleashed for destruction.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])

    with col1:
        with st.expander(" Hiroshima & Nagasaki: The Human Cost"):
            st.warning("☠️ *Hiroshima (August 6, 1945):* An estimated 140,000 lives lost.")
            st.warning("☠️ *Nagasaki (August 9, 1945):* Another 74,000 lives extinguished.")
            st.warning("⚠️ *Long-term Effects:* Survivors faced severe health issues from radiation.")
            st.warning("⚠️ *Environmental Devastation:* Widespread destruction and radioactive fallout.")

        with st.expander("📊 Impact Data"):
            data = pd.DataFrame({
                "City": ["Hiroshima", "Nagasaki"],
                "Initial Deaths": [140000, 74000],
            })
            st.bar_chart(data.set_index("City"))
            
        with st.expander("🗺️ Interactive Map"):
            map_data = pd.DataFrame({
                'city': ['Hiroshima', 'Nagasaki'],
                'lat': [34.3853, 32.7503],
                'lon': [132.4553, 129.8777]
            })
            st.map(map_data)


    with col2:
        lottie_explosion = load_lottie_from_url("https://assets9.lottiefiles.com/packages/lf20_t3o6gq.json")
        if lottie_explosion:
            st_lottie(lottie_explosion, speed=1, loop=False, quality="high", height=300)
        else:
            st.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Nagasakibomb.jpg", caption="Mushroom Cloud over Nagasaki", use_container_width=True)
        st.image("./oppenheimer_test_image.jpg", caption="Trinity Test, the first atomic bomb detonation", use_container_width=True, )


    st.subheader("🌌 The Principle Behind the Bomb: Uncontrolled Fission")
    st.code("""# Fission Chain Reaction (Simplified)
neutron_initiates_fission = True
if neutron_initiates_fission:
    # Heavy nucleus splits, releasing energy and more neutrons
    # These new neutrons hit other atoms, perpetuating the chain
    # If uncontrolled, this leads to an explosion.
    massive_explosion = True
""", language="python")

    st.markdown("> *\"Now I am become Death, the Destroyer of Worlds.\"* — J. Robert Oppenheimer")

    try:
        with open("oppenheimer_theme.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    except FileNotFoundError:
        st.info("🎵 To enhance the experience, add 'oppenheimer_theme.mp3' to your project folder.")

st.markdown("---")

# --- NEW SECTION: Core Quantum Concepts ---
st.header("💡 Core Quantum Concepts Explained")
tab1, tab2, tab3 = st.tabs(["🌀 Wave-Particle Duality", "🧊 Superposition & Measurement", " tunneling through the walls."])

with tab1:
    st.subheader("The Double-Slit Experiment")
    st.markdown("Quantum objects like electrons can act as both particles and waves. When not observed, they create an interference pattern like waves. When observed, they act like particles.")
    
    # Simple animation of the double-slit experiment
    show_pattern = st.checkbox("Show Wave Interference Pattern", value=True)
    if show_pattern:
        x = np.linspace(-10, 10, 400)
        # Simulating two slit sources
        y1 = np.sinc(x - 2)
        y2 = np.sinc(x + 2)
        y_interference = (y1 + y2)**2
        
        fig, ax = plt.subplots()
        ax.plot(x, y_interference, color='#64FFDA')
        ax.set_title("Wave Interference Pattern on Detector Screen")
        ax.set_xlabel("Position on Screen")
        ax.set_ylabel("Intensity")
        ax.set_facecolor("#0E1117")
        fig.patch.set_facecolor("#0E1117")
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        st.pyplot(fig)
    else:
        st.image("https://i.stack.imgur.com/2slp6.png", caption="When observed, electrons create two simple bands, acting like particles.")

with tab2:
    st.subheader("The Qubit & The Bloch Sphere")
    st.markdown("A qubit, the basic unit of quantum information, can be in a state of 0, 1, or a **superposition** of both simultaneously. The Bloch sphere is a way to visualize this state. When **measured**, the superposition collapses to either 0 or 1.")
    
    # Interactive Bloch Sphere
    st.write("Click the button to 'measure' the qubit.")
    if 'phi' not in st.session_state:
        st.session_state.phi = np.pi / 4
        st.session_state.theta = np.pi / 4

    if st.button("Measure Qubit!"):
        # Collapse to |0> (north pole) or |1> (south pole)
        st.session_state.theta = np.random.choice([0, np.pi])
        st.session_state.phi = 0
    
    # Convert spherical to cartesian
    x = np.sin(st.session_state.theta) * np.cos(st.session_state.phi)
    y = np.sin(st.session_state.theta) * np.sin(st.session_state.phi)
    z = np.cos(st.session_state.theta)
    
    fig = go.Figure(data=[
        go.Scatter3d(x=[0, x], y=[0, y], z=[0, z], mode='lines+markers', marker=dict(color='#64FFDA', size=5), line=dict(color='#64FFDA', width=4), name='Qubit State Vector'),
        go.Scatter3d(x=[0], y=[0], z=[1.05], mode='text', text=['|0⟩'], textfont=dict(color='white')),
        go.Scatter3d(x=[0], y=[0], z=[-1.1], mode='text', text=['|1⟩'], textfont=dict(color='white'))
    ])
    fig.update_layout(
        title="Interactive Bloch Sphere",
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
                   xaxis=dict(showbackground=False, color='white'),
                   yaxis=dict(showbackground=False, color='white'),
                   zaxis=dict(showbackground=False, color='white'),
                   aspectmode='cube'),
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Quantum Tunneling")
    st.markdown("In the quantum realm, a particle can pass through a potential energy barrier even if it doesn't have enough energy to overcome it classically. This is like a ghost walking through a wall.")
    
    barrier_height = st.slider("Barrier Height", 1.0, 5.0, 2.5)
    
    x = np.linspace(-5, 5, 400)
    # Simplified wave function visualization
    psi = np.exp(-x**2) # Initial wave packet
    
    # Simulate tunneling
    tunnel_x = np.linspace(2, 5, 100)
    tunnel_psi = (1 / barrier_height) * np.exp(-(tunnel_x-3.5)**2)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=psi, mode='lines', name='Wave Packet', line=dict(color='#64FFDA')))
    fig.add_shape(type="rect", x0=1, y0=0, x1=2, y1=barrier_height, line=dict(color="#FF4B4B"), fillcolor="#FF4B4B", opacity=0.5, name="Potential Barrier")
    fig.add_trace(go.Scatter(x=tunnel_x, y=tunnel_psi, mode='lines', name='Tunneled Wave', line=dict(color='#BB86FC', dash='dot')))
    
    fig.update_layout(
        title="Visualizing Quantum Tunneling",
        xaxis_title="Position", yaxis_title="Probability Amplitude",
        plot_bgcolor="#0E1117", paper_bgcolor="#0E1117", font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# --- Original Sections (Unchanged but validated) ---

# 🎲 Einstein's Dilemma
st.header("🎲 Einstein's Dilemma: God Doesn't Play Dice")
col_quote, col_animation = st.columns([2, 1])
with col_quote:
    st.markdown("<h3 style='text-align: center; color: #BB86FC;'>\"God does not play dice with the universe.\"</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>- Albert Einstein</p>", unsafe_allow_html=True)
with col_animation:
    lottie_dice = load_lottie_from_url("https://assets10.lottiefiles.com/packages/lf20_mxgd762x.json")
    if lottie_dice:
        st_lottie(lottie_dice, speed=1, loop=True, quality="high", height=200)

st.markdown("---")

# 📜 Timeline
st.header("📜 Timeline of Quantum Physics")
@st.cache_data
def load_timeline_data(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ timeline.json not found. Please ensure the file is in your repository.")
        return None
    except Exception as e:
        st.error(f"❌ Timeline failed to load: {e}.")
        return None

timeline_data = load_timeline_data("timeline.json")
if timeline_data:
    timeline(timeline_data, height=600)

st.markdown("---")

# 🎥 Videos (Unchanged)
st.header("🎥 Quantum Reality in Motion: Visualizing the Impact")
v_col1, v_col2 = st.columns(2)
with v_col1:
    try:
        with open("oppenheimer_intro.mp4", "rb") as f:
            st.video(f.read(), format="video/mp4")
            st.caption("A glimpse into the historical context.")
    except FileNotFoundError:
        st.warning("Video 'oppenheimer_intro.mp4' not found.")
with v_col2:
    try:
        with open("atomic_blast.mp4", "rb") as f:
            st.video(f.read(), format="video/mp4")
            st.caption("The raw power of an atomic explosion.")
    except FileNotFoundError:
        st.warning("Video 'atomic_blast.mp4' not found.")

st.markdown("---")


# Footer
st.caption("Created by Nakul | Powered by Streamlit & Quantum Insights | Inspired by the profound ethics of scientific discovery.")
st.markdown("<p style='text-align: center; color: gray;'>*Your choices shape the future of quantum applications.*</p>", unsafe_allow_html=True)
