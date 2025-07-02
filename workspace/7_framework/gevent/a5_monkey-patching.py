# Monkey patching
# Monkey patching makes standard library functions gevent-aware
# Monkey patching replaces standard library blocking calls (like time.sleep, socket, etc.) with Gevent-cooperative versions.

# 1. Monkey patching should be the very first thing executed.
from gevent import monkey
monkey.patch_all()

import time
import gevent
import requests
from typing import List, Dict, Any

# --- Configuration ---
# Use a session object for connection pooling and better performance.
HTTP_SESSION = requests.Session()

URLS_TO_FETCH = [
    'https://httpbin.org/delay/2',  # Delays response by 2 seconds
    'https://httpbin.org/delay/1',  # Delays response by 1 second
    'https://httpbin.org/json',
    'https://httpbin.org/html',
    'https://httpbin.org/status/418', # I'm a teapot
    'https://httpbin.org/invalid-url' # This will result in a 404
]

# --- Core Logic ---

def fetch_url(url: str) -> Dict[str, Any]:
    """
    Fetches a single URL and returns a dictionary with its details.
    Separates the "work" from the "printing".
    """
    print(f"  -> Starting request to {url}")
    start_time = time.time()
    try:
        # Use the global session object
        with HTTP_SESSION.get(url, timeout=10) as response:
            response_time = time.time() - start_time
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

            print(f"  <- Finished {url} in {response_time:.2f}s")
            return {
                'url': url,
                'status': response.status_code,
                'time_seconds': response_time,
                'size_bytes': len(response.content),
                'error': None
            }
    except requests.exceptions.RequestException as e:
        response_time = time.time() - start_time
        print(f"  <- FAILED {url} in {response_time:.2f}s: {e}")
        return {
            'url': url,
            'status': None,
            'time_seconds': response_time,
            'size_bytes': 0,
            'error': str(e)
        }

# --- Orchestration and Display ---

def process_results(results: List[Dict[str, Any]]):
    """Processes and prints the results from the greenlets."""
    print("\n--- Results ---")
    successful_requests = []
    failed_requests = []

    for res in results:
        if res['error']:
            failed_requests.append(res)
        else:
            successful_requests.append(res)
            print(
                f"✅ Success: {res['url']} | "
                f"Status: {res['status']} | "
                f"Time: {res['time_seconds']:.2f}s | "
                f"Size: {res['size_bytes']} bytes"
            )

    if failed_requests:
        print("\n--- Failed Requests ---")
        for res in failed_requests:
            print(f"❌ Failed:  {res['url']} | Error: {res['error']}")

def run_concurrent_benchmark():
    """Spawns greenlets to fetch all URLs concurrently and reports the time."""
    print("🚀 Starting concurrent fetching with gevent...")

    start_time = time.time()

    # Spawn a greenlet for each URL
    greenlets = [gevent.spawn(fetch_url, url) for url in URLS_TO_FETCH]

    # Wait for all greenlets to complete and retrieve their results
    gevent.joinall(greenlets, timeout=20)

    total_time = time.time() - start_time

    # Safely get values from potentially unfinished greenlets
    results = [g.value for g in greenlets if g.value is not None]

    print(f"\n✨ Concurrent execution finished in {total_time:.2f} seconds.")

    process_results(results)

    # --- Comparison ---
    # A true sequential run would take the sum of individual times.
    total_sequential_time = sum(r['time_seconds'] for r in results)
    print("\n--- Comparison ---")
    print(f"Total time for concurrent requests: {total_time:.2f}s")
    print(f"Theoretical time for sequential requests: {total_sequential_time:.2f}s")
    print(f"Performance Improvement: Concurrent was ~{total_sequential_time / total_time:.1f}x faster.")


if __name__ == "__main__":
    run_concurrent_benchmark()
