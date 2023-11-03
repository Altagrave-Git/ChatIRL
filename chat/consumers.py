import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # receive message from WebSocket
    async def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data['message']

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat.message', 'message': message}
        )

    async def chat_message(self, event):
        message = event['message']

        # send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))