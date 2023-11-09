from rest_framework import serializers
from chat.models import ChatRoom, ChatMessage, PrivateChat, PrivateMessage


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'title', 'slug', 'description', 'last_message', 'timestamp', 'sticky', 'users']


class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    color = serializers.CharField(source='user.color', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'text', 'timestamp', 'user', 'room', 'username', 'color']


class PrivateChatSerializer(serializers.ModelSerializer):
    usernames = serializers.SerializerMethodField()

    class Meta:
        model = PrivateChat
        fields = ['id', 'last_message', 'timestamp', 'users', 'usernames']

    def get_usernames(self, obj):
        usernames = [user.username for user in obj.users.all()]
        return usernames


class PrivateMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    color = serializers.CharField(source='user.color', read_only=True)

    class Meta:
        model = PrivateMessage
        fields = ['id', 'text', 'timestamp', 'user', 'room', 'username', 'color']