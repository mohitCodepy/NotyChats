from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
import time
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
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
class HomeView(View):
   
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        # user_obj = User.objects.all()
        print(dir(request))
        print(kwargs, args, request.get_host())
        return render(request, template_name = 'Notychat.html', context= {'path' : request.get_full_path()})
        # return render(request, 'verification.html')

class HomeView(View):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, request, *args, **kwargs):

        id = kwargs.get('id')
        print(id)
        user_detail_obj = await sync_to_async(User.objects.get)(id = id)
        # json.dumps(user_detail_obj)
        user_detail_obj = await sync_to_async(serializers.serialize)('json',[user_detail_obj])
        # user_detail_obj = User.objects.get(id = id)
        print(user_detail_obj)
        print('\n\n\n\n\n\n\n\n')
        
        await channel_layer.group_send(
            'mohit',
            {
                'type' : 'chat_message',
                'userdetail': user_detail_obj,
            }
        )
        return render(request, template_name = 'Notychat.html', context= {'path' : request.get_full_path()})

class AddFriend(View):
    def get(self, request, *args, **kwargs):

        return render(request, template_name = 'Addfriend.html')


    