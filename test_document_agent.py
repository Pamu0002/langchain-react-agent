import requests
import json

response = requests.post('http://localhost:8000/chat', json={
    'message': 'Summarize this',
    'session_id': 'test123',
    'use_multi_agent': True,
    'agent_type': 'document'
})

print('Status:', response.status_code)
print('Response:')
print(json.dumps(response.json(), indent=2))
