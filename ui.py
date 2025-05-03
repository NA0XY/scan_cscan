import streamlit as st
import numpy as np
import pandas as pd
from scan import run_scan
from cscan import run_cscan

# --- Custom Fonts and Perplexity-like Style ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;700&display=swap');
    @font-face {
      font-family: 'Inge';
      src: url('https://fonts.cdnfonts.com/s/17307/Inge.woff') format('woff');
    }
    html, body, [class*="css"]  {
      font-family: 'IBM Plex Sans', Arial, sans-serif;
      background: #f7f7fa;
    }
    h1, h2, h3 {
      font-family: 'Inge', 'IBM Plex Sans', Arial, sans-serif;
      letter-spacing: 1px;
    }
    .stButton>button {
      font-family: 'IBM Plex Sans', Arial, sans-serif;
      font-size: 1.1em;
      border-radius: 7px;
      padding: 0.4em 1.5em;
      background: #437ef7;
      color: #fff;
      border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions for Display ---
def matrix_input(label, rows, cols, key_prefix):
    st.write(f"**{label}**")
    matrix = []
    for i in range(rows):
        cols_vals = st.text_input(f"{label} for P{i} (space separated)", key=f"{key_prefix}_{i}")
        if cols_vals:
            vals = [int(x) for x in cols_vals.strip().split()]
            if len(vals) == cols:
                matrix.append(vals)
            else:
                st.warning(f"Enter exactly {cols} values for P{i}.")
                return None
        else:
            return None
    return matrix

def vector_input(label, cols, key):
    vals = st.text_input(f"{label} (space separated)", key=key)
    if vals:
        vals = [int(x) for x in vals.strip().split()]
        if len(vals) == cols:
            return vals
        else:
            st.warning(f"Enter exactly {cols} values.")
            return None
    return None

def display_matrix(matrix, row_labels, col_labels, caption):
    st.write(f"**{caption}**")
    arr = np.array(matrix)
    st.table(
        pd.DataFrame(arr, index=row_labels, columns=col_labels)
    )

def display_state(allocation, max_demand, available, need):
    n_proc = len(allocation)
    n_res = len(available)
    proc_labels = [f"P{i}" for i in range(n_proc)]
    res_labels = [f"R{j}" for j in range(n_res)]
    display_matrix(allocation, proc_labels, res_labels, "Allocation Matrix")
    display_matrix(max_demand, proc_labels, res_labels, "Max Demand Matrix")
    display_matrix(need, proc_labels, res_labels, "Need Matrix")
    st.write(f"**Available:** {available}")

# --- Streamlit UI ---
def run_ui(bankers, recovery, scan, cscan):
    st.title("Deadlock Prevention & Recovery (DPR)")
    st.caption("Project by Tejas V K with inputs from Ayush and Muskan.")

    st.sidebar.title("Choose Module")
    module = st.sidebar.radio("Select a module", ["Banker's Algorithm", "Disk Scheduling"])

    if module == "Banker's Algorithm":
        # existing code for Banker's algorithm...
        pass

    elif module == "Disk Scheduling":
        run_disk_scheduler(scan, cscan)


def run_disk_scheduler(scan, cscan):
    st.title("Disk Scheduling Simulator")
    st.caption("Using SCAN and CSCAN Algorithms")

    disk_requests = st.text_input("Enter disk requests (space-separated):", "82 170 43 140 24 16 190")
    head = st.number_input("Initial Head Position:", min_value=0, value=50)
    direction = st.selectbox("Direction", ["Left", "Right"])

    algorithm = st.selectbox("Select Algorithm", ["SCAN", "CSCAN"])

    if st.button("Run Disk Scheduling"):
        try:
            requests = list(map(int, disk_requests.strip().split()))
            if algorithm == "SCAN":
                sequence, total = scan(requests, head, direction)
            else:
                sequence, total = cscan(requests, head, direction)

            st.success(f"Servicing Sequence: {' → '.join(map(str, sequence))}")
            st.info(f"Total Head Movement: {total} cylinders")

        except Exception as e:
            st.error(f"Error: {e}")
