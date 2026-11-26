# Shared JSON Payload Schema

This document defines the JSON payload structure for communication between the Computer Vision modules and the Central FastAPI API.

## 1. Foot Traffic Module

```json
{
  "entries": 12,
  "exits": 4,
  "occupancy": 8
}
```

## 2. Checkout Queue Module

```json
{
  "queue_length": 5,
  "avg_wait_sec": 32.5,
  "alerts": []
}
```

## 3. Shelf Monitoring Module

```json
{
  "fill_rate_pct": 78.5,
  "empty_slots": [],
  "restock_alert": false
}
```

## 4. Privacy Module

The privacy module provides anonymized video frames through its `anonymize_frame(frame)` function. It does not currently have a separate metrics payload defined in the sprint specification.

## API Integration

The central FastAPI server receives module metrics through:

`POST /api/metrics/{module}`

Supported module names:
- `foot_traffic`
- `queue`
- `shelf`

Each module should send its metrics as a JSON request body.