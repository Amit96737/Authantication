from django.http import JsonResponse
from ai.utils.langchain_helper import ask_ai

def ai_chat(request):
    user_input = request.GET.get("q")

    if not user_input:
        return JsonResponse({"error": "No question provided"})

    answer = ask_ai(user_input)

    return JsonResponse({
        "question": user_input,
        "answer": answer
    })