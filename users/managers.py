from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy


class CustomUserManager(BaseUserManager) :

    def create_user(self, phone, full_name, password, **extra_fields):
        if not phone:
            raise ValueError(ugettext_lazy('The Phone must be set'))
        user = self.model(phone = phone, full_name = full_name , **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, full_name, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(ugettext_lazy('Superuser must have is_superuser=True.'))
        return self.create_user(phone , full_name, password, **extra_fields)