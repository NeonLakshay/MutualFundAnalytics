import os
from pathlib import Path

# Get the exact absolute path to the .pbix file in the same folder
file_path = Path(__file__).resolve().parent / "bluestock_mf_dashboard.pbix"

os.startfile(str(file_path))