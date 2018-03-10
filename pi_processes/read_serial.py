import serial
import json
import requests

port = '/dev/ttyACM0'
URL = ''

ser = serial.Serial(port)
with serial.Serial(port,9600,timeout = 1) as ser:
    data = json.loads(ser.readline())
    r = requests.post(URL, data)
    if data["potentiometer"]>100:
        ser.write("1")

