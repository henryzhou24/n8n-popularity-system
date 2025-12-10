import schedule
import time
import subprocess
import sys
from datetime import datetime

def run_collector():
    print(f"\n⏰ [Scheduler] Starting update job at {datetime.now()}...")
    
    # This runs 'main.py' using the same Python environment we are in now
    result = subprocess.run([sys.executable, "main.py"])
    
    if result.returncode == 0:
        print(f"✅ [Scheduler] Job finished successfully at {datetime.now()}")
    else:
        print(f"❌ [Scheduler] Job failed! Check errors above.")

# --- Configuration ---

# 1. Schedule it to run every day at midnight
schedule.every().day.at("00:00").do(run_collector)

# (Optional: For testing, uncomment the next line to run every 1 minute)
# schedule.every(1).minutes.do(run_collector)

print("🚀 Scheduler is running!")
print("   - It will run 'main.py' every day at 00:00.")
print("   - Running one immediate update now to prove it works...")

# 2. Run once immediately so we don't have to wait 24 hours to test
run_collector()

# 3. Keep the script alive forever
while True:
    schedule.run_pending()
    time.sleep(60) # Check every minute