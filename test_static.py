#!/usr/bin/env python3
import requests

print("Testing static file serving...")
try:
    response = requests.get("http://localhost:8000/static/app.js", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Content Length: {len(response.content)}")
    print(f"First 150 chars:\n{response.text[:150]}")
except Exception as e:
    print(f"Error: {e}")

print("\n\nTesting index.html...")
try:
    response = requests.get("http://localhost:8000/", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Content Length: {len(response.content)}")
    print(f"First 200 chars:\n{response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
