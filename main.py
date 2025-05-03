# main.py

import ui
from scan import scan_schedule
from cscan import cscan_schedule

if __name__ == "__main__":
    ui.run_ui(run_scan, run_cscan)
