FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock* ./

RUN uv pip install --system nats-py aiohttp || \
    (uv pip compile pyproject.toml -o requirements.txt && \
     uv pip install --system -r requirements.txt)

COPY src/ ./src/

RUN useradd -m -u 1000 nodeuser && chown -R nodeuser:nodeuser /app
USER nodeuser

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV NODE_PORT=8000

EXPOSE ${NODE_PORT}

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

CMD ["sh", "-c", "exec uv run python -m node.main --port=${NODE_PORT:-8000}"]

