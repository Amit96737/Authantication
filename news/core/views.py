from django.shortcuts import render
import requests
import os
from .forms import NewsFilterForm

API_KEY = os.getenv("API_KEY")


def news_details(request):
    url = "https://newsdata.io/api/1/latest"
    base_params = {
        "apikey": API_KEY,
        "language": "en",
    }

    form = NewsFilterForm(request.GET or None)

    selected_category = ""
    search_query = ""

    if form.is_valid():
        selected_category = form.cleaned_data.get("category")
        search_query = form.cleaned_data.get("q")

    try:
        ticker_res = requests.get(url, params=base_params, timeout=5)
        ticker_articles = ticker_res.json().get("results", [])[:10]
    except Exception as e:
        print(f"Ticker API Error: {e}")
        ticker_articles = []

    main_params = base_params.copy()
    if selected_category:
        main_params["category"] = selected_category
    if search_query:
        main_params["q"] = search_query

    try:
        res = requests.get(url, params=main_params, timeout=10)
        articles = res.json().get("results", [])
    except Exception as e:
        print(f"Main API Error: {e}")
        articles = []

    return render(request, "news/news_details.html", {
        "articles": articles,
        "ticker_articles": ticker_articles,
        "form": form,
    })