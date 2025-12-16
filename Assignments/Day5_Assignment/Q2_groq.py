import requests
import json
import os

API_KEY=os.getenv("GROQ_API_KEY")

url="https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

user_prompt = input("Ask anything: ")
req_data = {
    "model": "openai/gpt-oss-120b",
    "messages": [
        { "role": "user", "content": user_prompt }
    ],
}

response = requests.post(url, data=json.dumps(req_data), headers=headers)
chat_output=response.json()
print("Status:", response.status_code)
print(chat_output['choices'][0]['message']['content'])


