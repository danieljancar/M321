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
        
        # Get the value and check what type it is
        raw_value = json.get("value")
        print(f"Raw value: {raw_value}")
        print(f"Value type: {type(raw_value)}")
        print(f"Value length: {len(str(raw_value)) if raw_value is not None else 'None'}")
        
        # Check if it looks like hex data
        if isinstance(raw_value, str):
            print(f"Is hex-like: {all(c in '0123456789abcdefABCDEF' for c in raw_value)}")
        
        # Convert to string
        str_value = str(raw_value)
        
        # If the value is not already hex, try to convert it to hex
        if raw_value is not None and not all(c in '0123456789abcdefABCDEF' for c in str_value):
            try:
                # Try to convert to hex if it's a number
                if isinstance(raw_value, (int, float)):
                    hex_value = hex(int(raw_value))[2:]  # Remove '0x' prefix
                    print(f"Converted {raw_value} to hex: {hex_value}")
                    json["value"] = hex_value
                else:
                    # If it's a string, encode it to hex
                    hex_value = str_value.encode('utf-8').hex()
                    print(f"Encoded '{str_value}' to hex: {hex_value}")
                    json["value"] = hex_value
            except:
                # If conversion fails, just use the string
                json["value"] = str_value
        else:
            json["value"] = str_value
            
        return {"data": json.get("value")}
    except Exception as e:
        print(f"Error in get_data: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # massenstabilisator bruucht de atomic field sensor bzw. beidi münd laufe
    energy.set_limit_normal()
    app.run(host='0.0.0.0', port=2101)
