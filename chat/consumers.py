import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from chat.models import ChatRoom, ChatMessage, PrivateChat, PrivateMessage
from asgiref.sync import async_to_sync, sync_to_async
from users.models import User


active_users = {}

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        self.channel_layer = get_channel_layer()

        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Add to project-wide online user list
        await self.channel_layer.group_add("online_users", self.scope['user'].username)

        # Add to chat room online users list
        self.connected_users = active_users.setdefault(self.room_name, set())
        self.connected_users.add(self.scope['user'].username)
        
        # Send chat room user list on connect
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'send.initial.connected.users'}
        )


    async def disconnect(self, close_code):
        # Remove user from online list
        self.channel_layer.group_discard('online_users', self.scope['user'].username)

        # Remove user from room group
        self.connected_users.discard(self.scope['user'].username)

        # Send updated user list to chat room
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'send.initial.connected.users'}
        )

        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        await self.close()

    # receive message from WebSocket
    async def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data['message'][:280]
        user = self.scope.get('user')
        
        await self.save_message(user, message)

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat.message', 'user': user.username, 'message': message, 'color': user.color}
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        color = event['color']

        # send message to WebSocket
        await self.send(text_data=json.dumps({'action': 'message', 'user': user, 'message': message, 'color': color}))

    @database_sync_to_async
    def save_message(self, user, message):
        room = ChatRoom.objects.get(slug=self.scope['url_route']['kwargs']['room_name'])

        message_instance = ChatMessage(
            text=message,
            user=user,
            room=room
        )
        message_instance.save()

    async def send_initial_connected_users(self, event):
        # Send list of connected users to the new user
        await self.send(text_data=json.dumps({'action': 'users', 'connected_users': list(self.connected_users)}))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope['user']
            self.target_user = await self.get_target_user(self.scope['url_route']['kwargs']['username'])
            self.channel_layer = get_channel_layer()
        except:
            self.close()

        if self.user.is_authenticated and self.user.username != self.target_user.username:
            await self.accept()
            await self.channel_layer.group_add('online_users', self.user.username)
            self.room_name = f'private_{min(self.user.username, self.target_user.username)}_{max(self.user.username, self.target_user.username)}'
            await self.channel_layer.group_add(self.room_name, self.channel_name)

        else:
            self.close()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard('online_users', self.user.username)
        self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.close()

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data['message'][:280]
        
        await self.save_message(self.user, self.target_user, message)

        # send message to room group
        await self.channel_layer.group_send(
            self.room_name, {'type': 'chat.message', 'user': self.user.username, 'message': message, 'color': self.user.color}
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        color = event['color']

        # send message to WebSocket
        await self.send(text_data=json.dumps({'action': 'message', 'user': user, 'message': message, 'color': color}))

    @database_sync_to_async
    def get_target_user(self, username):
        return User.objects.get(username=username)
    
    @database_sync_to_async
    def save_message(self, user, target_user, message):
        try:
            room = PrivateChat.objects.filter(users__in=[user, target_user])[0]
        except:
            room = PrivateChat.objects.create()
            room.users.add(user, target_user)

        message_instance = PrivateMessage(
            text=message,
            user=user,
            room=room
        )
        message_instance.save()