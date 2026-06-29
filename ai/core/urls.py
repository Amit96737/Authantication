from django.urls import path
from ai.core.views import chat_boat_home, master_chef_home, chat_about_page

urlpatterns = [
    path('chat-about-page/', chat_about_page, name="chat_about_page"),
    path('chat-app/', chat_boat_home, name="chat-boat-home"),
    path('master-chef-app/', master_chef_home, name="master-chef-home"),
]