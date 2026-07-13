from datetime import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('message_type', 'text')
        message = text_data_json.get('message', '')

        file_url = text_data_json.get('file_url', text_data_json.get('audio_url', ''))

        sender = self.scope['user']
        current_time = datetime.now().strftime('%I:%M %p')

        if message_type == 'text':
            await self.save_message(sender, self.room_name, message, 'text')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_type': message_type,
                'message': message,
                'file_url': file_url,
                'username': sender.username,
                'first_name': sender.first_name if sender.first_name else sender.username,
                'timestamp': current_time
            }
        )

        if self.room_name != 'global':
            room_parts = self.room_name.split('_')
            if len(room_parts) >= 3:
                receiver_id = room_parts[2] if room_parts[1] == str(sender.id) else room_parts[1]
                channel_layer = get_channel_layer()
                sender_name = sender.first_name if sender.first_name else sender.username

                await channel_layer.group_send(
                    f"user_notify_{receiver_id}",
                    {
                        "type": "send_notification",
                        "notification": {
                            "title": f"New Message from {sender_name}",
                            "body": f"Sent an attachment: {message}" if message_type != 'text' else message,
                            "sender_id": str(sender.id)
                        }
                    }
                )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message_type': event['message_type'],
            'message': event['message'],
            'file_url': event.get('file_url', ''),
            'username': event['username'],
            'first_name': event['first_name'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def save_message(self, user, room_name, message, msg_type):
        return ChatMessage.objects.create(user=user, room_name=room_name, message=message, message_type=msg_type)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.user_id = self.scope["user"].id
            self.group_name = f"user_notify_{self.user_id}"

            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "notification": event["notification"]
        }))