from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json

from greenhack_backend.models import *

import datetime

# Create your views here.
def add_sensor_data(request):
    data = json.loads(request.body.decode('utf-8'))
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
    results1 = json.loads(serializers.serialize('json',Temperature.objects.all()))
    results2 = json.loads(serializers.serialize('json',Pressure.objects.all()))
    results3 = json.loads(serializers.serialize('json',Humidity.objects.all()))
    res1 = []
    res2 = []
    res3 = []
    for r in results1:
        print(r)
        res1.append((r["fields"]))
    for r in results2:
        res2.append((r["fields"]))
    for r in results3:
        res3.append((r["fields"]))
    print(res1,res2,res3)
    res3_ = [x["reading"] for x in res3]
    res2_ = [x["reading"] for x in res2]
    res1_ = [x["reading"] for x in res1]

    return render(request, 'main.html', {"results1": res1,"results2":res2, "results3":res3,"r3":res3_,"r2":res2_,"r1":res1_})