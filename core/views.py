from django.shortcuts import render
from django.views.generic import View
import time
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
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

class AddFriend(View):
    def get(self, request, *args, **kwargs):

        return render(request, template_name = 'Addfriend.html')


    