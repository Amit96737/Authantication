import requests
import os
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def chat_boat_app(request):
    user_message = request.GET.get('message')
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    print("response", response)

    result = response.json()

    reply = result["choices"][0]["message"]["content"]

    return JsonResponse({"response": reply})