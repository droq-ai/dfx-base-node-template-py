# NATS Examples

Quick examples for using NATS JetStream in your node.

## Setup

```python
from node.nats import NATSClient

nats_client = NATSClient()  # Uses NATS_URL and STREAM_NAME env vars
await nats_client.connect()
```

## Publish

```python
await nats_client.publish("output", {"message": "Hello", "data": {...}})
```

## Subscribe

```python
async def handle_message(data: dict, headers: dict):
    print(f"Received: {data}")

# Simple subscribe
await nats_client.subscribe("input", handle_message)

# With queue group (load balancing)
await nats_client.subscribe("input", handle_message, queue="my-queue")
```

## HTTP to NATS Pattern

```python
from node.http import HTTPClient
from node.nats import NATSClient

nats_client = NATSClient()
await nats_client.connect()

async with HTTPClient(base_url="https://api.example.com") as http:
    data = await http.get("/endpoint")
    await nats_client.publish("api-data", data)
```

## Node Types

**Source** (publish only):
```python
while not shutdown_event.is_set():
    data = await fetch_data()
    await nats_client.publish("output", data)
    await asyncio.sleep(60)
```

**Compute** (consume + publish):
```python
async def process(data: dict, headers: dict):
    result = compute(data)
    await nats_client.publish("output", result)

await nats_client.subscribe("input", process, queue="compute-queue")
```

**Sink** (consume only):
```python
async def store(data: dict, headers: dict):
    await save_to_database(data)

await nats_client.subscribe("input", store, queue="sink-queue")
```

## Testing

Start NATS: `docker compose -f compose.yml up -d nats`

Tests automatically use the NATS server from compose.
