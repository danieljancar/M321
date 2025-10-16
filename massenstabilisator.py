import requests
from flask import Flask
import energy

app = Flask(__name__)

@app.route(rule="/", methods=["GET"])
def get_data():
    try:
        response = requests.get("http://10.255.255.254:2038/data")
        json = response.json()
        print(json)
        # make value str
        json["value"] = str(json.get("value"))
        return {"data": json.get("value")}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # massenstabilisator bruucht de atomic field sensor bzw. beidi münd laufe
    energy.set_limit_normal()
    app.run(host='0.0.0.0', port=2101)
