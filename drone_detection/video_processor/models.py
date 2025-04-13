from django.db import models

class Video(models.Model):
    original_video = models.FileField(upload_to='uploads/')
    processed_video = models.FileField(upload_to='processed/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    focal_length = models.FloatField(help_text="Focal length in meters", null=True, blank=True)
    real_object_height = models.FloatField(help_text="Real height of the object in meters", null=True, blank=True)
    sensor_height = models.FloatField(help_text="Sensor height in meters", null=True, blank=True)

    def __str__(self):
        return f"Original Video: {self.original_video.name}\n Processed Video: {self.processed_video.name if self.processed_video else 'Not Processed Yet'}\n Uploaded At: {self.uploaded_at}"
