from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from users.models import User
from django.core import serializers
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('connected successfully')
        await self.accept()
        user_obj =  await sync_to_async(User.objects.all)()
        user_obj = await sync_to_async(serializers.serialize)('json', user_obj)
        await self.send(json.dumps({'reply' : 'hello frontend', 'db' : user_obj }))

    async def receive(self, text_data):
       print('receive')

    async def disconnect(self, event):
        await self.close()
