# Droq Node Template

A Python template for building Droqflow nodes.

## Quick Start

```bash
git clone git@github.com:droq-ai/dfx-base-node-template-py.git
cd dfx-base-node-template-py
uv sync

# Replace src/node/main.py with your code
# Add dependencies: uv add your-package

# Configure node.json with your node information
# Configure environment variables

# Test locally
PYTHONPATH=src uv run python -m node.main

# Run with Docker
docker compose up
```

## Next Steps

1. Complete your node development
2. Configure [node.json](docs/node-configuration.md) with your node metadata
3. Register your node in [droq-node-registry](https://github.com/droq-ai/droq-node-registry) to appear on [directory.droq.ai](https://directory.droq.ai)


### Node Configuration

Configure `node.json` with your node metadata. All fields are required:

- **Identity**: `version`, `node_id`, `name`, `description`
- **Runtime**: `api_url`, `ip_address`, `docker_image`, `status`, `deployment_location`
- **Metadata**: `author`, `created_at`, `source_code_location`
- **Components**: Define your node's functional components

See [Node Configuration Guide](docs/node-configuration.md) for complete details.

### Environment Variables

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

- [Node Configuration Guide](docs/node-configuration.md) - Complete node.json setup
- [Node Registration Guide](docs/node-registration.md) - Register your node in the registry
- [Usage Guide](docs/usage.md)
- [NATS Examples](docs/nats.md)

## License

Apache License 2.0