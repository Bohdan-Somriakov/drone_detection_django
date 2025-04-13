from django.urls import path
from . import views

urlpatterns = [
    path('',views.drone_list, name = 'drone_list')
]