from django.urls import path
from news.core import views

urlpatterns = [
    path('news/', views.news_details, name='news_details'),
    path('news_home/', views.news_home_page, name='news_home_page'),
]
