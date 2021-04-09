from django.contrib import admin
from .models import User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'full_name']
