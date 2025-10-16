import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def call_curl():
    """Calls curl for the local URL."""
    result = subprocess.run(
        ["curl", "-s", "http://10.1.1.224:5000/"], 
        capture_output=True, text=True
    )
    return result.stdout

def run_parallel_curls(n=100):
    """Runs n curl requests in parallel."""
    results = []
    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(call_curl) for _ in range(n)]
        for future in as_completed(futures):
            results.append(future.result())
    return results

if __name__ == "__main__":
    while True:
        responses = run_parallel_curls(10)
        #print(f"Completed {len(responses)} requests.")
