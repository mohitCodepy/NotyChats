from django.shortcuts import render
from django.views.generic import View
import time
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name = 'notychats.html')
    