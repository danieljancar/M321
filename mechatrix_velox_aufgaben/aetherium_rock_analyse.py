import energy
import navigation as nav
import requests
import concurrent.futures
import boto3
from botocore.client import Config

# --- S3 Konfiguration ---
S3_HOST = "http://10.255.255.254:2016"
S3_BUCKET = "analyzer-gamma"
S3_KEY = "data.hex"
S3_ACCESS_KEY = "theship"
S3_SECRET_KEY = "theship1234"

# --- Antimateriesensor Endpunkte ---
SENSOR_HOST = "http://10.255.255.254:2043"
DIRECTIONS = ["x", "y", "z"]

def measure(direction: str):
    url = f"{SENSOR_HOST}/{direction}/measure"
    r = requests.post(url, timeout=10)
    r.raise_for_status()
    return r.json()

def run_measurements():
    measurement = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(measure, d): d for d in DIRECTIONS}
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            if "measurement" in data:
                measurement = data["measurement"]
    if not measurement:
        raise RuntimeError("Keine Messung erhalten!")
    return measurement

def upload_to_s3(data: str):
    s3 = boto3.client(
        "s3",
        endpoint_url=S3_HOST,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"
    )
    s3.put_object(Bucket=S3_BUCKET, Key=S3_KEY, Body=data.encode("utf-8"))
    print(f"Messdaten erfolgreich in s3://{S3_BUCKET}/{S3_KEY} gespeichert.")

if __name__ == "__main__":
    energy.set_limit_normal()
    nav.travel_position_until_recive(-95375, -90773)

    energy.set_limits({
        "sensor_antimatter": 1,
        "analyzer_gamma": 1,
        "analyzer_alpha": 0,
        "analyzer_beta": 0,
        "nuclear_reactor": 0,
        "scanner": 0,
        "laser": 0,
        "cargo_bot": 0,
        "thruster_back": 0,
        "thruster_front": 0,
        "thruster_bottom_left": 0,
        "thruster_front_right": 0,
        "thruster_bottom_right": 0,
        "thruster_front_left": 0,
    })

    print("Starte Antimaterie-Messung ...")
    measurement = run_measurements()
    print("Messung erhalten:", measurement[:50], "...")
    upload_to_s3(measurement)

