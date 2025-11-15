import requests
import os
from dotenv import load_dotenv
load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

def ask_openrouter(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-3.5-turbo",  # or try "openai/gpt-4o"
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Simple chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    reply = ask_openrouter(user_input)
    print("AI:", reply)
