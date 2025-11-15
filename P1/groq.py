import requests
import os

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

def ask_groq(prompt):
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {resp.status_code} - {resp.text}"

def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        answer = ask_groq(user_input)
        print("AI:", answer)

if __name__ == "__main__":
    main()
