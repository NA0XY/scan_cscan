import streamlit as st
import scan
import cscan

def run_disk_ui():
    st.title("Disk Scheduling Simulator")
    st.caption("Supports SCAN and CSCAN algorithms. Visualize head movement and track servicing order.")

    requests_input = st.text_input("Enter disk requests (comma-separated)", "82,170,43,140,24,16,190")
    start = st.number_input("Enter initial head position", min_value=0, max_value=199, value=50)
    algorithm = st.selectbox("Choose Disk Scheduling Algorithm", ["SCAN", "CSCAN"])
    direction = st.radio("Choose initial direction (for SCAN)", ["left", "right"], horizontal=True)
    max_cylinder = st.number_input("Enter max cylinder number", min_value=1, value=199)

    if st.button("Run Scheduling"):
        try:
            requests = list(map(int, requests_input.strip().split(',')))
            if not requests:
                st.warning("Please enter at least one request.")
                return

            if algorithm == "SCAN":
                sequence, movement = scan.run_scan(requests, start, direction)
            elif algorithm == "CSCAN":
                sequence, movement = cscan.run_cscan(requests, start, max_cylinder)
            else:
                st.error("Invalid algorithm selected.")
                return

            st.success(f"Total Head Movement: {movement}")
            st.write("**Servicing Order:**")
            st.code(" → ".join(map(str, sequence)), language="text")

            # Optional matplotlib graph
            try:
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                ax.plot([start] + sequence, marker='o')
                ax.set_title(f"{algorithm} Scheduling")
                ax.set_xlabel("Operation Step")
                ax.set_ylabel("Track Number")
                st.pyplot(fig)
            except Exception as e:
                st.warning(f"Could not render graph: {e}")

        except Exception as e:
            st.error(f"Error: {e}")
