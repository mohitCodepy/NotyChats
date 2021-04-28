from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from users.models import User
from django.core import serializers
# from channels.layers import get_channel_layer
# channel_layer = get_channel_layer()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # group_name = 
        print(self, self.scope)
        print('connected successfully')
        await self.accept()
       
        await self.channel_layer.group_add(
            'mohit',
            self.channel_name
        )
        
        user_obj =  await sync_to_async(User.objects.all)()
        user_obj = await sync_to_async(serializers.serialize)('json', user_obj)
        await self.channel_layer.group_send(
            'mohit',
            {   
                'type' :  'chat_users',            
                'msg': user_obj
            }
        )

    async def receive(self, text_data):
        datas = json.loads(text_data)
        print(datas['msg'])
        user_obj =  await sync_to_async(User.objects.all)()
        user_obj = await sync_to_async(serializers.serialize)('json', user_obj)
        await self.channel_layer.group_send(
            'mohit',
            {   
                'type' :  'chat_message',            
                'message': datas['msg'],
                'msg':    user_obj,
            }
        )

    async def disconnect(self, event):
        await self.close()

    async def chat_message(self, event):
        message = event['message']
        userss = event['msg']
        print(message)
        await self.send(text_data=json.dumps({
            'message': message,
            'msg': json.dumps({'db' : userss})
        }))
        
    async def chat_users(self, event):
        message = event['msg']
        print(message)
        await self.send(text_data=json.dumps({
            'msg': json.dumps({'db' : message})
        }))
