import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat
import openai
from django.conf import settings


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        openai.api_key = settings.OPENAI_KEY

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
        isGPT = text_data_json["isGPT"]

        await self.create_chat(message, is_read=True)

        if isGPT:
            message = self.get_GPT_response(message)

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

    def get_GPT_response(self, user_message):
        # OpenAI GPT-3.5-turbo로 응답 생성
        response = openai.Completion.create(
            engine="text-davinci-003",  # GPT-3.5-turbo를 사용하려면 "text-davinci-003"으로 설정
            prompt=user_message,
            max_tokens=50,
            temperature=0.7
        )
        gpt3_turbo_response = response.choices[0].text.strip()
        return gpt3_turbo_response

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
        #isGPT = event["isGPT"]
        #new_msg = await self.create_chat(message, is_read=True)

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