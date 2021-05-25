from django.urls import path, re_path
from .views import HomeView, AddFriend, ConnectFriend
urlpatterns=[
    path('home/',HomeView.as_view(), name = 'home'),
    path('home/<int:id>',HomeView.as_view(), name = 'home'),
    path('addfriend/', AddFriend.as_view(), name = 'addfriend'),
    path('connectfriend/', ConnectFriend.as_view(), name='connectfriend')
]