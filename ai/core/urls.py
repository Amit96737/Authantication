from django.urls import path
from ai.core.views import chat_boat_home, master_chef_home

urlpatterns = [
    path('chat-app/', chat_boat_home, name="chat-boat-home"),
    path('master-chef-app/', master_chef_home, name="master-chef-home"),
]