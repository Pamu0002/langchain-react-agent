import requests
import json

# Test uploading test_document.txt
response = requests.post('http://localhost:8000/chat', json={
    'message': 'Summarize test_document.txt',
    'session_id': 'test456',
    'use_multi_agent': True,
    'agent_type': 'document'
})

print('Status:', response.status_code)
print('Response:')
print(json.dumps(response.json(), indent=2))
