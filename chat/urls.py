from django.urls import path
from . import views

urlpatterns = [
    path('upload-audio/', views.upload_chat_audio, name='upload_chat_audio'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
]