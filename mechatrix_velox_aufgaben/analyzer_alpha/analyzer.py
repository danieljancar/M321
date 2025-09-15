import grpc
from concurrent import futures
import time
import uuid
import requests
from pymongo import MongoClient
import api_pb2
import api_pb2_grpc

def trigger_measurement_and_store():
    client = MongoClient("mongodb://theship:theship1234@10.255.255.254:2021/theshipdb")
    db = client["theshipdb"]
    collection = db["vacuum-energy"]

    request_id = str(uuid.uuid4())

    trigger_url = "http://10.255.255.254:2037/trigger_measurement"
    data = {"request_id": request_id}
    response = requests.post(trigger_url, json=data)

    if response.status_code != 201:
        print(f"Fehler beim Triggern: {response.text}")
        client.close()
        return None

    measurement_url = f"http://10.255.255.254:2037/measurements/{request_id}"
    result = None

    while True:
        r = requests.get(measurement_url).json()
        if r["state"] == "measured":
            result = r.get("result")
            break
        time.sleep(2)

    if result:
        collection.delete_many({})
        collection.insert_one({"data": result})
        print(f"Messungsergebnis gespeichert: {result}")

    requests.delete(measurement_url)
    client.close()
    return result


class SensorService(api_pb2_grpc.SensorVoidEnergyServerServicer):
    def read_sensor_data(self, request, context):
        print("Analyzer fragt Sensordaten an...")
        result = trigger_measurement_and_store()
        if not result:
            result = ""
        return api_pb2.SensorData(hexdata=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    api_pb2_grpc.add_SensorVoidEnergyServerServicer_to_server(SensorService(), server)
    server.add_insecure_port("[::]:2102")
    server.start()
    print("SensorVoidEnergyServer läuft auf Port 2102")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
