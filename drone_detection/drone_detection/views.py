from django.shortcuts import render
from video_processor.models import Video
from drones.models import MilitaryDrone
from cameras.models import Camera


def home(request):
    # Fetch recent videos
    recent_videos = Video.objects.filter(processed_video__isnull=False).order_by('-uploaded_at')[
                    :4]

    drones = MilitaryDrone.objects.all()[:4]

    cameras = Camera.objects.all()[:4]

    return render(request, 'home.html', {'recent_videos': recent_videos, 'drones': drones, 'cameras': cameras})
