# Docker Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- Caddy network already created (`caddy_network`)
- Gemini API key available

## Setup Instructions

### 1. Environment Configuration
Copy `.env.example` to `.env` and add your Gemini API key:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Build and Start Services
```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Caddy Configuration
To route traffic from `text2json.haguma.com` to the Nginx container, add this to your Caddyfile:

```
text2json.haguma.com {
    reverse_proxy text2json_nginx:80
}
```

Then reload Caddy:
```bash
docker-compose -f <your-caddy-compose> reload
# or if Caddy is running directly:
caddy reload
```

## Architecture

```
Caddy (text2json.haguma.com:443)
    ↓
Nginx (text2json_nginx:80)
    ├─→ Static files (/index.html, CSS, JS)
    └─→ Reverse proxy /api/* → Backend (text2json_backend:8000)
```

## API Endpoints

All API requests should use `/api/` prefix:
- `POST /api/extract` - Extract structured data from text
- `POST /api/prompt` - Get the prompt that will be sent to Gemini
- `GET /api/health` - Health check

## Troubleshooting

### Check service status
```bash
docker-compose ps
```

### View backend logs
```bash
docker-compose logs backend
```

### View Nginx logs
```bash
docker-compose logs nginx
```

### Test API connectivity
```bash
curl http://localhost:8080/api/health
```

### Rebuild after code changes
```bash
docker-compose up -d --build
```

## Performance Notes

- **Nginx image**: `nginx:alpine` (~42MB) - lightweight and efficient
- **Python image**: `python:3.11-slim` (~150MB) - minimal dependencies
- **Multi-stage build**: Reduces final image size by excluding build tools
- **Gzip compression**: Enabled in Nginx for faster content delivery
- **Health checks**: Configured for both services to ensure reliability

## Security Notes

- API key is passed via environment variable
- Static files are served as read-only (`ro`)
- Nginx runs with minimal privileges
- Container names are namespaced to avoid conflicts
