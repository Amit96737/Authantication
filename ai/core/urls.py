from django.urls import path
from ai.core.views import chat_boat_home

urlpatterns = [
    path('chat/', chat_boat_home, name="chat-boat-home"),
]