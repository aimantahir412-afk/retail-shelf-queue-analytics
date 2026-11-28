import asyncio
import base64
import json
import websockets


async def test_video_frame():

    uri = "ws://127.0.0.1:8000/ws/live"

    # Connect receiver and sender
    async with websockets.connect(uri) as receiver:
        async with websockets.connect(uri) as sender:

            print("Both WebSocket clients connected!")

            # Read initial messages from both clients
            await receiver.recv()
            await sender.recv()

            # Create a small sample image as base64 data
            sample_image = base64.b64encode(
                b"Sample anonymized frame for testing"
            ).decode("utf-8")

            # Send the video-frame message
            await sender.send(json.dumps({
                "type": "video_frame",
                "module": "test_camera",
                "frame": sample_image
            }))

            print("Video frame sent successfully!")

            # Receive broadcast on the other connection
            response = await receiver.recv()

            received_data = json.loads(response)

            print("\nReceived video-frame message:")
            print(json.dumps(received_data, indent=4))

            # Verify the received message
            assert received_data["type"] == "video_frame"
            assert received_data["frame"] == sample_image

            print("\nVideo-frame broadcasting test passed!")


asyncio.run(test_video_frame())