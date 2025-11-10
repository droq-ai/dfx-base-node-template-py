# Template Usage

Quick guide to build a Droq node from this template.

## Quick Start

1. **Fork/clone** this template
2. **Replace** `src/node/main.py` with your code
3. **Add dependencies** in `pyproject.toml` or `uv add <package>`
4. **Test locally**: `uv run python -m node.main` or `docker compose up`
5. **Build**: `docker build -t your-node:latest .`

## Structure

```
src/node/
  ├── main.py      # Your code goes here
  ├── nats.py      # NATS client helper
  ├── http.py      # HTTP client helper
  └── logger.py    # Optional logging setup
```

## Common Patterns

**Environment Variables:**
```python
import os
api_key = os.getenv("API_KEY")
```

**Graceful Shutdown:**
```python
from node.main import shutdown_event

while not shutdown_event.is_set():
    await do_work()
```

**Dependencies:**
```bash
uv add requests aiohttp
# or edit pyproject.toml
```

## Testing

```bash
uv run pytest
```

Tests use NATS from `compose.yml` automatically.

## Next Steps

1. Test locally
2. Build Docker image
3. Register metadata in `droq-node-registry` (separate repo)
