import requests
import os
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

url = os.getenv("OPEN_ROUTER_URL")

def chat_boat_app(request):
    user_message = request.GET.get('message')

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

    result = response.json()

    reply = result["choices"][0]["message"]["content"]

    return JsonResponse({"response": reply})

def is_food_related(text):
    food_keywords = [
        "recipe", "cook", "food", "dish", "eat", "meal",
        "pizza", "burger", "cake", "rice", "chicken"
    ]
    text = text.lower()
    return any(word in text for word in food_keywords)

def master_chef_app(request):
    user_message = request.GET.get('message')

    if not is_food_related(user_message):
        return JsonResponse({
            "response": "Master Chef: I don't know the answer."
        })

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": "Your name is Master Chef. You are a strict cooking assistant. "
                            "You MUST ONLY answer food-related questions. "
                            "If the question is NOT about food, recipes, cooking, ingredients, or meals, "
                            "you MUST reply EXACTLY with: 'Master Chef: I don't know the answer.' "
                            "Do NOT explain anything else. Do NOT answer the question."},
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    reply = result["choices"][0]["message"]["content"]

    return JsonResponse({"response": reply})