from django.urls import path
from .views import chat_boat_app, master_chef_app

urlpatterns = [
    path('chat-app/', chat_boat_app, name="chat-boat"),
    path('master-chef-app/', master_chef_app, name="master-chef"),
]