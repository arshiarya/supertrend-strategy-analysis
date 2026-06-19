import subprocess
import sys
import os
from datetime import datetime

# ---- CONFIG ----
BASE = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\3_daily_updates"
LOG  = "C:\\Users\\mayan\\OneDrive\\Desktop\\stock_market_analysis\\3_daily_updates\\update_log.txt"
# ----------------

SCRIPTS = [
    "daily_nse_price_update.py",
    "daily_bse_price_update.py",
    "daily_nse_deals_update.py",
]

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    # Fix Windows terminal encoding issue
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode('ascii', 'ignore').decode('ascii'))
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run_script(script):
    path = os.path.join(BASE, script)
    log(f"Starting {script}...")
    result = subprocess.run(
        [sys.executable, path],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )
    # Log output
    if result.stdout:
        for line in result.stdout.strip().split("\n"):
            log(f"  {line}")
    # Log errors if any
    if result.stderr:
        for line in result.stderr.strip().split("\n"):
            log(f"  ERROR: {line}")
    if result.returncode == 0:
        log(f"SUCCESS: {script} completed successfully!")
    else:
        log(f"FAILED: {script} failed with code {result.returncode}")

def main():
    log("=" * 50)
    log("DAILY MARKET UPDATE STARTED")
    log("=" * 50)

    for script in SCRIPTS:
        run_script(script)
        log("")

    log("=" * 50)
    log("DAILY MARKET UPDATE COMPLETE")
    log("=" * 50)

if __name__ == "__main__":
    main()