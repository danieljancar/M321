import requests

def travel_to():
    url = "http://10.255.255.254:2009/set_target"
    cords = {"x": -500, "y": 500}
    payload = {"target": cords}
    return requests.post(url, json=payload)

def get_data_from_core_station():
    return requests.post("http://10.255.255.254:2027/receive").json()

def get_data_from_azura_station():
    return requests.get("http://10.255.255.254:2030/messages_for_other_stations").json()

def upload_data_to_azura_station():
    message = get_data_from_core_station()
    messages = message.get("received_messages")

    for msg_data in messages:
        msg = msg_data.get('data')
        payload = {
            "sending_station": "Core Station",
            "base64data": msg
        }
        response = requests.post("http://10.255.255.254:2030/put_message", json=payload)
        print(response.json())

def upload_data_to_core_station():
    message = get_data_from_azura_station()
    base64data = message.get("received_messages")[0].get('base64data')

    payload = {"source": "Azura Station", "message": base64data}
    response = requests.post("http://10.255.255.254:2027/send", json=payload)
    print(response.json())

while True:
    travel_to()
    upload_data_to_azura_station()
    upload_data_to_core_station()