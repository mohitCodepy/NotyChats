from django.shortcuts import render
from django.views.generic import View

class Verification_View(View):
    template_name = 'verification.html'
    def get(self, request, *args, **kwargs):
        return render(request, template_name = self.template_name)