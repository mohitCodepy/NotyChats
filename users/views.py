from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
import random
from .models import User
import http.client
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

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
        if request.user.is_authenticated:
            return redirect('/home')
        return render(request, template_name = self.template_name)
    def post(self, request, *args, **kwargs):
        phone  = request.POST.get('phone','')
        print(phone)
        if phone!='':
            try:
                if User.objects.filter(phone = int(phone), is_active = False).exists():
                    request.session['phone'] = phone
                    messages.success(request, 'Please regenerate your OTP ! Click on resend')
                    return render(request, 'verify_otp.html')
                if User.objects.filter(phone = int(phone)).exists():
                    request.session['phone'] = phone
                    messages.success(request, 'Number already registered  ')
                    return redirect('/auth/verify_otp/')
                otp_gen =  random.randint(100000,999999)
                request.session['phone'] = phone
                request.session['otp_gen'] = otp_gen
                print(phone, otp_gen)
                user_obj = User.objects.create_user(phone = int(phone), full_name = "unknown",password = str(otp_gen), is_active = False)
                if user_obj != None:
                    user_obj.save()
                    send_otp(phone, otp_gen)
                    messages.success(request, f'Enter the OTP sent to {phone}')
                    return render(request, 'verify_otp.html')
            except:
                messages.warning(request, 'Phone number must contains digits')
                return render(request, 'verification.html')
        messages.warning(request, 'Oops! enter the phone number')
        return render(request, 'verification.html')

class LoginView(View):
    template_name = 'verify_otp.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, template_name = self.template_name)
    def post(self, request, *args, **kwargs):
        phone = request.session.get('phone')
        user_otp = request.POST.get('otp')
        otp_gen = request.session.get('otp_gen')
        user = authenticate(request, phone = int(phone), password = user_otp)
        print(user,'data')
        if user!= None:
            print('jai')
            login(request, user)
            return redirect('/home')
        print(type(user_otp), type(otp_gen))
        if User.objects.filter(phone = phone).exists():
            print("hello")
            user_obj = User.objects.get(phone = phone) 
            if int(user_otp) == otp_gen:
                user_obj.is_active = True
                user_obj.save()
                user = authenticate(request, phone = int(phone), password = user_otp)
                print("hello")
                print(user)
                login(request, user_obj)
                return redirect('/home')
            messages.warning(request, 'Wrong OTP')
            return redirect('/auth/verify_otp/')
        else:
            return redirect('/auth/verify_phone')

class Resend_otp(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        phone = request.session.get('phone')
        print(phone)
        try:
            user_obj = get_object_or_404(User, phone = int(phone))
            otp_gen = random.randint(100000,999999)
            request.session['otp_gen'] = otp_gen
            user_obj.set_password(str(otp_gen))
            user_obj.save()
            send_otp(user_obj.phone, otp_gen)
            return redirect('/auth/verify_otp/')
        except Exception as e:
            print(e)
            messages.warning(request, 'No user registered with this number ')
            return render(request, 'verification.html')
        messages.warning(request, 'Uhoo ! Sent OTP successfully')
        return render(request, 'verification.html')

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('/auth/verify_phone/')