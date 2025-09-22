import time
from concurrent.futures import ThreadPoolExecutor
import boto3
import requests
from io import BytesIO
from botocore.exceptions import ClientError

antimatter_sensor_url = "http://10.255.255.254:2043/"
s3_host = "http://10.255.255.254:2016/"
bucket_name = "analyzer-gamma"
file_name = "data.hex"
access_key = "theship"
secret_key = "theship1234"

s3 = boto3.client('s3',
                  endpoint_url=s3_host,
                  access_key_id=access_key,
                  secret_access_key=secret_key)

def ensure_bucket_exists(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' existiert bereits.")
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            print(f"Bucket '{bucket_name}' existiert nicht. bucket wird erstellt")
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' erstellt.")
        else:
            raise e


def measure(direction):
    try:
        response = requests.post(url=antimatter_sensor_url + direction + "/measure", timeout=5)
        data = response.json()
        if "measurement" in data:
            return data["measurement"]
    except Exception as e:
        print(f"Error in direction {direction}: {e}")
    return None


def get_antimatter_sensor_data():
    with ThreadPoolExecutor(max_workers=3) as executor:
        responses = [executor.submit(measure, d) for d in ["x", "y", "z"]]

        for response in responses:
            result = response.result()
            if result:
                print("Measurement:", result)
                return result

    print("No measurement returned.")
    return None


def write_to_s3_storage(data):
    file_content = data.encode("utf-8")
    file_obj = BytesIO(file_content)
    s3.upload_fileobj(file_obj, bucket_name, file_name)
    print(f"Messdaten nach S3 hochgeladen: {file_name}")


def run():
    ensure_bucket_exists(bucket_name)
    while True:
        data = get_antimatter_sensor_data()
        if data is not None:
            write_to_s3_storage(data)
        time.sleep(2)
