from django.shortcuts import render
from django.http import HttpResponse

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

def main():
    pass