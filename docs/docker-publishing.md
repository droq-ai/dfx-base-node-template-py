# Docker Publishing

Automated Docker publishing via GitHub Actions.

## Setup

**Triggers:**
- Push to main branch → `latest` tag
- Git tags (v1.0.0) → version tags
- Pull requests → build only
- Manual dispatch → optional

**Registry Options:**
- **GitHub Container Registry** (default): `ghcr.io/{owner}/{repo}`
- **Private Registry**: Configure with secrets

## Private Registry Configuration

Add repository secrets:
- `PRIVATE_REGISTRY_URL`: Your registry URL
- `PRIVATE_REGISTRY_USERNAME`: Registry username
- `PRIVATE_REGISTRY_PASSWORD`: Registry password/token
- `PRIVATE_REGISTRY_IMAGE_NAME`: Optional custom image name

## Environment Variables

**Required:**
```bash
NODE_NAME=your-node-name
NODE_PORT=8000
NATS_URL=nats://nats:4222
STREAM_NAME=droq-stream
LOG_LEVEL=INFO
```

**Optional:**
```bash
# Node (NODE_ prefix)
NODE_HEALTH_CHECK_ENABLED=true

# NATS (NATS_ prefix)
NATS_CLIENT_NAME=${NODE_NAME}

# Metrics (METRICS_ prefix)
METRICS_PORT=8081
METRICS_ENABLED=true
```

## Usage

**Docker:**
```bash
docker pull ghcr.io/your-org/your-repo:latest
docker run -p 8080:8000 \
  -e NODE_NAME=my-node \
  -e NATS_URL=nats://localhost:4222 \
  ghcr.io/your-org/your-repo:latest
```

**Kubernetes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: droq-node
spec:
  replicas: 3
  selector:
    matchLabels:
      app: droq-node
  template:
    metadata:
      labels:
        app: droq-node
    spec:
      containers:
      - name: droq-node
        image: ghcr.io/your-org/your-repo:latest
        ports:
        - containerPort: 8000
        env:
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: NODE_PORT
          value: "8000"
        - name: NATS_URL
          value: "nats://nats-service:4222"
        - name: STREAM_NAME
          value: "droq-stream"
        - name: LOG_LEVEL
          value: "INFO"
```

## Features

- Multi-platform builds (amd64, arm64)
- Security scanning with Trivy
- SBOM generation for releases
- Multi-registry support