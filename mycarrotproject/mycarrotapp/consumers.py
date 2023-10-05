import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, ChatRoom, UserInfo, User
import openai
from django.conf import settings
import asyncio
from django.db.models import F, Q

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
        if "mark_as_read" in text_data_json:
            await self.mark_as_read(text_data_json) 
        else:
            message = text_data_json["message"]
            #roomname = text_data_json["roomname"]
            roomname = self.room_name
            username = text_data_json["username"]  # username을 추출
            time = text_data_json["time"]
            isGPT = text_data_json["isGPT"]

            if isGPT:
                await self.get_GPT_response(message, time)
                return
            new_msg = await self.create_chat(message, roomname, username, is_read=False)
            
                # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "roomname": roomname,
                    "username": username,
                    "time": time,
                    "message_id": new_msg.id
                },
            )

            if isGPT:
                await self.get_GPT_response(message, time)
        
        '''
        await self.create_chat(message, is_read=True)

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

        if isGPT:
            await self.get_GPT_response(message, time)
        '''

    async def mark_as_read(self, event):
        message_id = event["message_id"]
        message_sender = event["username"]
        room_id = self.room_name
        message = await self.get_message_by_id(message_id, room_id)
        await self.save_messages(room_id, message_id)
        # 메시지를 읽었을 때에만 is_read를 True로 설정
        if message:
            pass
            message.is_read = True
            await self.save_message(message)

        # 읽음 상태를 브로드캐스팅
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "read_status",
                "message_id": message_id,
                "message_sender": message_sender
            }
        )

    # Receive read status from room group
    async def read_status(self, event):
        message_id = event["message_id"]
        message_sender = event["message_sender"]

        # Send read status to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "read_status": True,
                    "message_id": message_id,
                    "message_sender": message_sender
                }
            )
        )
        
    async def get_GPT_response(self, user_message, time):
        query = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1024,
            temperature=0.7
        )
        response = query['choices'][0]['message']['content'].strip()

        #await self.create_chat(response)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": response,
                "roomname": self.room_name,
                "username": "ChatGPT",
                "time": time,
            },
        )

    # stackoverflow
    from channels.db import database_sync_to_async

    @database_sync_to_async
    def create_chat(self, message, roomname, username, is_read):
        roomname = ChatRoom.objects.get(pk=roomname)
        username = User.objects.get(username=username)
        return Chat.objects.create(content=message, from_id=username, room_id=roomname, is_read=is_read)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        roomname = event["roomname"]
        username = event["username"]  # username을 추출
        time = event["time"]
        try:
            message_id = event["mesage_id"]
        except:
            message_id = 99999
        #message_id = event["message_id"] if event["message_id"] else 9999
        #isGPT = event.get("isGPT", False)
        #new_msg = await self.create_chat(message, is_read=True)

        # Send message and username to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "roomname": roomname,
                    "username": username,
                    "time": time,
                    "message_id": message_id
                    #"isGPT": isGPT
                }  # username도 함께 전송
            )
        )

    @database_sync_to_async
    def get_message_by_id(self, message_id, room_id):
        try:
            return Chat.objects.get(id=message_id)
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, message):
        message.save()

    @database_sync_to_async
    def save_messages(self, room_id, message_id):
        try:
            # 현재 메시지 이전의 메시지들을 가져와서 is_read를 True로 업데이트
            Chat.objects.filter(
                Q(room_id=room_id) & Q(id__lte=message_id) & Q(is_read=False)
            ).update(is_read=True)

        except Exception as e:
            print(f"An error occurred while updating messages: {e}")