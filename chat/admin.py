from django.contrib import admin
from chat.models import ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message')

admin.site.register(ChatMessage, ChatMessageAdmin)
