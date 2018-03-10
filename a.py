import requests

data ={"potentiometer" : 1, "temperature" : 1, "humidity" : 1}

r = requests.post('http://127.0.0.1:8000/send_data', data=data)
