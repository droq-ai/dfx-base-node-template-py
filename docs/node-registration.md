# Node Registration Guide

This guide explains how to register your Droq node in the official droq-node-registry so it can be discovered by other users on [directory.droq.ai](https://directory.droq.ai).

## Overview

The droq-node-registry uses Git submodules to organize and manage registered nodes. Each node is added as a submodule under the `/nodes` directory, making it easy to maintain version control and updates.

## Prerequisites

Before registering your node, ensure you have:

### Development Requirements
- [x] Node development completed and tested
- [x] Docker image built and published to a registry
- [x] `node.json` file properly configured and validated
- [x] Source code pushed to a public GitHub repository

### node.json Requirements
- All required fields completed
- Correct semantic version (e.g., "1.0.0")
- Accurate `node_id` matching your repository name
- Valid `api_url` and `docker_image` references
- Proper timestamp in `created_at` field
- Complete component definitions

### Git Requirements
- GitHub account with access to your node repository
- Git installed locally
- Fork permissions on droq-node-registry repository

## Registration Process

### Step 1: Fork the Registry Repository

1. Visit [https://github.com/droq-ai/droq-node-registry](https://github.com/droq-ai/droq-node-registry)
2. Click "Fork" to create your personal copy
3. Note your fork URL: `https://github.com/YOUR_USERNAME/droq-node-registry`

### Step 2: Clone Your Fork

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/droq-node-registry.git
cd droq-node-registry

# Add upstream remote (optional, for keeping updated)
git remote add upstream https://github.com/droq-ai/droq-node-registry.git
```

### Step 3: Add Your Node as Submodule

Navigate to the nodes directory and add your node as a submodule:

```bash
cd nodes

# Add your node repository as submodule
# Replace {your-node-id} with your actual node_id from node.json
git submodule add https://github.com/YOUR_USERNAME/YOUR_NODE_REPOSITORY.git {your-node-id}

# Example:
# git submodule add https://github.com/johndoe/my-data-processor.git my-data-processor
```

### Step 4: Verify Submodule Configuration

Check that the submodule was added correctly:

```bash
# List submodules
git submodule status

# Should show your node with commit hash
#  a1b2c3d4 nodes/{your-node-id} (heads/main)
```

### Step 5: Commit and Push Changes

```bash
# Go back to repository root
cd ..

# Stage and commit the submodule addition
git add nodes/{your-node-id} .gitmodules
git commit -m "Add {node-name} node"

# Push to your fork
git push origin main
```

### Step 6: Create Pull Request

1. Visit your fork on GitHub
2. Click "Contribute" → "Open pull request"
3. Target branch: `main` (in droq-ai/droq-node-registry)
4. Fill in the pull request details (see PR Requirements below)

## Pull Request Requirements

### PR Title Format
```
Add {node-name} node
```

### PR Description Template

```markdown
## Node Information
- **Node ID**: {your-node-id}
- **Node Name**: {node-name from node.json}
- **Description**: {brief description from node.json}
- **Version**: {version from node.json}

## Docker Image
- **Registry**: {docker registry (e.g., ghcr.io, docker.io)}
- **Image**: {full image name with tag}
- **Source**: Link to node repository

## Components
{List main components from node.json}

## Testing
- [ ] Node builds and runs successfully
- [ ] Docker image is accessible
- [ ] node.json is valid and complete
- [ ] All components are properly defined

## Additional Notes
{Any additional information about the node}
```

## Submodule Management

### Using Specific Version/Tag

To register a specific version of your node instead of the latest commit:

```bash
# Navigate to the submodule directory
cd nodes/{your-node-id}

# Checkout specific tag or commit
git checkout v1.0.0  # or specific commit hash

# Go back to registry root and commit the version lock
cd ../..
git add nodes/{your-node-id}
git commit -m "Update {node-name} to v1.0.0"
```

### Updating Existing Node Registration

When you release a new version:

```bash
# Navigate to the submodule
cd nodes/{your-node-id}

# Pull latest changes or checkout new tag
git pull origin main
# OR: git checkout v2.0.0

# Go back to registry root
cd ..

# Stage and commit the update
git add nodes/{your-node-id}
git commit -m "Update {node-name} to {new-version}"
git push origin main

# Create PR for the update
```

### Removing a Node (for maintenance)

```bash
# Remove submodule
git submodule deinit -f nodes/{your-node-id}
git rm -f nodes/{your-node-id}
rm -rf .git/modules/nodes/{your-node-id}

# Commit the removal
git commit -m "Remove {node-name} node"
```

## Review Process

### Automated Checks
- Submodule points to valid repository
- node.json file exists and is valid JSON
- Basic field validation in node.json

### Manual Review
The Droq team will review:
- Node functionality and purpose
- Code quality and documentation
- Security considerations
- Integration with Droq ecosystem

### Approval and Merge
- Once approved, PR will be merged into main registry
- Your node will be automatically discovered and indexed
- Node appears on [directory.droq.ai](https://directory.droq.ai) after processing

## [directory.droq.ai](https://directory.droq.ai) Integration

After your node is registered and merged:

### Discovery Process
- Registry is periodically scanned for new nodes
- Each node's `node.json` is parsed and indexed
- Components are extracted and categorized
- Docker images are validated for accessibility

### What Users See
- **Node Name**: From `name` field in node.json
- **Description**: From `description` field
- **Author**: From `author` field
- **Version**: From `version` field
- **Components**: List of available components
- **Repository**: Link to source code
- **Docker Image**: Image reference for deployment

### Updates and Maintenance
- Node information updates when registry submodule is updated
- Version changes are reflected automatically
- Component additions/updates appear after next scan

## Troubleshooting

### Common Issues

**Submodule shows as empty:**
```bash
# Initialize and update submodules
git submodule update --init --recursive
```

**Wrong commit/branch in submodule:**
```bash
# Navigate to submodule and fix
cd nodes/{your-node-id}
git checkout main  # or specific tag
cd ../..
git add nodes/{your-node-id}
git commit -m "Fix submodule reference"
```

**PR not showing submodule changes:**
- Ensure `.gitmodules` file is staged
- Verify the submodule directory is tracked
- Check that changes are committed, not just staged

**node.json validation errors:**
- Validate JSON format: `python -m json.tool node.json`
- Check all required fields are present
- Verify URL formats and timestamp format

**Docker image not accessible:**
- Verify image exists in registry
- Check repository permissions (public vs private)
- Test image pull: `docker pull your-image:tag`

### Getting Help

- **Registry Issues**: Open issue in droq-node-registry repository
- **Node Development**: Refer to the node template documentation
- **Directory Listings**: Contact Droq team through official channels

## Best Practices

### Before Registration
- Test your node thoroughly
- Validate node.json format
- Ensure Docker image is accessible
- Document components clearly
- Use semantic versioning

### Submodule Management
- Use specific tags for releases instead of latest commits
- Keep submodule references up to date
- Update node.json when changing versions
- Document breaking changes in releases

### PR Process
- Provide clear, detailed PR descriptions
- Include testing status
- Respond to review feedback promptly
- Follow established naming conventions

### Maintenance
- Update registration when releasing new versions
- Monitor for issues or questions on your repository
- Keep documentation current
- Participate in Droq community discussions

## Example: Complete Registration Flow

Here's a complete example for registering a node called "my-processor":

```bash
# 1. Fork and clone registry
git clone https://github.com/johndoe/droq-node-registry.git
cd droq-node-registry

# 2. Add node as submodule
cd nodes
git submodule add https://github.com/johndoe/my-processor.git my-processor

# 3. Lock to specific version
cd my-processor
git checkout v1.0.0
cd ../..

# 4. Commit changes
git add nodes/my-processor .gitmodules
git commit -m "Add My Processor node"
git push origin main

# 5. Create PR on GitHub
# (Visit your fork and open pull request)
```

Your node will now be reviewed and, once approved, will appear on [directory.droq.ai](https://directory.droq.ai) for other users to discover and use.