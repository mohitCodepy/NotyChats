# Generated by Django 3.1.6 on 2021-04-19 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectingPeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_status', models.CharField(choices=[('Not_Connected', 'Not_Connected'), ('Sender_Sent', 'Sender_Sent'), ('Pending', 'Pending'), ('Connected', 'Connected')], default='Not_Connected', max_length=30)),
                ('connected_on', models.DateTimeField(auto_now_add=True)),
                ('connected_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection_reciever', to=settings.AUTH_USER_MODEL)),
                ('connection_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connection_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
