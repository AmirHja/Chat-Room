import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'


        try:
            self.room = await self.get_room(self.room_name)
        except Room.DoesNotExist:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message', '').strip()
        user = self.scope["user"]

        if isinstance(user, AnonymousUser) or not message_content:
            return

        msg = await self.save_message(user, self.room, message_content)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.message,
                "username": user.username,
                "timestamp": str(msg.created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"],
        }))

    @staticmethod
    async def get_room(room_name):
        return await Room.objects.aget(name=room_name)

    @staticmethod
    async def save_message(user, room, message_content):
        return await Message.objects.acreate(user=user, room=room, message=message_content)
