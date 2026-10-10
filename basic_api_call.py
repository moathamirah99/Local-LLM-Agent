import requests
response = requests.post('http://localhost:11434/api/generate', json={

"model": "llama3.2:1b",

"prompt": "what is the capital of jordan؟",

"stream": False

})

print(response.json()['response'])