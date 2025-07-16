# Advanced Subdomain Discovery SaaS Service

A comprehensive FastAPI-based service that discovers subdomains using multiple advanced methods including search engines, certificate transparency logs, and DNS enumeration.

## 🚀 Features

- **Multiple Discovery Methods:**
  - DNS enumeration with expanded wordlist
  - Google search engine dorking
  - Bing search engine dorking
  - Certificate Transparency logs (crt.sh)
  - nslookup with zone transfer attempts
- **Concurrent Processing** for maximum speed
- **Method Selection** - choose which discovery methods to use
- **Detailed Results** showing findings per method
- **RESTful API** with comprehensive validation

## 📦 Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
python main.py
```

## 🔧 API Usage

### Discover Subdomains (Advanced)

**POST** `/discover`

Request body:
```json
{
  "domain": "example.com",
  "methods": ["dns", "google", "crt", "nslookup"]
}
```

Available methods:
- `dns` - DNS enumeration using wordlist
- `google` - Google search dorking
- `bing` - Bing search dorking  
- `crt` - Certificate Transparency logs
- `nslookup` - DNS zone transfer and record enumeration

Response:
```json
{
  "domain": "example.com",
  "subdomains": [
    "www.example.com",
    "mail.example.com",
    "api.example.com",
    "blog.example.com"
  ],
  "total_found": 4,
  "methods_used": ["dns", "google", "crt"],
  "results_by_method": {
    "dns": ["www.example.com", "mail.example.com"],
    "google": ["blog.example.com"],
    "crt": ["api.example.com", "www.example.com"]
  }
}
```

### Get Available Methods

**GET** `/methods`

Returns all available discovery methods with descriptions.

### Health Check

**GET** `/health`

## 🧪 Example Usage

### Basic Discovery (All Methods)
```bash
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "google.com"}'
```

### Selective Methods
```bash
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "google.com", "methods": ["crt", "google"]}'
```

### Certificate Transparency Only
```bash
curl -X POST "http://localhost:8000/discover" \
     -H "Content-Type: application/json" \
     -d '{"domain": "facebook.com", "methods": ["crt"]}'
```

## 🌐 API Documentation

Once running, visit:
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔍 Discovery Methods Explained

1. **DNS Enumeration**: Tests common subdomain names against the target domain
2. **Google Dorking**: Uses `site:*.domain.com` to find indexed subdomains
3. **Bing Dorking**: Similar to Google but using Bing search engine
4. **Certificate Transparency**: Queries crt.sh for SSL certificates containing subdomains
5. **nslookup**: Attempts DNS zone transfers and queries various record types

## ⚡ Performance Tips

- Use `["crt"]` method for fastest results with high accuracy
- Combine `["dns", "crt"]` for balanced speed and coverage
- Use all methods `["dns", "google", "bing", "crt", "nslookup"]` for maximum discovery

## 🛡️ Rate Limiting & Ethics

- The service implements reasonable delays for search engines
- Certificate Transparency queries are generally unlimited
- Always ensure you have permission to scan target domains
- Consider implementing rate limiting for production use

## 🚀 Deployment

The service is production-ready and can be deployed to:
- Docker containers
- Cloud platforms (AWS, GCP, Azure)
- Kubernetes clusters
- Traditional VPS/dedicated servers