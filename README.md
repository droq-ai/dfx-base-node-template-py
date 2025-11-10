# Droq Node Template

A Python template for building Droq nodes. Works with any Python code - minimal updates needed.

## Quick Start

```bash
# 1. Clone and setup
git clone <repository-url>
cd droq-node-template-py
uv sync

# 2. Replace src/node/main.py with your code

# 3. Add dependencies
uv add your-package

# 4. Test locally
PYTHONPATH=src uv run python -m node.main
# or
docker compose up

# 5. Build
docker build -t your-node:latest .
```

## Documentation

- [Usage Guide](docs/usage.md) - How to use the template
- [NATS Examples](docs/nats.md) - NATS publishing and consuming examples

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

## Docker

```bash
# Build
docker build -t your-node:latest .

# Run
docker run --rm your-node:latest

# Development (with hot reload)
docker compose up
```

## Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Or set in `compose.yml` or pass to Docker:
- `NATS_URL` - NATS server URL (default: `nats://localhost:4222`)
- `STREAM_NAME` - JetStream name (default: `droq-stream`)
- `NODE_NAME` - Node identifier
- `LOG_LEVEL` - Logging level

## Next Steps

1. Test locally
2. Build Docker image
3. Register metadata in `droq-node-registry` (separate repo)

## License

Apache License 2.0
