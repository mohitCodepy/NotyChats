from django.db import models
from users.models import User

# Installed crum to get current user in the model

from crum import get_current_user 



#(_______________________________________________ Status for request _______________________________________________)


REQUEST_STATUS = (

    ('Not_Connected', 'Not_Connected'),
    ('Sender_Sent', 'Sender_Sent'),
    ('Pending', 'Pending'),
    ('Connected', 'Connected'),

)

#(_____________________________________________ NOKIA Connecting People _____________________________________________)


class ConnectingPeople(models.Model):
    connection_sender = models.ForeignKey(User, related_name='connection_sender', on_delete = models.CASCADE)
    connected_with = models.ForeignKey(User, related_name='connection_reciever', on_delete = models.CASCADE)
    request_status = models.CharField(max_length = 30, choices = REQUEST_STATUS, default= 'Not_Connected')
    connected_on = models.DateTimeField(auto_now_add = True)


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not user.pk:
            self.connection_sender = user
        super(ConnectingPeople, self).save(*args, **kwargs)
