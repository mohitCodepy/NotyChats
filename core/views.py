from django.db import connection
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.translation import templatize
from django.views.generic import View
import time
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
from .models import ConnectingPeople
from channels.layers import get_channel_layer
from django.core import serializers  
from asgiref.sync import sync_to_async
import json
from django.utils.decorators import classonlymethod
import asyncio
channel_layer = get_channel_layer()


# class HomeView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return render(request, template_name = 'notychats.html')
#         return render(request, 'verification.html')
# LoginRequiredMixin

#(_____________________________________________________Home / Chat Room_____________________________________________________)

class HomeView(View):
   
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        # user_obj = User.objects.all()
        print(dir(request))
        print(kwargs, args, request.get_host())
        return render(request, template_name = 'Notychat.html', context= {'path' : request.get_full_path()})
        # return render(request, 'verification.html')


#(_____________________________________________________Add Friend View_____________________________________________________)


class AddFriend(View):
    template_name = 'Addfriend.html'
    def get(self, request, *args, **kwargs):

        return render(request, template_name = self.template_name)

    def post(self, request, *args, **kwargs):

        friend_phone = request.POST.get('phone')

        print('dfdsf')
        if not ConnectingPeople.objects.filter(connection_sender__phone = request.user.phone, connected_with__phone = friend_phone).exists():
            if User.objects.filter(phone = friend_phone).exists():
                print('got him')
                friend_obj = User.objects.filter(phone = friend_phone).exclude(phone = request.user.phone)
                return render(request, template_name = self.template_name, context= {'friend': friend_obj})
        return render(request, template_name = self.template_name, context= {'invite': 'Already Your Friend'})
        return render(request, template_name = self.template_name, context= {'invite': 'Invite your friend to this awesome platform'})


class ConnectFriend(View):
    def post(self, request, *args, **kwargs):
        friend_id = request.POST.get('friend_id')
        print(friend_id)
        # user_obj = User.objects.get(id = friend_id)
        group_obj =  ConnectingPeople.objects.create(connection_sender_id = request.user.id, connected_with_id = friend_id, request_status = "Pending")
        group_obj.save()
        return redirect('/addfriend/')
    










# class HomeView(View):
#     @classonlymethod
#     def as_view(cls, **initkwargs):
#         view = super().as_view(**initkwargs)
#         view._is_coroutine = asyncio.coroutines._is_coroutine
#         return view

#     async def get(self, request, *args, **kwargs):

#         id = kwargs.get('id')
#         print(id)
#         user_detail_obj = await sync_to_async(User.objects.get)(id = id)
#         # json.dumps(user_detail_obj)
#         user_detail_obj = await sync_to_async(serializers.serialize)('json',[user_detail_obj])
#         # user_detail_obj = User.objects.get(id = id)
#         print(user_detail_obj)
#         print('\n\n\n\n\n\n\n\n')
        
#         await channel_layer.group_send(
#             'mohit',
#             {
#                 'type' : 'chat_message',
#                 'userdetail': user_detail_obj,
#             }
#         )
#         return render(request, template_name = 'Notychat.html', context= {'path' : request.get_full_path()})