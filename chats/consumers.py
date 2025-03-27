import json
import django
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "computerNetworkProject.settings")
django.setup()


class PublicChat(AsyncWebsocketConsumer):
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
        sender = self.scope["user"]  # تغییر از user به sender

        if isinstance(sender, AnonymousUser) or not message_content:
            return

        msg = await self.save_message(sender, self.room, message_content)  # تغییر از user به sender

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.message,
                "username": sender.username,  # تغییر از user به sender
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
    async def save_message(sender, room, message_content):  # تغییر از user به sender
        return await PublicMessage.objects.acreate(sender=sender, room=room, message=message_content)  # تغییر از user به sender


class PrivetChat(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.room_group_name = f"private_{self.user.id}"

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
        message_content = data.get("message", "").strip()
        receiver_username = data.get("receiver")

        if not message_content or not receiver_username:
            return

        try:
            receiver = await User.objects.aget(username=receiver_username)
        except User.DoesNotExist:
            return

        message = await PrivateMessage.objects.acreate(
            sender=self.user,
            receiver=receiver,
            message=message_content
        )


        await self.channel_layer.group_send(
            f"private_{receiver.id}",
            {
                "type": "private_message",
                "message": message.message,
                "sender": self.user.username,
                "timestamp": str(message.created_at),
            }
        )


        await self.channel_layer.group_send(
            f"private_{self.user.id}",
            {
                "type": "private_message",
                "message": message.message,
                "sender": self.user.username,
                "timestamp": str(message.created_at),
            }
        )

    async def private_message(self, event):

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))