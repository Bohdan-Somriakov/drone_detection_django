# Generated by Django 4.2.19 on 2025-03-14 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_processor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='focal_length',
            field=models.FloatField(blank=True, help_text='Focal length in meters', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='real_object_height',
            field=models.FloatField(blank=True, help_text='Real height of the object in meters', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='sensor_height',
            field=models.FloatField(blank=True, help_text='Sensor height in meters', null=True),
        ),
    ]
