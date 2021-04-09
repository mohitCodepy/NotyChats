from django.shortcuts import render
from django.views.generic import View
import time
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name = 'notychats.html')
    