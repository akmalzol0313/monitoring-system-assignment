import os
import time

# Configuration
MONITOR_DIR = "./data/monitored_dir"
LOG_FILE = "./logs/directory_events.csv"

def setup_environment():
    """Ensure the necessary directories and log files exist."""
    # Create the directory to be monitored if it doesn't exist [cite: 82]
    if not os.path.exists(MONITOR_DIR):
        os.makedirs(MONITOR_DIR)
        print(f"[SETUP] Created directory: {MONITOR_DIR}")
    
    # Initialize the log file with headers [cite: 68, 69]
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("Timestamp,Event,Filename,Size,Owner,Permissions\n")
        print(f"[SETUP] Created log file: {LOG_FILE}")

if __name__ == "__main__":
    print("--- Directory Monitoring Module: Week 7 Setup ---")
    setup_environment()
    print("[STATUS] Environment is ready.")
