from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=255)
    focal_length = models.FloatField(help_text="Focal length in mm")
    sensor_height = models.FloatField(help_text="Sensor height in meters")
    sensor_width = models.FloatField(help_text="Sensor width in meters")
    resolution = models.CharField(max_length=50, help_text="Resolution e.g. 1920x1080")
    brand = models.CharField(max_length=255, help_text="Camera brand")

    def __str__(self):
        return f"{self.brand} {self.name}"
