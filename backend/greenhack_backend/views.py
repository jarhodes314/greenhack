from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from greenhack_backend.models import *

import datetime

# Create your views here.
@csrf_exempt
def send_data(request):
    p = request.POST["potentiometer"]
    t = request.POST["temperature"]
    h = request.POST["humidity"]
    date = datetime.datetime.now()

    print(date)
    temp = Temperature(datetime = timezone.now(), reading = t)
    temp.save()

    hum = Humidity(datetime = timezone.now(), reading = h)
    hum.save()

    pot = Pressure(datetime = timezone.now(), reading = p)
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
        res1.append((r["fields"]))
    for r in results2:
        res2.append((r["fields"]))
    for r in results3:
        res3.append((r["fields"]))
    res3_ = [x["reading"] for x in res3]
    res2_ = [x["reading"] for x in res2]
    res1_ = [x["reading"] for x in res1]

    date3_ = [x["datetime"] for x in res3]
    date2_ = [x["datetime"] for x in res2]
    date1_ = [x["datetime"] for x in res1]

    return render(request, 'main.html', {"results1": res1,"results2":res2, "results3":res3,"r3":res3_,"r2":res2_,"r1":res1_,"d1":date1_,"d2":date2_,"d3":date3_})