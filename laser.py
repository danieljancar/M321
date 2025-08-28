import requests
import time

def activate():
    response = requests.post("http://10.255.255.254:2018/activate")
    print(f"activate laser: {response.json()}")

def deactive():
    response = requests.post("http://10.255.255.254:2018/deactivate")
    print(f"deactivate laser: {response.json()}")

def set_angle(angle):
    url = "http://10.255.255.254:2018/angle"
    data = {"angle": angle}

    response = requests.put(url, json=data)
    print(f"set angle: {response.json()}")

def get_state():
    response = requests.get("http://10.255.255.254:2018/state")
    print(f"state: {response.json()}")

activate()
time.sleep(1)
deactive()