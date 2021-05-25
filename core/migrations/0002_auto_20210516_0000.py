# Generated by Django 3.1.6 on 2021-05-15 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectingpeople',
            name='group_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='connectingpeople',
            name='request_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Connected', 'Connected'), ('Blocked', 'Blocked')], default='Not_Connected', max_length=30),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=500)),
                ('msg_date', models.DateTimeField(auto_now_add=True)),
                ('multimedia', models.FileField(blank=True, upload_to='')),
                ('msg_status', models.CharField(choices=[('Sent', 'Sent'), ('Pending', 'Pending'), ('Read', 'Read')], max_length=10)),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_messages', to='core.connectingpeople')),
            ],
        ),
    ]
