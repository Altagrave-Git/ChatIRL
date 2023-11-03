from rest_framework import serializers
from chat.models import ChatRoom, ChatMessage


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'title', 'slug', 'last_message', 'timestamp', 'users']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'timestamp', 'user', 'room']