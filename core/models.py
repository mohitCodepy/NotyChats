from django.db import connection, models
from users.models import User
from django.utils import timezone
import datetime
# Installed crum to get current user in the model

from crum import get_current_user 



#(_______________________________________________ Status for request _______________________________________________)


REQUEST_STATUS = (

    ('Pending', 'Pending'),
    ('Connected', 'Connected'),
    ('Blocked', 'Blocked'),

)

#(_____________________________________________ NOKIA Connecting People _____________________________________________)


class ConnectingPeople(models.Model):
    connection_sender = models.ForeignKey(User, related_name='connection_sender', on_delete = models.CASCADE)
    connection_receiver = models.ForeignKey(User, related_name='connection_reciever', on_delete = models.CASCADE)
    request_status = models.CharField(max_length = 30, choices = REQUEST_STATUS, default= 'Not_Connected')
    connected_on = models.DateTimeField(auto_now_add = True)
    group_name = models.CharField(max_length=30, blank=True)


    def save(self, *args, **kwargs):
        user = get_current_user()
        print(user, user.pk)
        if user and not user.pk:
            user = None
        if not user.pk:
            self.connection_sender = user

# (___________________________________Creating Unique group Name_____________________________________________________)

        if int(self.connection_sender_id) < int(self.connection_receiver_id):
            self.group_name = f'{self.connection_sender_id}_{self.connection_receiver_id}'
        else:
            self.group_name = f'{self.connection_receiver_id}_{self.connection_sender_id}'
        print(f'{self.connection_sender_id}_{self.connection_receiver_id}') 

        super(ConnectingPeople, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.connection_sender} binded with {self.connection_receiver}'



MSG_STATUS = (

    ('Sent', 'Sent'),
    ('Pending', 'Pending'),
    ('Read', 'Read'),

)


class Message(models.Model):
    group_id = models.ForeignKey(ConnectingPeople, related_name='user_messages', on_delete = models.CASCADE)
    sender = models.ForeignKey(User, related_name = 'msg_sender', on_delete = models.CASCADE)
    message = models.CharField(max_length = 500)
    msg_date = models.DateTimeField(auto_now_add= True) 
    multimedia = models.FileField(blank = True, null= True)
    msg_status = models.CharField(max_length = 10, choices = MSG_STATUS, default='Sent')
    
    def __str__(self):
        return f'{self.message} by {self.sender}'