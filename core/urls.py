from django.urls import path, re_path
from .views import HomeView, AddFriend, ConnectFriend, BasePoint
urlpatterns=[
    path('',BasePoint.as_view()),
    path('home/',HomeView.as_view(), name = 'home'),
    path('home/<id>',HomeView.as_view(), name = 'home'),
    path('addfriend/', AddFriend.as_view(), name = 'addfriend'),
    path('connectfriend/', ConnectFriend.as_view(), name='connectfriend')
]