
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Retail Shelf & Queue Analytics API",
    description="Central API for retail computer vision analytics",
    version="1.0.0"
)

# Temporary in-memory storage
metrics_store = {}


@app.get("/")
def home():
    return {
        "message": "Retail Analytics API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Retail Analytics API"
    }


@app.post("/api/metrics/{module}")
def receive_metrics(module: str, metrics: dict):

    allowed_modules = ["foot_traffic", "queue", "shelf"]

    if module not in allowed_modules:
        raise HTTPException(
            status_code=400,
            detail="Invalid module name"
        )

    metrics_store[module] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics
    }

    return {
        "message": f"{module} metrics received successfully",
        "data": metrics_store[module]
    }
