from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Tạo hoặc lấy phòng từ cơ sở dữ liệu
        self.room, created = await sync_to_async(Room.objects.get_or_create)(name=self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Gửi lại lịch sử tin nhắn
        messages = await self.get_message_history()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': messages
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']

        # Lưu tin nhắn vào cơ sở dữ liệu
        await self.save_message(sender, message)

        # Phát tin nhắn tới các thành viên trong phòng
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Gửi tin nhắn tới frontend
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender
        }))

    @sync_to_async
    def save_message(self, sender, content):
        Message.objects.create(room=self.room, sender=sender, content=content)

    @sync_to_async
    def get_message_history(self):
        messages = Message.objects.filter(room=self.room).order_by('timestamp')
        return [
        {
            'sender': msg.sender.username,
            'message': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for msg in messages
    ]
