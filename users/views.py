from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import View
import random
from .models import User
import http.client
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from asgiref.sync import sync_to_async
# (____________________________________________________ send otp api code ____________________________________________________)

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


# (________________________________________ registering and sending otp to phone no. ________________________________________)

class Verification_View(View):

    template_name = 'verification.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('/home')

        return render(request, template_name = self.template_name)


    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            phone  = request.POST.get('phone','')
            print(phone)
            if phone!='':
                print('i am inside condition')
                try:
                    if User.objects.filter(phone = int(phone), is_active = False).exists():
                        request.session['phone'] = phone
                        # messages.success(request, 'Please regenerate your OTP ! Click on resend')
                        return JsonResponse({"status":"400", 'msg':'Please regenerate your OTP ! Click on resend'})
                    if User.objects.filter(phone = int(phone)).exists():
                        print('i am inside user filter 2')
                        request.session['phone'] = phone
                        # messages.success(request, 'Number already registered  ')
                        # return redirect('/auth/verify_otp/')
                        return JsonResponse({"status":"200", 'msg': 'Number already registered'})
                    print('i am outside filter 2')
                    otp_gen =  random.randint(100000,999999)
                    request.session['phone'] = phone
                    request.session['otp_gen'] = otp_gen
                    print(phone, otp_gen)
                    user_obj = User.objects.create_user(phone = int(phone), full_name = "unknown",password = str(otp_gen), is_active = False)
                    print('created user',user_obj )
                    if user_obj != None:
                        print('user not none')
                        user_obj.save()
                        send_otp(phone, otp_gen)
                        print('otp sent')
                        # messages.success(request, f'Enter the OTP sent to {phone}')
                        return JsonResponse({"status":"200", 'msg':'Registered Successfully'})

                except Exception as e:
                    print(e)

                    # messages.warning(request, 'Phone number must contains digits')
                    return JsonResponse({"status":"400", 'msg':'Phone number must contains digits'})

            # messages.warning(request, 'Oops! enter the phone number')
            return JsonResponse({"status":"400", 'msg':'Oops! enter the phone number'})


# (________________________________________ verifying & authenticating user by phone  ________________________________________)


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
        if user!=None:
            login(request, user)
            return JsonResponse({'status':"200"})
            
        if User.objects.filter(phone = int(phone)).exists():

            user_obj = User.objects.get(phone = int(phone))
            print(user_obj) 
            if int(user_otp) == otp_gen:
                print('jjjjjjjjjj')
                user_obj.is_active = True
                user_obj.save()
                user = authenticate(request, phone = int(phone), password = user_otp)
                login(request, user_obj)

                return JsonResponse({'status':"200"})

            return JsonResponse({'status':"400", 'msg': 'Wrong OTP'})

        else:

            return redirect('/auth/verify_phone')

# (______________________________________________________ Resending otp  ______________________________________________________)


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
            return JsonResponse({'msg': 'Uhoo ! Sent OTP successfully'})
        except Exception as e:
            print(e)
            messages.warning(request, 'No user registered with this number ')
            return render(request, 'verification.html')
        # messages.warning(request, 'Uhoo ! Sent OTP successfully')

        return JsonResponse({'msg': 'Uhoo ! Sent OTP successfully'})

# (______________________________________________________ logout user ______________________________________________________)

class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('/auth/verify_phone/')
 
def frontpage(request):
    return render(request, 'search.html')