
import base64
from datetime import datetime, timezone

from fastapi import (
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect
)


app = FastAPI(
    title="Retail Shelf & Queue Analytics API",
    description="Central API for retail computer vision analytics",
    version="1.0.0"
)


# Temporary in-memory storage
metrics_store = {}


# WebSocket Connection Manager
class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []

        for connection in self.active_connections.copy():
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


# Home Route
@app.get("/")
def home():
    return {
        "message": "Retail Analytics API is running!"
    }


# Health Check Route
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Retail Analytics API"
    }


# Receive and Broadcast Metrics
@app.post("/api/metrics/{module}")
async def receive_metrics(module: str, metrics: dict):

    allowed_modules = ["foot_traffic", "queue", "shelf"]

    if module not in allowed_modules:
        raise HTTPException(
            status_code=400,
            detail="Invalid module name"
        )

    timestamp = datetime.now(timezone.utc).isoformat()

    metrics_store[module] = {
        "timestamp": timestamp,
        "metrics": metrics
    }

    # Broadcast live telemetry
    await manager.broadcast({
        "type": "telemetry",
        "module": module,
        "timestamp": timestamp,
        "data": metrics
    })

    return {
        "message": f"{module} metrics received successfully",
        "data": metrics_store[module]
    }


# Live WebSocket Endpoint
@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        # Send existing metrics to newly connected clients
        await websocket.send_json({
            "type": "initial_data",
            "data": metrics_store
        })

        while True:

            # Receive JSON messages from connected clients
            message = await websocket.receive_json()

            if message.get("type") == "video_frame":

                frame = message.get("frame")
                module = message.get("module")

                if not isinstance(frame, str) or not frame:
                    await websocket.send_json({
                        "type": "error",
                        "message": "A base64 video frame is required"
                    })
                    continue

                # Validate base64 data
                try:
                    base64.b64decode(frame, validate=True)
                except (ValueError, Exception):
                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid base64 frame"
                    })
                    continue

                # Broadcast video frame to connected clients
                await manager.broadcast({
                    "type": "video_frame",
                    "module": module,
                    "encoding": "base64",
                    "frame": frame
                })

            else:
                await websocket.send_json({
                    "type": "error",
                    "message": "Unsupported message type"
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
