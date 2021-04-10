from django.shortcuts import render, redirect
from django.views.generic import View
import random
from .models import User
import http.client
from django.conf import settings
from django.contrib.auth import login, authenticate, logout

def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY 
    headers = { 'content-type': "application/json" }
    space=" "
    url = f'http://control.msg91.com/api/sendotp.php?otp={otp}&message=Please_verify_your_otp_{otp}&mobile={mobile}&authkey={authkey}&country=91'
    conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None

    
class Verification_View(View):
    template_name = 'verification.html'
    def get(self, request, *args, **kwargs):
        return render(request, template_name = self.template_name)
    def post(self, request, *args, **kwargs):
        phone  = int(request.POST.get('phone'))
        request.session['phone'] = phone
        otp_gen =  random.randint(100000,999999)
        user_obj = User.objects.create_user(phone = phone, full_name = "unknown",password = str(otp_gen), is_active = False)
        if user_obj != None:
            user_obj.save()
            send_otp(phone, otp_gen)
            # confirm_otp pr redirect krdo
        return redirect('/auth/verify_phone')

class LoginView(View):
    def post(self, request, *args, **kwargs):
        phone = request.session.get('phone')
        user_otp = request.POST.get('otp')
        if User.objects.filter(phone = phone).exists():
            user = authenticate(phone = phone, password = user_otp)
            if user:
                user_obj = User.objects.get(phone = phone)
                user_obj.is_active = True
                user_obj.save()
                login(request, user)
                return render(request, 'notychats.html',{"msg": "Let's begin your chat now"})
            else:
                return redirect('/auth/verify_phone')

                
            

