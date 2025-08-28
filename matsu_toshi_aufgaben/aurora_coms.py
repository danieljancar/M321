import navigation
import socket
import struct
import base64
import requests

navigation.travel_position_until_recive(-11000, -11000)

def send_msg(ip, port, src, message):
    src_bytes = src.encode('utf-8')
    msg_bytes = message.encode('utf-8')

    total_length = 1 + len(src_bytes) + len(msg_bytes)

    payload = struct.pack('>H', total_length)
    payload += struct.pack('B', len(src_bytes))
    payload += src_bytes
    payload += msg_bytes

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(payload)

        data = s.recv(4096)
        return data

response = send_msg("10.255.255.254", 2031, "src", "test")

total_len = struct.unpack('>H', response[0:2])[0]
src_len = response[2]
src = response[3:3+src_len].decode('utf-8')
msg = base64.b64encode(bytes(response[3+src_len:])).decode('utf-8')
print(msg)


navigation.travel_station_wait_until_recive("Azura Station")

payload = {
    "sending_station": "Aurora Station",
    "base64data": msg
}
print(payload)
response = requests.post('http://10.255.255.254:2030/put_message', json=payload)
print(response.json())