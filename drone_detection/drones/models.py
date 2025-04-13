from django.db import models

class MilitaryDrone(models.Model):
    name = models.CharField(max_length=100)
    width = models.FloatField(help_text="Width of the drone")
    height = models.FloatField(help_text="Height of the drone")
    speed = models.FloatField(help_text="Speed of the drone")
    description = models.TextField(blank= True, null = True)
    image_url = models.URLField(help_text="URL of the drone image", blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
# Create your models here.
