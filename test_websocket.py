import asyncio
import json
import websockets


async def test_websocket():

    uri = "ws://127.0.0.1:8000/ws/live"

    async with websockets.connect(uri) as websocket:

        print("Connected to WebSocket server!")

        while True:
            message = await websocket.recv()

            print("\nReceived live update:")
            print(json.dumps(json.loads(message), indent=4))


asyncio.run(test_websocket())