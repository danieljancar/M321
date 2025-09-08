import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

last_measure = ""

@app.route("/data", methods=["GET"])
def laser_ampflifer():
    global last_measure
    print(last_measure)
    return last_measure

def update_measure_loop():
    global last_measure
    while True:
        try:
            response = requests.post("http://10.255.255.254:2042/measure", timeout=10)
            print("messdaten empfangen:", response.text)
            last_measure = response.json().get("result")
            print("last_measure:", last_measure)
        except Exception as e:
            print("fehler:", e)
        time.sleep(5)

def start_flask():
    app.run(host='0.0.0.0', port=2104, use_reloader=False)


def run():
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    update_measure_loop()


if __name__ == '__main__':
    run()