# Generated by Django 3.1.6 on 2021-06-13 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210609_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='msg_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
