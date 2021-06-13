from django.urls import path, re_path
from .views import HomeView, AddFriend, ConnectFriend, BasePoint, EditProfileView
urlpatterns=[
    path('',BasePoint.as_view()),
    path('home/',HomeView.as_view(), name = 'home'),
    path('home/<id>',HomeView.as_view(), name = 'home'),
    path('addfriend/', AddFriend.as_view(), name = 'addfriend'),
    path('edit_profile/', EditProfileView.as_view(), name = 'edit_profile'),
    path('edit_profile/<int:user_id>', EditProfileView.as_view(), name = 'edit_profile'),
    path('connectfriend/', ConnectFriend.as_view(), name='connectfriend')
]