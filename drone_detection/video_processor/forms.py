from django import forms
from .models import Video

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['original_video', 'focal_length', 'real_object_height', 'sensor_height']
