import streamlit as st
import matplotlib.pyplot as plt
from scan import run_scan
from cscan import run_cscan

def run_ui():
    # Page config
    st.set_page_config(
        page_title="Disk Scheduling Visualizer",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # === Theme: Material Design ===
    st.markdown(
        """
        <style>
        body, .css-1d391kg, .css-16huue1 {
            background-color: #F5F5F5 !important;
            color: #212121 !important;
        }
        .stTextInput > label, .stNumberInput > label {
            color: #212121 !important;
        }
        .stSelectbox > label, .stRadio > label {
            color: #212121 !important;
        }
        .stButton>button {
            background-color: #6200EE !important;
            color: #ffffff !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            border-radius: 4px;
            font-weight: 500;
        }
        .stButton>button:hover {
            background-color: #3700B3 !important;
        }
        .stSlider > label {
            color: #212121 !important;
        }
        .stTextInput, .stNumberInput, .stSelectbox, .stRadio {
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stTextInput input, .stNumberInput input, .stSelectbox select, .stRadio label {
            background-color: white !important;
            border-radius: 4px;
            padding: 10px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # === Title & Description ===
    st.title("🧠 Disk Scheduling Algorithms")
    st.write("Visualize **SCAN** and **C-SCAN** disk scheduling with accurate head movement tracking.")

    # === Inputs ===
    raw_requests = st.text_input(
        "Disk requests (comma-separated)", 
        value="82,170,43,140,24,16,190"
    )
    try:
        requests = list(map(int, raw_requests.strip().split(',')))
    except ValueError:
        st.error("Please enter comma-separated integers for disk requests.")
        return

    start = st.number_input(
        "Initial head position", 
        min_value=0, 
        value=50, 
        step=1
    )

    algo = st.selectbox(
        "Choose algorithm", 
        ("SCAN", "C-SCAN")
    )

    direction = st.radio(
        "Direction",
        ("right", "left"),
        index=0
    )

    max_cylinder = None
    if algo == "C-SCAN":
        max_cylinder = st.number_input(
            "Maximum cylinder number", 
            min_value=1, 
            value=200, 
            step=1
        )

    # === Run Button ===
    if st.button("Run Scheduling"):
        if not requests:
            st.error("No disk requests provided.")
            return

        # Call the appropriate algorithm
        if algo == "SCAN":
            sequence, movement = run_scan(requests, start, direction)
        else:
            # for C-SCAN, pass max_cylinder - 1 as the highest index
            sequence, movement = run_cscan(requests, start, direction, max_cylinder - 1)

        # === Results ===
        st.subheader("Results")
        st.success(f"Total head movement: {movement} cylinders")
        st.markdown("**Servicing sequence:**")
        st.code(" → ".join(map(str, sequence)), language="text")

        # === Plot ===
        fig, ax = plt.subplots()
        x = [start] + sequence
        ax.plot(range(len(x)), x, marker='o')
        ax.set_title(f"{algo} ({direction})")
        ax.set_xlabel("Step")
        ax.set_ylabel("Cylinder Number")
        ax.grid(True)
        st.pyplot(fig)
