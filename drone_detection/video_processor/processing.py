import os
import subprocess
import sys
from django.conf import settings

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2
import tensorflow as tf
from .models import Video
from tf_model.ObjectDetectionModel import ObjectDetectionModel


def process_video(input_video_path, output_video_path, focal_length, real_height, sensor_height):

    #model_dir = os.path.join(settings.BASE_DIR, 'tf_model', 'model')
    model_dir = r'E:\University\test\DjangoProject\drone_detection\video_processor\tf_model\model'
    detection_model = ObjectDetectionModel(
        model_dir=model_dir,
        focal_length=focal_length,
        real_height=real_height,
        sensor_height=sensor_height
    )
    detection_model.process_video(input_video_path, output_path=output_video_path)

def save_video(input_video_path, output_video_path, fps=30):
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    print(f"Video saved to {output_video_path}")
