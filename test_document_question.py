import requests
import json

response = requests.post('http://localhost:8000/chat', json={
    'message': 'What are the key challenges mentioned in the document?',
    'session_id': 'test789',
    'use_multi_agent': True,
    'agent_type': 'document'
})

print('Status:', response.status_code)
print('Response (first 900 chars):')
resp_json = response.json()
content = resp_json['response']
print(content[:900])
if len(content) > 900:
    print('...[truncated]')
