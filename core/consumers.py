import asyncio
from django.contrib.auth.models import Group
from django.db import connection
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from users.models import User
from .models import ConnectingPeople, Message
from django.core import serializers
from django.shortcuts import get_object_or_404


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
#       fetching currently logged-in user 
        self.sid = ""
        self.sender_id = 0
        self.current_login_user = self.scope['user'] 
       

#       getting friend's id from url 

        self.friend_id = self.scope['url_route']['kwargs']['id'] 

        
        print('connected successfully')
        await self.accept()


#       fetching group name created at the time of friend-request sent

        self.group_name = await self.get_group_name()


#       Using friend's id fetching his profile information

        friend_details_obj = await sync_to_async(User.objects.get)(id = self.friend_id)
        self.serialized_friend_details = await sync_to_async(serializers.serialize)('json',[friend_details_obj])


#       Getting all the messages of this group 

        all_msgs_obj =  await self.get_group_msgs(self.group_name)
        self.all_msg_json = await sync_to_async(serializers.serialize)('json',all_msgs_obj)

# New code :-----------------------------------------------------------------------------------------------------------

        all_friends_obj =  await self.get_users_connections()
        self.all_friends_json =  json.dumps(all_friends_obj)
        # breakpoint()
        await self.send(text_data=json.dumps({
            #msg
            'all_friends': self.all_friends_json, 
            'message' : self.all_msg_json,
             # single_user_data
            'current_friend': json.dumps({'current_friend':self.serialized_friend_details})

        }))
# New code End:-----------------------------------------------------------------------------------------------------------




#       Adding their group_name and channel_name

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )


#       getting all friends of currently logged-in user and converting to json format

        # all_friends_obj =  await self.get_users_connections()
        # all_friends_json =  json.dumps(all_friends_obj)


#       Sending current-user ,his friends and his current friend 

        # await self.channel_layer.group_send(
        #     self.group_name,
        #     {   
        #         'type' :  'chat_users',            
        #         # msg ---> all_friends

        #         'all_friends': all_friends_json,  

        #         # single_user_data
        #         'current_friend': serialized_friend_details

        #     }
        # )

 


    # async def chat_users(self, event):

    #     all_friends = event['all_friends']

    #     current_friend = event.get('current_friend')

    #     await self.send(text_data=json.dumps({
    #         #msg
    #         'all_friends': all_friends, 

    #          # single_user_data
    #         'current_friend': json.dumps({'current_friend':current_friend})

    #     }))
    

#   getting all friends function

    @database_sync_to_async
    def get_users_connections(self):
    
        user_data = ConnectingPeople.objects.filter(connection_receiver__id = self.current_login_user.id)
        print(user_data)
        # if user_data:
        print('got the connections of user1')
        list_of_friends1 = [ 

            { 'group_id' : i.id, 
            'friend_id' : i.connection_sender.id,
            'friend_phone': i.connection_sender.phone,
            'friend_picture' : i.connection_sender.picture.url
            }
            for i in user_data
        ]
        print(list_of_friends1, 'friend 1')
        # else:
        # print('got the connections of user2')
        # user_data = ConnectingPeople.objects.filter(connection_sender__id = self.current_login_user.id)
        #  ConnectingPeople.objects.filter(connection_receiver__id = self.current_login_user.id)
        user_data1 = ConnectingPeople.objects.filter(connection_sender__id = self.current_login_user.id)
        list_of_friends = [ 

            { 'group_id' : i.id, 
            'friend_id' : i.connection_receiver.id,
            'friend_phone': i.connection_receiver.phone,
            'friend_picture' : i.connection_receiver.picture.url
            }
            for i in user_data1
        ]
        print(list_of_friends, 'is the friend list 2')
        print(list_of_friends.extend(list_of_friends1), 'this is the friend list')
        return list_of_friends


#   getting group name

    @database_sync_to_async
    def get_group_name(self):

        try: 
            group_name = ConnectingPeople.objects.get(connection_sender__id = self.current_login_user.id, connection_receiver__id = self.friend_id)
            print(group_name.group_name)

        except Exception as e:
            print(e)
            group_name = ConnectingPeople.objects.get(connection_sender__id = self.friend_id, connection_receiver__id = self.current_login_user.id)
            
            print(group_name.group_name)
        group_name = group_name.group_name

        return group_name

    
#   For disconnecting current user
    async def disconnect(self, event):
        await self.close()







#   Unused functions start -----------------------------------------------------------------------------------
    async def receive(self, text_data):
        datas = json.loads(text_data)
        print(datas['msg'], 'this is reply')
        print(datas['s_id'])
        self.sid = datas['s_id']
        print(self.sid, 'is the id of sender')
        msg = datas['msg']
        self.getting_msgs, self.sender_id =  await self.saving_msgs_to_group(self.group_name, self.sid, msg)
        
        all_msgs_obj =  await self.get_group_msgs(self.group_name)
        self.all_msg_json = await sync_to_async(serializers.serialize)('json',all_msgs_obj)
        # print(all_msgs_obj)
        # print(getting_msgs)
        # print('sudhfushdufasudfsdnf',self.friend_detail)
        # user_obj =  await sync_to_async(User.objects.all)()
        # user_obj = await sync_to_async(serializers.serialize)('json', user_obj)
        # user_detail_obj = await sync_to_async(User.objects.get)(id = self.user.id)
        # user_detail_obj = await sync_to_async(serializers.serialize)('json',[user_detail_obj])
            #   Adding their group_name and channel_name

        
        await self.channel_layer.group_send(
            self.group_name,
            {   
                'type' :  'chat_message',            
                'message': self.all_msg_json,
                'sid':  self.sender_id,
                # 'all_msgs': self.all_msgs,
            }
        )
        # await self.channel_layer.group_send(
        #     self.group_name,
        #     {   
        #         'type' :  'chat_message',            
        #         'message': datas['msg'],
        #         'current_user': self.friend_detail,
        #         'msg':    user_obj,
        #         'user_data': user_detail_obj
        #     }
        # )

    async def chat_message(self, event):
        message = event.get('message')
        sender_is = event.get('sid')
        # all_msg = event.get('all_msgs')
        # userdetail = event.get('user_data')
        # print(userdetail, 'hthththththhhhhh')
        # print(message, 'htiththth')
        await self.send(text_data=json.dumps({
            'message': message,
            'all_friends': self.all_friends_json, 
            'id': sender_is,
            # 'all_msgs': self.all_msgs,
             # single_user_data
            'current_friend': json.dumps({'current_friend':self.serialized_friend_details})
            # 'c_user':  event.get('current_user'),
            # 'msg': json.dumps({'db' : userss}),
            # 'single_data': json.dumps({'single':userdetail})
        }))

    @database_sync_to_async
    def saving_msgs_to_group(self, group_name, s_id, msg):
        get_group_obj = get_object_or_404(ConnectingPeople, group_name = group_name)

        msg_obj = Message.objects.create(group_id = get_group_obj, sender_id = int(s_id), message = msg)
        msg_obj.save()
        print(msg_obj.sender.id)
        return msg_obj, msg_obj.sender.id

    @database_sync_to_async
    def get_group_msgs(self, grp_name):
        connection_obj =  ConnectingPeople.objects.get(group_name = grp_name)
        msg_queryset =  Message.objects.filter(group_id__connection_sender = connection_obj.connection_sender, group_id__connection_receiver =  connection_obj.connection_receiver).order_by('msg_date')
        # for i in msg:
        #     print(i)
        return msg_queryset



#   Unused functions end -----------------------------------------------------------------------------------


    # async def user_detail(self, event):
        
    #     await self.send(text_data = json.dumps({'user_detail' : json.dumps(event['message'])}))

        


