# Droq Node Template

A Python template for building Droqflow nodes.

## Quick Start

```bash
git clone <repository-url>
cd droq-node-template-py
uv sync

# Replace src/node/main.py with your code
# Add dependencies: uv add your-package

# Test locally
PYTHONPATH=src uv run python -m node.main

# Run with Docker
docker compose up
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

**Required:**
- `NODE_NAME` - Node identifier
- `NODE_PORT` - Port inside container (default: 8000)
- `NATS_URL` - NATS server URL (default: nats://localhost:4222)
- `STREAM_NAME` - JetStream name (default: droq-stream)
- `LOG_LEVEL` - Logging level (default: INFO)



## Docker

```bash
# Build
docker build -t your-node:latest .

# Run
docker run -p 8080:8000 \
  -e NODE_NAME=my-node \
  -e NATS_URL=nats://localhost:4222 \
  your-node:latest
```

## Development

```bash
# Run tests
PYTHONPATH=src uv run pytest

# Format code
uv run black src/ tests/
uv run ruff check src/ tests/

# Add dependencies
uv add package-name
```



## Documentation

- [Usage Guide](docs/usage.md)
- [NATS Examples](docs/nats.md)

## License

Apache License 2.0