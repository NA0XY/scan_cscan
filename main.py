# main.py

import ui
from scan import run_scan
from cscan import run_cscan

if __name__ == "__main__":
    ui.run_ui(run_scan, run_cscan)
