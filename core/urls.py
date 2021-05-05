from django.urls import path, re_path
from .views import HomeView, AddFriend
urlpatterns=[
    re_path(r'^home/*',HomeView.as_view(), name = 'home'),
    path('addfriend/', AddFriend.as_view(), name = 'addfriend')
]