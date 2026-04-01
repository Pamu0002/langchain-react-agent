#!/usr/bin/env python
import requests
import json

try:
    print("Testing API endpoint...")
    response = requests.post('http://localhost:8000/chat', 
        json={'message': 'hello', 'session_id': None},
        timeout=10)
    print('Status:', response.status_code)
    data = response.json()
    print('Response received!')
    print('Session ID:', data.get('session_id', 'N/A'))
    print('Agent used:', data.get('agent_used', 'N/A'))
    print('Response preview:', data.get('response', 'N/A')[:100])
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()
