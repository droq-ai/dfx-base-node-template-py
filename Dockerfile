# Dockerfile template for Droq nodes
# This is an agnostic template - customize as needed for your node

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
# Uncomment and add system packages as needed:
# RUN apt-get update && apt-get install -y \
#     gcc \
#     g++ \
#     make \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
# Install dependencies directly (not as editable package)
RUN uv pip install --system nats-py aiohttp || \
    (uv pip compile pyproject.toml -o requirements.txt && \
     uv pip install --system -r requirements.txt)

# Copy source code
COPY src/ ./src/

# Create non-root user for security
RUN useradd -m -u 1000 nodeuser && chown -R nodeuser:nodeuser /app
USER nodeuser

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Optional: Health check
# Uncomment and customize as needed:
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import sys; sys.exit(0)"

# Run the node
# Update this command to match your entry point
CMD ["uv", "run", "python", "-m", "node.main"]

