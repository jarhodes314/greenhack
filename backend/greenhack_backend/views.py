from django.shortcuts import render
from django.http import HttpResponse
from greenhack_backend.models import *

import datetime

# Create your views here.
def add_sensor_data(request):
    data = request.body
    p = data["potentiometer"]
    t = data["temperature"]
    h = data["humidity"]
    date = datetime.datetime.now()

    temp = Temperature()
    temp.date = date
    temp.reading = t
    temp.save()

    hum = Humidity()
    hum.date = date
    hum.reading = h
    hum.save()

    pot = Pressure()
    pot.date = date
    pot.reading = p
    pot.save()
    
    return HttpResponse(status=200)

def main(request):
    results1 = Temperature.objects.all()
    results2 = Pressure.objects.all()
    results3 = Humidity.objects.all()

    return render(request, 'main.html', {"results1": results1,"results2":results2, "results3":results3})