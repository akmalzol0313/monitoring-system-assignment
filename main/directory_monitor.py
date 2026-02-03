import os
import time
import pwd
import grp
from datetime import datetime

# 1. Configuration: Path setup for Linux environment [cite: 17, 82]
MONITOR_DIR = "./data/monitored_dir"
LOG_FILE = "./logs/directory_events.csv"

def get_metadata(filepath):
    """
    Extracts mandatory metadata using Python os and pwd modules[cite: 33, 40].
    Captures: Filename, Type, Size, Owner/Group, and Timestamps[cite: 34, 35, 36, 37, 38, 39].
    """
    s = os.stat(filepath)
    
    # Identify File Type (Regular file, directory, or symbolic link) [cite: 36]
    if os.path.islink(filepath):
        ftype = "Symbolic Link"
    elif os.path.isdir(filepath):
        ftype = "Directory"
    else:
        ftype = "Regular File"

    return {
        "type": ftype,
        "size": s.st_size, # Size in bytes [cite: 37]
        "owner": pwd.getpwuid(s.st_uid).pw_name, # Owner name [cite: 38]
        "group": grp.getgrgid(s.st_gid).gr_name, # Group name [cite: 38]
        "perms": oct(s.st_mode & 0o777), # File permissions [cite: 22]
        "mtime": datetime.fromtimestamp(s.st_mtime).strftime('%Y-%m-%d %H:%M:%S') # Mod timestamp [cite: 39]
    }

def log_to_csv(event, name, m):
    """Writes directory change logs to a structured CSV file[cite: 13, 68, 69]."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Format: Timestamp, Event, Filename, Type, Size, Owner, Permissions
    entry = f"{timestamp},{event},{name},{m['type']},{m['size']},{m['owner']},{m['perms']}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(entry)
    print(f"[!] {event} DETECTED: {name}")

def start_monitoring():
    """Main execution loop for directory monitoring[cite: 79, 81, 84]."""
    print(f"[*] Student A: Monitoring started on {MONITOR_DIR}...")
    
    # Initial snapshot to compare against [cite: 13]
    last_state = {f: get_metadata(os.path.join(MONITOR_DIR, f)) for f in os.listdir(MONITOR_DIR)}

    try:
        while True:
            time.sleep(10) # 10-second monitoring interval [cite: 42]
            current_files = os.listdir(MONITOR_DIR)
            current_state = {}

            # Detect New and Modified Files [cite: 19, 20, 26, 31]
            for f in current_files:
                path = os.path.join(MONITOR_DIR, f)
                try:
                    meta = get_metadata(path)
                    current_state[f] = meta

                    if f not in last_state:
                        log_to_csv("CREATED", f, meta) # New file detection [cite: 21]
                    elif meta != last_state[f]:
                        log_to_csv("MODIFIED", f, meta) # Changes in size/time/perms [cite: 31, 32]
                except FileNotFoundError:
                    continue

            # Detect Deleted Files [cite: 23, 24, 25]
            for f in last_state:
                if f not in current_state:
                    # Log deletion using last known metadata
                    log_to_csv("DELETED", f, last_state[f])

            last_state = current_state
            
    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped by user.")

if __name__ == "__main__":
    # Ensure log file has a header on first run
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("Timestamp,Event,Filename,Type,Size_Bytes,Owner,Permissions\n")
            
    start_monitoring()
