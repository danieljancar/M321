import asyncio
import websockets
import json
import base64

async def elyse_receive():
    url = "ws://10.255.255.254:2026/api"

    async with websockets.connect(url) as websocket:
        message = await websocket.recv()

        data = json.loads(message)
        print(f"response: {data}")

        if 'msg' in data:
            msg_bytes = bytes(data['msg'])
            msg_b64 = base64.b64encode(msg_bytes).decode('utf-8')
            print(f"Base64-encoded msg: {msg_b64}")
            
        await websocket.close()

asyncio.run(elyse_receive())
