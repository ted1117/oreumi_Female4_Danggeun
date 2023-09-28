import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # @sync_to_async
    def create_chat_message(self, message, is_read):
        Chat.objects.create(content=message, is_read=is_read)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]  # username을 추출
        time = text_data_json["time"]

        # await self.create_chat_message(message, is_read=True)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,  # username을 함께 전송
                "time": time,
            },
        )

    # stackoverflow
    from channels.db import database_sync_to_async

    @database_sync_to_async
    def create_chat(self, message, is_read):
        return Chat.objects.create(content=message, is_read=is_read)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]  # username을 추출
        time = event["time"]
        new_msg = await self.create_chat(message, is_read=True)

        # Send message and username to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "time": time,
                }  # username도 함께 전송
            )
        )