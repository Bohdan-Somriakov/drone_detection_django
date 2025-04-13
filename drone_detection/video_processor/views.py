import os
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Video
from .processing import process_video, save_video

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the video with the new fields
            video = form.save()

            focal_length = form.cleaned_data.get('focal_length')
            real_height = form.cleaned_data.get('real_object_height')
            sensor_height = form.cleaned_data.get('sensor_height')

            # Process the video
            input_video_path = video.original_video.path
            output_video_path = os.path.join(settings.MEDIA_ROOT, 'processed', f"processed_{video.id}.mp4")
            output_original_video_path = os.path.join(settings.MEDIA_ROOT, 'original', f"original_{video.id}.mp4")

            save_video(input_video_path, output_original_video_path)  # Save the original video
            process_video(input_video_path, output_video_path, focal_length, real_height, sensor_height)  # Process the video

            # Update the processed video path in the database
            video.processed_video = os.path.join('processed', f"processed_{video.id}.mp4").replace(os.sep, '/')
            video.save()

            return redirect('video_detail', video_id=video.id)
    else:
        form = VideoUploadForm()

    return render(request, 'upload_video.html', {'form': form})


def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)

    # Check if the video files exist
    original_video_exists = os.path.exists(video.original_video.path) if video.original_video else False
    processed_video_exists = os.path.exists(video.processed_video.path) if video.processed_video else False

    # Pass these values to the template
    return render(request, 'video_detail.html', {
        'video': video,
        'original_video_exists': original_video_exists,
        'processed_video_exists': processed_video_exists
    })

