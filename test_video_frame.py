
import asyncio
import base64
import json
import cv2
import numpy as np
import websockets


async def test_video_frame():

    uri = "ws://127.0.0.1:8000/ws/live"

    # Load the actual sample shelf image
    image = cv2.imread("samples/shelf_sample.jpg")

    if image is None:
        raise FileNotFoundError("Sample image could not be loaded")

    # Encode image into JPEG format
    success, buffer = cv2.imencode(".jpg", image)

    if not success:
        raise RuntimeError("JPEG encoding failed")

    # Convert JPEG bytes into Base64
    encoded_frame = base64.b64encode(
        buffer.tobytes()
    ).decode("utf-8")

    # Allow WebSocket messages up to 5 MB
    max_message_size = 5 * 1024 * 1024

    async with websockets.connect(
        uri,
        max_size=max_message_size
    ) as receiver:

        async with websockets.connect(
            uri,
            max_size=max_message_size
        ) as sender:

            print("Both WebSocket clients connected!")

            # Receive initial messages
            await receiver.recv()
            await sender.recv()

            # Send actual JPEG frame
            await sender.send(json.dumps({
                "type": "video_frame",
                "module": "shelf",
                "frame": encoded_frame
            }))

            print("Actual JPEG frame sent!")

            # Receive broadcast
            response = await receiver.recv()
            received_data = json.loads(response)

            print("\nReceived frame information:")
            print("Message type:", received_data["type"])
            print("Module:", received_data["module"])
            print("Encoding:", received_data["encoding"])

            # Decode received Base64 data
            decoded_frame = base64.b64decode(
                received_data["frame"]
            )

            # Decode JPEG bytes into an OpenCV image
            received_image = cv2.imdecode(
                np.frombuffer(decoded_frame, dtype=np.uint8),
                cv2.IMREAD_COLOR
            )

            if received_image is None:
                raise RuntimeError(
                    "Received image could not be decoded"
                )

            # Save the received image
            saved = cv2.imwrite(
                "received_shelf_frame.jpg",
                received_image
            )

            if not saved:
                raise RuntimeError("Could not save received image")

            print("Received image dimensions:", received_image.shape)
            print("Saved image: received_shelf_frame.jpg")
            print("Real JPEG frame broadcasting test passed!")


asyncio.run(test_video_frame())
