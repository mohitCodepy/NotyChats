from django.contrib import admin
from .models import ConnectingPeople, Message
# Register your models here.

@admin.register(ConnectingPeople)
class ConnectingPeopleAdmin(admin.ModelAdmin):
    list_display = ['id', 'connection_sender', 'connection_receiver', 'request_status', 'connected_on', 'group_name']

admin.site.register(Message)