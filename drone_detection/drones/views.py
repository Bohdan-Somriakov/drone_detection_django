from django.shortcuts import render
from .models import MilitaryDrone
def drone_list(request):
    drones = MilitaryDrone.objects.all()
    return render(request, 'drone_list.html', {'drones' : drones})
# Create your views here.
