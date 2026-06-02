from django.urls import path
from .views import chat_boat_app

urlpatterns = [
    path('chat/', chat_boat_app, name="chat-boat"),
]