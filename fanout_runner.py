import subprocess
import csv
import os
import time

# Configurations for Task 2 (Fanout Scaling)
APP_URL = "https://tiny-instagram-489816.appspot.com"
LOCUST_FILE = "locustfile.py"
OUT_DIR = "out"
RUN_TIME = "60s"
CONCURRENT_USERS = 50

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

def load_existing_results(filename):
    """Reads the CSV and returns a set of (param, run) tuples already completed."""
    completed = set()
    if os.path.exists(filename):
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    completed.add((int(row['PARAM']), int(row['RUN'])))
                except (ValueError, KeyError):
                    continue
    return completed

def get_instance_count():
    """Fetches the current number of GAE instances."""
    cmd = ["gcloud", "app", "instances", "list", "--format=csv(instance)"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    # We count lines minus header
    return str(len(lines) - 1) if len(lines) > 1 else "1"

def run_locust_test(users, spawn_rate):
    """Runs Locust headlessly and returns stats from the resulting CSV."""
    prefix = f"{OUT_DIR}/tmp_fanout"
    cmd = [
        "locust", "-f", LOCUST_FILE, "--headless",
        "-u", str(users), "-r", str(spawn_rate),
        "-t", RUN_TIME, "--host", APP_URL,
        "--csv", prefix, "--only-summary"
    ]
    subprocess.run(cmd, capture_output=True)
    
    stats_file = f"{prefix}_stats.csv"
    avg_latency, failure_count = 0, 0
    if os.path.exists(stats_file):
        with open(stats_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Name'] == 'Aggregated':
                    avg_latency = int(float(row['Average Response Time']))
                    failure_count = int(row['Failure Count'])
                    break
    
    # Cleanup temp files
    for f in os.listdir(OUT_DIR):
        if f.startswith("tmp_fanout"):
            os.remove(os.path.join(OUT_DIR, f))
    return avg_latency, failure_count

if __name__ == "__main__":
    csv_path = f"{OUT_DIR}/fanout.csv"
    completed = load_existing_results(csv_path)
    
    print("\n--- Starting Task 2: Fanout Benchmark ---")
    print("Note: Ensure you have seeded 1000 users and 100 posts/user first.")
    
    # Configurations: 20, 40, 60 followees
    for f_count in [20, 40, 60]:
        for run in range(1, 4):
            if (f_count, run) in completed:
                print(f"Skipping: {f_count} followees, Run {run} (Already in CSV)")
                continue

            print(f"Updating users to have {f_count} followees...")
            subprocess.run(["python3", "update_followees.py", "--count", str(f_count)], check=True)
            
            avg_latency, failures = run_locust_test(CONCURRENT_USERS, 5)
            instances = get_instance_count()
            is_failed = 1 if failures > 0 else 0
            
            file_exists = os.path.isfile(csv_path)
            with open(csv_path, "a", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["PARAM", "AVG_TIME", "RUN", "FAILED", "Nb instances"])
                writer.writerow([f_count, f"{avg_latency}ms", run, is_failed, instances])
            
            print(f"Done: {f_count} followees, Run {run}, Latency: {avg_latency}ms, Instances: {instances}")
            time.sleep(5) # Brief cooldown