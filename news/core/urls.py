from django.urls import path
from news.core import views

urlpatterns = [
    path('news/', views.news_details, name='news_details'),
]
