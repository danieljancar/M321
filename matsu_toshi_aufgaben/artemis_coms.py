import xmlrpc.client
import base64

url = 'http://10.255.255.254:2024/RPC2'
client = xmlrpc.client.ServerProxy(url)

try: 
    data = client.receive()
    for destination, message in data:
        base64_string = base64.b64encode(message.data).decode('utf-8')
        print(f"Destination: {destination}, Message: {base64_string}")
except Exception as e:
    print(f"Error while receiving message: {e}")
