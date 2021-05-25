import asyncio
from django.contrib.auth.models import Group
from django.db import connection
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from users.models import User
from .models import ConnectingPeople, REQUEST_STATUS
from django.core import serializers


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.user = self.scope['user']
        print('\n\n')
        print(self.scope['url_route']['kwargs']['id'])
        print('\n\n')
        self.friend_detail = self.scope['url_route']['kwargs']['id'] 
        print(self.user.id)
         
        print(self, self.scope['user'])
        print('connected successfully')
        await self.accept()

        self.group_name = await self.get_group_name()

        user_detail_obj = await sync_to_async(User.objects.get)(id = self.friend_detail)
        user_detail_obj = await sync_to_async(serializers.serialize)('json',[user_detail_obj])


        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        user_obj =  await self.get_users_connections()
        user_obj =  json.dumps(user_obj)
        await self.channel_layer.group_send(
            self.group_name,
            {   
                'type' :  'chat_users',            
                'msg': user_obj,
                'user_data': user_detail_obj
            }
        )

    async def receive(self, text_data):
        datas = json.loads(text_data)
        print(datas['msg'])
        print('sudhfushdufasudfsdnf',self.friend_detail)
        user_obj =  await sync_to_async(User.objects.all)()
        user_obj = await sync_to_async(serializers.serialize)('json', user_obj)
        user_detail_obj = await sync_to_async(User.objects.get)(id = self.user.id)
        user_detail_obj = await sync_to_async(serializers.serialize)('json',[user_detail_obj])
        await self.channel_layer.group_send(
            self.group_name,
            {   
                'type' :  'chat_message',            
                'message': datas['msg'],
                'current_user': self.friend_detail,
                'msg':    user_obj,
                'user_data': user_detail_obj
            }
        )

    async def disconnect(self, event):
        await self.close()

    async def chat_message(self, event):
        message = event.get('message')
        userss = event.get('msg')
        userdetail = event.get('user_data')
        print(userdetail, 'hthththththhhhhh')
        print(message, 'htiththth')
        await self.send(text_data=json.dumps({
            'message': message,
            'c_user':  event.get('current_user'),
            'msg': json.dumps({'db' : userss}),
            'single_data': json.dumps({'single':userdetail})
        }))
        
    async def chat_users(self, event):
        message = event['msg']
        userdetail = event.get('user_data')
        print(message)
        await self.send(text_data=json.dumps({
            'msg': message,
            'single_data': json.dumps({'single':userdetail})
        }))
    

    @database_sync_to_async
    def get_users_connections(self):

        

        user_data = ConnectingPeople.objects.filter(connected_with__id = self.user.id)
        print(user_data)
        if user_data:
            list_of_dict = [ 

                { 'group_id' : i.id, 
                'friend_id' : i.connection_sender.id,
                'friend_phone': i.connection_sender.phone,
                'friend_picture' : i.connection_sender.picture.url
                }
                for i in user_data
            ]
        else:
            user_data = ConnectingPeople.objects.filter(connection_sender__id = self.user.id)
            list_of_dict = [ 

                { 'group_id' : i.id, 
                'friend_id' : i.connected_with.id,
                'friend_phone': i.connected_with.phone,
                'friend_picture' : i.connected_with.picture.url
                }
                for i in user_data
            ]
       
        return list_of_dict

    @database_sync_to_async
    def get_group_name(self):
        print(self.user.id, self.friend_detail)
        try:
            group_name = ConnectingPeople.objects.get(connection_sender__id = self.user.id, connected_with__id = self.friend_detail)
        except:
            group_name = ConnectingPeople.objects.get(connection_sender__id = self.friend_detail, connected_with__id = self.user.id)
            # group_name = ConnectingPeople.objects.get(connection_sender__id = self.user.id, connected_with__id = self.friend_detail)
            print(group_name.group_name)
        group_name = group_name.group_name


        return group_name

       
    













    # async def user_detail(self, event):
        
    #     await self.send(text_data = json.dumps({'user_detail' : json.dumps(event['message'])}))

        


