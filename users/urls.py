from django.urls import path
from .views import(
    Verification_View,
    LoginView, 
    Resend_otp, 
    LogoutView,
    frontpage
    )
urlpatterns= [
    path('verify_phone/',Verification_View.as_view(), name = 'verify_phone'),
    path('verify_otp/',LoginView.as_view(), name = 'verify_otp'),
    path('resend_otp/',Resend_otp.as_view(), name = 'resend_otp'),
    path('userlogout/',LogoutView.as_view(), name = 'userlogout'),
    path('frontpage/',frontpage, name = 'front'),


    
]