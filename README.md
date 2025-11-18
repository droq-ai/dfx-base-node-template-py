# Droq Node Template

Python template for building Droq nodes with Docker publishing.

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

**Variable Naming Convention:**
- `NODE_` - Node configuration
- `NATS_` - NATS configuration
- `LOG_` - Logging configuration
- `DB_` - Database configuration
- `HTTP_` - HTTP client configuration
- `SERVICE_` - Service-specific configuration
- `METRICS_` - Metrics and monitoring

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

## Docker Publishing

The template includes GitHub Actions for automatic Docker publishing:

- **Triggers**: Push to main, git tags, manual dispatch
- **Registries**: GitHub Container Registry (default) + private registries
- **Platforms**: linux/amd64, linux/arm64
- **Features**: Security scanning, SBOM generation

Configure private registry with secrets:
- `PRIVATE_REGISTRY_URL`
- `PRIVATE_REGISTRY_USERNAME`
- `PRIVATE_REGISTRY_PASSWORD`

## Documentation

- [Usage Guide](docs/usage.md)
- [Docker Publishing](docs/docker-publishing.md)
- [NATS Examples](docs/nats.md)

## License

Apache License 2.0