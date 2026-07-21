from datetime import datetime
import schedule
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

ETL_SCRIPT = BASE_DIR / "scripts" / "etl_pipeline.py"

def run_etl():
    print("=" * 60)
    print(f"[{datetime.now()}] Starting Scheduled ETL Pipeline...")
    print("=" * 60)
    
    import sys
    
    result = subprocess.run(
    [sys.executable, str(ETL_SCRIPT)],
    capture_output=True,
    text=True
)

    print(result.stdout)

    if result.returncode != 0:
        print("ETL FAILED")
        print(result.stderr)
    else:
        print("ETL Completed Successfully!")

    print("=" * 60)




# Monday to Friday at 8:00 PM
schedule.every().monday.at("20:00").do(run_etl)
schedule.every().tuesday.at("20:00").do(run_etl)
schedule.every().wednesday.at("20:00").do(run_etl)
schedule.every().thursday.at("20:00").do(run_etl)
schedule.every().friday.at("20:00").do(run_etl)

print("Scheduled ETL started.")
print("Waiting for weekdays at 8:00 PM...")

while True:
    schedule.run_pending()
    time.sleep(60)