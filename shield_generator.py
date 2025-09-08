import uuid
import requests
import time
import energy
from pymongo import MongoClient

def trigger_measurement_and_store():
    client = MongoClient("mongodb://theship:theship1234@10.255.255.254:2021/admin")
    db = client["theshipdb"]
    collection = db["vacuum-energy"]

    random = str(uuid.uuid4())

    trigger_url = "http://10.255.255.254:2037/trigger_measurement"
    data = {"request_id": random}
    response = requests.post(trigger_url, json=data)

    if response.status_code == 201:
        print("Messung erfolgreich")
    else:
        print(f"Fehler beim Anfordern der Messung: {response.text}")
        return

    measurement_url = "http://10.255.255.254:2037/measurements/" + random
    while True:
        response = requests.get(measurement_url)
        result = response.json()

        print(result)

        if result["state"] == "measured":
            print("Messung fertig")
            break
        else:
            print("messung läuft...")
            time.sleep(2)


    result_to_return = ""
    if "result" in result:
        collection.delete_many({})
        result_to_return = result["result"]
        collection.insert_one({
            "data": result_to_return
        })
        print("messungsergebnis in db gespeichert")
    else:
        print("kein messungsergebnis vorhanden")

    delete_response = requests.delete(measurement_url)
    print(delete_response)
    if delete_response.status_code == 200:
        print("messung erfolgreich gelöscht")
    else:
        print("fehler beim löschen der messung")

    client.close()
    return result_to_return


if __name__ == "__main__":
    energy.set_limits({
        "sensor_void_energy": 1,
        "shield_generator": 1,
        "laser": 0,
        "scanner": 0,
        "cargo_bot": 0
    })

    while True:
        trigger_measurement_and_store()