from django.contrib import admin
from chat.models import ChatRoom, ChatMessage, PrivateChat, PrivateMessage


admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(PrivateChat)