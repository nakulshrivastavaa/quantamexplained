import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from streamlit_timeline import timeline
from streamlit_lottie import st_lottie
import requests
import plotly.graph_objects as go
import time # For animation
import base64 # Required for background image functions

# --- Page Configuration ---
# Removed 'icon' argument for broader compatibility
st.set_page_config(page_title="Quantum Explained", layout="wide")

# --- Background Setting Function ---
# This function applies a custom background to the Streamlit app.
# You can choose between an image background or a solid/gradient color.
def set_background(image_file=None, gradient_colors=None):
    """
    Sets a background for the Streamlit app.
    Args:
        image_file (str, optional): The path to the background image file. Defaults to None.
        gradient_colors (list, optional): A list of two or more hex color codes for a gradient background. E.g., ['#F0F2F6', '#DCDCDC']. Defaults to None.
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
        # Example: linear-gradient(to right, #F0F2F6, #DCDCDC);
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
        # Default fallback to a simple light grey if no specific background is chosen
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
# **Choose ONE of the options below by uncommenting it:**

# Option 1: Image Background
# set_background(image_file='./your_background_image.png')
# IMPORTANT: Make sure 'your_background_image.png' is in your GitHub repo!

# Option 2: Gradient Background (Recommended for a clean, modern look)
set_background(gradient_colors=['#000000', '#2C3E50']) # Dark gradient for a sleek, cosmic feel
# You can try other gradients, e.g., ['#F0F2F6', '#DCDCDC'] for light gray, or ['#ADD8E6', '#87CEEB'] for light blue

# Option 3: Solid Color Background (if you want something very simple)
# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-color: #f0f2f6; /* A light grey */
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )


# --- Helper Functions for Lottie Animations ---
@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 🕱️ Title
st.markdown("<h1 style='text-align: center; color: #64FFDA;'> Quantum Explained Visually</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Same atom: peaceful energy or devastating weapon? A journey through quantum possibilities.</h4>", unsafe_allow_html=True)
st.markdown("---")

# ⚖️ Choice
st.markdown("<h3><p style='text-align: center;'>Choose the path of humanity:</p></h3>", unsafe_allow_html=True)
choice = st.radio("", ["☮️ Peace", "💣 Destruction"], horizontal=True, label_visibility="collapsed")
st.markdown("---")

# 🔬 Animated Atomic Structure
st.header("🔬 Visualizing Atomic Structure (Animated)")
st.markdown("<p style='text-align: center; color: gray;'>Witness the dance of electrons around the nucleus.</p>", unsafe_allow_html=True)

# Animation control
animation_speed = st.slider("Electron Orbit Speed", 0.1, 2.0, 1.0, 0.1)

# Create a placeholder for the plot to update it
atomic_structure_placeholder = st.empty()

# Animation loop for electrons
for i in range(100): # Loop for 100 frames of animation
    t = i * 0.05 * animation_speed # Time variable for animation

    # Nucleus
    nucleus_x = [0]
    nucleus_y = [0]

    # Electron 1 (orbiting)
    electron1_radius = 1
    electron1_x = [electron1_radius * np.cos(t)]
    electron1_y = [electron1_radius * np.sin(t)]

    # Electron 2 (orbiting in opposite direction)
    electron2_radius = 1.2
    electron2_x = [electron2_radius * np.cos(t + np.pi)]
    electron2_y = [electron2_radius * np.sin(t + np.pi)]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=nucleus_x, y=nucleus_y, mode='markers', marker=dict(size=40, color='red', symbol='circle'), name='Nucleus (Protons & Neutrons)'))
    fig.add_trace(go.Scatter(x=electron1_x, y=electron1_y, mode='markers', marker=dict(size=15, color='blue', symbol='circle'), name='Electron 1'))
    fig.add_trace(go.Scatter(x=electron2_x, y=electron2_y, mode='markers', marker=dict(size=15, color='green', symbol='circle'), name='Electron 2'))

    # Add orbit paths (faint lines)
    orbit_t = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(go.Scatter(x=electron1_radius * np.cos(orbit_t), y=electron1_radius * np.sin(orbit_t), mode='lines', line=dict(color='blue', dash='dot', width=1), showlegend=False))
    fig.add_trace(go.Scatter(x=electron2_radius * np.cos(orbit_t), y=electron2_radius * np.sin(orbit_t), mode='lines', line=dict(color='green', dash='dot', width=1), showlegend=False))


    fig.update_layout(
        xaxis=dict(visible=False, range=[-1.5, 1.5]),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1, range=[-1.5, 1.5]), # Ensure aspect ratio
        showlegend=False,
        width=700,
        height=500,
        plot_bgcolor="black", # Background color for the plot area
        paper_bgcolor="black", # Background color for the entire figure (outside the plot area)
        margin=dict(l=0, r=0, t=0, b=0)
    )
    with atomic_structure_placeholder:
        st.plotly_chart(fig, use_container_width=True)
    time.sleep(0.05) # Control animation speed

st.markdown("---")

# --- Einstein's Quote and Animation ---
st.header("🎲 Einstein's Dilemma: God Doesn't Play Dice")
st.markdown("<p style='color: gray;'>Albert Einstein's famous resistance to the probabilistic nature of quantum mechanics.</p>", unsafe_allow_html=True)

col_quote, col_animation = st.columns([2, 1])

with col_quote:
    st.markdown("<h3 style='text-align: center; color: #BB86FC;'>\"God does not play dice with the universe.\"</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>- Albert Einstein</p>", unsafe_allow_html=True)

with col_animation:
    lottie_dice = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_mxgd762x.json") # Dice rolling animation
    if lottie_dice:
        st_lottie(lottie_dice, speed=1, reverse=False, loop=True, quality="high", height=200)
    else:
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/47/Dice_roll_animation.gif", caption="Conceptual representation of randomness", use_container_width=True)

st.markdown("---")
# --- End of Einstein's Quote and Animation ---

# ☮️ Peace Path
if choice == "☮️ Peace":
    st.header("🌿 Quantum for Peace: Harnessing Nature's Power")
    st.markdown("<p style='color: gray;'>Discover how quantum principles are used to heal, power, and secure our world.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2]) # Adjust column width

    with col1:
        st.success("✅ **Medical Imaging (MRI):** Powerful magnetic fields and radio waves interact with atomic nuclei to create detailed images of the human body, revolutionizing diagnostics.")
        st.success("✅ **Cancer Radiotherapy:** Precisely targeted radiation from isotopes destroys cancer cells while minimizing damage to healthy tissue.")
        st.success("✅ **Clean Energy (Nuclear Reactors):** Controlled nuclear fission releases vast amounts of energy from a small mass, providing a low-carbon power source for millions.")
        st.success("✅ **Quantum Encryption:** Leveraging principles like superposition and entanglement to create unhackable communication channels, vital for cybersecurity.")
        st.success("✅ **Atomic Clocks:** Unimaginably precise timekeeping devices based on atomic vibrations, essential for GPS and global communication networks.")

    with col2:
        lottie_clean_energy = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_e0wU3R.json") # Clean energy animation
        if lottie_clean_energy:
            st_lottie(lottie_clean_energy, speed=1, reverse=False, loop=True, quality="high", height=300)
        else:
            st.image("https://cdn.britannica.com/37/123637-050-1B14113C/nuclear-power-plant-Cattenom-France.jpg",
                     caption="Nuclear Power Plant producing clean energy",
                     use_container_width=True)

    st.subheader("📖 Fundamental Scientific Principles")
    st.code("E = mc² # Einstein's Energy-Mass Equivalence: The foundational principle behind nuclear energy, showing that mass can be converted into immense amounts of energy.", language="python")
    st.code("Ψ(x,t) # Wave Function (Schrödinger Equation): Describes the probability amplitude of a quantum particle's position and momentum, crucial for understanding atomic behavior.", language="python")
    st.markdown("> **\"He who sees all beings in the self and the self in all beings does not hate. When a man sees God in every creature, he cannot injure himself or others.\"** — *Bhagavad Gita, Chapter 6, Verse 30*")

# 💣 Destruction Path
else:
    st.header("💥 The Atomic Bomb: Power Misused, Humanity's Warning")
    st.markdown("<p style='color: gray;'>A stark reminder of the devastating consequences when quantum power is unleashed for destruction.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])

    with col1:
        st.warning("☠️ **Hiroshima (August 6, 1945):** An estimated 140,000 lives lost, a city vaporized in an instant, and the horrifying dawn of the nuclear age.")
        st.warning("☠️ **Nagasaki (August 9, 1945):** Another 74,000 lives extinguished, demonstrating the horrifying scale of atomic warfare.")
        st.warning("⚠️ **Long-term Radiation Effects:** Survivors faced severe health issues, including cancers and genetic mutations, for decades due to lingering radiation.")
        st.warning("⚠️ **Environmental Devastation:** The blasts caused widespread physical destruction and introduced radioactive fallout that contaminated land and water.")


    with col2:
        lottie_explosion = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_t3o6gq.json") # Explosion animation
        if lottie_explosion:
            st_lottie(lottie_explosion, speed=1, reverse=False, loop=False, quality="high", height=300)
        else:
            st.image("https://upload.wikimedia.org/wikipedia/commons/5/5f/Nagasakibomb.jpg",
                     caption="Mushroom Cloud over Nagasaki - August 9, 1945",
                     use_container_width=True)

    st.subheader("📊 Impact Data: The Human Cost")
    data = pd.DataFrame({
        "City": ["Hiroshima", "Nagasaki"],
        "Initial Deaths": [140000, 74000],
        "Estimated Radiation Affected (first few months)": [200000, 120000]
    })
    st.bar_chart(data.set_index("City"))

    st.subheader("🌌 The Principle Behind the Bomb: Uncontrolled Fission")
    st.code("""# Fission Chain Reaction (Simplified)
# A single neutron can trigger a cascade of nuclear reactions.
neutron_initiates_fission = True

if neutron_initiates_fission:
    # Heavy nucleus splits into lighter nuclei
    split_atom = True
    # Releases more neutrons and immense energy
    release_energy = True
    release_more_neutrons = True

    if release_more_neutrons:
        # These new neutrons hit other atoms, perpetuating the chain
        continue_chain_reaction = True
        # If uncontrolled, this leads to an explosion.
        massive_explosion = True
""", language="python")

    st.markdown("> **\"Now I am become Death, the Destroyer of Worlds.\"** — *J. Robert Oppenheimer, quoting the Bhagavad Gita upon witnessing the first atomic bomb test.*")

    # --- ADDED: Image below Oppenheimer quote ---
    st.image("./oppenheimer_test_image.jpg", caption="Trinity Test, the first atomic bomb detonation (Conceptual)", use_container_width=True)
    # Make sure 'oppenheimer_test_image.jpg' is in your folder and committed to GitHub!
    # You can change the image file name and caption as needed.
    # --- END ADDED ---

    try:
        # Assuming oppenheimer_theme.mp3 is in the same directory as your script
        with open("oppenheimer_theme.mp3", "rb") as f:
            st.audio(f.read(), format="audio/mp3", start_time=0)
    except FileNotFoundError:
        st.info("🎵 To enhance the experience, place an audio file named 'oppenheimer_theme.mp3' in the same folder as this script to play background music on the 'Destruction' path.")
    except Exception as e:
        st.error(f"Could not load audio file: {e}")

st.markdown("---")

# 📜 Timeline
st.header("📜 Timeline of Quantum Physics: A Journey of Discovery")
st.markdown("<p style='color: gray;'>Explore key milestones in the development of quantum mechanics and its applications.</p>", unsafe_allow_html=True)
try:
    # Ensure timeline.json is in the same directory as your script
    with open("timeline.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    timeline(data, height=600) # Increased height for better visibility
except FileNotFoundError:
    st.error("❌ `timeline.json` not found. Please ensure the timeline data file is in the same directory as your script. You can create one like this: "
             "```json\n[\n  {\"start_date\": {\"year\": \"1900\"}, \"text\": {\"headline\": \"Planck's Quantum Hypothesis\", \"text\": \"Max Planck introduces the idea that energy is emitted or absorbed in discrete packets called quanta.\"}},\n  {\"start_date\": {\"year\": \"1905\"}, \"text\": {\"headline\": \"Einstein and the Photoelectric Effect\", \"text\": \"Albert Einstein explains the photoelectric effect by postulatin g that light consists of particles called photons.\"}}\n]\n```")
except Exception as e:
    st.error(f"❌ Timeline failed to load: {e}. Please check the format of your `timeline.json` file.")

# 🎮 Lottie Animation: Quantum swirl
st.markdown("---")
st.header("🌌 Animated Quantum Vibe: The Fabric of Reality")
st.markdown("<p style='text-align: center; color: gray;'>A visual representation of the abstract and interconnected nature of the quantum world.</p>", unsafe_allow_html=True)

# Lottie URL has been updated here
lottie_q = load_lottieurl("https://assets.lottiefiles.com/packages/lf20_mkmq71a2.json") # New Lottie URL for Quantum Vibe
if lottie_q:
    st_lottie(lottie_q, speed=1, reverse=False, loop=True, quality="high", height=300)
else:
    st.info("Could not load Lottie animation for Quantum Vibe. Check internet connection or Lottie URL.")

# 🎥 Centered Videos
st.markdown("---")
st.header("🎥 Quantum Reality in Motion: Visualizing the Impact")
st.markdown("<div style='display: flex; justify-content: center; flex-wrap: wrap;'>", unsafe_allow_html=True) # Use flex-wrap for responsiveness

# Video 1: Oppenheimer Intro (if available)
st.markdown("<div style='margin: 10px; flex-grow: 1; min-width: 300px;'>", unsafe_allow_html=True)
try:
    # Corrected path assumption for local files (relative to script)
    with open("oppenheimer_intro.mp4", "rb") as f:
        st.video(f.read(), format="video/mp4", start_time=0)
    st.caption("A glimpse into the historical context.")
except FileNotFoundError:
    st.warning("Video 'oppenheimer_intro.mp4' not found. Please ensure the video file is in the same directory.")
except Exception as e:
    st.error(f"Error loading 'oppenheimer_intro.mp4': {e}")
st.markdown("</div>", unsafe_allow_html=True)

# Video 2: Atomic Blast (if available)
st.markdown("<div style='margin: 10px; flex-grow: 1; min-width: 300px;'>", unsafe_allow_html=True)
try:
    # Corrected path assumption for local files (relative to script)
    with open("atomic_blast.mp4", "rb") as f:
        st.video(f.read(), format="video/mp4", start_time=0)
    st.caption("The raw power of an atomic explosion.")
except FileNotFoundError:
    st.warning("Video 'atomic_blast.mp4' not found. Please ensure the video file is in the same directory (or 'videos/' subfolder if specified).")
except Exception as e:
    st.error(f"Error loading 'atomic_blast.mp4': {e}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # Close flex container

# Footer
st.markdown("---")
st.caption("Created by Nakul | Powered by Streamlit & Quantum Insights | Inspired by the profound ethics of scientific discovery.")
st.markdown("<p style='text-align: center; color: gray;'>**Your choices shape the future of quantum applications.**</p>", unsafe_allow_html=True)
