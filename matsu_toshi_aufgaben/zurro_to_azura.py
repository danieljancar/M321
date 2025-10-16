import requests

def travel_to():
    url = "http://10.255.255.254:2009/set_target"
    cords = {"x": -6792, "y": 6032}
    payload = {"target": cords}
    return requests.post(url, json=payload)

def get_data_from_zurro_station():
      return requests.post("http://10.255.255.254:2027/receive").json()

def get_data_from_azura_station():
    return requests.get("http://10.255.255.254:2028/receive").json()

def upload_data_to_azura_station():
    message = get_data_from_zurro_station()
    messages = message.get("received_messages")

    for msg_data in messages:
        msg = msg_data.get('data')
        payload = {
            "sending_station": "Zurro Station",
            "base64data": msg
        }
        response = requests.post("http://10.255.255.254:2028/send", json=payload)
