# Node Configuration Guide

This guide explains how to configure `node.json` for your Droq nodes. All fields are required and serve specific purposes in the Droq ecosystem.

## Overview

`node.json` is a metadata file that describes your node's identity, capabilities, and deployment configuration. It's used for:

- Node registry registration
- Orchestration and service discovery
- Runtime metadata management
- Component discovery and routing

## Required Fields

### Identity Fields

#### `version` (String)
**Purpose**: Semantic version of your node
**Format**: MAJOR.MINOR.PATCH (e.g., "1.0.0")
**Example**:
```json
"version": "1.2.3"
```

#### `node_id` (String)
**Purpose**: Unique identifier matching your repository name
**Format**: Repository name without organization prefix
**Examples**:
```json
"node_id": "my-custom-node"
"node_id": "data-processor-service"
"node_id": "math-executor-node"
```

#### `name` (String)
**Purpose**: Human-readable display name
**Example**:
```json
"name": "My Data Processing Node"
```

#### `description` (String)
**Purpose**: Brief description of what your node does
**Example**:
```json
"description": "Processes incoming data streams and applies transformations"
```

### Runtime Fields (Dynamic)

#### `api_url` (String)
**Purpose**: External API endpoint for your node
**Integration**: Should align with `NODE_PORT` environment variable
**Example**:
```json
"api_url": "http://localhost:8000"
```

#### `ip_address` (String)
**Purpose**: Network location where node is deployed
**Example**:
```json
"ip_address": "127.0.0.1"
```

#### `docker_image` (String)
**Purpose**: Container image reference for deployment
**Format**: `{registry}/{image}:{tag}`
**Examples**:
```json
"docker_image": "myorg/my-node:latest"
"docker_image": "my-node:1.2.3"
```

#### `deployment_location` (String)
**Purpose**: Geographic or logical deployment location
**Examples**:
```json
"deployment_location": "local"
"deployment_location": "on-premise"
```

#### `status` (String)
**Purpose**: Current operational status of the node
**Values**: `"active"`, `"inactive"`, `"maintenance"`, `"error"`
**Example**:
```json
"status": "active"
```

### Metadata Fields

#### `author` (String)
**Purpose**: Creator or organization name
**Example**:
```json
"author": "Droq Team"
"author": "My Company"
"author": "John Doe"
```

#### `created_at` (String)
**Purpose**: Node creation timestamp
**Format**: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
**Example**:
```json
"created_at": "2025-01-15T10:30:00Z"
```

#### `source_code_location` (String)
**Purpose**: Repository URL for source code
**Example**:
```json
"source_code_location": "https://github.com/myorg/my-node"
```

## Component Configuration

Components define the functional capabilities of your node. Each component has a unique path and metadata.

### Component Path Structure



### Component Structure
```json
"components": {
  "ComponentName": {
    "path": "dfx.base-node-template-py.core.main",
    "description": "What this component does",
    "author": "Component author (optional)"
  }
}
```

### Examples

**For node_id: "base-node-template-py"**:
```json
"components": {
  "MainComponent": {
    "path": "myapp.src.core.main",
    "description": "Main entry point for the node",
    "author": "Droq Team"
  },
  "DataProcessor": {
    "path": "myapp.src.processing.transform",
    "description": "Transforms incoming data",
    "author": "Droq Team"
  }
}
```

## Configuration Values

Set your configuration values directly in `node.json`:

```json
{
  "api_url": "http://localhost:8000",
  "ip_address": "127.0.0.1",
  "docker_image": "my-node:latest",
  "deployment_location": "local"
}
```

## Complete Examples

### Example 1: Simple Computational Node

```json
{
  "version": "1.0.0",
  "node_id": "math-calculator",
  "name": "Math Calculator Node",
  "description": "Performs mathematical operations on incoming data",
  "author": "Data Team",
  "api_url": "http://localhost:8000",
  "created_at": "2025-01-15T10:30:00Z",
  "ip_address": "127.0.0.1",
  "status": "active",
  "docker_image": "myorg/math-calculator:1.0.0",
  "deployment_location": "local",
  "source_code_location": "https://github.com/myorg/math-calculator",
  "components": {
    "Calculator": {
      "path": "dfx.math.calculator.core.main",
      "description": "Main calculator component",
      "author": "Data Team"
    }
  }
}
```

### Example 2: Multi-Component Node

```json
{
  "version": "1.0.0",
  "node_id": "data-service",
  "name": "Data Service Node",
  "description": "Provides data processing and validation services",
  "author": "My Team",
  "api_url": "http://localhost:8000",
  "created_at": "2025-01-15T10:30:00Z",
  "ip_address": "127.0.0.1",
  "status": "active",
  "docker_image": "myorg/data-service:latest",
  "deployment_location": "local",
  "source_code_location": "https://github.com/myorg/data-service",
  "components": {
    "Processor": {
      "path": "dfx.data.service.processing.transform",
      "description": "Transforms incoming data",
      "author": "My Team"
    },
    "Validator": {
      "path": "dfx.data.service.utils.validate",
      "description": "Validates data format",
      "author": "My Team"
    }
  }
}
```


## Integration with Docker and Environment Variables

### Port Alignment

Ensure `api_url` matches your `NODE_PORT` environment variable:

```bash
# .env file
NODE_PORT=8080

# node.json file
"api_url": "http://localhost:8080"
```

### Docker Image Reference

The `docker_image` field should match your Docker publishing configuration:

```json
"docker_image": "myorg/my-node:latest"
```

Corresponds to:
```yaml
# GitHub Actions workflow
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}  # myorg/my-node
```

### Environment Variable Integration

Common environment variables that relate to node.json fields:

```bash
# Node identification
NODE_NAME=my-custom-node

# Network configuration
NODE_PORT=8000
API_URL=http://localhost:8000

# Docker configuration
DOCKER_IMAGE=my-custom-node:latest
DEPLOYMENT_LOCATION=local
```

## Validation Checklist

Before deploying, verify your `node.json`:

- [ ] All required fields are present
- [ ] `version` follows semantic versioning (X.Y.Z)
- [ ] `node_id` matches repository name
- [ ] `api_url` is valid URL format
- [ ] Component paths follow `dfx.{node_id}.{category}.{component}` format
- [ ] `created_at` is valid ISO 8601 timestamp
- [ ] `status` is one of: "active", "inactive", "maintenance", "error"
- [ ] Component paths match your actual Python module structure

### JSON Validation

You can validate your JSON using command line:

```bash
# Using python
python -m json.tool node.json

# Using jq
jq . node.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

## Best Practices

1. **Naming Conventions**
   - Use kebab-case for `node_id`
   - Use descriptive names for components
   - Follow semantic versioning

2. **Component Organization**
   - Group related components by category
   - Use clear, descriptive component names
   - Document component responsibilities

3. **Version Management**
   - Update `version` when making changes
   - Tag releases consistently
   - Keep version in sync with Docker tags

4. **Configuration**
   - Validate JSON format before deployment
   - Keep configuration in version control
   - Test configuration changes before deployment