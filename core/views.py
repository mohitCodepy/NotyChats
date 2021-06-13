from django.db import connection
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.utils.translation import templatize
from django.views.generic import View
import time
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
from .models import ConnectingPeople, Message
from channels.layers import get_channel_layer
from django.core import serializers  
from asgiref.sync import sync_to_async
import json
from django.utils.decorators import classonlymethod
import asyncio
from django.contrib import messages
channel_layer = get_channel_layer()


# class HomeView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return render(request, template_name = 'notychats.html')
#         return render(request, 'verification.html')
# LoginRequiredMixin


class BasePoint(View):
    def get(self, request, *args, **kwargs):
        return redirect('/home/')



#(_____________________________________________________Home / Chat Room_____________________________________________________)

class HomeView(View):
   
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            
            print(kwargs)
            

            kwargs = kwargs.get('id', None)
            print(kwargs)
            if kwargs == None:
                # messages.success(request,)
                if ConnectingPeople.objects.filter(connection_sender = request.user.id).exists():
                    recent_friend = ConnectingPeople.objects.filter(connection_sender = request.user.id).last()
                    kwargs = recent_friend.connection_receiver.id
                    return redirect('/home/'f'{kwargs}')
                # return render(request, template_name = 'Notychat.html', context= {'path' : request.get_full_path()})
                elif ConnectingPeople.objects.filter(connection_receiver = request.user.id).exists():
                    recent_friend = ConnectingPeople.objects.filter(connection_receiver = request.user.id).last()
                    kwargs = recent_friend.connection_sender.id
                    return redirect('/home/'f'{kwargs}')
                else:
                    return render(request, 'Addfriend.html',  {'warn-msg': 'Please add you friend to chat with him'})
            else:

                try:
                    kwargs = int(kwargs) 
                except:
                    return render(request, template_name = '404.html')
                if User.objects.filter(id = kwargs).exists() and (ConnectingPeople.objects.filter(connection_sender_id = request.user.id, connection_receiver_id = kwargs) or ConnectingPeople.objects.filter(connection_receiver_id = request.user.id, connection_sender_id = kwargs)):
                    print('got the id', kwargs)
                    return render(request, template_name = 'Notychat.html', context= {'path' : request.get_full_path()})
                else:
                    return render(request, template_name = '404.html')
        return render(request, 'verification.html')


#(_____________________________________________________Add Friend View_____________________________________________________)


class AddFriend(View):
    template_name = 'Addfriend.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, template_name = self.template_name)
        else:
            return render(request, 'verification.html')

    def post(self, request, *args, **kwargs):

        friend_phone = request.POST.get('phone')

        print('dfdsf')
        if not ConnectingPeople.objects.filter(connection_sender__phone = request.user.phone, connection_receiver__phone = friend_phone).exists():
            if User.objects.filter(phone = friend_phone).exists():
                print('got him')
                friend_obj = User.objects.filter(phone = friend_phone).exclude(phone = request.user.phone)
                return render(request, template_name = self.template_name, context= {'friend': friend_obj})
            else:
                return render(request, template_name = self.template_name, context= {'invite': f'Invite your friend to this awesome platform {request.get_full_path()}'})
        return render(request, template_name = self.template_name, context= {'invite': 'Already Your Friend'})
        


class ConnectFriend(View):
    def post(self, request, *args, **kwargs):
        friend_id = request.POST.get('friend_id')
        print(friend_id)
        # user_obj = User.objects.get(id = friend_id)
        group_obj =  ConnectingPeople.objects.create(connection_sender_id = request.user.id, connection_receiver_id = friend_id, request_status = "Pending")
        group_obj.save()
        return redirect('/home/')
    



class EditProfileView(View):
    template_name = 'edit_profile.html'
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        print(user_id)
        if user_id!= None:
            user_profile = User.objects.get(id = user_id)
            return render(request, template_name= self.template_name, context= {'user_profile': user_profile})
        return render(request, template_name= '404.html',)
    
    def post(self, request, *args, **kwargs):
        fullname = request.POST.get('full_name')
        picture = request.FILES.get('picture')
        bio = request.POST.get('bio',' ')

        user_obj =  get_object_or_404(User, id = request.user.id)

        if picture!=None:
            user_obj.picture = picture
            user_obj.save()
        if fullname!= None and bio!=None:
            user_obj.full_name = fullname
            user_obj.bio = bio
            user_obj.save()
        return redirect(f'/edit_profile/{request.user.id}')


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