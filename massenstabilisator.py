import requests
from flask import Flask
import energy

app = Flask(__name__)

@app.route(rule="/", methods=["GET"])
def get_data():
    try:
        response = requests.get("http://10.255.255.254:2038/data")
        json = response.json()
        print("Raw JSON response:", json)
        
        # Get the value from 'result' field, not 'value'
        raw_value = json.get("result")  # Changed from "value" to "result"
        print(f"Raw value: {raw_value}")
        print(f"Value type: {type(raw_value)}")
        print(f"Value length: {len(str(raw_value)) if raw_value is not None else 'None'}")
        
        # Check if it looks like hex data
        if isinstance(raw_value, str):
            print(f"Is hex-like: {all(c in '0123456789abcdefABCDEF' for c in raw_value)}")
        
        # The result field already contains hex data, so just return it as is
        if raw_value is not None:
            # Clean up any whitespace or newlines from the hex string
            clean_hex = str(raw_value).replace('\n', '').replace(' ', '').strip()
            print(f"Cleaned hex value: {clean_hex}")
            return {"data": clean_hex}
        else:
            return {"data": ""}
            
    except Exception as e:
        print(f"Error in get_data: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # massenstabilisator bruucht de atomic field sensor bzw. beidi münd laufe
    energy.set_limit_normal()
    app.run(host='0.0.0.0', port=2101)
