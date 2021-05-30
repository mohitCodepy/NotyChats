from django.db import models
from django.contrib.auth.models import  AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    picture = models.ImageField(upload_to = 'media', default= '/media/dummy_image.png' ,blank = True, null = True)
    phone = models.IntegerField(unique=True, blank= False )
    full_name = models.CharField(max_length=20, blank=False )
    username= models.CharField(unique = False, max_length=10, blank = True, null = True)
    USERNAME_FIELD ='phone'
    REQUIRED_FIELDS = ['full_name']
    objects = CustomUserManager()
    def __str__(self):
        return self.full_name



