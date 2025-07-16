# Subdomain Discovery SaaS Service

A FastAPI-based service that discovers subdomains for a given domain name using DNS enumeration.

## Features

- Fast subdomain discovery using DNS lookups
- Concurrent processing for better performance
- RESTful API with proper validation
- Built-in health check endpoint
- Comprehensive error handling

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Usage

### Discover Subdomains

**POST** `/discover`

Request body:
```json
{
  "domain": "example.com"
}
```

Response:
```json
{
  "domain": "example.com",
  "subdomains": [
    "www.example.com",
    "mail.example.com",
    "api.example.com"
  ],
  "total_found": 3
}
```

### Health Check

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "service": "subdomain-discovery"
}
```

## Example Usage

```bash
# Test the service
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "google.com"}'
```

## API Documentation

Once running, visit:
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Notes

- The service uses a predefined list of common subdomains
- DNS lookups are performed concurrently for better performance
- Results include both A and CNAME record discoveries
- Domain validation ensures proper input format