# Generated by Django 2.2 on 2021-04-11 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foody_app', '0002_auto_20210409_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
