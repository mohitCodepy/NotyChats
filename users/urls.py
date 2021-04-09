from django.urls import path
from .views import Verification_View
urlpatterns= [
    path('verify_phone/',Verification_View.as_view(), name = 'verify_phone')
]