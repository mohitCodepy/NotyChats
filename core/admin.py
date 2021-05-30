from django.contrib import admin
from .models import ConnectingPeople
# Register your models here.

@admin.register(ConnectingPeople)
class ConnectingPeopleAdmin(admin.ModelAdmin):
    list_display = ['id', 'connection_sender', 'connection_receiver', 'request_status', 'connected_on', 'group_name']