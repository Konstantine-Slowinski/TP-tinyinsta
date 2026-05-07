import subprocess
import csv
import os
import time

# Configurations
APP_URL = "https://tiny-instagram-489816.appspot.com"
LOCUST_FILE = "locustfile.py"
OUT_DIR = "out"
RUN_TIME = "60s"  # How long to run each test

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

def run_locust_test(users, spawn_rate):
    """Runs Locust headlessly and returns stats from the resulting CSV."""
    prefix = f"{OUT_DIR}/tmp_stats"
    cmd = [
        "locust", "-f", LOCUST_FILE, "--headless",
        "-u", str(users), "-r", str(spawn_rate),
        "-t", RUN_TIME, "--host", APP_URL,
        "--csv", prefix, "--only-summary"
    ]
    print(f"--- Running test with {users} users ---")
    # We remove check=True because Locust returns exit code 1 if any request fails.
    subprocess.run(cmd, capture_output=True)
    
    # Read the summary stats
    stats_file = f"{prefix}_stats.csv"
    avg_latency = 0
    failure_count = 0
    
    if os.path.exists(stats_file):
        with open(stats_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Name'] == 'Aggregated':
                    avg_latency = int(float(row['Average Response Time']))
                    failure_count = int(row['Failure Count'])
                    break
    
    # Clean up temp files
    for f in os.listdir(OUT_DIR):
        if f.startswith("tmp_stats"):
            os.remove(os.path.join(OUT_DIR, f))
            
    return avg_latency, failure_count

def get_instance_count():
    """Fetches the current number of GAE instances."""
    # We list instances and count the lines of output (excluding header)
    cmd = ["gcloud", "app", "instances", "list", "--format=csv(instance)"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    return str(len(lines) - 1) if len(lines) > 1 else "1"

def run_task_1():
    print("\n--- Starting Task 1: Concurrency Benchmark ---")
    csv_path = f"{OUT_DIR}/conc.csv"
    completed = load_existing_results(csv_path)
    results = [] # We'll load existing into here first if we want to append
    
    # Configurations: 1, 10, 20, 50, 100, 1000 users
    for u in [1, 10, 20, 50, 100, 1000]:
        for run in range(1, 4): # Repeat 3 times
            if (u, run) in completed:
                print(f"Skipping: {u} users, Run {run} (Already in CSV)")
                continue

            avg_latency, failures = run_locust_test(u, max(1, u // 10))
            instances = get_instance_count()
            
            # Format: PARAM, AVG_TIME, RUN, FAILED, NB instances
            # FAILED is 1 if any failure occurred, else 0
            is_failed = 1 if failures > 0 else 0
            results.append([u, f"{avg_latency}ms", run, is_failed, instances])
            
            print(f"Done: {u} users, Run {run}, Latency: {avg_latency}ms, Instances: {instances}")
            time.sleep(5) # Brief cooldown between runs

    # Append new results to the file
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["PARAM", "AVG_TIME", "RUN", "FAILED", "NB instances"])
        writer.writerows(results)
    print(f"Task 1 progress saved to {csv_path}")

def run_task_2():
    """Passage à l'échelle sur taille des données (Fanout)"""
    print("\n--- Starting Task 2: Fanout Benchmark ---")
    csv_path = f"{OUT_DIR}/fanout.csv"
    completed = load_existing_results(csv_path)
    results = []

    # Configurations: 20, 40, 60 followees with 50 concurrent users
    users_count = 50
    for f_count in [20, 40, 60]:
        for run in range(1, 4):
            if (f_count, run) in completed:
                print(f"Skipping: {f_count} followees, Run {run} (Already in CSV)")
                continue
            
            # Update the environment for the fanout size
            print(f"Updating users to have {f_count} followees...")
            subprocess.run(["python3", "update_followees.py", "--count", str(f_count)], check=True)

            # Run the load test
            avg_latency, failures = run_locust_test(users_count, 5)
            instances = get_instance_count()
            
            is_failed = 1 if failures > 0 else 0
            results.append([f_count, f"{avg_latency}ms", run, is_failed, instances])
            
            print(f"Done: {f_count} followees, Run {run}, Latency: {avg_latency}ms, Instances: {instances}")
            time.sleep(5)

    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["PARAM", "AVG_TIME", "RUN", "FAILED", "Nb instances"])
        writer.writerows(results)
    print(f"Task 2 progress saved to {csv_path}")

if __name__ == "__main__":
    start_time = time.time()
    
    # Run both tasks
    run_task_1()
    run_task_2()

    end_time = time.time()
    print(f"\nBenchmark complete in {int(end_time - start_time)}s.")
