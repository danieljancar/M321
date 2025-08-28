import requests

url = "http://10.255.255.254:2012/hold"

def get_free_hold():
    return get_cargo_hold().json()["hold"]["hold_free"]

def get_cargo_hold():
    return requests.get(url)
