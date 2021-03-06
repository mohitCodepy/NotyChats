# Generated by Django 3.1.6 on 2021-06-05 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210530_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='msg_status',
            field=models.CharField(choices=[('Sent', 'Sent'), ('Pending', 'Pending'), ('Read', 'Read')], default='Sent', max_length=10),
        ),
        migrations.AlterField(
            model_name='message',
            name='multimedia',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
