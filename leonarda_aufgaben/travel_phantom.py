import requests

def travel_to():
    url = "http://10.255.255.254:2009/set_target"
    cords = {"x": -60000, "y": 9000}
    payload = {"target": cords}
    return requests.post(url, json=payload)
