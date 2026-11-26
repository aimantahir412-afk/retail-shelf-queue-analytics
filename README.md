# Retail Shelf & Queue Analytics

A privacy-first retail analytics system that brings together computer vision modules for foot-traffic counting, checkout queue monitoring, and shelf-stock analysis through a central FastAPI service.

## My Contribution

I am responsible for developing the Central Inference API, which receives metrics from the computer vision modules and provides a foundation for real-time dashboard integration.

## Current Features

- FastAPI application
- Health-check endpoint
- REST API for receiving module metrics
- In-memory storage for the latest metrics
- Shared JSON payload schema
- Interactive API documentation through Swagger UI

## Project Structure

```text
retail-shelf-queue-analytics/
│
├── server.py
├── requirements.txt
├── PAYLOAD_SCHEMA.md
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/aimantahir412-afk/retail-shelf-queue-analytics.git
cd retail-shelf-queue-analytics
```

Create and activate a virtual environment:

```bash
py -3.12 -m venv cv_env
```

Install dependencies:

```bash
cv_env\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the API

```bash
cv_env\Scripts\python.exe -m uvicorn server:app --reload
```

Open the API documentation:

`http://127.0.0.1:8000/docs`

Health-check endpoint:

`http://127.0.0.1:8000/health`

## Metrics API

The API accepts metrics through:

`POST /api/metrics/{module}`

Supported modules:

- `foot_traffic`
- `queue`
- `shelf`

Refer to [PAYLOAD_SCHEMA.md](PAYLOAD_SCHEMA.md) for the JSON payload structures.

## Development Status

The initial FastAPI service, health-check endpoint, metrics ingestion endpoint, and shared payload schema have been implemented. WebSocket broadcasting, dashboard development, and database integration are planned for subsequent stages of the sprint.

## Sample Media

The `samples/` directory contains sample retail shelf imagery for local testing and demonstration.

| File | Description | Source |
|---|---|---|
| `shelf_sample.jpg` | Supermarket shelf image | [Public Domain Pictures](https://www.publicdomainpictures.net/en/view-image.php?image=304765&picture=full-supermarket-shelves) |

The image is provided for sample testing. It is not a substitute for a representative evaluation dataset.


## FPS Benchmark

A basic OpenCV preprocessing benchmark was performed using the sample shelf image.

| Metric | Result |
|---|---:|
| Frames processed | 300 |
| Total processing time | 0.81 seconds |
| Processing speed | 372.42 FPS |

**Note:** This benchmark measures image resizing and colour conversion only. It does not represent YOLO inference or object-detection performance.

### Benchmark Screenshot

![OpenCV FPS Benchmark](screenshots/fps_benchmark.png)
