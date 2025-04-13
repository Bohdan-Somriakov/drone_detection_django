from django.urls import path
from .views import camera_list

urlpatterns = [
    path('', camera_list, name='camera_list'),
]
