# Generated by Django 3.1.6 on 2021-05-30 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210530_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, default='/media/dummy_image.png', null=True, upload_to='media'),
        ),
    ]
