# Fetching web pages in sync
# it waits for the first page to be fetched before fetching the second page

import requests
import time

start_time = time.time()

def fetch_webpage(url):
    return requests.get(url).text

page1 = fetch_webpage("https://jaygaha.com.np")
page2 = fetch_webpage("https://www.google.com")

print(f"DONE in {time.time() - start_time} seconds")# DONE in 1.0 seconds