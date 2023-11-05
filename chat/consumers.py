import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from chat.models import ChatRoom, ChatMessage

online_users = set()

active_users = {}

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Add to app wide online user list
        online_users.add(self.scope['user'].username)

        # Add to chat room online users
        self.connected_users = active_users.setdefault(self.room_name, set())
        self.connected_users.add(self.scope['user'].username)
        
        # Send chat room user list on connect
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'send.initial.connected.users'}
        )


    async def disconnect(self, close_code):
        # Remove user from online list
        online_users.discard(self.scope['user'].username)

        # Remove user from room group
        self.connected_users.discard(self.scope['user'].username)

        # Send updated user list to chat room
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'send.initial.connected.users'}
        )

        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

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