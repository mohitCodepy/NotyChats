from django.urls import path
from .views import Verification_View, LoginView
urlpatterns= [
    path('verify_phone/',Verification_View.as_view(), name = 'verify_phone'),
    path('verify_otp/',LoginView.as_view(), name = 'verify_otp')
    
]