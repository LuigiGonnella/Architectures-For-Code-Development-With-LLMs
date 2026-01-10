# Docker Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- (Optional) Ollama running on host if using local models

## Quick Start

### 1. Setup Environment Variables
```bash
cd single_agent_webapp/utils
cp .env.example .env
# Edit .env and set your API keys and model preferences
```

### 2. Build and Run with Docker Compose
```bash
# From the utils directory
docker-compose up --build
```

Or from the project root:
```bash
cd single_agent_webapp/utils
docker-compose up --build
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Using Ollama with Docker

If you're running Ollama on your host machine, the containers need to connect to it:

### Windows/Mac (Docker Desktop)
Use `host.docker.internal` to connect to host:
```yaml
# In docker-compose.yml, add to backend environment:
environment:
  - OLLAMA_HOST=http://host.docker.internal:11434
```

### Linux
Use the host network or add extra_hosts:
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

## Docker Commands

### Start services
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop services
```bash
docker-compose down
```

### Rebuild after changes
```bash
docker-compose up --build
```

### Remove all containers and volumes
```bash
docker-compose down -v
```

## Production Deployment

For production, consider:
1. Using environment-specific `.env` files
2. Setting up reverse proxy (nginx)
3. Enabling HTTPS
4. Using production-grade WSGI server settings
5. Implementing proper logging and monitoring

## Troubleshooting

### Cannot connect to Ollama
- Ensure Ollama is running on the host
- Use correct host address (host.docker.internal or container network)
- Check firewall settings

### Build fails
- Ensure you're running from the correct directory
- Check Docker has enough disk space
- Verify all files are present in the context

### Port conflicts
- Check if ports 3000 or 8000 are already in use
- Modify port mappings in docker-compose.yml if needed
