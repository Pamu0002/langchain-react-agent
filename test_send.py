#!/usr/bin/env python3
import requests
import json

url = 'http://localhost:8000/chat'
payload = {'message': 'Test message: Can you help me with this?', 'session_id': None}

try:
    print("Testing API...")
    response = requests.post(url, json=payload, timeout=10)
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'✅ API Working!')
        print(f'Session ID: {data.get("session_id")}')
        print(f'Agent Used: {data.get("agent_used")}')
        print(f'Response: {data["response"][:150]}...')
    else:
        print(f'❌ Error: {response.text}')
except Exception as e:
    print(f'❌ Connection error: {e}')
